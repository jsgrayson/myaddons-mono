#!/usr/bin/env python3
"""
scrape_talents.py - Scrapes talent export strings from Icy-Veins/Skill-Capped
and updates spec JSON files.

Usage: python3 scrape_talents.py
"""

import os
import json
import requests
from bs4 import BeautifulSoup

SPECS_DIR = os.path.join(os.path.dirname(__file__), "..", "Brain", "data", "specs")

# Spec mapping: spec_id -> (class, spec_name, icy_veins_slug)
SPECS = {
    # Rogue
    41: ("rogue", "assassination", "assassination-rogue"),
    42: ("rogue", "outlaw", "outlaw-rogue"),
    43: ("rogue", "subtlety", "subtlety-rogue"),
    # Death Knight
    61: ("death-knight", "blood", "blood-death-knight"),
    62: ("death-knight", "frost", "frost-death-knight"),
    63: ("death-knight", "unholy", "unholy-death-knight"),
    # Demon Hunter
    121: ("demon-hunter", "havoc", "havoc-demon-hunter"),
    122: ("demon-hunter", "vengeance", "vengeance-demon-hunter"),
    # Druid
    102: ("druid", "balance", "balance-druid"),
    103: ("druid", "feral", "feral-druid"),
    104: ("druid", "guardian", "guardian-druid"),
    105: ("druid", "restoration", "restoration-druid"),
    # Hunter
    31: ("hunter", "beast-mastery", "beast-mastery-hunter"),
    32: ("hunter", "marksmanship", "marksmanship-hunter"),
    33: ("hunter", "survival", "survival-hunter"),
    # Mage
    62: ("mage", "arcane", "arcane-mage"),
    63: ("mage", "fire", "fire-mage"),
    64: ("mage", "frost", "frost-mage"),
    # Monk
    101: ("monk", "brewmaster", "brewmaster-monk"),
    102: ("monk", "mistweaver", "mistweaver-monk"),
    103: ("monk", "windwalker", "windwalker-monk"),
    # Paladin
    65: ("paladin", "holy", "holy-paladin"),
    66: ("paladin", "protection", "protection-paladin"),
    70: ("paladin", "retribution", "retribution-paladin"),
    # Priest
    51: ("priest", "discipline", "discipline-priest"),
    52: ("priest", "holy", "holy-priest"),
    53: ("priest", "shadow", "shadow-priest"),
    # Shaman
    71: ("shaman", "elemental", "elemental-shaman"),
    72: ("shaman", "enhancement", "enhancement-shaman"),
    73: ("shaman", "restoration", "restoration-shaman"),
    # Warlock
    91: ("warlock", "affliction", "affliction-warlock"),
    92: ("warlock", "demonology", "demonology-warlock"),
    93: ("warlock", "destruction", "destruction-warlock"),
    # Warrior
    71: ("warrior", "arms", "arms-warrior"),
    72: ("warrior", "fury", "fury-warrior"),
    73: ("warrior", "protection", "protection-warrior"),
    # Evoker
    131: ("evoker", "devastation", "devastation-evoker"),
    132: ("evoker", "preservation", "preservation-evoker"),
    133: ("evoker", "augmentation", "augmentation-evoker"),
}

# Known talent strings (manually gathered from web searches)
# Format: spec_id -> {content_type: export_string}
KNOWN_TALENTS = {
    41: {  # Assassination Rogue
        "mythic": "CMQAA0tw2gAD7pPTLoW5IGZDewMjZmxMz2MAAAAAAMbzY2mBAAAAAgW2GGwYYmZZMYmxMjZmZMzYbbbMDD2mZbsxYGzSjZZbYy2wwyA",
        "raid": "CMQAA0tw2gAD7pPTLoW5IGZDeYMjZmxMjZAAAAAAYWmxsNDAAAAAAtsNMDMYmZWGDmZMzMzMzYG222GzwgtZWGbMmxs0YW2GmsNMsMA",
        "delve": "CMQAA0tw2gAD7pPTLoW5IGZDewMjZmxMz2MAAAAAAMbzY2mBAAAAAgW2GGwYYmZZMYmxMjZmZMzYbbbMDD2mZbsxYGzSjZZbYy2wwyA",
        "pvp": "CMQAA0tw2gAD7pPTLoW5IGZDeYMjZmxMDAAAAAAY2mxsNDAAAAAAtsMMDzMGzMzyYwMjZmZmZGzwy22YwgNzyADYJYZYCMsMA",
    },
}


def update_spec_file(spec_id: int, talent_loadouts: dict):
    """Update a spec JSON file with talent loadouts."""
    # Find the spec file
    for filename in os.listdir(SPECS_DIR):
        if filename.startswith(f"{spec_id}_") and filename.endswith('.json'):
            filepath = os.path.join(SPECS_DIR, filename)
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            data['talent_loadouts'] = talent_loadouts
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            
            print(f"[+] Updated {filename}")
            return True
    
    print(f"[-] Spec file not found for spec_id {spec_id}")
    return False


def main():
    print("SkillWeaver Talent Updater")
    print("=" * 40)
    
    for spec_id, talents in KNOWN_TALENTS.items():
        update_spec_file(spec_id, talents)
    
    print("\n[!] To add more specs, update KNOWN_TALENTS dict with export strings")
    print("[!] Get strings from:")
    print("    - PvE: https://www.icy-veins.com/wow/CLASS-SPEC-dps-guide")
    print("    - PvP: https://www.skill-capped.com/wow/")


if __name__ == "__main__":
    main()
