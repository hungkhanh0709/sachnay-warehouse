"""
SachDonga.vn scraper implementation.
"""

import time
from typing import Dict, Any, List
from bs4 import BeautifulSoup

from core.base_scraper import BaseScraper
from utils import TextUtils, URLUtils


class SachDongaScraper(BaseScraper):
    """Scraper for sachdonga.vn"""
    
    def __init__(self):
        super().__init__("sachdonga.vn")
    
    def build_page_url(self, page: int) -> str:
        """Build URL for a specific page number."""
        list_page_url = self.website_config.get("list_page_url", "/collections/sachmoi")
        return f"{self.base_url}{list_page_url}?page={page}"
    
    def find_book_elements(self, soup: BeautifulSoup) -> List:
        """Find book container elements on the page."""
        selector = self.website_config.get("selectors", {}).get("product_container", "div.product-item")
        return soup.find_all('div', class_='product-item')
    
    def extract_book_info(self, element, fetch_details: bool = False) -> Dict[str, Any]:
        """Extract book information from a product element."""
        try:
            selectors = self.website_config.get("selectors", {})
            
            # Extract title
            title_elem = element.find('div', class_='product-title')
            if title_elem:
                title_link = title_elem.find('a')
                title = TextUtils.clean_text(title_link.get_text()) if title_link else ""
            else:
                title = ""
            
            # Standardize the title
            title = TextUtils.standardize_title(title)
            
            # Extract author - sachdonga doesn't have author info in the grid
            author = ""
            
            # Extract price
            price_elem = element.find('span', class_='current-price')
            price = TextUtils.extract_price(price_elem.get_text()) if price_elem else ""
            
            # Extract image URL
            img_elem = element.find('img')
            image_url = ""
            if img_elem:
                image_url = img_elem.get('src') or img_elem.get('data-src', '')
                image_url = URLUtils.normalize_url(image_url, self.base_url)
            
            # Extract product URL
            link_elem = element.find('a')
            product_url = ""
            if link_elem:
                product_url = link_elem.get('href', '')
                product_url = URLUtils.normalize_url(product_url, self.base_url)
            
            # Fetch detailed information if requested
            if fetch_details and product_url:
                details = self.scrape_book_details(product_url)
                if details.get('title'):
                    title = TextUtils.standardize_title(details['title'])
                if details.get('author'):
                    author = details['author']
            
            if title:  # Only return if we have at least a title
                return {
                    'title': title,
                    'author': author,
                    'price': price,
                    'image_url': image_url,
                    'product_url': product_url,
                    'source': self.source_name,
                    'scraped_date': time.strftime('%Y-%m-%d %H:%M:%S')
                }
        
        except Exception as e:
            self.logger.error(f"Error extracting book info: {e}")
        
        return None
    
    def extract_book_details(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract detailed book information from sachdonga.vn detail page."""
        details = {"title": "", "author": "", "description": ""}
        
        try:
            selectors = self.website_config.get("selectors", {})
            
            # Extract full title from h1
            title_elem = soup.select_one(selectors.get("detail_title", "h1"))
            if title_elem:
                details['title'] = TextUtils.clean_text(title_elem.get_text())
            
            # Extract author using configured patterns
            product_content = soup.select_one(selectors.get("product_content", ".product-content"))
            if product_content:
                content_text = product_content.get_text()
                author_patterns = selectors.get("detail_author_patterns", [])
                author = TextUtils.extract_author_from_text(content_text, author_patterns)
                if author:
                    details['author'] = author
            
            # Extract description
            if product_content:
                desc_text = TextUtils.clean_text(product_content.get_text())
                details['description'] = desc_text[:500]  # Limit description length
        
        except Exception as e:
            self.logger.error(f"Error extracting book details: {e}")
        
        return details