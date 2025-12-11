import json
import csv
from pathlib import Path
from collections import defaultdict

CSV_FILE = Path("wow_tamer_abilities.csv")
ABILITIES_FILE = Path("abilities.json")
OUTPUT_FILE = Path("encounters.json")

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def normalize(text):
    return str(text).lower().strip()

def main():
    print("Loading databases...")
    ability_data = load_json(ABILITIES_FILE)
    abilities_db = ability_data.get('abilities', {})
    
    # Create Name -> Info map for fast lookup
    print("Indexing ability names...")
    name_to_info = {}
    for aid, info in abilities_db.items():
        if 'name' in info:
            name_to_info[normalize(info['name'])] = info
            # Also store ID
            name_to_info[str(aid)] = info

    print(f"Indexed {len(name_to_info)} keys.")

    # Parse CSV
    # Format: Tamer Name,Species ID,Abil1,Abil2,Abil3,Abil4,Abil5,Abil6
    encounters = defaultdict(list)
    
    print(f"Reading {CSV_FILE}...")
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader) # Skip header
            
            for row in reader:
                if len(row) < 3: continue
                
                tamer_name = row[0]
                species_id = int(row[1])
                ability_names = row[2:] # List of ability names
                
                # Build Pet Object
                pet_abilities = []
                for ab_name in ability_names:
                    if not ab_name or ab_name == "Bandage": continue # Skip empty/meta
                    
                    # Lookup
                    info = name_to_info.get(normalize(ab_name))
                    if info:
                        pet_abilities.append({
                            "id": int(info['id']),
                            "name": info['name'],
                            "cooldown": info.get("cooldown", 0),
                            "type": info.get("family_id", 7)
                        })
                    else:
                        print(f"[WARN] Unknown ability '{ab_name}' for {tamer_name}")
                        # Placeholder to prevent crash
                        pet_abilities.append({"id": 0, "name": ab_name, "cooldown": 0})

                # Select first 3 as active loadout (Standard NPC AI)
                # Or keep all 6 and let AI choose? Simulator expects 3 active.
                # We'll take the first 3 non-zero ones.
                active_loadout = pet_abilities[:3]
                
                new_pet = {
                    "name": f"Pet {species_id}", # Generic name if CSV lacks it
                    "species_id": species_id,
                    "abilities": active_loadout
                }
                
                encounters[tamer_name].append(new_pet)
                
    except FileNotFoundError:
        print("CSV file not found!")
        return

    # Construct final JSON
    final_list = []
    for tamer, pets in encounters.items():
        final_list.append({
            "name": tamer,
            "pets": pets
        })

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_list, f, indent=2)
        
    print(f"✅ Rebuilt {OUTPUT_FILE} with {len(final_list)} encounters.")
    print(f"   Sample: {final_list[0]['name']} has {len(final_list[0]['pets'])} pets.")

if __name__ == "__main__":
    main()
