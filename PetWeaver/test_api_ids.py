"""
Test API IDs

Diagnose why IDs are returning 404.
Tests:
1. /data/wow/pet/37 (From Addon.Species)
2. /data/wow/pet/872 (From Addon.RivalInfo)
3. /data/wow/creature/872 (Check if it's an NPC)
4. /data/wow/pet/index (List valid IDs)
"""

import json
import os
import requests
from blizzard_oauth import BlizzardOAuth

# Load environment variables manually
def load_env():
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    except FileNotFoundError:
        pass
    return env_vars

env = load_env()
CLIENT_ID = env.get('BLIZZARD_CLIENT_ID')
CLIENT_SECRET = env.get('BLIZZARD_CLIENT_SECRET')

class APITester:
    def __init__(self):
        self.oauth = BlizzardOAuth(CLIENT_ID, CLIENT_SECRET)
        self.access_token = None
        
        # Try to load user token first
        if self.oauth.load_token():
            self.access_token = self.oauth.token_data['access_token']
        else:
            print("User token invalid/expired. Attempting Client Credentials flow...")
            self.access_token = self.get_client_credentials_token()
            
        self.region = "us"
        self.api_base = f"https://{self.region}.api.blizzard.com"

    def get_client_credentials_token(self):
        url = "https://oauth.battle.net/token"
        data = {'grant_type': 'client_credentials'}
        auth = (CLIENT_ID, CLIENT_SECRET)
        try:
            response = requests.post(url, data=data, auth=auth, timeout=10)
            if response.status_code == 200:
                return response.json()['access_token']
        except:
            pass
        return None

    def make_request(self, endpoint, namespace="static-us"):
        if not self.access_token:
            print("No token")
            return
            
        url = f"{self.api_base}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Battlenet-Namespace': namespace
        }
        print(f"Requesting: {endpoint} (NS: {namespace})")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                if 'name' in data:
                    print(f"Name: {data['name']}")
                elif 'pets' in data:
                    print(f"Found {len(data['pets'])} pets in index")
                    print(f"Sample: {data['pets'][:3]}")
                else:
                    print("Success (unknown structure)")
            except:
                print("Success (parse error)")
        else:
            print(f"Error: {response.text[:100]}")

    def run(self):
        print("--- Testing ID 37 (From Addon.Species) ---")
        self.make_request("/data/wow/pet/37")
        
        print("\n--- Testing ID 872 (From Addon.RivalInfo) ---")
        self.make_request("/data/wow/pet/872")
        
        print("\n--- Testing Creature ID 872 ---")
        self.make_request("/data/wow/creature/872")
        
        print("\n--- Testing Ability ID 3 ---")
        self.make_request("/data/wow/pet-ability/3")
        
        print("\n--- Testing ID 675 (Potential Species ID) ---")
        self.make_request("/data/wow/pet/675")
        
        print("\n--- Testing Pet Index ---")
        self.make_request("/data/wow/pet/index")

if __name__ == "__main__":
    APITester().run()
