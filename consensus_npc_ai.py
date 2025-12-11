#!/usr/bin/env python3
"""
Find common player responses across DIFFERENT teams.
Since player pets vary but NPC is constant, consensus reveals NPC pattern.
"""

import json
import re
from collections import defaultdict, Counter

def find_consensus_npc_behavior():
    """Find what ALL strategies do in common = reveals NPC behavior"""
    
    with open('strategies_enhanced.json') as f:
        xufu_data = json.load(f)
    
    # Load NPC abilities
    with open('encounters.json') as f:
        squirt = json.load(f)['squirt']
        npc_abilities = {
            f"enemy{i+1}": {
                'name': pet['name'],
                'abilities': [(ab['id'], ab['name'], ab['power']) for ab in pet['abilities']]
            }
            for i, pet in enumerate(squirt['npc_pets'])
        }
    
    # Collect all strategies with their player pets
    strategies = []
    for exp, cats in xufu_data.items():
        for cat, encs in cats.items():
            for enc in encs:
                if 'squirt' in enc['encounter_name'].lower():
                    for strat in enc.get('strategies', []):
                        # Get player pets used
                        player_pets = []
                        for slot in strat.get('pet_slots', []):
                            if slot and len(slot) > 0:
                                player_pets.append(slot[0].get('name', 'Unknown'))
                        
                        strategies.append({
                            'player_pets': player_pets,
                            'script': strat.get('script', '')
                        })
    
    print(f"Analyzing {len(strategies)} Squirt strategies")
    print("Player teams vary, but NPC (Squirt) is constant")
    print("="*70)
    
    # Track what percentage of strategies do certain things
    enemy1_actions = defaultdict(int)
    enemy2_actions = defaultdict(int)
    enemy3_actions = defaultdict(int)
    
    for strat in strategies:
        script = strat['script']
        
        # Analyze actions when facing each enemy
        # Enemy #1 (Deebs)
        enemy1_section = re.search(r'if\s*\[\s*enemy\(#1\)\.active\s*\](.*?)(?:endif|if\s*\[\s*enemy)', script, re.DOTALL | re.IGNORECASE)
        if enemy1_section:
            section = enemy1_section.group(1).lower()
            if 'standby' in section:
                enemy1_actions['uses_standby'] += 1
            if 'dodge' in section or 'deflect' in section:
                enemy1_actions['uses_defensive'] += 1
            if re.search(r'change|swap', section):
                enemy1_actions['swaps_pet'] += 1
            # Count attack abilities
            attacks = len(re.findall(r'ability', section))
            if attacks > 0:
                enemy1_actions['avg_attacks'] += attacks
        
        # Enemy #2 (Tyri) 
        enemy2_section = re.search(r'if\s*\[\s*enemy\(#2\)\.active\s*\](.*?)(?:endif|if\s*\[\s*enemy)', script, re.DOTALL | re.IGNORECASE)
        if enemy2_section:
            section = enemy2_section.group(1).lower()
            if 'standby' in section:
                enemy2_actions['uses_standby'] += 1
            if 'dodge' in section or 'deflect' in section:
                enemy2_actions['uses_defensive'] += 1
            if re.search(r'change', section):
                enemy2_actions['swaps_pet'] += 1
        
        # Enemy #3 (Puzzle)
        enemy3_section = re.search(r'if\s*\[\s*enemy\(#3\)', script, re.DOTALL | re.IGNORECASE)
        if enemy3_section:
            # Get rest of script after this point
            section = script[enemy3_section.start():].lower()
            if 'standby' in section:
                enemy3_actions['uses_standby'] += 1
            if 'dodge' in section:
                enemy3_actions['player_dodges'] += 1
            if re.search(r'change.*#3', section):
                enemy3_actions['swaps_to_counter'] += 1
    
    total = len(strategies)
    
    print("\n🎯 CONSENSUS: What do ALL strategies do?")
    print("="*70)
    
    print(f"\nVS ENEMY #1 (Deebs):")
    print(f"   Abilities: Water Jet (20), Pump (13), Whirlpool (30)")
    for action, count in enemy1_actions.items():
        pct = (count/total)*100
        print(f"   {count}/{total} ({pct:.0f}%) strategies: {action}")
    print(f"   → NPC pattern: Likely spams highest power (Whirlpool)")
    
    print(f"\nVS ENEMY #2 (Tyri):")
    print(f"   Abilities: Tail Sweep (18), Moonfire (30), Lift-Off (40)")
    for action, count in enemy2_actions.items():
        pct = (count/total)*100
        print(f"   {count}/{total} ({pct:.0f}%) strategies: {action}")
    
    # Check if strategies mention specific abilities
    moonfire_mentions = sum(1 for s in strategies if '593' in s['script'] or 'moonfire' in s['script'].lower())
    liftoff_mentions = sum(1 for s in strategies if '489' in s['script'] or 'lift' in s['script'].lower())
    print(f"   {moonfire_mentions}/{total} mention Moonfire (593)")
    print(f"   {liftoff_mentions}/{total} mention Lift-Off")
    print(f"   → NPC pattern: Uses Lift-Off (40 power) - dangerous move")
    
    print(f"\nVS ENEMY #3 (Puzzle):")
    print(f"   Abilities: Build Turret (30), Batter (28), Dodge (0)")
    for action, count in enemy3_actions.items():
        pct = (count/total)*100
        print(f"   {count}/{total} ({pct:.0f}%) strategies: {action}")
    
    # Check for Dodge mentions
    dodge_mentions = sum(1 for s in strategies if re.search(r'enemy.*dodge|dodge.*enemy', s['script'].lower()))
    print(f"   {dodge_mentions}/{total} check for enemy Dodge")
    print(f"   → NPC pattern: Puzzle uses Dodge frequently")
    
    print("\n" + "="*70)
    print("DEDUCED NPC AI:")
    print("="*70)
    print("\nDeebs: Whirlpool (30) spam - highest damage")
    print("Tyri: Lift-Off (40) + Moonfire (30) - burst damage")  
    print("Puzzle: Dodge (0) defensively, then Build Turret/Batter")
    print("\n→ NPCs prioritize HIGH POWER abilities")
    print("→ Puzzle uses Dodge (low power buff) for defense")

if __name__ == "__main__":
    find_consensus_npc_behavior()
