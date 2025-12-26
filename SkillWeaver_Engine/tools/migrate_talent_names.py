import os
import json

specs_dir = "/Users/jgrayson/Documents/MyAddons-Mono/SkillWeaver_Engine/Brain/data/specs/"

def migrate_specs():
    for filename in os.listdir(specs_dir):
        if not filename.endswith(".json"):
            continue
            
        file_path = os.path.join(specs_dir, filename)
        
        # Get the spec name from the filename (e.g., "53_shadow.json" -> "shadow")
        name_part = filename.split("_", 1)[1].replace(".json", "")
        
        with open(file_path, "r") as f:
            data = json.load(f)
            
        if "talent_loadouts" not in data:
            continue
            
        old_loadouts = data["talent_loadouts"]
        new_loadouts = {}
        
        # Standard content keys
        content_keys = ["mythic", "raid", "delve", "pvp"]
        
        modified = False
        for key in content_keys:
            if key in old_loadouts:
                new_key = f"{name_part}_{key}"
                new_loadouts[new_key] = old_loadouts[key]
                modified = True
            elif f"{name_part}_{key}" in old_loadouts:
                # Already migrated or manually set
                new_loadouts[f"{name_part}_{key}"] = old_loadouts[f"{name_part}_{key}"]
        
        # Keep any other keys
        for key, value in old_loadouts.items():
            if key not in content_keys and not key.startswith(f"{name_part}_"):
                new_loadouts[key] = value
                
        if modified:
            data["talent_loadouts"] = new_loadouts
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Migrated {filename}: keys {list(new_loadouts.keys())}")

if __name__ == "__main__":
    migrate_specs()
