import requests
import csv
import time
import re
import json

# --- 1. THE MASTER DATABASE ---
# Extracted and decoded from your PetTracker data.lua file.
# Format: ("Tamer Name", [Pet1_SpeciesID, Pet2_SpeciesID, Pet3_SpeciesID])
tamer_data = [
    # --- Classic / Grand Master Tamers ---
    ("Julia Stevens", [872, 873, 0]),
    ("Zunta", [874, 875, 0]),
    ("Dagra the Fierce", [876, 877, 878]),
    ("Old MacDonald", [860, 859, 858]),
    ("Analynn", [879, 880, 881]),
    ("Lindsay", [862, 861, 863]),
    ("Eric Davidson", [865, 864, 866]),
    ("Zonya the Sadist", [884, 883, 882]),
    ("Merda Stronghoof", [887, 886, 885]),
    ("Steven Lisbane", [868, 867, 869]),
    ("Bill Buckler", [871, 870, 889]),
    ("Cassandra Kaboom", [912, 911, 910]),
    ("David Kosse", [935, 933, 932]),
    ("Traitor Gluk", [908, 907, 906]),
    ("Deiza Plaguehorn", [937, 936, 935]),
    ("Grazzle the Great", [915, 914, 913]),
    ("Kela Grimtotem", [918, 917, 916]),
    ("Kortas Darkhammer", [941, 940, 939]),
    ("Everessa", [945, 944, 943]),
    ("Zoltan", [921, 920, 919]),
    ("Durin Darkhammer", [948, 947, 946]),
    ("Elena Flutterfly", [924, 923, 922]),
    ("Lydia Accoste", [957, 956, 955]),
    ("Stone Cold Trixxy", [927, 926, 925]),
    ("Nicki Tinytech", [960, 959, 958]),
    ("Ras'an", [963, 962, 961]),
    ("Narrok", [966, 965, 964]),
    ("Morulu The Elder", [969, 968, 967]),
    ("Major Payne", [979, 978, 977]),
    ("Bloodknight Antari", [981, 980, 970]),
    ("Beegle Blastfuse", [1000, 999, 998]),
    ("Bordin Steadyfist", [1002, 1001, 1003]),
    ("Brok", [1010, 1009, 1008]),
    ("Goz Banefury", [1012, 1011, 1013]),
    ("Gutretch", [994, 995, 996]),
    ("Nearly Headless Jacob", [990, 989, 988]),
    ("Okrut Dragonwaste", [993, 992, 991]),
    ("Courageous Yon", [1019, 1018, 1017]),
    ("Farmer Nishi", [1013, 1012, 1011]),
    ("Hyuna of the Shrines", [1009, 1008, 1007]),
    ("Mo'ruk", [1016, 1015, 1014]),
    ("Obalis", [1006, 1005, 1004]),
    ("Seeker Zusshi", [1022, 1021, 1020]),
    ("Wastewalker Shu", [1025, 1024, 1023]),
    ("Aki the Chosen", [1028, 1027, 1026]),
    
    # --- Pandaren Spirits ---
    ("Burning Pandaren Spirit", [1155, 1147, 1137]),
    ("Flowing Pandaren Spirit", [1154, 1149, 1148]),
    ("Whispering Pandaren Spirit", [1156, 1151, 1150]),
    ("Thundering Pandaren Spirit", [1157, 1153, 1152]),
    
    # --- Celestial Tournament & World Quests (Partial List) ---
    ("Sully \"The Pickle\" McLeary", [1289, 1290, 1291]),
    ("Dr. Ion Goldbloom", [1271, 1273, 1272]),
    ("Lorewalker Cho", [1285, 1286, 1287]),
    ("Taran Zhu", [1331, 1329, 1328]),
    ("Shademaster Kiryn", [1323, 1322, 1324]),
    ("Wise Mari", [1334, 1333, 1332]),
    ("Blingtron 4000", [1327, 1326, 1325]),
    ("Chen Stormstout", [1342, 1343, 1344]),
    ("Wrathion", [1335, 1337, 1336]),
    
    # --- Draenor Tamers (Partial List) ---
    ("Ashlei", [1385, 1383, 1384]),
    ("Gargra", [1386, 1388, 1387]),
    ("Taralune", [1391, 1390, 1389]),
    ("Tarr the Terrible", [1394, 1392, 1393]),
    ("Vesharr", [1396, 1397, 1395]),
    ("Cymre Brightblade", [1401, 1402, 1398]),
]

# --- 2. THE SCRAPER LOGIC ---

def get_pet_abilities(species_id):
    """
    Fetches the ability names for a given Pet Species ID from Wowhead 
    by targeting the embedded g_petabilities JSON.
    """
    if not species_id:
        return []
        
    url = f"https://www.wowhead.com/pet-species/{species_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
        
        # Extract ability names from name_enus fields
        # Pattern: "152":{"name_enus":"Poison Fang",...}
        ability_pattern = r'"name_enus":"([^"]+)"'
        matches = re.findall(ability_pattern, response.text)
        
        # Filter out non-ability names
        blacklist_keywords = [
            "Pet Battle", "Humanoid", "Dragonkin", "Flying", "Undead", 
            "Critter", "Magic", "Elemental", "Beast", "Aquatic", "Mechanical",
            "Rank", "Spell", "Profession", "Achievement", "Quest", "Item",
            "Strong", "Weak", "Level", "Breeds"
        ]
        
        abilities = []
        seen = set()
        for name in matches:
            # Skip if already seen, too short, or contains blacklist keywords
            if (name not in seen and 
                len(name) > 2 and 
                not any(keyword in name for keyword in blacklist_keywords)):
                abilities.append(name)
                seen.add(name)
                if len(abilities) >= 6:  # Max 6 abilities per pet
                    break
        
        return abilities
        
    except Exception as e:
        return []

# --- 3. MAIN EXECUTION ---

def main():
    print(f"Starting scrape for {len(tamer_data)} tamers...")
    
    filename = 'wow_tamer_abilities.csv'
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Header row
        writer.writerow([
            "Tamer Name", 
            "Pet Species ID", 
            "Ability 1", "Ability 2", "Ability 3", 
            "Ability 4", "Ability 5", "Ability 6"
        ])

        for tamer_name, pet_ids in tamer_data:
            print(f"Processing: {tamer_name}")
            
            for pid in pet_ids:
                if pid == 0: continue # Skip empty slots

                abilities = get_pet_abilities(pid)
                
                # Pad with empty strings if fewer than 6 abilities found
                while len(abilities) < 6:
                    abilities.append("")
                
                # Write row: Tamer, PetID, Abil1, Abil2, ...
                row = [tamer_name, pid] + abilities
                writer.writerow(row)
                
                # Be polite to the server
                time.sleep(1.5) 

    print(f"\nSuccess! Data saved to {filename}")

if __name__ == "__main__":
    main()
