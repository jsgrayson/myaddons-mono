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

oauth = BlizzardOAuth(CLIENT_ID, CLIENT_SECRET)
if not oauth.load_token():
    print("No token found")
    exit()

token = oauth.token_data['access_token']
headers = {
    'Authorization': f'Bearer {token}',
    'Battlenet-Namespace': 'static-us'
}

# 1. Fetch Species 40
print("Fetching Species 40...")
url = "https://us.api.blizzard.com/data/wow/pet/40"
res = requests.get(url, headers=headers)
if res.status_code == 200:
    data = res.json()
    print(json.dumps(data, indent=2))
    
    # Try first ability
    if 'abilities' in data:
        first_ability = data['abilities'][0]
        ab_id = first_ability['ability']['id']
        print(f"\nFetching Ability {ab_id}...")
        
        url = f"https://us.api.blizzard.com/data/wow/pet-ability/{ab_id}"
        res = requests.get(url, headers=headers)
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            print(json.dumps(res.json(), indent=2))
        else:
            print(res.text)
else:
    print(f"Error: {res.status_code}")
    print(res.text)
