import asyncio
import aiohttp
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import logging
from typing import List, Optional
from urllib.parse import urljoin, urlparse

from models import NewsArticle, SentimentType, SourceConfig
from config import settings

logger = logging.getLogger(__name__)

class NewsScraper:
    def __init__(self):
        self.session = None
        self.driver = None

    async def get_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            )
        return self.session

    def get_driver(self):
        if not self.driver:
            try:
                options = Options()
                if settings.headless_browser:
                    options.add_argument("--headless=new")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")

                service = Service("C:/Windows/chromedriver.exe")
                self.driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                logger.error(f"Failed to initialize Chrome driver: {e}")
                return None
        return self.driver

    async def scrape_with_requests(self, source_config: SourceConfig) -> List[NewsArticle]:
        articles = []
        try:
            session = await self.get_session()
            async with session.get(source_config.url) as response:
                if response.status != 200:
                    logger.warning(f"Failed to fetch {source_config.name}: {response.status}")
                    return articles

                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                elements = soup.select(source_config.selectors.articles)

                for element in elements[:settings.max_articles_per_source]:
                    try:
                        article = await self.extract_article_data(element, source_config)
                        if article:
                            articles.append(article)
                    except Exception as e:
                        logger.error(f"Error extracting article from {source_config.name}: {e}")
        except Exception as e:
            logger.error(f"Error scraping {source_config.name} with requests: {e}")
        return articles

    def scrape_with_selenium(self, source_config: SourceConfig) -> List[NewsArticle]:
        articles = []
        driver = self.get_driver()
        if not driver:
            return articles

        try:
            driver.get(source_config.url)
            WebDriverWait(driver, settings.selenium_timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, source_config.selectors.articles))
            )

            elements = driver.find_elements(By.CSS_SELECTOR, source_config.selectors.articles)
            for element in elements[:settings.max_articles_per_source]:
                try:
                    article = self.extract_article_data_selenium(element, source_config)
                    if article:
                        articles.append(article)
                except Exception as e:
                    logger.error(f"Error extracting article from {source_config.name}: {e}")
        except Exception as e:
            logger.error(f"Error scraping {source_config.name} with Selenium: {e}")
        return articles

    async def extract_article_data(self, element, source_config: SourceConfig) -> Optional[NewsArticle]:
        try:
            title_el = element.select_one(source_config.selectors.title)
            if not title_el:
                return None
            title = title_el.get_text(strip=True)

            link_el = element.select_one(source_config.selectors.link)
            url = link_el.get("href") if link_el else ""

            if url.startswith("/"):
                base_url = f"{urlparse(source_config.url).scheme}://{urlparse(source_config.url).netloc}"
                url = urljoin(base_url, url)

            summary = ""
            if source_config.selectors.summary:
                summary_el = element.select_one(source_config.selectors.summary)
                if summary_el:
                    summary = summary_el.get_text(strip=True)

            img_el = element.select_one("img")
            image_url = img_el.get("src") or img_el.get("data-src") if img_el else None
            if image_url and image_url.startswith("/"):
                base_url = f"{urlparse(source_config.url).scheme}://{urlparse(source_config.url).netloc}"
                image_url = urljoin(base_url, image_url)

            return NewsArticle(
                title=title,
                summary=summary,
                url=url,
                source=source_config.name,
                category=source_config.category,
                image_url=image_url,
                sentiment=SentimentType.NEUTRAL,
                sentiment_score=0.0,
                read_time=self.estimate_read_time(summary),
                published_at=datetime.now()
            )
        except Exception as e:
            logger.error(f"Error extracting article data: {e}")
            return None

    def extract_article_data_selenium(self, element, source_config: SourceConfig) -> Optional[NewsArticle]:
        try:
            title_el = element.find_element(By.CSS_SELECTOR, source_config.selectors.title)
            title = title_el.text.strip()

            link_el = element.find_element(By.CSS_SELECTOR, source_config.selectors.link)
            url = link_el.get_attribute("href") if link_el else ""

            summary = ""
            if source_config.selectors.summary:
                try:
                    summary_el = element.find_element(By.CSS_SELECTOR, source_config.selectors.summary)
                    summary = summary_el.text.strip()
                except:
                    pass

            image_url = None
            try:
                img_el = element.find_element(By.CSS_SELECTOR, "img")
                image_url = img_el.get_attribute("src") or img_el.get_attribute("data-src")
            except:
                pass

            return NewsArticle(
                title=title,
                summary=summary,
                url=url,
                source=source_config.name,
                category=source_config.category,
                image_url=image_url,
                sentiment=SentimentType.NEUTRAL,
                sentiment_score=0.0,
                read_time=self.estimate_read_time(summary),
                published_at=datetime.now()
            )
        except Exception as e:
            logger.error(f"Error extracting article data with Selenium: {e}")
            return None

    def estimate_read_time(self, text: str) -> int:
        if not text:
            return 1
        return max(1, round(len(text.split()) / 200))

    async def scrape_source(self, source_config: SourceConfig) -> List[NewsArticle]:
        logger.info(f"Scraping {source_config.name}...")
        articles = await self.scrape_with_requests(source_config)

        if not articles:
            logger.warning(f"No articles scraped from {source_config.name} using requests.")
            logger.info(f"Trying Selenium for {source_config.name}")
            articles = self.scrape_with_selenium(source_config)
            
        logger.info(f"{source_config.name}: Scraped {len(articles)} articles.")
        return articles

    async def scrape_all_sources(self) -> List[NewsArticle]:
        all_articles = []
        tasks = [self.scrape_source(source) for source in settings.news_sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, list):
                all_articles.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Scraping task failed: {result}")

        logger.info(f"Total articles scraped: {len(all_articles)}")
        return all_articles

    async def close(self):
        if self.session:
            await self.session.close()
        if self.driver:
            self.driver.quit()

    def __del__(self):
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
