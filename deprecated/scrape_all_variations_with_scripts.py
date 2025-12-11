# scrape_all_variations_with_scripts.py
"""Extract per‑variation scripts from Xu‑Fu.

Some encounters provide *different* battle scripts for each alternative team.
This scraper uses Selenium to:
1. Load each encounter URL.
2. Click "Browse all alternatives" to open the modal.
3. Iterate over every row in the modal.
4. Click the "Script" element in the row (if present).
5. Read the tooltip (`#td_tooltip`) which now contains the script for that
   specific variation.
6. Record the three pet IDs for the row and the extracted script.

The results are written to `variations_with_scripts.json` in the format:
{
  "Encounter Name": [
    {"team": [id, id, id], "script": "..."},
    ...
  ],
  ...
}

The script runs headless Chrome and includes explicit waits to avoid the
timeouts we saw earlier.
"""

import json
import time
import re
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SOURCE_JSON = Path("strategies_enhanced.json")
OUTPUT_JSON = Path("variations_with_scripts.json")
PAGE_LOAD_TIMEOUT = 30
ROW_LOAD_TIMEOUT = 40  # increased to allow tooltip to appear reliably
DELAY_BETWEEN_ENCOUNTERS = 2.0
# ---------------------------------------------------------------------------

def get_encounter_list():
    """Return a list of (name, url) from the existing strategies JSON."""
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
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=opts)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver

def click_browse_all(driver):
    try:
        btn = driver.find_element(By.XPATH, "//a[contains(text(),'Browse all alternatives')]")
        btn.click()
        # Wait for the modal to appear
        WebDriverWait(driver, ROW_LOAD_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "alternatives_window"))
        )
        return True
    except (NoSuchElementException, TimeoutException):
        return False

def scroll_modal(driver):
    try:
        modal = driver.find_element(By.ID, "alternatives_window")
        for _ in range(5):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", modal)
            time.sleep(0.5)
    except NoSuchElementException:
        pass

def extract_rows(driver):
    try:
        modal = driver.find_element(By.ID, "alternatives_window")
        rows = modal.find_elements(By.XPATH, ".//tr")
        return rows
    except NoSuchElementException:
        return []

def extract_team_from_row(row):
    pet_ids = []
    links = row.find_elements(By.XPATH, ".//a[contains(@href,'/Pet/')]")
    for link in links:
        href = link.get_attribute("href")
        m = re.search(r"/Pet/(\d+)/", href)
        if m:
            pet_ids.append(int(m.group(1)))
    while len(pet_ids) < 3:
        pet_ids.append(0)
    return pet_ids[:3]

def get_tooltip_script(driver):
    try:
        tooltip = driver.find_element(By.ID, "td_tooltip")
        raw = tooltip.get_attribute("innerText") or ""
        lines = [ln for ln in raw.splitlines() if ln and not ln.startswith("Click the button")]
        return "\n".join(lines).strip()
    except NoSuchElementException:
        return ""

def process_encounter(driver, name, url):
    print(f"\nProcessing {name}")
    driver.get(url)
    # Give the page a moment to settle
    time.sleep(2)
    if not click_browse_all(driver):
        print("  No alternatives modal – skipping.")
        return []
    scroll_modal(driver)
    rows = extract_rows(driver)
    print(f"  Found {len(rows)} rows")
    variations = []
    # Process only a limited number of rows to avoid long runtimes
    max_rows = min(5, len(rows))
    # Start from the second row (index 1) to avoid the currently selected team
    for idx in range(1, max_rows):
        row = rows[idx]
        # Click the row to select the team (this updates the tooltip with the specific script)
        script_text = ""
        try:
            # Click the first cell of the row to select the team
            first_cell = row.find_element(By.XPATH, ".//td[1]")
            driver.execute_script("arguments[0].click();", first_cell)
            time.sleep(0.5)  # allow UI update
            # Wait for tooltip to contain a non‑empty script
            WebDriverWait(driver, ROW_LOAD_TIMEOUT).until(
                lambda d: get_tooltip_script(d) != ""
            )
            script_text = get_tooltip_script(driver)
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            # If clicking fails or tooltip never updates, leave script empty
            pass
        team_ids = extract_team_from_row(row)
        variations.append({"team": team_ids, "script": script_text})
        if (idx + 1) % 20 == 0:
            print(f"    Processed {idx+1}/{max_rows} rows")
    # Close modal
    try:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    except Exception:
        pass
    return variations

def main():
    encounters = get_encounter_list()
    driver = init_driver()
    all_data = {}
    # Limit to first 5 encounters for a quick demo – remove slice for full run
    for enc_name, enc_url in encounters:  # process all encounters
        try:
            variations = process_encounter(driver, enc_name, enc_url)
            if variations:
                all_data[enc_name] = variations
        except Exception as e:
            print(f"Error on {enc_name}: {e}")
        time.sleep(DELAY_BETWEEN_ENCOUNTERS)
    driver.quit()
    OUTPUT_JSON.write_text(json.dumps(all_data, indent=2))
    print(f"\n✅ Saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
