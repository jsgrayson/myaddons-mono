#!/usr/bin/env python3
"""
TURN-BY-TURN NPC BEHAVIOR EXTRACTION

Analyze player actions across ALL strategies to reverse-engineer exact NPC turn order:
1. Group strategies by encounter
2. Track what players do on turn 1, 2, 3... against each NPC pet
3. Find consensus (80%+ of strategies do X on turn Y)
4. Map player defensive/counter moves to NPC abilities
5. Output exact NPC ability rotation per turn

Example:
- Turn 1: 90% use Dodge → NPC uses high-power ability
- Turn 2: 85% use standby → NPC uses buff/dangerous move
- Turn 3: 100% attack → NPC uses normal rotation
"""

import json
import re
from collections import defaultdict, Counter

def analyze_turn_by_turn_behavior():
    """Extract exact NPC turn order from player strategy patterns"""
    
    with open('strategies_enhanced.json') as f:
        xufu_data = json.load(f)
    
    # Process each encounter
    for expansion, categories in xufu_data.items():
        for category, encounter_list in categories.items():
            for enc_data in encounter_list:
                if 'squirt' not in enc_data['encounter_name'].lower():
                    continue  # Focus on Squirt first
                
                print(f"\n{'='*70}")
                print(f"ENCOUNTER: {enc_data['encounter_name']}")
                print(f"{'='*70}")
                
                strategies = enc_data.get('strategies', [])
                print(f"Analyzing {len(strategies)} different team strategies...")
                
                # Track player actions by turn and enemy
                enemy_turn_actions = defaultdict(lambda: defaultdict(list))
                
                for strat_idx, strategy in enumerate(strategies):
                    script = strategy.get('script', '')
                    
                    # Parse the script to extract turn-specific actions
                    # Look for round conditionals and enemy sections
                    
                    # Split into enemy sections
                    for enemy_num in [1, 2, 3]:
                        pattern = rf'if\s*\[\s*enemy\(#{enemy_num}\)\.active\s*\](.*?)(?:endif|if\s*\[\s*enemy\(#(?!{enemy_num}))'
                        match = re.search(pattern, script, re.DOTALL | re.IGNORECASE)
                        
                        if match:
                            enemy_section = match.group(1)
                            
                            # Look for turn-specific actions within this section
                            turn_matches = re.findall(r'\[round[=~](\d+)\]([^\n]+)', enemy_section)
                            for turn, action in turn_matches:
                                enemy_turn_actions[f'enemy{enemy_num}'][int(turn)].append({
                                    'strat': strat_idx,
                                    'action': action.strip()
                                })
                            
                            # Also track general action patterns (no specific turn)
                            if 'standby' in enemy_section.lower():
                                enemy_turn_actions[f'enemy{enemy_num}']['has_standby'].append(True)
                            if 'dodge' in enemy_section.lower() or 'deflect' in enemy_section.lower():
                                enemy_turn_actions[f'enemy{enemy_num}']['has_defensive'].append(True)
                
                # Analyze consensus
                print("\n📊 TURN-BY-TURN CONSENSUS:")
                print("-"*70)
                
                for enemy in ['enemy1', 'enemy2', 'enemy3']:
                    if enemy not in enemy_turn_actions:
                        continue
                    
                    print(f"\n{enemy.upper()}:")
                    
                    # Show turn-specific patterns
                    turns_data = {k: v for k, v in enemy_turn_actions[enemy].items() if isinstance(k, int)}
                    if turns_data:
                        for turn in sorted(turns_data.keys()):
                            actions = turns_data[turn]
                            print(f"  Turn {turn}: ({len(actions)}/{len(strategies)} strategies)")
                            
                            # Summarize common actions
                            action_types = Counter()
                            for a in actions:
                                action_str = a['action'].lower()
                                if 'standby' in action_str:
                                    action_types['standby'] += 1
                                elif 'dodge' in action_str or 'deflect' in action_str:
                                    action_types['defensive_ability'] += 1
                                elif 'change' in action_str or 'swap' in action_str:
                                    action_types['swap'] += 1
                                elif 'ability' in action_str or 'use' in action_str:
                                    action_types['attack'] += 1
                            
                            for action_type, count in action_types.most_common():
                                pct = (count / len(actions)) * 100
                                print(f"    - {action_type}: {count}/{len(actions)} ({pct:.0f}%)")
                    
                    # Show general patterns
                    if 'has_standby' in enemy_turn_actions[enemy]:
                        count = len(enemy_turn_actions[enemy]['has_standby'])
                        print(f"  {count}/{len(strategies)} strategies use standby")
                    
                    if 'has_defensive' in enemy_turn_actions[enemy]:
                        count = len(enemy_turn_actions[enemy]['has_defensive'])
                        print(f"  {count}/{len(strategies)} strategies use defensive moves")
                
                # Only analyze Squirt for now
                return

if __name__ == "__main__":
    analyze_turn_by_turn_behavior()
    
    print("\n" + "="*70)
    print("NEXT: Map consensus patterns to NPC abilities to build rotation")
    print("="*70)
