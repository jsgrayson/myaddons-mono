"""
VISIBLE Multi-Script Scraper for Xu-Fu

This scraper runs in a VISIBLE Chrome window to extract all team variations and their scripts.
It handles:
1. Opening the encounter page.
2. Clicking "Browse all alternatives".
3. Scrolling through the modal to ensure all rows are loaded.
4. Clicking each team row (specifically the arrow/first cell) to trigger the script tooltip.
5. Extracting the script from the tooltip (#td_tooltip).

Usage: python3 scrape_all_team_scripts.py
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import re

def scrape_encounter(driver, url, name):
    """Extract all team scripts for one encounter"""
    print(f"\nProcessing: {name}")
    driver.get(url)
    time.sleep(3) # Wait for page load
    
    scripts = []
    
    try:
        # 1. Open "Browse all alternatives" modal
        try:
            browse_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Browse all alternatives"))
            )
            # Scroll to button to ensure visibility
            driver.execute_script("arguments[0].scrollIntoView(true);", browse_btn)
            time.sleep(1)
            browse_btn.click()
        except Exception as e:
            print(f"  ! Could not find/click 'Browse all alternatives': {e}")
            return []

        time.sleep(3) # Wait for modal to animate in
        
        # 2. Find the modal container and rows
        try:
            modal = driver.find_element(By.ID, "alternatives_window")
        except:
            try:
                modal = driver.find_element(By.CLASS_NAME, "remodal")
            except:
                print("  ! Could not find modal window")
                return []

        # 3. Iterate through rows
        # We fetch all rows first to get the count.
        rows = modal.find_elements(By.TAG_NAME, "tr")
        # Filter out header rows (usually have 'th')
        rows = [r for r in rows if r.find_elements(By.TAG_NAME, "td")]
        
        print(f"  Found {len(rows)} variations")
        
        # Limit to first 15 variations to save time, unless it's a critical run
        for i in range(min(len(rows), 15)):
            # Re-find rows to be safe
            current_rows = modal.find_elements(By.TAG_NAME, "tr")
            current_rows = [r for r in current_rows if r.find_elements(By.TAG_NAME, "td")]
            
            if i >= len(current_rows): break
            row = current_rows[i]
            
            try:
                # Scroll row into view
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", row)
                time.sleep(0.5)
                
                # Click the FIRST cell (Team composition / Arrow) to select it
                cells = row.find_elements(By.TAG_NAME, "td")
                if not cells: continue
                
                # Click logic: Try clicking the cell, or specifically an arrow if present
                # User mentioned "arrows", so let's look for an icon if possible, otherwise click cell
                target_click = cells[0]
                try:
                    arrow = row.find_element(By.CLASS_NAME, "fa-chevron-right") # Example class
                    if arrow.is_displayed(): target_click = arrow
                except: pass
                
                target_click.click()
                time.sleep(1.0) # Wait for tooltip to update
                
                # Extract Script from Tooltip
                script_text = ""
                try:
                    tooltip = driver.find_element(By.ID, "td_tooltip")
                    if tooltip.is_displayed():
                        raw_text = tooltip.text
                        # Clean up "Click the button..." garbage
                        lines = [l.strip() for l in raw_text.split('\n') 
                                 if l.strip() and not l.startswith("Click the button")]
                        script_text = "\n".join(lines)
                except:
                    pass 

                # Fallback: Check for inline code block
                if not script_text:
                    try:
                        code_div = row.find_element(By.CLASS_NAME, "code")
                        script_text = code_div.text
                    except: pass

                # Extract Team IDs
                pet_links = row.find_elements(By.CSS_SELECTOR, 'a[href*="/Pet/"]')
                team_ids = []
                for link in pet_links:
                    href = link.get_attribute('href')
                    match = re.search(r'/Pet/(\d+)/', href)
                    if match: team_ids.append(int(match.group(1)))
                
                # Pad team to 3
                while len(team_ids) < 3: team_ids.append(0)
                team_ids = team_ids[:3]

                if script_text:
                    scripts.append({
                        "variation_index": i,
                        "team": team_ids,
                        "script": script_text
                    })
                    print(f"    + Var {i+1}: Script found ({len(script_text)} chars)")
                else:
                    print(f"    - Var {i+1}: No script found in tooltip")

            except Exception as e:
                print(f"    ! Error on row {i+1}: {e}")
                continue
        
        # Close modal
        ActionChains(driver).send_keys('\ue00c').perform() # ESC
        time.sleep(1)

    except Exception as e:
        print(f"  ! Critical Error: {e}")

    print(f"  -> Extracted {len(scripts)} scripts")
    return scripts

def main():
    # List of encounters to scrape
    targets = [
        ("Rock Collector", "https://www.wow-petguide.com/Encounter/1589/Rock_Collector"),
        ("Robot Rumble", "https://www.wow-petguide.com/Encounter/1590/Robot_Rumble"),
        ("The Power of Friendship", "https://www.wow-petguide.com/Encounter/1592/The_Power_of_Friendship"),
        ("Major Malfunction", "https://www.wow-petguide.com/Encounter/1593/Major_Malfunction"),
        ("Miniature Army", "https://www.wow-petguide.com/Encounter/1595/Miniature_Army"),
        ("The Thing from the Swamp", "https://www.wow-petguide.com/Encounter/1596/The_Thing_from_the_Swamp"),
        ("Ziriak", "https://www.wow-petguide.com/Encounter/1598/Ziriak"),
        ("One Hungry Worm", "https://www.wow-petguide.com/Encounter/1599/One_Hungry_Worm")
    ]

    # Setup VISIBLE Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('window-size=1920,1080')

    driver = webdriver.Chrome(options=options)
    
    all_data = {}
    
    try:
        for name, url in targets:
            data = scrape_encounter(driver, url, name)
            if data:
                all_data[name] = data
            time.sleep(1)
            
    finally:
        driver.quit()
        
    # Save results
    with open("variations_with_scripts.json", "w") as f:
        json.dump(all_data, f, indent=2)
    
    print("\n✅ Done! Saved to variations_with_scripts.json")

if __name__ == "__main__":
    main()
