"""
Fetch complete WoW battle pet species from Blizzard API
This will give us ALL ~3000+ battlepets to populate the database
"""

import requests
import json
import time
import os

# Load from .env file
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

def fetch_all_species():
    """Fetch all battle pet species from Blizzard API"""
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get pet species index
    url = "https://us.api.blizzard.com/data/wow/pet/index"
    params = {"namespace": "static-us", "locale": "en_US"}
    
    response = requests.get(url, headers=headers, params=params)
    pets_index = response.json()
    
    print(f"Found {len(pets_index.get('pets', []))} total pet species!")
    
    # Save all species IDs
    all_species = {}
    for pet in pets_index.get('pets', []):
        species_id = pet['id']
        species_name = pet['name']
        all_species[species_id] = {
            'id': species_id,
            'name': species_name
        }
    
    # Save to file
    with open('all_wow_pets.json', 'w') as f:
        json.dump(all_species, f, indent=2)
    
    print(f"✅ Saved {len(all_species)} pet species to all_wow_pets.json")
    return all_species

if __name__ == "__main__":
    if not CLIENT_ID or not CLIENT_SECRET:
        print("⚠️  Could not load Blizzard API credentials from .env file!")
        print("Make sure .env has BLIZZARD_CLIENT_ID and BLIZZARD_CLIENT_SECRET")
    else:
        print(f"✅ Loaded credentials from .env")
        fetch_all_species()
