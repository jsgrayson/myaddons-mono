"""
Decode PetTracker Stables Data

Analyzes and decodes the Addon.Stables table from PetTracker data.
"""

import json
import re
from pettracker_decoder import PetTrackerDecoder

def parse_stables(lua_content):
    """Extract Stables table"""
    match = re.search(r'Addon\.Stables=\{([^}]+)\}', lua_content)
    if not match:
        return {}
    
    content = match.group(1)
    stables = {}
    
    # Parse [id]="encoded"
    for match in re.finditer(r'\[(\d+)\]="([^"]+)"', content):
        map_id = int(match.group(1))
        encoded = match.group(2)
        stables[map_id] = encoded
        
    return stables

def main():
    with open('/Users/jgrayson/Documents/petweaver/pettracker_data_source.lua', 'r') as f:
        lua_content = f.read()
        
    stables = parse_stables(lua_content)
    print(f"Found {len(stables)} maps with stable data")
    
    decoder = PetTrackerDecoder()
    
    # Decode a few samples
    for map_id, encoded in list(stables.items())[:5]:
        print(f"\nMap {map_id}: {encoded}")
        
        # Try chunk size 2
        decoded_2 = decoder.decode_base36(encoded) # Uses chunk size 2 by default now
        print(f"  Decoded (Chunk 2): {decoded_2}")
        
        # Try to interpret the numbers
        # Are they NPC IDs? Species IDs?
        # 64330 is Julia Stevens.
        
        # Let's see if any match RivalOrder IDs
        
    # Extract RivalOrder for comparison
    rival_match = re.search(r'Addon\.RivalOrder=\{([^}]+)\}', lua_content)
    if rival_match:
        rivals = [int(x) for x in re.findall(r'\d+', rival_match.group(1))]
        print(f"\nFound {len(rivals)} Rivals in RivalOrder")
        print(f"Sample Rivals: {rivals[:5]}")
        
        # Check if decoded values match rivals
        matches = 0
        total = 0
        for encoded in stables.values():
            decoded = decoder.decode_base36(encoded)
            for val in decoded:
                total += 1
                if val in rivals:
                    matches += 1
        
        print(f"\nMatch rate with RivalOrder: {matches}/{total} ({matches/total*100:.1f}%)")

if __name__ == "__main__":
    main()
