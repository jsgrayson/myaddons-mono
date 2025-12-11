#!/usr/bin/env python3
"""
Batch Encounter Scraper for The Codex
Scrapes all TWW raids and dungeons from Icy Veins
"""

import sys
import json
import time
sys.path.append('/Users/jgrayson/Documents/holocron/scrapers')
from icy_veins import IcyVeinsScraper

# TWW Encounter Definitions
ENCOUNTERS = {
    "raids": {
        "Nerub-ar Palace": {
            "slug": "nerub-ar-palace",
            "bosses": [
                {"name": "Ulgrax the Devourer", "slug": "ulgrax-the-devourer"},
                {"name": "The Bloodbound Horror", "slug": "the-bloodbound-horror"},
                {"name": "Sikran", "slug": "sikran-captain-of-the-sureki"},
                {"name": "Rasha'nan", "slug": "rashanan"},
                {"name": "Broodtwister Ovi'nax", "slug": "broodtwister-ovinax"},
                {"name": "Nexus-Princess Ky'veza", "slug": "nexus-princess-kyveza"},
                {"name": "The Silken Court", "slug": "the-silken-court"},
                {"name": "Queen Ansurek", "slug": "queen-ansurek"}
            ]
        }
    },
    "dungeons": {
        "Ara-Kara, City of Echoes": {
            "slug": "ara-kara",
            "bosses": [
                {"name": "Avanoxx", "slug": "avanoxx"},
                {"name": "Anub'zekt", "slug": "anubzekt"},
                {"name": "Ki'katal the Harvester", "slug": "kikatal-the-harvester"}
            ]
        },
        "City of Threads": {
            "slug": "city-of-threads",
            "bosses": [
                {"name": "Orator Krix'vizk", "slug": "orator-krixvizk"},
                {"name": "Fangs of the Queen", "slug": "fangs-of-the-queen"},
                {"name": "The Coaglamation", "slug": "the-coaglamation"},
                {"name": "Izo, the Grand Splicer", "slug": "izo-the-grand-splicer"}
            ]
        },
        "The Stonevault": {
            "slug": "the-stonevault",
            "bosses": [
                {"name": "E.D.N.A", "slug": "edna"},
                {"name": "Skarmorak", "slug": "skarmorak"},
                {"name": "Master Machinists", "slug": "master-machinists"},
                {"name": "Void Speaker Eirich", "slug": "void-speaker-eirich"}
            ]
        },
        "The Dawnbreaker": {
            "slug": "the-dawnbreaker",
            "bosses": [
                {"name": "Speaker Shadowcrown", "slug": "speaker-shadowcrown"},
                {"name": "Anub'ikkaj", "slug": "anubikkaj"},
                {"name": "Rasha'nan", "slug": "rashanan"}
            ]
        }
    }
}

def scrape_all_encounters():
    """Scrape all encounters and save to JSON"""
    scraper = IcyVeinsScraper("warrior", "arms")  # Class/spec don't matter
    results = {"raids": {}, "dungeons": {}}
    
    total_encounters = sum(len(instance["bosses"]) for instances in ENCOUNTERS.values() for instance in instances.values())
    current = 0
    
    print(f"Starting batch scrape of {total_encounters} encounters...")
    
    for category in ["raids", "dungeons"]:
        for instance_name, instance_data in ENCOUNTERS[category].items():
            print(f"\n{'='*60}")
            print(f"Instance: {instance_name} ({category.upper()})")
            print(f"{'='*60}")
            
            results[category][instance_name] = {
                "bosses": [],
                "slug": instance_data["slug"]
            }
            
            for boss in instance_data["bosses"]:
                current += 1
                print(f"\n[{current}/{total_encounters}] Scraping {boss['name']}...")
                
                try:
                    encounter_data = scraper.fetch_encounter(
                        instance_data["slug"],
                        boss["slug"]
                    )
                    
                    # Add metadata
                    encounter_data["display_name"] = boss["name"]
                    encounter_data["instance"] = instance_name
                    encounter_data["category"] = category
                    
                    results[category][instance_name]["bosses"].append(encounter_data)
                    
                    print(f"  ✓ Success! Found {len(encounter_data.get('abilities', []))} abilities")
                    
                except Exception as e:
                    print(f"  ✗ Error: {e}")
                    results[category][instance_name]["bosses"].append({
                        "error": str(e),
                        "display_name": boss["name"],
                        "boss": boss["slug"]
                    })
                
                # Rate limiting
                time.sleep(1)
    
    # Save to JSON
    output_file = "/Users/jgrayson/Documents/holocron/data/encounters.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"✓ Scraping complete! Saved to {output_file}")
    print(f"{'='*60}")
    
    # Print summary
    total_success = sum(
        1 for category in results.values()
        for instance in category.values()
        for boss in instance["bosses"]
        if "error" not in boss
    )
    
    print(f"\nSummary:")
    print(f"  Total Encounters: {total_encounters}")
    print(f"  Successful: {total_success}")
    print(f"  Failed: {total_encounters - total_success}")

if __name__ == "__main__":
    scrape_all_encounters()
