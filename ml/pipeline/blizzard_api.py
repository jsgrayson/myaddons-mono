import requests
import os
from loguru import logger
from typing import Dict, Optional, List
from dotenv import load_dotenv

# Load secrets
load_dotenv(os.path.join(os.path.dirname(__file__), "../../backend/config/secrets.env"))

class BlizzardAPI:
    def __init__(self, region: str = "us", locale: str = "en_US"):
        self.client_id = os.getenv("BLIZZARD_CLIENT_ID")
        self.client_secret = os.getenv("BLIZZARD_CLIENT_SECRET")
        self.region = region
        self.locale = locale
        self.access_token = None
        
        if not self.client_id or not self.client_secret:
            logger.warning("BLIZZARD_CLIENT_ID or BLIZZARD_CLIENT_SECRET not found.")

    def _get_access_token(self) -> Optional[str]:
        if self.access_token:
            # In a real app, check expiration
            return self.access_token
            
        url = "https://oauth.battle.net/token"
        auth = (self.client_id, self.client_secret)
        data = {"grant_type": "client_credentials"}
        
        try:
            response = requests.post(url, auth=auth, data=data)
            if response.status_code == 200:
                self.access_token = response.json().get("access_token")
                return self.access_token
            else:
                logger.error(f"Blizzard Auth Failed: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Blizzard Auth Error: {e}")
            return None

    def get_connected_realm_id(self, realm_slug: str) -> Optional[int]:
        """
        Find the connected realm ID for a given realm slug.
        """
        token = self._get_access_token()
        if not token:
            return None
            
        headers = {"Authorization": f"Bearer {token}"}
        
        # 1. Get Realm Index to verify slug and get ID (optional, but good for validation)
        # Actually, we can just hit the realm detail endpoint directly if we trust the slug.
        # But let's use the index to be safe as it worked in debug.
        
        url = f"https://{self.region}.api.blizzard.com/data/wow/realm/{realm_slug}"
        params = {
            "namespace": f"dynamic-{self.region}",
            "locale": self.locale
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                # connected_realm is a link: {"href": "..."}
                href = data.get("connected_realm", {}).get("href", "")
                if "connected-realm/" in href:
                    return int(href.split("connected-realm/")[1].split("?")[0])
                else:
                    logger.error(f"Connected realm href not found for {realm_slug}")
                    return None
            else:
                # If direct lookup fails, try index
                logger.warning(f"Direct realm lookup failed ({response.status_code}). Trying index...")
                return self._get_connected_realm_via_index(realm_slug, headers)
                
        except Exception as e:
            logger.error(f"Realm Lookup Error: {e}")
            return None

    def _get_connected_realm_via_index(self, realm_slug: str, headers: dict) -> Optional[int]:
        url = f"https://{self.region}.api.blizzard.com/data/wow/realm/index"
        params = {
            "namespace": f"dynamic-{self.region}",
            "locale": self.locale
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                realms = response.json().get("realms", [])
                for r in realms:
                    if r.get("slug") == realm_slug:
                        # Found it. Now we need the connected realm ID.
                        # The index entry usually has a 'key' link to the realm detail.
                        # We can follow that.
                        key_href = r.get("key", {}).get("href", "")
                        if key_href:
                            detail_resp = requests.get(key_href, headers=headers)
                            if detail_resp.status_code == 200:
                                data = detail_resp.json()
                                href = data.get("connected_realm", {}).get("href", "")
                                if "connected-realm/" in href:
                                    return int(href.split("connected-realm/")[1].split("?")[0])
                logger.error(f"Realm {realm_slug} not found in index.")
                return None
            else:
                logger.error(f"Realm Index Failed ({response.status_code}): {response.text}")
                return None
        except Exception as e:
            logger.error(f"Realm Index Error: {e}")
            return None

    def _fetch_connected_realm_from_id(self, realm_id: int) -> Optional[int]:
        """
        Given a realm ID, fetch its details to find the connected realm ID.
        """
        # We need to fetch the realm detail to get the connected realm link
        # But wait, the realm index might not have the link.
        # Let's try to fetch the realm detail using the slug or ID.
        # Actually, the realm index usually contains a link to the realm detail.
        
        # Let's try to fetch the realm detail directly using the ID is not standard.
        # But we can use the realm slug from the index to fetch the realm detail.
        # Wait, we already have the slug.
        
        # Let's just fetch the realm detail using the slug we have.
        # We don't need the ID from index if we have the slug.
        pass # We will implement this logic inside get_connected_realm_id or helper
        
    # Redefining _fetch_connected_realm_from_id is messy with replace_file_content if I don't replace the whole method.
    # I will implement the full logic in get_connected_realm_id for simplicity.

        token = self._get_access_token()
        url = f"https://{self.region}.api.blizzard.com/data/wow/realm/{realm_id}"
        params = {
            "namespace": f"dynamic-{self.region}",
            "locale": self.locale,
            "access_token": token
        }
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                # connected_realm is a link, e.g. https://us.api.blizzard.com/data/wow/connected-realm/3685?namespace=dynamic-us
                href = data.get("connected_realm", {}).get("href", "")
                if "connected-realm/" in href:
                    return int(href.split("connected-realm/")[1].split("?")[0])
        except Exception:
            pass
        return None

    def get_auctions(self, connected_realm_id: int) -> List[Dict]:
        """
        Fetch all active auctions for a connected realm.
        """
        token = self._get_access_token()
        if not token:
            return []
         # Fetch auction data
        url = f"https://{self.region}.api.blizzard.com/data/wow/connected-realm/{connected_realm_id}/auctions"
        params = {
            "namespace": f"dynamic-{self.region}",
            "locale": self.locale
        }
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            logger.info(f"Downloading auction data for realm {connected_realm_id}...")
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                return response.json().get("auctions", [])
            else:
                logger.error(f"Auction Fetch Failed ({response.status_code}): {response.text}")
                return []
        except Exception as e:
            logger.error(f"Auction Fetch Error: {e}")
            return []
