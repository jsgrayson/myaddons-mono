import requests
from bs4 import BeautifulSoup
import json
import time
import re

# CONFIGURATION
WOWHEAD_URL = "https://www.wowhead.com"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def fetch_instance_list(category, expansion_slug="the-war-within"):
    """
    Crawls the Wowhead list page to find instances dynamically.
    category: 'raids' or 'dungeons'
    """
    url = f"{WOWHEAD_URL}/zones/instances/{category}/{expansion_slug}"
    print(f"Crawling {category} list: {url}")
    
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to fetch list page: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Wowhead listviews are often JS-rendered, but sometimes have noscript or static data.
        # We look for links to /zone=ID or /zone=NAME
        # This is a best-effort scrape of the static HTML.
        
        instances = []
        # Look for specific table rows or list items. 
        # Wowhead usually puts data in a <script> block with `new Listview`
        
        script_content = None
        for script in soup.find_all('script'):
            if script.string and 'new Listview' in script.string:
                script_content = script.string
                break
        
        if script_content:
            # Extract the JSON-like data from the script
            # This is a regex hack to find the 'data' array
            match = re.search(r'data: \[(.*?)\]', script_content, re.DOTALL)
            if match:
                data_str = match.group(1)
                # This string is JS object literals, not valid JSON (keys no quotes).
                # We'll try to regex extract names and IDs.
                
                # Pattern for id: 1234, name: "Name"
                # Note: Wowhead uses 'id' for zone ID.
                entries = re.findall(r'id:\s*(\d+),\s*name:\s*"(.*?)"', data_str)
                
                for zone_id, name in entries:
                    # Filter out non-instance zones if necessary, but this URL should be filtered already
                    # Decode unicode escapes if any
                    name = bytes(name, 'utf-8').decode('unicode_escape')
                    
                    instances.append({
                        "name": name,
                        "id": int(zone_id),
                        "type": "Raid" if category == 'raids' else "Dungeon",
                        "url": f"{WOWHEAD_URL}/zone={zone_id}"
                    })
                    print(f"Found {category[:-1].title()}: {name} (ID: {zone_id})")
        
        return instances

    except Exception as e:
        print(f"Error crawling {category}: {e}")
        return []

def scrape_bosses_from_instance(instance):
    """
    Given an instance dict, fetch its page and find bosses.
    """
    print(f"Scraping instance: {instance['name']} ({instance['url']})")
    encounters = []
    
    try:
        response = requests.get(instance['url'], headers=HEADERS)
        if response.status_code != 200:
            return []
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for "Bosses" tab or list
        # Again, likely in a Listview script
        script_content = None
        for script in soup.find_all('script'):
            if script.string and 'new Listview' in script.string and 'id: "bosses"' in script.string:
                script_content = script.string
                break
        
        if script_content:
            match = re.search(r'data: \[(.*?)\]', script_content, re.DOTALL)
            if match:
                data_str = match.group(1)
                # Extract NPC IDs and Names
                # id: 1234, name: "Boss Name"
                entries = re.findall(r'id:\s*(\d+),\s*name:\s*"(.*?)"', data_str)
                
                for npc_id, name in entries:
                    name = bytes(name, 'utf-8').decode('unicode_escape')
                    encounters.append({
                        "id": int(npc_id), # Using NPC ID as Encounter ID for now
                        "name": name,
                        "npc_id": int(npc_id),
                        "instance_id": instance['id'],
                        "instance_name": instance['name'],
                        "type": instance['type'],
                        "guide_url": f"{WOWHEAD_URL}/npc={npc_id}"
                    })
                    # print(f"  Found Boss: {name}")
        
    except Exception as e:
        print(f"Error scraping instance {instance['name']}: {e}")
        
    return encounters

