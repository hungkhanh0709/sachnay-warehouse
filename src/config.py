"""
Configuration settings for the Sachnay Warehouse scraper.
"""

from typing import Dict, Any
import os
from pathlib import Path

# Base configuration
DEFAULT_CONFIG = {
    "scraping": {
        "max_pages": 5,
        "fetch_details": False,
        "delay_between_requests": 1.0,
        "max_retries": 3,
        "timeout": 30,
    },
    "output": {
        "default_filename": "output/books_data.json",
        "indent": 2,
        "ensure_ascii": False,
    },
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "log_file": "output/scraper.log",
    },
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

# Website-specific configurations
WEBSITE_CONFIGS = {
    "sachdonga.vn": {
        "base_url": "https://sachdonga.vn",
        "source_name": "sachdonga.vn",
        "list_page_url": "/collections/sachmoi",
        "selectors": {
            "product_container": "div.product-item",
            "title": "div.product-title a",
            "price": "span.current-price",
            "image": "img",
            "link": "a",
            "detail_title": "h1",
            "detail_author_patterns": [
                r'Tác giả[:\s]*([^.\n\r|]+?)(?:[.\n\r|]|Dịch giả|Kích thước|Số trang)',
                r'Tác giả[:\s]*([^.\n\r|]+?)(?:\s*Dịch giả|\s*Kích thước|\s*Số trang|\s*\||$)',
            ],
            "product_content": ".product-content",
        },
    },
    "nhanam.vn": {
        "base_url": "https://nhanam.vn",
        "source_name": "nhanam.vn",
        "list_page_url": "/sach-moi-xuat-ban",
        "selectors": {
            "product_container": "div.col-6.col-md-3.col-lg-3.product-col",
            "title": "h3.product-name a",
            "price": "span.price",
            "image": "img",
            "link": "a",
            "detail_title": "h1",
            "detail_author": ".author",
            "description_selectors": [".product-description", ".tab-content", ".product-content"],
        },
    },
}


class Config:
    """Configuration manager for the scraper."""
    
    def __init__(self, config_path: str = None):
        self.config = DEFAULT_CONFIG.copy()
        self.website_configs = WEBSITE_CONFIGS.copy()
        
        if config_path and os.path.exists(config_path):
            self._load_from_file(config_path)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key path (e.g., 'scraping.max_pages')."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_website_config(self, website: str) -> Dict[str, Any]:
        """Get configuration for a specific website."""
        return self.website_configs.get(website, {})
    
    def set(self, key: str, value: Any):
        """Set configuration value by key path."""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def _load_from_file(self, config_path: str):
        """Load configuration from JSON file."""
        import json
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                self._deep_update(self.config, file_config)
        except Exception as e:
            print(f"Warning: Could not load config from {config_path}: {e}")
    
    def _deep_update(self, base_dict: dict, update_dict: dict):
        """Deep update dictionary."""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value


# Global config instance
config = Config()