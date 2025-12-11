#!/usr/bin/env python3
"""
Extract specific NPC abilities per pet by analyzing player counters.
"""

import json
import re

def extract_npc_abilities_from_scripts():
    """Look for ability IDs in scripts that reference enemy pets"""
    
    with open('strategies_enhanced.json') as f:
        xufu_data = json.load(f)
    
    # Load ability stats to map IDs to names
    with open('ability_stats_manual.json') as f:
        ability_stats = json.load(f)['abilities']
    
    # Find all Squirt strategies
    squirt_scripts = []
    for exp, cats in xufu_data.items():
        for cat, encs in cats.items():
            for enc in encs:
                if 'squirt' in enc['encounter_name'].lower():
                    for strat in enc.get('strategies', []):
                        squirt_scripts.append(strat.get('script', ''))
    
    print(f"Analyzing {len(squirt_scripts)} Squirt scripts for NPC abilities...")
    print("="*60)
    
    # Look for patterns that reveal NPC abilities
    for script in squirt_scripts:
        # Find sections that reference specific enemy pets
        enemy1_section = re.search(r'if\s*\[\s*enemy\(#1\)\.active\s*\](.*?)(?:endif|if\s*\[)', script, re.DOTALL)
        enemy2_section = re.search(r'if\s*\[\s*enemy\(#2\)\.active\s*\](.*?)(?:endif|if\s*\[)', script, re.DOTALL)
        enemy3_section = re.search(r'if\s*\[\s*enemy\(#3\)\.active\s*\](.*?)(?:endif|$)', script, re.DOTALL)
        
        if enemy1_section or enemy2_section or enemy3_section:
            print("\n" + "="*60)
            
            if enemy1_section:
                print("\nVS ENEMY #1 (Deebs), Player uses:")
                abilities = re.findall(r'ability\((\d+)\)', enemy1_section.group(1))
                for ab_id in abilities[:5]:  # First 5
                    ab_name = ability_stats.get(ab_id, {}).get('name', f'Ability {ab_id}')
                    print(f"  - {ab_name} ({ab_id})")
            
            if enemy2_section:
                print("\nVS ENEMY #2 (Tyri), Player uses:")
                abilities = re.findall(r'ability\((\d+)\)', enemy2_section.group(1))
                for ab_id in abilities[:5]:
                    ab_name = ability_stats.get(ab_id, {}).get('name', f'Ability {ab_id}')
                    print(f"  - {ab_name} ({ab_id})")
            
            if enemy3_section:
                print("\nVS ENEMY #3 (Puzzle), Player uses:")
                abilities = re.findall(r'ability\((\d+)\)', enemy3_section.group(1))
                for ab_id in abilities[:5]:
                    ab_name = ability_stats.get(ab_id, {}).get('name', f'Ability {ab_id}')
                    print(f"  - {ab_name} ({ab_id})")
            
            # Only show first script
            break
    
    print("\n" + "="*60)
    print("\nNow checking what all Squirt scripts say about NPC pets...")
    print("="*60)
    
    # Look at all scripts to print raw sections
    print("\nRAW SCRIPT SECTIONS (first 3 strategies):")
    for i, script in enumerate(squirt_scripts[:3]):
        print(f"\n--- Strategy {i+1} ---")
        print(script[:400])
        print("...")

if __name__ == "__main__":
    extract_npc_abilities_from_scripts()
