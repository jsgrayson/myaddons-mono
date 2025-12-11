#!/usr/bin/env python3
"""
Create a practical encounters.json with real ability data but generic NPC teams.
Focus on quality over quantity - start with key encounters.
"""

import json

def create_practical_encounters():
    """Create encounters with REAL abilities but simplified NPC data"""
    
    # Load manual ability stats
    with open('ability_stats_manual.json', 'r') as f:
        ability_stats = json.load(f)['abilities']
    
    # Load converted encounters
    with open('encounters_converted.json', 'r') as f:
        converted = json.load(f)
    
    # Priority encounters to include (manually verify these later)
    priority_encounters = [
        'squirt',  # Already has real data
        'aki_the_chosen',
        'wise_mari', 
        'jeremy_feasel',
        'christoph_vonfeasel'
    ]
    
    # Start with real Squirt data
    with open('encounters.json', 'r') as f:
        encounters = json.load(f)
    
    # For other encounters, use the ability data but generic teams
    for enc_id in priority_encounters:
        if enc_id in encounters:
            continue  # Skip if already exists (like Squirt)
        
        if enc_id in converted:
            # Use converted data - it has REAL abilities
            encounters[enc_id] = converted[enc_id]
            encounters[enc_id]['note'] += " - NPC names are generic, abilities are real"
    
    # Save
    with open('encounters_practical.json', 'w') as f:
        json.dump(encounters, f, indent=2)
    
    print(f"✅ Created encounters_practical.json with {len(encounters)} encounters")
    print(f"   - 1 with full real data (Squirt)")
    print(f"   - {len(encounters)-1} with real abilities, generic NPC names")
    print(f"\nFile size: {len(json.dumps(encounters)) / 1024:.1f} KB")
    
    return encounters

if __name__ == "__main__":
    create_practical_encounters()
