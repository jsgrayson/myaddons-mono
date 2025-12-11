"""
Decode PetTracker Tamer Data

Extracts and decodes Tamer (Rival) data from Addon.RivalInfo.
"""

import json
import re
import os

# Base-36 alphabet
ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def decode_base36(encoded):
    """Decode a single Base-36 string to integer"""
    if not encoded:
        return 0
    try:
        return int(encoded, 36)
    except ValueError:
        return 0

def parse_rival_info(lua_content):
    """Extract RivalInfo table"""
    # Look for Addon.RivalInfo={...}
    # Since it might be on one line or multiple, we need to be careful.
    # The grep output showed it on one line.
    match = re.search(r'Addon\.RivalInfo=\{([^}]+)\}', lua_content)
    if not match:
        print("Could not find Addon.RivalInfo table")
        return {}
    
    content = match.group(1)
    rivals = {}
    
    # Parse [id]="encoded_string"
    # The strings contain colons, so we need a robust regex
    # Pattern: [123]="string",
    pattern = r'\[(\d+)\]="([^"]+)"'
    
    for match in re.finditer(pattern, content):
        npc_id = int(match.group(1))
        encoded_data = match.group(2)
        rivals[npc_id] = encoded_data
        
    return rivals

def decode_rival(npc_id, encoded_data):
    """
    Decode a rival string based on rival.lua format:
    name:model(4):map(2):quest(3):gold(1):items:currencies:pets
    """
    # Regex from rival.lua:
    # ^([^:]+):(%w%w%w%w)(%w%w)(%w%w%w)(%w)([^:]*):([^:]*):(.*)$
    
    # Python regex equivalent
    # Note: %w in Lua is [a-zA-Z0-9]
    pattern = r'^([^:]+):([a-zA-Z0-9]{4})([a-zA-Z0-9]{2})([a-zA-Z0-9]{3})([a-zA-Z0-9])([^:]*):([^:]*):(.*)$'
    
    match = re.match(pattern, encoded_data)
    if not match:
        print(f"Failed to parse rival {npc_id}: {encoded_data[:20]}...")
        return None
        
    name, model_str, map_str, quest_str, gold_str, items_str, currencies_str, pets_str = match.groups()
    
    rival = {
        "id": npc_id,
        "name": name,
        "model": decode_base36(model_str),
        "map_id": decode_base36(map_str),
        "quest_id": decode_base36(quest_str),
        "gold": decode_base36(gold_str),
        "team": []
    }
    
    # Parse pets
    # Lua: ([^:]+):(%w%w%w%w)(%w%w%w)(%w)(%w)
    # Name:Model(4):Specie(3):Level(1):Quality(1)
    pet_pattern = r'([^:]+):([a-zA-Z0-9]{4})([a-zA-Z0-9]{3})([a-zA-Z0-9])([a-zA-Z0-9])'
    
    for pet_match in re.finditer(pet_pattern, pets_str):
        p_name, p_model, p_specie, p_level, p_quality = pet_match.groups()
        
        rival["team"].append({
            "name": p_name,
            "species_id": decode_base36(p_specie),
            "level": decode_base36(p_level),
            "quality": decode_base36(p_quality),
            "model": decode_base36(p_model)
        })
        
    return rival

def main():
    try:
        with open('/Users/jgrayson/Documents/petweaver/pettracker_data_source.lua', 'r') as f:
            lua_content = f.read()
    except FileNotFoundError:
        print("Error: pettracker_data_source.lua not found")
        return

    raw_rivals = parse_rival_info(lua_content)
    print(f"Found {len(raw_rivals)} raw rival entries")
    
    decoded_rivals = []
    for npc_id, encoded in raw_rivals.items():
        rival = decode_rival(npc_id, encoded)
        if rival:
            decoded_rivals.append(rival)
            
    print(f"Successfully decoded {len(decoded_rivals)} rivals")
    
    # Save to JSON
    output_path = '/Users/jgrayson/Documents/petweaver/pettracker_tamers.json'
    with open(output_path, 'w') as f:
        json.dump(decoded_rivals, f, indent=2)
        
    print(f"Saved tamer data to {output_path}")
    
    # Show a sample
    if decoded_rivals:
        print("\nSample Tamer:")
        print(json.dumps(decoded_rivals[0], indent=2))

if __name__ == "__main__":
    main()
