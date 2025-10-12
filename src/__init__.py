"""
Sachnay Warehouse - Vietnamese Book Data Scraper

A web scraper for Vietnamese book data from online bookstores.
This tool crawls book information from popular Vietnamese book websites
and stores the data in JSON format with deduplication capabilities.
"""

__version__ = "1.0.0"
__author__ = "hungkhanh0709"
__description__ = "Vietnamese Book Data Scraper"

from .core.data_manager import BookDataManager
from .core.base_scraper import BaseScraper

__all__ = ["BookDataManager", "BaseScraper"]