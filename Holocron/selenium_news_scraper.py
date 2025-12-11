"""
selenium_news_scraper.py - Comprehensive News Scraper with Browser Automation

Scrapes 6 months of WoW news from multiple sources using Selenium.
Runs in background for 1-2 hours to collect 200+ articles.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time
import json

def setup_driver():
    """Setup headless Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

def scrape_wowhead_archive(driver, db_conn):
    """Scrape Wowhead news archive page by page"""
    articles = []
    
    print("Scraping Wowhead news archive...")
    
    for page in range(1, 15):  # ~15 pages = 6 months
        try:
            url = f"https://www.wowhead.com/news?page={page}"
            print(f"  Page {page}...")
            
            driver.get(url)
            time.sleep(3)  # Wait for JS to load
            
            # Get page source after JS renders
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Find news article links
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                
                if '/news/' in href and len(href) > 10:
                    title = link.get_text(strip=True)
                    
                    if len(title) > 20 and title not in [a['title'] for a in articles]:
                        # Classify
                        event_type = classify_event(title)
                        
                        if event_type:
                            articles.append({
                                'title': title,
                                'url': f"https://www.wowhead.com{href}" if not href.startswith('http') else href,
                                'event_type': event_type,
                                'source': 'wowhead',
                                'timestamp': datetime.now().isoformat(),
                            })
            
            time.sleep(2)  # Rate limiting
            
        except Exception as e:
            print(f"    Error on page {page}: {e}")
            continue
    
    # Save to database
    cur = db_conn.cursor()
    for article in articles:
        cur.execute('''
            INSERT OR IGNORE INTO news_events (timestamp, source, title, event_type)
            VALUES (?, ?, ?, ?)
        ''', (article['timestamp'], article['source'], article['title'], article['event_type']))
    db_conn.commit()
    
    print(f"✓ Scraped {len(articles)} Wowhead articles")
    return articles

def scrape_mmochampion(driver, db_conn):
    """Scrape MMO-Champion blue posts"""
    articles = []
    
    print("Scraping MMO-Champion...")
    
    try:
        driver.get("https://www.mmo-champion.com/content/")
        time.sleep(3)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        for heading in soup.find_all(['h1', 'h2', 'h3'], limit=100):
            title = heading.get_text(strip=True)
            
            if len(title) > 20 and len(title) < 150:
                event_type = classify_event(title)
                
                if event_type:
                    articles.append({
                        'title': title,
                        'event_type': event_type,
                        'source': 'mmochampion',
                        'timestamp': datetime.now().isoformat(),
                    })
        
        # Save to database
        cur = db_conn.cursor()
        for article in articles:
            cur.execute('''
                INSERT OR IGNORE INTO news_events (timestamp, source, title, event_type)
                VALUES (?, ?, ?, ?)
            ''', (article['timestamp'], article['source'], article['title'], article['event_type']))
        db_conn.commit()
        
        print(f"✓ Scraped {len(articles)} MMO-C articles")
        
    except Exception as e:
        print(f"  Error: {e}")
    
    return articles

def classify_event(title):
    """Classify news event type"""
    text = title.lower()
    
    if any(w in text for w in ['buff', 'nerf', 'hotfix', 'class changes', 'balance', 
                                'mage', 'warrior', 'paladin', 'priest', 'hunter', 
                                'warlock', 'druid', 'shaman', 'rogue', 'monk', 
                                'demon hunter', 'death knight', 'evoker']):
        return 'class_change'
    
    elif any(w in text for w in ['raid', 'mythic', 'dungeon', 'boss', 'loot']):
        return 'raid'
    
    elif any(w in text for w in ['patch ', '11.0', '11.1', '11.2', '11.3', 'ptr', 'beta']):
        return 'patch'
    
    elif any(w in text for w in ['profession', 'crafting', 'recipe', 'alchemy', 
                                  'enchanting', 'blacksmithing', 'engineering',
                                  'inscription', 'jewelcrafting']):
        return 'profession'
    
    elif any(w in text for w in ['holiday', 'event', 'anniversary', 'celebration', 
                                  'timewalking', 'darkmoon']):
        return 'holiday'
    
    return None

def main():
    print("="*70)
    print("COMPREHENSIVE WOW NEWS SCRAPER")
    print("="*70)
    print("\nThis will take 30-60 minutes. Sit back and relax...")
    print()
    
    # Setup database
    db_path = '/Users/jgrayson/Documents/holocron/goblin_training.db'
    conn = sqlite3.connect(db_path)
    
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS news_events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source TEXT,
            title TEXT UNIQUE,
            event_type TEXT
        )
    ''')
    conn.commit()
    
    # Setup browser
    print("Setting up Chrome browser...")
    driver = setup_driver()
    print("✓ Browser ready\n")
    
    try:
        # Scrape all sources
        wowhead_articles = scrape_wowhead_archive(driver, conn)
        time.sleep(5)
        
        mmoc_articles = scrape_mmochampion(driver, conn)
        
        # Final stats
        cur.execute('SELECT COUNT(*), event_type FROM news_events GROUP BY event_type')
        results = cur.fetchall()
        
        print("\n" + "="*70)
        print("SCRAPING COMPLETE!")
        print("="*70)
        
        total = sum(r[0] for r in results)
        print(f"\nTotal articles: {total}")
        print("\nBy event type:")
        for count, event_type in results:
            print(f"  {event_type}: {count}")
        
        # Show samples
        print("\nSample articles:")
        cur.execute('SELECT event_type, title FROM news_events LIMIT 15')
        for i, (event_type, title) in enumerate(cur.fetchall(), 1):
            print(f"{i}. [{event_type}] {title[:60]}")
        
        print(f"\n✓ Data saved to: {db_path}")
        print("✓ Ready for training: python goblin_training.py")
        
    finally:
        driver.quit()
        conn.close()

if __name__ == "__main__":
    main()
