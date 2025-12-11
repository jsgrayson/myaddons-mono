#!/usr/bin/env python3
"""
Load real WoW data from SavedVariables into backend engines
"""

import os
import sys
import re

# WoW SavedVariables path
SAVED_VARS = "/Applications/World of Warcraft/_retail_/WTF/Account/NIGHTHWK77/SavedVariables"

def load_datastore_characters():
    """Load character data from DataStore_Characters.lua"""
    file_path = os.path.join(SAVED_VARS, "DataStore_Characters.lua")
    
    if not os.path.exists(file_path):
        print("⚠️  DataStore_Characters.lua not found")
        return {}
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract character names and basic info
    chars = {}
    char_pattern = r'\["(.+?)"\] = \{.*?\["realm"\] = "(.+?)".*?\["class"\] = "(\w+)".*?\["level"\] = (\d+)'
    
    for match in re.finditer(char_pattern, content, re.DOTALL):
        name, realm, char_class, level = match.groups()
        if 'Jaina' not in name:  # Skip test data
            chars[name] = {
                'realm': realm,
                'class': char_class,
                'level': int(level)
            }
    
    return chars

def load_datastore_containers():
    """Load bag/bank data from DataStore_Containers.lua"""
    file_path = os.path.join(SAVED_VARS, "DataStore_Containers.lua")
    
    if not os.path.exists(file_path):
        print("⚠️  DataStore_Containers.lua not found")
        return {}
    
    # This would parse bag contents
    # For now, DeepPockets handles this
    return {}

def load_datastore_quests():
    """Load quest data from DataStore_Quests.lua"""
    file_path = os.path.join(SAVED_VARS, "DataStore_Quests.lua")
    
    if not os.path.exists(file_path):
        print("⚠️  DataStore_Quests.lua not found")
        return {}
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Count completed quests per character
    quests = {}
    # Complex parsing - simplified for now
    
    return quests

def load_datastore_reputations():
    """Load reputation data from DataStore_Reputations.lua"""
    file_path = os.path.join(SAVED_VARS, "DataStore_Reputations.lua")
    
    if not os.path.exists(file_path):
        print("⚠️  DataStore_Reputations.lua not found")
        return {}
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Parse reputation standings
    reps = {}
    rep_pattern = r'\["(.+?)"\] = (\d+)'
    
    for match in re.finditer(rep_pattern, content):
        faction, standing = match.groups()
        reps[faction] = int(standing)
    
    return reps

def load_savedinstances():
    """Load lockout data from SavedInstances.lua"""
    file_path = os.path.join(SAVED_VARS, "SavedInstances.lua")
    
    if not os.path.exists(file_path):
        print("⚠️  SavedInstances.lua not found")
        return {}
    
    # Parse instance lockouts
    instances = {}
    
    return instances

def load_tsm_data():
    """Load TSM pricing data"""
    # TSM uses AppData, not SavedVariables
    tsm_path = os.path.expanduser("~/Library/Application Support/TradeSkillMaster")
    
    if not os.path.exists(tsm_path):
        print("⚠️  TSM data not found")
        return {}
    
    # Would parse TSM databases
    return {}

def generate_summary():
    """Generate a summary of available data"""
    print("=" * 60)
    print("WOW DATA LOADER")
    print("=" * 60)
    
    # Check what's available
    available = []
    missing = []
    
    files_to_check = {
        'Characters': 'DataStore_Characters.lua',
        'Containers': 'DataStore_Containers.lua',
        'Quests': 'DataStore_Quests.lua',
        'Reputations': 'DataStore_Reputations.lua',
        'Instances': 'SavedInstances.lua',
        'DeepPockets': 'DeepPockets.lua',
        'PetWeaver': 'PetWeaver.lua',
        'PetTracker': 'PetTracker.lua'
    }
    
    for name, filename in files_to_check.items():
        path = os.path.join(SAVED_VARS, filename)
        if os.path.exists(path):
            size = os.path.getsize(path)
            available.append(f"  ✅ {name}: {size:,} bytes")
        else:
            missing.append(f"  ❌ {name}")
    
    if available:
        print("\nAvailable Data:")
        for item in available:
            print(item)
    
    if missing:
        print("\nMissing Data:")
        for item in missing:
            print(item)
    
    print("\n" + "=" * 60)
    
    # Load what we can
    chars = load_datastore_characters()
    reps = load_datastore_reputations()
    
    if chars:
        print(f"\n📊 Found {len(chars)} characters:")
        for name, data in chars.items():
            print(f"  • {name} ({data['class']} {data['level']})")
    
    if reps:
        print(f"\n🤝 Found {len(reps)} reputations")
    
    return {
        'characters': chars,
        'reputations': reps
    }

if __name__ == "__main__":
    data = generate_summary()
