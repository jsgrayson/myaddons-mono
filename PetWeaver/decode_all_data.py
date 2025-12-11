"""
Decode All PetTracker Data

Decodes the parsed PetTracker data using the identified Base-36 encoding (chunk size 2).
Validates the results against known ability IDs from abilities.json.
"""

import json
import os
import sys
from pettracker_decoder import PetTrackerDecoder

def main():
    # Load parsed PetTracker data
    try:
        with open('/Users/jgrayson/Documents/petweaver/pettracker_data.json', 'r') as f:
            pt_data = json.load(f)
    except FileNotFoundError:
        print("Error: pettracker_data.json not found. Run parse_pettracker_data.py first.")
        return

    # Load known abilities for validation
    known_ability_ids = set()
    try:
        with open('/Users/jgrayson/Documents/petweaver/abilities.json', 'r') as f:
            abilities_data = json.load(f)
            # Extract all ability IDs from the nested structure
            for species_id, abilities in abilities_data.get('species_abilities', {}).items():
                for ability_id in abilities:
                    known_ability_ids.add(ability_id)
        print(f"Loaded {len(known_ability_ids)} known ability IDs for validation")
    except FileNotFoundError:
        print("Warning: abilities.json not found. Validation will be skipped.")

    decoder = PetTrackerDecoder()
    
    decoded_species = {}
    total_abilities = 0
    valid_abilities = 0
    
    print("Decoding species data...")
    
    species_abilities = pt_data.get('species_abilities', {})
    
    for species_id, abilities in species_abilities.items():
        decoded_slots = {}
        
        # Handle both dict and list formats
        if isinstance(abilities, dict):
            items = abilities.items()
        elif isinstance(abilities, list):
            items = enumerate(abilities) # Lists are 0-indexed in Python, but slots might be 1-based
        else:
            continue
            
        for slot, encoded in items:
            if not isinstance(encoded, str):
                continue
                
            try:
                decoded_ids = decoder.decode_base36(encoded)
                decoded_slots[slot] = decoded_ids
                
                # Validation
                for aid in decoded_ids:
                    total_abilities += 1
                    if aid in known_ability_ids:
                        valid_abilities += 1
                        
            except Exception as e:
                print(f"Error decoding species {species_id} slot {slot}: {e}")
        
        if decoded_slots:
            decoded_species[species_id] = decoded_slots
            
    # Calculate match rate
    match_rate = (valid_abilities / total_abilities * 100) if total_abilities > 0 else 0
    print(f"\nDecoding Complete:")
    print(f"  Total decoded abilities: {total_abilities}")
    print(f"  Valid abilities (found in abilities.json): {valid_abilities}")
    print(f"  Match Rate: {match_rate:.2f}%")
    
    # Construct final dataset
    final_data = {
        "species": decoded_species,
        "breeds": pt_data.get('species_breeds', {}),
        "stats": pt_data.get('species_stats', {}),
        "metadata": {
            "source": "PetTracker addon",
            "decoding": "Base-36, chunk size 2",
            "match_rate": f"{match_rate:.2f}%",
            "timestamp": "2025-11-23"
        }
    }
    
    output_path = '/Users/jgrayson/Documents/petweaver/pettracker_decoded.json'
    with open(output_path, 'w') as f:
        json.dump(final_data, f, indent=2)
        
    print(f"\nSaved decoded data to: {output_path}")

if __name__ == "__main__":
    main()
