#!/usr/bin/env python3
"""
Migrate spec files to new key layout: F13, F16-F19, HOME, END, DELETE
"""
import json
from pathlib import Path

# Key mapping: old slot position -> new key name
# Slot 1: F13, Slot 2: F16, Slot 3: F17, Slot 4: F18, Slot 5: F19
# Slot 6: HOME, Slot 7: END, Slot 8: DELETE
KEY_REMAP = {
    "F13": "F13",
    "F14": "F16",
    "F15": "F17", 
    "F16": "F18",
    "F17": "F19",
    "F18": "HOME",
    "F19": "END",
    "F20": "DELETE",
    # Also remap the ones I changed earlier
    "INSERT": "HOME",
    "PRINTSCREEN": "DELETE",
}

SPECS_DIR = Path("/Users/jgrayson/Documents/MyAddons-Mono/SkillWeaver_Engine/Brain/data/specs")

def migrate_spec(filepath):
    with open(filepath, 'r') as f:
        spec = json.load(f)
    
    modified = False
    
    if "universal_slots" in spec:
        for slot_id, slot in spec["universal_slots"].items():
            if "key" in slot and slot["key"] in KEY_REMAP:
                old_key = slot["key"]
                new_key = KEY_REMAP[old_key]
                if old_key != new_key:
                    slot["key"] = new_key
                    modified = True
                    print(f"  {slot_id}: {old_key} -> {new_key}")
    
    if modified:
        with open(filepath, 'w') as f:
            json.dump(spec, f, indent=4)
        return True
    return False

def main():
    print("=== Key Migration: F13, F16-F19, HOME, END, DELETE ===\n")
    spec_files = list(SPECS_DIR.glob("*.json"))
    print(f"Found {len(spec_files)} spec files\n")
    
    migrated = 0
    for spec_file in sorted(spec_files):
        print(f"Processing: {spec_file.name}")
        if migrate_spec(spec_file):
            migrated += 1
    
    print(f"\n=== Done! Migrated {migrated} files ===")

if __name__ == "__main__":
    main()
