"""
Data management module for handling book data storage and deduplication.
"""

import json
import os
import logging
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Set

from config import config


class BookDataManager:
    """Manages book data storage and deduplication."""
    
    def __init__(self, data_file: str = None):
        self.data_file = data_file or config.get("output.default_filename", "books_data.json")
        self.logger = logging.getLogger(__name__)
        
    def load_existing_data(self) -> List[Dict[str, Any]]:
        """Load existing book data from JSON file."""
        if not os.path.exists(self.data_file):
            return []
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('books', [])
        except (json.JSONDecodeError, IOError) as e:
            self.logger.error(f"Error loading existing data: {e}")
            return []
    
    def save_data(self, books: List[Dict[str, Any]]) -> None:
        """Save book data to JSON file with metadata."""
        data = {
            'last_updated': datetime.now().isoformat(),
            'total_books': len(books),
            'books': books
        }
        
        try:
            indent = config.get("output.indent", 2)
            ensure_ascii = config.get("output.ensure_ascii", False)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=ensure_ascii, indent=indent)
            self.logger.info(f"Saved {len(books)} books to {self.data_file}")
        except IOError as e:
            self.logger.error(f"Error saving data: {e}")
    
    def generate_book_hash(self, book: Dict[str, Any]) -> str:
        """Generate a unique hash for a book based on title and author."""
        title = book.get('title', '').strip().lower()
        author = book.get('author', '').strip().lower()
        # Include price and source for better uniqueness
        price = str(book.get('price', '')).strip()
        source = book.get('source', '').strip()
        
        unique_string = f"{title}_{author}_{price}_{source}"
        return hashlib.md5(unique_string.encode('utf-8')).hexdigest()
    
    def deduplicate_books(self, existing_books: List[Dict[str, Any]], 
                         new_books: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicates and return only new books."""
        existing_hashes: Set[str] = set()
        
        # Generate hashes for existing books
        for book in existing_books:
            book_hash = self.generate_book_hash(book)
            existing_hashes.add(book_hash)
        
        # Filter new books
        unique_new_books = []
        for book in new_books:
            book_hash = self.generate_book_hash(book)
            if book_hash not in existing_hashes:
                unique_new_books.append(book)
                existing_hashes.add(book_hash)
        
        return unique_new_books
    
    def merge_books(self, existing_books: List[Dict[str, Any]], 
                   new_books: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge existing and new books, removing duplicates."""
        unique_new_books = self.deduplicate_books(existing_books, new_books)
        
        self.logger.info(f"Found {len(unique_new_books)} new unique books out of {len(new_books)} scraped books")
        
        # Add timestamps to new books
        for book in unique_new_books:
            book['added_date'] = datetime.now().isoformat()
        
        return existing_books + unique_new_books