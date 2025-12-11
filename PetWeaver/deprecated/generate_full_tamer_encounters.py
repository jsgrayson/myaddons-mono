# generate_full_tamer_encounters.py
"""
Generate a comprehensive encounters JSON for all tamers, including full ability objects.
Missing abilities are left empty and flagged with "missing_abilities": true.
Uses Blizzard API species endpoint to fetch abilities for missing species.
"""
import json
import os
import re
import requests
from blizzard_oauth import BlizzardOAuth

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))

TAMERS_PATH = os.path.join(PROJECT_ROOT, "pettracker_tamers.json")
DECODED_PATH = os.path.join(PROJECT_ROOT, "pettracker_decoded.json")
ABILITIES_PATH = os.path.join(PROJECT_ROOT, "abilities.json")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "encounters_full.json")

def load_env():
    env = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    env[k] = v
    except FileNotFoundError:
        pass
    return env

env = load_env()
CLIENT_ID = env.get('BLIZZARD_CLIENT_ID')
CLIENT_SECRET = env.get('BLIZZARD_CLIENT_SECRET')

class BlizzardAPI:
    def __init__(self):
        self.oauth = BlizzardOAuth(CLIENT_ID, CLIENT_SECRET)
        self.token = None
        self.region = "us"
        self.base = f"https://{self.region}.api.blizzard.com"
        self._ensure_token()
        self.species_cache = {}
        self.ability_cache = {}

    def _ensure_token(self):
        if self.oauth.load_token():
            self.token = self.oauth.token_data['access_token']
            return
        self.token = self._client_credentials_token()
        if not self.token:
            raise Exception('Unable to obtain Blizzard API token')

    def _client_credentials_token(self):
        """Obtain an access token using Blizzard client‑credentials flow."""
        token_url = "https://oauth.battle.net/token"
        data = {"grant_type": "client_credentials"}
        try:
            resp = requests.post(token_url, data=data, auth=(CLIENT_ID, CLIENT_SECRET), timeout=10)
            if resp.status_code == 200:
                return resp.json().get('access_token')
            print(f"⚠️ Failed to get client‑credentials token: {resp.status_code} {resp.text}")
        except Exception as e:
            print(f"⚠️ Exception while fetching token: {e}")
        return None
    
    def _request(self, endpoint, namespace="static-us"):
        if not self.token:
            return None
        url = f"{self.base}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Battlenet-Namespace": namespace
        }
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                print(f"Blizzard API error {resp.status_code} for {endpoint}")
                return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None

    def get_species_abilities(self, species_id):
        sid = str(species_id)
        if sid in self.species_cache:
            return self.species_cache[sid]
        data = self._request(f"/data/wow/pet/{species_id}")
        abilities = []
        if data and 'abilities' in data:
            for a in data['abilities']:
                abilities.append(a['ability']['id'])
        self.species_cache[sid] = abilities
        return abilities

    def get_ability_details(self, ability_id):
        aid = str(ability_id)
        if aid in self.ability_cache:
            return self.ability_cache[aid]
        data = self._request(f"/data/wow/pet-ability/{ability_id}")
        if not data:
            return None
        description = data.get('description', '')
        stats = {'power': None, 'accuracy': None, 'speed': None}
        if description:
            m = re.search(r"deals?\s+(\d+)\s+damage", description, re.I)
            if m:
                stats['power'] = int(m.group(1))
            m = re.search(r"(\d+)%\s+(?:chance|accuracy)", description, re.I)
            if m:
                stats['accuracy'] = int(m.group(1))
            m = re.search(r"\+?(\d+)\s+speed", description, re.I)
            if m:
                stats['speed'] = int(m.group(1))
        details = {
            "id": data['id'],
            "name": data['name'].get('en_US', ''),
            "cooldown": data.get('cooldown', 0),
            "rounds": data.get('rounds', 1),
            "family_id": data.get('battle_pet_type', {}).get('id', 0),
            "power": stats['power'] if stats['power'] is not None else 20,
            "accuracy": stats['accuracy'] if stats['accuracy'] is not None else 100,
            "speed": stats['speed'] if stats['speed'] is not None else 0,
        }
        self.ability_cache[aid] = details
        return details

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    tamers = load_json(TAMERS_PATH)
    decoded = load_json(DECODED_PATH)
    abilities_data = {}
    if os.path.exists(ABILITIES_PATH):
        abilities_data = load_json(ABILITIES_PATH)
    
    # Flatten species map from pettracker_decoded
    species_map = {}
    raw_species = decoded.get("species", {})
    if isinstance(raw_species, dict):
        for map_id, inner in raw_species.items():
            if isinstance(inner, dict):
                for sid, abil in inner.items():
                    species_map[str(sid)] = abil
            elif isinstance(inner, list):
                species_map[str(map_id)] = inner
    for sid, abil in raw_species.items():
        if isinstance(abil, list):
            species_map[str(sid)] = abil
    
    api = BlizzardAPI()
    full_encounters = []
    
    for tamer in tamers:
        tamer_entry = {
            "npc_id": tamer.get("id"),
            "name": tamer.get("name"),
            "map": tamer.get("map_id"),
            "quest": tamer.get("quest_id"),
            "gold": tamer.get("gold"),
            "pets": []
        }
        
        for pet in tamer.get("team", []):
            species_id = str(pet.get("species_id"))
            ability_ids = species_map.get(species_id)
            missing = False
            
            if not ability_ids:
                # Fetch from Blizzard API
                print(f"  Fetching abilities for species {species_id} via API...")
                ability_ids = api.get_species_abilities(species_id)
                if not ability_ids:
                    missing = True
                    ability_ids = []
            
            # Resolve ability objects
            ability_objs = []
            for aid in ability_ids:
                details = api.get_ability_details(aid)
                if details:
                    ability_objs.append(details)
                else:
                    # fallback to cached abilities.json
                    if str(aid) in abilities_data.get("abilities", {}):
                        ability_objs.append(abilities_data["abilities"][str(aid)])
            
            pet_entry = {
                "species_id": pet.get("species_id"),
                "model_id": pet.get("model"),
                "level": pet.get("level"),
                "quality": pet.get("quality"),
                "abilities": ability_objs,
                "missing_abilities": missing
            }
            tamer_entry["pets"].append(pet_entry)
        
        full_encounters.append(tamer_entry)
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(full_encounters, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Generated {OUTPUT_PATH} with {len(full_encounters)} tamers.")
    
    # Count missing
    total_pets = sum(len(t["pets"]) for t in full_encounters)
    missing_count = sum(1 for t in full_encounters for p in t["pets"] if p.get("missing_abilities"))
    print(f"📊 Total pets: {total_pets}, Missing abilities: {missing_count}")

if __name__ == "__main__":
    main()
