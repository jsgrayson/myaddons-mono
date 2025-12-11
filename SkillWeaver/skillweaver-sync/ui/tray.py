"""
System Tray GUI for SkillWeaver Sync
"""
import pystray
from PIL import Image, ImageDraw
from threading import Thread
import sys
from loguru import logger

def create_icon():
    """Create a simple icon for the system tray"""
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), 'blue')
    dc = ImageDraw.Draw(image)
    dc.rectangle([width//4, height//4, width*3//4, height*3//4], fill='white')
    return image

class SyncTrayApp:
    """System tray application for SkillWeaver Sync"""
    
    def __init__(self, sync_manager):
        self.sync_manager = sync_manager
        self.icon = None
        
    def on_quit(self, icon, item):
        """Quit the application"""
        logger.info("Shutting down...")
        icon.stop()
        sys.exit(0)
    
    def on_sync_now(self, icon, item):
        """Manually trigger sync"""
        logger.info("Manual sync triggered")
        self.sync_manager.sync_to_web()
    
    def on_download(self, icon, item):
        """Download recommendations"""
        logger.info("Downloading recommendations")
        self.sync_manager.download_recommendations()
    
    def run(self):
        """Start the system tray app"""
        menu = pystray.Menu(
            pystray.MenuItem("Sync Now", self.on_sync_now),
            pystray.MenuItem("Download Recommendations", self.on_download),
            pystray.MenuItem("Quit", self.on_quit)
        )
        
        self.icon = pystray.Icon(
            "SkillWeaver Sync",
            create_icon(),
            "SkillWeaver Sync",
            menu
        )
        
        # Start file watcher in background thread
        watcher_thread = Thread(target=self.sync_manager.start_watching, daemon=True)
        watcher_thread.start()
        
        # Run tray icon
        self.icon.run()

if __name__ == "__main__":
    from main import SyncManager
    
    sync_manager = SyncManager(
        wow_path="/Applications/World of Warcraft",
        api_url="http://localhost:8001"
    )
    
    app = SyncTrayApp(sync_manager)
    app.run()
