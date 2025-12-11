# extract_multi_scripts.py
"""Expand Xu‑Fu strategies to a full team‑script list.

The original scraper (scrape_xufu_enhanced.py) stores one script per
encounter together with all pet‑alternative slots. This helper reads that
JSON and creates a new file `expanded_team_scripts.json` where each
possible team (cartesian product of the alternative slots) is paired with
the single script for the encounter.

Result format:
{
  "Encounter Name": [
    {"team": [pet_id, pet_id, pet_id], "script": "..."},
    ...
  ],
  ...
}
"""
import json
from itertools import product
from pathlib import Path

# Load the enhanced strategies produced by the original scraper
SOURCE_FILE = Path("strategies_enhanced.json")
OUTPUT_FILE = Path("expanded_team_scripts.json")

if not SOURCE_FILE.is_file():
    raise FileNotFoundError(f"{SOURCE_FILE} not found – run the scraper first.")

with SOURCE_FILE.open() as f:
    data = json.load(f)

expanded = {}

# The JSON hierarchy is: expansion -> category -> list of encounters
for expansion, categories in data.items():
    for cat_name, encounters in categories.items():
        for enc in encounters:
            name = enc.get("encounter_name", "unknown")
            script = enc.get("script", "")
            # each slot is a list of pet dicts; we only need the pet id
            slots = [[p["id"] for p in slot if p.get("id")] for slot in enc.get("pet_slots", [])]
            # generate every combination (cartesian product) of one pet per slot
            combos = list(product(*slots)) if slots else []
            expanded[name] = [
                {"team": list(combo), "script": script}
                for combo in combos
            ]

OUTPUT_FILE.write_text(json.dumps(expanded, indent=2))
print(f"✅ Expanded data written to {OUTPUT_FILE}")
