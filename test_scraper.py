#!/usr/bin/env python3
"""
Test script for book scraper functionality with mock data.
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_manager import BookDataManager


def create_mock_books() -> List[Dict[str, Any]]:
    """Create mock book data for testing."""
    return [
        {
            'title': 'Dạy Con Làm Giàu Tập 1',
            'author': 'Robert Kiyosaki',
            'price': '150,000',
            'image_url': 'https://example.com/book1.jpg',
            'product_url': 'https://sachdonga.vn/products/day-con-lam-giau-1',
            'source': 'sachdonga.vn',
            'scraped_date': '2024-01-15 10:30:00'
        },
        {
            'title': 'Atomic Habits',
            'author': 'James Clear',
            'price': '180,000',
            'image_url': 'https://example.com/book2.jpg',
            'product_url': 'https://nhanam.vn/products/atomic-habits',
            'source': 'nhanam.vn',
            'scraped_date': '2024-01-15 10:35:00'
        },
        {
            'title': 'Sapiens',
            'author': 'Yuval Noah Harari',
            'price': '200,000',
            'image_url': 'https://example.com/book3.jpg',
            'product_url': 'https://sachdonga.vn/products/sapiens',
            'source': 'sachdonga.vn',
            'scraped_date': '2024-01-15 10:40:00'
        }
    ]


def create_duplicate_books() -> List[Dict[str, Any]]:
    """Create mock books with some duplicates for testing deduplication."""
    return [
        # Duplicate of first book (should be filtered out)
        {
            'title': 'Dạy Con Làm Giàu Tập 1',
            'author': 'Robert Kiyosaki',
            'price': '150,000',
            'image_url': 'https://example.com/book1_alt.jpg',
            'product_url': 'https://sachdonga.vn/products/day-con-lam-giau-1',
            'source': 'sachdonga.vn',
            'scraped_date': '2024-01-16 09:30:00'
        },
        # New book (should be added)
        {
            'title': 'Thinking, Fast and Slow',
            'author': 'Daniel Kahneman',
            'price': '220,000',
            'image_url': 'https://example.com/book4.jpg',
            'product_url': 'https://nhanam.vn/products/thinking-fast-slow',
            'source': 'nhanam.vn',
            'scraped_date': '2024-01-16 09:35:00'
        },
        # Another new book
        {
            'title': 'The Psychology of Money',
            'author': 'Morgan Housel',
            'price': '160,000',
            'image_url': 'https://example.com/book5.jpg',
            'product_url': 'https://sachdonga.vn/products/psychology-money',
            'source': 'sachdonga.vn',
            'scraped_date': '2024-01-16 09:40:00'
        }
    ]


def test_data_manager():
    """Test the BookDataManager functionality."""
    print("=== Testing BookDataManager ===")
    
    # Test file
    test_file = "test_books.json"
    
    # Clean up any existing test file
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Initialize data manager
    manager = BookDataManager(test_file)
    
    # Test 1: Initial save
    print("\n1. Testing initial save...")
    initial_books = create_mock_books()
    manager.save_data(initial_books)
    print(f"Saved {len(initial_books)} books to {test_file}")
    
    # Test 2: Load existing data
    print("\n2. Testing load existing data...")
    loaded_books = manager.load_existing_data()
    print(f"Loaded {len(loaded_books)} books from {test_file}")
    assert len(loaded_books) == len(initial_books), "Loaded data count mismatch"
    
    # Test 3: Deduplication
    print("\n3. Testing deduplication...")
    new_books = create_duplicate_books()
    print(f"Created {len(new_books)} new books (with duplicates)")
    
    unique_new_books = manager.deduplicate_books(loaded_books, new_books)
    print(f"After deduplication: {len(unique_new_books)} unique new books")
    
    # Should only have 2 new books (1 duplicate filtered out)
    assert len(unique_new_books) == 2, f"Expected 2 unique books, got {len(unique_new_books)}"
    
    # Test 4: Merge and save
    print("\n4. Testing merge and save...")
    all_books = manager.merge_books(loaded_books, new_books)
    manager.save_data(all_books)
    print(f"Total books after merge: {len(all_books)}")
    
    # Should have 5 total books (3 original + 2 new)
    assert len(all_books) == 5, f"Expected 5 total books, got {len(all_books)}"
    
    # Test 5: Verify saved data structure
    print("\n5. Testing saved data structure...")
    with open(test_file, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
    
    required_keys = ['last_updated', 'total_books', 'books']
    for key in required_keys:
        assert key in saved_data, f"Missing key: {key}"
    
    assert saved_data['total_books'] == len(all_books), "Total books count mismatch"
    
    # Clean up
    os.remove(test_file)
    
    print("\n✅ All BookDataManager tests passed!")


def test_hash_generation():
    """Test book hash generation for deduplication."""
    print("\n=== Testing Hash Generation ===")
    
    manager = BookDataManager()
    
    # Test identical books
    book1 = {
        'title': 'Test Book',
        'author': 'Test Author',
        'price': '100,000',
        'source': 'test.com'
    }
    
    book2 = {
        'title': 'Test Book',
        'author': 'Test Author',
        'price': '100,000',
        'source': 'test.com'
    }
    
    hash1 = manager.generate_book_hash(book1)
    hash2 = manager.generate_book_hash(book2)
    
    assert hash1 == hash2, "Identical books should have same hash"
    print("✅ Identical books produce same hash")
    
    # Test different books
    book3 = {
        'title': 'Different Book',
        'author': 'Test Author',
        'price': '100,000',
        'source': 'test.com'
    }
    
    hash3 = manager.generate_book_hash(book3)
    assert hash1 != hash3, "Different books should have different hashes"
    print("✅ Different books produce different hashes")


def main():
    """Run all tests."""
    print("Starting book scraper tests...\n")
    
    try:
        test_hash_generation()
        test_data_manager()
        
        print("\n🎉 All tests passed successfully!")
        print("\nThe scraper is ready to use. To run the actual scraper:")
        print("python3 main.py --max-pages 3 --output books_data.json")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()