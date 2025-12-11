import json
import os
import time
import re
import requests
from blizzard_oauth import BlizzardOAuth

# Load environment variables manually (no dotenv dependency)

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

class AbilityFetcher:
    def __init__(self):
        self.oauth = BlizzardOAuth(CLIENT_ID, CLIENT_SECRET)
        if not self.oauth.load_token():
            raise Exception("No valid token found. Please run app.py to authenticate first.")
        self.access_token = self.oauth.token_data['access_token']
        self.region = "us"
        self.api_base = f"https://{self.region}.api.blizzard.com"
        self.ability_cache = {}
        self.species_abilities = {}  # species_id -> [ability_ids]

    def _make_request(self, endpoint, namespace="static-us"):
        url = f"{self.api_base}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Battlenet-Namespace': namespace
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"404 Not Found: {endpoint}")
                return None
            else:
                print(f"Error {response.status_code}: {endpoint}")
                return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None

    def fetch_species_details(self, species_id):
        """Get abilities available for a species"""
        data = self._make_request(f"/data/wow/pet/{species_id}")
        if not data:
            return []
        abilities = []
        if 'abilities' in data:
            for ability in data['abilities']:
                abilities.append(ability['ability']['id'])
        return abilities

    def _parse_stats(self, description: str) -> dict:
        """Extract power, accuracy, speed from an ability description string.
        Returns dict with keys 'power', 'accuracy', 'speed' (may be None)."""
        stats = {'power': None, 'accuracy': None, 'speed': None}
        if not description:
            return stats
        # Power patterns (e.g., "deals 20 damage")
        m = re.search(r"deals?\s+(\d+)\s+damage", description, re.I)
        if m:
            stats['power'] = int(m.group(1))
        # Accuracy patterns (e.g., "30% chance" or "30% accuracy")
        m = re.search(r"(\d+)%\s+(?:chance|accuracy)", description, re.I)
        if m:
            stats['accuracy'] = int(m.group(1))
        # Speed patterns (e.g., "+5 speed" or "increases speed by 5")
        m = re.search(r"\+?(\d+)\s+speed", description, re.I)
        if m:
            stats['speed'] = int(m.group(1))
        return stats

    def fetch_ability_details(self, ability_id):
        """Get details for a specific ability, including parsed stats"""
        if ability_id in self.ability_cache:
            return self.ability_cache[ability_id]
        data = self._make_request(f"/data/wow/pet-ability/{ability_id}")
        if not data:
            return None
        description = data.get('description', '')
        parsed = self._parse_stats(description)
        details = {
            "id": data['id'],
            "name": data['name']['en_US'],
            "cooldown": data.get('cooldown', 0),
            "rounds": data.get('rounds', 1),
            "family_id": data['battle_pet_type']['id'] if 'battle_pet_type' in data else 0,
            "power": parsed['power'] if parsed['power'] is not None else 20,
            "accuracy": parsed['accuracy'] if parsed['accuracy'] is not None else 100,
            "speed": parsed['speed'] if parsed['speed'] is not None else 0,
        }
        self.ability_cache[ability_id] = details
        return details

    def run(self):
        # 1. Load Owned Pets
        print("Loading my_pets.json...")
        with open('my_pets.json', 'r') as f:
            data = json.load(f)
        owned_species = set()
        for pet in data.get('pets', []):
            if 'species' in pet:
                owned_species.add(pet['species']['id'])
        print(f"Found {len(owned_species)} unique species.")
        # 2. Fetch data for ALL owned species
        target_species = list(owned_species)
        print(f"Fetching data for {len(target_species)} species...")
        for i, species_id in enumerate(target_species, 1):
            print(f"[{i}/{len(target_species)}] Fetching Species {species_id}...")
            ability_ids = self.fetch_species_details(species_id)
            self.species_abilities[species_id] = ability_ids
            for ab_id in ability_ids:
                if ab_id not in self.ability_cache:
                    self.fetch_ability_details(ab_id)
                    time.sleep(0.1)
            time.sleep(0.1)
        # 3. Save results
        output = {
            "species_abilities": self.species_abilities,
            "abilities": self.ability_cache
        }
        with open('abilities.json', 'w') as f:
            json.dump(output, f, indent=2)
        print(f"Saved {len(self.ability_cache)} abilities to abilities.json")

if __name__ == "__main__":
    AbilityFetcher().run()
