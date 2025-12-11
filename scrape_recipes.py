#!/usr/bin/env python3
"""
Scrape profession recipe data from Wowhead and populate the database.
Focuses on current expansion (The War Within) recipes.
"""

import os
import psycopg2
import requests
from bs4 import BeautifulSoup
import time
import re

# Configuration
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://jgrayson@localhost/holocron')
WOWHEAD_URL = "https://www.wowhead.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# TWW Professions to scrape - using recipe list URLs
PROFESSIONS = {
    'Alchemy': 'alchemy',
    'Blacksmithing': 'blacksmithing',
    'Enchanting': 'enchanting',
    'Engineering': 'engineering',
    'Inscription': 'inscription',
    'Jewelcrafting': 'jewelcrafting',
    'Leatherworking': 'leatherworking',
    'Tailoring': 'tailoring'
}

# Gathering professions don't have recipes
GATHERING = ['Herbalism', 'Mining', 'Skinning']

def get_db_connection():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def scrape_profession_recipes(profession_name, profession_slug, limit=100):
    """
    Scrape recipes for a given profession from Wowhead recipe pages.
    Uses the /recipes/[profession] page format.
    """
    # Use the crafted-by page which lists items crafted by profession
    url = f"{WOWHEAD_URL}/items/crafted-by:{profession_slug}?filter=166:151;2:9;0:0"  # Filter for TWW items
    print(f"\n🔍 Scraping {profession_name} from {url}")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print(f"  ❌ Failed to fetch page: {response.status_code}")
            return []
        
        # For now, just create some mock recipes based on common TWW items
        # In a real implementation, you'd parse the actual page
        recipes = []
        
        # Mock recipe data for demonstration
        if profession_name == "Alchemy":
            recipes = [
                {'id': 430590, 'name': 'Algari Healing Potion', 'profession': profession_name},
                {'id': 430591, 'name': 'Algari Mana Potion', 'profession': profession_name},
                {'id': 430592, 'name': 'Tempered Potion', 'profession': profession_name},
            ]
        elif profession_name == "Blacksmithing":
            recipes = [
                {'id': 450217, 'name': 'Charged Slicer', 'profession': profession_name},
                {'id': 450218, 'name': 'Charged Facesmasher', 'profession': profession_name},
            ]
        elif profession_name == "Enchanting":
            recipes = [
                {'id': 445336, 'name': 'Enchant Weapon - Authority of Air', 'profession': profession_name},
                {'id': 445337, 'name': 'Enchant Weapon - Authority of Fire', 'profession': profession_name},
            ]
        
        print(f"  ✅ Found {len(recipes)} recipes (mock data)")
        return recipes
    
    except Exception as e:
        print(f"  ❌ Error scraping {profession_name}: {e}")
        return []

def import_recipes_to_db(recipes):
    """Import scraped recipes into the database"""
    conn = get_db_connection()
    if not conn:
        return 0
    
    cur = conn.cursor()
    imported = 0
    
    # First, we need to create a reference table for recipes since goblin.recipes
    # is for character-specific known recipes
    # Let's create a new table for recipe references
    
    try:
        # Create recipe reference table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS goblin.recipe_reference (
                recipe_id INT PRIMARY KEY,
                recipe_name VARCHAR(255),
                profession_name VARCHAR(100),
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        
        # Insert recipes
        for recipe in recipes:
            cur.execute("""
                INSERT INTO goblin.recipe_reference 
                (recipe_id, recipe_name, profession_name)
                VALUES (%s, %s, %s)
                ON CONFLICT (recipe_id) 
                DO UPDATE SET
                    recipe_name = EXCLUDED.recipe_name,
                    last_updated = CURRENT_TIMESTAMP
            """, (recipe['id'], recipe['name'], recipe['profession']))
            imported += 1
        
        conn.commit()
        print(f"\n✅ Imported {imported} recipes into database")
        
    except Exception as e:
        print(f"❌ Error importing recipes: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    
    return imported

def verify_import():
    """Verify the import by querying the database"""
    conn = get_db_connection()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("""
        SELECT profession_name, COUNT(*) as recipe_count
        FROM goblin.recipe_reference
        GROUP BY profession_name
        ORDER BY profession_name
    """)
    
    rows = cur.fetchall()
    
    print("\n📊 Recipe Summary by Profession:")
    print("-" * 50)
    for row in rows:
        print(f"  {row[0]:20} - {row[1]:4} recipes")
    print("-" * 50)
    
    cur.close()
    conn.close()

def main():
    print("=" * 60)
    print("WOWHEAD RECIPE SCRAPER")
    print("=" * 60)
    print("Target: The War Within Professions")
    print("=" * 60)
    
    all_recipes = []
    
    for profession, slug in PROFESSIONS.items():
        recipes = scrape_profession_recipes(profession, slug, limit=50)
        all_recipes.extend(recipes)
        time.sleep(1)  # Polite delay between requests
    
    if all_recipes:
        print(f"\n📝 Total recipes scraped: {len(all_recipes)}")
        imported = import_recipes_to_db(all_recipes)
        
        if imported > 0:
            verify_import()
    else:
        print("\n⚠️  No recipes were scraped.")

if __name__ == "__main__":
    main()
