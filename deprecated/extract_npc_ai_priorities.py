#!/usr/bin/env python3
"""
Extract NPC AI ability priorities from existing strategies.

Cross-references strategies with encounters_full.json to determine
which abilities each NPC tamer pet uses most frequently.
"""

import json
import re
from collections import defaultdict, Counter

def extract_npc_priorities():
    """Extract NPC ability usage patterns from all strategies."""
    
    # Load encounters with complete ability data
    with open('encounters_full.json', 'r') as f:
        encounters = json.load(f)
    
    # Create lookup: tamer name -> pets with abilities
    tamer_lookup = {}
    for tamer in encounters:
        tamer_name = tamer['name'].lower()
        tamer_lookup[tamer_name] = {
            'name': tamer['name'],
            'pets': tamer['pets']
        }
    
    # Load strategies
    try:
        with open('strategies_enhanced.json', 'r') as f:
            strategies_data = json.load(f)
    except FileNotFoundError:
        with open('strategies.json', 'r') as f:
            strategies_data = json.load(f)
    
    # Track NPC ability mentions per tamer
    npc_ability_usage = defaultdict(lambda: defaultdict(Counter))
    
    # Analyze all strategies
    strategy_count = 0
    for expansion, categories in strategies_data.items():
        if not isinstance(categories, dict):
            continue
            
        for category, encounters_list in categories.items():
            if not isinstance(encounters_list, list):
                continue
                
            for encounter in encounters_list:
                if not isinstance(encounter, dict):
                    continue
                    
                encounter_name = encounter.get('encounter_name', '').lower()
                
                # Try to match to a tamer
                matched_tamer = None
                for tamer_key, tamer_data in tamer_lookup.items():
                    if tamer_key in encounter_name or encounter_name in tamer_key:
                        matched_tamer = tamer_data
                        break
                
                if not matched_tamer:
                    continue
                
                # Analyze each strategy for this tamer
                for strategy in encounter.get('strategies', []):
                    strategy_count += 1
                    script = strategy.get('script', '')
                    
                    # Look for enemy ability mentions in conditions
                    # Pattern: enemy.ability(ID) or enemy(#N).ability(ID)
                    ability_refs = re.findall(r'enemy(?:\(#(\d+)\))?.ability\(([^)]+)\)', script)
                    
                    for pet_num, ability_ref in ability_refs:
                        # pet_num might be empty if not specified
                        if not pet_num:
                            # Generic enemy reference - apply to all pets
                            for i in range(len(matched_tamer['pets'])):
                                npc_ability_usage[matched_tamer['name']][i][ability_ref] += 1
                        else:
                            pet_index = int(pet_num) - 1
                            if 0 <= pet_index < len(matched_tamer['pets']):
                                npc_ability_usage[matched_tamer['name']][pet_index][ability_ref] += 1
    
    print(f"Analyzed {strategy_count} strategies")
    print(f"Found NPC patterns for {len(npc_ability_usage)} tamers\n")
    
    # Build priority lists
    npc_ai_behaviors = {}
    
    for tamer_name, pets_usage in npc_ability_usage.items():
        if tamer_name not in tamer_lookup:
            continue
            
        tamer_data = tamer_lookup[tamer_name.lower()]
        npc_ai_behaviors[tamer_name] = {'pets': []}
        
        for pet_index, ability_counter in sorted(pets_usage.items()):
            if pet_index >= len(tamer_data['pets']):
                continue
                
            pet = tamer_data['pets'][pet_index]
            
            # Get this pet's actual abilities
            pet_abilities = pet.get('abilities', [])
            if not pet_abilities:
                continue
            
            # Create priority list based on strategy mentions
            priority_list = []
            
            # Sort by mention frequency
            for ability_ref, count in ability_counter.most_common():
                # Try to match ability reference to actual ability IDs
                # Could be ability name or ID
                for ability in pet_abilities:
                    ability_id = ability.get('id')
                    ability_name = ability.get('name', '').lower()
                    
                    ref_lower = str(ability_ref).lower()
                    if str(ability_id) == ref_lower or ability_name == ref_lower:
                        if ability_id not in priority_list:
                            priority_list.append(ability_id)
                        break
            
            # If no priorities found from strategies, use high-power preference
            if not priority_list:
                # Sort by power
                sorted_abilities = sorted(pet_abilities, key=lambda a: a.get('power', 0), reverse=True)
                priority_list = [a['id'] for a in sorted_abilities[:3]]
            
            npc_ai_behaviors[tamer_name]['pets'].append({
                'species_id': pet['species_id'],
                'priority': priority_list
            })
    
    # Save to file
    with open('npc_ai_behaviors.json', 'w') as f:
        json.dump(npc_ai_behaviors, f, indent=2)
    
    print(f"✅ Generated AI behaviors for {len(npc_ai_behaviors)} tamers")
    print(f"📁 Saved to npc_ai_behaviors.json")
    
    # Show sample
    if npc_ai_behaviors:
        sample_tamer = list(npc_ai_behaviors.keys())[0]
        print(f"\n📊 Sample: {sample_tamer}")
        for i, pet in enumerate(npc_ai_behaviors[sample_tamer]['pets']):
            print(f"  Pet {i+1} (Species {pet['species_id']}): {pet['priority']}")

if __name__ == '__main__':
    extract_npc_priorities()
