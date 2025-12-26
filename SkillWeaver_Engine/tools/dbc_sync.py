#!/usr/bin/env python3
"""
dbc_sync.py - Auto-Populate Spec Files from WoW SavedVariables

This tool syncs your in-game keybinds directly into the spec JSON files,
eliminating manual entry for all 40 specs.

Usage:
    python3 dbc_sync.py /path/to/SkillWeaver.lua

Requirements:
    - SkillWeaver addon must export spellbook data to SavedVariables
    - Run after logging in on each character to capture their bindings
"""

import json
import re
import os
import sys
import glob


def parse_lua_keybinds(lua_content: str) -> dict:
    """
    Parse Lua SavedVariables format to extract action -> keybind mappings.
    
    Expected format in SkillWeaver.lua:
        SkillWeaverDB = {
            ["spellbook"] = {
                ["Mutilate"] = "F15",
                ["Envenom"] = "F16",
                ...
            }
        }
    """
    keybinds = {}
    
    # Pattern: ["Action Name"] = "Keybind"
    pattern = r'\["([^"]+)"\]\s*=\s*"([^"]+)"'
    
    for match in re.finditer(pattern, lua_content):
        action = match.group(1)
        keybind = match.group(2)
        # Only capture F-key style bindings
        if re.match(r'^(Shift\+|Ctrl\+|Alt\+)?F\d+$', keybind, re.IGNORECASE):
            keybinds[action] = keybind
            
    return keybinds


def sync_spec_file(json_path: str, keybinds: dict, dry_run: bool = False) -> int:
    """
    Update a spec JSON file with discovered keybinds.
    Returns the number of slots updated.
    """
    try:
        with open(json_path, 'r') as f:
            spec = json.load(f)
    except Exception as e:
        print(f"  [ERROR] Failed to read {json_path}: {e}")
        return 0
    
    updated = 0
    slots = spec.get('universal_slots', {})
    
    for slot_id, data in slots.items():
        action = data.get('action', '')
        
        # Try exact match first
        if action in keybinds:
            old_key = data.get('key', 'UNSET')
            new_key = keybinds[action]
            if old_key != new_key:
                print(f"  {slot_id}: {action} | {old_key} → {new_key}")
                data['key'] = new_key
                updated += 1
        else:
            # Try partial match for combined actions like "Mutilate / Ambush"
            for ingame_action, keybind in keybinds.items():
                if ingame_action in action or action in ingame_action:
                    old_key = data.get('key', 'UNSET')
                    if old_key != keybind:
                        print(f"  {slot_id}: {action} (matched '{ingame_action}') | {old_key} → {keybind}")
                        data['key'] = keybind
                        updated += 1
                    break
    
    if updated > 0 and not dry_run:
        with open(json_path, 'w') as f:
            json.dump(spec, f, indent=4)
    
    return updated


def sync_all_specs(specs_dir: str, keybinds: dict, dry_run: bool = False):
    """Sync all spec JSON files in the directory."""
    pattern = os.path.join(specs_dir, "*.json")
    spec_files = glob.glob(pattern)
    
    total_updated = 0
    
    for spec_file in sorted(spec_files):
        filename = os.path.basename(spec_file)
        print(f"\n[SYNC] {filename}")
        updated = sync_spec_file(spec_file, keybinds, dry_run)
        total_updated += updated
        
        if updated == 0:
            print("  (no changes)")
    
    return total_updated


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 dbc_sync.py /path/to/SkillWeaver.lua [--dry-run]")
        print("\nExample paths:")
        print("  macOS: /Applications/World of Warcraft/_retail_/WTF/Account/USERNAME/SavedVariables/SkillWeaver.lua")
        print("  Windows: C:/Program Files/World of Warcraft/_retail_/WTF/Account/USERNAME/SavedVariables/SkillWeaver.lua")
        sys.exit(1)
    
    lua_path = sys.argv[1]
    dry_run = '--dry-run' in sys.argv
    
    if not os.path.exists(lua_path):
        print(f"[ERROR] SavedVariables file not found: {lua_path}")
        sys.exit(1)
    
    # Read Lua file
    print(f"[LOAD] Reading {lua_path}")
    with open(lua_path, 'r') as f:
        lua_content = f.read()
    
    # Parse keybinds
    keybinds = parse_lua_keybinds(lua_content)
    print(f"[FOUND] {len(keybinds)} keybind mappings")
    
    if not keybinds:
        print("[WARN] No keybinds found. Ensure your addon exports to SavedVariables.")
        sys.exit(1)
    
    # Get specs directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    specs_dir = os.path.join(script_dir, "..", "Brain", "data", "specs")
    
    if not os.path.exists(specs_dir):
        # Try alternate path
        specs_dir = os.path.join(script_dir, "Brain", "data", "specs")
    
    if not os.path.exists(specs_dir):
        print(f"[ERROR] Specs directory not found. Expected: {specs_dir}")
        sys.exit(1)
    
    if dry_run:
        print("\n[DRY RUN] No files will be modified\n")
    
    # Sync all specs
    total = sync_all_specs(specs_dir, keybinds, dry_run)
    
    print(f"\n[DONE] Updated {total} slots across all specs")
    if dry_run:
        print("[DRY RUN] Run without --dry-run to apply changes")


if __name__ == "__main__":
    main()
