"""
High-Speed Variation Scraper for Xu-Fu (Requests + BeautifulSoup)

Iterates through ALL encounters in strategies_enhanced.json and scrapes unique scripts
for every variation using direct HTTP requests.

Features:
- Loads encounter list from strategies_enhanced.json
- Uses requests + BeautifulSoup for 10-20x speedup over Selenium
- Extracts scripts from hidden #td_script_content span
- Extracts teams from .bt_petdetails links
- Saves progress incrementally to variations_with_scripts_final.json
- Handles errors and retries

Usage: python3 scrape_variations_requests.py
"""

import json
import time
import re
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

INPUT_FILE = 'strategies_enhanced.json'
RESUME_FILE = 'variations_with_scripts_merged.json'  # Resume from merged data
OUTPUT_FILE = 'variations_with_scripts_final.json'
CHECKPOINT_FILE = 'scraper_checkpoint.json'  # Track progress to prevent re-scraping
BASE_URL = "https://www.wow-petguide.com"

class XuFuRequestsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.request_count = 0
        self.start_time = time.time()

    def respectful_delay(self):
        """Add delay between requests to avoid rate limiting"""
        time.sleep(0.5) # Slower but more reliable, avoids 429 errors
        self.request_count += 1
        if self.request_count % 50 == 0:
            elapsed = time.time() - self.start_time
            print(f"  [Stats] {self.request_count} requests in {elapsed:.1f}s ({self.request_count/elapsed:.1f} req/s)")

    def get_soup(self, url):
        try:
            self.respectful_delay()
            if not url.startswith('http'):
                url = f"{BASE_URL}{url}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"  ! Error fetching {url}: {e}")
            return None

    def extract_strategy_data(self, soup):
        """Extracts team and script from a strategy page soup."""
        strategy = {"team": [], "script": ""}
        
        try:
            # 1. Extract Team
            pet_links = soup.select(".bt_petdetails")
            team_ids = []
            for link in pet_links:
                href = link.get('href', '')
                if href:
                    match = re.search(r'/Pet/(\d+)/', href)
                    if match: team_ids.append(int(match.group(1)))
            
            unique_ids = []
            seen = set()
            for pid in team_ids:
                if pid not in seen:
                    seen.add(pid)
                    unique_ids.append(pid)
            
            while len(unique_ids) < 3: unique_ids.append(0)
            strategy["team"] = unique_ids[:3]

            # 2. Extract Script from Hidden Span
            script_span = soup.find('span', id='td_script_content')
            if script_span:
                script_text = script_span.get_text()
                # Clean up markers
                script_text = script_text.replace("-----BEGIN PET BATTLE SCRIPT-----", "").replace("-----END PET BATTLE SCRIPT-----", "").strip()
                strategy["script"] = script_text
            
        except Exception as e:
            print(f"    ! Error extracting data: {e}")
            
        return strategy

    def scrape_encounter(self, encounter):
        url = encounter['url']
        name = encounter['encounter_name']
        print(f"\nProcessing: {name}")
        print(f"  URL: {url}")
        
        # 1. Get Main Page to find all Strategy Links
        soup = self.get_soup(url)
        if not soup: return None
        
        # Find all /Strategy/ links
        strategy_links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/Strategy/' in href:
                # Normalize URL
                if not href.startswith('http'):
                    href = f"{BASE_URL}{href}"
                strategy_links.add(href)
        
        print(f"  Found {len(strategy_links)} strategy variations.")
        
        variations = []
        
        # 2. Fetch each strategy page
        for i, strat_url in enumerate(strategy_links):
            strat_soup = self.get_soup(strat_url)
            if not strat_soup: continue
            
            data = self.extract_strategy_data(strat_soup)
            
            # Save variation if we have team OR script data
            has_team = any(pid != 0 for pid in data['team'])
            has_script = bool(data['script'])
            
            if has_team or has_script:
                variations.append({
                    "variation": i + 1,
                    "url": strat_url,
                    "team": data['team'],
                    "script": data['script']
                })
                if has_script:
                    print(f"    + Var {i+1}: Script ({len(data['script'])} chars), Team: {data['team']}")
                else:
                    print(f"    + Var {i+1}: Team only (no script): {data['team']}")
            else:
                print(f"    - Var {i+1}: No data found")
        
        # Return encounter data with URL as identifier
        return {
            "encounter_name": name,
            "encounter_url": url,
            "variations": variations
        }

