import json
import os

def load_data():
    print("Loading data...")
    try:
        with open('abilities.json', 'r') as f:
            ability_data = json.load(f)
            # Handle structure if it's nested
            if 'species_abilities' in ability_data:
                species_abilities = {int(k): v for k, v in ability_data.get('species_abilities', {}).items()}
                abilities_db = ability_data.get('abilities', {})
            else:
                # Fallback if structure is different (based on grep output it seemed flat or nested)
                # But run_sequential_search.py uses 'species_abilities' key.
                species_abilities = {}
                abilities_db = ability_data
    except FileNotFoundError:
        print("Error: abilities.json not found")
        return None, None, None, None

    try:
        with open('species_data.json', 'r') as f:
            species_db = json.load(f)
    except FileNotFoundError:
        print("Error: species_data.json not found")
        return None, None, None, None

    try:
        with open('my_pets.json', 'r') as f:
            user_data = json.load(f)
            user_species_ids = set()
            for pet in user_data.get('pets', []):
                if 'species' in pet and 'id' in pet['species']:
                    user_species_ids.add(pet['species']['id'])
    except FileNotFoundError:
        print("Error: my_pets.json not found")
        return None, None, None, None
        
    return species_abilities, abilities_db, species_db, user_species_ids

if __name__ == "__main__":
    species_abilities, abilities_db, species_db, user_species_ids = load_data()
    
    if not species_abilities:
        print("Failed to load species_abilities. Exiting.")
        exit(1)

    # Define Winning Teams
    # 1. Pricklefury Hare (3272)
    # Abilities: Scratch (118), Dodge (312), Burrow (159)
    # Pool: [118, 312, 159, ...] (We'll use the full pool from species_abilities)
    
    # 2. Tiny Goldfish (652)
    # Abilities: [118, 230, 513, 509, 123, 297]
    
    targets = [3272, 652]
    
    for tid in targets:
        tname = species_db.get(str(tid), {}).get('name', 'Unknown')
        
        print(f"\n--------------------------------------------------")
        print(f"Searching for substitutes for: {tname} (ID: {tid})")
        
        # Get target's full ability pool
        t_abilities = set(species_abilities.get(tid, []))
        if not t_abilities:
            # Try string key
            t_abilities = set(species_abilities.get(str(tid), []))
            
        # Get ability names for display
        ability_names = []
        for ab_id in t_abilities:
            ab_info = abilities_db.get(str(ab_id), {})
            name = ab_info.get('name', str(ab_id))
            ability_names.append(name)
            
        print(f"  Ability Pool: {', '.join(ability_names)}")
        
        found_subs = []
        
        for sid, s_abilities in species_abilities.items():
            sid = int(sid)
            if sid == tid:
                continue
                
            # Check overlap
            s_abilities_set = set(s_abilities)
            
            # Loose: Must share at least 3 abilities (likely the same moveset)
            common = t_abilities.intersection(s_abilities_set)
            if len(common) >= 3:
                found_subs.append((sid, len(common)))
        
        # Sort by overlap count (descending)
        found_subs.sort(key=lambda x: x[1], reverse=True)
        
        # Filter by User Collection
        owned_subs = [s for s in found_subs if s[0] in user_species_ids]
        
        print(f"  Found {len(found_subs)} total substitutes (sharing 3+ abilities).")
        print(f"  You own {len(owned_subs)} of them:")
        
        for sid, count in owned_subs:
            sname = species_db.get(str(sid), {}).get('name', 'Unknown')
            print(f"    - {sname} (ID: {sid}) - Shares {count} abilities")
            
        if not owned_subs and found_subs:
            print(f"  (Unowned substitutes: {len(found_subs) - len(owned_subs)} others)")
