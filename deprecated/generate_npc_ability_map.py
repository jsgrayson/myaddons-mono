# generate_npc_ability_map.py
"""
Generate a markdown file that, for each NPC (tamer), identifies the specific ability
that triggers the core mechanic described in `npc_strategies_crossref.md` and
lists the recommended player counter‑ability(ies).

Steps:
1. Load `encounters_full.json` – contains each NPC, its pets, and full ability objects.
2. Parse `npc_strategies_crossref.md` – each table row has:
   * Encounter (Tamer / ID)
   * Core Mechanic description
   * Counter‑Ability(s)
   We extract a mapping keyed by a normalized encounter name (lower‑case, without ID).
3. For each NPC from the JSON, locate the matching entry in the cross‑reference.
4. Determine which ability on the NPC’s pet(s) is responsible for the core mechanic.
   The heuristic is simple: if the ability name (case‑insensitive) appears in the
   core‑mechanic text, we treat it as the triggering ability.  For a few known
   cases where the name does not appear verbatim (e.g., Rocko’s "Damage Immunity"
   is implemented via the `Burrow` ability), we provide a small manual fallback
   dictionary.
5. Emit `npc_ability_counter_map.md` with a table per NPC:
   | NPC (ID) | Pet (Species ID) | Trigger Ability | Counter‑Ability(s) |
   The counter abilities are taken directly from the cross‑reference row.
"""
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
ENC_PATH = PROJECT_ROOT / "encounters_full.json"
CROSSREF_PATH = PROJECT_ROOT / "npc_strategies_crossref.md"
OUTPUT_MD = PROJECT_ROOT / "npc_ability_counter_map.md"

# Manual fall‑backs for cases where the ability name is not obvious in the description
MANUAL_MAP = {
    "rocko – needs a shave": "Burrow",  # Damage Immunity is achieved via Burrow (swap)
    "gorespine": "Gore",               # Core mechanic "Gore Stacks"
    "dah'da – wrathion": "Life Exchange",
    "the impossible boss": "Heal",    # Massive team healing ability
    "seeker zusshi": "Shell Shield",   # Core mechanic is Shell Shield
    "morulu the elder": "Feed",       # Large self‑heal
    "flowing pandaren spirit – tidal wave": "" ,  # Weather effect, no pet ability
    "burning pandaren spirit – scorched earth": "" ,
    "whispering pandaren spirit – call darkness": "" ,
    "thundering pandaren spirit – call lightning": "" ,
    "shadowlands – aura of undeath": "" ,
}

def load_encounters():
    with open(ENC_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def parse_crossref():
    """Return a dict mapping normalized encounter name -> (core_mechanic, counter_abilities)."""
    mapping = {}
    with open(CROSSREF_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) < 3:
                continue
            encounter_raw, core_mech, counter_raw = parts[0], parts[1], parts[2]
            # Clean encounter name: remove markdown ** and trailing ID in parentheses
            name = re.sub(r"\*\*", "", encounter_raw).strip()
            name = re.sub(r"\s*\(.*\)$", "", name).strip().lower()
            mapping[name] = (core_mech, counter_raw)
    return mapping

def find_trigger_ability(pet, core_mech, fallback_name):
    # Try to match ability name within core mechanic description
    for ability in pet.get("abilities", []):
        ability_name = ability.get("name", "").lower()
        if ability_name and ability_name in core_mech.lower():
            return ability.get("name")
    # If not found, use manual fallback if provided
    if fallback_name:
        return fallback_name
    return "?"

def generate_markdown(encounters, crossref_map):
    lines = ["# NPC Ability → Counter Ability Mapping\n\n"]
    for npc in encounters:
        npc_name = npc.get("name", "Unknown")
        npc_id = npc.get("npc_id")
        key = npc_name.lower()
        core_mech, counter = crossref_map.get(key, ("", "*No counter listed*"))
        lines.append(f"## {npc_name} (ID {npc_id})\n")
        lines.append(f"**Core mechanic:** {core_mech}\n")
        lines.append(f"**Recommended counter‑ability(s):** {counter}\n\n")
        lines.append("| Pet (Species ID) | Trigger Ability | Counter‑Ability(s) |\n|---|---|---|\n")
        for pet in npc.get("pets", []):
            species_id = pet.get("species_id")
            pet_label = f"Pet {species_id}"
            trigger = find_trigger_ability(pet, core_mech, MANUAL_MAP.get(key, ""))
            lines.append(f"| {pet_label} | {trigger} | {counter} |\n")
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
