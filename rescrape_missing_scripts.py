"""
Re-scrape Missing Scripts

This script identifies strategy URLs that failed to extract scripts and retries them.
It reads the current variations_with_scripts_final.json and the original strategies_enhanced.json
to find missing variations.

Usage: python3 rescrape_missing_scripts.py
"""

import json
import time
import requests
from bs4 import BeautifulSoup
import re

INPUT_FILE = 'strategies_enhanced.json'
CURRENT_FILE = 'variations_with_scripts_final.json'
OUTPUT_FILE = 'missing_scripts.json'
BASE_URL = "https://www.wow-petguide.com"

def get_soup(url):
    time.sleep(0.2)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers, timeout=10)
    return BeautifulSoup(response.content, 'html.parser')

def extract_script(soup):
    """Extract script from hidden span"""
    script_span = soup.find('span', id='td_script_content')
    if script_span:
        script_text = script_span.get_text()
        script_text = script_text.replace("-----BEGIN PET BATTLE SCRIPT-----", "")
        script_text = script_text.replace("-----END PET BATTLE SCRIPT-----", "").strip()
        return script_text
    return None

def find_missing_urls():
    """Find all strategy URLs that exist but don't have scripts"""
    print("Loading current data...")
    
    # Load completed scrape
    with open(CURRENT_FILE, 'r') as f:
        completed = json.load(f)
    
    # Collect all URLs we've processed
    processed_urls = set()
    for encounter_name, variations in completed.items():
        for var in variations:
            if 'url' in var:
                processed_urls.add(var['url'])
    
    print(f"Found {len(processed_urls)} processed URLs with scripts")
    
    # Now find all URLs from the main encounter pages
    print("Finding all strategy URLs from encounter pages...")
    
    with open(INPUT_FILE, 'r') as f:
        encounters_data = json.load(f)
    
    all_encounter_urls = []
    for expansion, categories in encounters_data.items():
        for category, enc_list in categories.items():
            for enc in enc_list:
                all_encounter_urls.append({
                    'name': enc['encounter_name'],
                    'url': enc['url']
                })
    
    print(f"Found {len(all_encounter_urls)} encounters to check")
    
    # For each encounter, fetch all strategy links
    missing = {}
    
    for i, enc in enumerate(all_encounter_urls):
        print(f"[{i+1}/{len(all_encounter_urls)}] Checking: {enc['name']}")
        
        try:
            soup = get_soup(enc['url'])
            
            # Find all strategy links
            strategy_links = set()
            for a in soup.find_all('a', href=True):
                href = a['href']
                if '/Strategy/' in href:
                    if not href.startswith('http'):
                        href = f"{BASE_URL}{href}"
                    strategy_links.add(href)
            
            # Find which ones are missing
            missing_links = strategy_links - processed_urls
            
            if missing_links:
                missing[enc['name']] = list(missing_links)
                print(f"  Found {len(missing_links)} missing URLs")
        
        except Exception as e:
            print(f"  ! Error: {e}")
    
    return missing

def rescrape_missing(missing_urls):
    """Re-scrape the missing URLs"""
    results = {}
    
    total = sum(len(urls) for urls in missing_urls.values())
    count = 0
    
    for encounter_name, urls in missing_urls.items():
        print(f"\nRe-scraping {encounter_name}...")
        results[encounter_name] = []
        
        for url in urls:
            count += 1
            print(f"  [{count}/{total}] {url}")
            
            try:
                soup = get_soup(url)
                script = extract_script(soup)
                
                if script:
                    # Also extract team
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
                    
                    results[encounter_name].append({
                        "url": url,
                        "team": unique_ids[:3],
                        "script": script
                    })
                    print(f"    ✓ Found script ({len(script)} chars)")
                else:
                    print(f"    ✗ Still no script")
            
            except Exception as e:
                print(f"    ! Error: {e}")
    
    return results

def main():
    print("=== Re-scraping Missing Scripts ===\n")
    
    # Find missing URLs
    missing = find_missing_urls()
    
    print(f"\nTotal encounters with missing scripts: {len(missing)}")
    total_missing = sum(len(urls) for urls in missing.values())
    print(f"Total missing URLs: {total_missing}")
    
    if total_missing == 0:
        print("\n✓ No missing scripts!")
        return
    
    # Save the list
    with open('missing_urls.json', 'w') as f:
        json.dump(missing, f, indent=2)
    print(f"\nSaved missing URLs to missing_urls.json")
    
    # Ask to proceed
    print(f"\nReady to re-scrape {total_missing} URLs.")
    response = input("Proceed? (y/n): ")
    
    if response.lower() == 'y':
        results = rescrape_missing(missing)
        
        # Save results
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✓ Saved results to {OUTPUT_FILE}")
    else:
        print("Cancelled.")

if __name__ == "__main__":
    main()
