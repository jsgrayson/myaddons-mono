#!/usr/bin/env python3
"""
Scrape abilities for specific species from WoWHead
Targets only the 5 owned species missing ability data
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import re

# The 5 species we need
TARGET_SPECIES = {
    849: "Chi-Ji Kite",
    850: "Yu'lon Kite", 
    1514: "Mystical Spring Bouquet",
    1937: "Wondrous Wisdomball",
    1978: "Dutiful Squire"
}

def scrape_wowhead_abilities(species_id, species_name):
    """Scrape abilities from WoWHead for a specific pet species"""
    url = f"https://www.wowhead.com/battle-pet/{species_id}"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"  ❌ Failed to fetch {species_name}: HTTP {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # WoWHead embeds data in JavaScript - look for ability data
        # Pattern: abilities:[ability_id,ability_id,...]
        script_text = response.text
        
        # Try to find ability IDs in the page source
        # Look for patterns like: "abilities":[1,2,3,4,5,6]
        ability_pattern = r'"abilities"\s*:\s*\[([0-9,\s]+)\]'
        match = re.search(ability_pattern, script_text)
        
        if match:
            ability_ids_str = match.group(1)
            ability_ids = [int(x.strip()) for x in ability_ids_str.split(',') if x.strip()]
            return ability_ids
        
        print(f"  ⚠️  Could not find abilities for {species_name}")
        return None
        
    except Exception as e:
        print(f"  ❌ Error scraping {species_name}: {e}")
        return None

def main():
    print("🕷️  Scraping abilities for 5 missing species from WoWHead...")
    
    conn = sqlite3.connect('petweaver.db')
    cursor = conn.cursor()
    
    found_count = 0
    failed_count = 0
    
    for species_id, species_name in TARGET_SPECIES.items():
        print(f"\nFetching: {species_name} (ID: {species_id})")
        
        ability_ids = scrape_wowhead_abilities(species_id, species_name)
        
        if ability_ids and len(ability_ids) > 0:
            print(f"  ✅ Found {len(ability_ids)} abilities: {ability_ids}")
            
            # Insert into database
            for slot, ability_id in enumerate(ability_ids, start=1):
                cursor.execute('''
                    INSERT OR IGNORE INTO species_abilities (species_id, ability_id, slot)
                    VALUES (?, ?, ?)
                ''', (species_id, ability_id, slot))
            
            conn.commit()
            found_count += 1
        else:
            failed_count += 1
        
        # Be respectful to WoWHead servers
        time.sleep(1)
    
    print(f"\n📊 Results:")
    print(f"  Found: {found_count}/{len(TARGET_SPECIES)}")
    print(f"  Failed: {failed_count}/{len(TARGET_SPECIES)}")
    
    # Verify final coverage
    cursor.execute('''
        SELECT COUNT(DISTINCT p.species_id), 
               COUNT(DISTINCT CASE WHEN sa.species_id IS NOT NULL THEN p.species_id END)
        FROM pets p
        LEFT JOIN species_abilities sa ON p.species_id = sa.species_id
    ''')
    
    total, with_abilities = cursor.fetchone()
    print(f"\n✅ Owned pets with abilities: {with_abilities}/{total} ({with_abilities/total*100:.1f}%)")
    
    conn.close()

if __name__ == "__main__":
    main()
