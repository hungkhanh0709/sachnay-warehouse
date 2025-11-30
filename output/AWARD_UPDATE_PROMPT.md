# Literary Awards Update Instructions

## Context
You are tasked with checking and updating the literary awards database for the current year. 
The database tracks major international literary awards with a standardized structure.

## Current Awards Tracked

1. **Nobel Prize in Literature** (`intl_nobel_literature`)
   - Country: Sweden | Scope: International
   - Usually announced: October
   - File: `output/nobel_literature.json`

2. **Pulitzer Prize for Fiction** (`us_pulitzer_fiction`)
   - Country: United States | Scope: National
   - Usually announced: May
   - File: `output/pulitzer_fiction.json`

3. **The Booker Prize** (`uk_booker_prize`)
   - Country: United Kingdom | Scope: International
   - Usually announced: October/November
   - File: `output/booker_prize.json`

4. **Goodreads Choice Awards** (`intl_goodreads_choice`)
   - Country: United States | Scope: International
   - Usually announced: December
   - File: `output/goodreads_choice.json`

5. **Akutagawa Prize** (`japan_akutagawa`)
   - Country: Japan | Scope: National
   - Announced: Semi-annually (January & July)
   - File: `output/akutagawa_prize.json`

6. **Hugo Award for Best Novel** (`intl_hugo_best_novel`)
   - Country: United States | Scope: International
   - Usually announced: August (Worldcon)
   - File: `output/hugo_awards.json`

7. **International Booker Prize** (`intl_man_booker_international`)
   - Country: United Kingdom | Scope: International
   - Usually announced: May
   - File: `output/booker_prize_international.json`

## Task: Check and Update 2025 Awards

### Step 1: Identify Missing Awards for 2025

Check each award file to see if year 2025 exists and has complete data:

```bash
# Check structure for each file
cd output
for file in nobel_literature.json pulitzer_fiction.json booker_prize.json goodreads_choice.json akutagawa_prize.json hugo_awards.json booker_prize_international.json; do
    echo "Checking $file for 2025..."
    python3 -c "import json; data=json.load(open('$file')); print('2025' in data.get('laureates_by_year', {}))"
done
```

### Step 2: Search for Award Winners

For each missing or incomplete award, search for official announcements:

**Search Query Templates:**
- "Nobel Prize in Literature 2025 winner"
- "Pulitzer Prize Fiction 2025 winner"
- "Booker Prize 2025 winner"
- "Goodreads Choice Awards 2025 Fiction winner"
- "Akutagawa Prize 2025 upper half winner" (January)
- "Akutagawa Prize 2025 lower half winner" (July)
- "Hugo Award Best Novel 2025 winner"
- "International Booker Prize 2025 winner"

### Step 3: Data Structure Requirements

**For awards with work structure (All except Nobel):**

```json
{
  "laureates_by_year": {
    "2025": {
      "laureates": [
        {
          "name": "Author Name",
          "work": {
            "title": "Book Title",
            "translations": {}
          },
          "country": "Author's Country",
          "genre": ["Genre1", "Genre2"],
          "notes": "Any special notes (optional)"
        }
      ]
    }
  }
}
```

**For translated works (Akutagawa, International Booker):**

```json
{
  "name": "Author Name",
  "work": {
    "title": "English Title",
    "original_title": "Original Title (if different)",
    "original_language": "Original Language",
    "translator": "Translator Name",
    "translations": {}
  },
  "country": "Author's Country",
  "genre": ["Genre1", "Genre2"]
}
```

**For Nobel Prize (No work structure):**

```json
{
  "laureates_by_year": {
    "2025": {
      "laureates": [
        {
          "name": "Author Name",
          "country": "Country",
          "language": "Writing Language",
          "motivation": "Official motivation text",
          "genre": ["Genre1", "Genre2"]
        }
      ]
    }
  }
}
```

**For Goodreads (Multiple categories):**

```json
{
  "laureates_by_year": {
    "2025": {
      "laureates": [
        {
          "name": "Author Name",
          "work": {
            "title": "Book Title",
            "translations": {}
          },
          "category": "fiction",
          "notes": "Any special notes (optional)"
        },
        {
          "name": "Author Name 2",
          "work": {
            "title": "Book Title 2",
            "translations": {}
          },
          "category": "fantasy"
        }
        // ... repeat for all categories
      ]
    }
  }
}
```

### Step 4: Award-Specific Fields

**Pulitzer Fiction:**
- Required: `name`, `work.title`, `year_published`, `citation`
- Optional: `birth_state`, `notes`

**Booker Prize:**
- Required: `name`, `work.title`, `country`, `genre`
- Optional: `judges_chair`, `notes`

**Akutagawa Prize:**
- Required: `name`, `work.title`, `edition` (e.g., "174th (2025 Upper Half)")
- Optional: `published_in`, `genre`, `notes`

**Hugo Awards:**
- Required: `name`, `work.title`, `genre`
- Optional: `notes`, `is_retro` (for Retro-Hugo)

**International Booker:**
- Required: `name`, `work.title`, `work.original_title`, `work.translator`, `work.original_language`, `country`, `genre`
- Optional: `translator_country`, `notes`

### Step 5: Update Process

1. **Read the current file:**
   ```python
   import json
   with open('output/AWARD_FILE.json', 'r', encoding='utf-8') as f:
       data = json.load(f)
   ```

