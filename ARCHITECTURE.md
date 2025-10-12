# Sachnay Warehouse - Restructured Code Architecture

This document explains the new, improved code structure for the Sachnay Warehouse book scraper.

## 📁 New Project Structure

```
sachnay-warehouse/
├── src/
│       ├── __init__.py             # Package initialization
│       ├── config.py               # Configuration management
│       ├── cli.py                  # Command-line interface
│       ├── core/                   # Core functionality
│       │   ├── __init__.py
│       │   ├── base_scraper.py     # Abstract base scraper class
│       │   └── data_manager.py     # Data storage and management
│       ├── scrapers/               # Website-specific scrapers
│       │   ├── __init__.py
│       │   ├── sachdonga_scraper.py # SachDonga.vn scraper
│       │   └── nhanam_scraper.py   # NhaNam.vn scraper
│       └── utils/                  # Utility functions
│           └── __init__.py         # Text, URL, and logging utilities
├── tests/                          # Unit tests
│   └── test_utils.py              # Test utilities and core functions
├── config/                         # Configuration files
│   └── config.json                # Example configuration
├── main_new.py                     # New main entry point
├── setup.py                        # Package setup configuration
├── requirements.txt                # Dependencies
└── README.md                       # Documentation
```

## 🚀 Key Improvements

### 1. **Modular Architecture**
- **Separation of Concerns**: Each module has a single responsibility
- **Extensibility**: Easy to add new scrapers without modifying existing code
- **Maintainability**: Smaller, focused files are easier to maintain

### 2. **Configuration Management**
- **Centralized Settings**: All configuration in one place
- **Customizable**: Support for external configuration files
- **Website-Specific**: Separate configs for each website's selectors
- **Command-Line Override**: CLI arguments override config file values

### 3. **Proper Package Structure**
- **Standard Python Layout**: Follows Python packaging best practices
- **Installable Package**: Can be installed with pip
- **Import System**: Clean, predictable imports
- **Entry Points**: Proper console script entry points

### 4. **Enhanced Error Handling**
- **Structured Logging**: Proper logger hierarchy
- **Graceful Failures**: Better error recovery and reporting
- **Debugging Support**: Detailed logging for troubleshooting

### 5. **Utility Functions**
- **Reusable Code**: Common functions extracted to utilities
- **Type Safety**: Proper type hints throughout
- **Testing**: Comprehensive unit tests for utilities

## 🔧 Configuration System

### Default Configuration
The system comes with sensible defaults built-in:

```python
# Built-in defaults in config.py
DEFAULT_CONFIG = {
    "scraping": {
        "max_pages": 5,
        "fetch_details": False,
        "delay_between_requests": 1.0,
        "max_retries": 3,
        "timeout": 30,
    },
    "output": {
        "default_filename": "books_data.json",
        "indent": 2,
        "ensure_ascii": False,
    },
    "logging": {
        "level": "INFO",
        "log_file": "scraper.log",
    }
}
```

### Custom Configuration
You can override defaults with a JSON config file:

```json
{
  "scraping": {
    "max_pages": 3,
    "fetch_details": true,
    "delay_between_requests": 2.0
  },
  "output": {
    "default_filename": "my_books.json",
    "indent": 4
  },
  "logging": {
    "level": "DEBUG"
  }
}
```

### Website-Specific Configuration
Each website has its own configuration with selectors and URLs:

```python
WEBSITE_CONFIGS = {
    "sachdonga.vn": {
        "base_url": "https://sachdonga.vn",
        "selectors": {
            "product_container": "div.product-item",
            "title": "div.product-title a",
            "price": "span.current-price",
            # ... more selectors
        }
    }
}
```

## 🎯 Usage Examples

### Basic Usage (New Structure)
```bash
# Using the new modular system
python3 main_new.py --max-pages 5
```

### Advanced Usage with Configuration
```bash
# Using custom configuration file
python3 main_new.py --config config/config.json --max-pages 3 --fetch-details
```

### Programmatic Usage
```python
from sachnay_warehouse.scrapers import SachDongaScraper
from sachnay_warehouse.core.data_manager import BookDataManager

# Initialize scraper
scraper = SachDongaScraper()

# Scrape books
books = scraper.scrape_books(max_pages=2, fetch_details=True)

# Save data
manager = BookDataManager("output.json")
manager.save_data(books)
```

## 🧪 Testing

The new structure includes comprehensive unit tests:

```bash
# Run all tests
python3 tests/test_utils.py

# Run specific test
python3 -m unittest tests.test_utils.TestTextUtils.test_standardize_title
```

## 📦 Installation as Package

The restructured code can be installed as a proper Python package:

```bash
# Install in development mode
pip install -e .

# Use the installed command
sachnay-warehouse --max-pages 3 --fetch-details
```

## 🔄 Migration from Old Structure

### Old vs New Comparison

| Aspect | Old Structure | New Structure |
|--------|---------------|---------------|
| **Files** | 3 large files | 8+ focused modules |
| **Configuration** | Hard-coded values | Centralized config system |
| **Extensibility** | Modify existing files | Add new modules |
| **Testing** | Basic test file | Comprehensive test suite |
| **Installation** | Run scripts directly | Installable package |
| **Maintenance** | Monolithic code | Modular, focused code |

### Benefits of New Structure

1. **🎯 Better Organization**: Clear separation of responsibilities
2. **🔧 Easier Maintenance**: Smaller, focused modules
3. **🚀 Faster Development**: Modular design speeds up feature addition
4. **🛡️ More Robust**: Better error handling and testing
5. **📈 Scalable**: Easy to add new websites or features
6. **⚙️ Configurable**: Flexible configuration system
7. **📦 Professional**: Follows Python packaging standards

## 🎊 Summary

The restructured code provides:
- ✅ **Clean Architecture**: Proper separation of concerns
- ✅ **Extensibility**: Easy to add new scrapers or features  
- ✅ **Configuration**: Flexible, override-able settings
- ✅ **Testing**: Comprehensive unit test coverage
- ✅ **Documentation**: Clear code with type hints
- ✅ **Professional**: Follows Python best practices
- ✅ **Backward Compatibility**: All original functionality preserved

The new structure makes the codebase more maintainable, testable, and professional while preserving all the functionality you've built!