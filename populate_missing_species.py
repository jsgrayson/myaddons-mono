import json
import sqlite3

def populate_missing_species():
    print("--- POPULATING MISSING SPECIES ---")
    
    # Load species data
    with open('species_data.json', 'r') as f:
        species_data = json.load(f)
    
    conn = sqlite3.connect('petweaver.db')
    cursor = conn.cursor()
    
    # Get IDs used in strategies that aren't in species table
    cursor.execute('''
        SELECT DISTINCT pet1_species FROM strategies WHERE pet1_species > 0
        UNION
        SELECT DISTINCT pet2_species FROM strategies WHERE pet2_species > 0
        UNION
        SELECT DISTINCT pet3_species FROM strategies WHERE pet3_species > 0
    ''')
    
    strategy_ids = set(row[0] for row in cursor.fetchall())
    print(f"Found {len(strategy_ids)} unique pet IDs in strategies")
    
    # Get IDs already in species table
    cursor.execute('SELECT species_id FROM species')
    existing_ids = set(row[0] for row in cursor.fetchall())
    print(f"Species table has {len(existing_ids)} entries")
    
    # Find missing IDs
    missing_ids = strategy_ids - existing_ids
    print(f"Missing {len(missing_ids)} species")
    
    # Add missing species
    added = 0
    for species_id in missing_ids:
        str_id = str(species_id)
        if str_id in species_data:
            info = species_data[str_id]
            cursor.execute('''
                INSERT OR IGNORE INTO species (species_id, name, family_id, family_name, source_text)
                VALUES (?, ?, ?, ?, ?)
            ''', (species_id, info.get('name'), info.get('family_id'), 
                  info.get('family_name'), info.get('source_text', '')))
            added += 1
    
    conn.commit()
    conn.close()
    
    print(f"✓ Added {added} missing species to database")
    print(f"Note: {len(missing_ids) - added} IDs not found in species_data.json (likely NPC IDs)")

if __name__ == "__main__":
    populate_missing_species()
