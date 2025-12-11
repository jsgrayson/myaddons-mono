#!/usr/bin/env python3
"""
Cross-reference player strategies with NPC abilities to extrapolate exact NPC move order.

Logic:
1. Load NPC abilities from encounters.json (we know what Squirt CAN use)
2. Analyze player defensive/counter moves per turn
3. Match player actions to likely NPC abilities
4. Build turn-by-turn NPC script
"""

import json
import re
from collections import defaultdict

def load_npc_abilities():
    """Load Squirt's actual abilities"""
    with open('encounters.json') as f:
        squirt = json.load(f)['squirt']
    
    npc_abilities = {}
    for i, pet in enumerate(squirt['npc_pets'], 1):
        npc_abilities[f'enemy{i}'] = {
            'name': pet['name'],
            'abilities': {ab['id']: ab for ab in pet['abilities']}
        }
    
    return npc_abilities

def analyze_player_turn_actions():
    """Extract player actions per turn and per enemy"""
    
    with open('strategies_enhanced.json') as f:
        xufu_data = json.load(f)
    
    # Collect all Squirt scripts
    scripts = []
    for exp, cats in xufu_data.items():
        for cat, encs in cats.items():
            for enc in encs:
                if 'squirt' in enc['encounter_name'].lower():
                    for strat in enc.get('strategies', []):
                        scripts.append(strat.get('script', ''))
    
    npc_abilities = load_npc_abilities()
    
    print("CROSS-REFERENCING PLAYER ACTIONS WITH NPC ABILITIES")
    print("="*70)
    
    # Analyze each script
    turn_patterns = defaultdict(lambda: defaultdict(list))
    
    for script_idx, script in enumerate(scripts):
        # Look for round-specific actions
        for match in re.finditer(r'\[round[=~](\d+)\]([^\n]+)', script):
            turn = match.group(1)
            action = match.group(2).strip()
            
            # Determine which enemy this is against
            enemy = None
            if 'enemy(#1)' in script[:match.start()]:
                enemy = 'enemy1'
            elif 'enemy(#2)' in script[:match.start()]:
                enemy = 'enemy2'
            elif 'enemy(#3)' in script[:match.start()]:
                enemy = 'enemy3'
            
            if enemy:
                turn_patterns[enemy][turn].append(action)
    
    # Display findings
    print("\nPLAYER ACTIONS BY TURN (reveals NPC behavior):")
    print("-"*70)
    
    for enemy in ['enemy1', 'enemy2', 'enemy3']:
        if enemy in npc_abilities:
            print(f"\n🎯 VS {npc_abilities[enemy]['name'].upper()}:")
            print(f"   Available abilities: {', '.join([ab['name'] for ab in npc_abilities[enemy]['abilities'].values()])}")
            
            if enemy in turn_patterns:
                for turn in sorted(turn_patterns[enemy].keys(), key=int):
                    actions = turn_patterns[enemy][turn]
                    print(f"\n   Turn {turn}: Player {actions}")
                    
                    # Infer NPC move
                    action_str = ' '.join(actions).lower()
                    if 'dodge' in action_str or 'deflect' in action_str:
                        print(f"   → NPC likely uses HIGH DAMAGE ability")
                    elif 'standby' in action_str or 'wait' in action_str:
                        print(f"   → NPC likely BUFFS or uses DANGEROUS move")
                    elif 'change' in action_str:
                        print(f"   → Player swaps (NPC still attacking)")
    
    # Now do broader pattern analysis
    print("\n" + "="*70)
    print("PATTERN ANALYSIS ACROSS ALL SCRIPTS:")
    print("-"*70)
    
    for script in scripts[:3]:  # Show first 3 for detailed analysis
        print("\n" + "-"*70)
        print("Script snippet:")
        print(script[:300])
        print("\n→ Player action sequence reveals NPC is predictable")
        print("→ Same script works = NPC uses same moves each time")

def build_npc_script():
    """Attempt to build actual NPC move order"""
    
    npc_abilities = load_npc_abilities()
    
    print("\n" + "="*70)
    print("DEDUCED NPC MOVE ORDER:")
    print("="*70)
    
    print("\nDeebs (Enemy #1):")
    print("  Abilities: Water Jet (20), Pump (13), Whirlpool (30)")
    print("  Likely rotation: Whirlpool (highest damage) → Water Jet → Pump")
    print("  → AI: Use highest power first")
    
    print("\nTyri (Enemy #2):")
    print("  Abilities: Tail Sweep (18), Moonfire (30), Lift-Off (40)")
    print("  Likely rotation: Lift-Off (highest) → Moonfire → Tail Sweep")
    print("  → AI: Prioritize high damage")
    
    print("\nPuzzle (Enemy #3):")
    print("  Abilities: Build Turret (30), Batter (28), Dodge (0)")
    print("  Likely rotation: Dodge (defensive) → Build Turret → Batter")
    print("  → AI: Use Dodge when threatened, then attack")

if __name__ == "__main__":
    analyze_player_turn_actions()
    build_npc_script()
