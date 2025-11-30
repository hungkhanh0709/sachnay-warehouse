#!/usr/bin/env python3
"""
Script to merge literary awards data into a consolidated awards_by_year.json file.
Supports: Nobel Literature, Pulitzer Fiction, Booker Prize, Goodreads Choice Awards, 
Akutagawa Prize, Hugo Awards, and International Booker Prize.
"""

import json
from pathlib import Path
from typing import Dict, List, Any


def load_json(filepath: Path) -> Dict:
    """Load JSON file and return as dictionary."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict, filepath: Path) -> None:
    """Save dictionary as formatted JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_nobel_award_entry(year: str, year_data: Any) -> Dict:
    """Create simplified award entry for Nobel Prize."""
    award_entry = {
        "award_id": "intl_nobel_literature",
        "laureates": []
    }
    
    # Handle different data structures
    laureates = []
    notes = None
    
    if isinstance(year_data, dict):
        laureates = year_data.get("laureates", [])
        notes = year_data.get("notes")
    elif isinstance(year_data, list):
        # Some years have direct list of laureates
        laureates = year_data
    
    for laureate in laureates:
        laureate_entry = {
            "name": laureate.get("name"),
            "country": laureate.get("country"),
            "language": laureate.get("language"),
            "work_title": None,  # Nobel doesn't specify specific work
            "motivation": laureate.get("motivation"),
            "genre": laureate.get("genre", [])
        }
        award_entry["laureates"].append(laureate_entry)
    
    # Add notes if present
    if notes:
        award_entry["notes"] = notes
    
    return award_entry


def create_pulitzer_award_entry(year: str, year_data: Dict) -> Dict:
    """Create simplified award entry for Pulitzer Prize."""
    award_entry = {
        "award_id": "us_pulitzer_fiction",
        "laureates": []
    }
    
    laureates = year_data.get("laureates", [])
    
    for laureate in laureates:
        laureate_entry = {
            "name": laureate.get("name"),
            "country": "United States",
            "birth_state": laureate.get("birth_state"),
            "work_title": laureate.get("book_title"),
            "publisher": laureate.get("publisher"),
            "year_published": laureate.get("year_published"),
            "motivation": laureate.get("citation"),
            "genre": laureate.get("genre", [])
        }
        
        # Add individual notes if present
        if "notes" in laureate:
            laureate_entry["notes"] = laureate["notes"]
            
        award_entry["laureates"].append(laureate_entry)
    
    # Add award-level notes if present
    if "notes" in year_data:
        award_entry["notes"] = year_data["notes"]
    
    return award_entry


def create_booker_award_entry(year: str, year_data: Dict) -> Dict:
    """Create simplified award entry for Booker Prize."""
    award_entry = {
        "award_id": "uk_booker_prize",
        "laureates": []
    }
    
    laureates = year_data.get("laureates", [])
    
    for laureate in laureates:
        # Convert genre to array if it's a string for consistency
        genre = laureate.get("genre")
        if isinstance(genre, str):
            genre = [genre] if genre else []
        elif genre is None:
            genre = []
        
        laureate_entry = {
            "name": laureate.get("author"),
            "country": laureate.get("nationality"),
            "work_title": laureate.get("book"),
            "publisher": laureate.get("publisher"),
            "genre": genre,
            "judges_chair": laureate.get("judges_chair")
        }
        
        # Add individual notes if present
        if "notes" in laureate:
            laureate_entry["notes"] = laureate["notes"]
            
        award_entry["laureates"].append(laureate_entry)
    
    # Add award-level notes if present
    if "notes" in year_data:
        award_entry["notes"] = year_data["notes"]
    
    return award_entry


def create_goodreads_award_entry(year: str, year_data: Dict) -> Dict:
    """Create Goodreads Choice Awards entry for a year.
    
    Flattens the nested categories structure into a flat list of laureates.
    Each category becomes one laureate entry with category information.
    """
    award_entry = {
        "award_id": "intl_goodreads_choice",
        "laureates": []
    }
    
    # Extract categories
    categories = year_data.get("categories", {})
    
    # Iterate through each category
    for category_key, category_data in categories.items():
        laureate_entry = {}
        
        # Author name (required)
        if "author" in category_data:
            laureate_entry["name"] = category_data["author"]
        
        # Book title (required for Goodreads)
        if "book" in category_data:
            laureate_entry["work_title"] = category_data["book"]
        
        # Category information (e.g., "fiction", "fantasy", "romance")
        laureate_entry["category"] = category_key
        
        # Publisher (optional)
        if "publisher" in category_data and category_data["publisher"]:
            laureate_entry["publisher"] = category_data["publisher"]
        
        # Notes (optional)
        if "notes" in category_data and category_data["notes"]:
            laureate_entry["notes"] = category_data["notes"]
        
        # Special field for audiobook category
        if "narrator" in category_data and category_data["narrator"]:
            laureate_entry["narrator"] = category_data["narrator"]
        
        award_entry["laureates"].append(laureate_entry)
    
    # Add year-level notes if present
    if "notes" in year_data and year_data["notes"]:
        award_entry["notes"] = year_data["notes"]
    
    return award_entry


