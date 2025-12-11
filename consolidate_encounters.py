#!/usr/bin/env python3
"""
Consolidate all encounter data into a single clean encounters_complete.json file.
Merges data from:
- strategies.json (scripts)
- pettracker_tamers.json (NPC teams)
- encounters.json (manual entries)
- Known popular encounters (Squirt, etc.)
"""
import json
import os

def main():
    output = {}
    
    # 1. Load pettracker tamers (NPC teams with breed/ability data)
    if os.path.exists('pettracker_tamers.json'):
        with open('pettracker_tamers.json') as f:
            tamers = json.load(f)
            
        for tamer in tamers:
            name = tamer.get('name', 'Unknown')
            key = name.lower().replace(' ', '_').replace("'", '')
            
            output[key] = {
                'name': name,
                'location': tamer.get('location', 'Unknown'),
                'expansion': tamer.get('expansion', 'Unknown'),
                'npc_pets': []
            }
            
            # Convert pettracker team format to standard format
            for pet in tamer.get('team', []):
                output[key]['npc_pets'].append({
                    'species_id': pet.get('species_id'),
                    'breed_id': pet.get('breed_id'),
                    'level': pet.get('level', 25),
                    'abilities': pet.get('abilities', [])
                })
    
    # 2. Load strategies (scripts)
    if os.path.exists('strategies_master.json'):
        with open('strategies_master.json') as f:
            strategies = json.load(f)
            
        for expansion, categories in strategies.items():
            for category, encounters in categories.items():
                for encounter in encounters:
                    name = encounter.get('encounter_name', 'Unknown')
                    key = name.lower().replace(' ', '_').replace("'", '')
                    
                    # Add or update with strategy scripts
                    if key not in output:
                        output[key] = {'name': name}
                    
                    output[key]['strategies'] = encounter.get('strategies', [])
    
    # 3. Add known special encounters (like Squirt) manually
    # Load abilities.json to expand ability IDs
    abilities_db = {}
    if os.path.exists('abilities.json'):
        with open('abilities.json') as f:
            ability_data = json.load(f)
            abilities_db = ability_data.get('abilities', {})
    
    def expand_ability(ab_id):
        """Convert ability ID to full object with stats"""
        ab_info = abilities_db.get(str(ab_id), {})
        return {
            'id': ab_id,
            'name': ab_info.get('name', f'Ability {ab_id}'),
            'power': ab_info.get('power', 20),
            'accuracy': ab_info.get('accuracy', 100),
            'speed': ab_info.get('speed', 0),
            'cooldown': ab_info.get('cooldown', 0),
            'family_id': ab_info.get('family_id', 7)
        }
    
    output['squirt'] = {
        'name': 'Squirt (WoD Garrison)',
        'location': 'Lunarfall/Frostwall Garrison',
        'expansion': 'Warlords of Draenor',
        'type': 'daily_leveling',
        'special_tags': ['super_squirt_day', 'leveling_hotspot', 'repeatable'],
        'notes': 'Spawns during Pet Battle bonus week. Used for power-leveling pets.',
        'npc_pets': [
            {
                'name': 'Deebs',
                'species_id': 1934,
                'level': 25,
                'family': 'Magic',
                'stats': {'health': 1546, 'power': 273, 'speed': 273},
                'abilities': [expand_ability(122), expand_ability(110), expand_ability(120)]
            },
            {
                'name': 'Tyri',
                'species_id': 1935,
                'level': 25,
                'family': 'Humanoid',
                'stats': {'health': 1546, 'power': 273, 'speed': 273},
                'abilities': [expand_ability(115), expand_ability(593), expand_ability(489)]
            },
            {
                'name': 'Puzzle',
                'species_id': 1936,
                'level': 25,
                'family': 'Humanoid',
                'stats': {'health': 1546, 'power': 273, 'speed': 273},
                'abilities': [expand_ability(136), expand_ability(406), expand_ability(125)]
            }
        ],
        'popular_teams': [
            # Add known working teams from community
            {
                'name': 'Iron Starlette + Idol',
                'pets': [1387, 519],  # Iron Starlette, Anubisath Idol
                'notes': '2-pet carry team'
            }
        ]
    }
    
    # Mark other special encounters (Aura of Death, etc.)
    # TODO: Add Shadowlands encounters with Aura of Death mechanic
    
    # 4. Write consolidated file
    with open('encounters_complete.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f'✅ Consolidated {len(output)} encounters into encounters_complete.json')
    print(f'   - {len([e for e in output.values() if "npc_pets" in e])} with NPC teams')
    print(f'   - {len([e for e in output.values() if "strategies" in e])} with strategies')

if __name__ == '__main__':
    main()
