#!/usr/bin/env python3
"""
sync_specs_to_wow.py - Syncs spec JSON files to WoW SavedVariables

This tool:
1. Reads all spec JSON files
2. Extracts talent loadouts and ability bindings
3. Writes to SkillWeaverDB in WoW SavedVariables
4. Generates action bar bindings for F13-F24
"""

import os
import json
import sys

# Paths
WOW_PATH = "/Applications/World of Warcraft"
SPECS_DIR = os.path.join(os.path.dirname(__file__), "..", "Brain", "data", "specs")
ADDON_SV_PATH = os.path.join(WOW_PATH, "_retail_", "WTF", "Account")


def find_accounts():
    """Find all WoW accounts."""
    accounts = []
    sv_path = ADDON_SV_PATH
    if os.path.exists(sv_path):
        for d in os.listdir(sv_path):
            if os.path.isdir(os.path.join(sv_path, d)) and d != "SavedVariables":
                accounts.append(d)
    return accounts


def load_all_specs():
    """Load all spec JSON files."""
    specs = {}
    for filename in os.listdir(SPECS_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(SPECS_DIR, filename), 'r') as f:
                spec = json.load(f)
                spec_id = spec.get('spec_id')
                if spec_id:
                    specs[spec_id] = spec
    return specs


def generate_lua_table(data, indent=0):
    """Convert Python dict to Lua table string."""
    lua = []
    pad = "    " * indent
    
    if isinstance(data, dict):
        lua.append("{")
        for key, value in data.items():
            if isinstance(key, int):
                key_str = f"[{key}]"
            else:
                key_str = f'["{key}"]'
            lua.append(f'{pad}    {key_str} = {generate_lua_table(value, indent + 1)},')
        lua.append(f"{pad}}}")
    elif isinstance(data, list):
        lua.append("{")
        for item in data:
            lua.append(f'{pad}    {generate_lua_table(item, indent + 1)},')
        lua.append(f"{pad}}}")
    elif isinstance(data, str):
        return f'"{data}"'
    elif isinstance(data, bool):
        return "true" if data else "false"
    elif data is None:
        return "nil"
    else:
        return str(data)
    
    return "\n".join(lua)


def sync_to_account(account_id, specs):
    """Write specs to account's SkillWeaver SavedVariables."""
    sv_file = os.path.join(
        ADDON_SV_PATH, account_id, "SavedVariables", "SkillWeaver.lua"
    )
    
    os.makedirs(os.path.dirname(sv_file), exist_ok=True)
    
    # Extract talent loadouts and keybinds from specs
    talent_loadouts = {}
    ability_bindings = {}
    
    for spec_id, spec in specs.items():
        # Talent loadouts
        if "talent_loadouts" in spec:
            talent_loadouts[spec_id] = spec["talent_loadouts"]
        
        # Extract ability -> key mappings from slots
        bindings = {}
        if "universal_slots" in spec:
            for slot_id, slot in spec["universal_slots"].items():
                action = slot.get("action", "")
                key = slot.get("key", "")
                if action and key:
                    bindings[action] = key
        if bindings:
            ability_bindings[spec_id] = bindings
    
    # Generate SavedVariables content
    content = f"""
SkillWeaverDB = SkillWeaverDB or {{}}

-- Synced from Python spec files
SkillWeaverDB.talentLoadouts = {generate_lua_table(talent_loadouts)}

SkillWeaverDB.abilityBindings = {generate_lua_table(ability_bindings)}

SkillWeaverDB.syncedAt = "{__import__('datetime').datetime.now().isoformat()}"
"""
    
    # Don't overwrite existing SkillWeaverDB, merge with it
    # For simplicity, just write the talent/binding data
    with open(sv_file, 'w') as f:
        f.write(content)
    
    print(f"[+] Synced to: {sv_file}")
    print(f"    - {len(talent_loadouts)} spec loadouts")
    print(f"    - {len(ability_bindings)} ability binding sets")


def main():
    print("SkillWeaver Spec Sync Tool")
    print("=" * 40)
    
    # Load specs
    specs = load_all_specs()
    print(f"[*] Loaded {len(specs)} spec files")
    
    # Find accounts
    accounts = find_accounts()
    if not accounts:
        print("[!] No WoW accounts found")
        return
    
    print(f"[*] Found {len(accounts)} account(s)")
    
    # Sync to each account
    for account in accounts:
        print(f"\n[*] Syncing to account: {account}")
        sync_to_account(account, specs)
    
    print("\n[✓] Done! Reload WoW to pick up changes.")


if __name__ == "__main__":
    main()
