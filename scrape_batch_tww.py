"""
Test batch scraper for The War Within encounters.
This validates the browser-based scraping approach before scaling up.
"""

import json
from datetime import datetime

# The War Within World Quests encounters
TWW_ENCOUNTERS = [
    {"name": "Rock Collector", "url": "https://www.wow-petguide.com/Encounter/1589/Rock_Collector"},
    {"name": "Robot Rumble", "url": "https://www.wow-petguide.com/Encounter/1590/Robot_Rumble"},
    {"name": "The Power of Friendship", "url": "https://www.wow-petguide.com/Encounter/1592/The_Power_of_Friendship"},
    {"name": "Major Malfunction", "url": "https://www.wow-petguide.com/Encounter/1593/Major_Malfunction"},
    {"name": "Miniature Army", "url": "https://www.wow-petguide.com/Encounter/1595/Miniature_Army"},
    {"name": "The Thing from the Swamp", "url": "https://www.wow-petguide.com/Encounter/1596/The_Thing_from_the_Swamp"},
    {"name": "Ziriak", "url": "https://www.wow-petguide.com/Encounter/1598/Ziriak"},
    {"name": "One Hungry Worm", "url": "https://www.wow-petguide.com/Encounter/1599/One_Hungry_Worm"}
]

def save_encounter_data(encounter_name, teams_data, script_data):
    """Save individual encounter data"""
    filename = f"tww_test_{encounter_name.lower().replace(' ', '_')}.json"
    data = {
        "encounter_name": encounter_name,
        "scraped_at": datetime.now().isoformat(),
        "teams": teams_data,
        "script": script_data,
        "team_count": len(teams_data) if teams_data else 0
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved {encounter_name}: {len(teams_data) if teams_data else 0} teams")
    return filename

if __name__ == "__main__":
    print("The War Within Test Scrape Coordinator")
    print(f"Will scrape {len(TWW_ENCOUNTERS)} encounters")
    print("\nEncounters to scrape:")
    for enc in TWW_ENCOUNTERS:
        print(f"  - {enc['name']}")
