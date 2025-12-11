# scrape_all_team_scripts_full.py
"""Scrape ALL strategy variations (including per‑variation scripts) from Xu‑Fu.

The site shows a "Browse all alternatives" modal. Inside the modal each row
represents a possible team. Clicking the "Script" element in a row populates a
tooltip (id='td_tooltip') with the battle script for that specific variation.

This script:
1. Loads the list of encounter URLs from `strategies_enhanced.json` (the
   existing JSON already contains every encounter and its default script).
2. For each encounter it opens the page with Selenium, clicks the "Browse all
   alternatives" link, and iterates over every row in the alternatives modal.
3. For each row it extracts:
   * The pet IDs for that team (from the pet icon links).
   * The script text if a script button is present – otherwise the script is
     recorded as an empty string.
4. All results are saved to `all_variations_with_scripts.json` in the format:
   {
       "Encounter Name": [
           {"team": [id, id, id], "script": "..."},
           ...
       ],
       ...
   }

The script runs headless Chrome; it respects a short delay between actions to
avoid being rate‑limited.
"""

import json
import time
import re
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SOURCE_JSON = Path("strategies_enhanced.json")
OUTPUT_JSON = Path("all_variations_with_scripts.json")
# Adjust delay if needed (seconds)
PAGE_LOAD_DELAY = 2.0
MODAL_SCROLL_ITER = 5
SCROLL_PAUSE = 0.5
# ---------------------------------------------------------------------------

def get_encounter_list():
    """Return a list of (encounter_name, url) tuples from the existing JSON."""
    with SOURCE_JSON.open() as f:
        data = json.load(f)
    encounters = []
    for expansion, categories in data.items():
        for cat_name, enc_list in categories.items():
            for enc in enc_list:
                name = enc.get("encounter_name")
                url = enc.get("url")
                if name and url:
                    encounters.append((name, url))
    return encounters

def init_driver():
    chrome_opts = Options()
    chrome_opts.add_argument("--headless")
    chrome_opts.add_argument("--disable-gpu")
    chrome_opts.add_argument("--no-sandbox")
    chrome_opts.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_opts)
    driver.set_page_load_timeout(30)
    return driver

def click_browse_all(driver):
    """Click the 'Browse all alternatives' link if present."""
    try:
        btn = driver.find_element(By.XPATH, "//a[contains(text(),'Browse all alternatives')]")
        btn.click()
        time.sleep(1)
        return True
    except NoSuchElementException:
        return False

def scroll_modal(driver):
    """Scroll the alternatives modal to force lazy‑loading of rows."""
    try:
        modal = driver.find_element(By.ID, "alternatives_window")
        for _ in range(MODAL_SCROLL_ITER):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", modal)
            time.sleep(SCROLL_PAUSE)
    except NoSuchElementException:
        pass

def extract_rows(driver):
    """Return a list of row WebElements inside the alternatives modal."""
    try:
        modal = driver.find_element(By.ID, "alternatives_window")
        rows = modal.find_elements(By.XPATH, ".//tr[contains(@class,'strategy-row') or @data-strategy-id]")
        # Fallback: any <tr> inside the modal
        if not rows:
            rows = modal.find_elements(By.TAG_NAME, "tr")
        return rows
    except NoSuchElementException:
        return []

def extract_team_from_row(row):
    """Parse pet IDs from a row. Returns a list of three IDs (missing slots are 0)."""
    pet_ids = []
    # Links to pet pages are <a href="/Pet/<id>/...">
    links = row.find_elements(By.XPATH, ".//a[contains(@href,'/Pet/')]")
    for link in links:
        href = link.get_attribute("href")
        m = re.search(r"/Pet/(\d+)/", href)
        if m:
            pet_ids.append(int(m.group(1)))
    # Ensure exactly three entries (pad with 0)
    while len(pet_ids) < 3:
        pet_ids.append(0)
    return pet_ids[:3]

def extract_script(driver):
    """Read the tooltip text from the page after a script button was clicked."""
    try:
        tooltip = driver.find_element(By.ID, "td_tooltip")
        raw = tooltip.get_attribute("innerText") or ""
        # Clean up the typical header line "Click the button to copy the script..."
        lines = [ln for ln in raw.splitlines() if ln and not ln.startswith("Click the button")]
        return "\n".join(lines).strip()
    except NoSuchElementException:
        return ""

def process_encounter(driver, name, url):
    print(f"\nProcessing {name}")
    driver.get(url)
    time.sleep(PAGE_LOAD_DELAY)
    # Try to open the alternatives modal
    has_modal = click_browse_all(driver)
    if not has_modal:
        # No alternatives – fall back to default script already in source JSON
        print("  No alternatives modal; will use default script later.")
        return []
    # Ensure all rows are loaded
    scroll_modal(driver)
    rows = extract_rows(driver)
    print(f"  Found {len(rows)} rows")
    variations = []
    for idx, row in enumerate(rows):
        # Click the script button inside the row if it exists
        try:
            script_btn = row.find_element(By.XPATH, ".//div[contains(text(),'Script')]")
            script_btn.click()
            time.sleep(0.5)
            script_text = extract_script(driver)
        except NoSuchElementException:
            script_text = ""
        team_ids = extract_team_from_row(row)
        variations.append({"team": team_ids, "script": script_text})
        if (idx + 1) % 20 == 0:
            print(f"    Processed {idx+1}/{len(rows)} rows")
    # Close the modal (press Escape)
    try:
        from selenium.webdriver.common.keys import Keys
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    except Exception:
        pass
    return variations

def main():
    encounters = get_encounter_list()
    driver = init_driver()
    all_data = {}
    for enc_name, enc_url in encounters:
        try:
            variations = process_encounter(driver, enc_name, enc_url)
            if variations:
                all_data[enc_name] = variations
        except Exception as e:
            print(f"Error processing {enc_name}: {e}")
        # Respectful pause between encounters
        time.sleep(1.5)
    driver.quit()
    OUTPUT_JSON.write_text(json.dumps(all_data, indent=2))
    print(f"\n✅ Saved all variations to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
