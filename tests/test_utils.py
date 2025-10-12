"""
Tests for the Sachnay Warehouse scraper.
"""

import unittest
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sachnay_warehouse.utils import TextUtils, URLUtils
from sachnay_warehouse.config import config


class TestTextUtils(unittest.TestCase):
    """Test text utility functions."""
    
    def test_clean_text(self):
        """Test text cleaning functionality."""
        self.assertEqual(TextUtils.clean_text("  Hello   World  "), "Hello World")
        self.assertEqual(TextUtils.clean_text(""), "")
        self.assertEqual(TextUtils.clean_text(None), "")
    
    def test_standardize_title(self):
        """Test title standardization."""
        self.assertEqual(
            TextUtils.standardize_title("Book Title..."),
            "Book Title"
        )
        self.assertEqual(
            TextUtils.standardize_title("Book Title with   spaces"),
            "Book Title with spaces"
        )
        self.assertEqual(
            TextUtils.standardize_title("Book Title...."),
            "Book Title"
        )
    
    def test_extract_price(self):
        """Test price extraction."""
        self.assertEqual(TextUtils.extract_price("123,000₫"), "123,000")
        self.assertEqual(TextUtils.extract_price("Price: $123.45"), "123.45")
        self.assertEqual(TextUtils.extract_price(""), "")


class TestURLUtils(unittest.TestCase):
    """Test URL utility functions."""
    
    def test_normalize_url(self):
        """Test URL normalization."""
        base_url = "https://example.com"
        
        # Protocol-relative URL
        self.assertEqual(
            URLUtils.normalize_url("//cdn.example.com/image.jpg", base_url),
            "https://cdn.example.com/image.jpg"
        )
        
        # Relative URL
        self.assertEqual(
            URLUtils.normalize_url("/path/to/page", base_url),
            "https://example.com/path/to/page"
        )
        
        # Absolute URL (should remain unchanged)
        self.assertEqual(
            URLUtils.normalize_url("https://other.com/page", base_url),
            "https://other.com/page"
        )
        
        # Data URL (should remain unchanged)
        self.assertEqual(
            URLUtils.normalize_url("data:image/gif;base64,abc", base_url),
            "data:image/gif;base64,abc"
        )


class TestConfig(unittest.TestCase):
    """Test configuration management."""
    
    def test_get_config(self):
        """Test getting configuration values."""
        self.assertIsNotNone(config.get("scraping.max_pages"))
        self.assertEqual(config.get("nonexistent.key", "default"), "default")
    
    def test_website_config(self):
        """Test website-specific configuration."""
        sachdonga_config = config.get_website_config("sachdonga.vn")
        self.assertIn("base_url", sachdonga_config)
        self.assertIn("selectors", sachdonga_config)


if __name__ == "__main__":
    unittest.main()