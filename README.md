# sachnay-warehouse

A web scraper for Vietnamese book data from online bookstores. This tool crawls book information from popular Vietnamese book websites and stores the data in JSON format with deduplication capabilities.

## Features

- **Multi-source scraping**: Supports sachdonga.vn and nhanam.vn
- **Deduplication**: Automatically filters out duplicate books based on title, author, price, and source
- **Incremental updates**: Only scrapes new books, doesn't re-fetch existing data
- **JSON storage**: Stores data in structured JSON format for easy processing
- **Configurable**: Adjustable scraping parameters and output options
- **Logging**: Comprehensive logging for monitoring scraping progress

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

## Usage

### Basic usage:
```bash
python3 main.py
```

### Advanced usage with options:
```bash
python3 main.py --max-pages 5 --output my_books.json --log-level DEBUG
```

### Available options:
- `--max-pages`: Maximum pages to scrape per source (default: 5)
- `--output`: Output JSON file path (default: books_data.json)
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR)

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

The project consists of three main components:

1. **Scrapers** (`scrapers.py`): Web scraping logic for each supported website
2. **Data Manager** (`data_manager.py`): Handles data storage, deduplication, and merging
3. **Main Script** (`main.py`): Orchestrates the scraping process

## Supported Websites

- **sachdonga.vn**: /collections/sachmoi
- **nhanam.vn**: /sach-moi-xuat-ban

## Testing

Run the test suite to verify functionality:

```bash
python3 test_scraper.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and research purposes. Please respect the websites' robots.txt and terms of service when scraping data.