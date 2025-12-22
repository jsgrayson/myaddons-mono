import os
import requests
import time
from requests.auth import HTTPBasicAuth

# CONFIG
CLIENT_ID = os.getenv("BLIZZARD_CLIENT_ID")
CLIENT_SECRET = os.getenv("BLIZZARD_CLIENT_SECRET")
REGION = "us"
LOCALE = "en_US"

class BlizzardUplink:
    def __init__(self):
        self.access_token = None
        self.token_expiry = 0
        self.session = requests.Session()

    def _auth(self):
        """Refreshes the OAuth Token"""
        if self.access_token and time.time() < self.token_expiry:
            return

        print("[GOBLIN_UPLINK] Refreshing Blizzard OAuth Token...")
        url = f"https://{REGION}.battle.net/oauth/token"
        try:
            response = self.session.post(
                url, 
                data={"grant_type": "client_credentials"},
                auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"[ERROR] Blizzard Auth Failed: {response.text}")
                return
                
            data = response.json()
            self.access_token = data['access_token']
            self.token_expiry = time.time() + data['expires_in'] - 60 # Buffer
            print(f"[GOBLIN_UPLINK] Uplink Secured. Valid for {data['expires_in']}s")
        except Exception as e:
            print(f"[ERROR] Blizzard Auth Exception: {e}")

    def get_headers(self):
        self._auth()
        if not self.access_token:
            return {}
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Battlenet-Namespace": f"dynamic-{REGION}", 
            "content-type": "application/json"
        }

    # 1. THE GOLD STANDARD (WoW Token)
    def get_token_price(self):
        """Returns the current Gold value of a WoW Token"""
        url = f"https://{REGION}.api.blizzard.com/data/wow/token/index?namespace=dynamic-{REGION}&locale={LOCALE}"
        try:
            res = self.session.get(url, headers=self.get_headers(), timeout=10)
            if res.status_code == 200:
                data = res.json()
                # Convert raw copper to Gold
                gold_price = int(data['price'] / 100 / 100)
                return gold_price
            else:
                 print(f"[ERROR] Token Price Fetch Failed: {res.status_code}")
                 return 0
        except Exception as e:
            print(f"[ERROR] Token Price Fetch Exception: {e}")
            return 0

    # 2. THE COMMODITIES EXCHANGE (Region-Wide Mats)
    def get_commodities_dump(self):
        """
        Downloads the massive AH dump for region-wide commodities (Herbs, Ore, Consumables).
        WARNING: This is a heavy payload.
        """
        url = f"https://{REGION}.api.blizzard.com/data/wow/auctions/commodities?namespace=dynamic-{REGION}&locale={LOCALE}"
        print("[GOBLIN_UPLINK] Initiating Commodities Download...")
        try:
            res = self.session.get(url, headers=self.get_headers(), timeout=30)
            
            if res.status_code == 200:
                return res.json().get('auctions', [])
            else:
                print(f"[ERROR] Commodities Sync Failed: {res.status_code}")
                return []
        except Exception as e:
            print(f"[ERROR] Commodities Download Exception: {e}")
            return []

    # 3. REALM SPECIFIC (Gear, BoEs)
    def get_connected_realm_auctions(self, connected_realm_id: int):
        """
        Fetches auctions specific to your server (Armor, Weapons, Pets).
        """
        url = f"https://{REGION}.api.blizzard.com/data/wow/connected-realm/{connected_realm_id}/auctions?namespace=dynamic-{REGION}&locale={LOCALE}"
        try:
            res = self.session.get(url, headers=self.get_headers(), timeout=30)
            if res.status_code == 200:
                return res.json().get('auctions', [])
            else:
                print(f"[ERROR] Realm Auction Fetch Failed: {res.status_code}")
                return []
        except Exception as e:
            print(f"[ERROR] Realm Auction Fetch Exception: {e}")
            return []

# USAGE EXAMPLE
if __name__ == "__main__":
    if not CLIENT_ID or not CLIENT_SECRET:
        print("[GOBLIN_UPLINK] ERROR: BLIZZARD_CLIENT_ID and BLIZZARD_CLIENT_SECRET env vars must be set.")
    else:
        uplink = BlizzardUplink()
        price = uplink.get_token_price()
        print(f"CURRENT WOW TOKEN PRICE: {price:,}g")
