from pydantic_settings import BaseSettings
from typing import List
from pydantic import Field
from models import SourceConfig, SelectorConfig

class Settings(BaseSettings):
    mongodb_url: str = Field(default="mongodb://localhost:27017", alias="MONGO_URI")
    database_name: str = Field(default="news_aggregator", alias="DATABASE_NAME")

    scraping_interval_minutes: int = 30
    max_articles_per_source: int = 20

    news_sources: List[SourceConfig] = [
        SourceConfig(
            name="Times of India",
            url="https://timesofindia.indiatimes.com",
            selectors=SelectorConfig(
                articles="figure",
                title="figcaption",
                link="a",
                summary=""
            ),
            category="General"
        ),
        SourceConfig(
            name="NDTV",
            url="https://www.ndtv.com/latest",
            selectors=SelectorConfig(
                articles="div.NwsLstPg-a",
                title="a.NwsLstPg_ttl-lnk",
                link="a.NwsLstPg_img",
                summary="p.NwsLstPg_txt"
            ),
            category="General"
        ),
        SourceConfig(
            name="CNN",
            url="https://edition.cnn.com/health",
            selectors=SelectorConfig(
                articles="div.container__item",
                title="span.container__headline-text",
                link="a",
                summary=""
            ),
            category="Health",
            
        ),
        SourceConfig(
            name="NY Times",
            url="https://www.nytimes.com/international/section/technology",
            selectors=SelectorConfig(
                articles="article.css-1l4spti",
                title="a.css-8hzhxf",
                link="a.css-8hzhxf",
                summary="a.css-8hzhxf"
            ),
            category="Tech",
             
        )
    ]

    selenium_timeout: int = 10
    headless_browser: bool = True

    class Config:
        env_file = ".env"
        extra = "forbid"

settings = Settings()
