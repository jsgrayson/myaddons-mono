"""
Comprehensive Enemy Moveset Deduction

Analyzes ALL battle scripts to build a complete enemy ability database
by identifying patterns in what abilities players defend against.
"""

import json
import re
from collections import defaultdict, Counter

def extract_enemy_abilities_from_conditions(conditions):
    """Extract enemy abilities mentioned in script conditions."""
    enemy_abilities = []
    
    for condition in conditions:
        # Pattern: enemy.aura(AbilityName:ID)
        aura_matches = re.findall(r'enemy\.aura\(([^:]+):(\d+)\)', condition)
        for ability_name, ability_id in aura_matches:
            enemy_abilities.append({
                'ability_id': int(ability_id),
                'ability_name': ability_name,
                'source': 'aura_check',
                'condition': condition
            })
        
        # Pattern: enemy ability references in conditions
        if 'enemy' in condition:
            # Look for ability IDs
            ability_refs = re.findall(r':(\d+)', condition)
            for ability_id in ability_refs:
                enemy_abilities.append({
                    'ability_id': int(ability_id),
                    'ability_name': 'Unknown',
                    'source': 'enemy_condition',
                    'condition': condition
                })
    
    return enemy_abilities

def analyze_all_encounters(data):
    """Analyze all encounters to build enemy ability database."""
    
    enemy_database = {}
    
    for encounter_url, encounter_data in data.items():
        encounter_name = encounter_data['encounter_name']
        variations = encounter_data.get('variations', [])
        
        if not variations:
            continue
        
        enemy_abilities = defaultdict(lambda: {
            'count': 0,
            'conditions': [],
            'names': Counter()
        })
        
        player_counters = Counter()
        
        for var in variations:
            script = var.get('script', '')
            if not script:
                continue
            
            lines = script.split('\\n')
            for line in lines:
                if not line.strip():
                    continue
                
                # Extract conditions
                conditions = re.findall(r'\[([^\]]+)\]', line)
                
                # Find enemy abilities mentioned
                abilities = extract_enemy_abilities_from_conditions(conditions)
                for ability in abilities:
                    ability_id = ability['ability_id']
                    enemy_abilities[ability_id]['count'] += 1
                    enemy_abilities[ability_id]['conditions'].append(ability['condition'])
                    enemy_abilities[ability_id]['names'][ability['ability_name']] += 1
                
                # Track player abilities used
                use_match = re.search(r'use\(([^:]+):(\d+)\)', line)
                if use_match:
                    player_counters[int(use_match.group(2))] += 1
        
        # Build enemy moveset for this encounter
        if enemy_abilities or player_counters:
            enemy_database[encounter_name] = {
                'encounter_url': encounter_url,
                'total_variations': len(variations),
                'enemy_abilities': {
                    ability_id: {
                        'frequency': data['count'],
                        'most_common_name': data['names'].most_common(1)[0][0] if data['names'] else 'Unknown',
                        'example_conditions': list(set(data['conditions']))[:3]
                    }
                    for ability_id, data in enemy_abilities.items()
                },
                'top_player_counters': dict(player_counters.most_common(10))
            }
    
    return enemy_database

def main():
    print("Loading complete battle data...")
    with open('variations_with_scripts_final.json', 'r') as f:
        data = json.load(f)
    
    print(f"Analyzing all {len(data)} encounters for enemy abilities...\n")
    
    enemy_database = analyze_all_encounters(data)
    
    print(f"✅ Analysis complete!")
    print(f"Found enemy ability data for {len(enemy_database)} encounters\n")
    
    # Show sample
    sample_encounters = list(enemy_database.items())[:5]
    for encounter_name, info in sample_encounters:
        print(f"{encounter_name}:")
        print(f"  {len(info['enemy_abilities'])} enemy abilities detected")
        for ability_id, ability_data in list(info['enemy_abilities'].items())[:3]:
            print(f"    - {ability_data['most_common_name']} (ID: {ability_id}) - seen {ability_data['frequency']} times")
        print()
    
    # Save complete database
    output = {
        'generated': '2025-11-26',
        'total_encounters': len(enemy_database),
        'encounters': enemy_database
    }
    
    with open('enemy_abilities_database.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"💾 Saved to: enemy_abilities_database.json")
    
    # Summary stats
    total_abilities_found = sum(len(info['enemy_abilities']) for info in enemy_database.values())
    print(f"\n📊 Summary:")
    print(f"   Encounters analyzed: {len(enemy_database)}")
    print(f"   Total enemy abilities identified: {total_abilities_found}")

if __name__ == "__main__":
    main()
