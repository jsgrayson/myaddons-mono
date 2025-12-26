#!/usr/bin/env python3
"""
talent_scraper_selenium.py - Automated talent export scraper using Selenium

Scrapes talent export strings from Icy-Veins and Skill-Capped using browser automation.

Requirements:
    pip install selenium webdriver-manager

Usage:
    python3 talent_scraper_selenium.py
"""

import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

SPECS_DIR = os.path.join(os.path.dirname(__file__), "..", "Brain", "data", "specs")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "scraped_talents.json")

# Spec configurations: (spec_id, spec_filename_prefix, class, spec, urls)
SPEC_CONFIGS = [
    # Rogue
    (41, "41_assassin", "rogue", "assassination", {
        "mythic": "https://www.icy-veins.com/wow/assassination-rogue-pve-dps-mythic-plus-tips",
        "raid": "https://www.icy-veins.com/wow/assassination-rogue-pve-dps-talents-builds",
        "pvp": "https://www.skill-capped.com/wow/builds/assassination-rogue",
    }),
    (42, "42_outlaw", "rogue", "outlaw", {
        "mythic": "https://www.icy-veins.com/wow/outlaw-rogue-pve-dps-mythic-plus-tips",
        "raid": "https://www.icy-veins.com/wow/outlaw-rogue-pve-dps-talents-builds",
        "pvp": "https://www.skill-capped.com/wow/builds/outlaw-rogue",
    }),
    (43, "43_sub", "rogue", "subtlety", {
        "mythic": "https://www.icy-veins.com/wow/subtlety-rogue-pve-dps-mythic-plus-tips",
        "raid": "https://www.icy-veins.com/wow/subtlety-rogue-pve-dps-talents-builds",
        "pvp": "https://www.skill-capped.com/wow/builds/subtlety-rogue",
    }),
    # Druid
    (103, "103_feral", "druid", "feral", {
        "mythic": "https://www.icy-veins.com/wow/feral-druid-pve-dps-mythic-plus-tips",
        "raid": "https://www.icy-veins.com/wow/feral-druid-pve-dps-talents-builds",
        "pvp": "https://www.skill-capped.com/wow/builds/feral-druid",
    }),
    (102, "102_balance", "druid", "balance", {
        "mythic": "https://www.icy-veins.com/wow/balance-druid-pve-dps-mythic-plus-tips",
        "raid": "https://www.icy-veins.com/wow/balance-druid-pve-dps-talents-builds",
    }),
    (104, "104_guardian", "druid", "guardian", {
        "mythic": "https://www.icy-veins.com/wow/guardian-druid-pve-tank-mythic-plus-tips",
        "raid": "https://www.icy-veins.com/wow/guardian-druid-pve-tank-talents-builds",
    }),
    # Warrior
    (72, "72_fury", "warrior", "fury", {
        "mythic": "https://www.icy-veins.com/wow/fury-warrior-pve-dps-mythic-plus-tips",
        "raid": "https://www.icy-veins.com/wow/fury-warrior-pve-dps-talents-builds",
        "pvp": "https://www.skill-capped.com/wow/builds/fury-warrior",
    }),
    (71, "71_arms", "warrior", "arms", {
        "mythic": "https://www.icy-veins.com/wow/arms-warrior-pve-dps-mythic-plus-tips",
        "raid": "https://www.icy-veins.com/wow/arms-warrior-pve-dps-talents-builds",
        "pvp": "https://www.skill-capped.com/wow/builds/arms-warrior",
    }),
    # Add more specs as needed...
]


