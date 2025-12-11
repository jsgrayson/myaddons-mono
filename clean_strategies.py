"""
Clean strategies_enhanced.json to produce a usable dataset.
Filters out junk data ('1', '2', id:0) and preserves valid pets.
"""

import json

def clean_strategies():
    print("Loading strategies_enhanced.json...")
    with open('strategies_enhanced.json', 'r') as f:
        data = json.load(f)
    
    cleaned_data = {}
    total_encounters = 0
    total_strategies = 0
    
    for expansion, categories in data.items():
        cleaned_data[expansion] = {}
        for category, encounters in categories.items():
            cleaned_data[expansion][category] = []
            
            for enc in encounters:
                clean_enc = {
                    'encounter_name': enc['encounter_name'],
                    'url': enc['url'],
                    'strategies': []
                }
                
                for strat in enc.get('strategies', []):
                    clean_strat = {
                        'name': strat.get('name', 'Default Strategy'),
                        'script': strat.get('script', ''),
                        'pet_slots': []
                    }
                    
                    # Process each slot
                    for slot in strat.get('pet_slots', []):
                        clean_slot = []
                        for pet in slot:
                            # Filter junk
                            if pet['id'] != 0 and pet['name'] not in ['1', '2', '3', 'Leveling Pet']:
                                clean_slot.append(pet)
                        
                        # If slot is empty but originally had items, it might be a leveling slot
                        # But for matching purposes, an empty slot means "we can't match this specific requirement"
                        # OR it means "Any Pet". 
                        # If the original data had "Leveling Pet", we should probably treat it as a wildcard.
                        # For now, we'll keep it empty if no specific pets were found.
                        clean_strat['pet_slots'].append(clean_slot)
                    
                    # Only add strategy if it has slots
                    if clean_strat['pet_slots']:
                        clean_enc['strategies'].append(clean_strat)
                        total_strategies += 1
                
                cleaned_data[expansion][category].append(clean_enc)
                total_encounters += 1
                
    print(f"Processed {total_encounters} encounters.")
    print(f"Recovered {total_strategies} strategies.")
    
    # Save cleaned data
    with open('strategies_cleaned.json', 'w') as f:
        json.dump(cleaned_data, f, indent=2)
    print("Saved to strategies_cleaned.json")

if __name__ == "__main__":
    clean_strategies()
