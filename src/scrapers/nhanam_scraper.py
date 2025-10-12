"""
NhaNam.vn scraper implementation.
"""

import re
import time
from typing import Dict, Any, List
from bs4 import BeautifulSoup

from core.base_scraper import BaseScraper
from utils import TextUtils, URLUtils


class NhaNamScraper(BaseScraper):
    """Scraper for nhanam.vn"""
    
    def __init__(self):
        super().__init__("nhanam.vn")
    
    def build_page_url(self, page: int) -> str:
        """Build URL for a specific page number."""
        list_page_url = self.website_config.get("list_page_url", "/sach-moi-xuat-ban")
        return f"{self.base_url}{list_page_url}?page={page}"
    
    def find_book_elements(self, soup: BeautifulSoup) -> List:
        """Find book container elements on the page."""
        return soup.find_all('div', class_=['col-6', 'col-md-3', 'col-lg-3', 'product-col'])
    
    def extract_book_info(self, element, fetch_details: bool = False) -> Dict[str, Any]:
        """Extract book information from a product element."""
        try:
            selectors = self.website_config.get("selectors", {})
            
            # Extract title
            title_elem = element.find('h3', class_='product-name')
            if title_elem:
                title_link = title_elem.find('a')
                title = TextUtils.clean_text(title_link.get_text()) if title_link else ""
            else:
                title = ""
            
            # Standardize the title
            title = TextUtils.standardize_title(title)
            
            # Extract author - nhanam doesn't have author info in the grid
            author = ""
            
            # Extract price
            price_elem = element.find('span', class_='price')
            price = TextUtils.extract_price(price_elem.get_text()) if price_elem else ""
            
            # Extract image URL
            img_elem = element.find('img')
            image_url = ""
            if img_elem:
                # nhanam uses lazy loading with data-src
                image_url = img_elem.get('data-src') or img_elem.get('src', '')
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
        """Extract detailed book information from nhanam.vn detail page."""
        details = {"title": "", "author": "", "description": ""}
        
        try:
            selectors = self.website_config.get("selectors", {})
            
            # Extract full title from h1
            title_elem = soup.select_one(selectors.get("detail_title", "h1"))
            if title_elem:
                details['title'] = TextUtils.clean_text(title_elem.get_text())
            
            # Extract author - nhanam has .author class
            author_elem = soup.select_one(selectors.get("detail_author", ".author"))
            if author_elem:
                author_text = author_elem.get_text()
                # Clean up "Tác giả:" prefix
                author = re.sub(r'^Tác giả[:\s]*', '', author_text, flags=re.IGNORECASE)
                details['author'] = TextUtils.clean_text(author)
            
            # Try to extract description from product tabs or content
            desc_selectors = selectors.get("description_selectors", [".product-description", ".tab-content", ".product-content"])
            for selector in desc_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    desc_text = TextUtils.clean_text(desc_elem.get_text())
                    details['description'] = desc_text[:500]  # Limit description length
                    break
        
        except Exception as e:
            self.logger.error(f"Error extracting book details: {e}")
        
        return details