import json
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from market_manager import MarketManager

class GoblinHandler(FileSystemEventHandler):
    def __init__(self, market_manager, goblin_file):
        self.market_manager = market_manager
        self.goblin_file = goblin_file

    def on_modified(self, event):
        if event.src_path.endswith(self.goblin_file):
            print(f"Goblin data file modified: {event.src_path}")
            self.process_goblin_data()

    def process_goblin_data(self):
        if not os.path.exists(self.goblin_file):
            return

        try:
            with open(self.goblin_file, 'r') as f:
                data = json.load(f)
                
            # Assume Goblin exports a list of {speciesId, price, name}
            # or a dict keyed by speciesId
            
            count = 0
            if isinstance(data, list):
                for item in data:
                    self.market_manager.update_price(
                        item.get('speciesId'), 
                        item.get('price'), 
                        item.get('name', 'Unknown'),
                        market_value=item.get('marketValue', 0),
                        discount=item.get('discount', 0),
                        is_deal=item.get('isDeal', False),
                        level=item.get('level', 0)
                    )
                    count += 1
            elif isinstance(data, dict):
                for sid, info in data.items():
                    self.market_manager.update_price(
                        sid, 
                        info.get('price'), 
                        info.get('name', 'Unknown'),
                        market_value=info.get('marketValue', 0),
                        discount=info.get('discount', 0),
                        is_deal=info.get('isDeal', False),
                        level=info.get('level', 0)
                    )
                    count += 1
                    
            print(f"Updated {count} market prices from Goblin.")
            
        except Exception as e:
            print(f"Error processing Goblin data: {e}")

class GoblinIntegrator:
    def __init__(self, market_manager, watch_dir='.', goblin_filename='price_list.json'):
        self.market_manager = market_manager
        self.watch_dir = watch_dir
        self.goblin_filename = goblin_filename
        self.observer = Observer()

    def start(self):
        event_handler = GoblinHandler(self.market_manager, self.goblin_filename)
        self.observer.schedule(event_handler, self.watch_dir, recursive=False)
        self.observer.start()
        print(f"Goblin Integrator watching {self.watch_dir}/{self.goblin_filename}")
        
        # Initial load
        event_handler.process_goblin_data()

    def stop(self):
        self.observer.stop()
        self.observer.join()
