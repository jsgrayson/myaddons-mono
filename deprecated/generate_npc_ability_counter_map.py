# generate_npc_ability_counter_map.py
"""
Generate a markdown file that, for every NPC (tamer), lists each of its pet abilities
and the recommended player counter‑ability(ies) based on the PC‑strategies table
(`npc_strategies_crossref.md`).

Steps:
1. Load `encounters_full.json` – contains all NPCs, their pets, and each pet's
   ability objects (name, id, etc.).
2. Parse `npc_strategies_crossref.md` – the markdown table where each row has:
   * Encounter (Tamer / ID)
   * Core Mechanic
   * Counter‑Ability(s)
   We extract a mapping from the encounter identifier (e.g., "Rocko – Needs a Shave")
   to the list of counter abilities.
3. For each NPC in the encounters JSON, we look up its name/ID in the mapping.
   If found, we emit a section with a table:
   | Pet (Species ID) | Ability | Counter‑Ability(s) |
   The Counter‑Ability column repeats the list from the cross‑reference.
4. Write the markdown to `npc_ability_counter_map.md`.

The script is deterministic and can be re‑run whenever the JSON or the
cross‑reference is updated.
"""
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
ENC_PATH = PROJECT_ROOT / "encounters_full.json"
CROSSREF_PATH = PROJECT_ROOT / "npc_strategies_crossref.md"
OUTPUT_MD = PROJECT_ROOT / "npc_ability_counter_map.md"

def load_encounters():
    with open(ENC_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def parse_crossref():
    """Return a dict mapping a normalized encounter name to its counter abilities.
    The markdown table rows look like:
    | **Rocko – Needs a Shave** (98572) | Damage Immunity … | **Dodge**, **Burrow**, **Heal**, … |
    We'll extract the text before the first '(' as the key.
    """
    mapping = {}
    with open(CROSSREF_PATH, "r", encoding="utf-8") as f:
        for line in f:
            # Only process table rows that start with a pipe
            if not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) < 3:
                continue
            encounter_raw = parts[0]
            counter_raw = parts[2]
            # Clean encounter name – remove markdown ** and trailing ID
            encounter_name = re.sub(r"\*\*", "", encounter_raw).strip()
            # Remove the ID in parentheses
            encounter_name = re.sub(r"\s*\(.*\)$", "", encounter_name).strip()
            # Counter abilities – keep as‑is (comma‑separated list)
            counter_abilities = counter_raw
            mapping[encounter_name.lower()] = counter_abilities
    return mapping

def generate_markdown(encounters, crossref_map):
    lines = ["# NPC Ability → Counter‑Ability Mapping\n\n"]
    for npc in encounters:
        name = npc.get("name", "Unknown")
        npc_id = npc.get("npc_id")
        key = f"{name}".lower()
        counter = crossref_map.get(key, "*No specific counter listed*")
        lines.append(f"## {name} (ID {npc_id})\n")
        lines.append(f"**Recommended Counter‑Ability(s):** {counter}\n\n")
        lines.append("| Pet (Species ID) | Ability | Counter‑Ability(s) |\n|---|---|---|\n")
        for pet in npc.get("pets", []):
            species_id = pet.get("species_id")
            pet_label = f"Pet {species_id}"
            for ability in pet.get("abilities", []):
                ability_name = ability.get("name", "?")
                lines.append(f"| {pet_label} | {ability_name} | {counter} |\n")
        lines.append("\n")
    return "".join(lines)

def main():
    encounters = load_encounters()
    crossref_map = parse_crossref()
    md = generate_markdown(encounters, crossref_map)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ Generated {OUTPUT_MD} with ability → counter mapping for {len(encounters)} NPCs.")

if __name__ == "__main__":
    main()
