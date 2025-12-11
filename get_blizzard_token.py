# get_blizzard_token.py
"""
Fetch a client‑credentials token from Blizzard and store it in token.json.
"""
import os, json, requests

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
client_id = env.get('BLIZZARD_CLIENT_ID')
client_secret = env.get('BLIZZARD_CLIENT_SECRET')
if not client_id or not client_secret:
    raise Exception('Missing Blizzard credentials in .env')

token_url = "https://oauth.battle.net/token"
resp = requests.post(token_url, data={"grant_type": "client_credentials"}, auth=(client_id, client_secret), timeout=10)
if resp.status_code != 200:
    raise Exception(f"Failed to obtain token: {resp.status_code} {resp.text}")

token_data = resp.json()
# Add expiration timestamp for convenience
import datetime, time
expires_in = token_data.get('expires_in', 0)
expires_at = int(time.time()) + expires_in
token_data['expires_at'] = expires_at
with open('token.json', 'w') as f:
    json.dump(token_data, f, indent=2)
print('Token saved to token.json')
