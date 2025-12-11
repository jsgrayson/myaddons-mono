#!/usr/bin/env python3
"""
Generate NPC AI priority lists from strategy data.

This script analyzes Xu-Fu strategies to determine which abilities NPCs actually use.
It outputs a JSON file mapping Tamer Name -> Pet Index -> [Ability Priority List].
"""

import json
import re
import difflib
from collections import defaultdict, Counter

def normalize_name(name):
    """Normalize name for matching."""
    return name.lower().replace("'", "").replace(":", "").strip()

def generate_npc_ai():
    print("Loading data...")
    
    with open('encounters_complete.json', 'r') as f:
        encounters_dict = json.load(f)
        # Convert dict to list if needed, or handle dict
        # encounters_complete is dict: key -> data
        encounters = list(encounters_dict.values())
        
    try:
        with open('strategies_enhanced.json', 'r') as f:
            strategies_data = json.load(f)
    except FileNotFoundError:
        print("strategies_enhanced.json not found, trying strategies.json")
        with open('strategies.json', 'r') as f:
            strategies_data = json.load(f)

    # Map normalized tamer names to their full data
    tamer_map = {}
    for tamer in encounters:
        norm_name = normalize_name(tamer['name'])
        tamer_map[norm_name] = tamer

    # Store ability counts: tamer_name -> pet_index -> ability_id -> count
    npc_ability_counts = defaultdict(lambda: defaultdict(Counter))
    
    # Track matches for reporting
    matched_encounters = set()
    total_strategies = 0

    print("Analyzing strategies...")
    
    for expansion, categories in strategies_data.items():
        if not isinstance(categories, dict): continue
        
        for category, encounter_list in categories.items():
            if not isinstance(encounter_list, list): continue
            
            for encounter in encounter_list:
                if not isinstance(encounter, dict): continue
                
                enc_name = encounter.get('encounter_name', '')
                norm_enc_name = normalize_name(enc_name)
                
                # Find matching tamer
                matched_tamer = None
                
                # 1. Exact match
                if norm_enc_name in tamer_map:
                    matched_tamer = tamer_map[norm_enc_name]
                
                # 2. Partial match (e.g. "Squirt" in "Squirt (WoD Garrison)")
                if not matched_tamer:
                    for t_name, t_data in tamer_map.items():
                        if t_name in norm_enc_name or norm_enc_name in t_name:
                            matched_tamer = t_data
                            break
                
                if not matched_tamer:
                    # print(f"No match for {enc_name}")
                    continue
                
                # Debug print for Squirt
                if 'squirt' in matched_tamer['name'].lower():
                    print(f"DEBUG: Found Squirt! Analyzing strategy...")
                
                matched_encounters.add(matched_tamer['name'])
                
                # Analyze strategies
                for strategy in encounter.get('strategies', []):
                    total_strategies += 1
                    script = strategy.get('script', '')
                    
                    # Regex for enemy ability checks: enemy.ability(ID)
                    # Also captures enemy(#X).ability(ID)
                    ability_matches = re.finditer(r'enemy(?:\(#(\d+)\))?\.ability\(([^)]+)\)', script)
                    
                    for m in ability_matches:
                        pet_idx_str = m.group(1)
                        ability_ref = m.group(2) # Name or ID
                        
                        # If pet index specified, use it. Otherwise assume active pet (could be any, but usually #1 starts)
                        # For safety, if no index, we'll add to all pets for now, or maybe just skip?
                        # Better heuristic: if no index, it's likely the current active enemy.
                        # Since we can't easily simulate the whole script flow here, we'll assign to ALL pets
                        # but weight it lower? Or just assign to all and filter by who actually HAS the ability later.
                        
                        target_indices = []
                        if pet_idx_str:
                            target_indices = [int(pet_idx_str) - 1]
                        # Get pets list (handle both keys)
                        tamer_pets = matched_tamer.get('npc_pets') or matched_tamer.get('pets', [])
                        
                        target_indices = []
                        if pet_idx_str:
                            target_indices = [int(pet_idx_str) - 1]
                        else:
                            target_indices = range(len(tamer_pets))
                            
                        for idx in target_indices:
                            if idx < len(tamer_pets):
                                npc_ability_counts[matched_tamer['name']][idx][ability_ref] += 1
                                if 'squirt' in matched_tamer['name'].lower():
                                    print(f"DEBUG: Squirt usage: Pet {idx} used {ability_ref}")

                    # Regex for enemy aura checks: enemy.aura(ID)
                    aura_matches = re.finditer(r'enemy(?:\(#(\d+)\))?\.aura\(([^)]+)\)', script)
                    for m in aura_matches:
                        pet_idx_str = m.group(1)
                        aura_ref = m.group(2)
                        
                        target_indices = []
                        if pet_idx_str:
                            target_indices = [int(pet_idx_str) - 1]
                        # Get pets list (handle both keys)
                        tamer_pets = matched_tamer.get('npc_pets') or matched_tamer.get('pets', [])

                        target_indices = []
                        if pet_idx_str:
                            target_indices = [int(pet_idx_str) - 1]
                        else:
                            target_indices = range(len(tamer_pets))
                            
                        for idx in target_indices:
                            if idx < len(tamer_pets):
                                npc_ability_counts[matched_tamer['name']][idx][aura_ref] += 1

    print(f"Processed {total_strategies} strategies.")
    print(f"Matched {len(matched_encounters)} unique tamers.")
    
    # Build final priority map
    # Tamer Name -> Pet Index -> [Ability IDs]
    final_priorities = {}
    
    for tamer_name, pets_data in npc_ability_counts.items():
        # Find the tamer data to verify abilities
        # (We used the real name as key in npc_ability_counts)
        # We need to look it up in encounters list again or use a map
        # tamer_map keys are normalized, so let's just find it.
        
        real_tamer_data = next((t for t in encounters if t['name'] == tamer_name), None)
        if not real_tamer_data: continue
        
        tamer_priorities = {}
        
        tamer_pets = real_tamer_data.get('npc_pets') or real_tamer_data.get('pets', [])
        
        if 'squirt' in tamer_name.lower():
            print(f"DEBUG: Processing Squirt priorities. Pets data: {len(pets_data)}")
            
        for pet_idx, counts in pets_data.items():
            if pet_idx >= len(tamer_pets): continue
            
            pet = tamer_pets[pet_idx]
            pet_abilities = pet.get('abilities', [])
            
            # Resolve references (names/IDs) to actual Ability IDs this pet has
            confirmed_counts = Counter()
            
            for ref, count in counts.items():
                ref_str = str(ref).lower()
                
                # Parse ref if it contains colon (Name:ID)
                ref_id = None
                ref_name = ref_str
                if ':' in ref_str:
                    parts = ref_str.split(':')
                    ref_name = parts[0].strip()
                    if len(parts) > 1 and parts[1].strip().isdigit():
                        ref_id = parts[1].strip()
                
                # Check against this pet's abilities
                for ability in pet_abilities:
                    ab_id = str(ability['id'])
                    ab_name = ability['name'].lower()
                    
                    # Match ID or Name
                    match = False
                    if ref_id and ref_id == ab_id:
                        match = True
                    elif ref_name == ab_name:
                        match = True
                    elif ref_str == ab_id: # In case ref was just ID
                        match = True
                        
                    if match:
                        confirmed_counts[ability['id']] += count
                        
                    # Also check if the aura name matches an ability name (often same)
                    # e.g. "Black Claw" aura implies "Black Claw" ability usage
                    if ref_name == ab_name:
                        confirmed_counts[ability['id']] += count

            if confirmed_counts:
                # Sort by frequency
                priority_list = [ab_id for ab_id, _ in confirmed_counts.most_common()]
                tamer_priorities[pet_idx] = priority_list
        
        if tamer_priorities:
            final_priorities[tamer_name] = tamer_priorities

    print(f"Generated priorities for {len(final_priorities)} tamers.")
    
    # Save to JSON
    with open('npc_ai_priorities.json', 'w') as f:
        json.dump(final_priorities, f, indent=2)
        
    print("Saved to npc_ai_priorities.json")

if __name__ == "__main__":
    generate_npc_ai()
