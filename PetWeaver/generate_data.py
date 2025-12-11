import json
import os

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def generate_lua_table(data, indent=0):
    """Recursively generates a Lua table string from a Python dict/list."""
    spaces = "    " * indent
    if isinstance(data, dict):
        lua_str = "{\n"
        for k, v in data.items():
            key_str = f'["{k}"]' if isinstance(k, str) else f"[{k}]"
            lua_str += f"{spaces}    {key_str} = {generate_lua_table(v, indent + 1)},\n"
        lua_str += f"{spaces}}}"
        return lua_str
    elif isinstance(data, list):
        lua_str = "{\n"
        for item in data:
            lua_str += f"{spaces}    {generate_lua_table(item, indent + 1)},\n"
        lua_str += f"{spaces}}}"
        return lua_str
    elif isinstance(data, str):
        # Escape newlines and quotes
        safe_str = data.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '')
        return f'"{safe_str}"'
    elif isinstance(data, bool):
        return "true" if data else "false"
    elif data is None:
        return "nil"
    else:
        return str(data)

def main():
    base_path = "/Users/jgrayson/Documents/petweaver"
    
    print("Loading data...")
    my_pets_data = load_json(os.path.join(base_path, "my_pets.json"))
    strategies_enhanced = load_json(os.path.join(base_path, "strategies_enhanced.json"))
    strategies_variations = load_json(os.path.join(base_path, "deprecated/variations_with_scripts.json"))
    encounters_data = load_json(os.path.join(base_path, "encounters_converted.json"))

    # 1. Build Name -> Species ID Map (from My Pets)
    # We use a dictionary to map Name -> Species ID. 
    # If multiple pets have the same name, any valid species ID is fine (usually they are the same species).
    my_pet_map = {} 
    for pet in my_pets_data.get("pets", []):
        name = pet["species"]["name"]["en_US"]
        species_id = pet["species"]["id"]
        my_pet_map[name] = species_id
    
    print(f"Found {len(my_pet_map)} unique pet names in collection.")

    # 2. Build Xu-Fu ID -> Name Map (from Strategies Enhanced)
    xufu_id_to_name = {}
    
    def extract_ids(data):
        if isinstance(data, dict):
            if "id" in data and "name" in data:
                xufu_id_to_name[data["id"]] = data["name"]
            for v in data.values():
                extract_ids(v)
        elif isinstance(data, list):
            for item in data:
                extract_ids(item)
                
    extract_ids(strategies_enhanced)
    print(f"Found {len(xufu_id_to_name)} Xu-Fu ID mappings.")

    # 3. Process Strategies and Filter
    valid_teams = []
    
    for encounter_name, teams in strategies_variations.items():
        for team_entry in teams:
            team_pets_xufu = team_entry.get("team", [])
            script = team_entry.get("script", "")
            
            # Check if we have all pets
            has_all_pets = True
            final_team_pets = []
            
            for xufu_id in team_pets_xufu:
                if xufu_id == 0:
                    final_team_pets.append(0) # Empty/Leveling slot
                    continue
                
                pet_name = xufu_id_to_name.get(xufu_id)
                if not pet_name:
                    # Try to find name in my_pet_map by checking if xufu_id matches any species_id? 
                    # Unlikely, but let's assume missing name means unknown pet.
                    has_all_pets = False
                    break
                
                # Check if we own this pet
                if pet_name in my_pet_map:
                    final_team_pets.append(my_pet_map[pet_name])
                else:
                    has_all_pets = False
                    break
            
            if has_all_pets and any(pid != 0 for pid in final_team_pets):
                # Create the team object for Lua
                lua_team = {
                    "name": f"{encounter_name} Team",
                    "encounterName": encounter_name,
                    "pets": final_team_pets,
                    "script": script,
                    "isLeveling": False 
                }
                valid_teams.append(lua_team)

    print(f"Found {len(valid_teams)} valid teams matching your collection.")

    # 4. Process Encounters
    lua_encounters = {}
    for key, encounter in encounters_data.items():
        display_name = encounter.get("name")
        if display_name:
            lua_encounters[display_name] = {
                "npcPets": encounter.get("npc_pets", []),
                "id": key 
            }

    # 5. Generate Lua Files
    print("Generating Lua files...")
    
    # teams_data.lua
    with open(os.path.join(base_path, "PetWeaver/teams_data.lua"), "w") as f:
        f.write("PetWeaver_DefaultTeams = ")
        f.write(generate_lua_table(valid_teams))
        f.write("\n")
        
    # encounters_data.lua
    with open(os.path.join(base_path, "PetWeaver/encounters_data.lua"), "w") as f:
        f.write("PetWeaver_Encounters = ")
        f.write(generate_lua_table(lua_encounters))
        f.write("\n")

    print("Done!")

if __name__ == "__main__":
    main()
