"""
SkillWeaver Sync - Desktop Companion App
Syncs WoW addon data with the web portal
"""
import os
import time
import json
import requests
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from loguru import logger
import sys

# Configure logging
logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add("skillweaver_sync.log", rotation="10 MB")

class SavedVariablesHandler(FileSystemEventHandler):
    """Watches for changes to SkillWeaver SavedVariables"""
    
    def __init__(self, sync_manager):
        self.sync_manager = sync_manager
        self.last_sync = 0
        
    def on_modified(self, event):
        if event.src_path.endswith("SkillWeaverDB.lua"):
            # Debounce: only sync once per 5 seconds
            current_time = time.time()
            if current_time - self.last_sync > 5:
                logger.info("SavedVariables changed, syncing...")
                self.sync_manager.sync_to_web()
                self.last_sync = current_time

class SyncManager:
    """Manages bidirectional sync between addon and web portal"""
    
    def __init__(self, wow_path, api_url, auth_token=None):
        self.wow_path = Path(wow_path)
        self.api_url = api_url
        self.auth_token = auth_token
        self.pending_recommendations = None
        
        # Find SavedVariables path
        self.saved_vars_path = self._find_saved_variables()
        if not self.saved_vars_path:
            raise FileNotFoundError("Could not find SkillWeaver SavedVariables")
        
        logger.info(f"Monitoring: {self.saved_vars_path}")
    
    def is_wow_running(self):
        """Check if WoW is currently running (cross-platform)"""
        import psutil
        import platform
        
        # Different process names per OS
        if platform.system() == "Darwin":  # macOS
            process_names = ["World of Warcraft", "Wow"]
        elif platform.system() == "Windows":
            process_names = ["Wow.exe", "WowClassic.exe", "World of Warcraft.exe"]
        else:  # Linux (Wine)
            process_names = ["Wow.exe", "wine"]
        
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name']
                if any(name in proc_name for name in process_names):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False
    
    def _find_saved_variables(self):
        """Locate SkillWeaver SavedVariables file"""
        # Typical path: WoW/_retail_/WTF/Account/[ACCOUNT]/SavedVariables/SkillWeaverDB.lua
        wtf_path = self.wow_path / "_retail_" / "WTF" / "Account"
        
        if not wtf_path.exists():
            return None
        
        # Find first account's SavedVariables
        for account_dir in wtf_path.iterdir():
            if account_dir.is_dir():
                sv_file = account_dir / "SavedVariables" / "SkillWeaverDB.lua"
                if sv_file.exists():
                    return sv_file
        
        return None
    
    def parse_lua_saved_variables(self):
        """Parse Lua SavedVariables into Python dict"""
        try:
            with open(self.saved_vars_path, 'r') as f:
                content = f.read()
            
            # Simple parser for SkillWeaverDB structure
            # In production, use a proper Lua parser or slpp
            data = {}
            
            # Extract character data (simplified)
            # This is a basic implementation - would need proper Lua parsing
            if "Characters" in content:
                data["characters"] = []
                # TODO: Implement proper Lua table parsing
            
            return data
        except Exception as e:
            logger.error(f"Failed to parse SavedVariables: {e}")
            return {}
    
    def sync_to_web(self):
        """Upload character data to web portal"""
        try:
            data = self.parse_lua_saved_variables()
            
            if not data:
                logger.warning("No data to sync")
                return
            
            # Upload to API
            headers = {}
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"
            
            response = requests.post(
                f"{self.api_url}/api/characters/sync",
                json=data,
                headers=headers
            )
            
            if response.status_code == 200:
                logger.info("✓ Synced to web portal")
            else:
                logger.error(f"Sync failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Sync error: {e}")
    
    def download_recommendations(self):
        """Download recommendations from web portal"""
        try:
            headers = {}
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"
            
            response = requests.get(
                f"{self.api_url}/api/characters/recommendations",
                headers=headers
            )
            
            if response.status_code == 200:
                recommendations = response.json()
                
                # Check if WoW is running
                if self.is_wow_running():
                    logger.warning("⏸️  WoW is running - queuing recommendations for later")
                    self.pending_recommendations = recommendations
                else:
                    self._write_recommendations_to_addon(recommendations)
                    logger.info("✓ Downloaded and applied recommendations")
            else:
                logger.error(f"Download failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Download error: {e}")
    
    def apply_pending_recommendations(self):
        """Apply queued recommendations (call when WoW closes)"""
        if self.pending_recommendations and not self.is_wow_running():
            logger.info("✓ WoW closed - applying queued recommendations")
            self._write_recommendations_to_addon(self.pending_recommendations)
            self.pending_recommendations = None
    
    def _write_recommendations_to_addon(self, recommendations):
        """Write recommendations back to SavedVariables"""
        try:
            # Read current SavedVariables
            with open(self.saved_vars_path, 'r') as f:
                content = f.read()
            
            # Inject recommendations (simplified - would need proper Lua generation)
            # For now, just log
            logger.info(f"Would write recommendations: {recommendations}")
            
            # TODO: Implement proper Lua table generation and writing
            
        except Exception as e:
            logger.error(f"Write error: {e}")
    
    def start_watching(self):
        """Start watching SavedVariables for changes"""
        from threading import Thread
        
        event_handler = SavedVariablesHandler(self)
        observer = Observer()
        observer.schedule(
            event_handler,
            str(self.saved_vars_path.parent),
            recursive=False
        )
        observer.start()
        
        logger.info("🔄 File watching started")
        
        # Start periodic sync in background thread
        sync_thread = Thread(target=self._periodic_sync, daemon=True)
        sync_thread.start()
        
        try:
            was_running = self.is_wow_running()
            while True:
                time.sleep(2)
                
                # Check if WoW just closed
                is_running = self.is_wow_running()
                if was_running and not is_running:
                    logger.info("WoW closed - checking for pending updates")
                    self.apply_pending_recommendations()
                was_running = is_running
                
        except KeyboardInterrupt:
            observer.stop()
            logger.info("Stopped watching")
        
        observer.join()
    
    def _periodic_sync(self):
        """Background thread for periodic sync"""
        upload_interval = 300  # 5 minutes
        download_interval = 600  # 10 minutes
        
        last_upload = 0
        last_download = 0
        
        logger.info(f"⏰ Periodic sync enabled: Upload every {upload_interval//60}min, Download every {download_interval//60}min")
        
        while True:
            current_time = time.time()
            
            # Upload character data
            if current_time - last_upload >= upload_interval:
                logger.info("⏰ Periodic upload...")
                self.sync_to_web()
                last_upload = current_time
            
            # Download recommendations
            if current_time - last_download >= download_interval:
                logger.info("⏰ Periodic download...")
                self.download_recommendations()
                last_download = current_time
            
            time.sleep(60)  # Check every minute

def get_default_wow_path():
    """Get default WoW installation path for current OS"""
    import platform
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return "/Applications/World of Warcraft"
    elif system == "Windows":
        # Try common locations
        paths = [
            "C:\\Program Files (x86)\\World of Warcraft",
            "C:\\Program Files\\World of Warcraft"
        ]
        for path in paths:
            if Path(path).exists():
                return path
        return paths[0]  # Default to first if none exist
    else:  # Linux
        # Common Wine prefix location
        home = Path.home()
        return str(home / ".wine/drive_c/Program Files (x86)/World of Warcraft")

def browse_for_wow_path():
    """Open file browser to select WoW installation directory"""
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()  # Hide main window
        
        logger.info("Opening file browser...")
        path = filedialog.askdirectory(
            title="Select World of Warcraft Installation Folder",
            initialdir=str(Path.home())
        )
        
        root.destroy()
        return path if path else None
    except Exception as e:
        logger.error(f"File browser error: {e}")
        return None

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="SkillWeaver Sync")
    parser.add_argument(
        "--wow-path",
        default=get_default_wow_path(),
        help=f"Path to WoW installation (default: {get_default_wow_path()})"
    )
    parser.add_argument(
        "--api-url",
        default="http://localhost:8001",
        help="SkillWeaver API URL"
    )
    parser.add_argument(
        "--token",
        help="Authentication token"
    )
    
    args = parser.parse_args()
    
    logger.info("SkillWeaver Sync starting...")
    logger.info(f"OS: {platform.system()}")
    logger.info(f"WoW Path: {args.wow_path}")
    
    # Check if WoW path exists
    wow_path = args.wow_path
    if not Path(wow_path).exists():
        logger.warning(f"WoW not found at: {wow_path}")
        logger.info("Opening file browser to select WoW installation...")
        
        browsed_path = browse_for_wow_path()
        if browsed_path:
            wow_path = browsed_path
            logger.info(f"✓ Selected: {wow_path}")
        else:
            logger.error("No WoW path selected. Exiting.")
            sys.exit(1)
    
    try:
        sync_manager = SyncManager(wow_path, args.api_url, args.token)
        sync_manager.start_watching()
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        logger.info("Could not find SavedVariables in the selected WoW directory")
        logger.info("Make sure you've logged in at least once so SavedVariables are created")
        
        # Try browsing again
        logger.info("Would you like to select a different folder?")
        retry_path = browse_for_wow_path()
        if retry_path:
            try:
                sync_manager = SyncManager(retry_path, args.api_url, args.token)
                sync_manager.start_watching()
            except FileNotFoundError:
                logger.error("Still could not find SavedVariables. Exiting.")
                sys.exit(1)
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()