def create_akutagawa_award_entry(year: str, year_data: Dict) -> Dict:
    """Create Akutagawa Prize entry for a year.
    
    Handles semi-annual award structure with 'edition' field for upper/lower half.
    """
    award_entry = {
        "award_id": "japan_akutagawa",
        "laureates": []
    }
    
    # Extract laureates
    laureates = year_data.get("laureates", [])
    
    for laureate in laureates:
        laureate_entry = {}
        
        # Author name (required)
        if "name" in laureate:
            laureate_entry["name"] = laureate["name"]
        
        # Work title (required)
        if "work_title" in laureate:
            laureate_entry["work_title"] = laureate["work_title"]
        
        # Edition (upper/lower half)
        if "edition" in laureate:
            laureate_entry["edition"] = laureate["edition"]
        
        # Published in (magazine/journal)
        if "published_in" in laureate and laureate["published_in"]:
            laureate_entry["published_in"] = laureate["published_in"]
        
        # Genre
        if "genre" in laureate:
            laureate_entry["genre"] = laureate["genre"]
        
        # English translation
        if "english_translation" in laureate:
            laureate_entry["english_translation"] = laureate["english_translation"]
        
        # Notes
        if "notes" in laureate and laureate["notes"]:
            laureate_entry["notes"] = laureate["notes"]
        
        award_entry["laureates"].append(laureate_entry)
    
    return award_entry


def create_hugo_award_entry(year: str, year_data: Dict) -> Dict:
    """Create Hugo Award entry for a year.
    
    Only includes winners (not finalists) to maintain consistency with other awards.
    Includes Retro-Hugo awards with is_retro flag.
    """
    award_entry = {
        "award_id": "intl_hugo_best_novel",
        "laureates": []
    }
    
    # Extract laureates
    laureates = year_data.get("laureates", [])
    
    for laureate in laureates:
        # Only include winners, skip finalists
        # Note: Retro-Hugo laureates don't have status field, so include them by default
        if "status" in laureate and laureate.get("status") != "winner":
            continue
        
        laureate_entry = {}
        
        # Author name (required)
        if "name" in laureate:
            laureate_entry["name"] = laureate["name"]
        
        # Work title (required)
        if "work_title" in laureate:
            laureate_entry["work_title"] = laureate["work_title"]
        
        # Publisher
        if "publisher" in laureate and laureate["publisher"]:
            laureate_entry["publisher"] = laureate["publisher"]
        
        # Genre
        if "genre" in laureate:
            laureate_entry["genre"] = laureate["genre"]
        
        # Translator (for translated works)
        if "translator" in laureate and laureate["translator"]:
            laureate_entry["translator"] = laureate["translator"]
        
        # Original language
        if "original_language" in laureate and laureate["original_language"]:
            laureate_entry["original_language"] = laureate["original_language"]
        
        # Retro-Hugo flag and awarded year
        if laureate.get("is_retro", False):
            laureate_entry["is_retro"] = True
            if "retro_awarded_year" in laureate:
                laureate_entry["retro_awarded_year"] = laureate["retro_awarded_year"]
        
        # Notes
        if "notes" in laureate and laureate["notes"]:
            laureate_entry["notes"] = laureate["notes"]
        
        award_entry["laureates"].append(laureate_entry)
    
    return award_entry