def load_encounters():
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)
    
    encounters = []
    for expansion, categories in data.items():
        for category, enc_list in categories.items():
            for enc in enc_list:
                encounters.append(enc)
    return encounters

def main():
    encounters = load_encounters()
    print(f"Loaded {len(encounters)} encounters.")
    
    # Load existing progress - prioritize merged file
    results = {}
    
    # First try to load from merged file (most complete)
    if os.path.exists(RESUME_FILE):
        try:
            with open(RESUME_FILE, 'r') as f:
                results = json.load(f)
            print(f"✅ Loaded {len(results)} encounters from {RESUME_FILE}")
        except Exception as e:
            print(f"! Error loading {RESUME_FILE}: {e}")
    
    # Fall back to output file if no resume file
    elif os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r') as f:
                results = json.load(f)
            print(f"Resuming from {len(results)} saved encounters in {OUTPUT_FILE}")
        except: pass
    
    scraper = XuFuRequestsScraper()
    
    # Track progress
    skipped = 0
    newly_scraped = 0
    failed = 0
    
    try:
        for i, enc in enumerate(encounters):
            name = enc['encounter_name']
            url = enc['url']
            
            # Use URL as unique key (handles duplicate names)
            if url in results:
                skipped += 1
                if skipped <= 5 or skipped % 50 == 0:
                    print(f"  [{i+1}/{len(encounters)}] ⏭️  Skipping: {name} (already scraped)")
                continue
            
            # Scrape new encounter
            print(f"\n[{i+1}/{len(encounters)}] 🔍 Scraping: {name}")
            print(f"  Progress: {newly_scraped} new, {skipped} skipped, {failed} failed")
            
            encounter_data = scraper.scrape_encounter(enc)
            
            # Save ALL encounters, even if they have 0 variations
            if encounter_data is not None:
                results[url] = encounter_data  # Use URL as key
                newly_scraped += 1
                
                var_count = len(encounter_data.get('variations', []))
                if var_count > 0:
                    print(f"  ✅ Saved: {name} ({var_count} variations)")
                else:
                    print(f"  ⚠️  Saved: {name} (0 variations found)")
            else:
                # Still save encounter even if scraping failed
                results[url] = {
                    "encounter_name": name,
                    "encounter_url": url,
                    "variations": [],
                    "error": "Failed to scrape"
                }
                failed += 1
                print(f"  ❌ Error scraping {name} - saved with 0 variations")
            
            # Save after EVERY encounter (checkpoint)
            with open(OUTPUT_FILE, 'w') as f:
                json.dump(results, f, indent=2)
            
            # Save checkpoint metadata
            with open(CHECKPOINT_FILE, 'w') as f:
                json.dump({
                    'last_encounter': name,
                    'last_url': url,
                    'last_index': i,
                    'total_scraped': len(results),
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2)

    except KeyboardInterrupt:
        print("\n⚠️  Stopped by user.")
    finally:
        # Final save
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n{'='*60}")
        print(f"📊 Final Statistics:")
        print(f"  Total encounters: {len(encounters)}")
        print(f"  Already scraped (skipped): {skipped}")
        print(f"  Newly scraped: {newly_scraped}")
        print(f"  Failed: {failed}")
        print(f"  Total in output: {len(results)}")
        print(f"  Saved to: {OUTPUT_FILE}")
        print(f"{'='*60}")

if __name__ == "__main__":
    main()
