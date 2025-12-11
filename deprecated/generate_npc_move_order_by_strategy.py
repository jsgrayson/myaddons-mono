# generate_npc_move_order_by_strategy.py
"""
Generate a markdown file that, for each NPC (tamer), lists the *exact* ability
sequence the NPC will use, derived from the core‑mechanic description in
`npc_strategies_crossref.md`, the pet ability data in `encounters_full.json`,
**and ability cooldowns**.

Approach:
1. Load `encounters_full.json` – each pet entry contains a list of abilities
   with fields such as `name`, `priority`, `speed`, `cooldown` (in rounds) and
   `rounds` (duration of the ability effect).
2. Parse `npc_strategies_crossref.md`. Each row has:
   * Encounter (tamer name / ID)
   * Core mechanic description – often mentions a duration (e.g. "for 10
     rounds")
   * Counter‑ability(s)
3. For each NPC we locate the *trigger ability* that produces the core mechanic.
   - If the ability name appears in the mechanic text we use it.
   - A small manual fallback dictionary handles cases where the name is not
     obvious (Rocko → Burrow, Gorespine → Gore, etc.).
4. Extract a duration (number of rounds) from the mechanic text using a regex.
   If no explicit duration is found we assume the ability is used once.
5. **Simulate rounds** (up to `MAX_ROUNDS = 12`) for each pet:
   * If we are still within the trigger‑ability duration, use that ability.
   * Otherwise, among abilities whose cooldown counter is 0, pick the one with
     highest priority, then highest effective speed (`pet.speed + ability.speed`).
   * After using an ability, set its cooldown counter to the ability's
     `cooldown` value (default 0).  At the end of each round, decrement all
     non‑zero cooldown counters.
6. Build a markdown table per NPC showing round, pet, and chosen ability.
7. Write `npc_move_order_by_strategy.md`.
"""
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
ENC_PATH = PROJECT_ROOT / "encounters_full.json"
CROSSREF_PATH = PROJECT_ROOT / "npc_strategies_crossref.md"
OUTPUT_MD = PROJECT_ROOT / "npc_move_order_by_strategy.md"

MAX_ROUNDS = 12

# Manual fall‑backs for abilities that are not named verbatim in the description
MANUAL_MAP = {
    "rocko – needs a shave": "Burrow",
    "gorespine": "Gore",
    "dah'da – wrathion": "Life Exchange",
    "the impossible boss": "Heal",
    "seeker zusshi": "Shell Shield",
    "morulu the elder": "Feed",
    "flowing pandaren spirit – tidal wave": "",  # weather effect, no pet ability
    "burning pandaren spirit – scorched earth": "",
    "whispering pandaren spirit – call darkness": "",
    "thundering pandaren spirit – call lightning": "",
    "shadowlands – aura of undeath": "",
}