def main():
    print("Starting Dynamic Wowhead Crawler...")
    
    all_instances = []
    all_encounters = []
    
    # Hardcoded list of targets (Raids, Dungeons, World Bosses)
    # Definitive TWW List (Patch 11.2.7 / Season 3)
    targets = [
        # --- TWW RAIDS ---
        {"name": "Manaforge Omega", "id": 10001, "type": "Raid", "url": "https://www.wowhead.com/zone=manaforge-omega"},
        {"name": "Liberation of Undermine", "id": 10002, "type": "Raid", "url": "https://www.wowhead.com/zone=liberation-of-undermine"},
        {"name": "Blackrock Depths", "id": 10003, "type": "Raid", "url": "https://www.wowhead.com/zone=blackrock-depths"},
        {"name": "Wastes of K'aresh", "id": 10004, "type": "Raid", "url": "https://www.wowhead.com/zone=wastes-of-karesh"},
        {"name": "The Glassed Expanse", "id": 10005, "type": "Raid", "url": "https://www.wowhead.com/zone=the-glassed-expanse"},
        {"name": "Nerub-ar Palace", "id": 1293, "type": "Raid", "url": "https://www.wowhead.com/zone=nerub-ar-palace"},

        # --- TWW DUNGEONS (All 10) ---
        {"name": "Operation: Floodgate", "id": 10006, "type": "Dungeon", "url": "https://www.wowhead.com/zone=operation-floodgate"},
        {"name": "Eco-Dome Al'dani", "id": 10007, "type": "Dungeon", "url": "https://www.wowhead.com/zone=eco-dome-aldani"},
        {"name": "Ara-Kara, City of Echoes", "id": 2624, "type": "Dungeon", "url": "https://www.wowhead.com/zone=ara-kara-city-of-echoes"},
        {"name": "City of Threads", "id": 2627, "type": "Dungeon", "url": "https://www.wowhead.com/zone=city-of-threads"},
        {"name": "The Stonevault", "id": 2631, "type": "Dungeon", "url": "https://www.wowhead.com/zone=the-stonevault"},
        {"name": "The Dawnbreaker", "id": 2635, "type": "Dungeon", "url": "https://www.wowhead.com/zone=the-dawnbreaker"},
        {"name": "Cinderbrew Meadery", "id": 2640, "type": "Dungeon", "url": "https://www.wowhead.com/zone=cinderbrew-meadery"},
        {"name": "Darkflame Cleft", "id": 2645, "type": "Dungeon", "url": "https://www.wowhead.com/zone=darkflame-cleft"},
        {"name": "Priory of the Sacred Flame", "id": 2650, "type": "Dungeon", "url": "https://www.wowhead.com/zone=priory-of-the-sacred-flame"},
        {"name": "The Rookery", "id": 2655, "type": "Dungeon", "url": "https://www.wowhead.com/zone=the-rookery"},

        # --- TWW WORLD BOSSES (6 Total - Definitive Season 3 List) ---
        {"name": "Kordac, the Dormant Protector", "id": 2620, "npc_id": 221084, "type": "World Boss", "instance": "Isle of Dorn", "guide_url": "https://www.wowhead.com/npc=221084"},
        {"name": "Aggregation of Horrors", "id": 2621, "npc_id": 221224, "type": "World Boss", "instance": "Ringing Deeps", "guide_url": "https://www.wowhead.com/npc=221224"},
        {"name": "Shurrai, Atrocity of the Undersea", "id": 2622, "npc_id": 221196, "type": "World Boss", "instance": "Hallowfall", "guide_url": "https://www.wowhead.com/npc=221196"},
        {"name": "Orta, the Broken Mountain", "id": 2623, "npc_id": 221251, "type": "World Boss", "instance": "Azj-Kahet", "guide_url": "https://www.wowhead.com/npc=221251"},
        {"name": "The Gobfather", "id": 2659, "npc_id": 228000, "type": "World Boss", "instance": "Undermine", "guide_url": "https://www.wowhead.com/npc=228000"},
        {"name": "Reshanor, The Untethered", "id": 2660, "npc_id": 230000, "type": "World Boss", "instance": "K'aresh", "guide_url": "https://www.wowhead.com/npc=230000"},
    ]



    
    # 1. Use the hardcoded targets directly
    all_instances.extend([t for t in targets if t['type'] in ['Raid', 'Dungeon']])
    all_encounters.extend([t for t in targets if t['type'] == 'World Boss']) # Add World Bosses directly to encounters

    # 2. Scrape Bosses for each Instance (Raids/Dungeons)
    for inst in all_instances:
        if inst['url']:
            bosses = scrape_bosses_from_instance(inst)
            all_encounters.extend(bosses)
            time.sleep(1) # Polite delay
        else:
            print(f"Skipping scrape for {inst['name']} (No URL)")

    # 3. Save Data
    codex_data = {
        "instances": all_instances,
        "encounters": all_encounters
    }
    
    with open("codex_data.json", "w") as f:
        json.dump(codex_data, f, indent=4)
        
    print(f"✓ Crawl Complete. Found {len(all_instances)} instances and {len(all_encounters)} encounters.")

if __name__ == "__main__":
    main()
