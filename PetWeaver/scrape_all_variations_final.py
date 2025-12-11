"""
Full Variation Scraper for Xu-Fu (Production)

Iterates through ALL encounters in strategies_enhanced.json and scrapes unique scripts
for every variation using the "Hidden Span + Arrow Navigation" method.

Features:
- Loads encounter list from strategies_enhanced.json
- Uses Selenium with JS clicks to bypass overlays
- Extracts scripts from hidden #td_script_content span
- Saves progress incrementally to variations_with_scripts_final.json
- Handles errors and retries

Usage: python3 scrape_all_variations_final.py
"""

import json
import time
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

INPUT_FILE = 'strategies_enhanced.json'
OUTPUT_FILE = 'variations_with_scripts_final.json'

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('window-size=1920,1080')
    # options.add_argument('--headless') # Keep visible for now to monitor
    
    # Block images/fonts for speed
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.fonts": 2,
    }
    options.add_experimental_option("prefs", prefs)
    
    return webdriver.Chrome(options=options)

def load_encounters():
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)
    
    encounters = []
    for expansion, categories in data.items():
        for category, enc_list in categories.items():
            for enc in enc_list:
                encounters.append(enc)
    return encounters

def extract_current_strategy(driver):
    """Extracts the currently visible team and script."""
    strategy = {"team": [], "script": ""}
    
    try:
        # 1. Extract Team
        pet_links = driver.find_elements(By.CSS_SELECTOR, ".bt_petdetails")
        team_ids = []
        for link in pet_links:
            href = link.get_attribute('href')
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
        script_text = ""
        try:
            script_span = driver.find_element(By.ID, "td_script_content")
            script_text = script_span.get_attribute('textContent')
            script_text = script_text.replace("-----BEGIN PET BATTLE SCRIPT-----", "").replace("-----END PET BATTLE SCRIPT-----", "").strip()
        except: pass
        
        strategy["script"] = script_text

    except Exception as e:
        print(f"    ! Error extracting strategy: {e}")
        
    return strategy

def scrape_encounter(driver, encounter):
    url = encounter['url']
    name = encounter['encounter_name']
    print(f"\nProcessing: {name} ({url})")
    
    try:
        driver.get(url)
        # Wait for body
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(1.5) # Initial load
        
        variations = []
        seen_scripts = set()
        
        # Max 50 variations per encounter to prevent infinite loops
        for i in range(50):
            # 1. Extract
            strat = extract_current_strategy(driver)
            
            # Save if valid and new script (or if it's the first one)
            # Note: Some variations might share scripts, but we want to capture the team mapping.
            # However, to avoid duplicates if the arrow doesn't work, we check if team+script is identical?
            # Actually, let's just check if we've seen this exact team+script combo.
            
            combo_key = f"{strat['team']}-{len(strat['script'])}"
            
            # If script is empty, skip
            if not strat['script']:
                print(f"    - Var {i+1}: Empty script")
            else:
                variations.append({
                    "variation": i + 1,
                    "team": strat["team"],
                    "script": strat["script"]
                })
                print(f"    + Var {i+1}: Captured (Team: {strat['team']}, Script: {len(strat['script'])} chars)")

            # 2. Click Next
            try:
                next_arrow = driver.find_element(By.XPATH, "//div[contains(@class, 'alts_opener_mid')]/following-sibling::div[contains(@class, 'alts_opener_side')]//a")
                
                if not next_arrow.is_displayed():
                    print("    -> End (arrow hidden)")
                    break
                
                # Check href to see if we are looping back to start? 
                # Xu-Fu usually cycles. We should stop if we see a team we've already captured?
                # Let's stop if we encounter the exact same team composition as the first one (after the first iteration)
                if i > 0 and strat['team'] == variations[0]['team']:
                     print("    -> Looped back to start")
                     break

                driver.execute_script("arguments[0].click();", next_arrow)
                time.sleep(1.0) # Wait for update
                
            except Exception as e:
                print(f"    -> End (arrow not found): {e}")
                break
        
        return variations

    except Exception as e:
        print(f"  !!! Error scraping {name}: {e}")
        return []

def main():
    encounters = load_encounters()
    print(f"Loaded {len(encounters)} encounters.")
    
    # Load existing progress
    results = {}
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r') as f:
                results = json.load(f)
            print(f"Resuming from {len(results)} saved encounters.")
        except: pass
    
    driver = get_driver()
    
    try:
        for i, enc in enumerate(encounters):
            name = enc['encounter_name']
            if name in results:
                continue
                
            print(f"[{i+1}/{len(encounters)}] Scrape: {name}")
            vars_data = scrape_encounter(driver, enc)
            
            if vars_data:
                results[name] = vars_data
                
                # Save every 5 encounters
                if len(results) % 5 == 0:
                    with open(OUTPUT_FILE, 'w') as f:
                        json.dump(results, f, indent=2)
                    print(f"  >> Saved progress ({len(results)} encounters)")
            else:
                print(f"  >> No variations found for {name}")

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        # Final save
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Final save to {OUTPUT_FILE}")
        driver.quit()

if __name__ == "__main__":
    main()
