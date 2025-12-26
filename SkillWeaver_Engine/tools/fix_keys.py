#!/usr/bin/env python3
"""
Fix spec files to correct key layout: F13, F16, F17, F18, F19, HOME, END, DELETE
Maps by slot position, not by old key name.
"""
import json
from pathlib import Path

# Slot number to key mapping
SLOT_TO_KEY = {
    1: "F13",
    2: "F16",
    3: "F17",
    4: "F18",
    5: "F19",
    6: "HOME",
    7: "END",
    8: "DELETE",
}

SPECS_DIR = Path("/Users/jgrayson/Documents/MyAddons-Mono/SkillWeaver_Engine/Brain/data/specs")

def fix_spec(filepath):
    with open(filepath, 'r') as f:
        spec = json.load(f)
    
    modified = False
    
    if "universal_slots" in spec:
        for slot_id, slot in spec["universal_slots"].items():
            # Extract slot number from slot_id (e.g., "slot_01" -> 1)
            try:
                slot_num = int(slot_id.replace('slot_', '').lstrip('0') or '0')
            except:
                continue
                
            # Only fix slots 1-8 (base rotation slots)
            if slot_num in SLOT_TO_KEY:
                correct_key = SLOT_TO_KEY[slot_num]
                if slot.get("key") != correct_key:
                    old_key = slot.get("key", "None")
                    slot["key"] = correct_key
                    modified = True
                    print(f"  {slot_id}: {old_key} -> {correct_key}")
    
    if modified:
        with open(filepath, 'w') as f:
            json.dump(spec, f, indent=4)
        return True
    return False

def main():
    print("=== Fix Key Layout: F13, F16-F19, HOME, END, DELETE ===\n")
    spec_files = list(SPECS_DIR.glob("*.json"))
    print(f"Found {len(spec_files)} spec files\n")
    
    fixed = 0
    for spec_file in sorted(spec_files):
        print(f"Processing: {spec_file.name}")
        if fix_spec(spec_file):
            fixed += 1
    
    print(f"\n=== Done! Fixed {fixed} files ===")

if __name__ == "__main__":
    main()
