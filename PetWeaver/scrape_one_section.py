"""
One-section-at-a-time scraper. Reliable and resumable.
Usage: python3 scrape_one_section.py "The War Within" "World Quests"
"""

import json
import time
import sys
from playwright.sync_api import sync_playwright
from pathlib import Path

def teams_to_slots(teams):
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

def scrape_section(expansion, category, section_url):
    """Scrape one section"""
    base_url = "https://www.wow-petguide.com"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f"\n{'='*60}")
        print(f"{expansion} - {category}")
        print(f"{'='*60}\n")
        
        # Get encounter list
        page.goto(base_url + section_url, wait_until="domcontentloaded", timeout=60000)
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
        print(f"Found {len(encounters)} encounters\n")
        
        results = []
        successful = 0
        
        for i, enc in enumerate(encounters, 1):
            try:
                enc_url = enc['url'] if enc['url'].startswith('http') else base_url + enc['url']
                page.goto(enc_url, wait_until="domcontentloaded", timeout=60000)
                time.sleep(1.5)
                
                # Click alternatives
                page.wait_for_selector('text="Browse all alternatives"', timeout=10000)
                page.click('text="Browse all alternatives"', timeout=10000)
                page.wait_for_selector('#alternatives_window', timeout=10000)
                time.sleep(1)
                
                # Scroll
                page.evaluate("""
                    const modal = document.getElementById('alternatives_window');
                    if (modal) modal.scrollTop = modal.scrollHeight;
                """)
                time.sleep(0.5)
                
                # Extract
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
                page.keyboard.press('Escape')
                time.sleep(0.3)
                
                pet_slots = teams_to_slots(teams)
                
                results.append({
                    'encounter_name': enc['name'],
                    'url': enc_url,
                    'strategies': [{'pet_slots': pet_slots}],
                    'team_count': len(teams)
                })
                
                if len(teams) > 0:
                    successful += 1
                    print(f"✓ [{i}/{len(encounters)}] {enc['name']}: {len(teams)} teams")
                else:
                    print(f"✗ [{i}/{len(encounters)}] {enc['name']}: NO DATA")
                
                time.sleep(2)
                
            except Exception as e:
                print(f"✗ [{i}/{len(encounters)}] {enc['name']}: ERROR")
                results.append({
                    'encounter_name': enc['name'],
                    'url': enc_url if 'enc_url' in locals() else '',
                    'error': str(e)
                })
        
        browser.close()
        
        print(f"\n{'='*60}")
        print(f"Complete: {successful}/{len(encounters)} successful")
        print(f"{'='*60}\n")
        
        return results

if __name__ == "__main__":
    SECTIONS = {
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
    
    if len(sys.argv) == 3:
        # Scrape specific section
        expansion = sys.argv[1]
        category = sys.argv[2]
        
        if expansion not in SECTIONS or category not in SECTIONS[expansion]:
            print(f"Invalid section: {expansion} - {category}")
            sys.exit(1)
        
        results = scrape_section(expansion, category, SECTIONS[expansion][category])
        
        # Save to file
        filename = f"section_{expansion.replace(' ', '_')}_{category.replace(' ', '_').replace('&', 'and')}.json"
        with open(filename, 'w') as f:
            json.dump({
                'expansion': expansion,
                'category': category,
                'encounters': results
            }, f, indent=2)
        
        print(f"Saved to {filename}")
    else:
        print("Available sections:")
        for exp, cats in SECTIONS.items():
            print(f"\n{exp}:")
            for cat in cats:
                print(f"  - {cat}")
        print(f"\nUsage: python3 {sys.argv[0]} '<expansion>' '<category>'")
        print(f"Example: python3 {sys.argv[0]} 'The War Within' 'World Quests'")
