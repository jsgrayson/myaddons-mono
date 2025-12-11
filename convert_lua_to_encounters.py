#!/usr/bin/env python3
"""
Convert P PetWeaverData.lua (which has REAL species IDs) to encounters.json format.
This uses YOUR OWN ADDON DATA which is 100% real game data.
"""

import re
import json

def parse_lua_encounters():
    """Parse the Lua file to extract encounter data"""
    
    with open('PetWeaver/PetWeaverData.lua', 'r') as f:
        lua_content = f.read()
    
    encounters = {}
    
    # Regex to match encounter blocks
    encounter_pattern = re.compile(
        r'\["([^"]+)"\]\s*=\s*\{([^}]+pet1[^}]+)\}',
        re.DOTALL
    )
    
    for match in encounter_pattern.finditer(lua_content):
        encounter_name = match.group(1)
        encounter_block = match.group(2)
        
        # Extract pet species IDs
        pet1 = re.search(r'pet1\s*=\s*(\d+)', encounter_block)
        pet2 = re.search(r'pet2\s*=\s*(\d+)', encounter_block)
        pet3 = re.search(r'pet3\s*=\s*(\d+)', encounter_block)
        
        # Extract script
        script_match = re.search(r'script\s*=\s*"([^"]*)"', encounter_block, re.DOTALL)
        
        if not (pet1 and pet2 and pet3 and script_match):
            continue
        
        species_ids = [
            int(pet1.group(1)),
            int(pet2.group(1)) if pet2 else 0,
            int(pet3.group(1)) if pet3 else 0
        ]
        
        # Filter out zero IDs
        species_ids = [sid for sid in species_ids if sid > 0]
        
        if len(species_ids) < 1:  # Need at least one pet
            continue
        
        script = script_match.group(1)
        
        # Create encounter ID
        enc_id = encounter_name.lower().replace(' ', '_').replace("'", '').replace(':', '').replace('(', '').replace(')', '')
        enc_id = re.sub(r'[^a-z0-9_]', '', enc_id)
        
        encounters[enc_id] = {
            'name': encounter_name,
            'note': f"Real data from PetWeaver addon - Player strategy using species {', '.join(map(str, species_ids))}",
            'player_strategy': {
                'pet_species': species_ids,
                'script': script
            }
        }
    
    return encounters

def main():
    print("Converting PetWeaverData.lua to encounters.json...")
    print("="*60)
    
    encounters = parse_lua_encounters()
    
    print(f"✅ Parsed {len(encounters)} encounters from PetWeaverData.lua")
    print(f"\nSample encounters:")
    for i, (enc_id, data) in enumerate(list(encounters.items())[:5]):
        print(f"  - {enc_id}: {data['name']}")
        print(f"    Species: {data['player_strategy']['pet_species']}")
    
    # Save
    with open('encounters_from_lua.json', 'w') as f:
        json.dump(encounters, f, indent=2)
    
    print(f"\n✅ Saved to encounters_from_lua.json")
    print(f"File size: {len(json.dumps(encounters)) / 1024:.1f} KB")
    print(f"\nThese are REAL SPECIES IDs from your addon!")
    
if __name__ == "__main__":
    main()
