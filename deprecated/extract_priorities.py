import json
import re
import os

def parse_rematch_script(script_text):
    """
    Parses a Rematch script into a structured priority list.
    Returns a list of dicts: {'action': 'use'|'change', 'id': int, 'condition': str}
    """
    lines = script_text.split('\n')
    priority_list = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('--'): continue
        
        # Parse "use(Ability:123) [condition]"
        # or "use(123) [condition]"
        # or "change(#2) [condition]"
        # or "change(next) [condition]"
        
        # Regex for USE
        use_match = re.match(r'use\((?:[^:]+:)?(\d+)\)(?:\s*\[(.*)\])?', line)
        if use_match:
            ability_id = int(use_match.group(1))
            condition = use_match.group(2)
            priority_list.append({
                'type': 'ability',
                'id': ability_id,
                'condition': condition
            })
            continue
            
        # Regex for CHANGE
        change_match = re.match(r'change\(([^)]+)\)(?:\s*\[(.*)\])?', line)
        if change_match:
            target = change_match.group(1) # "#2", "next", "Pet Name"
            condition = change_match.group(2)
            priority_list.append({
                'type': 'change',
                'target': target,
                'condition': condition
            })
            continue
            
        # Regex for STANDBY
        if line.startswith('standby'):
            priority_list.append({
                'type': 'pass',
                'condition': None
            })
            
    return priority_list

def extract_priorities():
    print("Loading variations_with_scripts.json...")
    try:
        with open('variations_with_scripts.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: variations_with_scripts.json not found.")
        return

    priorities_db = {} # Key: "id1,id2,id3", Value: PriorityList
    
    count = 0
    
    for encounter_name, variations in data.items():
        for variant in variations:
            team = variant.get('team')
            script = variant.get('script')
            
            if not team or not script: continue
            
            # Create a unique key for this team composition
            # Sort of... exact order matters for scripts usually
            team_key = ",".join(str(x) for x in team)
            
            parsed_script = parse_rematch_script(script)
            
            if parsed_script:
                priorities_db[team_key] = parsed_script
                count += 1
                
    print(f"Extracted scripts for {count} teams.")
    
    with open('player_scripts.json', 'w') as f:
        json.dump(priorities_db, f, indent=2)
    print("Saved to player_scripts.json")

if __name__ == "__main__":
    extract_priorities()
