import requests
from bs4 import BeautifulSoup
import json
import time
import random
import re
import os

class XuFuScraper:
    def __init__(self):
        self.base_url = "https://www.wow-petguide.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.data = {}
        self.visited_urls = set()

    def get_soup(self, url):
        if url in self.visited_urls:
            return None
        
        print(f"Fetching: {url}")
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                self.visited_urls.add(url)
                # Add random delay to be polite
                time.sleep(random.uniform(1.0, 2.0))
                return BeautifulSoup(response.text, 'html.parser')
            else:
                print(f"Failed to fetch {url}: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape_category(self, expansion, category_name, url_suffix):
        full_url = f"{self.base_url}/{url_suffix}"
        soup = self.get_soup(full_url)
        if not soup:
            return

        print(f"Processing {expansion} - {category_name}")
        
        # Find all encounter links
        links = soup.find_all('a', href=re.compile(r'/(Strategy|Encounter)/'))
        
        encounters = []
        for link in links:
            href = link.get('href')
            name = link.get_text().strip()
            if not name or href.startswith('#'):
                continue
                
            if any(e['url'] == href for e in encounters):
                continue

            encounters.append({
                'name': name,
                'url': href
            })

        print(f"Found {len(encounters)} encounters in {category_name}")
        
        # Initialize structure if needed
        if expansion not in self.data:
            self.data[expansion] = {}
        
        self.data[expansion][category_name] = []
        
        for encounter in encounters:
            strategies = self.scrape_encounter(encounter['url'])
            if strategies:
                self.data[expansion][category_name].append({
                    'encounter_name': encounter['name'],
                    'url': encounter['url'],
                    'strategies': strategies
                })

    def scrape_encounter(self, url_suffix):
        if url_suffix.startswith('http'):
            full_url = url_suffix
        else:
            # Ensure leading slash if needed
            if not url_suffix.startswith('/'):
                url_suffix = '/' + url_suffix
            full_url = f"{self.base_url}{url_suffix}"
            
        soup = self.get_soup(full_url)
        if not soup:
            return []

        strategies = []
        
        # On a strategy page, there might be multiple tabs or a list
        # For now, let's assume the page loaded IS the main strategy or contains them
        
        # Extract the main strategy on the page
        strategy = self.extract_strategy_from_page(soup)
        # Only add if it has pets or a script
        if strategy and (strategy.get('pet_slots') or strategy['script']):
            strategies.append(strategy)
            
        # TODO: Check for other strategies (sidebar, tabs)
        # This part is tricky without seeing the live DOM for multiple strategies
        
        return strategies

    def extract_strategy_from_page(self, soup):
        # Try to find strategy name
        strategy_name = "Default Strategy"
        # Look for active tab or header
        active_tab = soup.find('div', class_='nav-link active')
        if active_tab:
            strategy_name = active_tab.get_text().strip()
        
        strategy = {
            'name': strategy_name,
            'pet_slots': [],  # Changed from 'pets' to 'pet_slots' to be more accurate
            'script': ''
        }
        
        # 1. Extract Pets by Slot
        # Xu-Fu shows pet slots with a main pet and alternatives
        # We need to group by slot (typically 3 slots per strategy)
        # Look for pet containers that indicate slots
        pet_containers = soup.find_all('div', class_='col-auto')
        
        current_slot = []
        for container in pet_containers:
            # Check if this is a pet card
            pet_card = container.find(class_='bt_petname')
            if pet_card:
                link = pet_card.find('a', class_='bt_petdetails')
                if link:
                    pet_name = link.get_text().strip()
                    pet_href = link.get('href')
                    pet_id = 0
                    if pet_href:
                        match = re.search(r'/Pet/(\d+)/', pet_href)
                        if match:
                            pet_id = int(match.group(1))
                    
                    current_slot.append({
                        'name': pet_name,
                        'id': pet_id
                    })
            
            # Check if we've hit a slot boundary (e.g., next pet group)
            # Heuristic: if we have pets accumulated and hit certain markers, finalize slot
            # For now, we'll use a simpler approach: group every few pets as alternatives
            
        # Fallback: if we couldn't properly detect slots, just add all pets as one slot
        # This is a simplified approach - we'd need to inspect the actual HTML structure more
        if current_slot:
            strategy['pet_slots'].append(current_slot)
        
        # TEMPORARY FIX: For now, let's just take the first 3 unique pets as a simple team
        # This is not ideal but will work better than the current approach
        all_pets = []
        pet_cards = soup.find_all(class_='bt_petname')
        seen_pets = set()
        for card in pet_cards:
            link = card.find('a', class_='bt_petdetails')
            if link:
                pet_name = link.get_text().strip()
                if pet_name not in seen_pets:  # Avoid duplicates
                    seen_pets.add(pet_name)
                    pet_href = link.get('href')
                    pet_id = 0
                    if pet_href:
                        match = re.search(r'/Pet/(\d+)/', pet_href)
                        if match:
                            pet_id = int(match.group(1))
                    
                    all_pets.append({
                        'name': pet_name,
                        'id': pet_id
                    })
                    
                    if len(all_pets) >= 3:  # Pet battles use max 3 pets
                        break
        
        # Use the first 3 unique pets as the team
        strategy['pet_slots'] = [[pet] for pet in all_pets[:3]]
        
        # 2. Extract Script
        tooltip = soup.find(id='td_tooltip')
        if tooltip:
            script_text = tooltip.get_text().strip()
            lines = script_text.split('\n')
            # Filter out UI text
            clean_lines = [l for l in lines if "Click the button" not in l and "wow-petsim" not in l]
            strategy['script'] = '\n'.join(clean_lines).strip()
        
        return strategy

    def save_data(self, filename='strategies.json'):
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=2)
        print(f"Saved data to {filename}")

