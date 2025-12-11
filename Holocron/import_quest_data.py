#!/usr/bin/env python3
"""
Import quest data from Blizzard API for The Codex module.
Fetches quest definitions, prerequisites, and build quest chains.
"""

import os
import os
import sqlite3
import requests
import time
import json
from dotenv import load_dotenv

load_dotenv()

DB_FILE = "/Users/jgrayson/Documents/holocron/holocron.db"
CLIENT_ID = os.getenv('BLIZZARD_CLIENT_ID')
CLIENT_SECRET = os.getenv('BLIZZARD_CLIENT_SECRET')

class BlizzardAPIClient:
    """Client for Blizzard's WoW Game Data API"""
    
    def __init__(self, client_id, client_secret, region='us'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.region = region
        self.token = None
        self.token_expires = 0
        
    def get_access_token(self):
        """Get OAuth access token"""
        if self.token and time.time() < self.token_expires:
            return self.token
            
        url = f"https://{self.region}.battle.net/oauth/token"
        response = requests.post(
            url,
            data={'grant_type': 'client_credentials'},
            auth=(self.client_id, self.client_secret)
        )
        response.raise_for_status()
        
        data = response.json()
        self.token = data['access_token']
        self.token_expires = time.time() + data['expires_in'] - 60
        
        return self.token
    
    def get_quest_categories(self):
        """Get list of quest categories"""
        token = self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/data/wow/quest/category/index"
        
        response = requests.get(
            url,
            params={'namespace': f'static-{self.region}', 'locale': 'en_US'},
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code != 200:
            print(f"Quest categories failed: {response.status_code}")
            return {}
        
        return response.json()
    
    def get_quests_by_category(self, category_id):
        """Get quests in a specific category"""
        token = self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/data/wow/quest/category/{category_id}"
        
        response = requests.get(
            url,
            params={'namespace': f'static-{self.region}', 'locale': 'en_US'},
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code != 200:
            return {}
        
        return response.json()
    
    def get_quest_details(self, quest_id):
        """Get detailed quest information"""
        token = self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/data/wow/quest/{quest_id}"
        
        response = requests.get(
            url,
            params={'namespace': f'static-{self.region}', 'locale': 'en_US'},
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code != 200:
            return None
        
        return response.json()

def get_db_connection():
    """Connect to SQLite database"""
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def create_quest_tables():
    """Create quest data tables if they don't exist"""
    conn = get_db_connection()
    if not conn:
        return False
    
    cur = conn.cursor()
    try:
        print("📊 Creating quest tables...")
        
        # Quest definitions table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS quest_definitions (
                quest_id INTEGER PRIMARY KEY,
                title TEXT,
                min_level INTEGER,
                max_level INTEGER,
                area_name TEXT,
                description TEXT,
                rewards_json TEXT,
                x_coord REAL,
                y_coord REAL,
                map_id INTEGER,
                category_id INTEGER,
                category_name TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Quest dependencies table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS quest_dependencies (
                quest_id INTEGER,
                required_quest_id INTEGER,
                PRIMARY KEY (quest_id, required_quest_id)
            )
        """)
        
        conn.commit()
        print("✅ Quest tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def import_quests(limit=50):
    """Import quest data from Blizzard API"""
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ Blizzard API credentials not found!")
        return 0
    
    conn = get_db_connection()
    if not conn:
        return 0
    
    client = BlizzardAPIClient(CLIENT_ID, CLIENT_SECRET)
    cur = conn.cursor()
    
    try:
        print("\n🔍 Fetching quest categories...")
        categories = client.get_quest_categories()
        
        quest_cats = categories.get('categories', [])
        print(f"✅ Found {len(quest_cats)} quest categories")
        
        imported = 0
        
        # Process all categories
        for cat in quest_cats:
            cat_id = cat['id']
            cat_name = cat.get('category', {}).get('name', 'Unknown')
            
            print(f"\n📋 Category: {cat_name} (ID: {cat_id})")
            
            # Get quests in this category
            cat_data = client.get_quests_by_category(cat_id)
            quests = cat_data.get('quests', [])
            
            print(f"  Found {len(quests)} quests")
            
            for quest in quests:
                quest_id = quest['id']
                
                # Get quest details
                details = client.get_quest_details(quest_id)
                if not details:
                    continue
                
                title = details.get('title', 'Unknown')
                requirements = details.get('requirements', {})
                min_level = requirements.get('min_character_level')
                max_level = requirements.get('max_character_level')
                area = details.get('area', {}).get('name')
                
                # Coordinates (Start Location)
                x_coord = None
                y_coord = None
                map_id = None
                
                start_loc = details.get('start_location')
                if start_loc:
                    map_info = start_loc.get('map', {})
                    map_id = map_info.get('id')
                    # Blizzard API coords are often 0-100 or 0-1, normalizing to 0-100 for display
                    # API usually returns 0.505 for 50.5
                    raw_x = start_loc.get('x', 0)
                    raw_y = start_loc.get('y', 0)
                    
                    x_coord = round(raw_x * 100, 1)
                    y_coord = round(raw_y * 100, 1)
                
                # Insert quest
                cur.execute("""
                    INSERT INTO quest_definitions 
                    (quest_id, title, min_level, max_level, area_name, x_coord, y_coord, map_id, category_id, category_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT (quest_id) DO UPDATE SET
                        title = excluded.title,
                        x_coord = excluded.x_coord,
                        y_coord = excluded.y_coord,
                        map_id = excluded.map_id,
                        category_id = excluded.category_id,
                        category_name = excluded.category_name,
                        last_updated = CURRENT_TIMESTAMP
                """, (quest_id, title, min_level, max_level, area, x_coord, y_coord, map_id, cat_id, cat_name))
                
                # Process Dependencies (Quest Chain)
                # Blizzard API often puts this in 'requirements' -> 'min_quest_id' or 'quests' list
                # Checking for 'requirements' -> 'quest' -> 'id'
                req_quest_id = None
                req_quest = requirements.get('quest')
                if req_quest:
                    req_quest_id = req_quest.get('id')
                
                if req_quest_id:
                    cur.execute("""
                        INSERT OR IGNORE INTO quest_dependencies (quest_id, required_quest_id)
                        VALUES (?, ?)
                    """, (quest_id, req_quest_id))
                
                imported += 1
                if imported % 10 == 0:
                    print(f"  ✅ Imported {imported} quests...")
                    conn.commit()
                
                time.sleep(0.1)
            
            time.sleep(0.5)
        
        conn.commit()
        print(f"\n✅ Imported {imported} quests")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    
    return imported

if __name__ == "__main__":
    print("=" * 60)
    print("QUEST DATA IMPORT")
    print("=" * 60)
    
    # Create tables
    if not create_quest_tables():
        print("Failed to create tables, exiting")
        exit(1)
    
    # Import quests
    imported = import_quests()
    
    if imported > 0:
        print(f"\n✅ Successfully imported {imported} quests")
    else:
        print("\n⚠️  No quests imported")
