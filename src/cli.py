#!/usr/bin/env python3
"""
Command-line interface for the Sachnay Warehouse scraper.

This script orchestrates the scraping process, data management, and CLI interface.
"""

import sys
import argparse
import logging
from pathlib import Path

from .config import config
from .core.data_manager import BookDataManager
from .scrapers import SachDongaScraper, NhaNamScraper
from .utils import LoggerUtils


def setup_logging(log_level: str) -> None:
    """Setup logging configuration."""
    config.set("logging.level", log_level)
    LoggerUtils.setup_logger(
        "sachnay_warehouse",
        log_level=log_level,
        log_file=config.get("logging.log_file", "scraper.log")
    )


def scrape_all_sources(max_pages: int = None, fetch_details: bool = None) -> list:
    """Scrape books from all configured sources."""
    max_pages = max_pages or config.get("scraping.max_pages", 5)
    fetch_details = fetch_details if fetch_details is not None else config.get("scraping.fetch_details", False)
    
    all_books = []
    logger = logging.getLogger("sachnay_warehouse.main")
    
    # Initialize scrapers
    scrapers = [
        SachDongaScraper(),
        NhaNamScraper()
    ]
    
    for scraper in scrapers:
        try:
            logger.info(f"Starting scraping from {scraper.source_name}")
            if fetch_details:
                logger.info(f"Detail scraping enabled - this will be slower but more comprehensive")
            
            books = scraper.scrape_books(max_pages=max_pages, fetch_details=fetch_details)
            all_books.extend(books)
            logger.info(f"Scraped {len(books)} books from {scraper.source_name}")
        except Exception as e:
            logger.error(f"Failed to scrape from {scraper.source_name}: {e}")
    
    return all_books


def main():
    """Main function to orchestrate the scraping process."""
    parser = argparse.ArgumentParser(description='Scrape book data from Vietnamese book stores')
    parser.add_argument('--max-pages', type=int, default=None, 
                       help=f'Maximum pages to scrape per source (default: {config.get("scraping.max_pages")})')
    parser.add_argument('--output', type=str, default=None,
                       help=f'Output JSON file (default: {config.get("output.default_filename")})')
    parser.add_argument('--log-level', type=str, default=None,
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help=f'Logging level (default: {config.get("logging.level")})')
    parser.add_argument('--fetch-details', action='store_true',
                       help='Fetch detailed information from individual book pages (slower but more complete)')
    parser.add_argument('--config', type=str,
                       help='Path to configuration file')
    
    args = parser.parse_args()
    
    # Load custom config if specified
    if args.config:
        config._load_from_file(args.config)
    
    # Override config with command line arguments
    if args.max_pages is not None:
        config.set("scraping.max_pages", args.max_pages)
    if args.output is not None:
        config.set("output.default_filename", args.output)
    if args.log_level is not None:
        config.set("logging.level", args.log_level)
    if args.fetch_details:
        config.set("scraping.fetch_details", True)
    
    # Setup logging
    setup_logging(config.get("logging.level", "INFO"))
    
    logger = logging.getLogger("sachnay_warehouse.main")
    
    logger.info("Starting book data scraping process")
    
    try:
        # Initialize data manager
        data_manager = BookDataManager(config.get("output.default_filename"))
        
        # Load existing data
        existing_books = data_manager.load_existing_data()
        logger.info(f"Loaded {len(existing_books)} existing books")
        
        # Scrape new data
        new_books = scrape_all_sources(
            max_pages=config.get("scraping.max_pages"),
            fetch_details=config.get("scraping.fetch_details")
        )
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
        print(f"Data saved to: {config.get('output.default_filename')}")
        
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()