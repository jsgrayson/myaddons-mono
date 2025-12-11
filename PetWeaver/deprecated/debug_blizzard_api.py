import requests
import os
import json
import time

def debug_api():
    # Load token
    try:
        with open('token.json', 'r') as f:
            data = json.load(f)
            token = data.get('access_token')
            print(f"Loaded token: {token[:10]}...")
    except Exception as e:
        print(f"Failed to load token: {e}")
        return

    # Test Connected Realm Index (should always work)
    url = "https://us.api.blizzard.com/data/wow/connected-realm/index"
    params = {
        "namespace": "dynamic-us",
        "locale": "en_US",
        "access_token": token
    }
    
    print(f"Testing URL: {url}")
    resp = requests.get(url, params=params)
    print(f"Status: {resp.status_code}")
    if resp.status_code != 200:
        print(f"Response: {resp.text}")
        
    # Test Pet Index
    url = "https://us.api.blizzard.com/data/wow/pet/index"
    params = {
        "namespace": "static-us",
        "locale": "en_US",
        "access_token": token
    }
    print(f"Testing Pet Index: {url}")
    resp = requests.get(url, params=params)
    print(f"Status: {resp.status_code}")
    if resp.status_code != 200:
        print(f"Response: {resp.text}")

if __name__ == "__main__":
    debug_api()