def setup_driver():
    """Setup Chrome WebDriver with options."""
    options = Options()
    options.add_argument("--headless")  # Run headless
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def scrape_icy_veins(driver, url: str) -> str | None:
    """Scrape talent export string from Icy-Veins page."""
    try:
        driver.get(url)
        time.sleep(3)  # Wait for page load
        
        # Look for export/copy button
        export_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Export') or contains(text(), 'Copy')]")
        
        for btn in export_buttons:
            try:
                btn.click()
                time.sleep(1)
                
                # Check clipboard or modal for export string
                # Icy-Veins may use a modal or copy to clipboard
                modals = driver.find_elements(By.CLASS_NAME, "modal")
                for modal in modals:
                    text_areas = modal.find_elements(By.TAG_NAME, "textarea")
                    for ta in text_areas:
                        value = ta.get_attribute('value')
                        if value and len(value) > 50:  # Talent strings are long
                            return value
                
                # Try input fields
                inputs = driver.find_elements(By.XPATH, "//input[contains(@value, 'C') and string-length(@value) > 50]")
                for inp in inputs:
                    value = inp.get_attribute('value')
                    if value:
                        return value
                        
            except Exception as e:
                print(f"    Button click failed: {e}")
                continue
        
        # Fallback: look for pre-formatted talent strings in page
        elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'CMQA') or contains(text(), 'CYGA') or contains(text(), 'CIQA')]")
        for el in elements:
            text = el.text.strip()
            if len(text) > 50 and text.startswith('C'):
                return text
                
        return None
        
    except Exception as e:
        print(f"    Error scraping {url}: {e}")
        return None


def scrape_skill_capped(driver, url: str) -> str | None:
    """Scrape talent export string from Skill-Capped page."""
    try:
        driver.get(url)
        time.sleep(3)
        
        # Skill-Capped typically has copy buttons
        buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Copy') or contains(@class, 'copy')]")
        
        for btn in buttons:
            try:
                btn.click()
                time.sleep(1)
            except:
                continue
        
        # Look for visible talent strings
        elements = driver.find_elements(By.XPATH, "//code | //pre | //input[@readonly]")
        for el in elements:
            text = el.text or el.get_attribute('value')
            if text and len(text) > 50 and text.startswith('C'):
                return text
        
        return None
        
    except Exception as e:
        print(f"    Error scraping PvP: {e}")
        return None


def scrape_all_specs():
    """Scrape talent exports for all configured specs."""
    print("SkillWeaver Talent Scraper (Selenium)")
    print("=" * 50)
    
    driver = setup_driver()
    results = {}
    
    try:
        for spec_id, filename_prefix, class_name, spec_name, urls in SPEC_CONFIGS:
            print(f"\n[*] Scraping {class_name.title()} - {spec_name.title()}")
            
            spec_talents = {}
            
            for content_type, url in urls.items():
                print(f"    [{content_type}] {url}")
                
                if "skill-capped" in url:
                    talent_string = scrape_skill_capped(driver, url)
                else:
                    talent_string = scrape_icy_veins(driver, url)
                
                if talent_string:
                    spec_talents[content_type] = talent_string
                    print(f"    ✓ Found: {talent_string[:40]}...")
                else:
                    print(f"    ✗ Not found")
            
            # Copy mythic to delve if delve not scraped
            if "mythic" in spec_talents and "delve" not in spec_talents:
                spec_talents["delve"] = spec_talents["mythic"]
            
            results[spec_id] = {
                "filename": filename_prefix,
                "class": class_name,
                "spec": spec_name,
                "talents": spec_talents
            }
    
    finally:
        driver.quit()
    
    # Save results
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n[+] Results saved to: {OUTPUT_FILE}")
    return results


def apply_to_spec_files(results: dict):
    """Apply scraped talents to spec JSON files."""
    print("\n[*] Applying to spec files...")
    
    for spec_id, data in results.items():
        talents = data.get("talents", {})
        if not talents:
            continue
        
        # Find spec file
        for filename in os.listdir(SPECS_DIR):
            if filename.startswith(f"{spec_id}_") and filename.endswith('.json'):
                filepath = os.path.join(SPECS_DIR, filename)
                
                with open(filepath, 'r') as f:
                    spec_data = json.load(f)
                
                spec_data['talent_loadouts'] = talents
                
                with open(filepath, 'w') as f:
                    json.dump(spec_data, f, indent=4)
                
                print(f"    ✓ Updated {filename}")
                break


if __name__ == "__main__":
    results = scrape_all_specs()
    apply_to_spec_files(results)
    print("\n[✓] Done!")
