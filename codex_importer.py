import requests
import json
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

# CONFIGURATION
CLIENT_ID = os.getenv("BLIZZARD_CLIENT_ID")
CLIENT_SECRET = os.getenv("BLIZZARD_CLIENT_SECRET")
REGION = "us"
LOCALE = "en_US"

class BlizzardAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        
    def get_token(self):
        """Get OAuth token"""
        url = f"https://{REGION}.battle.net/oauth/token"
        data = {"grant_type": "client_credentials"}
        auth = (self.client_id, self.client_secret)
        response = requests.post(url, data=data, auth=auth)
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            return True
        print(f"Failed to get token: {response.text}")
        return False
        
    def get_journal_instance(self, instance_id):
        """Get instance details from Journal API"""
        url = f"https://{REGION}.api.blizzard.com/data/wow/journal-instance/{instance_id}"
        params = {
            "namespace": f"static-{REGION}",
            "locale": LOCALE,
            "access_token": self.token
        }
        return requests.get(url, params=params).json()

    def get_journal_encounter(self, encounter_id):
        """Get encounter details including loot and abilities"""
        url = f"https://{REGION}.api.blizzard.com/data/wow/journal-encounter/{encounter_id}"
        params = {
            "namespace": f"static-{REGION}",
            "locale": LOCALE,
            "access_token": self.token
        }
        return requests.get(url, params=params).json()

def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Please set BLIZZARD_CLIENT_ID and BLIZZARD_CLIENT_SECRET env vars.")
        return

    api = BlizzardAPI(CLIENT_ID, CLIENT_SECRET)
    if not api.get_token():
        return

    # Target Instances (Nerub-ar Palace, The Stonevault)
    target_instances = [1293, 1269] 
    
    codex_data = {
        "instances": [],
        "encounters": []
    }

    for inst_id in target_instances:
        print(f"Fetching Instance {inst_id}...")
        inst_data = api.get_journal_instance(inst_id)
        
        codex_data["instances"].append({
            "id": inst_data["id"],
            "name": inst_data["name"],
            "type": inst_data.get("category", {}).get("type", "Unknown"),
            "bosses": len(inst_data.get("encounters", [])),
            "location": inst_data.get("location", {}).get("name", "Unknown")
        })
        
        for enc_ref in inst_data.get("encounters", []):
            enc_id = enc_ref["id"]
            print(f"  Fetching Encounter {enc_id} ({enc_ref['name']})...")
            enc_data = api.get_journal_encounter(enc_id)
            
            # Process Abilities (Sections)
            abilities = []
            for section in enc_data.get("sections", []):
                # Simplified logic to extract top-level mechanics
                abilities.append({
                    "id": section["id"],
                    "name": section["title"],
                    "role": "EVERYONE", # Logic needed to parse icons/text for role
                    "description": section.get("body_text", "No description"),
                    "importance": "Medium"
                })
                
            # Process Loot
            loot = []
            for item in enc_data.get("items", []):
                loot.append({
                    "id": item["item"]["id"],
                    "name": item["item"]["name"],
                    "slot": "Unknown", # Requires Item API lookup
                    "type": "Unknown",
                    "ilvl": 0 # Requires context
                })

            codex_data["encounters"].append({
                "id": enc_data["id"],
                "name": enc_data["name"],
                "instance_id": inst_id,
                "order": enc_ref.get("order_index", 0),
                "description": enc_data.get("description", ""),
                "abilities": abilities[:5], # Limit for demo
                "loot": loot[:5]
            })

    # Save to JSON
    with open("codex_data.json", "w") as f:
        json.dump(codex_data, f, indent=4)
    print("✓ Saved real data to codex_data.json")

if __name__ == "__main__":
    main()
