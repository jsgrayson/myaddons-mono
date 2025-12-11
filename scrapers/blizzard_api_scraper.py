#!/usr/bin/env python3
"""
Blizzard API Encounter Scraper
Gets official encounter journal data from Blizzard's Game Data API
"""

import requests
import json
import time

class BlizzardAPIClient:
    """
    Client for Blizzard's WoW Game Data API
    Docs: https://develop.battle.net/documentation/world-of-warcraft/game-data-apis
    """
    
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
        self.token_expires = time.time() + data['expires_in'] - 60  # 60s buffer
        
        return self.token
    
    def get_journal_instance(self, instance_id):
        """
        Get instance data from encounter journal
        Args:
            instance_id: e.g., 1273 for Nerub-ar Palace
        """
        token = self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/data/wow/journal-instance/{instance_id}"
        
        response = requests.get(
            url,
            params={
                'namespace': f'static-{self.region}',
                'locale': 'en_US',
                'access_token': token
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_journal_encounter(self, encounter_id):
        """
        Get encounter details
        Args:
            encounter_id: e.g., 2922 for Queen Ansurek
        """
        token = self.get_access_token()
        url = f"https://{self.region}.api.blizzard.com/data/wow/journal-encounter/{encounter_id}"
        
        response = requests.get(
            url,
            params={
                'namespace': f'static-{self.region}',
                'locale': 'en_US',
                'access_token': token
            }
        )
        response.raise_for_status()
        return response.json()

# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    # Load credentials from .env
    load_dotenv('/Users/jgrayson/Documents/petweaver/.env')
    CLIENT_ID = os.getenv('BLIZZARD_CLIENT_ID')
    CLIENT_SECRET = os.getenv('BLIZZARD_CLIENT_SECRET')
    
    if not CLIENT_ID or not CLIENT_SECRET:
        print("ERROR: Blizzard API credentials not found in .env file!")
        exit(1)
    
    client = BlizzardAPIClient(CLIENT_ID, CLIENT_SECRET)
    
    # Test: Get Nerub-ar Palace (instance ID 1273)
    print("\n" + "="*60)
    print("Fetching Nerub-ar Palace instance data...")
    print("="*60)
    
    try:
        instance = client.get_journal_instance(1273)
        print(f"\nInstance: {instance['name']}")
        print(f"Encounters: {len(instance.get('encounters', []))}")
        
        # Save full data
        with open('/Users/jgrayson/Documents/holocron/data/nerub_ar_palace.json', 'w') as f:
            json.dump(instance, f, indent=2)
        print("\n✓ Saved to data/nerub_ar_palace.json")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test: Get Queen Ansurek encounter (encounter ID 2922)
    print("\n" + "="*60)
    print("Fetching Queen Ansurek encounter...")
    print("="*60)
    
    try:
        encounter = client.get_journal_encounter(2922)
        print(f"\nBoss: {encounter['name']}")
        print(f"Instance: {encounter['instance']['name']}")
        
        # Count abilities/sections
        sections = encounter.get('sections', [])
        print(f"Sections: {len(sections)}")
        
        # Save full data
        with open('/Users/jgrayson/Documents/holocron/data/queen_ansurek.json', 'w') as f:
            json.dump(encounter, f, indent=2)
        print("\n✓ Saved to data/queen_ansurek.json")
        
    except Exception as e:
        print(f"✗ Error: {e}")
