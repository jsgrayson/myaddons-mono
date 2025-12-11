#!/usr/bin/env python3
"""
Analyze player strategies to deduce NPC ability usage.

By looking at what players do (defensive moves, swaps, counters),
we can infer which abilities NPCs must be using.
"""

import json
import re
from collections import defaultdict, Counter

def analyze_npc_from_strategies():
    """Analyze strategies to deduce NPC behavior."""
    
    # Load encounters with NPC abilities
    with open('encounters_full.json', 'r') as f:
        encounters = json.load(f)
    
    # Load strategies
    with open('strategies_enhanced.json', 'r') as f:
        strategies_data = json.load(f)
    
    print("Analyzing player strategies to deduce NPC behavior...")
    print("=" * 70)
    
    # For each tamer, track what the strategy does
    tamer_analysis = {}
    
    for expansion, categories in strategies_data.items():
        if not isinstance(categories, dict):
            continue
        
        for category, encounter_list in categories.items():
            if not isinstance(encounter_list, list):
                continue
            
            for encounter in encounter_list:
                if not isinstance(encounter, dict):
                    continue
                
                encounter_name = encounter.get('encounter_name', '')
                
                # Find matching tamer in encounters_full
                matched_tamer = None
                for tamer in encounters:
                    if tamer['name'].lower() in encounter_name.lower():
                        matched_tamer = tamer
                        break
                
                if not matched_tamer:
                    continue
                
                if matched_tamer['name'] not in tamer_analysis:
                    tamer_analysis[matched_tamer['name']] = {
                        'npc': matched_tamer,
                        'strategies': [],
                        'common_actions': []
                    }
                
                # Analyze each strategy
                for strategy in encounter.get('strategies', []):
                    script = strategy.get('script', '')
                    
                    # Extract player actions
                    actions = []
                    
                    # Find defensive abilities used
                    defensive = re.findall(r'use\(([^:]+:[^)]+)\)\s*\[enemy', script, re.IGNORECASE)
                    if defensive:
                        actions.append(f"Defensive: {', '.join(defensive[:2])}")
                    
                    # Find swaps
                    swaps = re.findall(r'change\(#(\d+)\)', script)
                    if swaps:
                        actions.append(f"Swaps to pet {','.join(swaps[:2])}")
                    
                    # Find round-specific actions (indicates NPC timing)
                    round_actions = re.findall(r'\[round=(\d+)\]', script)
                    if round_actions:
                        actions.append(f"Critical rounds: {','.join(round_actions[:3])}")
                    
                    if actions:
                        tamer_analysis[matched_tamer['name']]['strategies'].append({
                            'name': strategy.get('name', 'Unknown'),
                            'actions': actions
                        })
    
    # Print analysis
    print(f"\nAnalyzed strategies for {len(tamer_analysis)} tamers\n")
    
    for tamer_name, data in sorted(tamer_analysis.items())[:10]:  # Show first 10
        print(f"\n{'='*70}")
        print(f"📊 {tamer_name}")
        print(f"{'='*70}")
        
        # Show NPC abilities
        npc = data['npc']
        print(f"\nNPC Team ({len(npc['pets'])} pets):")
        for i, pet in enumerate(npc['pets'], 1):
            abilities = pet.get('abilities', [])
            if abilities:
                print(f"\n  Pet {i} (Species {pet['species_id']}):")
                for ability in abilities[:3]:  # First 3 abilities
                    power = ability.get('power', 0)
                    name = ability.get('name', 'Unknown')
                    print(f"    - {name} (Power: {power})")
        
        # Show what players do
        print(f"\n  Player Strategies ({len(data['strategies'])} found):")
        for strat in data['strategies'][:3]:  # First 3
            print(f"    • {strat['name']}")
            for action in strat['actions']:
                print(f"      → {action}")
        
        print(f"\n  ⚡ Likely NPC Pattern:")
        print(f"    Players use defensive/swap moves on specific rounds")
        print(f"    → NPCs probably use high-power abilities consistently")
    
    print(f"\n\n{'='*70}")
    print("Summary: NPCs likely prioritize highest-power abilities")
    print("Players react with timed defenses/swaps on dangerous rounds")
    print(f"{'='*70}\n")
    
    return tamer_analysis

if __name__ == '__main__':
    analyze_npc_from_strategies()
