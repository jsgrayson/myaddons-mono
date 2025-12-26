#!/usr/bin/env python3
"""
add_shift_row_to_all_specs.py - Adds slots 27-36 (Shift+F15-F24) to all spec files.

This ensures all specs have abilities mapped to the full 36-key grid:
- Row 1: F13-F24 (slots 1-12)
- Row 2: Ctrl+F13-F24 (slots 13-24)
- Row 3: Shift+F13-F24 (slots 25-36)
"""

import os
import json

SPECS_DIR = os.path.join(os.path.dirname(__file__), "..", "Brain", "data", "specs")

# Default abilities for each class's Shift row (slots 27-36)
# These are common PvP/talent abilities that might be swapped in
CLASS_SHIFT_ABILITIES = {
    # Warrior (1x)
    "warrior": [
        "Bladestorm", "Ravager", "Thunder Clap", "Rallying Cry", 
        "Spell Reflection", "Shattering Throw", "Intimidating Shout",
        "Heroic Throw", "Intervene", "Berserker Rage"
    ],
    # Paladin (2x)
    "paladin": [
        "Avenging Wrath", "Divine Toll", "Execution Sentence", "Holy Avenger",
        "Seraphim", "Final Reckoning", "Wake of Ashes",
        "Turn Evil", "Blessing of Freedom", "Cleanse"
    ],
    # Hunter (3x)
    "hunter": [
        "Binding Shot", "Steel Trap", "Scatter Shot", "Intimidation",
        "Kill Command", "Mend Pet", "Roar of Sacrifice",
        "Disengage", "Exhilaration", "Aspect of the Turtle"
    ],
    # Rogue (4x)
    "rogue": [
        "Shadowstep", "Shiv", "Blind", "Smoke Bomb",
        "Shadow Dance", "Marked for Death", "Thistle Tea",
        "Tricks of the Trade", "Shroud of Concealment", "Distract"
    ],
    # Priest (5x)
    "priest": [
        "Mind Spike", "Dark Ascension", "Mindbender", "Shadow Word: Horror",
        "Damnation", "Mind Sear", "Angelic Feather",
        "Thoughtsteal", "Mind Control", "Shackle Undead"
    ],
    # Death Knight (6x)
    "deathknight": [
        "Anti-Magic Zone", "Abomination Limb", "Raise Ally", "Lichborne",
        "Death and Decay", "Death Coil", "Remorseless Winter",
        "Control Undead", "Chains of Ice", "Path of Frost"
    ],
    # Shaman (7x)
    "shaman": [
        "Capacitor Totem", "Earthgrab Totem", "Wind Rush Totem", "Tremor Totem",
        "Ancestral Guidance", "Spirit Link Totem", "Healing Stream Totem",
        "Bloodlust", "Astral Shift", "Earth Elemental"
    ],
    # Mage (8x)
    "mage": [
        "Ice Block", "Shimmer", "Alter Time", "Ring of Frost",
        "Dragon's Breath", "Supernova", "Arcane Explosion",
        "Slow Fall", "Time Warp", "Remove Curse"
    ],
    # Warlock (9x)
    "warlock": [
        "Demonic Circle", "Howl of Terror", "Dark Pact", "Mortal Coil",
        "Soulburn", "Soul Rot", "Summon Infernal",
        "Soulstone", "Create Healthstone", "Banish"
    ],
    # Monk (10x)
    "monk": [
        "Touch of Death", "Leg Sweep", "Ring of Peace", "Diffuse Magic",
        "Fortifying Brew", "Detox", "Transcendence",
        "Paralysis", "Tiger's Lust", "Spear Hand Strike"
    ],
    # Druid (11x)
    "druid": [
        "Convoke the Spirits", "Heart of the Wild", "Nature's Vigil", "Typhoon",
        "Mass Entanglement", "Incapacitating Roar", "Stampeding Roar",
        "Remove Corruption", "Soothe", "Hibernate"
    ],
    # Demon Hunter (12x)
    "demonhunter": [
        "Darkness", "Netherwalk", "Rain from Above", "Spectral Sight",
        "Sigil of Flame", "Sigil of Misery", "Sigil of Silence",
        "Consume Magic", "Imprison", "Torment"
    ],
    # Evoker (13x)
    "evoker": [
        "Deep Breath", "Dream Flight", "Zephyr", "Oppressing Roar",
        "Landslide", "Quell", "Cauterizing Flame",
        "Time Spiral", "Blessing of the Bronze", "Expunge"
    ]
}

# Map spec_id to class
SPEC_TO_CLASS = {
    11: "warrior", 12: "warrior", 13: "warrior",  # Arms, Fury, Prot
    21: "paladin", 22: "paladin", 23: "paladin",  # Holy, Prot, Ret
    31: "hunter", 32: "hunter", 33: "hunter",     # BM, MM, Surv
    41: "rogue", 42: "rogue", 43: "rogue",        # Assa, Outlaw, Sub
    51: "priest", 52: "priest", 53: "priest",     # Disc, Holy, Shadow
    61: "deathknight", 62: "deathknight", 63: "deathknight",  # Blood, Frost, Unholy
    71: "shaman", 72: "shaman", 73: "shaman",     # Ele, Enh, Resto
    81: "mage", 82: "mage", 83: "mage",           # Arcane, Fire, Frost
    91: "warlock", 92: "warlock", 93: "warlock",  # Aff, Demo, Destro
    101: "monk", 102: "monk", 103: "monk",        # BrM, MW, WW
    111: "druid", 112: "druid", 113: "druid", 114: "druid",  # Bal, Feral, Guard, Resto
    121: "demonhunter", 122: "demonhunter", 123: "demonhunter",  # Havoc, Veng, ? (placeholder for Devourer)
    131: "evoker", 132: "evoker", 133: "evoker",  # Devas, Pres, Aug
}


def add_shift_slots(filepath):
    """Add slots 27-36 to a spec file if they don't exist."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    spec_id = data.get('spec_id')
    if not spec_id:
        return False
    
    class_name = SPEC_TO_CLASS.get(spec_id)
    if not class_name:
        print(f"  [SKIP] Unknown spec_id: {spec_id}")
        return False
    
    abilities = CLASS_SHIFT_ABILITIES.get(class_name, [])
    if not abilities:
        print(f"  [SKIP] No abilities defined for class: {class_name}")
        return False
    
    slots = data.get('universal_slots', {})
    
    # Check if slot_27 already exists (already has Shift row)
    if 'slot_27' in slots:
        print(f"  [SKIP] {os.path.basename(filepath)} already has Shift row")
        return False
    
    # Add slots 27-36 (Shift+F15 through Shift+F24)
    for i, ability in enumerate(abilities):
        slot_num = 27 + i
        key_num = 15 + i  # F15 through F24
        slots[f"slot_{slot_num:02d}"] = {
            "action": ability,
            "key": f"Shift+F{key_num}",
            "min_resource": 0,
            "conditions": ["target_valid"] if i < 7 else []
        }
    
    data['universal_slots'] = slots
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    
    return True


def main():
    print("Adding Shift Row (slots 27-36) to all spec files...")
    print("=" * 50)
    
    count = 0
    for filename in sorted(os.listdir(SPECS_DIR)):
        if filename.endswith('.json'):
            filepath = os.path.join(SPECS_DIR, filename)
            if add_shift_slots(filepath):
                print(f"  [+] Updated: {filename}")
                count += 1
    
    print("=" * 50)
    print(f"Done! Updated {count} files.")


if __name__ == "__main__":
    main()