def main():
    scraper = XuFuScraper()
    
    # Define categories to scrape by expansion
    # Format: (Expansion, Category, URL_Suffix)
    targets = [
        # The War Within
        ('The War Within', 'World Quests', 'Section/104/World_Quests'),
        ('The War Within', 'The Undermine', 'Section/110/The_Undermine'),
        
        # Dragonflight
        ('Dragonflight', 'World Quests', 'Section/97/World_Quests'),
        ('Dragonflight', 'The Forbidden Reach', 'Section/99/The_Forbidden_Reach'),
        ('Dragonflight', 'Zaralek Cavern', 'Section/100/Zaralek_Cavern'),
        
        # Shadowlands
        ('Shadowlands', 'World Quests', 'Section/80/World_Quests'),
        ('Shadowlands', 'Covenant Adventures', 'Section/85/Covenant_Adventures'),
        ('Shadowlands', 'Torghast', 'Section/87/Torghast_Tower_of_the_Damned'),
        ('Shadowlands', 'Family Exorcist', 'Section/89/Family_Exorcist'),
        
        # Battle for Azeroth
        ('BfA', 'World Quests', 'Section/64/World_Quests'),
        ('BfA', 'Island Expeditions', 'Section/68/Island_Expeditions'),
        ('BfA', 'Warfronts', 'Section/69/Warfronts'),
        ('BfA', 'Family Battler', 'Section/71/Battle_for_Azeroth_Family_Battler'),
        ('BfA', 'Nazjatar & Mechagon', 'Section/72/Nazjatar_and_Mechagon'),
        
        # Legion
        ('Legion', 'World Quests', 'Section/49/World_Quests'),
        ('Legion', 'Family Familiar', 'Section/51/Family_Familiar'),
        ('Legion', 'Broken Isles', 'Section/48/Broken_Isles_Tamers'),
        
        # Draenor
        ('Draenor', 'Garrison', 'Section/36/Garrison'),
        ('Draenor', 'The Menagerie', 'Section/37/The_Menagerie'),
        ('Draenor', 'Tamers', 'Section/38/Draenor_Tamers'),
        
        # Pandaria
        ('Pandaria', 'Spirit Tamers', 'Section/19/Pandaren_Spirit_Tamers'),
        ('Pandaria', 'Beasts of Fable', 'Section/20/Beasts_of_Fable'),
        ('Pandaria', 'Tamers', 'Section/21/Tamers'),
        ('Pandaria', 'Celestial Tournament', 'Section/22/Celestial_Tournament'),
        
        # Dungeons
        ('Dungeons', 'Wailing Caverns', 'Section/54/Wailing_Caverns'),
        ('Dungeons', 'Deadmines', 'Section/55/Deadmines'),
        ('Dungeons', 'Stratholme', 'Section/73/Stratholme'),
        ('Dungeons', 'Blackrock Depths', 'Section/74/Blackrock_Depths'),
        ('Dungeons', 'Gnomeregan', 'Section/75/Gnomeregan'),
        
        # Misc
        ('Misc', 'Darkmoon Faire', 'Section/25/Darkmoon_Faire'),
    ]
    
    print(f"Starting scrape of {len(targets)} categories...")
    
    for expansion, category, url_suffix in targets:
        scraper.scrape_category(expansion, category, url_suffix)
        
    scraper.save_data()

if __name__ == "__main__":
    main()
