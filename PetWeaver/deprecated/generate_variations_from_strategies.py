# generate_variations_from_strategies.py
"""Generate variations_with_scripts.json using only the data in strategies_enhanced.json.

For each encounter we have:
- "strategies" list, containing objects with:
    - "script" – the default script.
    - "pet_slots" – a list of slot arrays.

We compute the Cartesian product of the pet IDs for the three slots, producing every
possible team composition. Each team is paired with the script from that strategy.

The output format matches what the rest of the project expects:
{
  "Encounter Name": [
    {"team": [id1, id2, id3], "script": "..."},
    ...
  ],
  ...
}
"""
import json, itertools
from pathlib import Path

SOURCE = Path("strategies_enhanced.json")
OUTPUT = Path("variations_with_scripts.json")

def load_strategies():
    with SOURCE.open() as f:
        return json.load(f)

def extract_encounters(data):
    """Yield (encounter_name, script, list_of_slot_lists)"""
    for exp, cats in data.items():
        for cat, encs in cats.items():
            for enc in encs:
                name = enc.get("encounter_name")
                strategies = enc.get("strategies", [])
                
                # Iterate through all strategies found for this encounter
                for strat in strategies:
                    script = strat.get("script", "").strip()
                    pet_slots = strat.get("pet_slots", [])
                    
                    # Convert each slot to a list of pet IDs (including alternatives)
                    slot_ids = []
                    for slot in pet_slots:
                        # Extract IDs, defaulting to 0 if missing
                        ids = [pet.get("id", 0) for pet in slot]
                        # Ensure at least one ID (fallback to 0)
                        if not ids:
                            ids = [0]
                        slot_ids.append(ids)
                    
                    # Ensure we have exactly 3 slots for the product (pad if needed)
                    while len(slot_ids) < 3:
                        slot_ids.append([0])
                    slot_ids = slot_ids[:3]

                    if name:
                        yield name, script, slot_ids

def generate_variations():
    data = load_strategies()
    result = {}
    
    count = 0
    for name, script, slot_ids in extract_encounters(data):
        # If any slot list is empty, skip (should not happen due to padding)
        if not slot_ids:
            continue
            
        # Cartesian product of the slot ID lists
        teams = [list(t) for t in itertools.product(*slot_ids)]
        
        # Create variations
        new_variations = [{"team": team, "script": script} for team in teams]
        
        if name in result:
            result[name].extend(new_variations)
        else:
            result[name] = new_variations
            
        count += 1

    return result

def main():
    if not SOURCE.exists():
        print(f"❌ Source file {SOURCE} not found.")
        return

    variations = generate_variations()
    OUTPUT.write_text(json.dumps(variations, indent=2))
    print(f"✅ Saved variations for {len(variations)} encounters to {OUTPUT}")

if __name__ == "__main__":
    main()
