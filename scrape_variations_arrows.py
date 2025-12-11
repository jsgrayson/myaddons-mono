"""
Arrow-Based Variation Scraper for Xu-Fu (Hidden Script Fix)

This scraper extracts unique scripts by cycling through strategies using the "Next" arrow.
It handles:
1. Navigating to the encounter.
2. Extracting the script directly from the hidden #td_script_content span.
3. Extracting the current team.
4. Clicking the "Next" arrow (using JS click).
5. Repeating until all variations are captured.

Usage: python3 scrape_variations_arrows.py
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('window-size=1920,1080')
    
    return webdriver.Chrome(options=options)

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
            # Use textContent to get hidden text
            script_span = driver.find_element(By.ID, "td_script_content")
            script_text = script_span.get_attribute('textContent')
            
            # Clean up the "BEGIN/END PET BATTLE SCRIPT" markers
            script_text = script_text.replace("-----BEGIN PET BATTLE SCRIPT-----", "").replace("-----END PET BATTLE SCRIPT-----", "").strip()
            
        except Exception as e:
            # Fallback to visible text if span not found
            pass
        
        strategy["script"] = script_text

    except Exception as e:
        print(f"  ! Error extracting strategy: {e}")
        
    return strategy

def scrape_encounter_arrows(driver, url, name):
    print(f"\n🚀 Processing: {name}")
    driver.get(url)
    time.sleep(2)
    
    variations = []
    seen_scripts = set()
    
    # Limit to 15 variations for testing
    for i in range(15):
        # 1. Extract Current
        strat = extract_current_strategy(driver)
        
        if strat["script"] and strat["script"] not in seen_scripts:
            variations.append({
                "variation": i + 1,
                "team": strat["team"],
                "script": strat["script"]
            })
            seen_scripts.add(strat["script"])
            print(f"  + Var {i+1}: Captured (Script len: {len(strat['script'])})")
        else:
            print(f"  - Var {i+1}: Duplicate or empty script")

        # 2. Click Next Arrow
        try:
            # CORRECTED SELECTOR: Look for the arrow inside the sibling div
            next_arrow = driver.find_element(By.XPATH, "//div[contains(@class, 'alts_opener_mid')]/following-sibling::div[contains(@class, 'alts_opener_side')]//a")
            
            # Use JS Click to bypass "growl-message" or other overlays
            driver.execute_script("arguments[0].click();", next_arrow)
            
            time.sleep(1.5) # Wait for page update
            
        except Exception as e:
            print(f"  -> End of variations (arrow not found/error): {e}")
            break
            
    return variations

def main():
    driver = get_driver()
    try:
        # Test on Rock Collector
        data = scrape_encounter_arrows(
            driver, 
            "https://www.wow-petguide.com/Encounter/1589/Rock_Collector", 
            "Rock Collector"
        )
        
        print("\nResults:")
        print(json.dumps(data, indent=2))
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
