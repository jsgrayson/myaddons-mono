"""
ULTRA-ROBUST Playwright scraper with retries and error recovery.
Slower but reliable for all 282+ encounters.
"""

import json
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from datetime import datetime

class RobustXuFuScraper:
    def __init__(self):
        self.base_url = "https://www.wow-petguide.com"
        self.categories = {
            "The War Within": {
                "World Quests": "/Section/104/World_Quests",
                "The Undermine": "/Section/110/The_Undermine"
            },
            "Dragonflight": {
                "World Quests": "/Section/97/World_Quests",
                "The Forbidden Reach": "/Section/99/The_Forbidden_Reach",
                "Zaralek Cavern": "/Section/100/Zaralek_Cavern"
            },
            "Shadowlands": {
                "World Quests": "/Section/80/World_Quests",
                "Covenant Adventures": "/Section/85/Covenant_Adventures",
                "Torghast": "/Section/87/Torghast_Tower_of_the_Damned",
                "Family Exorcist": "/Section/89/Family_Exorcist"
            },
            "BfA": {
                "World Quests": "/Section/64/World_Quests",
                "Island Expeditions": "/Section/68/Island_Expeditions",
                "Warfronts": "/Section/69/Warfronts",
                "Family Battler": "/Section/71/Battle_for_Azeroth_Family_Battler",
                "Nazjatar & Mechagon": "/Section/72/Nazjatar_and_Mechagon"
            },
            "Legion": {
                "World Quests": "/Section/49/World_Quests",
                "Family Familiar": "/Section/51/Family_Familiar",
                "Broken Isles": "/Section/48/Broken_Isles_Tamers"
            },
            "Draenor": {
                "Garrison": "/Section/36/Garrison",
                "The Menagerie": "/Section/37/The_Menagerie",
                "Tamers": "/Section/38/Draenor_Tamers"
            },
            "Pandaria": {
                "Spirit Tamers": "/Section/19/Pandaren_Spirit_Tamers",
                "Beasts of Fable": "/Section/20/Beasts_of_Fable",
                "Tamers": "/Section/21/Tamers",
                "Celestial Tournament": "/Section/22/Celestial_Tournament"
            },
            "Dungeons": {
                "Wailing Caverns": "/Section/54/Wailing_Caverns",
                "Deadmines": "/Section/55/Deadmines",
                "Stratholme": "/Section/73/Stratholme",
                "Blackrock Depths": "/Section/74/Blackrock_Depths",
                "Gnomeregan": "/Section/75/Gnomeregan"
            },
            "Misc": {
                "Darkmoon Faire": "/Section/25/Darkmoon_Faire"
            }
        }
    
    def extract_teams_robust(self, page, max_retries=3):
        """Extract teams with retry logic"""
        for attempt in range(max_retries):
            try:
                # Wait for alternatives button
                page.wait_for_selector('text="Browse all alternatives"', timeout=10000)
                page.click('text="Browse all alternatives"', timeout=10000)
                
                # Wait for modal to appear
                page.wait_for_selector('#alternatives_window', timeout=10000)
                time.sleep(1)  # Extra time for modal animation
                
                # Scroll modal
                page.evaluate("""
                    const modal = document.getElementById('alternatives_window');
                    if (modal) {
                        modal.scrollTop = 0;
                        setTimeout(() => { modal.scrollTop = modal.scrollHeight; }, 100);
                    }
                """)
                time.sleep(0.8)  # Wait for scroll
                
                # Extract teams
                teams_json = page.evaluate("""
                    (() => {
                        const table = document.getElementById('alternatives_window');
                        if (!table) return '[]';
                        const rows = table.querySelectorAll('tr');
                        const teams = [];
                        rows.forEach(row => {
                            const petDivs = row.querySelectorAll('td:first-child > div');
                            const team = [];
                            petDivs.forEach(div => {
                                const link = div.querySelector('a');
                                const img = div.querySelector('img');
                                if (link) {
                                    const href = link.getAttribute('href');
                                    let name = '[Unknown]';
                                    let id = 0;
                                    const match = href.match(/\\/Pet\\/(\\d+)\\/(.*)/);
                                    if (match) {
                                        id = parseInt(match[1]);
                                        name = match[2].replace(/_/g, ' ');
                                    }
                                    team.push({ name, id });
                                } else if (img && img.getAttribute('alt') === 'Leveling Pet') {
                                    team.push({ name: '[Empty/Leveling]', id: 0 });
                                }
                            });
                            if (team.length === 3) teams.push(team);
                        });
                        return JSON.stringify(teams);
                    })()
                """)
                
                teams = json.loads(teams_json)
                
                # Close modal with Escape
                page.keyboard.press('Escape')
                time.sleep(0.5)
                
                return teams
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"      Retry {attempt + 1}/{max_retries}: {str(e)[:50]}")
                    time.sleep(2)
                else:
                    print(f"      Failed after {max_retries} attempts")
                    return []
        
        return []
    
    def teams_to_slots(self, teams):
        """Convert teams to pet_slots"""
        if not teams:
            return []
        
        slot1, slot2, slot3 = set(), set(), set()
        for team in teams:
            if len(team) >= 3:
                slot1.add((team[0]['name'], team[0]['id']))
                slot2.add((team[1]['name'], team[1]['id']))
                slot3.add((team[2]['name'], team[2]['id']))
        
        return [
            [{'name': n, 'id': i} for n, i in slot1 if i != 0 or n == '[Empty/Leveling]'],
            [{'name': n, 'id': i} for n, i in slot2 if i != 0 or n == '[Empty/Leveling]'],
            [{'name': n, 'id': i} for n, i in slot3 if i != 0 or n == '[Empty/Leveling]']
        ]
    
    def scrape_all(self):
        """Scrape all encounters with browser restarts"""
        all_data = {}
        total_enc = 0
        total_successful = 0
        encounter_count = 0
        
        with sync_playwright() as p:
            browser = None
            page = None
            
            for expansion, categories in self.categories.items():
                print(f"\n{'='*70}\n{expansion}\n{'='*70}")
                all_data[expansion] = {}
                
                for category, url in categories.items():
                    print(f"\n{category}:")
                    
                    # Restart browser every 20 encounters
                    if encounter_count % 20 == 0:
                        if browser:
                            browser.close()
                            print("  [Restarting browser for stability]")
                        browser = p.chromium.launch(headless=True)
                        page = browser.new_page()
                        time.sleep(2)
                    
                    try:
                        # Get encounter list
                        page.goto(self.base_url + url, wait_until="domcontentloaded", timeout=60000)
                        time.sleep(2)
                        
                        encounters_json = page.evaluate("""
                            (() => {
                                const encs = [];
                                document.querySelectorAll('a[href*="/Encounter/"]').forEach(link => {
                                    const href = link.getAttribute('href');
                                    const name = link.innerText.trim();
                                    if (name && !encs.find(e => e.url === href)) {
                                        encs.push({ name, url: href });
                                    }
                                });
                                return JSON.stringify(encs);
                            })()
                        """)
                        
                        encounters = json.loads(encounters_json)
                        print(f"  Found {len(encounters)} encounters")
                        
                        all_data[expansion][category] = []
                        
                        for i, enc in enumerate(encounters, 1):
                            encounter_count += 1
                            
                            try:
                                # Navigate to encounter
                                enc_url = enc['url'] if enc['url'].startswith('http') else self.base_url + enc['url']
                                page.goto(enc_url, wait_until="domcontentloaded", timeout=60000)
                                time.sleep(2)
                                
                                # Extract teams
                                teams = self.extract_teams_robust(page)
                                pet_slots = self.teams_to_slots(teams)
                                
                                all_data[expansion][category].append({
                                    'encounter_name': enc['name'],
                                    'url': enc_url,
                                    'strategies': [{'pet_slots': pet_slots}],
                                    'team_count': len(teams)
                                })
                                
                                if len(teams) > 0:
                                    total_successful += 1
                                    print(f"    ✓ [{i}/{len(encounters)}] {enc['name']}: {len(teams)} teams")
                                else:
                                    print(f"    ✗ [{i}/{len(encounters)}] {enc['name']}: NO DATA")
                                
                                total_enc += 1
                                
                                # Respectful delay
                                time.sleep(2.5)
                                
                            except Exception as e:
                                print(f"    ✗ [{i}/{len(encounters)}] {enc['name']}: ERROR - {str(e)[:60]}")
                        
                        # Save progress after each category
                        with open('strategies_final.json', 'w') as f:
                            json.dump(all_data, f, indent=2)
                        print(f"  Progress saved ({total_successful}/{total_enc} successful)")
                        
                    except Exception as e:
                        print(f"  Category ERROR: {e}")
            
            if browser:
                browser.close()
        
        print(f"\n{'='*70}")
        print(f"COMPLETE: {total_successful}/{total_enc} encounters successfully scraped")
        print(f"Output: strategies_final.json")

if __name__ == "__main__":
    print("ROBUST XU-FU SCRAPER - ALL ENCOUNTERS")
    print("Estimated time: 30-45 minutes (slower but reliable)")
    print("="*70)
    
    scraper = RobustXuFuScraper()
    scraper.scrape_all()
