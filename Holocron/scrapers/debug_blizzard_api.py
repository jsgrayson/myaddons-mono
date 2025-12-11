#!/usr/bin/env python3
"""
Debug Blizzard API
Test various endpoints to find the correct path to data
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load credentials
load_dotenv('/Users/jgrayson/Documents/petweaver/.env')
CLIENT_ID = os.getenv('BLIZZARD_CLIENT_ID')
CLIENT_SECRET = os.getenv('BLIZZARD_CLIENT_SECRET')

def get_token():
    response = requests.post(
        "https://us.battle.net/oauth/token",
        data={'grant_type': 'client_credentials'},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    response.raise_for_status()
    return response.json()['access_token']

def test_endpoint(name, url, token, params=None):
    print(f"\nTesting {name}...")
    print(f"URL: {url}")
    
    if params is None:
        params = {}
    
    params['access_token'] = token
    params['locale'] = 'en_US'
    
    response = requests.get(url, params=params)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✓ Success!")
        # Print summary keys
        print(f"Keys: {list(data.keys())[:5]}")
        return data
    else:
        print(f"Error: {response.text}")
        return None

if __name__ == "__main__":
    try:
        token = get_token()
        print("✓ Got access token")
        
        # 1. Test Achievement Categories (Static Namespace Check)
        test_endpoint(
            "Achievement Categories (Static Check)",
            "https://us.api.blizzard.com/data/wow/achievement-category/index",
            token,
            {'namespace': 'static-us'}
        )
        
        # 2. Test Connected Realms (Dynamic Namespace Check)
        test_endpoint(
            "Connected Realms (Dynamic Check)",
            "https://us.api.blizzard.com/data/wow/connected-realm/index",
            token,
            {'namespace': 'dynamic-us'}
        )
        
        # 3. Test Journal Instances (Static)
        test_endpoint(
            "Journal Instances",
            "https://us.api.blizzard.com/data/wow/journal-instance/index",
            token,
            {'namespace': 'static-us'}
        )
        
        # 4. Test Region Index (Dynamic) - Should be very safe
        test_endpoint(
            "Region Index",
            "https://us.api.blizzard.com/data/wow/region/index",
            token,
            {'namespace': 'dynamic-us'}
        )

        # 5. Test Playable Classes (Static) - Should be very safe
        test_endpoint(
            "Playable Classes",
            "https://us.api.blizzard.com/data/wow/playable-class/index",
            token,
            {'namespace': 'static-us'}
        )
        
    except Exception as e:
        print(f"Fatal error: {e}")
