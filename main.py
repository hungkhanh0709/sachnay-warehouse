#!/usr/bin/env python3
"""
Book Data Scraper
Scrapes book data from sachdonga.vn and nhanam.vn, stores in JSON with deduplication.
"""

import logging
import sys
import argparse
from typing import List, Dict, Any

from scrapers import SachDongaScraper, NhaNamScraper
from data_manager import BookDataManager


def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('scraper.log')
        ]
    )


def scrape_all_sources(max_pages: int = 5) -> List[Dict[str, Any]]:
    """Scrape books from all configured sources."""
    all_books = []
    logger = logging.getLogger(__name__)
    
    # Initialize scrapers
    scrapers = [
        SachDongaScraper(),
        NhaNamScraper()
    ]
    
    for scraper in scrapers:
        try:
            logger.info(f"Starting scraping from {scraper.source_name}")
            books = scraper.scrape_books(max_pages=max_pages)
            all_books.extend(books)
            logger.info(f"Scraped {len(books)} books from {scraper.source_name}")
        except Exception as e:
            logger.error(f"Failed to scrape from {scraper.source_name}: {e}")
    
    return all_books


def main():
    """Main function to orchestrate the scraping process."""
    parser = argparse.ArgumentParser(description='Scrape book data from Vietnamese book stores')
    parser.add_argument('--max-pages', type=int, default=5, 
                       help='Maximum pages to scrape per source (default: 5)')
    parser.add_argument('--output', type=str, default='books_data.json',
                       help='Output JSON file (default: books_data.json)')
    parser.add_argument('--log-level', type=str, default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level (default: INFO)')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting book data scraping process")
    
    try:
        # Initialize data manager
        data_manager = BookDataManager(args.output)
        
        # Load existing data
        existing_books = data_manager.load_existing_data()
        logger.info(f"Loaded {len(existing_books)} existing books")
        
        # Scrape new data
        new_books = scrape_all_sources(max_pages=args.max_pages)
        logger.info(f"Scraped {len(new_books)} total books from all sources")
        
        # Merge and deduplicate
        all_books = data_manager.merge_books(existing_books, new_books)
        
        # Save data
        data_manager.save_data(all_books)
        
        logger.info(f"Process completed. Total books in database: {len(all_books)}")
        
        # Print summary
        print(f"\n=== Scraping Summary ===")
        print(f"Existing books: {len(existing_books)}")
        print(f"Newly scraped books: {len(new_books)}")
        print(f"New unique books added: {len(all_books) - len(existing_books)}")
        print(f"Total books in database: {len(all_books)}")
        print(f"Data saved to: {args.output}")
        
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()