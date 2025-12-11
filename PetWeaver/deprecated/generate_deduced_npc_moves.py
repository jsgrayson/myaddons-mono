import json
import re
from pathlib import Path
from collections import defaultdict

STRATEGIES_FILE = Path(__file__).resolve().parent / "strategies_enhanced.json"
ENCOUNTERS_FILE = Path(__file__).resolve().parent / "encounters_full.json"
OUTPUT_FILE = Path(__file__).resolve().parent / "npc_deduced_moves.md"

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_ability_name(ability_id, ability_db):
    # This is a placeholder. In a real scenario we'd look up the ID.
    # We can try to find it in the encounters file if available.
    return f"Ability({ability_id})"

def analyze_npc(npc_name, strategies, npc_data):
    """
    Analyze all strategies for a single NPC to deduce move order.
    """
    # round_events[pet_index][round_num] = list of observations
    round_events = defaultdict(lambda: defaultdict(list))
    
    # known_abilities[pet_index] = set of ability IDs seen
    known_abilities = defaultdict(set)
    
    for strat in strategies:
        script = strat.get("script", "")
        lines = script.replace("\r", "\n").split("\n")
        
        current_pet_idx = 1 # Default to enemy pet 1
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith("--"):
                continue
            
            # Check for enemy pet changes in conditions? 
            # Usually scripts don't change enemy pets explicitly, but check enemy(#X).active
            
            # Regex for round conditions: [round=1], [round~1,3], [enemy.round=1]
            round_matches = re.findall(r'\[.*?(?:round|turn)[=~](\d+(?:,\d+)*).*?\]', line.lower())
            
            # Regex for ability checks: [enemy.ability(Name:123).usable]
            ability_matches = re.findall(r'enemy(?:\(#(\d)\))?\.ability\((?:[^:]+:)?(\d+)\)\.usable', line.lower())
            
            # Regex for aura checks: [enemy.aura(Name:123).exists]
            aura_matches = re.findall(r'enemy(?:\(#(\d)\))?\.aura\((?:[^:]+:)?(\d+)\)\.(?:exists|duration)', line.lower())
            
            # Regex for specific enemy active checks: [enemy(#2).active]
            active_match = re.search(r'enemy\(#(\d)\)\.active', line.lower())
            if active_match:
                current_pet_idx = int(active_match.group(1))
            
            # Process round matches
            for rounds in round_matches:
                # Split "1,3" into individual rounds
                for r in rounds.split(','):
                    try:
                        r_num = int(r)
                        # What is the player doing?
                        # Extract the command: use(Ability) or change(#)
                        command_match = re.match(r'(?:use|ability)\(([^)]+)\)|change\(([^)]+)\)', line)
                        action = "Unknown"
                        if command_match:
                            if command_match.group(1):
                                action = f"Player uses {command_match.group(1)}"
                            else:
                                action = f"Player changes to {command_match.group(2)}"
                        
                        round_events[current_pet_idx][r_num].append(action)
                    except ValueError:
                        pass

            # Process ability matches
            for pet_idx_str, ab_id in ability_matches:
                idx = int(pet_idx_str) if pet_idx_str else current_pet_idx
                known_abilities[idx].add(ab_id)
                
            # Process aura matches
            for pet_idx_str, aura_id in aura_matches:
                idx = int(pet_idx_str) if pet_idx_str else current_pet_idx
                # Auras often imply an ability was used previously
                pass

    return round_events, known_abilities

def generate_markdown(deduced_data):
    lines = ["# Deduced NPC Move Orders\n\n"]
    lines.append("> **Note:** This data is reverse-engineered from player strategies (Xufu).\n")
    lines.append("> It shows what players do on specific rounds, which implies the NPC's fixed behavior.\n\n")
    
    for expansion, npcs in deduced_data.items():
        lines.append(f"## {expansion}\n\n")
        for npc_name, data in npcs.items():
            lines.append(f"### {npc_name}\n\n")
            
            round_events = data['round_events']
            
            if not round_events:
                lines.append("*No round-specific data found in strategies.*\n\n")
                continue
                
            for pet_idx in sorted(round_events.keys()):
                lines.append(f"#### Enemy Pet #{pet_idx}\n")
                lines.append("| Round | Player Action (Implies NPC Move) |\n")
                lines.append("| :--- | :--- |\n")
                
                events = round_events[pet_idx]
                for r in sorted(events.keys()):
                    # Deduplicate actions
                    actions = sorted(list(set(events[r])))
                    action_str = "<br>".join(actions)
                    lines.append(f"| {r} | {action_str} |\n")
                lines.append("\n")
                
    return "".join(lines)

def main():
    strategies = load_json(STRATEGIES_FILE)
    # encounters = load_json(ENCOUNTERS_FILE) # Not strictly needed if we just parse scripts
    
    deduced_data = defaultdict(dict)
    
    for expansion, content in strategies.items():
        if isinstance(content, dict):
            for category, encounter_list in content.items():
                if isinstance(encounter_list, list):
                    for enc in encounter_list:
                        name = enc.get("encounter_name", "Unknown")
                        strats = enc.get("strategies", [])
                        
                        r_events, k_abilities = analyze_npc(name, strats, None)
                        
                        if r_events:
                            deduced_data[expansion][name] = {
                                'round_events': r_events,
                                'known_abilities': k_abilities
                            }
    
    md_content = generate_markdown(deduced_data)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"✅ Generated {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
