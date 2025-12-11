#!/usr/bin/env python3
"""
Fetch profession recipe data from Blizzard's Game Data API
Populates the database with real recipe information
"""

import os
import psycopg2
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://jgrayson@localhost/holocron')
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
    
    def get_profession_index(self):
        """Get list of all professions"""
        token = self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/data/wow/profession/index"
        
        response = requests.get(
            url,
            params={
                'namespace': f'static-{self.region}',
                'locale': 'en_US'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code != 200:
            print(f"❌ Profession index failed: {response.status_code}")
            print(f"URL: {url}")
            print(f"Response: {response.text[:200]}")
            return {}
            
        return response.json()
    
    def get_profession_details(self, profession_id):
        """Get profession details including skill tiers"""
        token = self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/data/wow/profession/{profession_id}"
        
        response = requests.get(
            url,
            params={
                'namespace': f'static-{self.region}',
                'locale': 'en_US'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code != 200:
            return {}
            
        return response.json()
    
    def get_skill_tier(self, profession_id, skill_tier_id):
        """Get specific skill tier with recipes"""
        token = self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/data/wow/profession/{profession_id}/skill-tier/{skill_tier_id}"
        
        response = requests.get(
            url,
            params={
                'namespace': f'static-{self.region}',
                'locale': 'en_US'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code != 200:
            return {}
            
        return response.json()

def get_db_connection():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def import_recipes():
    """Fetch and import recipe data from Blizzard API"""
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ Blizzard API credentials not found!")
        print("Please set BLIZZARD_CLIENT_ID and BLIZZARD_CLIENT_SECRET in .env")
        return 0
    
    conn = get_db_connection()
    if not conn:
        return 0
    
    client = BlizzardAPIClient(CLIENT_ID, CLIENT_SECRET)
    cur = conn.cursor()
    total_recipes = 0  # Initialize here
    
    try:
        # Create recipe reference table if needed
        cur.execute("""
            CREATE TABLE IF NOT EXISTS goblin.recipe_reference (
                recipe_id INT PRIMARY KEY,
                recipe_name VARCHAR(255),
                profession_name VARCHAR(100),
                profession_id INT,
                skill_tier_name VARCHAR(100),
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        
        print("=" * 60)
        print("BLIZZARD API RECIPE IMPORT")
        print("=" * 60)
        
        # Get profession list
        print("\n🔍 Fetching profession list...")
        prof_index = client.get_profession_index()
        professions = prof_index.get('professions', [])
        
        print(f"✅ Found {len(professions)} total professions")
        print(f"Professions: {', '.join([p['name'] for p in professions])}")
        
        total_recipes = 0
        
        for prof in professions:  # Import ALL professions from the API
            prof_id = prof['id']
            prof_name = prof['name']
            
            print(f"\n📖 {prof_name} (ID: {prof_id})")
            
            try:
                # Get profession details
                prof_details = client.get_profession_details(prof_id)
                skill_tiers = prof_details.get('skill_tiers', [])
                
                print(f"  Found {len(skill_tiers)} skill tiers (expansions)")
                
                # Import recipes from ALL skill tiers (all expansions)
                for tier in skill_tiers:
                    tier_name = tier['name']
                    print(f"  📚 {tier_name}")
                    
                    # Get recipes from this tier
                    tier_data = client.get_skill_tier(prof_id, tier['id'])
                    categories = tier_data.get('categories', [])
                    
                    tier_recipe_count = 0
                    for category in categories:
                        recipes = category.get('recipes', [])
                        
                        for recipe in recipes:  # Import ALL recipes
                            cur.execute("""
                                INSERT INTO goblin.recipe_reference 
                                (recipe_id, recipe_name, profession_name, profession_id, skill_tier_name)
                                VALUES (%s, %s, %s, %s, %s)
                                ON CONFLICT (recipe_id) 
                                DO UPDATE SET
                                    recipe_name = EXCLUDED.recipe_name,
                                    last_updated = CURRENT_TIMESTAMP
                            """, (recipe['id'], recipe['name'], prof_name, prof_id, tier_name))
                            total_recipes += 1
                            tier_recipe_count += 1
                    
                    print(f"    ✅ Imported {tier_recipe_count} recipes from {tier_name}")
                    time.sleep(0.5)  # Small delay between tiers
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"  ❌ Error fetching {prof_name}: {e}")
                continue
        
        conn.commit()
        print(f"\n✅ Imported {total_recipes} recipes from Blizzard API")
        
        # Verify
        cur.execute("SELECT profession_name, COUNT(*) FROM goblin.recipe_reference GROUP BY profession_name")
        print("\n📊 Recipe Summary:")
        print("-" * 50)
        for row in cur.fetchall():
            print(f"  {row[0]:20} - {row[1]:4} recipes")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    
    return total_recipes

if __name__ == "__main__":
    import_recipes()
