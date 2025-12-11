import json
import re
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

class XuFuBrowserScraper:
    def __init__(self):
        self.base_url = "https://www.wow-petguide.com"
        self.data = {}
        
    def auto_scroll(self, page):
        """Scrolls to bottom of page to trigger lazy loading."""
        last_height = page.evaluate("document.body.scrollHeight")
        while True:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(1000)
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def scrape_encounter_page(self, page, url):
        print(f"  Visiting: {url}")
        try:
            page.goto(url, wait_until="domcontentloaded")
            # Force desktop view
            page.set_viewport_size({"width": 1920, "height": 1080})
            page.wait_for_timeout(2000) # Wait for JS
            
            # Try to close cookie banner if present
            try:
                page.locator("button:has-text('Agree')").click(timeout=1000)
            except: pass

        except Exception as e:
            print(f"    ! Error loading page: {e}")
            return []

        strategies = []
        
        # 1. Find Strategy Switchers (Broad Selectors)
        # We look for standard Bootstrap tabs OR list groups (sidebars)
        potential_tabs = page.locator('a.nav-link, ul.nav li a, .list-group-item-action')
        
        count = potential_tabs.count()
        
        if count > 0:
            # We found tabs/buttons. Let's iterate them.
            # Note: The "Description" or "Comments" tabs might be included, we filter them.
            
            # We use a set of seen script signatures to avoid duplicates
            seen_scripts = set()

            for i in range(count):
                try:
                    tab = potential_tabs.nth(i)
                    if not tab.is_visible(): continue
                    
                    tab_text = tab.inner_text().strip()
                    # Skip navigation/irrelevant tabs
                    if any(x in tab_text for x in ["Comment", "Discussion", "Log", "Export", "Guide", "Home"]):
                        continue
                        
                    # Filter: Strategy tabs usually have numbers or specific names
                    # If it's a generic nav link (like "Discord"), skip it
                    href = tab.get_attribute('href')
                    if href and "http" in href and "wow-petguide" not in href: continue

                    # Click to load strategy
                    # Use force=True to bypass simple overlays
                    tab.click(force=True)
                    page.wait_for_timeout(500) 
                    
                    # Find the active content container
                    # Xu-Fu usually puts content in .tab-pane.active
                    # But sometimes it's just the main body if it's a page reload
                    active_pane = page.locator('.tab-pane.active, #main-content').first
                    
                    if active_pane.count() > 0:
                        strat_data = self._extract_data_from_pane(active_pane, tab_text)
                        
                        # Deduplicate based on script content
                        if strat_data['script'] and strat_data['script'] not in seen_scripts:
                            strategies.append(strat_data)
                            seen_scripts.add(strat_data['script'])
                            
                except Exception as e:
                    # Ignore click errors (some nav links might not be tabs)
                    pass
        
        # Fallback: If no tabs yielded results (or no tabs found), scrape current view
        if not strategies:
            print("    No strategy tabs found/processed. Scraping main view...")
            main_content = page.locator('body')
            strat_data = self._extract_data_from_pane(main_content, "Default Strategy")
            if strat_data['pet_slots'] or strat_data['script']:
                strategies.append(strat_data)

        print(f"    -> Captured {len(strategies)} unique strategies.")
        return strategies

    def _extract_data_from_pane(self, pane, name):
        strategy = {'name': name, 'pet_slots': [], 'script': ''}
        
        # 1. Extract Pets
        pets = []
        # Look for pet links visible in the pane
        # 'bt_petdetails' is the class Xu-Fu uses for pet links
        pet_links = pane.locator('a.bt_petdetails').all()
        
        for link in pet_links:
            if not link.is_visible(): continue
            
            p_name = link.inner_text().strip()
            href = link.get_attribute('href')
            p_id = 0
            if href:
                match = re.search(r'/Pet/(\d+)/', href)
                if match: p_id = int(match.group(1))
            pets.append({'name': p_name, 'id': p_id})
            
        # Remove duplicates while preserving order
        unique_pets = []
        seen = set()
        for p in pets:
            if p['id'] not in seen:
                seen.add(p['id'])
                unique_pets.append(p)
        pets = unique_pets

        # Slot Heuristic (3 slots)
        if len(pets) >= 3:
            slot1, slot2, slot3 = [pets[0]], [pets[1]], [pets[2]]
            # Alternatives often follow the main 3
            for i, p in enumerate(pets[3:]):
                idx = i % 3
                if idx == 0: slot1.append(p)
                elif idx == 1: slot2.append(p)
                else: slot3.append(p)
            strategy['pet_slots'] = [slot1, slot2, slot3]
        elif len(pets) > 0:
            strategy['pet_slots'] = [[p] for p in pets]
        else:
            strategy['pet_slots'] = []

        # 2. Extract Script
        script_text = ""
        
        # Search for code containers
        script_box = pane.locator('.code:visible, .script-box:visible, textarea.form-control:visible').first
        
        if script_box.count() > 0:
            tag = script_box.evaluate("el => el.tagName")
            if tag == 'TEXTAREA':
                script_text = script_box.input_value()
            else:
                script_text = script_box.inner_text()
        
        if not script_text:
            # Fallback: scan text
            try:
                full_text = pane.inner_text()
                if "use(" in full_text:
                    lines = [l.strip() for l in full_text.split('\n') if "use(" in l or "change(" in l or "standby" in l]
                    script_text = "\n".join(lines)
            except: pass
        
        strategy['script'] = script_text
        return strategy

    def scrape_category(self, page, category_url):
        print(f"\nScanning Category: {category_url}")
        try:
            page.goto(category_url, wait_until="domcontentloaded")
            page.set_viewport_size({"width": 1920, "height": 1080})
            self.auto_scroll(page) 
        except: return []
        
        links = page.locator('a[href*="/Strategy/"], a[href*="/Encounter/"]').all()
        
        encounters = []
        seen_urls = set()
        
        for link in links:
            url = link.get_attribute('href')
            if not url: continue
            
            full_url = f"{self.base_url}{url}" if not url.startswith('http') else url
            if full_url in seen_urls: continue
            
            name = link.inner_text().strip()
            if not name: continue
            
            # Filter out junk links
            if len(name) < 3 or "Comment" in name: continue

            seen_urls.add(full_url)
            encounters.append({'name': name, 'url': full_url})
            
        return encounters

    def run(self):
        print("Starting Playwright Scraper (Desktop Mode)...")
        
        categories = {
            "Pandaria": ["/Section/19/Pandaren_Spirit_Tamers", "/Section/20/Beasts_of_Fable", "/Section/21/Tamers"],
            "Draenor": ["/Section/38/Draenor_Tamers"],
            "Legion": ["/Section/48/Broken_Isles_Tamers"],
            "Shadowlands": ["/Section/80/World_Quests"],
            "The War Within": ["/Section/104/World_Quests"]
        }

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True) 
            page = browser.new_page()
            
            for expansion, paths in categories.items():
                self.data[expansion] = {}
                
                for path in paths:
                    full_path = f"{self.base_url}{path}"
                    encounters = self.scrape_category(page, full_path)
                    print(f"Found {len(encounters)} encounters in {path}")
                    
                    cat_data = []
                    for enc in encounters:
                        strategies = self.scrape_encounter_page(page, enc['url'])
                        if strategies:
                            cat_data.append({
                                'encounter_name': enc['name'],
                                'url': enc['url'],
                                'strategies': strategies
                            })
                            
                    self.data[expansion][path] = cat_data
            
            browser.close()
            
        with open('strategies_full_browser.json', 'w') as f:
            json.dump(self.data, f, indent=2)
        print("\n✅ Scraping Complete. Saved to strategies_full_browser.json")

if __name__ == "__main__":
    scraper = XuFuBrowserScraper()
    scraper.run()