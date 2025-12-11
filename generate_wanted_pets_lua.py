"""
Generate PetWeaverWanted.lua from missing_pets_summary table.
This file allows the in-game addon to know which wild pets are needed.
"""

import sqlite3
import os

def generate_wanted_pets_lua():
    print("Generating PetWeaverWanted.lua...")
    
    db_path = 'petweaver.db'
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get missing pets from summary table
    # We only care about pets that can be caught (source=1 usually means Drop, 2=Quest, 3=Vendor, 4=Profession, 5=Wild)
    # Actually, let's just dump all missing pets and let the addon filter or just alert on any match
    # But for "Wild Pet Alert", we specifically care about wild pets.
    # The 'source' column in species table might help, but let's check what we have in summary.
    
    # Check columns in missing_pets_summary
    cursor.execute('PRAGMA table_info(missing_pets_summary)')
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Summary table columns: {columns}")
    
    # We need species_id and name. Source would be good if available.
    cursor.execute('SELECT species_id, name, source, strategy_count FROM missing_pets_summary ORDER BY strategy_count DESC')
    rows = cursor.fetchall()
    
    # Load market data
    market_data = {}
    market_path = '../goblin-clean-1/market_data.json'
    if os.path.exists(market_path):
        try:
            with open(market_path, 'r') as f:
                market_json = json.load(f)
                # Assuming structure is {itemID: {marketValue: 12345}} or similar
                # Or maybe {speciesID: value}? Let's assume itemID for now, which is tricky for pets.
                # If it's species based, great. If not, we might skip for now.
                pass 
        except:
            print("Error loading market data")

    # For now, let's just add a placeholder for value integration
    # We'll query the species table to get all species, not just missing ones, to check for value
    
    lua_content = "-- PetWeaverWanted.lua\n-- Generated list of pets needed for strategies or high value\n\n"
    lua_content += "PetWeaverWanted = {\n"
    
    # Track added species to avoid duplicates
    added_species = set()
    
    count = 0
    
    # 1. Add Missing Pets (Strategy Priority)
    for row in rows:
        species_id, name, source, strategy_count = row
        safe_name = name.replace("'", "\\'")
        
        lua_content += f"    [{species_id}] = {{name='{safe_name}', count={strategy_count}, source='{source}', value=0}},\n"
        lua_content += f"    ['{safe_name}'] = {{id={species_id}, count={strategy_count}, value=0}},\n"
        added_species.add(species_id)
        count += 1
        
    # 2. Add High Value Pets (Value Priority) - Placeholder for now
    # If we had market data, we'd loop through it here and add any species not in added_species
    # with value > 5000
    
    lua_content += "}\n"
    
    output_path = 'PetWeaver/PetWeaverWanted.lua'
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write(lua_content)
        
    print(f"✓ Generated {output_path} with {count} wanted pets")
    conn.close()

if __name__ == "__main__":
    import json # Added import
    generate_wanted_pets_lua()
