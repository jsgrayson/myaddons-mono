#!/usr/bin/env python3
"""
Extend recipe data with materials and skill information from Blizzard API.
Fetches detailed recipe data for crafting leveling guides.
"""

import os
import psycopg2
import requests
import time
import json
from dotenv import load_dotenv

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
    
    def get_recipe_details(self, recipe_id):
        """Get detailed recipe information including materials"""
        token = self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/data/wow/recipe/{recipe_id}"
        
        response = requests.get(
            url,
            params={
                'namespace': f'static-{self.region}',
                'locale': 'en_US'
            },
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code != 200:
            return None
            
        return response.json()

def get_db_connection():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def extend_recipe_table():
    """Add columns for materials and skill data"""
    conn = get_db_connection()
    if not conn:
        return False
    
    cur = conn.cursor()
    try:
        print("📊 Extending recipe_reference table...")
        cur.execute("""
            ALTER TABLE goblin.recipe_reference 
            ADD COLUMN IF NOT EXISTS materials JSONB,
            ADD COLUMN IF NOT EXISTS crafted_item_id INT,
            ADD COLUMN IF NOT EXISTS crafted_quantity INT DEFAULT 1,
            ADD COLUMN IF NOT EXISTS min_crafts INT,
            ADD COLUMN IF NOT EXISTS max_crafts INT
        """)
        conn.commit()
        print("✅ Table extended successfully")
        return True
    except Exception as e:
        print(f"❌ Error extending table: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def fetch_recipe_materials(limit=100):
    """Fetch materials for recipes from Blizzard API"""
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ Blizzard API credentials not found!")
        return 0
    
    conn = get_db_connection()
    if not conn:
        return 0
    
    client = BlizzardAPIClient(CLIENT_ID, CLIENT_SECRET)
    cur = conn.cursor()
    
    try:
        # Get recipes that don't have materials yet
        cur.execute("""
            SELECT recipe_id, recipe_name, profession_name
            FROM goblin.recipe_reference
            WHERE materials IS NULL
            ORDER BY recipe_id
            LIMIT %s
        """, (limit,))
        
        recipes = cur.fetchall()
        print(f"\n🔍 Fetching materials for {len(recipes)} recipes...")
        print(f"(Limiting to {limit} for this run)")
        
        updated = 0
        skipped = 0
        
        for recipe_id, recipe_name, profession in recipes:
            try:
                details = client.get_recipe_details(recipe_id)
                
                if not details:
                    skipped += 1
                    continue
                
                # Extract materials
                reagents = details.get('reagents', [])
                materials = []
                for reagent in reagents:
                    materials.append({
                        'item_id': reagent['reagent']['id'],
                        'quantity': reagent['quantity']
                    })
                
                # Extract crafted item
                crafted_item = details.get('crafted_item', {})
                crafted_item_id = crafted_item.get('id')
                crafted_quantity = details.get('crafted_quantity', {}).get('value', 1)
                
                # Update database
                cur.execute("""
                    UPDATE goblin.recipe_reference
                    SET materials = %s,
                        crafted_item_id = %s,
                        crafted_quantity = %s,
                        last_updated = CURRENT_TIMESTAMP
                    WHERE recipe_id = %s
                """, (
                    json.dumps(materials),
                    crafted_item_id,
                    crafted_quantity,
                    recipe_id
                ))
                
                updated += 1
                if updated % 10 == 0:
                    print(f"  ✅ Updated {updated}/{len(recipes)} recipes...")
                    conn.commit()
                
                time.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                print(f"  ⚠️  Error for recipe {recipe_id}: {e}")
                skipped += 1
                continue
        
        conn.commit()
        print(f"\n✅ Updated {updated} recipes with materials")
        print(f"⚠️  Skipped {skipped} recipes (API errors or missing data)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    
    return updated

def verify_materials():
    """Check how many recipes have materials"""
    conn = get_db_connection()
    if not conn:
        return
    
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            profession_name,
            COUNT(*) as total,
            COUNT(materials) as with_materials
        FROM goblin.recipe_reference
        GROUP BY profession_name
        ORDER BY total DESC
    """)
    
    print("\n📊 Recipe Materials Status:")
    print("-" * 60)
    for row in cur.fetchall():
        prof, total, with_mats = row
        pct = (with_mats / total * 100) if total > 0 else 0
        print(f"  {prof:20} - {with_mats:4}/{total:4} ({pct:5.1f}%)")
    print("-" * 60)
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("RECIPE MATERIALS IMPORT")
    print("=" * 60)
    
    # Extend table
    if not extend_recipe_table():
        print("Failed to extend table, exiting")
        exit(1)
    
    # Fetch materials (process ALL recipes)
    updated = fetch_recipe_materials(limit=10000)
    
    # Verify
    if updated > 0:
        verify_materials()
