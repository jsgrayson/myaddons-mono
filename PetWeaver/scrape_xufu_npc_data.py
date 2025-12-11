#!/usr/bin/env python3
"""
Scrape Xu-Fu NPC pages directly to get NPC pet teams, stats, and AI.
The strategies_enhanced.json only has player strategies - need to get NPC data from actual pages.
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time

class XuFuNPCScraper:
    def __init__(self):
        self.base_url = "https://www.wow-petguide.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def scrape_encounter_npc_data(self, encounter_url):
        """Scrape NPC pet data from an encounter page"""
        try:
            time.sleep(1.5)  # Respectful delay
            response = self.session.get(encounter_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            npc_pets = []
            
            # Look for enemy pet information
            # Xu-Fu shows enemy pets in a specific section
            enemy_section = soup.find('div', class_='enemy-team') or soup.find('h3', string=re.compile(r'Enemy Team', re.I))
            
            if enemy_section:
                # Find pet cards in enemy section
                pet_cards = soup.find_all('div', class_='pet-card')
                
                for card in pet_cards[:3]:  # NPC teams have max 3 pets
                    pet_name_elem = card.find('a', class_='bt_petdetails')
                    if not pet_name_elem:
                        continue
                    
                    pet_name = pet_name_elem.get_text().strip()
                    pet_href = pet_name_elem.get('href', '')
                    
                    # Extract species ID from URL
                    species_id = 0
                    match = re.search(r'/Pet/(\d+)/', pet_href)
                    if match:
                        species_id = int(match.group(1))
                    
                    # Extract abilities
                    abilities = []
                    ability_links = card.find_all('a', href=re.compile(r'/Ability/'))
                    for idx, ab_link in enumerate(ability_links[:3]):
                        ab_name = ab_link.get_text().strip()
                        ab_href = ab_link.get('href', '')
                        ab_id_match = re.search(r'/Ability/(\d+)/', ab_href)
                        if ab_id_match:
                            abilities.append({
                                'id': int(ab_id_match.group(1)),
                                'name': ab_name,
                                'slot': idx + 1
                            })
                    
                    npc_pets.append({
                        'name': pet_name,
                        'species_id': species_id,
                        'abilities': abilities,
                        'level': 25,
                        'quality': 'rare',
                        'health': 1546,  # Default rare stats
                        'power': 273,
                        'speed': 273
                    })
            
            return npc_pets
            
        except Exception as e:
            print(f"Error scraping {encounter_url}: {e}")
            return []
    
    def process_all_encounters(self):
        """Process encounters from strategies_enhanced.json"""
        
        with open('strategies_enhanced.json', 'r') as f:
            xufu_data = json.load(f)
        
        encounters = {}
        count = 0
        visited_urls = set()
        
        for expansion, categories in xufu_data.items():
            for category, encounter_list in categories.items():
                for encounter_data in encounter_list:  # Process all
                    encounter_name = encounter_data['encounter_name']
                    encounter_url = encounter_data['url']
                    
                    if encounter_url in visited_urls:
                        continue
                    visited_urls.add(encounter_url)
                    
                    print(f"Scraping {encounter_name}...")
                    npc_pets = self.scrape_encounter_npc_data(encounter_url)
                    
                    if npc_pets:
                        enc_id = encounter_name.lower().replace(' ', '_').replace("'", '')
                        enc_id = re.sub(r'[^a-z0-9_]', '', enc_id)
                        
                        encounters[enc_id] = {
                            'name': encounter_name,
                            'note': f"NPC data from Xu-Fu - {expansion} {category}",
                            'npc_pets': npc_pets
                        }
                        count += 1
                        print(f"Scraped {count} encounters so far...")
                        
                        # Save incrementally
                        if count % 10 == 0:
                            print("Saving progress...")
                            with open('npc_encounters.json', 'w') as f:
                                json.dump(encounters, f, indent=2)
                        
        return encounters

def main():
    print("Scraping NPC data from Xu-Fu pages...")
    print("="*60)
    
    scraper = XuFuNPCScraper()
    encounters = scraper.process_all_encounters()
    
    # Save
    with open('npc_encounters.json', 'w') as f:
        json.dump(encounters, f, indent=2)
    
    print(f"\n✅ Scraped {len(encounters)} NPC encounters")
    print(f"Saved to npc_encounters.json")

if __name__ == "__main__":
    main()
