"""
Utility functions for the Sachnay Warehouse scraper.
"""

import re
import time
import logging
from typing import Any
from urllib.parse import urljoin


class TextUtils:
    """Utilities for text processing."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text."""
        if not text:
            return ""
        return re.sub(r'\s+', ' ', text.strip())
    
    @staticmethod
    def standardize_title(title: str) -> str:
        """Standardize book title by cleaning and normalizing it."""
        if not title:
            return ""
        
        # Clean whitespace and normalize
        title = TextUtils.clean_text(title)
        
        # Remove trailing dots (...) that indicate truncation
        title = re.sub(r'\.{2,}$', '', title.strip())
        
        # Handle incomplete parentheses - remove if opening ( without closing )
        if '(' in title and ')' not in title:
            # Remove incomplete parenthetical part
            title = re.sub(r'\s*\([^)]*$', '', title.strip())
        
        # Handle truncated words at the end - remove incomplete words
        # Look for words that are likely truncated (very short, incomplete)
        title = TextUtils._remove_truncated_ending(title)
        
        # Remove extra spaces after cleaning
        title = title.strip()
        
        # Convert to proper title case
        title = TextUtils._convert_to_title_case(title)
        
        # Final cleanup - normalize whitespace
        title = re.sub(r'\s+', ' ', title)
        
        return title
    
    @staticmethod
    def _convert_to_title_case(title: str) -> str:
        """Convert title to proper title case, handling Vietnamese text."""
        if not title:
            return ""
        
        # Handle parenthetical content separately
        def format_parenthetical(match):
            content = match.group(1)
            # Common Vietnamese parenthetical patterns
            if any(word in content.lower() for word in ['bìa', 'khổ', 'tập', 'quyển', 'song ngữ']):
                # Format publishing details in parentheses
                words = content.split()
                formatted_words = []
                for word in words:
                    if word.lower() in ['bìa', 'khổ', 'tập', 'quyển']:
                        formatted_words.append(word.capitalize())
                    elif word.lower() == 'ngữ':
                        formatted_words.append('Ngữ')
                    elif word.lower() == 'song':
                        formatted_words.append('Song')
                    else:
                        formatted_words.append(word.title())
                return f"({' '.join(formatted_words)})"
            else:
                return f"({content.title()})"
        
        # Handle all uppercase titles with dashes/separators
        if title.isupper():
            # First handle parentheses
            title = re.sub(r'\(([^)]+)\)', format_parenthetical, title)
            
            # Split by common separators (dash, pipe, etc.) but preserve parentheses
            parts = re.split(r'\s*[-–—|]\s*', title)
            
            # Convert each part to title case
            converted_parts = []
            for part in parts:
                if part.strip():
                    # Check if this part has parentheses (already formatted above)
                    if '(' in part and ')' in part:
                        # Already formatted, just clean up case for non-parenthetical parts
                        main_part = re.sub(r'\([^)]+\)', '', part).strip()
                        paren_part = re.search(r'\([^)]+\)', part)
                        if main_part:
                            main_formatted = main_part.lower().title()
                            if paren_part:
                                converted_parts.append(f"{main_formatted} {paren_part.group()}")
                            else:
                                converted_parts.append(main_formatted)
                        elif paren_part:
                            converted_parts.append(paren_part.group())
                    else:
                        # Convert to lowercase first, then title case
                        part_lower = part.strip().lower()
                        part_title = part_lower.title()
                        converted_parts.append(part_title)
            
            # Join with proper spacing - take the main title (first part)
            # and handle subtitle if exists
            if len(converted_parts) > 1:
                # Main title + subtitle format
                main_title = converted_parts[0]
                subtitle = converted_parts[1]
                
                # For very long subtitles, might want to truncate or simplify
                if len(subtitle) > 30:
                    # Take first few meaningful words of subtitle
                    subtitle_words = subtitle.split()[:4]
                    subtitle = ' '.join(subtitle_words)
                
                return f"{main_title} - {subtitle}"
            else:
                return converted_parts[0] if converted_parts else title
        
        # For mixed case titles, handle parentheses and clean up
        else:
            # First handle parenthetical content
            title = re.sub(r'\(([^)]+)\)', format_parenthetical, title)
            
            # Split by words and capitalize appropriately
            # But preserve parenthetical content
            def process_non_paren_text(text):
                words = text.split()
                title_words = []
                
                # Common Vietnamese words that should stay lowercase (unless first word)
                lowercase_words = {'và', 'của', 'cho', 'với', 'từ', 'đến', 'trong', 'ngoài', 'về', 'theo'}
                
                for i, word in enumerate(words):
                    if i == 0 or word.lower() not in lowercase_words:
                        # Capitalize first letter of each major word
                        title_words.append(word.capitalize())
                    else:
                        # Keep connecting words lowercase
                        title_words.append(word.lower())
                
                return ' '.join(title_words)
            
            # Process text outside parentheses
            parts = re.split(r'(\([^)]+\))', title)
            processed_parts = []
            for part in parts:
                if part.startswith('(') and part.endswith(')'):
                    # Keep parenthetical as-is (already formatted) but ensure space before
                    if processed_parts and not processed_parts[-1].endswith(' '):
                        processed_parts.append(' ' + part)
                    else:
                        processed_parts.append(part)
                else:
                    # Process regular text
                    processed_parts.append(process_non_paren_text(part))
            
            return ''.join(processed_parts)
    
    @staticmethod
    def _remove_truncated_ending(title: str) -> str:
        """Remove truncated words at the end of title using general heuristics."""
        if not title:
            return ""
        
        words = title.strip().split()
        if len(words) < 2:
            return title
        
        last_word = words[-1]
        
        # Heuristics to detect truncated words:
        # 1. Very short words (1-2 characters) at the end that don't make sense
        # 2. Words that end with unusual character combinations
        # 3. Words that are likely incomplete based on context
        
        is_truncated = False
        
        # Check if last word is suspiciously short and might be truncated
        if len(last_word) <= 2 and not last_word.isdigit():
            # Common single/double letters that indicate truncation in Vietnamese
            if last_word in ['Ch', 'Nhữ', 'Khu', 'T', 'Đồ', 'Đơ', 'C', 'N', 'K', 'D']:
                is_truncated = True
            # But preserve valid short words
            elif last_word.upper() not in ['A', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']:
                # Check context - if previous word suggests truncation
                if len(words) >= 2:
                    second_last = words[-2].lower()
                    if second_last in ['không', 'tặng', 'và', '-', 'sentence']:
                        is_truncated = True
        
        # Check for 3-letter words that might be truncated
        elif len(last_word) == 3:
            # If the word before is a connector and this looks incomplete
            if len(words) >= 2:
                second_last = words[-2].lower()
                # More specific check for 3-letter truncations
                if (second_last in ['của'] and 
                    not last_word.isdigit() and 
                    last_word.upper() not in ['ABC', 'XYZ', 'DVD', 'VCD']):
                    # Could be author initials being truncated
                    if len(last_word) == 3 and last_word.isupper():
                        pass  # Keep author initials like ABC
                    else:
                        is_truncated = True
        
        # Remove the truncated word if detected
        if is_truncated:
            return ' '.join(words[:-1])
        
        return title
    
    @staticmethod
    def extract_price(price_text: str) -> str:
        """Extract and normalize price."""
        if not price_text:
            return ""
        
        # Remove currency symbols and normalize
        price = re.sub(r'[^\d,.]', '', price_text)
        return price.strip()
    
    @staticmethod
    def extract_author_from_text(content_text: str, patterns: list) -> str:
        """Extract author using regex patterns."""
        for pattern in patterns:
            match = re.search(pattern, content_text, re.IGNORECASE | re.MULTILINE)
            if match:
                author = TextUtils.clean_text(match.group(1).strip())
                # Clean up common suffixes and prefixes
                author = re.sub(r'^\s*[\-\|]+\s*', '', author)  # Remove leading dashes/pipes
                author = re.sub(r'\s*[\-\|]+\s*$', '', author)  # Remove trailing dashes/pipes
                # Ensure it's actually an author name (not technical info)
                if len(author) > 3 and not re.search(r'(kích thước|số trang|mã|giá|isbn|nxb|cm|tr)', author.lower()):
                    return author
        return ""


class URLUtils:
    """Utilities for URL handling."""
    
    @staticmethod
    def normalize_url(url: str, base_url: str) -> str:
        """Normalize URL - convert relative to absolute."""
        if not url:
            return ""
        
        if url.startswith('//'):
            return 'https:' + url
        elif not url.startswith('http') and not url.startswith('data:'):
            return urljoin(base_url, url)
        
        return url


class DelayUtils:
    """Utilities for managing request delays."""
    
    @staticmethod
    def sleep_with_jitter(delay: float, jitter_factor: float = 0.1):
        """Sleep with random jitter to avoid being too predictable."""
        import random
        actual_delay = delay + (random.random() * delay * jitter_factor)
        time.sleep(actual_delay)


class LoggerUtils:
    """Utilities for logging setup."""
    
    @staticmethod
    def setup_logger(name: str, log_level: str = "INFO", log_file: str = None) -> logging.Logger:
        """Set up a logger with the specified configuration."""
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, log_level.upper()))
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler (if specified)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger