import time
import schedule
import psycopg2
import os
from backend.services.blizzard_uplink import BlizzardUplink

DB_DSN = os.getenv("DATABASE_URL")

def sync_wow_token():
    print("[WORKER] Syncing WoW Token Price...")
    try:
        uplink = BlizzardUplink()
        price = uplink.get_token_price()
        
        if price > 0:
            conn = psycopg2.connect(DB_DSN)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO global_constants (key, value_json, updated_at) VALUES (%s, %s, NOW()) "
                "ON CONFLICT (key) DO UPDATE SET value_json = EXCLUDED.value_json, updated_at = NOW()",
                ('WOW_TOKEN', str(price))
            )
            conn.commit()
            conn.close()
            print(f"[WORKER] Token Updated: {price:,}g")
        else:
            print("[WORKER] Token Price Check Failed (Price=0)")
            
    except Exception as e:
        print(f"[WORKER] Sync Status Failed: {e}")

def sync_commodities():
    print("[WORKER] Syncing Region Commodities...")
    # (Insert heavy logic for fetching and batch-inserting API data here)
    pass

if __name__ == "__main__":
    print("[WORKER] Goblin Uplink Service Online.")
    
    # Schedule Tasks
    schedule.every(15).minutes.do(sync_wow_token)
    schedule.every(1).hours.do(sync_commodities)
    
    # Run loop
    while True:
        schedule.run_pending()
        time.sleep(1)
