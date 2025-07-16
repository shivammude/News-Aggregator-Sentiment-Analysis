from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import logging

from database import Database
from scraper import NewsScraper
from sentiment_analyzer import SentimentAnalyzer
from models import NewsArticle, SentimentStats, ScrapingStatus
from config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
db = Database()
scraper = NewsScraper()
sentiment_analyzer = SentimentAnalyzer()

# App lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting News Aggregator API...")
    await db.connect()
    asyncio.create_task(periodic_scraping())
    yield
    logger.info("Shutting down News Aggregator API...")
    await scraper.close()
    await db.disconnect()

# FastAPI app
app = FastAPI(
    title="News Aggregator Sentiment Analysis API",
    description="API for scraping news articles and analyzing sentiment",
    version="1.0.0",
    lifespan=lifespan
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Background task for periodic scraping
async def periodic_scraping():
    while True:
        try:
            logger.info("Starting periodic news scraping...")
            await scrape_and_analyze_news()
            logger.info("Periodic scraping completed")
        except Exception as e:
            logger.error(f"Error in periodic scraping: {e}")
        await asyncio.sleep(settings.scraping_interval_minutes * 60)

# Core function to scrape and analyze
async def scrape_and_analyze_news():
    try:
        articles = await scraper.scrape_all_sources()
        if not articles:
            logger.warning("No articles scraped.")
            return []

        for article in articles:
            sentiment_data = sentiment_analyzer.analyze(article.content or article.summary)
            article.sentiment = sentiment_data['sentiment']
            article.sentiment_score = sentiment_data['score']

        await db.save_articles(articles)
        logger.info(f"Scraped and analyzed {len(articles)} articles")
        return articles
    except Exception as e:
        logger.error(f"Error in scrape_and_analyze_news: {e}")
        return []

# Routes
@app.get("/")
async def root():
    return {"message": "News Aggregator Sentiment Analysis API", "status": "running"}

@app.get("/api/articles", response_model=list[NewsArticle])
async def get_articles(limit: int = 50, sentiment: str = "all", source: str = "all", category: str = "all", search: str = ""):
    try:
        return await db.get_articles(
            limit=limit,
            sentiment=None if sentiment == "all" else sentiment,
            source=None if source == "all" else source,
            category=None if category == "all" else category,
            search=None if not search else search
        )
    except Exception as e:
        logger.error(f"Error getting articles: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch articles")

@app.get("/api/sentiment-stats", response_model=SentimentStats)
async def get_sentiment_stats():
    try:
        return await db.get_sentiment_stats()
    except Exception as e:
        logger.error(f"Error getting sentiment stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch sentiment statistics")

@app.get("/api/sources")
async def get_sources():
    try:
        return {"sources": await db.get_unique_sources()}
    except Exception as e:
        logger.error(f"Error getting sources: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch sources")

@app.get("/api/categories")
async def get_categories():
    try:
        return {"categories": await db.get_unique_categories()}
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch categories")

@app.post("/api/scrape")
async def trigger_scraping(background_tasks: BackgroundTasks):
    background_tasks.add_task(scrape_and_analyze_news)
    return {"message": "Scraping started in background", "status": "triggered"}

@app.get("/api/scraping-status", response_model=ScrapingStatus)
async def get_scraping_status():
    try:
        return await db.get_scraping_status()
    except Exception as e:
        logger.error(f"Error getting scraping status: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch scraping status")

@app.delete("/api/articles")
async def clear_articles():
    try:
        await db.clear_articles()
        return {"message": "All articles cleared"}
    except Exception as e:
        logger.error(f"Error clearing articles: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear articles")

@app.post("/api/scrape-cnn")
async def scrape_cnn():
    try:
        cnn_config = settings.news_sources[2]  # CNN config
        articles = await scraper.scrape_source(cnn_config)

        if not articles:
            return {"message": "No articles scraped for CNN."}

        for article in articles:
            sentiment_data = sentiment_analyzer.analyze(article.content or article.summary)
            article.sentiment = sentiment_data['sentiment']
            article.sentiment_score = sentiment_data['score']

        await db.save_articles(articles)
        return {"message": f"{len(articles)} CNN articles scraped and saved."}

    except Exception as e:
        logger.error(f"Error scraping CNN: {e}")
        raise HTTPException(status_code=500, detail="Failed to scrape CNN.")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
