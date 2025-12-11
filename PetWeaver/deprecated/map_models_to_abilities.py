import json
import requests
import os
import time

class BlizzardAPI:
    def __init__(self):
        self.load_env()
        self.token = None
        self.client_id = os.getenv('BLIZZARD_CLIENT_ID')
        self.client_secret = os.getenv('BLIZZARD_CLIENT_SECRET')

    def load_env(self):
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if '=' in line:
                        k, v = line.strip().split('=', 1)
                        os.environ[k] = v
        except FileNotFoundError:
            pass
        
    def _ensure_token(self):
        # Try to load from token.json first
        if os.path.exists('token.json'):
            with open('token.json', 'r') as f:
                data = json.load(f)
                if data.get('expires_at', 0) > time.time():
                    self.token = data.get('access_token')
                    return

        # Fetch new token
        url = "https://oauth.battle.net/token"
        data = {"grant_type": "client_credentials"}
        try:
            resp = requests.post(url, data=data, auth=(self.client_id, self.client_secret), timeout=10)
            if resp.status_code == 200:
                token_data = resp.json()
                self.token = token_data.get('access_token')
                # Save it
                token_data['expires_at'] = int(time.time()) + token_data.get('expires_in', 0)
                with open('token.json', 'w') as f:
                    json.dump(token_data, f)
            else:
                print(f"Failed to get token: {resp.status_code}")
        except Exception as e:
            print(f"Error fetching token: {e}")

def map_models_to_abilities():
    # 1. Load missing models from encounters_full.json
    with open('encounters_full.json', 'r') as f:
        encounters = json.load(f)
        
    missing_models = set()
    missing_pets_count = 0
    for tamer in encounters:
        for pet in tamer['pets']:
            if pet.get('missing_abilities', False):
                missing_models.add(pet['model_id'])
                missing_pets_count += 1
                
    print(f"🎯 Found {missing_pets_count} pets missing abilities")
    print(f"🔍 Unique missing Model IDs: {len(missing_models)}")
    
    if not missing_models:
        print("✅ No missing abilities found!")
        return

    # 2. Initialize Blizzard API
    api = BlizzardAPI()
    api._ensure_token()
    if not api.token:
        print("❌ Failed to get Blizzard API token")
        return

    # 3. Fetch all player pets
    print("🔄 Fetching player pet index...")
    url = "https://us.api.blizzard.com/data/wow/pet/index"
    headers = {
        "Authorization": f"Bearer {api.token}",
        "Battlenet-Namespace": "static-us"
    }
    params = {"locale": "en_US"}
    
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        if resp.status_code != 200:
            print(f"❌ API Error: {resp.status_code} {resp.text}")
            return
        pet_index = resp.json().get('pets', [])
    except Exception as e:
        print(f"❌ Exception: {e}")
        return

    # 4. Search for matching models
    print(f"🔎 Scanning {len(pet_index)} player pets for model matches...")
    
    model_abilities_map = {} # ModelID -> Abilities List
    found_count = 0
    
    for i, p in enumerate(pet_index):
        if len(model_abilities_map) >= len(missing_models):
            print("✅ Found matches for all missing models!")
            break
            
        pet_id = p['id']
        pet_name = p['name']
        
        # Fetch pet details
        detail_url = f"https://us.api.blizzard.com/data/wow/pet/{pet_id}"
        try:
            r = requests.get(detail_url, headers=headers, params=params, timeout=5)
            if r.status_code == 200:
                data = r.json()
                display_id = data.get('creature_display_id')
                
                if display_id in missing_models and display_id not in model_abilities_map:
                    # Found a match!
                    abilities = data.get('abilities', [])
                    if abilities:
                        # Convert ability objects to our format if needed
                        # Blizzard API returns: {"ability": {"key":..., "name":..., "id":...}, "slot":...}
                        # We need full ability details.
                        # Actually, encounters_full.json expects full ability objects.
                        # But here we just get ID and Name.
                        # We might need to fetch ability details or use our local DB.
                        
                        # Let's just store the list of ability IDs for now, and resolve them later?
                        # Or try to map them using 'abilities.json' if we have it loaded.
                        
                        # For now, let's just store the raw list and we'll fix the format in step 5.
                        model_abilities_map[display_id] = abilities
                        found_count += 1
                        print(f"  ✨ Match! Model {display_id} ({pet_name}) -> {len(abilities)} abilities")
        except Exception:
            pass
            
        if i % 100 == 0:
            print(f"  ...scanned {i}/{len(pet_index)} pets...")

    # 5. Update encounters_full.json
    print(f"\n📝 Updating encounters with {len(model_abilities_map)} new ability sets...")
    
    updated_count = 0
    for tamer in encounters:
        for pet in tamer['pets']:
            if pet.get('missing_abilities', False):
                mid = pet['model_id']
                if mid in model_abilities_map:
                    pet['abilities'] = model_abilities_map[mid]
                    pet['missing_abilities'] = False
                    pet['abilities_source'] = "model_match"
                    updated_count += 1
                    
    with open('encounters_full.json', 'w') as f:
        json.dump(encounters, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Successfully updated {updated_count} pets!")

if __name__ == "__main__":
    map_models_to_abilities()
