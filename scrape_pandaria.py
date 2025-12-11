"""
Scrape Pandaria Tamers

Scrapes strategy data for Pandaria Tamers to find missing ability info.
"""

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
                time.sleep(random.uniform(0.5, 1.0))
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
        
        if expansion not in self.data:
            self.data[expansion] = {}
        
        self.data[expansion][category_name] = []
        
        for i, encounter in enumerate(encounters):
            print(f"[{i+1}/{len(encounters)}] Scraping {encounter['name']}...")
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
            if not url_suffix.startswith('/'):
                url_suffix = '/' + url_suffix
            full_url = f"{self.base_url}{url_suffix}"
            
        soup = self.get_soup(full_url)
        if not soup:
            return []

        strategies = []
        strategy = self.extract_strategy_from_page(soup)
        if strategy and (strategy.get('pet_slots') or strategy['script']):
            strategies.append(strategy)
            
        return strategies

    def extract_strategy_from_page(self, soup):
        strategy_name = "Default Strategy"
        active_tab = soup.find('div', class_='nav-link active')
        if active_tab:
            strategy_name = active_tab.get_text().strip()
        
        strategy = {
            'name': strategy_name,
            'pet_slots': [],
            'script': '',
            'enemy_team': [] # Try to extract enemy team!
        }
        
        # Extract Enemy Team (if visible)
        # Look for "Enemy Team" section or similar
        # Xu-Fu often lists enemy pets at the top
        
        # Attempt to find enemy pets by looking for pet links that are NOT in the strategy slots
        # This is hard, but let's try to grab ALL pet links and filter
        
        # Better: Look for the script and see if it mentions enemy abilities
        
        # 1. Extract Player Pets (Same logic as before)
        all_pets = []
        pet_cards = soup.find_all(class_='bt_petname')
        seen_pets = set()
        for card in pet_cards:
            link = card.find('a', class_='bt_petdetails')
            if link:
                pet_name = link.get_text().strip()
                if pet_name not in seen_pets:
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
                    
                    if len(all_pets) >= 3:
                        break
        
        strategy['pet_slots'] = [[pet] for pet in all_pets[:3]]
        
        # 2. Extract Script
        tooltip = soup.find(id='td_tooltip')
        if tooltip:
            script_text = tooltip.get_text().strip()
            lines = script_text.split('\n')
            clean_lines = [l for l in lines if "Click the button" not in l and "wow-petsim" not in l]
            strategy['script'] = '\n'.join(clean_lines).strip()
        
        return strategy

    def save_data(self, filename='strategies_pandaria.json'):
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=2)
        print(f"Saved data to {filename}")

def main():
    scraper = XuFuScraper()
    
    # Target Pandaria Tamers
    targets = [
        ('Pandaria', 'Tamers', 'Section/21/Tamers'),
    ]
    
    print(f"Starting scrape of {len(targets)} categories...")
    
    for expansion, category, url_suffix in targets:
        scraper.scrape_category(expansion, category, url_suffix)
        
    scraper.save_data()

if __name__ == "__main__":
    main()
