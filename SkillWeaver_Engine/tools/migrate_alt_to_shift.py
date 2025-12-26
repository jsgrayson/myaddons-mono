#!/usr/bin/env python3
"""
migrate_alt_to_shift.py - Changes Alt+ to Shift+ in all spec JSON files
"""

import os
import json

SPECS_DIR = os.path.join(os.path.dirname(__file__), "..", "Brain", "data", "specs")

def migrate_spec(filepath):
    """Change Alt+ to Shift+ in a spec file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace Alt+ with Shift+
    modified = content.replace('"Alt+', '"Shift+')
    
    if modified != content:
        with open(filepath, 'w') as f:
            f.write(modified)
        return True
    return False

def main():
    print("Migrating Alt+ to Shift+ in spec files...")
    count = 0
    
    for filename in os.listdir(SPECS_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(SPECS_DIR, filename)
            if migrate_spec(filepath):
                print(f"  [+] Updated: {filename}")
                count += 1
    
    print(f"\nDone! Updated {count} files.")

if __name__ == "__main__":
    main()
