#!/usr/bin/env python3
"""
Find Blizzard API Encounter IDs
Lists all available journal instances to find the correct IDs
"""

import os
from dotenv import load_dotenv
import requests
import json

# Load credentials
load_dotenv('/Users/jgrayson/Documents/petweaver/.env')
CLIENT_ID = os.getenv('BLIZZARD_CLIENT_ID')
CLIENT_SECRET = os.getenv('BLIZZARD_CLIENT_SECRET')

# Get token
response =requests.post(
    "https://us.battle.net/oauth/token",
    data={'grant_type': 'client_credentials'},
    auth=(CLIENT_ID, CLIENT_SECRET)
)
token = response.json()['access_token']

# List all journal instances
url = "https://us.api.blizzard.com/data/wow/journal-instance/index"
response = requests.get(url, params={
    'namespace': 'static-us',
    'locale': 'en_US',
    'access_token': token
})

try:
    instances = response.json()
except json.JSONDecodeError:
    print(f"Error decoding JSON. Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    exit(1)

print("\n" + "="*80)
print("ALL AVAILABLE JOURNAL INSTANCES")
print("="*80 + "\n")

# Filter for recent/relevant content
for inst in instances.get('instances', []):
    print(f"ID: {inst['id']:5} - {inst['name']}")
    
# Save full list
with open('/Users/jgrayson/Documents/holocron/data/blizzard_instances.json', 'w') as f:
    json.dump(instances, f, indent=2)

print(f"\n✓ Saved full list to data/blizzard_instances.json")
print(f"\nTotal instances: {len(instances.get('instances', []))}")
