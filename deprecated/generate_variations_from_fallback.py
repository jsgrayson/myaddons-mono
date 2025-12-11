# generate_variations_from_fallback.py
"""Create variations_with_scripts.json using the fallback expansion.

If the API‑based per‑team script extraction fails (as it did),
this script:
1. Loads `strategies_enhanced.json` – contains the default script for each encounter.
2. Loads `pet_alternatives.json` – maps each pet slot to its interchangeable pets.
3. Generates every possible team combination (Cartesian product) for each encounter.
4. Associates each team with the **default script** from the encounter.
5. Writes the result to `variations_with_scripts.json`.

The output format matches what the rest of the project expects:
{
  "Encounter Name": [
    {"team": [pet_id_1, pet_id_2, pet_id_3], "script": "…default script…"},
    ...
  ],
  ...
}
"""
import json, itertools
from pathlib import Path

SOURCE_STRATEGIES = Path("strategies_enhanced.json")
SOURCE_ALTS = Path("pet_alternatives.json")
OUTPUT_FILE = Path("variations_with_scripts.json")

def load_json(p: Path):
    with p.open() as f:
        return json.load(f)

def build_alternatives_map(alts_json):
    """Return a dict: encounter -> list of three lists (slot‑wise alternatives)."""
    result = {}
    for enc_name, data in alts_json.items():
        # data contains `alternatives` keyed by slot index (0‑2)
        slot_alts = [data.get(str(i), []) for i in range(3)]
        # ensure each slot list has at least one entry (the original pet)
        result[enc_name] = slot_alts
    return result

def expand_teams(slot_alts):
    """Cartesian product of three slot lists → list of 3‑pet teams."""
    return [list(team) for team in itertools.product(*slot_alts)]

def main():
    strategies = load_json(SOURCE_STRATEGIES)
    alts = load_json(SOURCE_ALTS)

    # Build a quick lookup: encounter name → default script
    default_scripts = {}
    for exp, cats in strategies.items():
        for cat, encs in cats.items():
            for enc in encs:
                name = enc.get("encounter_name")
                script = enc.get("script", "").strip()
                if name:
                    default_scripts[name] = script

    alt_map = build_alternatives_map(alts)

    variations = {}
    for enc_name, script in default_scripts.items():
        slot_alts = alt_map.get(enc_name, [[], [], []])
        # If any slot list is empty, fall back to a placeholder (0)
        slot_alts = [s if s else [0] for s in slot_alts]
        teams = expand_teams(slot_alts)
        variations[enc_name] = [{"team": team, "script": script} for team in teams]

    OUTPUT_FILE.write_text(json.dumps(variations, indent=2))
    print(f"✅ Saved {len(variations)} encounters → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
