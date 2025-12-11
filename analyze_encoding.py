"""
Analyze PetTracker Encoding Alphabet

Reads the parsed JSON data and identifies all unique characters used in the encoded strings
to determine the Base-32 alphabet.
"""

import json

def main():
    with open('/Users/jgrayson/Documents/petweaver/pettracker_data.json', 'r') as f:
        data = json.load(f)
        
    species_data = data.get('species_abilities', {})
    
    chars = set()
    for species_id, abilities in species_data.items():
        # Handle list (JSON array) or dict
        values = []
        if isinstance(abilities, list):
            values = abilities
        elif isinstance(abilities, dict):
            values = abilities.values()
            
        for encoded in values:
            if not isinstance(encoded, str):
                continue
            for char in encoded:
                chars.add(char)
                
    sorted_chars = sorted(list(chars))
    print(f"Found {len(sorted_chars)} unique characters:")
    print("".join(sorted_chars))
    
    # Check against standard alphabets
    standard_b32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    crockford_b32 = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
    pettracker_guess = "0123456789ABCDEFGHJKMNPQRSTUVWXYZ" # From my previous guess
    
    print(f"\nStandard Base32 match: {all(c in standard_b32 for c in chars)}")
    print(f"Crockford Base32 match: {all(c in crockford_b32 for c in chars)}")
    print(f"Previous Guess match: {all(c in pettracker_guess for c in chars)}")

if __name__ == "__main__":
    main()
