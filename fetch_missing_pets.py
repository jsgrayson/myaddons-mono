import json
import requests
import re
import time
import os

MISSING_IDS = [150381, 86067, 4280, 519]

def get_pet_abilities(species_id):
    """Fetches ability names for a species from Wowhead"""
    url = f"https://www.wowhead.com/pet-species/{species_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        print(f"Fetching {species_id}...")
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {species_id}: {response.status_code}")
            return []
        
        # Extract ability IDs from the "abilities" section in the source
        # Pattern: "abilities":[110,360,168,369,1085,706]
        # Or look for "id":123 inside the abilities data
        
        # Wowhead source often has `g_petabilities` or similar.
        # Let's try to find the `abilities` array in the `g_species` or similar block.
        # Or just regex for `"abilities":\[(.*?)\]`
        
        # Actually, scrape_wowhead_abilities.py used names. We need IDs.
        # Let's try to find the ability IDs directly.
        
        # Look for: "abilities":[123,456,...]
        match = re.search(r'"abilities":\[([\d,]+)\]', response.text)
        if match:
            ids_str = match.group(1)
            ids = [int(x) for x in ids_str.split(',')]
            print(f"  Found IDs: {ids}")
            return ids
            
        # Fallback: Look for `g_petabilities` keys if the above fails
        # var g_petabilities = {110:..., 360:...}
        # This lists ALL abilities on the page.
        
        # Let's try a broader regex for the specific species data
        # "id":150381, ... "abilities":[...]
        
        print("  Could not parse abilities array directly.")
        return []

    except Exception as e:
        print(f"  Error: {e}")
        return []

def main():
    # Load existing
    with open('abilities.json', 'r') as f:
        data = json.load(f)
    
    species_abilities = data.get('species_abilities', {})
    
    updated = False
    for pid in MISSING_IDS:
        if str(pid) in species_abilities:
            print(f"Skipping {pid}, already exists.")
            continue
            
        abilities = get_pet_abilities(pid)
        if abilities:
            # Ensure we have 6 (pad with 0 if needed, though usually it's 6)
            # The solver expects list of IDs.
            species_abilities[str(pid)] = abilities
            updated = True
            time.sleep(1)
            
    if updated:
        data['species_abilities'] = species_abilities
        with open('abilities.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("✅ Updated abilities.json")
    else:
        print("No changes made.")

if __name__ == "__main__":
    main()
