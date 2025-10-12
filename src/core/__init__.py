"""
Core modules for the Sachnay Warehouse scraper.
"""

from .base_scraper import BaseScraper
from .data_manager import BookDataManager

__all__ = ["BaseScraper", "BookDataManager"]