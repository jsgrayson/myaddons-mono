import json
import os

def load_json(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return {}
    return {}

def merge_strategies():
    files = [
        'strategies.json',
        'strategies_cleaned.json',
        'strategies_pandaria.json',
        'strategies_browser_complete.json',
        'strategies_enhanced.json'
    ]
    
    master_db = {} # expansion -> category -> list of encounters
    
    total_strategies = 0
    merged_encounters = 0
    
    for filename in files:
        print(f"Processing {filename}...")
        data = load_json(filename)
        
        for expansion, categories in data.items():
            if expansion not in master_db:
                master_db[expansion] = {}
                
            for category, encounters in categories.items():
                if category not in master_db[expansion]:
                    master_db[expansion][category] = []
                
                for encounter in encounters:
                    name = encounter.get('encounter_name')
                    if not name: continue
                    
                    # Check if encounter already exists in master
                    existing = next((e for e in master_db[expansion][category] if e['encounter_name'] == name), None)
                    
                    if existing:
                        # Merge strategies
                        existing_strats = existing.get('strategies', [])
                        new_strats = encounter.get('strategies', [])
                        
                        # Add new strategies if they don't exist (by name)
                        for s in new_strats:
                            s_name = s.get('name', 'Unknown Strategy')
                            if not any(es.get('name', 'Unknown Strategy') == s_name for es in existing_strats):
                                existing_strats.append(s)
                                total_strategies += 1
                                
                        # Update metadata if missing (url, etc)
                        if not existing.get('url') and encounter.get('url'):
                            existing['url'] = encounter['url']
                            
                    else:
                        # Add new encounter
                        master_db[expansion][category].append(encounter)
                        merged_encounters += 1
                        total_strategies += len(encounter.get('strategies', []))

    print(f"\nConsolidation Complete.")
    print(f"Total Encounters: {merged_encounters}")
    print(f"Total Strategies: {total_strategies}")
    
    with open('strategies_master.json', 'w') as f:
        json.dump(master_db, f, indent=2)
    print("Saved to strategies_master.json")

if __name__ == "__main__":
    merge_strategies()
