#!/usr/bin/env python3
"""
Convert Xu-Fu strategies to encounters.json format with full NPC pet data.
This script parses strategies_enhanced.json and creates comprehensive encounter definitions.
"""

import json
import re
from collections import defaultdict

def extract_npc_info_from_script(script):
    """
    Parse Xu-Fu script to extract NPC pet information.
    Scripts use ability IDs like: use(Curse of Doom:218)
    """
    ability_pattern = re.compile(r'(?:use|ability)\(([^:]+):(\d+)\)')
    abilities_found = []
    
    for match in ability_pattern.finditer(script):
        ability_name = match.group(1)
        ability_id = int(match.group(2))
        abilities_found.append({'name': ability_name, 'id': ability_id})
    
    return abilities_found

def load_ability_stats():
    """Load manual ability stats"""
    try:
        with open('ability_stats_manual.json', 'r') as f:
            data = json.load(f)
            return data.get('abilities', {})
    except FileNotFoundError:
        print("WARNING: ability_stats_manual.json not found")
        return {}

def convert_xufu_to_encounters():
    """Main conversion function"""
    print("Loading Xu-Fu strategies...")
    with open('strategies_enhanced.json', 'r') as f:
        xufu_data = json.load(f)
    
    ability_stats = load_ability_stats()
    encounters = {}
    conversion_stats = defaultdict(int)
    
    # Priority encounters to convert first
    priority_encounters = [
        "Squirt",
        "Aki the Chosen",
        "Wise Mari",
        "Jeremy Feasel",
        "Christoph VonFeasel"
    ]
    
    for expansion, categories in xufu_data.items():
        for category, encounter_list in categories.items():
            for encounter_data in encounter_list:
                encounter_name = encounter_data['encounter_name']
                strategies = encounter_data.get('strategies', [])
                
                if not strategies:
                    conversion_stats['no_strategies'] += 1
                    continue
                
                # Use first strategy as the canonical one
                strategy = strategies[0]
                script = strategy.get('script', '')
                
                if not script:
                    conversion_stats['no_script'] += 1
                    continue
                
                # Extract abilities from script
                npc_abilities = extract_npc_info_from_script(script)
                
                if not npc_abilities:
                    conversion_stats['no_abilities_found'] += 1
                    continue
                
                # Create encounter ID (lowercase, underscores)
                encounter_id = encounter_name.lower().replace(' ', '_').replace('(', '').replace(')', '')
                encounter_id = re.sub(r'[^a-z0-9_]', '', encounter_id)
                
                # Build NPC pets (placeholder - would need more data from Wowhead/Blizzard API)
                # For now, create based on script analysis
                npc_pets = []
                
                # Heuristic: Group abilities into 3 pets (typical team size)
                abilities_per_pet = max(1, len(npc_abilities) // 3)
                for i in range(3):
                    start_idx = i * abilities_per_pet
                    end_idx = start_idx + abilities_per_pet if i < 2 else len(npc_abilities)
                    pet_abilities_subset = npc_abilities[start_idx:end_idx]
                    
                    if not pet_abilities_subset:
                        break
                    
                    # Build abilities with stats
                    abilities = []
                    for idx, ab in enumerate(pet_abilities_subset[:3]):  # Max 3 abilities per slot
                        ability_id_str = str(ab['id'])
                        if ability_id_str in ability_stats:
                            stats = ability_stats[ability_id_str]
                            abilities.append({
                                'id': ab['id'],
                                'name': stats.get('name', ab['name']),
                                'slot': idx + 1,
                                'power': stats.get('power', 20),
                                'accuracy': stats.get('accuracy', 100),
                                'speed': stats.get('speed', 0),
                                'cooldown': stats.get('cooldown', 0)
                            })
                        else:
                            # Use defaults if not in manual stats
                            abilities.append({
                                'id': ab['id'],
                                'name': ab['name'],
                                'slot': idx + 1,
                                'power': 20,
                                'accuracy': 100,
                                'speed': 0,
                                'cooldown': 0
                            })
                    
                    # Create NPC pet with placeholder stats
                    # TODO: Get real stats from Blizzard API or Wowhead
                    npc_pets.append({
                        'name': f"NPC Pet {i+1}",
                        'species_id': 1000 + i,  # Placeholder
                        'level': 25,
                        'quality': 'rare',
                        'family': 'Unknown',
                        'health': 1546,
                        'power': 273,
                        'speed': 273,
                        'abilities': abilities
                    })
                
                if npc_pets:
                    encounters[encounter_id] = {
                        'name': encounter_name,
                        'note': f"Converted from XuFu {expansion} - {category}",
                        'npc_pets': npc_pets
                    }
                    conversion_stats['converted'] += 1
                    
                    if any(priority in encounter_name for priority in priority_encounters):
                        conversion_stats['priority_converted'] += 1
    
    print(f"\nConversion Statistics:")
    print(f"  Total converted: {conversion_stats['converted']}")
    print(f"  Priority encounters: {conversion_stats['priority_converted']}")
    print(f"  Skipped (no strategies): {conversion_stats['no_strategies']}")
    print(f"  Skipped (no script): {conversion_stats['no_script']}")
    print(f"  Skipped (no abilities): {conversion_stats['no_abilities_found']}")
    
    # Save to file
    output_file = 'encounters_converted.json'
    with open(output_file, 'w') as f:
        json.dump(encounters, f, indent=2)
    
    print(f"\n✅ Saved {len(encounters)} encounters to {output_file}")
    print(f"File size: {len(json.dumps(encounters)) / 1024:.1f} KB")
    
    return encounters

if __name__ == "__main__":
    convert_xufu_to_encounters()
