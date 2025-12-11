import requests
import csv
import time
import re
import json
import os

# --- 1. THE MASTER DATABASE ---
# (Same tamer list as before)
# Load tamer data from encounters_full.json
try:
    with open('encounters_full.json', 'r') as f:
        encounters = json.load(f)
        
    tamer_data = []
    skipped_count = 0
    for tamer in encounters:
        name = tamer['name']
        # Only include pets that are missing abilities
        pet_ids = []
        for p in tamer['pets']:
            if p.get('missing_abilities', False):
                pet_ids.append(p['species_id'])
            else:
                skipped_count += 1
                
        if pet_ids:
            tamer_data.append((name, pet_ids))
        
    print(f"Loaded {len(tamer_data)} tamers with missing data (Skipped {skipped_count} known pets)")
except FileNotFoundError:
    print("❌ encounters_full.json not found!")
    tamer_data = []

# Load abilities.json to map IDs to names
try:
    with open('abilities.json', 'r') as f:
        abilities_data = json.load(f)
        # Map ID -> Name
        ability_map = {int(k): v['name'] for k, v in abilities_data.get('abilities', {}).items()}
except FileNotFoundError:
    print("⚠️ abilities.json not found, ability names will be missing!")
    ability_map = {}

def get_pet_abilities(species_id):
    """
    Fetches ability IDs from Wowhead search results using filter=id={species_id}.
    Locates the species object in the response and extracts abilities.
    """
    if not species_id:
        return []
        
    url = f"https://www.wowhead.com/pet-species?filter=id={species_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
            
        text = response.text
        
        # Find "species":species_id or "species": species_id
        # We look for the ID and then expand outwards to find the containing object {}
        # This is safer than regexing the whole Listview
        
        # Pattern to find the species ID key-value pair
        # Matches: species:872, "species":872, species: 872, etc.
        target = f'species["\']?:\s*{species_id}'
        match = re.search(target, text)
        
        if match:
            start_idx = match.start()
            
            # Walk backwards to find the opening brace '{' of this object
            # We need to be careful of nested braces, but this object structure is usually flat-ish
            brace_count = 0
            obj_start = -1
            for i in range(start_idx, -1, -1):
                if text[i] == '}':
                    brace_count += 1
                elif text[i] == '{':
                    if brace_count == 0:
                        obj_start = i
                        break
                    brace_count -= 1
            
            if obj_start != -1:
                # Walk forwards to find the closing brace '}'
                brace_count = 0
                obj_end = -1
                for i in range(obj_start, len(text)):
                    if text[i] == '{':
                        brace_count += 1
                    elif text[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            obj_end = i + 1
                            break
                
                if obj_end != -1:
                    obj_str = text[obj_start:obj_end]
                    
                    # Now extract abilities from this object string
                    # Pattern: "abilities":[1,2,3]
                    abil_match = re.search(r'abilities["\']?:\s*\[([\d,]+)\]', obj_str)
                    if abil_match:
                        ids_str = abil_match.group(1)
                        ids = [int(x) for x in ids_str.split(',')]
                        
                        # Convert IDs to names
                        names = []
                        for aid in ids:
                            name = ability_map.get(aid, f"Unknown({aid})")
                            names.append(name)
                        return names
                        
        return []
        
    except Exception as e:
        print(f"  [!] Error fetching {species_id}: {e}")
        return []

def main():
    print(f"Starting FINAL scrape for {len(tamer_data)} tamers...")
    
    filename = 'wow_tamer_abilities_final.csv'
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Tamer Name", "Pet Species ID", "Ability 1", "Ability 2", "Ability 3", "Ability 4", "Ability 5", "Ability 6"])

        for tamer_name, pet_ids in tamer_data:
            print(f"Processing: {tamer_name}")
            
            for pid in pet_ids:
                if pid == 0: continue
                
                print(f"  - Fetching Species {pid}...", end='', flush=True)
                abilities = get_pet_abilities(pid)
                
                if abilities:
                    print(f" ✅ Found {len(abilities)}: {abilities[:3]}...")
                else:
                    print(f" ❌ Not found")
                
                while len(abilities) < 6:
                    abilities.append("")
                
                row = [tamer_name, pid] + abilities
                writer.writerow(row)
                time.sleep(1.0) # Be polite

    print(f"\nSuccess! Data saved to {filename}")

if __name__ == "__main__":
    main()
