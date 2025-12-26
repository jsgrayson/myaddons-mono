#!/usr/bin/env python3
"""
Add cooldown values to spec files.
DoTs get longer CDs (12s), spenders get GCD (1.5s), fillers get 0.
"""
import json
from pathlib import Path

SPECS_DIR = Path("/Users/jgrayson/Documents/MyAddons-Mono/SkillWeaver_Engine/Brain/data/specs")

# Ability type -> cooldown in seconds
ABILITY_COOLDOWNS = {
    # DoTs (should only reapply when falling off)
    "Vampiric Touch": 12.0,
    "Shadow Word: Pain": 12.0,
    "Agony": 12.0,
    "Corruption": 12.0,
    "Unstable Affliction": 12.0,
    "Immolate": 12.0,
    "Rake": 10.0,
    "Rip": 12.0,
    "Garrote": 15.0,
    "Rupture": 12.0,
    "Flame Shock": 12.0,
    "Moonfire": 10.0,
    "Sunfire": 10.0,
    
    # Major cooldowns (longer)
    "Void Eruption": 90.0,
    "Power Infusion": 120.0,
    "Summon Darkglare": 120.0,
    "Apocalypse": 60.0,
    "Metamorphosis": 120.0,
    "Combustion": 120.0,
    "Icy Veins": 120.0,
    "Avenging Wrath": 120.0,
    "Shadow Dance": 60.0,
    "Vendetta": 120.0,
    "Berserk": 120.0,
    "Tiger's Fury": 30.0,
    "Pillar of Frost": 60.0,
    "Breath of Sindragosa": 120.0,
    
    # Builders/Spenders (just GCD)
    "Mind Blast": 9.0,  # Actually has 9s CD
    "Kill Command": 6.0,
    "Barbed Shot": 12.0,
    "Bite": 1.5,
    
    # Fillers (GCD only)
    "Mind Flay": 0.5,  # Short CD so it cycles
    "Shadow Bolt": 0.5,
    "Frostbolt": 0.5,
    "Fireball": 0.5,
    "Arcane Blast": 0.5,
    "Wrath": 0.5,
    "Smite": 0.5,
    "Incinerate": 0.5,
    "Cobra Shot": 0.5,
    "Steady Shot": 0.5,
}

def add_cooldowns(filepath):
    with open(filepath, 'r') as f:
        spec = json.load(f)
    
    modified = False
    
    if "universal_slots" in spec:
        for slot_id, slot in spec["universal_slots"].items():
            action = slot.get("action", "")
            if action in ABILITY_COOLDOWNS:
                old_cd = slot.get("cooldown")
                new_cd = ABILITY_COOLDOWNS[action]
                if old_cd != new_cd:
                    slot["cooldown"] = new_cd
                    modified = True
                    print(f"  {slot_id}: {action} -> {new_cd}s CD")
    
    if modified:
        with open(filepath, 'w') as f:
            json.dump(spec, f, indent=4)
        return True
    return False

def main():
    print("=== Adding Cooldowns to Spec Files ===\n")
    spec_files = list(SPECS_DIR.glob("*.json"))
    print(f"Found {len(spec_files)} spec files\n")
    
    updated = 0
    for spec_file in sorted(spec_files):
        print(f"Processing: {spec_file.name}")
        if add_cooldowns(spec_file):
            updated += 1
    
    print(f"\n=== Done! Updated {updated} files ===")

if __name__ == "__main__":
    main()
