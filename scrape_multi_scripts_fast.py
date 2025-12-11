"""
Fast Playwright scraper - clicks each team to get all scripts
"""
from playwright.sync_api import sync_playwright
import time
import json

def scrape_all_team_scripts(page, url, name):
    """Get all team scripts by clicking each row"""
    print(f"\n{name}")
    page.goto(url, wait_until='domcontentloaded', timeout=30000)
    time.sleep(2)
    
    scripts = []
    
    try:
        # Click browse alternatives
        page.click('text="Browse all alternatives"', timeout=5000)
        time.sleep(1)
        
        # Find all team rows in the modal
        rows = page.locator('tr').all()
        print(f"  Found {len(rows)} rows")
        
        for i, row in enumerate(rows[:35]):  # Limit to 35
            try:
                # Click the row to select this team
                row.click(timeout=1000)
                time.sleep(0.3)  # Wait for script to update
                
                # Get the script
                tooltip = page.locator('#td_tooltip').first
                if tooltip.is_visible(timeout=1000):
                    script = tooltip.inner_text()
                    if len(script) > 50:  # Has actual content
                        # Get team pets
                        pets = []
                        pet_links = row.locator('a[href*="/Pet/"]').all()
                        for link in pet_links[:3]:
                            import re
                            match = re.search(r'/Pet/(\d+)/', link.get_attribute('href') or '')
                            if match:
                                pets.append(int(match.group(1)))
                        
                        scripts.append({'team': pets, 'script': script})
                        print(f"  ✓ Team {i+1}: {len(script)} chars")
            except:
                continue
        
        page.keyboard.press('Escape')  # Close modal
    except Exception as e:
        print(f"  Error: {e}")
    
    return scripts

# Test on 3 encounters
encounters = [
    ('Rock Collector', 'https://www.wow-petguide.com/Encounter/1589/Rock_Collector'),
    ('Robot Rumble', 'https://www.wow-petguide.com/Encounter/1590/Robot_Rumble'),
]

results = {}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    for name, url in encounters:
        results[name] = scrape_all_team_scripts(page, url, name)
    
    browser.close()

with open('test_multi_scripts.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n✓ Saved to test_multi_scripts.json")
for enc, scripts in results.items():
    print(f"  {enc}: {len(scripts)} scripts")
