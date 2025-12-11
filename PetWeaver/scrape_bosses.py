
from scrape_wowhead_npcs import scrape_encounter_data, WowheadNPCScraper
import json

def main():
    targets = [
        "Unit 17",
        "Tiffany Nelson",
        "Environeer Bert", # Possible "Impossible Boss"?
        "Postmaster Malown",
        "Gorespine", # Already have, but good to check
        "Rocko"      # Already have
    ]
    
    results = {}
    
    for target in targets:
        print(f"--- Scraping {target} ---")
        data = scrape_encounter_data(target)
        if data:
            results[target] = data
            print(f"SUCCESS: Found {target} (NPC ID: {data['npc_id']})")
        else:
            print(f"FAILED: Could not find {target}")
            
    print("\n=== RESULTS ===")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
