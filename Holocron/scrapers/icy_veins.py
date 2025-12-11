import requests
from bs4 import BeautifulSoup
import re
import json
import sys

class IcyVeinsScraper:
    BASE_URL = "https://www.icy-veins.com/wow"

    def __init__(self, class_name, spec_name):
        self.class_name = class_name
        self.spec_name = spec_name
        # Construct slug, e.g., "havoc-demon-hunter-pve-dps"
        self.slug = f"{spec_name}-{class_name}-pve-dps"

    def fetch_stats(self):
        url = f"{self.BASE_URL}/{self.slug}-stat-priority"
        print(f"Fetching Stats from: {url}")
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
            response.raise_for_status()
        except Exception as e:
            print(f"Error fetching stats: {e}")
            return {}

        soup = BeautifulSoup(response.text, 'html.parser')
        stats_data = {}
        
        # Standard Stat Names Mapping
        stat_map = {
            "Agility": "MainStat", "Strength": "MainStat", "Intellect": "MainStat",
            "Critical Strike": "Crit", "Crit": "Crit",
            "Haste": "Haste",
            "Mastery": "Mastery",
            "Versatility": "Versatility"
        }

        # Find all headers
        headers = soup.find_all(['h2', 'h3', 'h4'])
        print(f"Found {len(headers)} headers.")
        
        for header in headers:
            text = header.get_text(strip=True)
            # print(f"Checking header: {text}") # Uncomment for verbose debug
            
            if "Stat Priority" in text and "Changelog" not in text and "Summary" not in text:
                print(f"  -> Match! Processing: {text}")
                context_name = text.replace("Stat Priority", "").strip() or "General"
                
                # Scan forward for the first <ol> before the next header
                stat_list = []
                
                # Get all subsequent elements
                siblings = header.find_all_next()
                
                for elem in siblings:
                    if elem.name in ['h2', 'h3', 'h4']:
                        # Stop if we hit a new header
                        break
                    
                    if elem.name == 'ol':
                        for li in elem.find_all('li'):
                            stat_text = li.get_text(strip=True)
                            clean = re.sub(r'^\d+\.\s*', '', stat_text)
                            clean = re.sub(r'[;.]', '', clean)
                            
                            if "=" in clean:
                                parts = [p.strip() for p in clean.split('=')]
                                stat_list.extend(parts)
                            elif ">" in clean:
                                parts = [p.strip() for p in clean.split('>')]
                                stat_list.extend(parts)
                            else:
                                stat_list.append(clean)
                        break # Found the list, stop searching
                
                if stat_list:
                    print(f"    -> Found stats: {stat_list}")
                    weights = {}
                    current_weight = 1.2
                    for stat in stat_list:
                        matched_stat = None
                        for key, val in stat_map.items():
                            if key.lower() in stat.lower():
                                matched_stat = val
                                break
                        
                        if matched_stat:
                            weights[matched_stat] = round(current_weight, 2)
                            current_weight -= 0.1
                    
                    if "MainStat" not in weights:
                        weights["MainStat"] = 1.0
                        
                    stats_data[context_name] = weights

        return stats_data

    def fetch_talents(self):
        url = f"{self.BASE_URL}/{self.slug}-spec-builds-talents"
        print(f"Fetching Talents from: {url}")
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
            response.raise_for_status()
        except Exception as e:
            print(f"Error fetching talents: {e}")
            return {}

        soup = BeautifulSoup(response.text, 'html.parser')
        talents_data = {}

        # Keywords for Context
        context_keywords = {
            "Raid": ["Raid", "Single-Target"],
            "MythicPlus": ["Mythic+", "AoE", "Dungeon"],
            "Delves": ["Delves"],
            "PvP": ["PvP", "War Mode"]
        }

        # Find all headers
        headers = soup.find_all(['h2', 'h3', 'h4'])
        print(f"Found {len(headers)} headers.")
        
        for header in headers:
            text = header.get_text(strip=True)
            
            # Determine Context
            found_context = None
            for context, keywords in context_keywords.items():
                if any(k in text for k in keywords):
                    found_context = context
                    break
            
            if found_context:
                print(f"  -> Match Context '{found_context}' in header: {text}")
                
                # Scan forward for copy button/input
                siblings = header.find_all_next()
                
                for elem in siblings:
                    if elem.name in ['h2', 'h3', 'h4']:
                        break
                        
                    # 1. Check <input value="...">
                    if elem.name == 'input':
                        val = elem.get('value', '')
                        if len(val) > 50 and not " " in val: 
                            key = f"{found_context} ({text})"
                            talents_data[key] = val
                            print(f"    -> Found string for {key}")
                            break
                    
                    # 2. Check elements with class *copy*
                    # This is a bit broad, so we check specifically for data attributes
                    if elem.has_attr('class') and any('copy' in c.lower() for c in elem['class']):
                        val = elem.get('data-clipboard-text')
                        if val and len(val) > 50:
                            key = f"{found_context} ({text})"
                            talents_data[key] = val
                            print(f"    -> Found string for {key}")
                            break
                    
                    # 4. Check for Icy Veins "export_string_widget"
                    if elem.name == 'div' and elem.has_attr('class') and 'export_string_widget' in elem['class']:
                        # Found a widget!
                        # Get the label from the span
                        label_span = elem.find('span')
                        label = label_span.get_text(strip=True) if label_span else "Unknown"
                        
                        # Get the string from the hidden div (or any div with long text)
                        # Usually it's the last div or a div with style display:none
                        inner_divs = elem.find_all('div')
                        for div in inner_divs:
                            text_val = div.get_text(strip=True)
                            if len(text_val) > 50 and not " " in text_val:
                                # Found it!
                                key = f"{found_context} ({label})"
                                talents_data[key] = text_val
                                print(f"    -> Found string for {key}")
                                break
                        
                        # If we found one in this widget, we might want to continue searching for MORE widgets
                        # but usually they are grouped. Let's not break the main loop yet, 
                        # but we should probably mark this widget as processed.
                        continue

        return talents_data

    def fetch_gear(self):
        url = f"{self.BASE_URL}/{self.slug}-bis-gear"
        print(f"Fetching Gear from: {url}")
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
            response.raise_for_status()
        except Exception as e:
            print(f"Error fetching gear: {e}")
            return {}

        soup = BeautifulSoup(response.text, 'html.parser')
        gear_data = {}

        # Icy Veins BiS pages usually have tables for each slot or one big table.
        # Common format: Headers (h3/h4) like "Head", "Neck" followed by a table.
        # OR a single table with a "Slot" column.
        
        # Strategy 1: Look for headers matching slot names, then the next table.
        slots = [
            "Head", "Neck", "Shoulders", "Back", "Chest", "Wrist", 
            "Hands", "Waist", "Legs", "Feet", "Finger", "Trinket", 
            "Main Hand", "Off Hand", "Two-Hand", "Weapon"
        ]
        
        # Find all headers
        headers = soup.find_all(['h2', 'h3', 'h4'])
        
        for header in headers:
            text = header.get_text(strip=True)
            
            # Check if header matches a slot
            matched_slot = None
            for slot in slots:
                if slot in text and "Enchant" not in text:
                    matched_slot = slot
                    break
            
            if matched_slot:
                # Look for the next table
                table = header.find_next('table')
                if table:
                    # Check if this table is "close" to the header (not miles away)
                    # For now, assume it's the right one.
                    
                    rows = table.find_all('tr')
                    items = []
                    
                    for row in rows:
                        cols = row.find_all('td')
                        if not cols: continue
                        
                        # Extract Item Name and Link
                        item_link = row.find('a', href=True)
                        if item_link:
                            name = item_link.get_text(strip=True)
                            href = item_link['href']
                            
                            # Extract ID from Wowhead link (item=12345)
                            item_id = None
                            match = re.search(r'item=(\d+)', href)
                            if match:
                                item_id = match.group(1)
                            
                            # Extract Source (usually last column)
                            source = cols[-1].get_text(strip=True)
                            
                            if item_id and name:
                                items.append({
                                    "name": name,
                                    "id": item_id,
                                    "source": source,
                                    "slot": matched_slot
                                })
                    
                    if items:
                        if matched_slot not in gear_data:
                            gear_data[matched_slot] = []
                        gear_data[matched_slot].extend(items)
                        print(f"  -> Found {len(items)} items for {matched_slot}")

        return gear_data

    def fetch_consumables(self):
        url = f"{self.BASE_URL}/{self.slug}-enchants-gems"
        print(f"Fetching Consumables from: {url}")
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
            response.raise_for_status()
        except Exception as e:
            print(f"Error fetching consumables: {e}")
            return {}

        soup = BeautifulSoup(response.text, 'html.parser')
        consumables = {
            "enchants": [],
            "gems": []
        }

        # 1. Enchants
        # Look for headers like "Enchants" or specific slots "Chest", "Ring"
        # Usually presented in a table or list.
        # Strategy: Find headers for slots, then look for the recommended item.
        
        slots = ["Weapon", "Chest", "Cloak", "Legs", "Wrist", "Boots", "Ring"]
        
        headers = soup.find_all(['h2', 'h3', 'h4'])
        for header in headers:
            text = header.get_text(strip=True)
            
            # Check for Slot Headers
            matched_slot = None
            for slot in slots:
                if slot in text and "Enchant" not in text: # e.g. "Chest" header under "Enchants" section
                     # This is tricky because headers might just be "Chest"
                     # We need to ensure we are in the Enchants section.
                     pass
            
            # Better Strategy: Look for tables that contain "Enchant" text in cells?
            # Or look for the specific format Icy Veins uses.
            # Usually: <h3>Enchants</h3> <table>...</table>
            
            if "Enchants" in text and "Best" in text:
                 # Found the main Enchants section/header
                 # The next table usually lists them all.
                 table = header.find_next('table')
                 if table:
                     rows = table.find_all('tr')
                     for row in rows:
                         cols = row.find_all('td')
                         if len(cols) >= 2:
                             slot_name = cols[0].get_text(strip=True)
                             enchant_name = cols[1].get_text(strip=True)
                             
                             # Clean up
                             # Remove " (Alliance)" etc if needed
                             
                             consumables["enchants"].append({
                                 "slot": slot_name,
                                 "name": enchant_name
                             })
        
        # Fallback: If no big table, look for individual slot tables (older format)
        if not consumables["enchants"]:
             # Try to find any table with "Item" and "Enchant" headers?
             pass

        # 2. Gems
        # Look for "Gems" header
        for header in headers:
            text = header.get_text(strip=True)
            if "Gems" in text and "Best" in text:
                # Look for list or table
                # Often a bulleted list of "Best X Gem: [Item Name]"
                siblings = header.find_all_next()
                for elem in siblings:
                    if elem.name in ['h2', 'h3', 'h4']:
                        break
                    
                    if elem.name == 'ul':
                        for li in elem.find_all('li'):
                            # Extract link text
                            link = li.find('a')
                            if link:
                                gem_name = link.get_text(strip=True)
                                consumables["gems"].append(gem_name)
                        break
                    
                    if elem.name == 'table':
                        # Sometimes in a table
                        rows = elem.find_all('tr')
                        for row in rows:
                            cols = row.find_all('td')
                            for col in cols:
                                link = col.find('a')
                                if link:
                                    consumables["gems"].append(link.get_text(strip=True))
                        break

        # Deduplicate Gems
        consumables["gems"] = list(set(consumables["gems"]))

        return consumables

    def save_to_json(self, data, filename):
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Saved data to {filename}")
        except Exception as e:
            print(f"Error saving to {filename}: {e}")

    def fetch_encounter(self, instance, boss):
        """
        Scrape encounter information from Icy Veins
        Args:
            instance: e.g., "nerub-ar-palace"
            boss: e.g., "queen-ansurek"
        Returns:
            dict with abilities, phases, tactics
        """
        # Construct URL
        url = f"{self.BASE_URL}/{instance}-{boss}-strategy-guide"
        print(f"Fetching Encounter from: {url}")
        
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
        except Exception as e:
            print(f"Error fetching encounter: {e}")
            return {"error": str(e)}
        
        soup = BeautifulSoup(response.text, 'html.parser')
        encounter = {
            "instance": instance,
            "boss": boss,
            "url": url,
            "overview": "",
            "abilities": [],
            "phases": [],
            "role_notes": {
                "tank": [],
                "healer": [],
                "dps": []
            }
        }
        
        # Extract overview (usually in the first paragraph)
        intro_p = soup.find('p')
        if intro_p:
            encounter["overview"] = intro_p.get_text(strip=True)[:500]  # First 500 chars
        
        # Extract abilities
        # Look for sections like "Abilities" or "Key Mechanics"
        headers = soup.find_all(['h2', 'h3', 'h4'])
        for header in headers:
            text = header.get_text(strip=True)
            
            if any(keyword in text.lower() for keyword in ['abilities', 'mechanics', 'spells']):
                # Find next ul/ol
                next_list = header.find_next(['ul', 'ol'])
                if next_list:
                    for li in next_list.find_all('li'):
                        ability_text = li.get_text(strip=True)
                        if ability_text:
                            encounter["abilities"].append(ability_text)
            
            # Extract phases
            if 'phase' in text.lower():
                phase_content = []
                # Get content until next h2/h3
                sibling = header.find_next_sibling()
                while sibling and sibling.name not in ['h2', 'h3']:
                    if sibling.name in ['p', 'ul', 'ol']:
                        phase_content.append(sibling.get_text(strip=True))
                    sibling = sibling.find_next_sibling()
                
                encounter["phases"].append({
                    "name": text,
                    "description": " ".join(phase_content)[:300]  # Limit length
                })
            
            # Extract role-specific notes
            text_lower = text.lower()
            for role in ['tank', 'healer', 'dps']:
                if role in text_lower:
                    next_list = header.find_next(['ul', 'ol', 'p'])
                    if next_list:
                        role_text = next_list.get_text(strip=True)
                        if role_text:
                            encounter["role_notes"][role].append(role_text[:200])
        
        return encounter

if __name__ == "__main__":
    # Test with Havoc Demon Hunter
    scraper = IcyVeinsScraper("demon-hunter", "havoc")
    
    print("--- STATS ---")
    stats = scraper.fetch_stats()
    print(json.dumps(stats, indent=2))
    scraper.save_to_json(stats, "scraped_stats.json")
    
    print("\n--- TALENTS ---")
    talents = scraper.fetch_talents()
    print(json.dumps(talents, indent=2))
    scraper.save_to_json(talents, "scraped_talents.json")
