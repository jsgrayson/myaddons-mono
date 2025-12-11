import json
import re
from pathlib import Path
from collections import defaultdict

ENCOUNTERS_FILE = Path(__file__).resolve().parent / "encounters.json"
STRATEGIES_FILE = Path(__file__).resolve().parent / "strategies.json"
OUTPUT_FILE = Path(__file__).resolve().parent / "npc_move_orders.md"

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[WARN] File not found: {path}")
        return {}

def normalize_name(name):
    if not name: return ""
    return re.sub(r'[^a-z0-9]', '', name.lower())

def get_npc_data(encounters):
    npc_lookup = {}
    
    def process_list(enc_list):
        for enc in enc_list:
            name = enc.get('name') or enc.get('encounter_name')
            if not name: continue
            
            norm_name = normalize_name(name)
            pets = {}
            pet_list = enc.get('pets') or enc.get('npc_pets') or []
            
            for i, pet in enumerate(pet_list, 1):
                abilities = []
                raw_abilities = pet.get('abilities', [])
                for ab in raw_abilities:
                    if isinstance(ab, dict):
                        abilities.append(ab)
                    else:
                        abilities.append({'id': ab, 'name': f"Ability {ab}", 'cooldown': 0})
                
                pets[i] = {
                    'name': pet.get('name', f"Pet {i}"),
                    'species_id': pet.get('species_id'),
                    'abilities': abilities
                }
            
            npc_lookup[norm_name] = {'real_name': name, 'pets': pets}

    if isinstance(encounters, list): process_list(encounters)
    elif isinstance(encounters, dict):
        for key, val in encounters.items():
            if isinstance(val, list): process_list(val)
            elif isinstance(val, dict):
                for subkey, subval in val.items():
                    if isinstance(subval, list): process_list(subval)
                
    return npc_lookup

def build_ability_map(pets):
    mapping = {}
    for i, pet in pets.items():
        for ab in pet['abilities']:
            mapping[str(ab.get('id', ''))] = i
            if 'name' in ab: mapping[normalize_name(ab['name'])] = i
    return mapping

def analyze_strategies(strategies_data, npc_lookup):
    npc_observations = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    all_encounters = []
    if isinstance(strategies_data, list): all_encounters = strategies_data
    elif isinstance(strategies_data, dict):
        for k, v in strategies_data.items():
            if isinstance(v, list): all_encounters.extend(v)
            elif isinstance(v, dict):
                for subk, subv in v.items():
                    if isinstance(subv, list): all_encounters.extend(subv)

    for enc in all_encounters:
        name = enc.get("encounter_name") or enc.get("name")
        if not name: continue
        
        norm_name = normalize_name(name)
        if norm_name not in npc_lookup: continue
            
        npc_info = npc_lookup[norm_name]
        ability_map = build_ability_map(npc_info['pets'])
        
        for strat in enc.get("strategies", []):
            script = strat.get("script", "")
            lines = script.replace("\r", "\n").split("\n")
            current_pet_idx = 1
            
            for line in lines:
                line = line.strip().lower()
                if not line or line.startswith("--"): continue
                
                active_match = re.search(r'enemy\(#(\d)\)\.(?:active|exists|dead)', line)
                if active_match: current_pet_idx = int(active_match.group(1))
                
                ability_matches = re.findall(r'ability\(([^)]+)\)', line)
                for ab_ref in ability_matches:
                    clean_ref = normalize_name(ab_ref.strip("'\""))
                    if clean_ref in ability_map: current_pet_idx = ability_map[clean_ref]

                round_matches = re.findall(r'\[.*?(?:round|turn)[=~](\d+(?:,\d+)*).*?\]', line)
                
                action = "attack"
                if any(x in line for x in ['dodge', 'deflect', 'block', 'decoy', 'avoid']): action = "nuke"
                elif "change" in line: action = "swap"

                for rounds in round_matches:
                    for r in rounds.split(','):
                        try:
                            r_num = int(r)
                            npc_observations[norm_name][current_pet_idx][r_num].append(action)
                        except: pass
                                        
    return npc_observations

def simulate_npc_move_order(pet_data, observations, max_rounds=15):
    move_order = []
    abilities = pet_data['abilities']
    cooldowns = {ab['id']: 0 for ab in abilities}
    
    # Priority: 3 > 2 > 1
    sorted_abilities = sorted(abilities, key=lambda x: abilities.index(x), reverse=True)
    
    # Identify the "Filler" move (0 Cooldown)
    filler_move = None
    for ab in abilities:
        if ab.get('cooldown', 0) == 0:
            filler_move = ab
            break
    if not filler_move and abilities: filler_move = abilities[0] # Fallback

    for r in range(1, max_rounds + 1):
        selected_ability = None
        obs = observations.get(r, [])
        is_nuke_turn = "nuke" in obs
        
        usable = [ab for ab in sorted_abilities if cooldowns[ab['id']] == 0]
        
        if not usable:
            # CRITICAL FIX: Use Filler if everything is on CD
            if filler_move:
                selected_ability = filler_move
            else:
                move_order.append("Pass")
                continue
        else:
            if is_nuke_turn:
                selected_ability = max(usable, key=lambda x: x.get('cooldown', 0))
            else:
                selected_ability = usable[0]
            
        move_order.append(selected_ability['name'])
        
        for ab_id in cooldowns:
            if cooldowns[ab_id] > 0: cooldowns[ab_id] -= 1
            
        cooldowns[selected_ability['id']] = selected_ability.get('cooldown', 0)
        
    return move_order

def generate_markdown(npc_lookup, npc_observations):
    lines = ["# NPC Move Orders (Auto-Generated)\n\n"]
    
    for norm_name in sorted(npc_lookup.keys()):
        npc_data = npc_lookup[norm_name]
        real_name = npc_data['real_name']
        pets = npc_data['pets']
        
        lines.append(f"## {real_name}\n")
        
        for i in range(1, 4):
            if i not in pets: continue
            pet = pets[i]
            
            lines.append(f"### Pet {i}: {pet['name']}\n")
            
            obs = npc_observations.get(norm_name, {}).get(i, {})
            moves = simulate_npc_move_order(pet, obs)
            
            lines.append("| Round | Predicted Move | Type |\n| :--- | :--- | :--- |\n")
            for r, move in enumerate(moves, 1):
                move_type = "Cooldown"
                if obs.get(r) and "nuke" in obs.get(r): move_type = "Scripted Nuke"
                elif r == 1: move_type = "Opener"
                
                lines.append(f"| {r} | {move} | {move_type} |\n")
            lines.append("\n")
            
    return "".join(lines)

def main():
    print("Loading data...")
    encounters = load_json(ENCOUNTERS_FILE)
    strategies = load_json(STRATEGIES_FILE)
    
    print("Processing NPC data...")
    npc_lookup = get_npc_data(encounters)
    
    print("Cross-referencing strategies...")
    npc_observations = analyze_strategies(strategies, npc_lookup)
    
    print("Generating move orders...")
    md_content = generate_markdown(npc_lookup, npc_observations)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"✅ Generated {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
