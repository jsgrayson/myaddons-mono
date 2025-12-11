#!/usr/bin/env python3
"""
Wowhead Encounter Scraper for The Codex
Scrapes encounter data from Wowhead's encounter journal guides
"""

import sys
import json
import time
import requests
from bs4 import BeautifulSoup

class WowheadEncounterScraper:
    BASE_URL = "https://www.wowhead.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def scrape_encounter(self, guide_url):
        """
        Scrape a single encounter from Wowhead guide page
        Args:
            guide_url: e.g., "/guide/raids/nerub-ar-palace/queen-ansurek"
        Returns:
            dict with encounter data
        """
        full_url = f"{self.BASE_URL}{guide_url}"
        print(f"Fetching: {full_url}")
        
        try:
            response = self.session.get(full_url, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return {"error": str(e), "url": full_url}
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        encounter = {
            "url": full_url,
            "overview": "",
            "abilities": [],
            "phases": [],
            "role_notes": {
                "tank": [],
                "healer": [],
                "dps": []
            }
        }
        
        # Extract overview (usually in first paragraphs)
        overview_section = soup.find('div', {'class': 'text'})
        if overview_section:
            paragraphs = overview_section.find_all('p', limit=3)
            encounter["overview"] = " ".join([p.get_text(strip=True) for p in paragraphs])[:500]
        
        # Extract abilities from encounter journal sections
        # Wowhead uses structured divs with ability information
        ability_sections = soup.find_all(['h2', 'h3'], string=lambda text: text and 'abilit' in text.lower())
        for header in ability_sections:
            # Find abilities list after header
            next_elem = header.find_next_sibling()
            while next_elem and next_elem.name in ['ul', 'p', 'div']:
                if next_elem.name == 'ul':
                    for li in next_elem.find_all('li'):
                        ability_text = li.get_text(strip=True)
                        if ability_text:
                            encounter["abilities"].append(ability_text)
                next_elem = next_elem.find_next_sibling()
                if next_elem and next_elem.name in ['h2', 'h3']:
                    break
        
        # Extract phases
        phase_headers = soup.find_all(['h2', 'h3'], string=lambda text: text and 'phase' in text.lower())
        for phase_header in phase_headers:
            phase_name = phase_header.get_text(strip=True)
            phase_content = []
            
            next_elem = phase_header.find_next_sibling()
            while next_elem and next_elem.name not in ['h2', 'h3']:
                if next_elem.name in ['p', 'ul']:
                    phase_content.append(next_elem.get_text(strip=True))
                next_elem = next_elem.find_next_sibling()
            
            encounter["phases"].append({
                "name": phase_name,
                "description": " ".join(phase_content)[:300]
            })
        
        # Extract role-specific notes
        for role in ['tank', 'healer', 'dps', 'damage dealer']:
            role_headers = soup.find_all(['h2', 'h3', 'h4'], 
                                        string=lambda text: text and role in text.lower())
            for header in role_headers:
                next_list = header.find_next(['ul', 'p'])
                if next_list:
                    note_text = next_list.get_text(strip=True)
                    if note_text:
                        role_key = 'dps' if role == 'damage dealer' else role
                        encounter["role_notes"][role_key].append(note_text[:200])
        
        print(f"  ✓ Success! Found {len(encounter['abilities'])} abilities")
        return encounter

# TWW Encounter Definitions (Wowhead URLs)
ENCOUNTERS = {
    "raids": {
        "Nerub-ar Palace": [
            {"name": "Ulgrax the Devourer", "url": "/guide/raids/nerub-ar-palace/ulgrax-the-devourer"},
            {"name": "The Bloodbound Horror", "url": "/guide/raids/nerub-ar-palace/bloodbound-horror"},
            {"name": "Sikran", "url": "/guide/raids/nerub-ar-palace/sikran"},
            {"name": "Rasha'nan", "url": "/guide/raids/nerub-ar-palace/rashanan"},
            {"name": "Broodtwister Ovi'nax", "url": "/guide/raids/nerub-ar-palace/broodtwister-ovinax"},
            {"name": "Nexus-Princess Ky'veza", "url": "/guide/raids/nerub-ar-palace/nexus-princess-kyveza"},
            {"name": "The Silken Court", "url": "/guide/raids/nerub-ar-palace/silken-court"},
            {"name": "Queen Ansurek", "url": "/guide/raids/nerub-ar-palace/queen-ansurek"}
        ]
    },
    "dungeons": {
        "Ara-Kara, City of Echoes": [
            {"name": "Avanoxx", "url": "/guide/dungeons/ara-kara-city-of-echoes/avanoxx"},
            {"name": "Anub'zekt", "url": "/guide/dungeons/ara-kara-city-of-echoes/anubzekt"},
            {"name": "Ki'katal the Harvester", "url": "/guide/dungeons/ara-kara-city-of-echoes/kikatal-the-harvester"}
        ],
        "City of Threads": [
            {"name": "Orator Krix'vizk", "url": "/guide/dungeons/city-of-threads/orator-krixvizk"},
            {"name": "Fangs of the Queen", "url": "/guide/dungeons/city-of-threads/fangs-of-the-queen"},
            {"name": "The Coaglamation", "url": "/guide/dungeons/city-of-threads/coaglamation"},
            {"name": "Izo, the Grand Splicer", "url": "/guide/dungeons/city-of-threads/izo"}
        ]
    }
}

def scrape_all():
    scraper = WowheadEncounterScraper()
    results = {"raids": {}, "dungeons": {}}
    
    total = sum(len(bosses) for instances in ENCOUNTERS.values() for bosses in instances.values())
    current = 0
    
    print(f"Starting scrape of {total} encounters from Wowhead...")
    
    for category in ["raids", "dungeons"]:
        for instance_name, bosses in ENCOUNTERS[category].items():
            print(f"\n{'='*60}")
            print(f"Instance: {instance_name}")
            print(f"{'='*60}")
            
            results[category][instance_name] = {"bosses": []}
            
            for boss in bosses:
                current += 1
                print(f"\n[{current}/{total}] {boss['name']}...")
                
                encounter_data = scraper.scrape_encounter(boss['url'])
                encounter_data["display_name"] = boss["name"]
                encounter_data["instance"] = instance_name
                encounter_data["category"] = category
                
                results[category][instance_name]["bosses"].append(encounter_data)
                
                time.sleep(2)  # Rate limiting
    
    # Save
    output_file = "/Users/jgrayson/Documents/holocron/data/wowhead_encounters.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"✓ Complete! Saved to {output_file}")
    print(f"{'='*60}")

if __name__ == "__main__":
    scrape_all()
