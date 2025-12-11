import json
import re
from pathlib import Path
from collections import defaultdict

# FILE PATHS
ENCOUNTERS_FILE = Path(__file__).resolve().parent / "encounters.json"
STRATEGIES_FILE = Path(__file__).resolve().parent / "strategies_enhanced.json"  # FIXED: Use existing file
ABILITIES_FILE = Path(__file__).resolve().parent / "abilities.json" # CRITICAL
OUTPUT_FILE = Path(__file__).resolve().parent / "npc_move_orders.json"

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

def get_npc_data(encounters, abilities_db):
    npc_lookup = {}
    
    # Handle both list and dict formats
    enc_list = []
    if isinstance(encounters, list):
        enc_list = encounters
    elif isinstance(encounters, dict):
        # Dict format: convert to list
        for enc_key, enc_data in encounters.items():
            enc_list.append(enc_data)
    
    # Process encounters
    for enc_data in enc_list:
        name = enc_data.get('name', 'Unknown')
        
        norm_name = normalize_name(name)
        pets = {}
        pet_list = enc_data.get('pets') or enc_data.get('npc_pets') or []
        
        for i, pet in enumerate(pet_list, 1):
            final_abilities = []
            raw_abilities = pet.get('abilities', [])
            
            for ab in raw_abilities:
                ab_id = None
                if isinstance(ab, dict): ab_id = ab.get('id')
                else: ab_id = ab
                
                # LOOKUP REAL STATS IN ABILITY DB
                real_stats = abilities_db.get(str(ab_id)) or abilities_db.get(ab_id)
                
                if real_stats:
                    final_abilities.append({
                        'id': int(ab_id),
                        'name': real_stats.get('name', f"Ability {ab_id}"),
                        'cooldown': real_stats.get('cooldown', 0)
                    })
                else:
                    # If missing in DB, default to 0 CD
                    name_guess = ab.get('name', f"Ability {ab_id}") if isinstance(ab, dict) else f"Ability {ab_id}"
                    final_abilities.append({'id': int(ab_id), 'name': name_guess, 'cooldown': 0})
            
            pets[i] = {
                'name': pet.get('name', f"Pet {i}"),
                'species_id': pet.get('species_id'),
                'abilities': final_abilities
            }
        
        npc_lookup[norm_name] = {'real_name': name, 'pets': pets}
                
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

def simulate_npc_move_order(pet_data, observations, max_rounds=20):
    move_order = {}
    abilities = pet_data['abilities']
    
    # If no abilities found, return empty dict (prevents crash/spam)
    if not abilities: return {}

    cooldowns = {ab['id']: 0 for ab in abilities}
    
    # Priority: Slot 3 > Slot 2 > Slot 1
    sorted_abilities = sorted(abilities, key=lambda x: abilities.index(x), reverse=True)
    
    # Identify Filler Move (0 Cooldown)
    filler_move = None
    for ab in abilities:
        if ab.get('cooldown', 0) == 0:
            filler_move = ab
            break
    # If no explicit 0-CD move found, default to first ability (better than passing)
    if not filler_move and abilities: filler_move = abilities[0]

    for r in range(1, max_rounds + 1):
        selected_ability = None
        obs = observations.get(r, [])
        is_nuke_turn = "nuke" in obs
        
        # Filter usable (CD=0)
        usable = [ab for ab in sorted_abilities if cooldowns[ab['id']] == 0]
        
        if not usable:
            # If everything on CD, use filler
            if filler_move: selected_ability = filler_move
            else: continue # Pass
        else:
            if is_nuke_turn:
                selected_ability = max(usable, key=lambda x: x.get('cooldown', 0))
            else:
                selected_ability = usable[0]
            
        move_order[str(r)] = selected_ability['name']
        
        for ab_id in cooldowns:
            if cooldowns[ab_id] > 0: cooldowns[ab_id] -= 1
            
        cooldowns[selected_ability['id']] = selected_ability.get('cooldown', 0)
        
    return move_order

def generate_json(npc_lookup, npc_observations):
    output = {}
    
    for norm_name in npc_lookup:
        npc_data = npc_lookup[norm_name]
        real_name = npc_data['real_name']
        pets = npc_data['pets']
        
        npc_moves = {}
        for i in range(1, 4):
            if i not in pets: continue
            pet = pets[i]
            obs = npc_observations.get(norm_name, {}).get(i, {})
            moves = simulate_npc_move_order(pet, obs)
            npc_moves[str(i)] = moves
            
        output[real_name] = npc_moves
        
    return output

def main():
    print("Loading data...")
    encounters = load_json(ENCOUNTERS_FILE)
    strategies = load_json(STRATEGIES_FILE)
    
    # NEW: Load Abilities DB
    ability_data_full = load_json(ABILITIES_FILE)
    abilities_db = ability_data_full.get('abilities', {})
    print(f"Loaded {len(abilities_db)} ability definitions.")
    
    print("Processing NPC data...")
    # Pass ability DB to hydration function
    npc_lookup = get_npc_data(encounters, abilities_db)
    print(f"Found {len(npc_lookup)} NPCs.")
    
    print("Cross-referencing strategies...")
    npc_observations = analyze_strategies(strategies, npc_lookup)
    
    print("Generating move orders...")
    json_content = generate_json(npc_lookup, npc_observations)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(json_content, f, indent=2)
        
    print(f"✅ Generated {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
