import os

# Mock Data (normally queried from DB)
MOCK_LOADOUTS = {
    577: { # Havoc DH
        "Raid": "BEkAAAAAAAAAAAAAAAAAAAAAAQCJhkIkkk0IJtkkkAAAAAAASLJpQikkkWSLJhAAAAAA",
        "MythicPlus": "BEkAAAAAAAAAAAAAAAAAAAAAAQCJhkIkkk0IJtkkkAAAAAAASLJpQikkkWSLJhAAAAAA", # Same for now
        "PvP": "BEkAAAAAAAAAAAAAAAAAAAAAAQCJhkIkkk0IJtkkkAAAAAAASLJpQikkkWSLJhAAAAAA"
    },
    257: { # Holy Priest
        "Raid": "BAQAAAAAAAAAAAAAAAAAAAAAA0k0SjIJRjkkk0IJtkkkAAAAAAASLJpQikkkWSLJhAAAAAA",
        "MythicPlus": "BAQAAAAAAAAAAAAAAAAAAAAAA0k0SjIJRjkkk0IJtkkkAAAAAAASLJpQikkkWSLJhAAAAAA"
    }
}

# Mock Stat Weights (Normalized)
MOCK_WEIGHTS = {
    577: { # Havoc DH
        "Raid": { "Agility": 1.0, "Crit": 1.2, "Haste": 0.8, "Mastery": 1.1, "Versatility": 0.9 },
        "MythicPlus": { "Agility": 1.0, "Crit": 1.1, "Haste": 0.9, "Mastery": 1.0, "Versatility": 1.3 }
    },
    257: { # Holy Priest
        "Raid": { "Intellect": 1.0, "Crit": 1.1, "Haste": 0.9, "Mastery": 1.2, "Versatility": 0.8 },
        "MythicPlus": { "Intellect": 1.0, "Crit": 1.2, "Haste": 1.1, "Mastery": 0.9, "Versatility": 1.0 }
    }
}

def export_loadouts_to_lua():
    """Generates SkillWeaver_Data.lua from mock data."""
    
    # Path to Addon Data (Mocking the WoW directory structure locally for verification)
    # In real usage, this would be the user's WoW path.
    output_dir = "mock_wow/Interface/AddOns/SkillWeaver/Data"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Loadouts
    output_file_loadouts = os.path.join(output_dir, "Loadouts.lua")
    with open(output_file_loadouts, "w") as f:
        f.write("SkillWeaverDB = SkillWeaverDB or {}\n")
        f.write("SkillWeaverDB.Loadouts = {\n")
        
        for spec_id, content_map in MOCK_LOADOUTS.items():
            f.write(f"    [{spec_id}] = {{\n")
            for content_type, loadout_string in content_map.items():
                f.write(f"        [\"{content_type}\"] = \"{loadout_string}\",\n")
            f.write("    },\n")
            
        f.write("}\n")
    print(f"Exported loadouts to {output_file_loadouts}")

    # 2. Stat Weights
    output_file_weights = os.path.join(output_dir, "StatWeights.lua")
    with open(output_file_weights, "w") as f:
        f.write("SkillWeaverDB = SkillWeaverDB or {}\n")
        f.write("SkillWeaverDB.StatWeights = {\n")
        
        for spec_id, content_map in MOCK_WEIGHTS.items():
            f.write(f"    [{spec_id}] = {{\n")
            for content_type, weights in content_map.items():
                f.write(f"        [\"{content_type}\"] = {{\n")
                for stat, value in weights.items():
                    f.write(f"            [\"{stat}\"] = {value},\n")
                f.write("        },\n")
            f.write("    },\n")
            
        f.write("}\n")
    print(f"Exported stat weights to {output_file_weights}")

if __name__ == "__main__":
    export_loadouts_to_lua()
