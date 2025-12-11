"""
FAST Variation Scraper for Xu-Fu (Refined)

Optimized for speed but reliable:
1. Blocks images/CSS/fonts.
2. Uses 'normal' loading strategy (wait for load event) to ensure JS runs.
3. Explicitly targets the 'Rock Collector' encounter for testing.
4. Extracts unique scripts for each variation.

Usage: python3 scrape_variations_fast.py
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re

def get_fast_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('window-size=1920,1080')
    
    # Use normal strategy to ensure JS loads, but block assets
    options.page_load_strategy = 'normal' 
    
    # Block images, fonts, media
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.notifications": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.cookies": 2,
        "profile.managed_default_content_settings.javascript": 1, 
        "profile.managed_default_content_settings.plugins": 2,
        "profile.managed_default_content_settings.popups": 2,
        "profile.managed_default_content_settings.geolocation": 2,
        "profile.managed_default_content_settings.media_stream": 2,
    }
    options.add_experimental_option("prefs", prefs)
    
    return webdriver.Chrome(options=options)

def scrape_encounter_variations(driver, url, name):
    print(f"\n🚀 Processing: {name}")
    driver.get(url)
    
    scripts = []
    
    try:
        # 1. Open "Browse all alternatives"
        print("  Looking for alternatives button...")
        try:
            # Wait for button to be clickable
            browse_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Browse all alternatives"))
            )
            # Scroll to it
            driver.execute_script("arguments[0].scrollIntoView(true);", browse_btn)
            time.sleep(0.5)
            # Click
            browse_btn.click()
        except Exception as e:
            print(f"  ! Button issue: {e}")
            return []

        # Wait for modal
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "alternatives_window"))
            )
            time.sleep(1) # Allow animation
        except:
            print("  ! Modal didn't appear")
            return []

        # 2. Get Rows
        modal = driver.find_element(By.ID, "alternatives_window")
        rows = modal.find_elements(By.TAG_NAME, "tr")
        rows = [r for r in rows if r.find_elements(By.TAG_NAME, "td")]
        
        print(f"  Found {len(rows)} variations. Scraping first 5...")
        
        # 3. Iterate
        for i in range(min(len(rows), 5)): 
            # Re-fetch rows
            current_rows = modal.find_elements(By.TAG_NAME, "tr")
            current_rows = [r for r in current_rows if r.find_elements(By.TAG_NAME, "td")]
            if i >= len(current_rows): break
            row = current_rows[i]
            
            try:
                # Scroll row
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", row)
                
                # Click the first cell (Team)
                cells = row.find_elements(By.TAG_NAME, "td")
                if cells:
                    cells[0].click()
                
                # Wait for tooltip update
                time.sleep(0.5) 
                
                # Read Tooltip
                script_text = ""
                try:
                    tooltip = driver.find_element(By.ID, "td_tooltip")
                    script_text = tooltip.get_attribute('innerText')
                except: pass
                
                # Clean script
                if script_text:
                    lines = [l.strip() for l in script_text.split('\n') 
                             if l.strip() and not l.startswith("Click the button")]
                    script_text = "\n".join(lines)

                # Extract Team IDs
                row_html = row.get_attribute('innerHTML')
                team_ids = [int(x) for x in re.findall(r'/Pet/(\d+)/', row_html)]
                while len(team_ids) < 3: team_ids.append(0)
                team_ids = team_ids[:3]

                if script_text:
                    scripts.append({
                        "variation": i+1,
                        "team": team_ids,
                        "script_preview": script_text[:40].replace('\n', ' ') + "..."
                    })
                    print(f"    + Var {i+1}: Script found ({len(script_text)} chars)")
                else:
                    print(f"    - Var {i+1}: No script")
                
            except Exception as e:
                print(f"    ! Error row {i}: {e}")
                continue
                
    except Exception as e:
        print(f"  ! Error: {e}")
        
    return scripts

def main():
    driver = get_fast_driver()
    try:
        data = scrape_encounter_variations(
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
