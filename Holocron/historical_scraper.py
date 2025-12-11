"""
historical_scraper.py - Scrape Historical News & Market Data

Scrapes:
1. Wowhead news archives (last 6 months)
2. TheUndermineJournal price history
3. Correlates events with price movements
4. Imports into PostgreSQL for training

Usage:
    python historical_scraper.py --months 6 --realm "Area 52"
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import json
import psycopg2
import os
from typing import List, Dict, Tuple
import re

# ============================================================================
# Wowhead News Archive Scraper
# ============================================================================

class WowheadArchiveScraper:
    def __init__(self):
        self.base_url = "https://www.wowhead.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def scrape_news_archive(self, months_back: int = 6) -> List[Dict]:
        """
        Scrape Wowhead news articles from the last N months
        
        Returns:
            List of news articles with title, date, content
        """
        articles = []
        
        # Wowhead news page structure
        news_url = f"{self.base_url}/news"
        
        print(f"Scraping Wowhead news from last {months_back} months...")
        
        # Pagination through news pages
        for page in range(1, 20):  # ~20 pages should cover 6 months
            print(f"  Page {page}...")
            
            try:
                response = self.session.get(f"{news_url}?page={page}", timeout=15)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find news article links (adjust selectors as needed)
                article_links = soup.find_all('a', class_=re.compile(r'.*news.*'))
                
                for link in article_links[:10]:  # Process top 10 per page
                    href = link.get('href')
                    if not href or not href.startswith('/news/'):
                        continue
                    
                    article_url = f"{self.base_url}{href}"
                    article_data = self._scrape_article(article_url)
                    
                    if article_data and self._within_timeframe(article_data['date'], months_back):
                        articles.append(article_data)
                    
                    time.sleep(0.5)  # Rate limiting
                
                # Stop if we're past our timeframe
                if articles and not self._within_timeframe(articles[-1]['date'], months_back):
                    break
                    
            except Exception as e:
                print(f"Error on page {page}: {e}")
                continue
        
        print(f"Scraped {len(articles)} Wowhead articles")
        return articles
    
    def _scrape_article(self, url: str) -> Dict:
        """Scrape individual article content"""
        try:
            response = self.session.get(url, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title_elem = soup.find('h1')
            title = title_elem.get_text(strip=True) if title_elem else "Unknown"
            
            # Extract date
            date_elem = soup.find('time')
            date_str = date_elem.get('datetime') if date_elem else None
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00')) if date_str else datetime.now()
            
            # Extract content
            content_elem = soup.find('div', class_=re.compile(r'.*article.*content.*'))
            content = content_elem.get_text(strip=True)[:500] if content_elem else ""
            
            # Classify event type
            event_type = self._classify_event(title, content)
            
            return {
                "source": "wowhead",
                "title": title,
                "url": url,
                "date": date,
                "content": content,
                "event_type": event_type,
            }
        except Exception as e:
            print(f"Error scraping article {url}: {e}")
            return None
    
    def _classify_event(self, title: str, content: str) -> str:
        """Classify news event type"""
        text = (title + " " + content).lower()
        
        if any(word in text for word in ['buff', 'nerf', 'hotfix', 'balance']):
            return 'class_change'
        elif any(word in text for word in ['raid', 'mythic', 'dungeon']):
            return 'raid'
        elif any(word in text for word in ['patch', 'update', 'ptr']):
            return 'patch'
        elif any(word in text for word in ['holiday', 'event', 'anniversary']):
            return 'holiday'
        elif any(word in text for word in ['profession', 'crafting', 'recipe']):
            return 'profession'
        else:
            return 'general'
    
    def _within_timeframe(self, date: datetime, months: int) -> bool:
        """Check if date is within timeframe"""
        cutoff = datetime.now() - timedelta(days=months * 30)
        return date >= cutoff

# ============================================================================
# TheUndermineJournal Price Data Scraper
# ============================================================================

class UndermineJournalScraper:
    def __init__(self, realm: str = "area-52", region: str = "us"):
        self.base_url = "https://theunderminejournal.com"
        self.realm = realm.lower().replace(" ", "-")
        self.region = region.lower()
        self.session = requests.Session()
    
    def scrape_item_history(self, item_id: int, days_back: int = 180) -> List[Dict]:
        """
        Scrape price history for an item
        
        Returns:
            List of {timestamp, price, quantity} dicts
        """
        # TheUndermineJournal uses data endpoints
        # Example: https://theunderminejournal.com/api/history.php?house=XXX&item=210814
        
        # Get house ID for realm
        house_id = self._get_house_id()
        
        if not house_id:
            print(f"Could not find house ID for {self.realm}")
            return []
        
        url = f"{self.base_url}/api/history.php"
        params = {
            'house': house_id,
            'item': item_id,
        }
        
        try:
            response = self.session.get(url, params=params, timeout=15)
            data = response.json()
            
            # Parse response (format may vary)
            history = []
            
            if 'stats' in data:
                for entry in data['stats']:
                    timestamp = datetime.fromtimestamp(entry.get('when', 0))
                    price = entry.get('price', 0)
                    quantity = entry.get('quantity', 0)
                    
                    # Filter to timeframe
                    cutoff = datetime.now() - timedelta(days=days_back)
                    if timestamp >= cutoff:
                        history.append({
                            'timestamp': timestamp,
                            'price': price,
                            'quantity': quantity,
                        })
            
            return history
            
        except Exception as e:
            print(f"Error scraping item {item_id}: {e}")
            return []
    
    def _get_house_id(self) -> int:
        """Get house ID for realm"""
        # TheUndermineJournal house IDs
        # This would normally query their API or scrape the realm list
        # For now, return common house IDs
        
        house_map = {
            'area-52': 113,
            'illidan': 3,
            'stormrage': 60,
            'tichondrius': 11,
            # Add more as needed
        }
        
        return house_map.get(self.realm, 113)  # Default to Area 52
    
    def bulk_scrape_items(self, item_ids: List[int], days_back: int = 180) -> Dict[int, List[Dict]]:
        """
        Scrape multiple items with rate limiting
        
        Returns:
            Dict mapping item_id -> price history
        """
        results = {}
        
        print(f"Scraping {len(item_ids)} items from TheUndermineJournal...")
        
        for i, item_id in enumerate(item_ids):
            print(f"  [{i+1}/{len(item_ids)}] Item {item_id}...")
            
            history = self.scrape_item_history(item_id, days_back)
            results[item_id] = history
            
            time.sleep(1)  # Rate limiting - 1 request per second
        
        return results

# ============================================================================
# Database Importer
# ============================================================================

class HistoricalDataImporter:
    def __init__(self, db_connection):
        self.conn = db_connection
    
    def import_news_events(self, articles: List[Dict]):
        """Import news articles into database"""
        cur = self.conn.cursor()
        
        print(f"Importing {len(articles)} news events...")
        
        for article in articles:
            cur.execute("""
                INSERT INTO auctionhouse.news_events 
                (timestamp, source, title, content, event_type)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                article['date'],
                article['source'],
                article['title'],
                article['content'],
                article['event_type'],
            ))
        
        self.conn.commit()
        cur.close()
        
        print("News events imported successfully")
    
    def import_price_history(self, item_id: int, history: List[Dict]):
        """Import price history for an item"""
        cur = self.conn.cursor()
        
        # Create a synthetic scan for each price point
        for entry in history:
            # Insert scan
            cur.execute("""
                INSERT INTO auctionhouse.scans 
                (realm, faction, character, timestamp, item_count)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING scan_id
            """, ('Historical', 'Both', 'Scraper', entry['timestamp'], 1))
            
            scan_id = cur.fetchone()[0]
            
            # Insert scan item
            cur.execute("""
                INSERT INTO auctionhouse.scan_items 
                (scan_id, item_id, price, quantity)
                VALUES (%s, %s, %s, %s)
            """, (scan_id, item_id, entry['price'], entry['quantity']))
        
        self.conn.commit()
        cur.close()

