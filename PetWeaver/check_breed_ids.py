# check_breed_ids.py
"""
Script to verify breed IDs from pettracker data using Blizzard API.
It loads pettracker_tamers.json, extracts all breed_id values, and attempts to fetch
breed abilities via Blizzard API. It prints a summary and writes a report to
breed_check_report.txt.
"""
import json, os
from blizzard_oauth import BlizzardOAuth
import requests

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
        self.breed_cache = {}
    def _ensure_token(self):
        if self.oauth.load_token():
            self.token = self.oauth.token_data['access_token']
        else:
            token_url = "https://oauth.battle.net/token"
            data = {"grant_type": "client_credentials"}
            resp = requests.post(token_url, data=data, auth=(CLIENT_ID, CLIENT_SECRET), timeout=10)
            if resp.status_code == 200:
                self.token = resp.json().get('access_token')
            else:
                raise Exception(f"Failed token request: {resp.status_code} {resp.text}")
    def _request(self, endpoint, namespace="static-us"):
        if not self.token:
            return None
        url = f"{self.base}{endpoint}"
        headers = {"Authorization": f"Bearer {self.token}", "Battlenet-Namespace": namespace}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        return None
    def get_breed_abilities(self, breed_id):
        return self._request(f"/data/wow/pet/breed/{breed_id}")

def main():
    tamers_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "pettracker_tamers.json")
    with open(tamers_path, 'r', encoding='utf-8') as f:
        tamers = json.load(f)
    breed_ids = set()
    for t in tamers:
        for pet in t.get('team', []):
            bid = pet.get('breed_id')
            if bid is not None:
                breed_ids.add(bid)
    api = BlizzardAPI()
    report_lines = []
    for bid in sorted(breed_ids):
        data = api.get_breed_abilities(bid)
        if data and 'abilities' in data:
            report_lines.append(f"Breed ID {bid}: FOUND {len(data['abilities'])} abilities")
        else:
            report_lines.append(f"Breed ID {bid}: NOT FOUND or no abilities")
    report_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "breed_check_report.txt")
    with open(report_path, 'w', encoding='utf-8') as out:
        out.write("\n".join(report_lines))
    print("Breed check completed. Report written to", report_path)

if __name__ == "__main__":
    main()
