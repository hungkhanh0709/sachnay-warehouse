import requests
from bs4 import BeautifulSoup
import logging
import time
from typing import List, Dict, Any
from urllib.parse import urljoin, urlparse
import re

class BaseScraper:
    """Base class for book scrapers."""
    
    def __init__(self, base_url: str, source_name: str):
        self.base_url = base_url
        self.source_name = source_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.logger = logging.getLogger(__name__)
    
    def fetch_page(self, url: str, max_retries: int = 3) -> BeautifulSoup:
        """Fetch and parse a web page."""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return BeautifulSoup(response.content, 'html.parser')
            except requests.RequestException as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        if not text:
            return ""
        return re.sub(r'\s+', ' ', text.strip())
    
    def extract_price(self, price_text: str) -> str:
        """Extract and normalize price."""
        if not price_text:
            return ""
        
        # Remove currency symbols and normalize
        price = re.sub(r'[^\d,.]', '', price_text)
        return price.strip()
    
    def scrape_books(self, max_pages: int = 5) -> List[Dict[str, Any]]:
        """Scrape books from the source. To be implemented by subclasses."""
        raise NotImplementedError


class SachDongaScraper(BaseScraper):
    """Scraper for sachdonga.vn"""
    
    def __init__(self):
        super().__init__("https://sachdonga.vn", "sachdonga.vn")
    
    def scrape_books(self, max_pages: int = 5) -> List[Dict[str, Any]]:
        """Scrape books from sachdonga.vn/collections/sachmoi"""
        books = []
        
        for page in range(1, max_pages + 1):
            try:
                url = f"{self.base_url}/collections/sachmoi?page={page}"
                self.logger.info(f"Scraping {url}")
                
                soup = self.fetch_page(url)
                
                # Find book containers (adjust selectors based on actual site structure)
                book_elements = soup.find_all('div', class_=['product-item', 'product-card', 'item'])
                
                if not book_elements:
                    # Try alternative selectors
                    book_elements = soup.find_all('div', attrs={'data-product-id': True})
                
                if not book_elements:
                    self.logger.warning(f"No books found on page {page}")
                    break
                
                for element in book_elements:
                    book = self.extract_book_info(element)
                    if book:
                        books.append(book)
                
                self.logger.info(f"Found {len(book_elements)} books on page {page}")
                time.sleep(1)  # Be respectful to the server
                
            except Exception as e:
                self.logger.error(f"Error scraping page {page}: {e}")
                break
        
        return books
    
    def extract_book_info(self, element) -> Dict[str, Any]:
        """Extract book information from a product element."""
        try:
            # Extract title
            title_elem = element.find(['h3', 'h4', 'h5'], class_=['product-title', 'title']) or \
                        element.find(['a'], class_=['product-link', 'title-link'])
            title = self.clean_text(title_elem.get_text()) if title_elem else ""
            
            # Extract author
            author_elem = element.find(['div', 'span'], class_=['author', 'product-author']) or \
                         element.find(['div', 'span'], string=re.compile(r'Tác giả'))
            author = self.clean_text(author_elem.get_text()) if author_elem else ""
            
            # Extract price
            price_elem = element.find(['span', 'div'], class_=['price', 'product-price', 'current-price'])
            price = self.extract_price(price_elem.get_text()) if price_elem else ""
            
            # Extract image URL
            img_elem = element.find('img')
            image_url = ""
            if img_elem:
                image_url = img_elem.get('src') or img_elem.get('data-src', '')
                if image_url and not image_url.startswith('http'):
                    image_url = urljoin(self.base_url, image_url)
            
            # Extract product URL
            link_elem = element.find('a')
            product_url = ""
            if link_elem:
                product_url = link_elem.get('href', '')
                if product_url and not product_url.startswith('http'):
                    product_url = urljoin(self.base_url, product_url)
            
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


class NhaNamScraper(BaseScraper):
    """Scraper for nhanam.vn"""
    
    def __init__(self):
        super().__init__("https://nhanam.vn", "nhanam.vn")
    
    def scrape_books(self, max_pages: int = 5) -> List[Dict[str, Any]]:
        """Scrape books from nhanam.vn/sach-moi-xuat-ban"""
        books = []
        
        for page in range(1, max_pages + 1):
            try:
                url = f"{self.base_url}/sach-moi-xuat-ban?page={page}"
                self.logger.info(f"Scraping {url}")
                
                soup = self.fetch_page(url)
                
                # Find book containers (adjust selectors based on actual site structure)
                book_elements = soup.find_all('div', class_=['product-item', 'book-item', 'item'])
                
                if not book_elements:
                    # Try alternative selectors
                    book_elements = soup.find_all(['article', 'div'], attrs={'data-product': True})
                
                if not book_elements:
                    self.logger.warning(f"No books found on page {page}")
                    break
                
                for element in book_elements:
                    book = self.extract_book_info(element)
                    if book:
                        books.append(book)
                
                self.logger.info(f"Found {len(book_elements)} books on page {page}")
                time.sleep(1)  # Be respectful to the server
                
            except Exception as e:
                self.logger.error(f"Error scraping page {page}: {e}")
                break
        
        return books
    
    def extract_book_info(self, element) -> Dict[str, Any]:
        """Extract book information from a product element."""
        try:
            # Extract title
            title_elem = element.find(['h3', 'h4', 'h5'], class_=['title', 'book-title']) or \
                        element.find(['a'], class_=['book-link', 'product-link'])
            title = self.clean_text(title_elem.get_text()) if title_elem else ""
            
            # Extract author
            author_elem = element.find(['div', 'span'], class_=['author', 'book-author']) or \
                         element.find(['div', 'span'], string=re.compile(r'Tác giả'))
            author = self.clean_text(author_elem.get_text()) if author_elem else ""
            
            # Extract price
            price_elem = element.find(['span', 'div'], class_=['price', 'book-price', 'current-price'])
            price = self.extract_price(price_elem.get_text()) if price_elem else ""
            
            # Extract image URL
            img_elem = element.find('img')
            image_url = ""
            if img_elem:
                image_url = img_elem.get('src') or img_elem.get('data-src', '')
                if image_url and not image_url.startswith('http'):
                    image_url = urljoin(self.base_url, image_url)
            
            # Extract product URL
            link_elem = element.find('a')
            product_url = ""
            if link_elem:
                product_url = link_elem.get('href', '')
                if product_url and not product_url.startswith('http'):
                    product_url = urljoin(self.base_url, product_url)
            
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