# ============================================================================
# Main Scraping Workflow
# ============================================================================

def scrape_and_import(months: int = 6, realm: str = "Area 52"):
    """
    Main workflow: Scrape news + prices, import to database
    """
    print("=" * 60)
    print("HISTORICAL DATA SCRAPER")
    print("=" * 60)
    
    # Connect to database
    db_url = os.environ.get('DATABASE_URL')
    conn = None
    
    if db_url:
        try:
            conn = psycopg2.connect(db_url)
        except Exception as e:
            print(f"⚠️ Database connection failed: {e}")
    
    if not conn:
        print("Running in FILE-ONLY mode (saving to scraped_data.json)")
    
    # Step 1: Scrape news
    news_scraper = WowheadArchiveScraper()
    # For dev speed, limit to 1 month if no DB
    months_to_scrape = months if conn else 1
    articles = news_scraper.scrape_news_archive(months_back=months_to_scrape)
    
    # Step 2: Import news
    if conn:
        importer = HistoricalDataImporter(conn)
        importer.import_news_events(articles)
    
    # Step 3: Identify items mentioned in news
    # For MVP, use common items
    common_items = [
        210814,  # Algari Mana Potion
        211515,  # Null Stone
        210816,  # Algari Healing Potion
        212754,  # Enchant Weapon - Authority of Storms
        # Add more item IDs
    ]
    
    # Step 4: Scrape price history
    price_scraper = UndermineJournalScraper(realm=realm)
    price_data = price_scraper.bulk_scrape_items(common_items, days_back=months * 30)
    
    # Step 5: Import price history or Save to File
    if conn:
        for item_id, history in price_data.items():
            if history:
                print(f"Importing {len(history)} price points for item {item_id}...")
                importer.import_price_history(item_id, history)
        conn.close()
    else:
        # Save to file
        output = {
            "news": articles,
            "prices": price_data
        }
        with open('scraped_data.json', 'w') as f:
            json.dump(output, f, indent=2, default=str)
        print("Saved scraped data to scraped_data.json")
    
    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE!")
    print(f"Imported {len(articles)} news events")
    print(f"Imported price history for {len(price_data)} items")
    print("Ready for training: python goblin_training.py")
    print("=" * 60)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape historical WoW market data')
    parser.add_argument('--months', type=int, default=6, help='Months of history to scrape')
    parser.add_argument('--realm', type=str, default='Area 52', help='WoW realm name')
    
    args = parser.parse_args()
    
    scrape_and_import(months=args.months, realm=args.realm)
