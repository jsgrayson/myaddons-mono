"""
Search Pet Index

Fetch the full pet index and search for specific names to find their real IDs.
"""

import json
import requests
from blizzard_oauth import BlizzardOAuth
from test_api_ids import load_env, CLIENT_ID, CLIENT_SECRET

class PetSearcher:
    def __init__(self):
        self.oauth = BlizzardOAuth(CLIENT_ID, CLIENT_SECRET)
        self.access_token = None
        if self.oauth.load_token():
            self.access_token = self.oauth.token_data['access_token']
        else:
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

    def run(self):
        if not self.access_token:
            print("No token")
            return

        print("Fetching Pet Index...")
        url = f"{self.api_base}/data/wow/pet/index"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Battlenet-Namespace': "static-us"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Error fetching index: {response.status_code}")
            return

        data = response.json()
        pets = data.get('pets', [])
        print(f"Found {len(pets)} pets.")

        # Search for specific names
        targets = ["Slither", "Abyssius", "Fangs", "Spike", "Mumtar"]
        
        found = {}
        for pet in pets:
            name = pet['name']['en_US']
            if name in targets:
                print(f"Found {name}: ID {pet['id']}")
                found[name] = pet['id']
                
        # Also check if 872 or 37 appear as IDs
        ids_to_check = [37, 872]
        for pet in pets:
            if pet['id'] in ids_to_check:
                print(f"ID {pet['id']} is {pet['name']['en_US']}")

if __name__ == "__main__":
    PetSearcher().run()
