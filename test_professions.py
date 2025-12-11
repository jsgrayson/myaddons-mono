#!/usr/bin/env python3
"""Quick test to see what professions the Blizzard API returns"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('BLIZZARD_CLIENT_ID')
CLIENT_SECRET = os.getenv('BLIZZARD_CLIENT_SECRET')

# Get token
response = requests.post(
    "https://us.battle.net/oauth/token",
    data={'grant_type': 'client_credentials'},
    auth=(CLIENT_ID, CLIENT_SECRET)
)
token = response.json()['access_token']

# Get profession index
response = requests.get(
    "https://us.api.blizzard.com/data/wow/profession/index",
    params={'namespace': 'static-us', 'locale': 'en_US'},
   headers={'Authorization': f'Bearer {token}'}
)

if response.status_code == 200:
    data = response.json()
    print(f"Total professions: {len(data.get('professions', []))}")
    print("\nAll professions from API:")
    for prof in data.get('professions', []):
        print(f"  - {prof['name']} (ID: {prof['id']})")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
