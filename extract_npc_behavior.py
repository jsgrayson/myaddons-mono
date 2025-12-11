#!/usr/bin/env python3
"""
Analyze ALL Squirt strategies to reverse-engineer exact NPC behavior.
With multiple strategies, we can find common patterns that reveal NPC moves.
"""

import json
import re
from collections import Counter, defaultdict

def analyze_all_squirt_strategies():
    """Analyze all Squirt strategies to find NPC behavioral consensus"""
    
    with open('strategies_enhanced.json') as f:
        xufu_data = json.load(f)
    
    all_strategies = []
    
    # Collect all Squirt strategies
    for exp, cats in xufu_data.items():
        for cat, encs in cats.items():
            for enc in encs:
                if 'squirt' in enc['encounter_name'].lower():
                    for strat in enc.get('strategies', []):
                        all_strategies.append({
                            'expansion': exp,
                            'category': cat,
                            'name': strat.get('name', 'Unknown'),
                            'script': strat.get('script', '')
                        })
    
    print(f"Found {len(all_strategies)} Squirt strategies")
    print("="*60)
    
    # Analyze patterns across all strategies
    enemy_refs = Counter()
    enemy_abilities = Counter()
    enemy_auras = Counter()
    round_actions = defaultdict(list)
    standby_conditions = []
    defensive_moves = Counter()
    
    for strat in all_strategies:
        script = strat['script']
        
        # Count enemy pet references
        for match in re.finditer(r'enemy\(#(\d+)\)', script):
            enemy_refs[f"enemy#{match.group(1)}"] += 1
        
        # Track enemy abilities
        for match in re.finditer(r'enemy\.ability\(([^)]+)\)', script):
            enemy_abilities[match.group(1)] += 1
        
        # Track enemy auras
        for match in re.finditer(r'enemy\.aura\(([^)]+)\)', script):
            enemy_auras[match.group(1)] += 1
        
        # Track round-specific actions
        for match in re.finditer(r'\[round[=~](\d+)\]', script):
            round_num = match.group(1)
            # Get the line this appears on
            lines = script[:match.start()].split('\n')
            context = lines[-1] if lines else ""
            round_actions[round_num].append(context)
        
        # Track standby conditions
        for match in re.finditer(r'standby\s*\[([^\]]+)\]', script):
            standby_conditions.append(match.group(1))
        
        # Track defensive abilities
        for match in re.finditer(r'use\((Dodge|Deflection|Decoy|Block|Ice Tomb)[^)]*\)', script):
            defensive_moves[match.group(1)] += 1
    
    print("\n📊 CONSENSUS PATTERNS:")
    print("="*60)
    
    if enemy_refs:
        print("\nEnemy Pet References:")
        for enemy, count in enemy_refs.most_common():
            print(f"  {enemy}: {count}/{len(all_strategies)} strategies ({count/len(all_strategies)*100:.0f}%)")
    
    if enemy_abilities:
        print("\nEnemy Abilities Players Expect:")
        for ability, count in enemy_abilities.most_common():
            print(f"  {ability}: {count} strategies mention this")
    
    if enemy_auras:
        print("\nEnemy Buffs/Debuffs:")
        for aura, count in enemy_auras.most_common(10):
            print(f"  {aura}: {count} strategies check for this")
    
    if defensive_moves:
        print("\nDefensive Moves Players Use (reveals NPC threats):")
        for move, count in defensive_moves.most_common():
            print(f"  {move}: {count} times → NPC has attacks worth defending against")
    
    if standby_conditions:
        print(f"\nStandby Conditions ({len(standby_conditions)} total):")
        standby_counter = Counter(standby_conditions)
        for condition, count in standby_counter.most_common(10):
            print(f"  [{condition}]: {count} times")
    
    print("\n🎯 NPC BEHAVIOR INFERENCE:")
    print("="*60)
    
    # Deduce NPC pet order
    if 'enemy#1' in enemy_refs and 'enemy#2' in enemy_refs and 'enemy#3' in enemy_refs:
        print("✅ NPCs come in fixed order: #1 (Deebs), #2 (Tyri), #3 (Puzzle)")
    
    # Deduce NPC ability patterns
    if standby_conditions:
        print("\n✅ NPCs use predictable abilities (players prepare counters):")
        print("   - Common standby conditions reveal dangerous NPC moves")
    
    # Deduce NPC doesn't swap strategically
    swap_mentions = sum(1 for s in all_strategies if 'enemy' in s['script'] and 'change' in s['script'])
    print(f"\n✅ Players rarely force NPC swaps ({swap_mentions}/{len(all_strategies)})")
    print("   → NPCs likely stay with current pet until death")
    
    return all_strategies

if __name__ == "__main__":
    strategies = analyze_all_squirt_strategies()
    
    print("\n" + "="*60)
    print(f"Analyzed {len(strategies)} strategies across all expansions")
    print("="*60)
