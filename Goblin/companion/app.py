"""
Companion App - File Watcher & Auto-Sync
"""
import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from loguru import logger
import requests

class SavedVariablesHandler(FileSystemEventHandler):
    """Watch for changes to GoblinAI.lua and upload automatically."""
    
    def __init__(self, wtf_path: str, api_url: str, api_key: str = None):
        self.wtf_path = wtf_path
        self.api_url = api_url
        self.api_key = api_key
        self.last_upload = 0
        self.cooldown = 5 # Seconds between uploads to prevent spam
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        if event.src_path.endswith("GoblinAI.lua"):
            now = time.time()
            if now - self.last_upload > self.cooldown:
                logger.info(f"Detected change in {event.src_path}")
                self.upload_file(event.src_path)
                self.last_upload = now
                
    def upload_file(self, filepath: str):
        """Upload the file to the Goblin AI server."""
        try:
            logger.info("Uploading SavedVariables...")
            with open(filepath, 'rb') as f:
                files = {'file': f}
                headers = {}
                if self.api_key:
                    headers['Authorization'] = f"Bearer {self.api_key}"
                    
                response = requests.post(
                    f"{self.api_url}/api/upload",
                    files=files,
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.success(f"Upload successful! Processed {result.get('items_scanned', 0)} items.")
                    # Trigger download of new recommendations
                    self.download_recommendations()
                else:
                    logger.error(f"Upload failed: {response.text}")
                    
        except Exception as e:
            logger.error(f"Error uploading file: {e}")

    def download_recommendations(self):
        """Download new recommendations.lua to the SavedVariables folder."""
        try:
            logger.info("Downloading new recommendations...")
            headers = {}
            if self.api_key:
                headers['Authorization'] = f"Bearer {self.api_key}"
                
            response = requests.get(
                f"{self.api_url}/api/download/recommendations",
                headers=headers
            )
            
            if response.status_code == 200:
                # Save to the same directory (or specific addon directory if needed)
                # Usually recommendations go into the same SV folder or a specific Addon folder
                # For now, save to SV folder as GoblinAI_Recommendations.lua
                
                save_path = os.path.join(os.path.dirname(self.wtf_path), "GoblinAI_Recommendations.lua")
                
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                    
                logger.success(f"Recommendations saved to {save_path}")
                logger.info("Reload UI in game (/reload) to see updates!")
            else:
                logger.error(f"Download failed: {response.text}")
                
        except Exception as e:
            logger.error(f"Error downloading recommendations: {e}")

class CompanionApp:
    def __init__(self, wtf_path: str, api_url: str = "http://localhost:8001"):
        self.wtf_path = wtf_path
        self.api_url = api_url
        self.observer = Observer()
        
    def start(self):
        logger.info(f"Starting Companion App...")
        logger.info(f"Watching: {self.wtf_path}")
        
        event_handler = SavedVariablesHandler(self.wtf_path, self.api_url)
        self.observer.schedule(event_handler, self.wtf_path, recursive=False)
        self.observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

if __name__ == "__main__":
    # Example usage
    # User would configure their path
    WTF_PATH = "/Applications/World of Warcraft/_retail_/WTF/Account/YOUR_ACCOUNT/SavedVariables"
    
    if not os.path.exists(WTF_PATH):
        # Create a dummy path for testing if real one doesn't exist
        os.makedirs("mock_wtf", exist_ok=True)
        WTF_PATH = "mock_wtf"
        
    app = CompanionApp(WTF_PATH)
    app.start()
