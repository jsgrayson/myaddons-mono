"""
Fill in Team Data for No-Script Variations

This script scans the existing variations_with_scripts_final.json and identifies
variations that don't have scripts but should have team data. It then scrapes
just those variations to add the team compositions.
"""

import json
import time
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

INPUT_FILE = 'variations_with_scripts_final.json'
OUTPUT_FILE = 'variations_with_scripts_final.json'
BASE_URL = "https://www.wow-petguide.com"

class TeamOnlyScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.request_count = 0
        
    def get_soup(self, url):
        try:
            time.sleep(0.2)  # Faster rate (5 req/sec vs 2 req/sec)
            self.request_count += 1
            
            if self.request_count % 50 == 0:
                print(f"    [Progress: {self.request_count} requests]")
            
            if not url.startswith('http'):
                url = f"{BASE_URL}{url}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"  ! Error fetching {url}: {e}")
            return None
    
    def extract_team(self, soup):
        """Extract just team data from strategy page."""
        team_ids = []
        try:
            pet_links = soup.select(".bt_petdetails")
            for link in pet_links:
                href = link.get('href', '')
                if href:
                    match = re.search(r'/Pet/(\d+)/', href)
                    if match:
                        team_ids.append(int(match.group(1)))
            
            # Remove duplicates while preserving order
            unique_ids = []
            seen = set()
            for pid in team_ids:
                if pid not in seen:
                    seen.add(pid)
                    unique_ids.append(pid)
            
            # Pad to 3 pets
            while len(unique_ids) < 3:
                unique_ids.append(0)
            
            return unique_ids[:3]
        except Exception as e:
            print(f"    ! Error extracting team: {e}")
            return [0, 0, 0]

def main():
    print("Loading existing data...")
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)
    
    scraper = TeamOnlyScraper()
    
    # Find all variations without scripts AND without teams
    no_script_variations = []
    
    for encounter_url, encounter_data in data.items():
        encounter_name = encounter_data['encounter_name']
        variations = encounter_data.get('variations', [])
        
        for i, var in enumerate(variations):
            var_url = var.get('url', '').strip()
            var_script = var.get('script', '').strip()
            var_team = var.get('team', [0, 0, 0])
            
            # Skip if has script, no URL, or already has team
            if var_script:
                continue
            if not var_url:
                continue
            if any(pid != 0 for pid in var_team):
                continue
            
            # This variation needs team data
            no_script_variations.append({
                'encounter_url': encounter_url,
                'encounter_name': encounter_name,
                'variation_index': i,
                'variation_url': var_url,
                'current_team': var_team
            })
    
    print(f"\nFound {len(no_script_variations)} variations without scripts")
    
    if len(no_script_variations) == 0:
        print("✅ All variations already have complete data!")
        return
    
    # Ask for confirmation
    print(f"\nWill scrape team data for {len(no_script_variations)} variations.")
    print("This will take approximately {:.1f} minutes...".format(len(no_script_variations) * 0.5 / 60))
    
    updated_count = 0
    skipped_count = 0
    
    for i, var_info in enumerate(no_script_variations):
        print(f"\n[{i+1}/{len(no_script_variations)}] {var_info['encounter_name']}")
        print(f"  URL: {var_info['variation_url'][:80]}")
        
        # Scrape the team
        soup = scraper.get_soup(var_info['variation_url'])
        if not soup:
            print(f"  ❌ Failed to fetch page")
            continue
        
        team = scraper.extract_team(soup)
        
        if any(pid != 0 for pid in team):
            # Verify we're updating the right variation by matching URL
            enc_url = var_info['encounter_url']
            var_idx = var_info['variation_index']
            
            # Double-check the URL matches
            if data[enc_url]['variations'][var_idx]['url'] == var_info['variation_url']:
                data[enc_url]['variations'][var_idx]['team'] = team
                updated_count += 1
                print(f"  ✅ Updated team: {team} ✓ URL verified")
            else:
                print(f"  ⚠️  URL mismatch! Skipping to avoid data corruption")
                continue
            
            # Save progress every 10 updates
            if updated_count % 10 == 0:
                with open(OUTPUT_FILE, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"  💾 Saved progress ({updated_count} updates)")
        else:
            print(f"  ⚠️  No team data found")
    
    # Final save
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"📊 Final Statistics:")
    print(f"  No-script variations found: {len(no_script_variations)}")
    print(f"  Teams added: {updated_count}")
    print(f"  Already had teams (skipped): {skipped_count}")
    print(f"  Saved to: {OUTPUT_FILE}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
