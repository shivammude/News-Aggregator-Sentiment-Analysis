from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class NewsArticle(BaseModel):
    id: Optional[str] = None
    title: str
    summary: Optional[str] = None
    content: Optional[str] = None
    url: str
    source: str
    author: Optional[str] = None
    published_at: datetime = Field(default_factory=datetime.now)
    sentiment: SentimentType
    sentiment_score: float
    category: str
    image_url: Optional[str] = None
    read_time: int = 5
    scraped_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SentimentStats(BaseModel):
    positive: int = 0
    negative: int = 0
    neutral: int = 0
    total: int = 0

class ScrapingStatus(BaseModel):
    last_scrape: Optional[datetime] = None
    articles_scraped: int = 0
    sources_active: int = 0
    status: str = "idle"
    next_scrape: Optional[datetime] = None

class NewsSource(BaseModel):
    id: str
    name: str
    domain: str
    credibility: float
    logo: str

class SelectorConfig(BaseModel):
    articles: str
    title: str
    link: str
    summary: Optional[str] = ""

class SourceConfig(BaseModel):
    name: str
    url: str
    category: str
    selectors: Optional[SelectorConfig] = None  
    
