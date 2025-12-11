# quick_variation_scrape.py
"""Fast scrape of a single alternative script per encounter.

For each encounter listed in `strategies_enhanced.json` we:
1. Open the page.
2. Click "Browse all alternatives".
3. Click the **second** row in the modal (index 1) – this guarantees we are not on the default team.
4. Read the tooltip (`#td_tooltip`) which now contains the script for that specific team.
5. Record the three pet IDs for that row and the extracted script.

All results are written to `variations_with_scripts.json` as:
{
  "Encounter Name": [{"team": [id, id, id], "script": "..."}],
  ...
}
"""

import json, time, re
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

SOURCE_JSON = Path("strategies_enhanced.json")
OUTPUT_JSON = Path("variations_with_scripts.json")
PAGE_LOAD_TIMEOUT = 30
ROW_LOAD_TIMEOUT = 30
DELAY_BETWEEN = 1.5

def get_encounters():
    with SOURCE_JSON.open() as f:
        data = json.load(f)
    out = []
    for exp, cats in data.items():
        for cat, encs in cats.items():
            for enc in encs:
                name = enc.get("encounter_name")
                url = enc.get("url")
                if name and url:
                    out.append((name, url))
    return out

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
        WebDriverWait(driver, ROW_LOAD_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "alternatives_window"))
        )
        return True
    except (NoSuchElementException, TimeoutException):
        return False

def extract_team(row):
    ids = []
    for link in row.find_elements(By.XPATH, ".//a[contains(@href,'/Pet/')]"):
        m = re.search(r"/Pet/(\d+)/", link.get_attribute("href"))
        if m:
            ids.append(int(m.group(1)))
    while len(ids) < 3:
        ids.append(0)
    return ids[:3]

def get_tooltip(driver):
    try:
        txt = driver.find_element(By.ID, "td_tooltip").get_attribute("innerText") or ""
        lines = [l for l in txt.splitlines() if l and not l.startswith("Click the button")]
        return "\n".join(lines).strip()
    except NoSuchElementException:
        return ""

def process(enc_name, enc_url, driver):
    driver.get(enc_url)
    time.sleep(2)
    if not click_browse_all(driver):
        return None
    rows = driver.find_elements(By.XPATH, "//div[@id='alternatives_window']//tr")
    if len(rows) < 2:
        return None
    # pick the second row (index 1)
    row = rows[1]
    # click first cell to load its script
    try:
        first_cell = row.find_element(By.XPATH, ".//td[1]")
        driver.execute_script("arguments[0].click();", first_cell)
        time.sleep(0.5)
        WebDriverWait(driver, ROW_LOAD_TIMEOUT).until(lambda d: get_tooltip(d) != "")
        script = get_tooltip(driver)
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
        script = ""
    team = extract_team(row)
    return {"team": team, "script": script}

def main():
    encounters = get_encounters()
    driver = init_driver()
    result = {}
    for name, url in encounters:
        data = process(name, url, driver)
        if data:
            result[name] = [data]
        time.sleep(DELAY_BETWEEN)
    driver.quit()
    OUTPUT_JSON.write_text(json.dumps(result, indent=2))
    print(f"✅ Saved {len(result)} entries to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