2. **Add 2025 data:**
   ```python
   data['laureates_by_year']['2025'] = {
       "laureates": [
           # ... new laureate data
       ]
   }
   ```

3. **Update statistics if needed:**
   - Increment counters
   - Update year ranges
   - Add to totals

4. **Write back:**
   ```python
   with open('output/AWARD_FILE.json', 'w', encoding='utf-8') as f:
       json.dump(data, f, ensure_ascii=False, indent=2)
   ```

5. **Regenerate consolidated file:**
   ```bash
   python3 src/merge_awards_by_year.py
   ```

### Step 6: Verification

After updating, verify the structure:

```python
import json

files = [
    'nobel_literature.json',
    'pulitzer_fiction.json', 
    'booker_prize.json',
    'goodreads_choice.json',
    'akutagawa_prize.json',
    'hugo_awards.json',
    'booker_prize_international.json'
]

for filename in files:
    with open(f'output/{filename}', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if '2025' in data.get('laureates_by_year', {}):
        year_data = data['laureates_by_year']['2025']
        laureates = year_data.get('laureates', [])
        print(f"✅ {filename}: 2025 has {len(laureates)} laureate(s)")
        
        # Check structure
        if laureates:
            sample = laureates[0]
            has_name = 'name' in sample
            has_work = 'work' in sample
            print(f"   - Has name: {has_name}")
            if has_work:
                work = sample['work']
                print(f"   - Work title: {work.get('title', 'MISSING')[:50]}")
                print(f"   - Has translations: {'translations' in work}")
    else:
        print(f"⚠️  {filename}: 2025 data missing")
```

## Important Notes

### Data Quality Guidelines

1. **Author Names:**
   - Use full official name
   - For Japanese: Use romanization (e.g., "Haruki Murakami")
   - Include both names if joint winners

2. **Book Titles:**
   - Use official English title for `work.title`
   - Use original title for `work.original_title` (if translated)
   - Keep original script when available (Japanese, Korean, etc.)

3. **Genres:**
   - Always use array format: `["Genre1", "Genre2"]`
   - Use consistent genre names (check existing data)
   - Common genres: Literary fiction, Historical fiction, Science fiction, Fantasy, etc.

4. **Countries:**
   - Use standard country names
   - For dual nationality: "Country1 / Country2"

5. **Translations Field:**
   - Always initialize as empty dict: `{}`
   - Do NOT populate it during update
   - Will be filled later with Vietnamese translations

### Special Cases

1. **No Award Given:**
   ```json
   "2025": {
     "laureates": [],
     "notes": "No award given in 2025"
   }
   ```

2. **Joint Winners:**
   ```json
   "2025": {
     "laureates": [
       {
         "name": "Author 1",
         "work": {...},
         "notes": "Joint winner"
       },
       {
         "name": "Author 2",
         "work": {...},
         "notes": "Joint winner"
       }
     ],
     "notes": "First joint winners since..."
   }
   ```

3. **Posthumous Awards:**
   ```json
   {
     "name": "Author Name",
     "work": {...},
     "notes": "Posthumous award. Author died on YYYY-MM-DD"
   }
   ```

### Common Errors to Avoid

❌ **DON'T:**
- Use `work_title` field (old structure)
- Include `publisher` field (removed)
- Use `original` or `primary` nested structures (removed)
- Leave `translations` as null (use empty dict `{}`)
- Use inconsistent field names across awards

✅ **DO:**
- Use `work.title` for all book titles
- Keep `translations` as empty dict
- Use flat structure for work object
- Follow award-specific required fields
- Maintain consistent genre naming

## Example Complete Update

### Example: Adding Pulitzer 2025

```json
{
  "laureates_by_year": {
    "2025": {
      "laureates": [
        {
          "name": "Percival Everett",
          "work": {
            "title": "James",
            "translations": {}
          },
          "country": "United States",
          "birth_state": "South Carolina",
          "year_published": 2024,
          "citation": "A daring retelling of a literary classic that interrogates legacy, race, and freedom",
          "genre": ["Literary fiction", "Historical fiction"],
          "notes": "Retelling of Mark Twain's Huckleberry Finn from Jim's perspective"
        }
      ]
    }
  }
}
```

### Example: Adding International Booker 2025

```json
{
  "laureates_by_year": {
    "2025": {
      "laureates": [
        {
          "name": "Banu Mushtaq",
          "work": {
            "title": "Heart Lamp: Selected Stories",
            "original_title": "ಎದೆಯ ಹಣತೆ",
            "original_language": "Kannada",
            "translator": "Deepa Bhasthi",
            "translations": {}
          },
          "country": "India",
          "translator_country": "India",
          "genre": ["Short stories", "Literary fiction"],
          "notes": "First Kannada work to win the International Booker Prize"
        }
      ]
    }
  }
}
```

## Execution Checklist

- [ ] Check current date and determine which awards have been announced
- [ ] Search for official winner announcements
- [ ] Verify winner information from multiple reliable sources
- [ ] Prepare data in correct JSON structure
- [ ] Update individual award file(s)
- [ ] Update statistics in award file(s)
- [ ] Regenerate `awards_by_year.json` using merge script
- [ ] Verify all updates using verification script
- [ ] Commit changes with descriptive message

## References

- Official websites listed in each award file's `metadata` section
- Wikipedia pages for historical data verification
- Publisher websites for book details
- Goodreads for genre classification

---

**Last Updated:** 2025-11-30  
**Database Version:** 7.0  
**Structure Version:** Simplified (post-refactor)