def create_man_booker_international_award_entry(year: str, year_data: Dict) -> Dict:
    """Create Man Booker International Prize entry for a year.
    
    Handles both lifetime achievement awards (2005-2015) and translated fiction awards (2016+).
    """
    award_entry = {
        "award_id": "intl_man_booker_international",
        "laureates": []
    }
    
    # Extract laureates
    laureates = year_data.get("laureates", [])
    phase = year_data.get("phase", "translated_fiction")
    
    for laureate in laureates:
        laureate_entry = {}
        
        # Author name (required)
        if "name" in laureate:
            laureate_entry["name"] = laureate["name"]
        
        # Work title (for translated fiction phase)
        if "work_title" in laureate:
            laureate_entry["work_title"] = laureate["work_title"]
        
        # Original title
        if "original_title" in laureate and laureate["original_title"]:
            laureate_entry["original_title"] = laureate["original_title"]
        
        # Translator (for translated fiction phase)
        if "translator" in laureate and laureate["translator"]:
            laureate_entry["translator"] = laureate["translator"]
        
        # Translator country
        if "translator_country" in laureate and laureate["translator_country"]:
            laureate_entry["translator_country"] = laureate["translator_country"]
        
        # Translators (for lifetime achievement phase with multiple translators)
        if "translators" in laureate and laureate["translators"]:
            laureate_entry["translators"] = laureate["translators"]
        
        # Country
        if "country" in laureate:
            laureate_entry["country"] = laureate["country"]
        
        # Original language
        if "original_language" in laureate:
            laureate_entry["original_language"] = laureate["original_language"]
        
        # Publisher (for translated fiction phase)
        if "publisher" in laureate and laureate["publisher"]:
            laureate_entry["publisher"] = laureate["publisher"]
        
        # Genre
        if "genre" in laureate:
            laureate_entry["genre"] = laureate["genre"]
        
        # Award phase (lifetime_achievement or translated_fiction)
        if phase:
            laureate_entry["award_phase"] = phase
        
        # Notes
        if "notes" in laureate and laureate["notes"]:
            laureate_entry["notes"] = laureate["notes"]
        
        award_entry["laureates"].append(laureate_entry)
    
    return award_entry


