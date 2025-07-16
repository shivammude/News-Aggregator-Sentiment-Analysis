import motor.motor_asyncio
from pymongo import ASCENDING, DESCENDING
from datetime import datetime, timedelta
from typing import List, Optional
import logging
from bson import ObjectId

from models import NewsArticle, SentimentStats, ScrapingStatus
from config import settings

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.articles_collection = None
        self.status_collection = None

    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
            self.db = self.client[settings.database_name]
            self.articles_collection = self.db.articles
            self.status_collection = self.db.scraping_status
            
            # Create indexes
            await self.articles_collection.create_index([("url", ASCENDING)], unique=True)
            await self.articles_collection.create_index([("published_at", DESCENDING)])
            await self.articles_collection.create_index([("sentiment", ASCENDING)])
            await self.articles_collection.create_index([("source", ASCENDING)])
            await self.articles_collection.create_index([("category", ASCENDING)])
            
            logger.info("Connected to MongoDB successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            # Fallback to in-memory storage for development
            self.articles_data = []
            self.use_memory = True

    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()

    async def save_articles(self, articles: List[NewsArticle]):
        """Save articles to database"""
        if not articles:
            return
        
        try:
            if hasattr(self, 'use_memory'):
                # In-memory storage fallback
                for article in articles:
                    article.id = str(len(self.articles_data))
                    self.articles_data.append(article.dict())
                return
            
            # MongoDB storage
            for article in articles:
                article_dict = article.dict()
                article_dict.pop('id', None)  # Remove id for upsert
                
                await self.articles_collection.update_one(
                    {"url": article.url},
                    {"$set": article_dict},
                    upsert=True
                )
            
            # Update scraping status
            await self.status_collection.update_one(
                {"_id": "scraping_status"},
                {
                    "$set": {
                        "last_scrape": datetime.now(),
                        "articles_scraped": len(articles),
                        "status": "completed"
                    }
                },
                upsert=True
            )
            
            logger.info(f"Saved {len(articles)} articles to database")
            
        except Exception as e:
            logger.error(f"Error saving articles: {e}")

    async def get_articles(
        self,
        limit: int = 50,
        sentiment: Optional[str] = None,
        source: Optional[str] = None,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[NewsArticle]:
        """Get filtered articles from database"""
        try:
            if hasattr(self, 'use_memory'):
                # In-memory storage fallback
                articles = self.articles_data.copy()
                
                # Apply filters
                if sentiment:
                    articles = [a for a in articles if a['sentiment'] == sentiment]
                if source:
                    articles = [a for a in articles if a['source'] == source]
                if category:
                    articles = [a for a in articles if a['category'] == category]
                if search:
                    search_lower = search.lower()
                    articles = [a for a in articles if 
                              search_lower in a['title'].lower() or 
                              search_lower in (a.get('summary', '') or '').lower()]
                
                # Sort by published_at descending and limit
                articles = sorted(articles, key=lambda x: x['published_at'], reverse=True)[:limit]
                
                # Convert to NewsArticle objects
                result = []
                for article_dict in articles:
                    article_dict['id'] = str(article_dict.get('id', ''))
                    result.append(NewsArticle(**article_dict))
                
                return result
            
            # MongoDB query
            query = {}
            if sentiment:
                query['sentiment'] = sentiment
            if source:
                query['source'] = source
            if category:
                query['category'] = category
            if search:
                query['$or'] = [
                    {'title': {'$regex': search, '$options': 'i'}},
                    {'summary': {'$regex': search, '$options': 'i'}},
                    {'content': {'$regex': search, '$options': 'i'}}
                ]
            
            cursor = self.articles_collection.find(query).sort('published_at', DESCENDING).limit(limit)
            articles = []
            
            async for doc in cursor:
                doc['id'] = str(doc['_id'])
                doc.pop('_id')
                articles.append(NewsArticle(**doc))
            
            return articles
            
        except Exception as e:
            logger.error(f"Error getting articles: {e}")
            return []

    async def get_sentiment_stats(self) -> SentimentStats:
        """Get sentiment statistics"""
        try:
            if hasattr(self, 'use_memory'):
                # In-memory storage fallback
                stats = SentimentStats()
                for article in self.articles_data:
                    sentiment = article['sentiment']
                    if sentiment == 'positive':
                        stats.positive += 1
                    elif sentiment == 'negative':
                        stats.negative += 1
                    elif sentiment == 'neutral':
                        stats.neutral += 1
                    stats.total += 1
                return stats
            
            # MongoDB aggregation
            pipeline = [
                {
                    '$group': {
                        '_id': '$sentiment',
                        'count': {'$sum': 1}
                    }
                }
            ]
            
            stats = SentimentStats()
            async for doc in self.articles_collection.aggregate(pipeline):
                sentiment = doc['_id']
                count = doc['count']
                
                if sentiment == 'positive':
                    stats.positive = count
                elif sentiment == 'negative':
                    stats.negative = count
                elif sentiment == 'neutral':
                    stats.neutral = count
                
                stats.total += count
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting sentiment stats: {e}")
            return SentimentStats()

    async def get_unique_sources(self) -> List[str]:
        """Get unique news sources"""
        try:
            if hasattr(self, 'use_memory'):
                sources = list(set(article['source'] for article in self.articles_data if article.get('source')))
            else:
                sources = await self.articles_collection.distinct('source')
                sources = [src for src in sources if src]  # filter out None or empty

            return sorted(sources)  # consistent sorted list

            
        except Exception as e:
            logger.error(f"Error getting sources: {e}")
            return []

    async def get_unique_categories(self) -> List[str]:
        """Get unique categories"""
        try:
            if hasattr(self, 'use_memory'):
                return list(set(article['category'] for article in self.articles_data))
            
            categories = await self.articles_collection.distinct('category')
            return categories
            
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
            return []

    async def get_scraping_status(self) -> ScrapingStatus:
        """Get scraping status"""
        try:
            if hasattr(self, 'use_memory'):
                return ScrapingStatus(
                    last_scrape=datetime.now() - timedelta(minutes=5),
                    articles_scraped=len(self.articles_data),
                    sources_active=4,
                    status="completed"
                )
            
            doc = await self.status_collection.find_one({"_id": "scraping_status"})
            if doc:
                doc.pop('_id')
                return ScrapingStatus(**doc)
            else:
                return ScrapingStatus()
                
        except Exception as e:
            logger.error(f"Error getting scraping status: {e}")
            return ScrapingStatus()

    async def clear_articles(self):
        """Clear all articles"""
        try:
            if hasattr(self, 'use_memory'):
                self.articles_data.clear()
                return
            
            await self.articles_collection.delete_many({})
            logger.info("Cleared all articles from database")
            
        except Exception as e:
            logger.error(f"Error clearing articles: {e}")