def load_encounters():
    with open(ENC_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def parse_crossref():
    """Return dict: normalized encounter name -> (core_mechanic, counter_abilities)."""
    mapping = {}
    with open(CROSSREF_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.startswith("|"):
                continue
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) < 3:
                continue
            encounter_raw, core_mech, counter_raw = parts[0], parts[1], parts[2]
            # Clean name: remove markdown ** and trailing (ID)
            name = re.sub(r"\*\*", "", encounter_raw).strip()
            name = re.sub(r"\s*\(.*\)$", "", name).strip().lower()
            mapping[name] = (core_mech, counter_raw)
    return mapping

def find_trigger_ability(pet, core_mech, fallback):
    # Try to match ability name inside the core mechanic text
    for ability in pet.get("abilities", []):
        ability_name = ability.get("name", "").lower()
        if ability_name and ability_name in core_mech.lower():
            return ability.get("name")
    # Manual fallback if provided
    if fallback:
        return fallback
    return None

def extract_duration(core_mech):
    # Look for patterns like "for 10 rounds", "10‑round", "10 round", "10‑turn"
    match = re.search(r"(\d+)\s*[-‑]?\s*round", core_mech, re.IGNORECASE)
    if not match:
        match = re.search(r"for\s+(\d+)\s+rounds?", core_mech, re.IGNORECASE)
    if not match:
        match = re.search(r"(\d+)\s*[-‑]?\s*turn", core_mech, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 1

def ability_sort_key(pet, ability):
    prio = ability.get("priority", 0)
    if ability.get("name", "").lower() == "swap":
        prio = 9999
    spd = pet.get("speed", 0) + ability.get("speed", 0)
    return (-prio, -spd)

def simulate_pet_rounds(pet, trigger_ability_name, trigger_duration):
    """Return a list of ability names for each round (up to MAX_ROUNDS).
    Cooldowns are respected.  Abilities without a `cooldown` field are assumed to be
    usable every round.
    """
    abilities = pet.get("abilities", [])
    # Build a lookup by name for quick access
    ability_by_name = {ab.get("name"): ab for ab in abilities}
    # Initialize cooldown counters (name -> rounds left)
    cooldowns = {ab.get("name"): 0 for ab in abilities}
    result = []
    round_num = 1
    while round_num <= MAX_ROUNDS:
        # 1️⃣ If we are still in the trigger ability duration, use it
        if trigger_ability_name and trigger_duration > 0:
            result.append(trigger_ability_name)
            # Decrement trigger duration for next round
            trigger_duration -= 1
            # Apply cooldown if the trigger ability has one
            trig_ab = ability_by_name.get(trigger_ability_name)
            if trig_ab:
                cd = trig_ab.get("cooldown", 0)
                cooldowns[trigger_ability_name] = cd
        else:
            # 2️⃣ Choose the best off‑cooldown ability
            # Filter abilities whose cooldown counter is 0
            available = [ab for ab in abilities if cooldowns.get(ab.get("name"), 0) == 0]
            if not available:
                # All abilities on cooldown – wait a turn (no action)
                result.append("—")
            else:
                # Pick highest priority then speed
                available.sort(key=lambda ab: ability_sort_key(pet, ab))
                chosen = available[0]
                chosen_name = chosen.get("name")
                result.append(chosen_name)
                # Set its cooldown
                cd = chosen.get("cooldown", 0)
                cooldowns[chosen_name] = cd
        # 3️⃣ Decrement all cooldown counters (except those already at 0)
        for name in list(cooldowns.keys()):
            if cooldowns[name] > 0:
                cooldowns[name] -= 1
        round_num += 1
    return result

def generate_markdown(encounters, crossref_map):
    lines = ["# NPC Move‑Order Determined from Strategies (Cooldown‑Aware)\n\n"]
    for npc in encounters:
        npc_name = npc.get("name", "Unknown")
        npc_id = npc.get("npc_id")
        key = npc_name.lower()
        core_mech, _ = crossref_map.get(key, ("", ""))
        lines.append(f"## {npc_name} (ID {npc_id})\n")
        lines.append(f"**Core mechanic:** {core_mech}\n\n")
        lines.append("| Round | Pet (Species ID) | Ability |\n|------|------------------|--------|\n")
        # Determine trigger ability and its duration for each pet
        for pet in npc.get("pets", []):
            species_id = pet.get("species_id")
            pet_label = f"Pet {species_id}"
            trigger = find_trigger_ability(pet, core_mech, MANUAL_MAP.get(key, ""))
            duration = extract_duration(core_mech) if trigger else 0
            # Simulate rounds for this pet
            ability_sequence = simulate_pet_rounds(pet, trigger, duration)
            for rnd, ability_name in enumerate(ability_sequence, start=1):
                lines.append(f"| {rnd} | {pet_label} | {ability_name} |\n")
        lines.append("\n")
    return "".join(lines)

def main():
    encounters = load_encounters()
    crossref_map = parse_crossref()
    md = generate_markdown(encounters, crossref_map)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"✅ Generated {OUTPUT_MD} with cooldown‑aware move order for {len(encounters)} NPCs.")

if __name__ == "__main__":
    main()
