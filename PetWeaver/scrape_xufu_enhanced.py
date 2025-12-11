import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime

class XuFuScraperEnhanced:
    def __init__(self):
        self.base_url = "https://www.wow-petguide.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.data = {}
        self.request_count = 0
        self.start_time = None
        
    def respectful_delay(self):
        """Add 1.5 second delay between requests to be respectful"""
        time.sleep(1.5)
        self.request_count += 1
        if self.request_count % 10 == 0:
            elapsed = time.time() - self.start_time if self.start_time else 0
            print(f"Progress: {self.request_count} requests in {elapsed:.1f}s (avg {elapsed/self.request_count:.2f}s per request)")
    
    def get_soup(self, url):
        try:
            self.respectful_delay()
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def _parse_single_pane(self, container, strategy_name):
        """Extract pets and script from a specific HTML container (tab pane)"""
        strategy = {
            'name': strategy_name,
            'pet_slots': [],
            'script': ''
        }
        
        # 1. Extract Pets
        # Look for pet cards specifically within this container
        current_slot_pets = []
        all_pet_links = container.find_all('a', class_='bt_petdetails')
        
        for link in all_pet_links:
            pet_name = link.get_text().strip()
            pet_href = link.get('href', '')
            
            pet_id = 0
            if pet_href:
                match = re.search(r'/Pet/(\d+)/', pet_href)
                if match: pet_id = int(match.group(1))
            
            # Store pet info
            current_slot_pets.append({'name': pet_name, 'id': pet_id})

        # Group into 3 Slots (Heuristic)
        # Xu-Fu lists main pets then alternatives. 
        # If we have >3 pets, we assume 1, 2, 3 are main, and rest are alts.
        total_pets = len(current_slot_pets)
        if total_pets >= 3:
            slot1 = [current_slot_pets[0]]
            slot2 = [current_slot_pets[1]]
            slot3 = [current_slot_pets[2]]
            
            # Distribute alternatives
            for i, pet in enumerate(current_slot_pets[3:]):
                idx = i % 3
                if idx == 0: slot1.append(pet)
                elif idx == 1: slot2.append(pet)
                else: slot3.append(pet)
                
            strategy['pet_slots'] = [slot1, slot2, slot3]
        else:
            # Less than 3 pets? Just list them as slots.
            strategy['pet_slots'] = [[p] for p in current_slot_pets]

        # 2. Extract Script
        script_text = ""
        
        # Method A: Check for code blocks/textareas
        code_blocks = container.find_all(['pre', 'code', 'textarea', 'div'], class_=['code', 'script-box'])
        for block in code_blocks:
            text = block.get_text()
            if "use(" in text or "change(" in text:
                script_text = text
                break
        
        # Method B: Fallback search in raw text
        if not script_text:
            text = container.get_text()
            if "use(" in text:
                lines = text.split('\n')
                # Filter for script-like lines
                script_lines = [l.strip() for l in lines if "use(" in l or "change(" in l or "standby" in l or "if" in l]
                script_text = "\n".join(script_lines)

        strategy['script'] = script_text.strip()
        
        return strategy

    def extract_strategies_from_page(self, soup):
        """Parses ALL tabs to get every strategy variation"""
        strategies = []
        
        # 1. Find all Tab Panes (The content containers)
        tab_panes = soup.find_all('div', class_='tab-pane')
        
        if not tab_panes:
            # Fallback: Single page view (no tabs)
            main_strat = self._parse_single_pane(soup, "Default Strategy")
            if main_strat['pet_slots'] or main_strat['script']:
                strategies.append(main_strat)
            return strategies

        # 2. Map Tab IDs to Names (from the nav bar)
        tab_names = {}
        nav_links = soup.find_all('a', class_='nav-link')
        for link in nav_links:
            href = link.get('href', '')
            if href.startswith('#'):
                tab_id = href[1:]
                tab_names[tab_id] = link.get_text(strip=True)

        # 3. Process Each Pane
        for pane in tab_panes:
            pane_id = pane.get('id')
            # Skip if it's a comment/discussion tab
            name = tab_names.get(pane_id, f"Strategy {pane_id}")
            if "comment" in name.lower() or "discussion" in name.lower():
                continue

            strat_data = self._parse_single_pane(pane, name)
            
            # Only save if valid
            if strat_data['pet_slots'] or strat_data['script']:
                strategies.append(strat_data)

        return strategies

    def scrape_encounter(self, encounter_url, url_suffix):
        """Scrape strategies for a single encounter"""
        print(f"Fetching: {encounter_url}")
        
        if url_suffix.startswith('http'): full_url = url_suffix
        else: full_url = f"{self.base_url}{url_suffix}"
            
        soup = self.get_soup(full_url)
        if not soup: return []

        # Use the new Multi-Strategy Extractor
        strategies = self.extract_strategies_from_page(soup)
        
        if strategies:
            print(f"  -> Found {len(strategies)} strategies")
        else:
            print("  -> No strategies found.")
            
        return strategies

    def scrape_category(self, category_url, category_suffix):
        """Scrape all encounters in a category"""
        print(f"\nScanning Category: {category_url}")
        soup = self.get_soup(category_url)
        if not soup: return []

        encounters = []
        links = soup.find_all('a', href=re.compile(r'/(Strategy|Encounter)/\d+'))
        
        for link in links:
            href = link.get('href')
            encounter_name = link.get_text().strip()
            
            if href and encounter_name:
                encounter_url = f"{self.base_url}{href}" if not href.startswith('http') else href
                encounters.append({
                    'name': encounter_name,
                    'url': encounter_url,
                    'url_suffix': href
                })
        
        # Deduplicate
        seen_urls = set()
        unique_encounters = []
        for enc in encounters:
            if enc['url'] not in seen_urls:
                seen_urls.add(enc['url'])
                unique_encounters.append(enc)
        
        return unique_encounters

    def scrape_all(self):
        """Main scraping method"""
        self.start_time = time.time()
        print(f"Starting enhanced scrape at {datetime.now().strftime('%H:%M:%S')}")
        
        # List of Categories to Scrape
        categories = {
            "The War Within": {
                "World Quests": "/Section/104/World_Quests"
            },
            "Pandaria": {
                "Spirit Tamers": "/Section/19/Pandaren_Spirit_Tamers",
                "Beasts of Fable": "/Section/20/Beasts_of_Fable",
                "Tamers": "/Section/21/Tamers",
                "Celestial Tournament": "/Section/22/Celestial_Tournament"
            },
            "Draenor": {
                "Tamers": "/Section/38/Draenor_Tamers"
            }
        }
        
        for expansion, cats in categories.items():
            self.data[expansion] = {}
            for category_name, category_suffix in cats.items():
                category_url = f"{self.base_url}{category_suffix}"
                
                encounters_list = self.scrape_category(category_url, category_suffix)
                print(f"Found {len(encounters_list)} encounters in {category_name}")
                
                category_data = []
                for encounter in encounters_list:
                    strategies = self.scrape_encounter(encounter['url'], encounter['url_suffix'])
                    if strategies:
                        category_data.append({
                            'encounter_name': encounter['name'],
                            'url': encounter['url'],
                            'strategies': strategies
                        })
                
                self.data[expansion][category_name] = category_data
        
        elapsed = time.time() - self.start_time
        print(f"\nScraping complete! {self.request_count} requests in {elapsed/60:.1f} minutes")

    def save_data(self, filename='strategies_enhanced.json'):
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=2)
        print(f"Saved data to {filename}")

def main():
    scraper = XuFuScraperEnhanced()
    scraper.scrape_all()
    scraper.save_data()

if __name__ == "__main__":
    main()
