#!/usr/bin/env python3
"""
Convert scraped Xu-Fu NPC data to AI priority lists.

Takes the output of scrape_xufu_npc_data.py (npc_encounters.json)
and converts it to the format expected by SmartEnemyAgent.
"""

import json

def convert_to_priorities():
    print("Loading scraped data...")
    try:
        with open('npc_encounters.json', 'r') as f:
            scraped_data = json.load(f)
    except FileNotFoundError:
        print("Error: npc_encounters.json not found. Run scrape_xufu_npc_data.py first.")
        return

    # Load encounters_full to map names
    with open('encounters_full.json', 'r') as f:
        encounters_full = json.load(f)
    
    # Create map for fuzzy matching
    tamer_map = {}
    for tamer in encounters_full:
        norm_name = tamer['name'].lower().replace("'", "").replace(":", "").strip()
        tamer_map[norm_name] = tamer['name']

    priorities = {}
    matched_count = 0
    
    print(f"Processing {len(scraped_data)} scraped encounters...")
    
    for enc_id, enc_data in scraped_data.items():
        enc_name = enc_data['name']
        norm_enc_name = enc_name.lower().replace("'", "").replace(":", "").strip()
        
        # Find matching tamer
        matched_tamer_name = None
        
        # 1. Exact match
        if norm_enc_name in tamer_map:
            matched_tamer_name = tamer_map[norm_enc_name]
        
        # 2. Partial match
        if not matched_tamer_name:
            for t_norm, t_real in tamer_map.items():
                if t_norm in norm_enc_name or norm_enc_name in t_norm:
                    matched_tamer_name = t_real
                    break
        
        if not matched_tamer_name:
            # print(f"Skipping {enc_name} - no matching tamer found")
            continue
            
        matched_count += 1
        
        # Extract priorities
        tamer_priorities = {}
        
        for i, pet in enumerate(enc_data['npc_pets']):
            abilities = pet.get('abilities', [])
            if not abilities:
                continue
                
            # The abilities listed on Xu-Fu are the ones the NPC uses
            # So we just list their IDs as the priority list
            priority_list = [ab['id'] for ab in abilities]
            
            if priority_list:
                tamer_priorities[str(i)] = priority_list
        
        if tamer_priorities:
            priorities[matched_tamer_name] = tamer_priorities

    print(f"Matched {matched_count} encounters to known tamers.")
    print(f"Generated priorities for {len(priorities)} tamers.")
    
    # Save
    with open('npc_ai_priorities.json', 'w') as f:
        json.dump(priorities, f, indent=2)
    
    print("Saved to npc_ai_priorities.json")

if __name__ == "__main__":
    convert_to_priorities()
