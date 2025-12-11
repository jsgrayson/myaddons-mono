import os
import pandas as pd
from datetime import datetime
from loguru import logger
import yaml
from .blizzard_api import BlizzardAPI

# Load core config
config_path = os.path.join(os.path.dirname(__file__), "../../backend/config/core.yaml")
with open(config_path, "r") as f:
    core_config = yaml.safe_load(f)

def ingest_data():
    blizz_config = core_config.get("blizzard", {})
    region = blizz_config.get("region", "us")
    realm_slug = blizz_config.get("realm_slug", "dalaran") # slug format: lowercase, no spaces
    
    api = BlizzardAPI(region=region)
    
    # 1. Resolve Connected Realm ID
    logger.info(f"Resolving connected realm for {realm_slug}...")
    connected_realm_id = api.get_connected_realm_id(realm_slug)
    
    if not connected_realm_id:
        logger.error("Could not resolve connected realm ID. Check config/secrets.")
        return pd.DataFrame()
        
    logger.info(f"Connected Realm ID: {connected_realm_id}")
    
    # 2. Fetch Auctions
    auctions = api.get_auctions(connected_realm_id)
    
    if not auctions:
        logger.warning("No auctions found.")
        return pd.DataFrame()
        
    logger.info(f"Fetched {len(auctions)} active auctions.")
    
    # 3. Process and Save All Data
    logger.info(f"Processing {len(auctions)} auctions...")
    
    processed_data = []
    for auc in auctions:
        item_id = auc.get("item", {}).get("id")
        # Blizzard returns 'unit_price' or 'buyout'
        price = auc.get("unit_price", auc.get("buyout", 0))
        quantity = auc.get("quantity", 1)
        
        if price > 0:
            processed_data.append({
                "item_id": item_id,
                "price": price, # Price in copper
                "quantity": quantity,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": "blizzard_api"
            })
            
    if processed_data:
        df = pd.DataFrame(processed_data)
        
        # Save to Database
        try:
            import sys
            sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
            from backend.database import DatabaseManager
            
            db_path = os.path.join(os.path.dirname(__file__), "../../goblin_ai.db")
            db = DatabaseManager(db_path)
            db.save_scan_data(df)
            logger.success(f"Saved {len(df)} records to database.")
        except Exception as e:
            logger.error(f"Failed to save to database: {e}")
            
        return df
    else:
        logger.warning("No valid auctions found (all zero price?).")
        return pd.DataFrame()

if __name__ == "__main__":
    ingest_data()
