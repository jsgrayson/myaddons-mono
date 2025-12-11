"""
Playwright-based scraper to extract ALL strategy variations and their scripts from Xu-Fu.

This scraper:
1. Opens each encounter page
2. Clicks "Browse all alternatives"
3. Scrolls through the modal to load all strategies
4. Extracts each strategy's team and script (if available)
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
import json

def scrape_encounter_all_strategies(page, encounter_url, encounter_name):
    """Scrape all strategy variations for a single encounter"""
    print(f"\n Scraping: {encounter_name}")
    print(f"  URL: {encounter_url}")
    
    page.goto(encounter_url, wait_until='domcontentloaded', timeout=30000)
    time.sleep(3)  # Wait for JS to load
    
    strategies = []
    
    try:
        # Click "Browse all alternatives"
        browse_btn = page.locator('text="Browse all alternatives"').first
        if browse_btn.is_visible(timeout=5000):
            browse_btn.click()
            time.sleep(2)
            print(f"  Opened alternatives modal")
            
            # Find the modal/container with strategies
            # The modal might be in a remodal or similar container
            modal = page.locator('.remodal, [role="dialog"], .alternatives-container').first
            
            # Scroll down to load all strategies
            print(f"  Scrolling to load all strategies...")
            for _ in range(10):  # Scroll multiple times to load all
                modal.evaluate('el => el.scrollTop = el.scrollHeight')
                time.sleep(0.5)
            
            # Find all strategy rows
            # These are typically in a table or list
            strategy_rows = page.locator('tr.strategy-row, .alternative-team, [data-strategy-id]').all()
            
            if not strategy_rows:
                # Fallback: look for any rows in the modal
                strategy_rows = modal.locator('tr').all()
            
            print(f"  Found {len(strategy_rows)} strategy rows")
            
            for idx, row in enumerate(strategy_rows[:35]):  # Limit to 35 to be safe
                try:
                    # Click the script button for this row
                    script_btn = row.locator('button:has-text("Script"), .script-button, [title*="Script"]').first
                    
                    if script_btn.is_visible(timeout=1000):
                        script_btn.click()
                        time.sleep(0.5)
                        
                        # Extract script from tooltip
                        tooltip = page.locator('#td_tooltip, .tooltip-content').first
                        if tooltip.is_visible(timeout=2000):
                            script_text = tooltip.inner_text()
                            
                            # Clean script text
                            lines = script_text.split('\n')
                            clean_lines = [l for l in lines if l.strip() and "Click the button" not in l]
                            script = '\n'.join(clean_lines).strip()
                            
                            if script:
                                # Extract team from this row
                                pet_links = row.locator('a[href*="/Pet/"]').all()
                                team = []
                                for link in pet_links[:3]:
                                    href = link.get_attribute('href')
                                    if href:
                                        import re
                                        match = re.search(r'/Pet/(\d+)/', href)
                                        if match:
                                            team.append(int(match.group(1)))
                                
                                if len(team) == 3:
                                    strategies.append({
                                        'variation_num': idx + 1,
                                        'team': team,
                                        'script': script
                                    })
                                    print(f"    ✓ Strategy {idx+1}: {len(script)} chars, team: {team}")
                        
                        # Close tooltip if needed
                        try:
                            page.keyboard.press('Escape')
                        except:
                            pass
                            
                except Exception as e:
                    # Some rows might not have scripts
                    continue
            
            # Close modal
            try:
                page.keyboard.press('Escape')
                time.sleep(0.5)
            except:
                pass
                
        else:
            print(f"  No 'Browse all alternatives' button found")
            
            # Fallback: get the default strategy
            tooltip = page.locator('#td_tooltip').first
            if tooltip.is_visible(timeout=2000):
                script = tooltip.inner_text().strip()
                strategies.append({
                    'variation_num': 1,
                    'team': [],  # Would need to extract
                    'script': script
                })
                print(f"  ✓ Got default strategy: {len(script)} chars")
                
    except Exception as e:
        print(f"  Error: {e}")
    
    return strategies


def main():
    """Test scraper on a few encounters"""
    test_encounters = [
        ('Rock Collector', 'https://www.wow-petguide.com/Encounter/1589/Rock_Collector'),
        ('Robot Rumble', 'https://www.wow-petguide.com/Encounter/1590/Robot_Rumble'),
        ('Major Payne', 'https://www.wow-petguide.com/Strategy/21310/Major_Payne'),
    ]
    
    all_data = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for production
        page = browser.new_page()
        
        for name, url in test_encounters:
            strategies = scrape_encounter_all_strategies(page, url, name)
            all_data[name] = strategies
            time.sleep(2)  # Be respectful
        
        browser.close()
    
    # Save results
    with open('xufu_all_scripts_test.json', 'w') as f:
        json.dump(all_data, f, indent=2)
    
    print(f"\n✓ Saved to xufu_all_scripts_test.json")
    print(f"Total encounters: {len(all_data)}")
    for enc, strats in all_data.items():
        print(f"  {enc}: {len(strats)} strategies with scripts")


if __name__ == '__main__':
    main()
