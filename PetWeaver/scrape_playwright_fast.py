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
        """Aggressive scrolling to ensure all lazy content loads."""
        # Scroll down in large chunks
        for i in range(10):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(500)
            
            # Check if a "Load More" button exists and click it
            try:
                load_more = page.locator("button:has-text('Load more')")
                if load_more.is_visible():
                    load_more.click()
                    page.wait_for_timeout(1000)
            except: pass

    def extract_script_from_modal(self, page):
        """Extracts script from tooltip or clipboard button."""
        script_text = ""
        try:
            # 1. Try Tooltip
            tooltip = page.locator("#td_tooltip")
            if tooltip.is_visible():
                text = tooltip.inner_text()
                lines = [l.strip() for l in text.split('\n') if l.strip() and not l.startswith("Click the button")]
                script_text = "\n".join(lines)
            
            # 2. Try "Copy Script" button if tooltip failed
            if not script_text:
                copy_btn = page.locator(".fa-copy").first
                if copy_btn.is_visible():
                    # We can't easily read clipboard in headless, so we rely on tooltip/display
                    pass
        except: pass
        return script_text

    def scrape_alternatives(self, page):
        """Fast scrape of alternatives."""
        variations = []
        try:
            browse_btn = page.locator("a:has-text('Browse all alternatives')")
            if not browse_btn.is_visible(): return []
            
            browse_btn.click()
            page.wait_for_selector("#alternatives_window", timeout=3000)
            
            # Get all rows
            rows = page.locator("#alternatives_window tr").all()
            
            # Limit to first 5 variations for SPEED
            for i in range(1, min(len(rows), 6)):
                row = rows[i]
                
                # Extract IDs quickly
                html = row.inner_html()
                team_ids = [int(x) for x in re.findall(r'/Pet/(\d+)/', html)]
                while len(team_ids) < 3: team_ids.append(0)
                team_ids = team_ids[:3]

                # Click row to trigger script display
                try:
                    row.locator("td").first.click(timeout=300)
                    page.wait_for_timeout(200) # Short wait
                    
                    script = self.extract_script_from_modal(page)
                    if script:
                        variations.append({"team": team_ids, "script": script})
                except: continue

            page.keyboard.press("Escape")
        except: 
            try: page.keyboard.press("Escape") 
            except: pass
            
        return variations

    def scrape_encounter_page(self, page, url):
        # Optimization: Don't print every URL to reduce I/O lag
        try:
            page.goto(url, wait_until="domcontentloaded")
            
            # Quick check for main script
            main_script = ""
            try:
                main_script = page.locator('.code, .script-box, textarea.form-control').first.inner_text()
            except: pass

            strategies = []
            if main_script:
                strategies.append({
                    "name": "Default",
                    "pet_slots": [], # We can skip detailed pet parsing for speed if needed
                    "script": main_script
                })

            # Quick check for alternatives
            alts = self.scrape_alternatives(page)
            for alt in alts:
                strategies.append({
                    "name": "Variation",
                    "pet_slots": [[{'id': pid, 'name': 'Unknown'}] for pid in alt['team']],
                    "script": alt['script'],
                    "is_variation": True
                })
                
            return strategies

        except: return []

    def scrape_category(self, context, category_url):
        print(f"Scanning: {category_url}")
        page = context.new_page()
        try:
            page.goto(category_url, wait_until="domcontentloaded")
            self.auto_scroll(page)
            
            # Extract all links at once
            links = page.evaluate("""() => {
                return Array.from(document.querySelectorAll('a[href*="/Strategy/"], a[href*="/Encounter/"]'))
                    .map(a => ({text: a.innerText, href: a.href}))
                    .filter(a => a.text.length > 3 && !a.text.includes('Comment'));
            }""")
            
            seen = set()
            encounters = []
            for link in links:
                if link['href'] not in seen:
                    seen.add(link['href'])
                    encounters.append({'name': link['text'], 'url': link['href']})
            
            page.close()
            return encounters
        except: 
            page.close()
            return []

    def run(self):
        print("Starting Optimized Parallel Scraper...")
        
        categories = {
            "Pandaria": ["/Section/19/Pandaren_Spirit_Tamers", "/Section/20/Beasts_of_Fable"],
            "Draenor": ["/Section/38/Draenor_Tamers"],
            "The War Within": ["/Section/104/World_Quests"]
        }

        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            
            for expansion, paths in categories.items():
                self.data[expansion] = {}
                
                for path in paths:
                    full_path = f"{self.base_url}{path}"
                    encounters = self.scrape_category(context, full_path)
                    print(f"  Found {len(encounters)} encounters. Scraping details...")
                    
                    # Process encounters in chunks to manage memory/tabs
                    cat_data = []
                    for i, enc in enumerate(encounters):
                        # Re-use a single page for details to avoid opening/closing overhead
                        page = context.new_page()
                        strategies = self.scrape_encounter_page(page, enc['url'])
                        page.close()
                        
                        if strategies:
                            cat_data.append({
                                'encounter_name': enc['name'],
                                'url': enc['url'],
                                'strategies': strategies
                            })
                        
                        if i % 5 == 0: print(f"    Processed {i}/{len(encounters)}")
                            
                    self.data[expansion][path] = cat_data
            
            browser.close()
            
        with open('strategies_fast.json', 'w') as f:
            json.dump(self.data, f, indent=2)
        print("\n✅ Done! Saved to strategies_fast.json")

if __name__ == "__main__":
    scraper = XuFuBrowserScraper()
    scraper.run()
