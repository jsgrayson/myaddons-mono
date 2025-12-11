import json
import sqlite3
import os

def fix_strategies():
    print("--- REPAIRING STRATEGIES TABLE ---")
    
    # 1. Load Species Data
    print("Loading species data...")
    try:
        with open('species_data.json', 'r') as f:
            species_data = json.load(f)
    except FileNotFoundError:
        print("Error: species_data.json not found!")
        return

    # 2. Load Strategies JSON
    print("Loading strategies JSON...")
    try:
        # Use the backup file which has valid team IDs!
        with open('deprecated/variations_with_scripts_merged_OLD.json', 'r') as f:
            strategies_json = json.load(f)
    except FileNotFoundError:
        print("Error: variations_with_scripts_merged_OLD.json not found!")
        return

    # 3. Connect to DB
    conn = sqlite3.connect('petweaver.db')
    cursor = conn.cursor()
    
    # Optional: Clear existing strategies if they are broken?
    # Let's check if we should clear. The user has 282 strategies.
    # The JSON has many more probably.
    # Let's truncate and rebuild to be safe.
    print("Clearing existing strategies...")
    cursor.execute('DELETE FROM strategies')
    
    count = 0
    
    # 4. Process and Insert
    print("Processing strategies...")
    for encounter, variations in strategies_json.items():
        for var in variations:
            team = var.get('team', [0, 0, 0])
            script = var.get('script', '')
            
            # Resolve pets
            pet_names = []
            pet_ids = []
            
            # Check if team is valid (has non-zero IDs)
            has_valid_team = any(pid > 0 for pid in team)
            
            if has_valid_team:
                for pet_id in team:
                    if pet_id == 0:
                        pet_names.append(None)
                        pet_ids.append(None)
                        continue
                    
                    # Try to find name
                    str_id = str(pet_id)
                    if str_id in species_data:
                        name = species_data[str_id].get('name')
                        pet_names.append(name)
                        pet_ids.append(pet_id)
                    else:
                        pet_names.append(f"NPC {pet_id}")
                        pet_ids.append(pet_id)
            else:
                # Fallback: Parse script for pets!
                # Look for change(Name:ID) patterns
                import re
                # Pattern: change(Name:ID) or use(Ability:ID) - actually just look for Name:ID patterns
                # But be careful not to match abilities. 
                # Usually pets appear in change() or if() conditions
                # Example: change(Ikky:1532)
                
                # Find all unique ID matches associated with names
                # We look for :ID) or :ID] patterns preceded by a Name
                matches = re.findall(r'([a-zA-Z0-9\s\-\'\.]+):(\d+)[)\]]', script)
                
                found_pets = {} # ID -> Name
                
                for name, pid_str in matches:
                    pid = int(pid_str)
                    # Check if this ID is a species ID (not an ability ID)
                    # Heuristic: Check if it exists in species_data
                    if str(pid) in species_data:
                        # It's a pet!
                        real_name = species_data[str(pid)].get('name')
                        found_pets[pid] = real_name
                
                # Add found pets to the list (up to 3)
                for pid, name in list(found_pets.items())[:3]:
                    pet_ids.append(pid)
                    pet_names.append(name)
            
            # Pad to 3
            
            # Pad to 3
            while len(pet_names) < 3:
                pet_names.append(None)
                pet_ids.append(None)
            
            # Insert
            cursor.execute('''
                INSERT INTO strategies (
                    encounter_name, encounter_id, 
                    pet1_species, pet1_name,
                    pet2_species, pet2_name,
                    pet3_species, pet3_name,
                    script, is_verified
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            ''', (
                encounter, 0, # encounter_id unknown
                pet_ids[0], pet_names[0],
                pet_ids[1], pet_names[1],
                pet_ids[2], pet_names[2],
                script
            ))
            count += 1
            
    conn.commit()
    conn.close()
    print(f"✓ Successfully restored {count} strategies with pet data!")

if __name__ == "__main__":
    fix_strategies()
