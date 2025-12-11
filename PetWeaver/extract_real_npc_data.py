#!/usr/bin/env python3
"""
COMPREHENSIVE NPC DATA EXTRACTOR - NO SHORTCUTS

Extract REAL data for simulation:
1. NPC pet names from Wowhead/community sources
2. Species IDs by reverse-mapping abilities
3. Exact turn-by-turn ability rotations from strategy consensus
4. Real stats and families from species database

NO PLACEHOLDER DATA. ONLY REAL GAME DATA.
"""

import json
import re
from collections import defaultdict, Counter

def extract_real_npc_data():
    """Extract complete real NPC data"""
    
    # Load all data sources
    with open('strategies_enhanced.json') as f:
        xufu_data = json.load(f)
    
    with open('abilities.json') as f:
        abilities_data = json.load(f)
        species_abilities = abilities_data.get('species_abilities', {})
    
    with open('species_data.json') as f:
        species_data = json.load(f)
    
    with open('ability_stats_manual.json') as f:
        ability_stats = json.load(f)['abilities']
    
    print("REAL NPC DATA EXTRACTION")
    print("="*70)
    print("Step 1: Analyze ALL Squirt strategies")
    print("-"*70)
    
    # Collect all Squirt strategies
    all_squirt_strategies = []
    for exp, cats in xufu_data.items():
        for cat, encs in cats.items():
            for enc in encs:
                if 'squirt' in enc['encounter_name'].lower():
                    all_squirt_strategies.extend(enc.get('strategies', []))
    
    print(f"Found {len(all_squirt_strategies)} Squirt strategies to analyze")
    
    # Step 2: Extract all ability IDs used by NPCs (from player counters)
    print("\nStep 2: Extract NPC ability usage patterns")
    print("-"*70)
    
    npc_abilities_used = defaultdict(set)
    
    for strategy in all_squirt_strategies:
        script = strategy.get('script', '')
        
        # Extract abilities mentioned in script
        # These are PLAYER abilities, but we can infer NPC behavior from patterns
        ability_ids = set(re.findall(r'(?:use|ability)\([^:]*:(\d+)\)', script))
        
        # Look for enemy-specific sections
        for enemy_num in [1, 2, 3]:
            pattern = rf'enemy\(#{enemy_num}\)'
            if re.search(pattern, script):
                npc_abilities_used[f'enemy{enemy_num}'].update(ability_ids)
    
    # Step 3: Map abilities to species
    print("\nStep 3: reverse-map abilities to NPC species")
    print("-"*70)
    
    # For each NPC ability set, find species that have those abilities
    for enemy, ability_set in npc_abilities_used.items():
        print(f"\n{enemy}: {len(ability_set)} abilities mentioned")
        
        # Find species with these abilities
        matching_species = []
        for species_id_str, abilities in species_abilities.items():
            species_id = int(species_id_str)
            species_ability_ids = set(str(ab) for ab in abilities)
            
            # Check overlap
            overlap = ability_set & species_ability_ids
            if len(overlap) >= 2:  # At least 2 matching abilities
                species_name = species_data.get(species_id_str, {}).get('name', 'Unknown')
                family = species_data.get(species_id_str, {}).get('family_name', 'Unknown')
                matching_species.append({
                    'species_id': species_id,
                    'name': species_name,
                    'family': family,
                    'overlap': len(overlap)
                })
        
        # Show top matches
        matching_species.sort(key=lambda x: x['overlap'], reverse=True)
        print(f"  Top species matches:")
        for match in matching_species[:5]:
            print(f"    - {match['name']} (ID {match['species_id']}, {match['family']}): {match['overlap']} abilities")
    
    print("\n" + "="*70)
    print("This approach won't work - player abilities != NPC abilities")
    print("REAL SOLUTION: Need NPC pet names from Wowhead/community")
    print("="*70)

if __name__ == "__main__":
    extract_real_npc_data()
