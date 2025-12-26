#!/usr/bin/env python3
"""
Generate Lua rotation data from spec JSON files for SkillWeaver addon.
Outputs a Lua file with 32 slots per spec:
- Bar 6 slots 1-8 (action slots 61-68)
- Bar 7 slots 1-8 (action slots 73-80)  
- Bar 8 slots 1-8 (action slots 85-92)
- Bar 6 slots 9-12 (action slots 69-72) - Alt modifier
- Bar 7 slots 9-12 (action slots 81-84) - Shift+Alt modifier
"""
import json
from pathlib import Path

SPECS_DIR = Path("/Users/jgrayson/Documents/MyAddons-Mono/SkillWeaver_Engine/Brain/data/specs")
OUTPUT_FILE = Path("/Users/jgrayson/Documents/MyAddons-Mono/SkillWeaver/data/SpecRotations.lua")

def load_spec(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def extract_spells(spec):
    """Extract spell names for all 32 slots from universal_slots."""
    bars = {
        "bar6_main": [],   # Slots 1-8 (action 61-68)
        "bar7_main": [],   # Slots 9-16 -> bar 7 slots 1-8 (action 73-80)
        "bar8_main": [],   # Slots 17-24 -> bar 8 slots 1-8 (action 85-92)
        "bar6_alt": [],    # Slots 25-28 -> bar 6 slots 9-12 (action 69-72)
        "bar7_alt": [],    # Slots 29-32 -> bar 7 slots 9-12 (action 81-84)
    }
    
    universal = spec.get("universal_slots", {})
    
    # Bar 6 main: slots 1-8
    for i in range(1, 9):
        slot_key = f"slot_{i:02d}"
        slot = universal.get(slot_key, {})
        action = slot.get("action", "")
        bars["bar6_main"].append(action if action else "")
    
    # Bar 7 main: slots 9-16
    for i in range(9, 17):
        slot_key = f"slot_{i:02d}"
        slot = universal.get(slot_key, {})
        action = slot.get("action", "")
        bars["bar7_main"].append(action if action else "")
    
    # Bar 8 main: slots 17-24
    for i in range(17, 25):
        slot_key = f"slot_{i:02d}"
        slot = universal.get(slot_key, {})
        action = slot.get("action", "")
        bars["bar8_main"].append(action if action else "")
    
    # Bar 6 alt (slots 9-12): slots 25-28 in spec
    for i in range(25, 29):
        slot_key = f"slot_{i:02d}"
        slot = universal.get(slot_key, {})
        action = slot.get("action", "")
        bars["bar6_alt"].append(action if action else "")
    
    # Bar 7 alt (slots 9-12): slots 29-32 in spec
    for i in range(29, 33):
        slot_key = f"slot_{i:02d}"
        slot = universal.get(slot_key, {})
        action = slot.get("action", "")
        bars["bar7_alt"].append(action if action else "")
    
    return bars

def clean_empty_trailing(spells):
    """Remove empty trailing entries."""
    while spells and spells[-1] == "":
        spells.pop()
    return spells

def format_lua_array(spells):
    """Format spell list as Lua array string."""
    if not spells or all(s == "" for s in spells):
        return "{}"
    cleaned = [f'"{s}"' if s else '""' for s in spells]
    return "{" + ", ".join(cleaned) + "}"

def main():
    print("=== Generating SpecRotations.lua (32 slots per spec) ===\n")
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    spec_files = sorted(SPECS_DIR.glob("*.json"))
    print(f"Found {len(spec_files)} spec files\n")
    
    lua_lines = [
        "-- Auto-generated spec rotation data for SkillWeaver",
        "-- 32 slots per spec:",
        "-- [1] = Bar 6 slots 1-8 (No mod, action 61-68)",
        "-- [2] = Bar 7 slots 1-8 (Shift, action 73-80)",
        "-- [3] = Bar 8 slots 1-8 (Ctrl, action 85-92)",
        "-- [4] = Bar 6 slots 9-12 (Alt, action 69-72)",
        "-- [5] = Bar 7 slots 9-12 (Shift+Alt, action 81-84)",
        "",
        "SkillWeaverRotations = {",
    ]
    
    for spec_file in spec_files:
        spec = load_spec(spec_file)
        spec_id = spec.get("spec_id")
        spec_name = spec.get("spec_name", "Unknown")
        bars = extract_spells(spec)
        
        if spec_id:
            bar6_main = format_lua_array(clean_empty_trailing(bars["bar6_main"]))
            bar7_main = format_lua_array(clean_empty_trailing(bars["bar7_main"]))
            bar8_main = format_lua_array(clean_empty_trailing(bars["bar8_main"]))
            bar6_alt = format_lua_array(clean_empty_trailing(bars["bar6_alt"]))
            bar7_alt = format_lua_array(clean_empty_trailing(bars["bar7_alt"]))
            
            lua_lines.append(f'    [{spec_id}] = {{ -- {spec_name}')
            lua_lines.append(f'        {bar6_main}, -- Bar 6 main (1-8)')
            lua_lines.append(f'        {bar7_main}, -- Bar 7 main (1-8)')
            lua_lines.append(f'        {bar8_main}, -- Bar 8 main (1-8)')
            lua_lines.append(f'        {bar6_alt}, -- Bar 6 alt (9-12)')
            lua_lines.append(f'        {bar7_alt}, -- Bar 7 alt (9-12)')
            lua_lines.append(f'    }},')
            
            total_spells = sum(len([s for s in b if s]) for b in bars.values())
            print(f"  {spec_id}: {spec_name} - {total_spells} spells")
    
    lua_lines.append("}")
    lua_lines.append("")
    
    with open(OUTPUT_FILE, 'w') as f:
        f.write("\n".join(lua_lines))
    
    print(f"\n=== Done! Written to {OUTPUT_FILE} ===")

if __name__ == "__main__":
    main()
