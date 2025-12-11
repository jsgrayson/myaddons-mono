import json
from pathlib import Path

# Paths
ENCOUNTERS_PATH = Path("encounters.json")
ABILITIES_PATH = Path("abilities.json")

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Could not find {path}")
        return {}

def main():
    print("Loading data...")
    encounters = load_json(ENCOUNTERS_PATH)
    ability_data = load_json(ABILITIES_PATH)
    
    # Map: SpeciesID (int) -> [AbilityID, AbilityID...]
    # Ensure keys are strings for lookup
    species_abilities = ability_data.get("species_abilities", {})
    
    # Map: AbilityID (str) -> {name, cooldown, ...}
    abilities_db = ability_data.get("abilities", {})
    
    print(f"Loaded {len(species_abilities)} species definitions.")
    
    
    updated_count = 0
    
    # Encounters is a dict with encounter names as keys
    print(f"Scanning {len(encounters)} encounters for missing abilities...")
    
    for enc_key, enc_data in encounters.items():
        # Each encounter is a dict with 'npc_pets' key
        pets = enc_data.get("pets") or enc_data.get("npc_pets") or []
        
        for pet in pets:
            # Check if abilities are missing/empty
            if not pet.get("abilities"):
                sid = str(pet.get("species_id"))
                
                if sid in species_abilities:
                    # Found valid ability list!
                    ab_ids = species_abilities[sid]
                    
                    # Hydrate full ability info
                    full_abilities = []
                    for aid in ab_ids:
                        aid_str = str(aid)
                        if aid_str in abilities_db:
                            info = abilities_db[aid_str]
                            full_abilities.append({
                                "id": int(aid),
                                "name": info.get("name", f"Ability {aid}"),
                                "cooldown": info.get("cooldown", 0),
                                "type": info.get("family_id", 0) # Useful for logic
                            })
                    
                    # Update the pet
                    pet["abilities"] = full_abilities
                    updated_count += 1
                    print(f"  Hydrated {pet['name']} (species {sid}) with {len(full_abilities)} abilities")

    
    # Save fixed file
    with open(ENCOUNTERS_PATH, "w", encoding="utf-8") as f:
        json.dump(encounters, f, indent=2)
        
    print(f"✅ Success! Hydrated {updated_count} pets with real ability data.")
    print("You can now run 'generate_final_npc_move_orders.py' to generate valid scripts.")

if __name__ == "__main__":
    main()
