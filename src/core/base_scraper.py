"""
Base scraper class for all website scrapers.
"""

import requests
from bs4 import BeautifulSoup
import logging
import time
from typing import List, Dict, Any
from abc import ABC, abstractmethod

from config import config
from utils import TextUtils, URLUtils, DelayUtils


class BaseScraper(ABC):
    """Abstract base class for book scrapers."""
    
    def __init__(self, website_key: str):
        self.website_config = config.get_website_config(website_key)
        self.base_url = self.website_config.get("base_url", "")
        self.source_name = self.website_config.get("source_name", website_key)
        
        # Set up HTTP session
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.get("user_agent")
        })
        
        # Set up logging
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def fetch_page(self, url: str, max_retries: int = None) -> BeautifulSoup:
        """Fetch and parse a web page."""
        max_retries = max_retries or config.get("scraping.max_retries", 3)
        timeout = config.get("scraping.timeout", 30)
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=timeout)
                response.raise_for_status()
                return BeautifulSoup(response.content, 'html.parser')
            except requests.RequestException as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
    
    def scrape_books(self, max_pages: int = None, fetch_details: bool = None) -> List[Dict[str, Any]]:
        """Scrape books from the source."""
        max_pages = max_pages or config.get("scraping.max_pages", 5)
        fetch_details = fetch_details if fetch_details is not None else config.get("scraping.fetch_details", False)
        
        books = []
        
        for page in range(1, max_pages + 1):
            try:
                url = self.build_page_url(page)
                self.logger.info(f"Scraping {url}")
                
                soup = self.fetch_page(url)
                book_elements = self.find_book_elements(soup)
                
                if not book_elements:
                    self.logger.warning(f"No books found on page {page}")
                    break
                
                page_books = []
                for element in book_elements:
                    book = self.extract_book_info(element, fetch_details=fetch_details)
                    if book:
                        page_books.append(book)
                        books.append(book)
                
                self.logger.info(f"Found {len(book_elements)} book elements, extracted {len(page_books)} books on page {page}")
                
                # Delay between pages
                DelayUtils.sleep_with_jitter(config.get("scraping.delay_between_requests", 1.0))
                
            except Exception as e:
                self.logger.error(f"Error scraping page {page}: {e}")
                break
        
        return books
    
    def scrape_book_details(self, product_url: str) -> Dict[str, str]:
        """Scrape detailed information from a book's detail page."""
        try:
            soup = self.fetch_page(product_url)
            return self.extract_book_details(soup)
        except Exception as e:
            self.logger.warning(f"Failed to scrape details from {product_url}: {e}")
            return {"title": "", "author": "", "description": ""}
    
    @abstractmethod
    def build_page_url(self, page: int) -> str:
        """Build URL for a specific page number."""
        pass
    
    @abstractmethod
    def find_book_elements(self, soup: BeautifulSoup) -> List:
        """Find book container elements on the page."""
        pass
    
    @abstractmethod
    def extract_book_info(self, element, fetch_details: bool = False) -> Dict[str, Any]:
        """Extract book information from a product element."""
        pass
    
    @abstractmethod
    def extract_book_details(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract detailed book information from detail page."""
        pass