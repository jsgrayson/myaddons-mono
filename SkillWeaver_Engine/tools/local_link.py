import os
import time
import shutil
import logging
from datetime import datetime

# CONFIGURATION
WATCH_DIR = "../updates"
TARGET_ROOT = "../Brain"
BACKUP_DIR = "../backups"
POLL_INTERVAL = 2.0

# MAPPING (Where to send files based on destination)
# Simple heuristic: flatten structure or mirror?
# Let's try recursive mirroring if folders exist, or simple filename matching.
# For now: We assume flat structure in updates/ triggers routing.
DIRECTORY_MAP = {
    "_spec.json": "data/specs",
    "_vs_all.json": "matchups",
    "logic_processor.py": "modules",
    "vision.py": "modules",
    "matrix.json": ".",
    "encounters.json": "."
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [WATCHDOG] - %(message)s',
    datefmt='%H:%M:%S'
)

def deploy_file(filename, source_path):
    # Determine destination
    dest_subdir = "."
    
    # 1. Exact Match Logic
    if filename in DIRECTORY_MAP:
        dest_subdir = DIRECTORY_MAP[filename]
    # 2. Suffix Match Logic
    elif filename.endswith("_spec.json"):
        dest_subdir = "data/specs" # e.g. 62_arcane_spec.json -> data/specs/62_arcane.json?
        # Actually standard naming is 62_arcane.json.
        # Let's adjust matching.
    elif filename.endswith("_vs_all.json"):
        dest_subdir = "matchups"
    elif filename.endswith(".json"):
        # Check if first part is number?
        parts = filename.split('_')
        if parts[0].isdigit():
             dest_subdir = "data/specs"
        else:
             dest_subdir = "." # Default root
    elif filename.endswith(".py"):
        dest_subdir = "modules"
    
    dest_path = os.path.join(TARGET_ROOT, dest_subdir, filename)
    
    # Check if target exists (for backup)
    if os.path.exists(dest_path):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{filename}.{ts}.bak"
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        shutil.copy2(dest_path, backup_path)
        logging.info(f"Backed up {filename} -> {backup_name}")
    
    # Move/Copy new file
    try:
        shutil.move(source_path, dest_path)
        logging.info(f"DEPLOYED: {filename} -> {dest_path}")
        return True
    except Exception as e:
        logging.error(f"Failed to deploy {filename}: {e}")
        return False

def main():
    logging.info(f"Initializing Midnight Deployment Sync...")
    logging.info(f"Watching: {os.path.abspath(WATCH_DIR)}")
    logging.info(f"Target:   {os.path.abspath(TARGET_ROOT)}")
    
    # Ensure dirs
    os.makedirs(WATCH_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    try:
        while True:
            # Scan directory
            files = [f for f in os.listdir(WATCH_DIR) if not f.startswith('.')]
            
            for f in files:
                source = os.path.join(WATCH_DIR, f)
                if os.path.isfile(source):
                    logging.info(f"Detected Artifact: {f}")
                    # Brief settle time for writes
                    time.sleep(0.5) 
                    deploy_file(f, source)
            
            time.sleep(POLL_INTERVAL)
            
    except KeyboardInterrupt:
        logging.info("Watchdog terminated by user.")

if __name__ == "__main__":
    main()
