"""
Generates TARGETS configuration for all WoW classes and specs
"""

# All classes with spec IDs
CLASSES = {
    "DEATHKNIGHT": [
        {"spec": "Blood", "id": "250", "role": "tank"},
        {"spec": "Frost", "id": "251", "role": "dps"},
        {"spec": "Unholy", "id": "252", "role": "dps"},
    ],
    "DEMONHUNTER": [
        {"spec": "Havoc", "id": "577", "role": "dps"},
        {"spec": "Vengeance", "id": "581", "role": "tank"},
    ],
    "DRUID": [
        {"spec": "Balance", "id": "102", "role": "dps"},
        {"spec": "Feral", "id": "103", "role": "dps"},
        {"spec": "Guardian", "id": "104", "role": "tank"},
        {"spec": "Restoration", "id": "105", "role": "healer"},
    ],
    "EVOKER": [
        {"spec": "Devastation", "id": "1467", "role": "dps"},
        {"spec": "Preservation", "id": "1468", "role": "healer"},
        {"spec": "Augmentation", "id": "1473", "role": "support"},
    ],
    "HUNTER": [
        {"spec": "Beast Mastery", "id": "253", "role": "dps"},
        {"spec": "Marksmanship", "id": "254", "role": "dps"},
        {"spec": "Survival", "id": "255", "role": "dps"},
    ],
    "MAGE": [
        {"spec": "Arcane", "id": "62", "role": "dps"},
        {"spec": "Fire", "id": "63", "role": "dps"},
        {"spec": "Frost", "id": "64", "role": "dps"},
    ],
    "MONK": [
        {"spec": "Brewmaster", "id": "268", "role": "tank"},
        {"spec": "Mistweaver", "id": "270", "role": "healer"},
        {"spec": "Windwalker", "id": "269", "role": "dps"},
    ],
    "PALADIN": [
        {"spec": "Holy", "id": "65", "role": "healer"},
        {"spec": "Protection", "id": "66", "role": "tank"},
        {"spec": "Retribution", "id": "70", "role": "dps"},
    ],
    "PRIEST": [
        {"spec": "Discipline", "id": "256", "role": "healer"},
        {"spec": "Holy", "id": "257", "role": "healer"},
        {"spec": "Shadow", "id": "258", "role": "dps"},
    ],
    "ROGUE": [
        {"spec": "Assassination", "id": "259", "role": "dps"},
        {"spec": "Outlaw", "id": "260", "role": "dps"},
        {"spec": "Subtlety", "id": "261", "role": "dps"},
    ],
    "SHAMAN": [
        {"spec": "Elemental", "id": "262", "role": "dps"},
        {"spec": "Enhancement", "id": "263", "role": "dps"},
        {"spec": "Restoration", "id": "264", "role": "healer"},
    ],
    "WARLOCK": [
        {"spec": "Affliction", "id": "265", "role": "dps"},
        {"spec": "Demonology", "id": "266", "role": "dps"},
        {"spec": "Destruction", "id": "267", "role": "dps"},
    ],
    "WARRIOR": [
        {"spec": "Arms", "id": "71", "role": "dps"},
        {"spec": "Fury", "id": "72", "role": "dps"},
        {"spec": "Protection", "id": "73", "role": "tank"},
    ],
}

def to_url_format(class_name, spec_name):
    """Convert to icy-veins URL format: death-knight, beast-mastery, etc."""
    # Map class names to URL format
    class_map = {
        "DEATHKNIGHT": "death-knight",
        "DEMONHUNTER": "demon-hunter",
        "DRUID": "druid",
        "EVOKER": "evoker",
        "HUNTER": "hunter",
        "MAGE": "mage",
        "MONK": "monk",
        "PALADIN": "paladin",
        "PRIEST": "priest",
        "ROGUE": "rogue",
        "SHAMAN": "shaman",
        "WARLOCK": "warlock",
        "WARRIOR": "warrior"
    }
    
    class_url = class_map.get(class_name, class_name.lower())
    spec_url = spec_name.lower().replace(" ", "-")
    return class_url, spec_url

def generate_targets():
    """Generate TARGETS list for all classes"""
    targets = []
    
    for class_name, specs in CLASSES.items():
        for spec_info in specs:
            class_url, spec_url = to_url_format(class_name, spec_info["spec"])
            role = spec_info["role"]
            
            target = {
                "class": class_name,
                "spec": spec_info["spec"],
                "spec_id": spec_info["id"],
                "modes": {}
            }
            
            # Raid
            target["modes"]["Raid"] = {
                "rotation": f"https://www.icy-veins.com/wow/{spec_url}-{class_url}-{role}-pve-rotation-cooldowns-abilities" if role != "tank" else f"https://www.icy-veins.com/wow/{spec_url}-{class_url}-tank-pve-rotation-cooldowns-abilities",
                "talents": f"https://www.icy-veins.com/wow/{spec_url}-{class_url}-{role}-pve-spec-builds-talents" if role != "tank" else f"https://www.icy-veins.com/wow/{spec_url}-{class_url}-tank-pve-spec-builds-talents",
                "wowhead": f"https://www.wowhead.com/guide/classes/{class_url}/{spec_url}/raid-pve-{role}" if role != "tank" else f"https://www.wowhead.com/guide/classes/{class_url}/{spec_url}/raid-tank"
            }
            
            # Mythic+
            target["modes"]["MythicPlus"] = {
                "rotation": f"https://www.icy-veins.com/wow/{spec_url}-{class_url}-{role}-pve-mythic-plus-tips" if role != "tank" else f"https://www.icy-veins.com/wow/{spec_url}-{class_url}-tank-pve-mythic-plus-tips",
                "talents": f"https://www.icy-veins.com/wow/{spec_url}-{class_url}-{role}-pve-mythic-plus-builds-talents" if role != "tank" else f"https://www.icy-veins.com/wow/{spec_url}-{class_url}-tank-pve-mythic-plus-builds-talents",
                "wowhead": f"https://www.wowhead.com/guide/classes/{class_url}/{spec_url}/mythic-plus-pve-{role}" if role != "tank" else f"https://www.wowhead.com/guide/classes/{class_url}/{spec_url}/mythic-plus-tank"
            }
            
            # Delves (use Raid as fallback since Delves guides might not exist)
            target["modes"]["Delves"] = target["modes"]["Raid"].copy()
            
            # PvP
            target["modes"]["PvP"] = {
                "rotation": f"https://www.icy-veins.com/wow/{spec_url}-{class_url}-pvp-{role}-rotation" if role != "tank" else f"https://www.icy-veins.com/wow/{spec_url}-{class_url}-pvp-tank-rotation",
                "talents": f"https://www.icy-veins.com/wow/{spec_url}-{class_url}-pvp-{role}-spec-builds-talents" if role != "tank" else f"https://www.icy-veins.com/wow/{spec_url}-{class_url}-pvp-tank-spec-builds-talents",
                "wowhead": f"https://www.wowhead.com/guide/classes/{class_url}/{spec_url}/pvp-arena"
            }
            
            targets.append(target)
    
    return targets

if __name__ == "__main__":
    targets = generate_targets()
    print(f"Generated {len(targets)} class/spec combinations")
    print(f"Total modes: {len(targets) * 4}")
    
    # Print sample
    for t in targets[:2]:
        print(f"\n{t['class']} - {t['spec']} ({t['spec_id']})")
        for mode in t['modes']:
            print(f"  {mode}")
