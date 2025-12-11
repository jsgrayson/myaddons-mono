import json
import csv
import os

def merge_data():
    csv_file = 'wow_tamer_abilities_final.csv'
    json_file = 'encounters_full.json'
    abilities_file = 'abilities.json'
    
    if not os.path.exists(csv_file):
        print(f"❌ {csv_file} not found!")
        return

    # Load abilities.json for looking up full ability data by name
    with open(abilities_file, 'r', encoding='utf-8') as f:
        abilities_data = json.load(f)
        # Map Name -> Ability Object
        ability_lookup = {v['name'].lower(): v for v in abilities_data.get('abilities', {}).values()}

    # Load CSV data
    species_abilities = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) # Skip header
        for row in reader:
            if len(row) < 8: continue
            
            tamer_name = row[0]
            try:
                species_id = int(row[1])
            except ValueError:
                continue
                
            # Abilities are in columns 2-7 (indices 2 to 7)
            # But wait, the CSV header is: Tamer Name, Pet Species ID, Ability 1, ...
            # So indices are 2, 3, 4, 5, 6, 7
            
            ability_names = [row[i] for i in range(2, 8) if row[i]]
            
            # Convert names to full ability objects
            ability_objs = []
            for name in ability_names:
                if name.lower() in ability_lookup:
                    ability_objs.append(ability_lookup[name.lower()])
                else:
                    # Create a placeholder if not found (shouldn't happen often if scraper worked)
                    # But scraper might return "Unknown(123)"
                    if "Unknown" not in name:
                        print(f"⚠️ Ability '{name}' not found in database")
            
            if ability_objs:
                species_abilities[species_id] = ability_objs

    # Update encounters_full.json
    with open(json_file, 'r', encoding='utf-8') as f:
        encounters = json.load(f)
        
    updated_count = 0
    total_pets = 0
    
    for tamer in encounters:
        for pet in tamer['pets']:
            total_pets += 1
            sid = pet['species_id']
            
            if sid in species_abilities:
                pet['abilities'] = species_abilities[sid]
                pet['missing_abilities'] = False
                updated_count += 1
            elif pet.get('missing_abilities') and sid not in species_abilities:
                # Keep it flagged as missing
                pass

    # Save updated JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(encounters, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Merged abilities for {updated_count}/{total_pets} pets")
    print(f"📁 Saved to {json_file}")

if __name__ == "__main__":
    merge_data()
