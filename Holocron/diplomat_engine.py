#!/usr/bin/env python3
"""
The Diplomat - Reputation & World Quest Optimizer
Recommends most efficient WQs for factions close to Paragon rewards
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Faction:
    faction_id: int
    name: str
    expansion: str
    paragon_threshold: int = 10000
    
@dataclass
class ReputationStatus:
    faction_id: int
    current_value: int
    is_paragon: bool = True
    
    @property
    def progress_percent(self) -> int:
        return int((self.current_value / 10000) * 100)
    
    @property
    def remaining(self) -> int:
        return 10000 - self.current_value
    
    @property
    def is_opportunity(self) -> bool:
        """Faction is >80% to next Paragon reward"""
        return self.progress_percent >= 80

@dataclass
class WorldQuest:
    quest_id: int
    title: str
    zone_id: int
    zone_name: str
    faction_id: int
    rep_reward: int
    estimated_time_seconds: int
    gold_reward: int = 0
    expires_at: Optional[datetime] = None
    
    @property
    def efficiency(self) -> float:
        """Rep per minute"""
        if self.estimated_time_seconds == 0:
            return 0
        return (self.rep_reward / self.estimated_time_seconds) * 60
    
    @property
    def efficiency_score(self) -> str:
        if self.efficiency >= 400:
            return "Excellent"
        elif self.efficiency >= 200:
            return "Good"
        elif self.efficiency >= 100:
            return "Average"
        else:
            return "Poor"

from utils.lua_parser import LuaParser
import os
import glob

class DiplomatEngine:
    """
    Reputation optimizer that identifies Paragon opportunities
    and recommends most efficient World Quests
    """
    
    def __init__(self):
        self.factions = {}
        self.reputation_status = {}
        self.active_wqs = []
        self.lua_parser = LuaParser()
        
    def load_real_data(self):
        """
        Load real reputation data from DataStore_Reputations.json (uploaded) or .lua (local)
        """
        print("Loading real reputation data...")
        
        # 1. Check for uploaded JSON
        import json
        json_path = "DataStore_Reputations.json"
        
        if os.path.exists(json_path):
            print(f"Found uploaded data: {json_path}")
            try:
                with open(json_path, "r") as f:
                    data = json.load(f)
                self._process_datastore_data(data)
                return
            except Exception as e:
                print(f"Error loading JSON: {e}")
        
        # 2. Fallback to finding the SavedVariables file (Local Mode)
        # Check common locations or environment variable
        possible_paths = [
            os.environ.get('WOW_SAVED_VARIABLES_PATH'),
            os.path.expanduser("~/Documents/holocron/SavedVariables"), # Local override
            "/Applications/World of Warcraft/_retail_/WTF/Account/*/SavedVariables", # Mac Standard
            "C:/Program Files (x86)/World of Warcraft/_retail_/WTF/Account/*/SavedVariables" # Windows Standard
        ]
        
        file_path = None
        for path_pattern in possible_paths:
            if not path_pattern: continue
            
            # Use glob to handle wildcards (Account name)
            matches = glob.glob(os.path.join(path_pattern, "DataStore_Reputations.lua"))
            if matches:
                file_path = matches[0] # Use first match
                break
                
        if not file_path:
            print("Could not find DataStore_Reputations.lua. Falling back to mock data.")
            self.load_mock_data()
            return
 
        print(f"Parsing {file_path}...")
        
        # 3. Parse the Lua file
        data = self.lua_parser.parse_file(file_path, "DataStore_ReputationsDB")
        
        if not data:
            print("Failed to parse reputation data. Falling back to mock data.")
            self.load_mock_data()
            return
            
        self._process_datastore_data(data)
        
    def _process_datastore_data(self, data):
        """Process the raw DataStore dictionary"""
        # DataStore structure: DataStore_ReputationsDB.global.Characters[GUID].Factions[FactionID]
        # We need to aggregate or pick the current character. 
        # For MVP, we'll pick the character with the most recent update or just the first one.
        
        # Simplified: Just iterate all characters and find the max rep for each faction (account-wide view)
        
        try:
            db_global = data.get("global", {})
            characters = db_global.get("Characters", {})
            
            if not characters:
                # Maybe structure is different (profile based?)
                # Try profile keys if global is empty
                pass
                
            # Reset data
            self.factions = {}
            self.reputation_status = {}
            
            count = 0
            for char_key, char_data in characters.items():
                factions_data = char_data.get("Factions", {})
                
                for faction_id_str, rep_data in factions_data.items():
                    # rep_data might be a list or dict depending on DataStore version
                    # Usually: { name, earned, total, standing, ... }
                    
                    # Note: LuaParser might return keys as strings or ints depending on format
                    faction_id = int(faction_id_str)
                    
                    # Extract data (DataStore format varies, assuming standard fields)
                    # If it's a list: [name, earned, rate, ...]
                    # If it's a dict: {name=..., earned=...}
                    
                    name = "Unknown Faction"
                    current = 0
                    max_rep = 42000 # Exalted/Paragon
                    
                    if isinstance(rep_data, dict):
                        name = rep_data.get("name", name)
                        current = rep_data.get("earned", 0)
                        # max might not be stored, assume standard or look up
                    elif isinstance(rep_data, list):
                        # Heuristic mapping if list
                        if len(rep_data) > 0: name = rep_data[0]
                        if len(rep_data) > 1: current = rep_data[1]
                        
                    # Update our DB (Account-wide max)
                    if faction_id not in self.reputation_status or current > self.reputation_status[faction_id].current_value:
                        self.factions[faction_id] = Faction(faction_id, name, "Unknown") # Expansion unknown from DataStore
                        self.reputation_status[faction_id] = ReputationStatus(faction_id, current)
                        count += 1
                        
            print(f"✓ Loaded {len(self.factions)} factions from real data")
            
            # Load mock WQs since we don't have a WQ scraper yet
            self._load_mock_wqs()
            
        except Exception as e:
            print(f"Error processing reputation data: {e}")
            self.load_mock_data()

    def _load_mock_wqs(self):
        """Load mock WQs only (helper for real data mode)"""
        now = datetime.now()
        self.active_wqs = [
            WorldQuest(70001, "Protect the Core", 2248, "Isle of Dorn", 2600, 250, 30, 150, now + timedelta(hours=6)),
            WorldQuest(70004, "Defend the Lighthouse", 2215, "Hallowfall", 2602, 350, 90, 175, now + timedelta(hours=5)),
        ]

    def load_mock_data(self):
        """Load mock reputation and emissary data"""
        
        # TWW Factions
        self.factions = {
            2600: Faction(2600, "Council of Dornogal", "TWW"),
            2601: Faction(2601, "The Assembly of the Deeps", "TWW"),
            2602: Faction(2602, "Hallowfall Arathi", "TWW"),
            2603: Faction(2603, "The Severed Threads", "TWW"),
        }
        
        # Mock reputation (Council of Dornogal is close to Paragon)
        self.reputation_status = {
            2600: ReputationStatus(2600, 8500),  # 85% - OPPORTUNITY!
            2601: ReputationStatus(2601, 4200),  # 42%
            2602: ReputationStatus(2602, 9100),  # 91% - OPPORTUNITY!
            2603: ReputationStatus(2603, 2000),  # 20%
        }
        
        # Mock active World Quests
        now = datetime.now()
        self.active_wqs = [
            # Council of Dornogal quests (faction 2600)
            WorldQuest(70001, "Protect the Core", 2248, "Isle of Dorn", 
                      2600, 250, 30, 150, now + timedelta(hours=6)),  # 500 rep/min - EXCELLENT
            WorldQuest(70002, "Gather Minerals", 2248, "Isle of Dorn",
                      2600, 150, 120, 100, now + timedelta(hours=4)),  # 75 rep/min - Poor
            WorldQuest(70003, "Kill Rare Elite", 2248, "Isle of Dorn",
                      2600, 300, 60, 200, now + timedelta(hours=8)),   # 300 rep/min - Good
            
            # Hallowfall Arathi quests (faction 2602)
            WorldQuest(70004, "Defend the Lighthouse", 2215, "Hallowfall",
                      2602, 350, 90, 175, now + timedelta(hours=5)),   # 233 rep/min - Good
            WorldQuest(70005, "Clear Undead", 2215, "Hallowfall",
                      2602, 250, 45, 125, now + timedelta(hours=7)),   # 333 rep/min - Good
            
            # Assembly of the Deeps (faction 2601)
            WorldQuest(70006, "Mine Ore", 2024, "The Azure Span",
                      2601, 200, 180, 150, now + timedelta(hours=3)),  # 67 rep/min - Poor
        ]
        
        print(f"✓ Loaded {len(self.factions)} factions, {len(self.active_wqs)} active WQs")
    
    def find_paragon_opportunities(self) -> List[Dict]:
        """Find factions close to Paragon rewards (>80%)"""
        opportunities = []
        
        for faction_id, status in self.reputation_status.items():
            if status.is_opportunity:
                faction = self.factions.get(faction_id)
                if faction:
                    opportunities.append({
                        "faction_id": faction_id,
                        "faction_name": faction.name,
                        "current": status.current_value,
                        "max": faction.paragon_threshold,
                        "remaining": status.remaining,
                        "percent": status.progress_percent,
                        "priority": "HIGH" if status.progress_percent >= 90 else "MEDIUM"
                    })
        
        return sorted(opportunities, key=lambda x: x["percent"], reverse=True)
        
    def get_opportunities(self) -> List[Dict]:
        """Alias for find_paragon_opportunities (Dashboard compatibility)"""
        return self.find_paragon_opportunities()
    
    def get_recommended_quests(self, faction_id: int, limit: int = 5) -> List[Dict]:
        """Get best WQs for a faction, sorted by efficiency"""
        quests = [wq for wq in self.active_wqs if wq.faction_id == faction_id]
        
        # Sort by efficiency (rep/min)
        quests.sort(key=lambda q: q.efficiency, reverse=True)
        
        results = []
        for wq in quests[:limit]:
            results.append({
                "quest_id": wq.quest_id,
                "title": wq.title,
                "zone": wq.zone_name,
                "rep_reward": wq.rep_reward,
                "time_seconds": wq.estimated_time_seconds,
                "efficiency": round(wq.efficiency, 1),
                "efficiency_score": wq.efficiency_score,
                "gold": wq.gold_reward,
                "expires_hours": (wq.expires_at - datetime.now()).total_seconds() / 3600 if wq.expires_at else None
            })
        
        return results
    
    def generate_recommendations(self) -> Dict:
        """
        Generate complete Diplomat recommendations
        Returns: {opportunities: [], all_quests: []}
        """
        opportunities = self.find_paragon_opportunities()
        
        # For each opportunity, add recommended WQs
        for opp in opportunities:
            opp["recommended_quests"] = self.get_recommended_quests(opp["faction_id"])
        
        # All WQs sorted by efficiency
        all_wqs = []
        for wq in self.active_wqs:
            faction = self.factions.get(wq.faction_id)
            all_wqs.append({
                "quest_id": wq.quest_id,
                "title": wq.title,
                "faction": faction.name if faction else "Unknown",
                "zone": wq.zone_name,
                "rep_reward": wq.rep_reward,
                "efficiency": round(wq.efficiency, 1),
                "efficiency_score": wq.efficiency_score
            })
        
        all_wqs.sort(key=lambda x: x["efficiency"], reverse=True)
        
        return {
            "opportunities": opportunities,
            "all_quests": all_wqs,
            "timestamp": datetime.now().isoformat()
        }

    def get_reputation_matrix(self) -> Dict:
        """
        Get reputation matrix for all characters
        Returns: { columns: [Factions], rows: [{char, standings: []}] }
        """
        # Define Major Factions to track
        major_factions = [
            {"id": 2600, "name": "Council of Dornogal"},
            {"id": 2601, "name": "The Assembly of the Deeps"},
            {"id": 2602, "name": "Hallowfall Arathi"},
            {"id": 2603, "name": "The Severed Threads"}
        ]
        
        # Get DB Connection
        conn = sqlite3.connect("/Users/jgrayson/Documents/holocron/holocron.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        try:
            # 1. Get All Characters
            cur.execute("SELECT character_guid, name, realm, class FROM characters ORDER BY name")
            chars = [dict(row) for row in cur.fetchall()]
            
            rows = []
            for char in chars:
                standings = []
                for faction in major_factions:
                    # Get Standing
                    cur.execute("""
                        SELECT current_standing, renown_level 
                        FROM reputation_standings 
                        WHERE character_guid = ? AND faction_id = ?
                    """, (char["character_guid"], faction["id"]))
                    
                    row = cur.fetchone()
                    if row:
                        standings.append({
                            "renown": row["renown_level"],
                            "value": row["current_standing"],
                            "is_max": row["renown_level"] >= 25 # Assumption
                        })
                    else:
                        standings.append({"renown": 0, "value": 0, "is_max": False})
                
                rows.append({
                    "character": char,
                    "standings": standings
                })
                
            return {
                "columns": major_factions,
                "rows": rows
            }
            
        except Exception as e:
            print(f"Error generating matrix: {e}")
            return {"columns": major_factions, "rows": []}
        finally:
            conn.close()

if __name__ == "__main__":
    # Test the engine
    print("\n" + "="*70)
    print("THE DIPLOMAT - Reputation Optimizer")
    print("="*70)
    
    engine = DiplomatEngine()
    engine.load_mock_data()
    
    # Test 1: Find Paragon opportunities
    print("\n" + "="*70)
    print("PARAGON OPPORTUNITIES (>80% to reward)")
    print("="*70)
    
    opportunities = engine.find_paragon_opportunities()
    for opp in opportunities:
        print(f"\n  {opp['faction_name']}")
        print(f"    Progress: {opp['current']:,}/{opp['max']:,} ({opp['percent']}%)")
        print(f"    Remaining: {opp['remaining']:,} rep")
        print(f"    Priority: {opp['priority']}")
    
    # Test 2: Get recommended WQs for Council of Dornogal
    print("\n" + "="*70)
    print("RECOMMENDED WQs - Council of Dornogal")
    print("="*70)
    
    quests = engine.get_recommended_quests(2600)
    for i, quest in enumerate(quests, 1):
        print(f"\n  {i}. {quest['title']}")
        print(f"     Zone: {quest['zone']}")
        print(f"     Rep: {quest['rep_reward']} | Time: {quest['time_seconds']}s")
        print(f"     Efficiency: {quest['efficiency']} rep/min ({quest['efficiency_score']})")
        print(f"     Gold: {quest['gold']} | Expires: {quest['expires_hours']:.1f}h")
    
    # Test 3: Full recommendations
    print("\n" + "="*70)
    print("COMPLETE RECOMMENDATIONS")
    print("="*70)
    
    recommendations = engine.generate_recommendations()
    print(f"\n  Found {len(recommendations['opportunities'])} opportunities")
    print(f"  Total active WQs: {len(recommendations['all_quests'])}")
    
    print("\n  Top 3 Most Efficient WQs (any faction):")
    for i, wq in enumerate(recommendations['all_quests'][:3], 1):
        print(f"    {i}. {wq['title']} - {wq['efficiency']} rep/min ({wq['faction']})")
    
    print("\n" + "="*70)
    print("✓ All tests complete!")
    print("="*70)
