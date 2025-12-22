import time
import os
import psycopg2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from parsers.tsm_decoder import ingest_pricing_snapshot
from slpp import slpp as lua

# ENV VARS
WTF_PATH = os.getenv("WOW_WTF_PATH", "/mnt/wow/WTF/Account/SavedVariables")
DB_DSN = os.getenv("DATABASE_URL", "postgresql://goblin:goldcap@localhost:5432/goblin_ledger")

class FileMonitor(FileSystemEventHandler):
    def on_modified(self, event):
        filename = os.path.basename(event.src_path)
        
        if filename == "TradeSkillMaster.lua":
            print(f"[WATCHDOG] TSM Database Update Detected.")
            self.update_prices(event.src_path)
            
        elif filename == "Holocron.lua":
            print(f"[WATCHDOG] Inventory/Warbank Update Detected.")
            self.update_inventory(event.src_path)

    def update_prices(self, path):
        data = ingest_pricing_snapshot(path)
        conn = psycopg2.connect(DB_DSN)
        cur = conn.cursor()
        
        # Batch Insert for Speed
        # We use ON CONFLICT to update prices if the item exists
        args_list = [(k, v['mv'], v['source']) for k, v in data.items()]
        
        query = """
        INSERT INTO item_pricing (item_id, market_value, source) 
        VALUES (%s, %s, %s)
        ON CONFLICT (item_id) DO UPDATE 
        SET market_value = EXCLUDED.market_value, last_seen = NOW();
        """
        
        cur.executemany(query, args_list)
        conn.commit()
        cur.close()
        conn.close()
        print(f"[WATCHDOG] Database updated with {len(args_list)} price records.")

    def update_inventory(self, path):
        # Parses the Holocron export for Warbank/Bag data
        # (Logic provided in previous turn)
        pass

if __name__ == "__main__":
    print(f"[GOBLIN] Watchdog Service Starting on {WTF_PATH}...")
    observer = Observer()
    observer.schedule(FileMonitor(), path=WTF_PATH, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
