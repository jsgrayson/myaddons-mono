#!/usr/bin/env python3
"""
Fetch complete species data from Blizzard API
This will fill in all missing family/type, icons, descriptions, and source info
"""

import requests
import json
import time
import sqlite3
import os
from datetime import datetime

# Load credentials from .env
def load_env():
    env = {}
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env[key] = value
    return env

env = load_env()
CLIENT_ID = env.get('BLIZZARD_CLIENT_ID')
CLIENT_SECRET = env.get('BLIZZARD_CLIENT_SECRET')

def get_access_token():
    """Get OAuth token from Blizzard"""
    url = "https://oauth.battle.net/token"
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    return response.json()['access_token']

def fetch_species_details(species_id, token):
    """Fetch detailed info for a specific species"""
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://us.api.blizzard.com/data/wow/pet/{species_id}"
    params = {"namespace": "static-us", "locale": "en_US"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None  # Species doesn't exist
        else:
            print(f"Warning: Status {response.status_code} for species {species_id}")
            return None
    except Exception as e:
        print(f"Error fetching species {species_id}: {e}")
        return None

def update_species_in_db(conn, species_id, data):
    """Update species with fetched data"""
    cursor = conn.cursor()
    
    # Extract data
    name = data.get('name', '')
    battle_pet_type = data.get('battle_pet_type', {})
    pet_type = battle_pet_type.get('id') if battle_pet_type else None
    
    description = data.get('description', '')
    source = data.get('source', {}).get('name', '')
    is_capturable = data.get('is_capturable', False)
    is_tradable = data.get('is_tradable', False)
    is_battlepet = data.get('is_battlepet', True)
    
    # Icon - get from media if available
    icon_url = ''
    media = data.get('media', {})
    if media and 'key' in media:
        # Could fetch media URL but for now just note we have it
        icon_url = media.get('key', {}).get('href', '')
    
    cursor.execute('''
        UPDATE species 
        SET name = COALESCE(NULLIF(?, ''), name),
            pet_type = COALESCE(?, pet_type),
            can_battle = COALESCE(?, can_battle),
            is_tradable = COALESCE(?, is_tradable),
            source_text = COALESCE(NULLIF(?, ''), source_text),
            description = COALESCE(NULLIF(?, ''), description),
            is_capturable = COALESCE(?, is_capturable),
            icon = COALESCE(NULLIF(?, ''), icon)
        WHERE species_id = ?
    ''', (name, pet_type, is_battlepet, is_tradable, source, description, is_capturable, icon_url, species_id))
    
    return cursor.rowcount > 0

def main():
    print("🔍 Fetching complete species data from Blizzard API...")
    print(f"Started at: {datetime.now().strftime('%H:%M:%S')}")
    
    # Get all species IDs from database
    conn = sqlite3.connect('petweaver.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT species_id, name FROM species WHERE pet_type IS NULL ORDER BY species_id")
    missing_type = cursor.fetchall()
    
    print(f"Found {len(missing_type)} species missing family/type data")
    print(f"Will fetch data with rate limiting (may take a few minutes)...")
    
    # Get token
    token = get_access_token()
    print(f"✅ Got API access token")
    
    updated_count = 0
    failed_count = 0
    not_found_count = 0
    
    for i, (species_id, current_name) in enumerate(missing_type, 1):
        if i % 50 == 0:
            print(f"Progress: {i}/{len(missing_type)} ({i/len(missing_type)*100:.1f}%)")
        
        # Rate limiting - 100 requests per second max, so wait 10ms between requests
        time.sleep(0.01)
        
        data = fetch_species_details(species_id, token)
        
        if data:
            if update_species_in_db(conn, species_id, data):
                updated_count += 1
            else:
                failed_count += 1
        else:
            not_found_count += 1
        
        # Commit every 100 species
        if i % 100 == 0:
            conn.commit()
    
    # Final commit
    conn.commit()
    
    # Show final stats
    cursor.execute("SELECT COUNT(*) FROM species WHERE pet_type IS NOT NULL")
    total_with_type = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM species")
    total_species = cursor.fetchone()[0]
    
    print(f"\n📊 Results:")
    print(f"  Updated: {updated_count}")
    print(f"  Not Found: {not_found_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Total with Type: {total_with_type}/{total_species} ({total_with_type/total_species*100:.1f}%)")
    print(f"\nCompleted at: {datetime.now().strftime('%H:%M:%S')}")
    
    conn.close()

if __name__ == "__main__":
    if not CLIENT_ID or not CLIENT_SECRET:
        print("⚠️  Missing Blizzard API credentials in .env")
        exit(1)
    main()