def merge_awards_by_year(nobel_data: Dict, pulitzer_data: Dict, booker_data: Dict, goodreads_data: Dict, akutagawa_data: Dict, hugo_data: Dict, man_booker_intl_data: Dict) -> Dict:
    """Merge awards data by year into simplified structure."""
    # Get all years
    nobel_years = set(nobel_data.get("laureates_by_year", {}).keys())
    pulitzer_years = set(pulitzer_data.get("laureates_by_year", {}).keys())
    booker_years = set(booker_data.get("laureates_by_year", {}).keys())
    goodreads_years = set(goodreads_data.get("laureates_by_year", {}).keys())
    akutagawa_years = set(akutagawa_data.get("laureates_by_year", {}).keys())
    hugo_years = set(hugo_data.get("laureates_by_year", {}).keys())
    man_booker_intl_years = set(man_booker_intl_data.get("laureates_by_year", {}).keys())
    all_years = sorted(nobel_years | pulitzer_years | booker_years | goodreads_years | akutagawa_years | hugo_years | man_booker_intl_years)
    
    # Initialize result with simplified structure
    result = {}
    
    # Statistics tracking
    stats = {
        "years_all_seven_awarded": 0,
        "years_all_six_awarded": 0,
        "years_all_five_awarded": 0,
        "years_all_four_awarded": 0,
        "years_all_three_awarded": 0,
        "years_nobel_pulitzer": 0,
        "years_nobel_booker": 0,
        "years_pulitzer_booker": 0,
        "years_only_nobel": 0,
        "years_only_pulitzer": 0,
        "years_only_booker": 0,
        "years_only_goodreads": 0,
        "years_only_akutagawa": 0,
        "years_only_hugo": 0,
        "years_only_man_booker_intl": 0,
        "years_none_awarded": 0,
        "total_laureates": 0
    }
    
    for year in all_years:
        # Check which awards are present this year
        has_nobel = year in nobel_years
        has_pulitzer = year in pulitzer_years
        has_booker = year in booker_years
        has_goodreads = year in goodreads_years
        has_akutagawa = year in akutagawa_years
        has_hugo = year in hugo_years
        has_man_booker_intl = year in man_booker_intl_years
        
        # Create awards array for this year
        awards = []
        year_laureates = 0
        
        # Add Nobel if present
        if has_nobel:
            nobel_year_data = nobel_data["laureates_by_year"][year]
            nobel_entry = create_nobel_award_entry(year, nobel_year_data)
            awards.append(nobel_entry)
            year_laureates += len(nobel_entry["laureates"])
        
        # Add Pulitzer if present
        if has_pulitzer:
            pulitzer_year_data = pulitzer_data["laureates_by_year"][year]
            pulitzer_entry = create_pulitzer_award_entry(year, pulitzer_year_data)
            awards.append(pulitzer_entry)
            year_laureates += len(pulitzer_entry["laureates"])
        
        # Add Booker if present
        if has_booker:
            booker_year_data = booker_data["laureates_by_year"][year]
            booker_entry = create_booker_award_entry(year, booker_year_data)
            awards.append(booker_entry)
            year_laureates += len(booker_entry["laureates"])
        
        # Add Goodreads if present
        if has_goodreads:
            goodreads_year_data = goodreads_data["laureates_by_year"][year]
            goodreads_entry = create_goodreads_award_entry(year, goodreads_year_data)
            awards.append(goodreads_entry)
            year_laureates += len(goodreads_entry["laureates"])
        
        # Add Akutagawa if present
        if has_akutagawa:
            akutagawa_year_data = akutagawa_data["laureates_by_year"][year]
            akutagawa_entry = create_akutagawa_award_entry(year, akutagawa_year_data)
            awards.append(akutagawa_entry)
            year_laureates += len(akutagawa_entry["laureates"])
        
        # Add Hugo if present
        if has_hugo:
            hugo_year_data = hugo_data["laureates_by_year"][year]
            hugo_entry = create_hugo_award_entry(year, hugo_year_data)
            awards.append(hugo_entry)
            year_laureates += len(hugo_entry["laureates"])
        
        # Add Man Booker International if present
        if has_man_booker_intl:
            man_booker_intl_year_data = man_booker_intl_data["laureates_by_year"][year]
            man_booker_intl_entry = create_man_booker_international_award_entry(year, man_booker_intl_year_data)
            awards.append(man_booker_intl_entry)
            year_laureates += len(man_booker_intl_entry["laureates"])
        
        # Store awards array directly under year key
        result[year] = awards
        
        # Update statistics - now tracking 7 awards
        awards_count = sum([has_nobel, has_pulitzer, has_booker, has_goodreads, has_akutagawa, has_hugo, has_man_booker_intl])
        
        if awards_count == 7:
            stats["years_all_seven_awarded"] += 1
        elif awards_count == 6:
            stats["years_all_six_awarded"] += 1
        elif awards_count == 5:
            stats["years_all_five_awarded"] += 1
        elif awards_count == 4:
            stats["years_all_four_awarded"] += 1
        elif awards_count == 3:
            stats["years_all_three_awarded"] += 1
        elif awards_count == 2:
            if has_nobel and has_pulitzer:
                stats["years_nobel_pulitzer"] += 1
            elif has_nobel and has_booker:
                stats["years_nobel_booker"] += 1
            elif has_pulitzer and has_booker:
                stats["years_pulitzer_booker"] += 1
        elif awards_count == 1:
            if has_nobel:
                stats["years_only_nobel"] += 1
            elif has_pulitzer:
                stats["years_only_pulitzer"] += 1
            elif has_booker:
                stats["years_only_booker"] += 1
            elif has_goodreads:
                stats["years_only_goodreads"] += 1
            elif has_akutagawa:
                stats["years_only_akutagawa"] += 1
            elif has_hugo:
                stats["years_only_hugo"] += 1
            elif has_man_booker_intl:
                stats["years_only_man_booker_intl"] += 1
        else:
            stats["years_none_awarded"] += 1
        
        stats["total_laureates"] += year_laureates
    
    return result, stats


