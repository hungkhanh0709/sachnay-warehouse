# sachnay-warehouse

A web scraper for Vietnamese book data from online bookstores. This tool crawls book information from popular Vietnamese book websites and stores the data in JSON format with deduplication capabilities.

## Features

- **Multi-source scraping**: Supports sachdonga.vn and nhanam.vn
- **Deduplication**: Automatically filters out duplicate books based on title, author, price, and source
- **Incremental updates**: Only scrapes new books, doesn't re-fetch existing data
- **JSON storage**: Stores data in structured JSON format for easy processing
- **Configurable**: Adjustable scraping parameters and output options
- **Logging**: Comprehensive logging for monitoring scraping progress
- **Title standardization**: Automatically cleans and standardizes book titles
- **Detail extraction**: Optional detailed scraping for complete titles and author information
- **Modular architecture**: Clean, maintainable code structure with separated concerns

## Installation

1. Clone the repository:
```bash
git clone https://github.com/hungkhanh0709/sachnay-warehouse.git
cd sachnay-warehouse
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Install as a package:
```bash
pip install -e .
```

## Usage

### Basic usage:
```bash
python3 main.py
```

### Advanced usage with options:
```bash
python3 main.py --max-pages 5 --output my_books.json --log-level DEBUG
```

### Enhanced data extraction:
```bash
python3 main.py --max-pages 3 --fetch-details --output detailed_books.json
```

### With custom configuration:
```bash
python3 main.py --config config/config.json --max-pages 2 --fetch-details
```

### Available options:
- `--max-pages`: Maximum pages to scrape per source (default: 5)
- `--output`: Output JSON file path (default: output/books_data.json)
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `--fetch-details`: Fetch detailed information from individual book pages (slower but more complete)
- `--config`: Path to custom configuration file

## Data Structure

The scraped data is stored in JSON format with the following structure:

```json
{
  "last_updated": "2024-01-15T10:30:00",
  "total_books": 150,
  "books": [
    {
      "title": "Book Title",
      "author": "Author Name",
      "price": "150,000",
      "image_url": "https://example.com/book.jpg",
      "product_url": "https://example.com/product",
      "source": "sachdonga.vn",
      "scraped_date": "2024-01-15 10:30:00",
      "added_date": "2024-01-15T10:30:00"
    }
  ]
}
```

## Architecture

The project features a modular architecture with clear separation of concerns:

```
sachnay-warehouse/
├── main.py                    # Main entry point
├── output/                    # Output files
│   ├── books_data.json       # Scraped book data
│   └── scraper.log          # Application logs
├── src/                       # Source code
│   ├── config.py             # Configuration management
│   ├── core/                 # Core functionality
│   │   ├── base_scraper.py   # Abstract base scraper class
│   │   └── data_manager.py   # Data storage and deduplication
│   ├── scrapers/             # Website-specific scrapers
│   │   ├── sachdonga_scraper.py
│   │   └── nhanam_scraper.py
│   └── utils/                # Utility functions
│       └── __init__.py       # Text, URL, and logging utilities
├── tests/                    # Unit tests
├── config/                   # Configuration files
└── requirements.txt          # Dependencies
```

### Key Components:

1. **Core** (`src/core/`): Base classes and data management
2. **Scrapers** (`src/scrapers/`): Website-specific scraping logic
3. **Utils** (`src/utils/`): Utility functions for text processing, URLs, and logging
4. **Config** (`src/config.py`): Centralized configuration management
5. **Tests** (`tests/`): Unit tests and test utilities

For detailed architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Supported Websites

- **sachdonga.vn**: /collections/sachmoi
- **nhanam.vn**: /sach-moi-xuat-ban

## Testing

Run the test suite to verify functionality:

```bash
# Run all tests
python3 tests/test_utils.py

# Run specific tests
python3 -m unittest tests.test_utils.TestTextUtils
```
