#!/usr/bin/env python3
"""
Utility Tracker - Mount, Toy, Spell, and Transmog Collection Progress
Tracks collectibles and shows completion percentages
"""

from typing import List, Dict
from dataclasses import dataclass
from enum import Enum

class CollectionType(Enum):
    MOUNT = "Mount"
    TOY = "Toy"
    SPELL = "Spell"
    PET = "Battle Pet"
    APPEARANCE = "Transmog"

@dataclass
class Collectible:
    item_id: int
    name: str
    collection_type: CollectionType
    source: str  # "Raid", "Dungeon", "Achievement", "Vendor", "Rare Drop"
    difficulty: str  # "Easy", "Medium", "Hard", "Very Hard"
    expansion: str
    
from utils.lua_parser import LuaParser
import os
import glob
import json

class UtilityTracker:
    """Tracks mount, toy, spell, and transmog collections"""
    
    def __init__(self):
        self.all_collectibles = []
        self.owned = set()
        self.lua_parser = LuaParser()
        
    def load_real_data(self):
        """Load real collection data from DataStore_Mounts/Pets/CanIMogIt (JSON or Lua)"""
        print("Loading real collection data...")
        
        # 1. Try loading from JSON (Uploaded)
        mounts_json = "DataStore_Mounts.json"
        pets_json = "DataStore_Pets.json"
        mog_json = "CanIMogIt.json"
        
        json_loaded = False
        if os.path.exists(mounts_json):
            try:
                with open(mounts_json, "r") as f:
                    data = json.load(f)
                self._process_mounts_data(data)
                json_loaded = True
            except Exception as e:
                print(f"Error loading mounts JSON: {e}")
                
        if os.path.exists(pets_json):
            try:
                with open(pets_json, "r") as f:
                    data = json.load(f)
                self._process_pets_data(data)
                json_loaded = True
            except Exception as e:
                print(f"Error loading pets JSON: {e}")

        if os.path.exists(mog_json):
            try:
                with open(mog_json, "r") as f:
                    data = json.load(f)
                self._process_mog_data(data)
                json_loaded = True
            except Exception as e:
                print(f"Error loading mog JSON: {e}")
                
        if json_loaded:
            print(f"✓ Loaded {len(self.all_collectibles)} collectibles, {len(self.owned)} owned from JSON")
            return

        # 2. Fallback to SavedVariables (Local)
        possible_paths = [
            os.environ.get('WOW_SAVED_VARIABLES_PATH'),
            os.path.expanduser("~/Documents/holocron/SavedVariables"),
            "/Applications/World of Warcraft/_retail_/WTF/Account/*/SavedVariables",
            "C:/Program Files (x86)/World of Warcraft/_retail_/WTF/Account/*/SavedVariables"
        ]
        
        sv_path = None
        for path_pattern in possible_paths:
            if not path_pattern: continue
            matches = glob.glob(os.path.join(path_pattern, "DataStore_Mounts.lua"))
            if matches:
                sv_path = os.path.dirname(matches[0])
                break
                
        if not sv_path:
            print("Could not find SavedVariables. Falling back to mock data.")
            self.load_mock_data()
            return

        # Load from Lua files
        self._load_mounts_lua(sv_path)
        self._load_pets_lua(sv_path)
        self._load_mog_lua(sv_path)
        
        print(f"✓ Loaded {len(self.all_collectibles)} collectibles, {len(self.owned)} owned from Lua")

    def _load_mog_lua(self, sv_path):
        mog_file = os.path.join(sv_path, "CanIMogIt.lua")
        if not os.path.exists(mog_file): return
        data = self.lua_parser.parse_file(mog_file, "CanIMogItDB")
        if data: self._process_mog_data(data)

    def _process_mog_data(self, data):
        try:
            # CanIMogIt structure: global.appearances[ID] = true
            db_global = data.get("global", {})
            appearances = db_global.get("appearances", {})
            
            for item_id, known in appearances.items():
                if known:
                    try:
                        iid = int(item_id)
                        self.owned.add(iid)
                        self._ensure_collectible(iid, CollectionType.APPEARANCE)
                    except: pass
        except Exception as e:
            print(f"Error processing mog: {e}")
        
    def _load_mounts_lua(self, sv_path):
        mount_file = os.path.join(sv_path, "DataStore_Mounts.lua")
        data = self.lua_parser.parse_file(mount_file, "DataStore_MountsDB")
        if data: self._process_mounts_data(data)

    def _load_pets_lua(self, sv_path):
        pet_file = os.path.join(sv_path, "DataStore_Pets.lua")
        if not os.path.exists(pet_file): return
        data = self.lua_parser.parse_file(pet_file, "DataStore_PetsDB")
        if data: self._process_pets_data(data)

    def _process_mounts_data(self, data):
        try:
            db_global = data.get("global", {})
            characters = db_global.get("Characters", {})
            
            for char_key, char_data in characters.items():
                mounts = char_data.get("Mounts", [])
                if isinstance(mounts, list):
                    for m_id in mounts:
                        if isinstance(m_id, int):
                            self.owned.add(m_id)
                            self._ensure_collectible(m_id, CollectionType.MOUNT)
                elif isinstance(mounts, dict):
                    for m_id in mounts:
                        self.owned.add(int(m_id))
                        self._ensure_collectible(int(m_id), CollectionType.MOUNT)
        except Exception as e:
            print(f"Error processing mounts: {e}")

    def _process_pets_data(self, data):
        try:
            db_global = data.get("global", {})
            characters = db_global.get("Characters", {})
            
            for char_key, char_data in characters.items():
                pets = char_data.get("Pets", [])
                if isinstance(pets, list):
                    for p in pets:
                        if isinstance(p, str) and "|" in p:
                            try:
                                species_id = int(p.split("|")[0])
                                self.owned.add(species_id)
                                self._ensure_collectible(species_id, CollectionType.PET)
                            except: pass
                        elif isinstance(p, int):
                            self.owned.add(p)
                            self._ensure_collectible(p, CollectionType.PET)
        except Exception as e:
            print(f"Error processing pets: {e}")

    def _ensure_collectible(self, item_id: int, c_type: CollectionType):
        # Check if already exists
        for c in self.all_collectibles:
            if c.item_id == item_id and c.collection_type == c_type:
                return
        
        # Create generic entry since we don't have a name DB
        self.all_collectibles.append(Collectible(
            item_id, f"{c_type.value} #{item_id}", c_type, "Unknown", "Medium", "Unknown"
        ))

    def load_mock_data(self):
        """Load mock collection data"""
        
        # Mounts
        self.all_collectibles = [
            # Easy mounts
            Collectible(1, "Reins of the Bronze Drake", CollectionType.MOUNT,
                       "The Culling of Stratholme (Timed)", "Easy", "WotLK"),
            Collectible(2, "Swift White Hawkstrider", CollectionType.MOUNT,
                       "Magister's Terrace", "Easy", "TBC"),
            
            # Hard mounts
            Collectible(3, "Invincible's Reins", CollectionType.MOUNT,
                       "Icecrown Citadel (Heroic 25)", "Very Hard", "WotLK"),
            Collectible(4, "Ashes of Al'ar", CollectionType.MOUNT,
                       "Tempest Keep", "Very Hard", "TBC"),
            Collectible(5, "Flametalon of Alysrazor", CollectionType.MOUNT,
                       "Firelands", "Hard", "Cataclysm"),
            
            # Toys
            Collectible(100, "Toy Train Set", CollectionType.TOY,
                       "Vendor (Winter Veil)", "Easy", "Vanilla"),
            Collectible(101, "Faded Wizard Hat", CollectionType.TOY,
                       "Achievement: Higher Learning", "Medium", "WotLK"),
            Collectible(102, "Blazing Wings", CollectionType.TOY,
                       "Firelands Rare Drop", "Hard", "Cataclysm"),
            
            # Spells/Appearances
            Collectible(200, "Moonkin Form (Glyph)", CollectionType.SPELL,
                       "Inscription", "Easy", "Various"),
            Collectible(201, "Fandral's Seed Pouch (Druid)", CollectionType.SPELL,
                       "Firelands Questline", "Medium", "Cataclysm"),
            Collectible(202, "Hidden Artifact Appearance", CollectionType.SPELL,
                       "Secret Quest Chain", "Very Hard", "Legion"),
            
            # Transmog
            Collectible(300, "Tusks of Mannoroth", CollectionType.APPEARANCE,
                        "Siege of Orgrimmar", "Very Hard", "MoP"),
        ]
        
        # Mock owned items
        self.owned = {1, 2, 100, 101, 200}  # Have 5 items
        
        print(f"✓ Loaded {len(self.all_collectibles)} collectibles, {len(self.owned)} owned")
    
    def get_progress(self, collection_type: CollectionType = None) -> Dict:
        """Get collection progress statistics"""
        
        if collection_type:
            items = [c for c in self.all_collectibles if c.collection_type == collection_type]
        else:
            items = self.all_collectibles
        
        total = len(items)
        owned_count = sum(1 for c in items if c.item_id in self.owned)
        missing_count = total - owned_count
        percent = int((owned_count / total) * 100) if total > 0 else 0
        
        # Group missing by difficulty
        missing_by_difficulty = {"Easy": 0, "Medium": 0, "Hard": 0, "Very Hard": 0}
        for item in items:
            if item.item_id not in self.owned:
                missing_by_difficulty[item.difficulty] += 1
        
        return {
            "total": total,
            "owned": owned_count,
            "missing": missing_count,
            "percent": percent,
            "missing_by_difficulty": missing_by_difficulty
        }
    
    def get_missing_items(self, collection_type: CollectionType, limit: int = 10) -> List[Dict]:
        """Get missing items sorted by difficulty (easiest first)"""
        
        difficulty_order = {"Easy": 1, "Medium": 2, "Hard": 3, "Very Hard": 4}
        
        missing = [
            c for c in self.all_collectibles
            if c.collection_type == collection_type and c.item_id not in self.owned
        ]
        
        # Sort by difficulty (easiest first)
        missing.sort(key=lambda x: difficulty_order.get(x.difficulty, 99))
        
        return [{
            "id": item.item_id,
            "name": item.name,
            "source": item.source,
            "difficulty": item.difficulty,
            "expansion": item.expansion
        } for item in missing[:limit]]
    
    def get_summary(self) -> Dict:
        """Get complete collection summary"""
        
        mounts = self.get_progress(CollectionType.MOUNT)
        toys = self.get_progress(CollectionType.TOY)
        spells = self.get_progress(CollectionType.SPELL)
        mog = self.get_progress(CollectionType.APPEARANCE)
        
        return {
            "mounts": mounts,
            "toys": toys,
            "spells": spells,
            "transmog": mog,
            "overall": self.get_progress()
        }

if __name__ == "__main__":
    # Test the tracker
    print("\n" + "="*70)
    print("UTILITY TRACKER - Collection Progress")
    print("="*70)
    
    tracker = UtilityTracker()
    tracker.load_mock_data()
    
    # Test 1: Overall summary
    print("\n" + "="*70)
    print("COLLECTION SUMMARY")
    print("="*70)
    
    summary = tracker.get_summary()
    
    print(f"\n  Mounts: {summary['mounts']['owned']}/{summary['mounts']['total']} ({summary['mounts']['percent']}%)")
    print(f"  Toys: {summary['toys']['owned']}/{summary['toys']['total']} ({summary['toys']['percent']}%)")
    print(f"  Spells: {summary['spells']['owned']}/{summary['spells']['total']} ({summary['spells']['percent']}%)")
    print(f"  Transmog: {summary['transmog']['owned']}/{summary['transmog']['total']} ({summary['transmog']['percent']}%)")
    print(f"\n  Overall: {summary['overall']['owned']}/{summary['overall']['total']} ({summary['overall']['percent']}%)")
    
    print("\n" + "="*70)
    print("✓ All tests complete!")
    print("="*70)