def main():
    """Main function to merge award data."""
    
    # Define paths
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / "output"
    
    nobel_file = output_dir / "nobel_literature.json"
    pulitzer_file = output_dir / "pulitzer_fiction.json"
    booker_file = output_dir / "booker_prize.json"
    goodreads_file = output_dir / "goodreads_choice.json"
    akutagawa_file = output_dir / "akutagawa_prize.json"
    hugo_file = output_dir / "hugo_awards.json"
    man_booker_intl_file = output_dir / "man_booker_international.json"
    output_file = output_dir / "awards_by_year.json"
    
    print("Loading data files...")
    nobel_data = load_json(nobel_file)
    pulitzer_data = load_json(pulitzer_file)
    booker_data = load_json(booker_file)
    goodreads_data = load_json(goodreads_file)
    akutagawa_data = load_json(akutagawa_file)
    hugo_data = load_json(hugo_file)
    man_booker_intl_data = load_json(man_booker_intl_file)
    
    print("Merging awards by year...")
    awards_by_year, stats = merge_awards_by_year(nobel_data, pulitzer_data, booker_data, goodreads_data, akutagawa_data, hugo_data, man_booker_intl_data)
    
    # Get sorted years from the result
    sorted_years = sorted(awards_by_year.keys())
    
    # Create final structure
    final_data = {
        "metadata": {
            "title": "Tổng hợp Giải thưởng Văn học Theo Năm",
            "title_en": "Literary Awards by Year",
            "description": "Tổng hợp các giải thưởng văn học lớn được trao theo từng năm, giúp có cái nhìn tổng quan về xu hướng văn học thế giới",
            "created_date": "2024-11-30",
            "version": "7.0",
            "data_sources": [
                "nobel_literature.json",
                "pulitzer_fiction.json",
                "booker_prize.json",
                "goodreads_choice.json",
                "akutagawa_prize.json",
                "hugo_awards.json",
                "man_booker_international.json"
            ],
            "awards_included": [
                {
                    "id": "intl_nobel_literature",
                    "name": "Nobel Prize in Literature",
                    "country": "Sweden",
                    "scope": "international",
                    "established": 1901
                },
                {
                    "id": "us_pulitzer_fiction",
                    "name": "Pulitzer Prize for Fiction",
                    "country": "United States",
                    "scope": "national",
                    "established": 1918
                },
                {
                    "id": "uk_booker_prize",
                    "name": "The Booker Prize",
                    "country": "United Kingdom",
                    "scope": "international",
                    "established": 1969
                },
                {
                    "id": "intl_goodreads_choice",
                    "name": "Goodreads Choice Awards",
                    "country": "United States",
                    "scope": "international",
                    "established": 2009
                },
                {
                    "id": "japan_akutagawa",
                    "name": "Akutagawa Prize",
                    "country": "Japan",
                    "scope": "national",
                    "established": 1935
                },
                {
                    "id": "intl_hugo_best_novel",
                    "name": "Hugo Award for Best Novel",
                    "country": "United States",
                    "scope": "international",
                    "established": 1953
                },
                {
                    "id": "intl_man_booker_international",
                    "name": "International Booker Prize",
                    "country": "United Kingdom",
                    "scope": "international",
                    "established": 2005
                }
            ],
            "years_covered": f"{sorted_years[-1]}-{sorted_years[0]}",
            "total_years": len(sorted_years),
            "notes": "File này tổng hợp đầy đủ dữ liệu từ các file giải thưởng riêng lẻ. Có thể mở rộng thêm các giải khác như Prix Goncourt, Man Asian Literary Prize, v.v."
        },
        "awards_by_year": awards_by_year,
        "statistics": {
            "total_years_in_dataset": len(sorted_years),
            "years_with_data": len(sorted_years),
            "years_all_seven_awarded": stats["years_all_seven_awarded"],
            "years_all_six_awarded": stats["years_all_six_awarded"],
            "years_all_five_awarded": stats["years_all_five_awarded"],
            "years_all_four_awarded": stats["years_all_four_awarded"],
            "years_all_three_awarded": stats["years_all_three_awarded"],
            "years_nobel_pulitzer": stats["years_nobel_pulitzer"],
            "years_nobel_booker": stats["years_nobel_booker"],
            "years_pulitzer_booker": stats["years_pulitzer_booker"],
            "years_only_nobel": stats["years_only_nobel"],
            "years_only_pulitzer": stats["years_only_pulitzer"],
            "years_only_booker": stats["years_only_booker"],
            "years_only_goodreads": stats["years_only_goodreads"],
            "years_only_akutagawa": stats["years_only_akutagawa"],
            "years_only_hugo": stats["years_only_hugo"],
            "years_only_man_booker_intl": stats["years_only_man_booker_intl"],
            "years_none_awarded": stats["years_none_awarded"],
            "total_laureates_all_awards": stats["total_laureates"],
            "nobel_stats": {
                "total_years": len(nobel_data["laureates_by_year"]),
                "years_awarded": nobel_data["statistics"]["years_awarded"],
                "years_not_awarded": len(nobel_data["statistics"]["not_awarded_years"]),
                "total_laureates": nobel_data["statistics"]["total_laureates"]
            },
            "pulitzer_stats": {
                "total_years": pulitzer_data["award_info"]["total_years"],
                "years_awarded": pulitzer_data["statistics"]["years_awarded"],
                "years_not_awarded": pulitzer_data["statistics"]["years_not_awarded"],
                "total_laureates": pulitzer_data["statistics"]["total_authors"]
            },
            "booker_stats": {
                "total_years": len(booker_data["laureates_by_year"]),
                "years_awarded": booker_data["statistics"]["total_awards"],
                "total_laureates": booker_data["statistics"]["total_laureates"]
            },
            "goodreads_stats": {
                "total_years": goodreads_data["statistics"]["years_awarded"],
                "total_categories": goodreads_data["statistics"]["total_categories"],
                "total_laureates": goodreads_data["statistics"]["years_awarded"] * 15  # Approximate
            },
            "akutagawa_stats": {
                "total_years": len(akutagawa_data["laureates_by_year"]),
                "total_editions": akutagawa_data["statistics"]["total_editions"],
                "total_laureates": akutagawa_data["statistics"]["total_laureates"]
            },
            "hugo_stats": {
                "total_years": len(hugo_data["laureates_by_year"]),
                "total_laureates": hugo_data["statistics"]["combined_totals"]["total_laureates"]
            },
            "man_booker_intl_stats": {
                "total_years": len(man_booker_intl_data["laureates_by_year"]),
                "total_laureates": man_booker_intl_data["statistics"]["total_laureates"]
            }
        },
        "usage_notes": {
            "purpose": "Tổng hợp các giải thưởng văn học lớn theo năm để dễ dàng so sánh và phân tích xu hướng",
            "structure": "Mỗi năm có danh sách các giải thưởng được trao, mỗi giải có thể có nhiều người nhận (laureates)",
            "expansion": "File này có thể mở rộng thêm các giải như Prix Goncourt, Man Asian Literary Prize, v.v.",
            "benefits": [
                "Xem tổng quan giải thưởng theo năm",
                "So sánh xu hướng văn học giữa các khu vực",
                "Phát hiện năm có nhiều giải thưởng đặc biệt",
                "Dễ dàng tìm kiếm theo năm cụ thể",
                "Hỗ trợ phân tích thống kê và data mining"
            ]
        }
    }
    
    # Add the year data
    for year in sorted_years:
        final_data[year] = awards_by_year[year]
    
    print(f"Saving merged data to {output_file}...")
    save_json(final_data, output_file)
    
    print("\n✅ Merge completed successfully!")
    print(f"📊 Statistics:")
    print(f"   - Total years: {len(sorted_years)} ({sorted_years[-1]}-{sorted_years[0]})")
    print(f"   - Years all seven awarded: {stats['years_all_seven_awarded']}")
    print(f"   - Years all six awarded: {stats['years_all_six_awarded']}")
    print(f"   - Years all five awarded: {stats['years_all_five_awarded']}")
    print(f"   - Years all four awarded: {stats['years_all_four_awarded']}")
    print(f"   - Years all three awarded: {stats['years_all_three_awarded']}")
    print(f"   - Years Nobel + Pulitzer: {stats['years_nobel_pulitzer']}")
    print(f"   - Years Nobel + Booker: {stats['years_nobel_booker']}")
    print(f"   - Years Pulitzer + Booker: {stats['years_pulitzer_booker']}")
    print(f"   - Years only Nobel: {stats['years_only_nobel']}")
    print(f"   - Years only Pulitzer: {stats['years_only_pulitzer']}")
    print(f"   - Years only Booker: {stats['years_only_booker']}")
    print(f"   - Years only Goodreads: {stats['years_only_goodreads']}")
    print(f"   - Years only Akutagawa: {stats['years_only_akutagawa']}")
    print(f"   - Years only Hugo: {stats['years_only_hugo']}")
    print(f"   - Years only Man Booker Intl: {stats['years_only_man_booker_intl']}")
    print(f"   - Years none awarded: {stats['years_none_awarded']}")
    print(f"   - Total laureates: {stats['total_laureates']}")
    print(f"\n📚 Award-specific stats:")
    print(f"   - Nobel: {nobel_data['statistics']['total_laureates']} laureates")
    print(f"   - Pulitzer: {pulitzer_data['statistics']['total_authors']} laureates")
    print(f"   - Booker: {booker_data['statistics']['total_laureates']} laureates")
    print(f"   - Goodreads: {goodreads_data['statistics']['years_awarded']} years across {goodreads_data['statistics']['total_categories']} categories")
    print(f"   - Akutagawa: {akutagawa_data['statistics']['total_laureates']} laureates across {akutagawa_data['statistics']['total_editions']} editions")
    print(f"   - Hugo: {hugo_data['statistics']['combined_totals']['total_laureates']} laureates")
    print(f"   - Man Booker International: {man_booker_intl_data['statistics']['total_laureates']} laureates")


if __name__ == "__main__":
    main()
