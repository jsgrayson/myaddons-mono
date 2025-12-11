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

    def extract_script_from_modal(self, page):
        """Extracts script from the currently open alternatives modal tooltip."""
        try:
            # Wait for tooltip to be visible and contain text
            tooltip = page.locator("#td_tooltip")
            tooltip.wait_for(state="visible", timeout=2000)
            text = tooltip.inner_text()
            
            # Clean up the script text
            lines = [l.strip() for l in text.split('\n') if l.strip() and not l.startswith("Click the button")]
            return "\n".join(lines)
        except:
            return ""

    def scrape_alternatives(self, page):
        """Clicks 'Browse all alternatives' and scrapes each team's script."""
        variations = []
        
        try:
            # Click the button to open modal
            browse_btn = page.locator("a:has-text('Browse all alternatives')")
            if not browse_btn.is_visible():
                return []
            
            browse_btn.click()
            page.wait_for_selector("#alternatives_window", timeout=5000)
            
            # Get all rows in the modal
            rows = page.locator("#alternatives_window tr").all()
            
            # Skip header row if present (usually first row is header or empty)
            start_idx = 1 if len(rows) > 0 else 0
            
            # Limit to first 10 variations to avoid timeouts/excessive time per encounter
            # You can increase this limit if needed
            for i in range(start_idx, min(len(rows), 15)):
                row = rows[i]
                
                # Extract Team IDs
                pet_links = row.locator("a[href*='/Pet/']").all()
                team_ids = []
                for link in pet_links:
                    href = link.get_attribute("href")
                    if href:
                        m = re.search(r'/Pet/(\d+)/', href)
                        if m: team_ids.append(int(m.group(1)))
                
                # Pad with 0 if less than 3 pets
                while len(team_ids) < 3: team_ids.append(0)
                team_ids = team_ids[:3]

                # Click the row to load its script into the tooltip
                # We click the first cell to be safe
                try:
                    row.locator("td").first.click(timeout=1000)
                    page.wait_for_timeout(500) # Wait for tooltip update
                    
                    script = self.extract_script_from_modal(page)
                    
                    if script:
                        variations.append({
                            "team": team_ids,
                            "script": script
                        })
                except Exception as e:
                    print(f"      ! Failed to click row {i}: {e}")
                    continue

            # Close modal (Escape key)
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
            
        except Exception as e:
            print(f"    ! Error scraping alternatives: {e}")
            # Try to ensure modal is closed before continuing
            try: page.keyboard.press("Escape") 
            except: pass
            
        return variations

    def scrape_encounter_page(self, page, url):
        print(f"  Visiting: {url}")
        try:
            page.goto(url, wait_until="domcontentloaded")
            page.set_viewport_size({"width": 1920, "height": 1080})
            page.wait_for_timeout(2000) # Wait for JS
            
            # Try to close cookie banner
            try: page.locator("button:has-text('Agree')").click(timeout=1000)
            except: pass

        except Exception as e:
            print(f"    ! Error loading page: {e}")
            return []

        strategies = []
        
        # 1. Scrape the Main/Default Strategy first
        # (This logic remains similar to before, extracting from the main pane)
        main_strat = self._extract_data_from_pane(page.locator('body'), "Default Strategy")
        if main_strat['pet_slots'] or main_strat['script']:
            strategies.append(main_strat)

        # 2. Scrape Alternatives (The requested feature)
        # This extracts specific team+script combos from the modal
        alts = self.scrape_alternatives(page)
        if alts:
            print(f"    -> Found {len(alts)} alternative variations with scripts.")
            # Add these as separate strategy entries or store them specially
            # For now, we'll append them as strategies named "Variation X"
            for idx, alt in enumerate(alts):
                strategies.append({
                    "name": f"Variation {idx+1}",
                    "pet_slots": [[{'id': pid, 'name': 'Unknown'}] for pid in alt['team']], # Simplified structure
                    "script": alt['script'],
                    "is_variation": True
                })

        print(f"    -> Captured {len(strategies)} total strategies (including variations).")
        return strategies

    def _extract_data_from_pane(self, pane, name):
        strategy = {'name': name, 'pet_slots': [], 'script': ''}
        
        # 1. Extract Pets
        pets = []
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
            
        unique_pets = []
        seen = set()
        for p in pets:
            if p['id'] not in seen:
                seen.add(p['id'])
                unique_pets.append(p)
        pets = unique_pets

        if len(pets) >= 3:
            slot1, slot2, slot3 = [pets[0]], [pets[1]], [pets[2]]
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
        script_box = pane.locator('.code:visible, .script-box:visible, textarea.form-control:visible').first
        
        if script_box.count() > 0:
            tag = script_box.evaluate("el => el.tagName")
            if tag == 'TEXTAREA':
                script_text = script_box.input_value()
            else:
                script_text = script_box.inner_text()
        
        if not script_text:
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
