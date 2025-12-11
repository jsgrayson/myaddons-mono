#!/usr/bin/env python3
"""
The Codex - Encounter Guide Engine
Provides raid and dungeon strategies, loot tables, and ability breakdowns
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import json
import sqlite3
import os

DB_FILE = "/Users/jgrayson/Documents/holocron/holocron.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

class Role(Enum):
    TANK = "Tank"
    HEALER = "Healer"
    DPS = "DPS"
    EVERYONE = "Everyone"

class Difficulty(Enum):
    LFR = "LFR"
    NORMAL = "Normal"
    HEROIC = "Heroic"
    MYTHIC = "Mythic"

@dataclass
class Ability:
    name: str
    description: str
    role: Role
    importance: str  # "Critical", "High", "Medium", "Low"
    phase: int = 1

@dataclass
class LootItem:
    name: str
    slot: str
    item_level: int
    type: str  # "Plate", "Trinket", "Weapon", etc.

@dataclass
class Quest:
    id: int
    title: str
    description: str
    min_level: int
    zone: str
    x: float = None
    y: float = None
    map_id: int = None
    is_completed: bool = False
    rewards: List[str] = None

@dataclass
class Encounter:
    id: int
    name: str
    description: str
    abilities: List[Ability]
    loot: List[LootItem]
    guide_url: str = ""

@dataclass
class Instance:
    id: int
    name: str
    type: str  # "Raid", "Dungeon"
    encounters: List[Encounter]

from scrapers.wowhead_scraper import WowheadScraper

class CodexEngine:
    """
    Engine for The Codex encounter guide
    """
    
    def __init__(self):
        self.instances = {}
        self.encounters = {}
        self.scraper = WowheadScraper()
        
    def load_from_wowhead_json(self):
        """Load raid/dungeon boss data from data/wowhead_encounters.json"""
        try:
            with open('data/wowhead_encounters.json', 'r') as f:
                data = json.load(f)
            
            instance_id = 1000  # Counter for instance IDs
            encounter_id = 1    # Counter for encounter IDs
            
            # Load Raids
            for raid_name, raid_data in data.get('raids', {}).items():
                instance_id += 1
                instance = Instance(
                    id=instance_id,
                    name=raid_name,
                    type="Raid",
                    encounters=[]
                )
                
                for boss in raid_data.get('bosses', []):
                    encounter_id += 1
                    encounter = Encounter(
                        id=encounter_id,
                        name=boss.get('display_name', 'Unknown'),
                        description=boss.get('description', f"Boss in {raid_name}"),
                        abilities=[],
                        loot=[],
                        guide_url=boss.get('url', '')
                    )
                    instance.encounters.append(encounter)
                    self.encounters[encounter_id] = encounter
                
                self.instances[instance_id] = instance
            
            # Load Dungeons
            for dungeon_name, dungeon_data in data.get('dungeons', {}).items():
                instance_id += 1
                instance = Instance(
                    id=instance_id,
                    name=dungeon_name,
                    type="Dungeon",
                    encounters=[]
                )
                
                for boss in dungeon_data.get('bosses', []):
                    encounter_id += 1
                    encounter = Encounter(
                        id=encounter_id,
                        name=boss.get('display_name', 'Unknown'),
                        description=boss.get('description', f"Boss in {dungeon_name}"),
                        abilities=[],
                        loot=[],
                        guide_url=boss.get('url', '')
                    )
                    instance.encounters.append(encounter)
                    self.encounters[encounter_id] = encounter
                
                self.instances[instance_id] = instance
            
            # Count totals
            raid_count = len([i for i in self.instances.values() if i.type == "Raid"])
            dungeon_count = len([i for i in self.instances.values() if i.type == "Dungeon"])
            print(f"✓ Loaded {raid_count} raids, {dungeon_count} dungeons, {len(self.encounters)} bosses from wowhead_encounters.json")
            
        except FileNotFoundError:
            print("❌ data/wowhead_encounters.json not found. Falling back to codex_data.json")
            self.load_mock_data()
        except Exception as e:
            print(f"❌ Error loading wowhead encounters: {e}")
            self.load_mock_data()

        
    def load_real_data(self):
        """Load real data from Wowhead Scraper"""
        print("Fetching real data from Wowhead...")
        
        # Get Nerub-ar Palace data
        raid_data = self.scraper.get_nerubar_palace_data()
        
        if not raid_data:
            print("Failed to fetch data. Falling back to mock data.")
            self.load_mock_data()
            return

        # Parse Encounters
        encounters = []
        for enc_data in raid_data["encounters"]:
            # Parse Abilities
            abilities = []
            for ab_data in enc_data.get("abilities", []):
                # Map importance string to Role enum if possible, or default
                # The scraper returns "Tank", "Healer", "DPS", "Important", "Critical"
                # We need to map these to Role enum and importance string
                
                role = Role.EVERYONE
                if ab_data.get("importance") == "Tank":
                    role = Role.TANK
                elif ab_data.get("importance") == "Healer":
                    role = Role.HEALER
                elif ab_data.get("importance") == "DPS":
                    role = Role.DPS
                
                abilities.append(Ability(
                    name=ab_data["name"],
                    description=ab_data["description"],
                    role=role,
                    importance=ab_data.get("importance", "Medium"),
                    phase=1 # Default phase
                ))
            
            # Parse Loot (Scraper doesn't return loot yet, so empty list)
            loot = [] 
            
            encounters.append(Encounter(
                id=enc_data["id"],
                name=enc_data["name"],
                description=enc_data["description"],
                abilities=abilities,
                loot=loot
            ))
            
        # Create Instance
        instance = Instance(
            id=raid_data["id"],
            name=raid_data["name"],
            type="Raid",
            encounters=encounters
        )
        
        self.instances[instance.id] = instance
        print(f"✓ Loaded {instance.name} with {len(instance.encounters)} encounters from Wowhead")

    def load_mock_data(self):
        """Load data from codex_data.json"""
        # Initialize encounters dict
        self.encounters = {}
        
        try:
            with open('codex_data.json', 'r') as f:
                data = json.load(f)
                
            # Load Instances
            for inst in data.get('instances', []):
                self.instances[inst['id']] = Instance(
                    id=inst['id'],
                    name=inst['name'],
                    type=inst['type'],
                    encounters=[]
                )
                
            # Load Encounters
            for enc in data.get('encounters', []):
                encounter = Encounter(
                    id=enc['id'],
                    name=enc['name'],
                    description=enc.get('description', f"Encounter in {enc.get('instance', 'Unknown')}"),
                    abilities=[],
                    loot=[],
                    guide_url=enc.get('guide_url', '')
                )
                self.encounters[enc['id']] = encounter
                
                # Link encounter to its instance
                instance_name = enc.get('instance')
                if instance_name:
                    for inst in self.instances.values():
                        if inst.name == instance_name:
                            inst.encounters.append(encounter)
                            break
                            
                # Load Abilities for this encounter (if present)
                for a in enc.get('abilities', []):
                    role_str = a.get('role', 'EVERYONE').upper()
                    try:
                        role = Role[role_str]
                    except KeyError:
                        role = Role.EVERYONE
                        
                    encounter.abilities.append(Ability(
                        name=a['name'],
                        description=a.get('description', ''),
                        role=role,
                        importance=a.get('importance', 'Medium'),
                        phase=a.get('phase', 1)
                    ))
                    
                # Load Loot for this encounter (if present)
                for l in enc.get('loot', []):
                    encounter.loot.append(LootItem(
                        name=l['name'],
                        slot=l.get('slot', 'Unknown'),
                        item_level=l.get('ilvl', 0),
                        type=l.get('type', 'Unknown')
                    ))
                    
            print(f"✓ Loaded {len(self.instances)} instances, {len(self.encounters)} encounters from JSON")
            
        except FileNotFoundError:
            print("❌ codex_data.json not found! Creating empty data.")
            self.encounters = {}
        except Exception as e:
            print(f"❌ Error loading codex data: {e}")
            self.encounters = {}

    def get_instances(self):
        # This method needs to be updated to return actual Instance objects, not just asdict
        # The original `get_instances` was returning `asdict(i)` from `self.instances.values()`
        # The new `load_mock_data` populates `self.instances` with `Instance` objects.
        # The `asdict` import is missing, so I'll assume it's intended to be `dataclasses.asdict`
        from dataclasses import asdict
        return [asdict(i) for i in self.instances.values()]

    def get_encounter_details(self, encounter_id: int):
        if encounter_id not in self.encounters:
            return None
        
        encounter = asdict(self.encounters[encounter_id])
        encounter['abilities'] = [asdict(a) for a in self.abilities.get(encounter_id, [])]
        encounter['loot'] = [asdict(l) for l in self.loot.get(encounter_id, [])]
        return encounter
        
    def get_instance(self, instance_id: int) -> Optional[Dict]:
        """Get instance details"""
        instance = self.instances.get(instance_id)
        if not instance:
            return None
            
        return {
            "id": instance.id,
            "name": instance.name,
            "type": instance.type,
            "encounters": [
                {"id": e.id, "name": e.name, "description": e.description}
                for e in instance.encounters
            ]
        }
        
    def get_encounter(self, encounter_id: int) -> Optional[Dict]:
        """Get encounter details with abilities and loot"""
        for instance in self.instances.values():
            for encounter in instance.encounters:
                if encounter.id == encounter_id:
                    return {
                        "id": encounter.id,
                        "name": encounter.name,
                        "description": encounter.description,
                        "instance": instance.name,
                        "abilities": [
                            {
                                "name": a.name,
                                "description": a.description,
                                "role": a.role.value,
                                "importance": a.importance,
                                "phase": a.phase
                            }
                            for a in encounter.abilities
                        ],
                        "loot": [
                            {
                                "name": l.name,
                                "slot": l.slot,
                                "ilvl": l.item_level,
                                "type": l.type
                            }
                            for l in encounter.loot
                        ]
                    }
        return None

    def get_quest(self, quest_id: int, character_guid: str = None) -> Optional[Dict]:
        """Get quest details and completion status"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            # Get Definition
            cur.execute("SELECT * FROM quest_definitions WHERE quest_id = ?", (quest_id,))
            row = cur.fetchone()
            
            if not row:
                return None
                
            quest = {
                "id": row["quest_id"],
                "title": row["title"],
                "description": row["description"],
                "min_level": row["min_level"],
                "zone": row["area_name"],
                "x": row["x_coord"],
                "y": row["y_coord"],
                "map_id": row["map_id"],
                "completed": False
            }
            
            # Check Completion
            if character_guid:
                cur.execute(
                    "SELECT 1 FROM completed_quests WHERE character_guid = ? AND quest_id = ?", 
                    (character_guid, quest_id)
                )
                if cur.fetchone():
                    quest["completed"] = True
                    
            return quest
            
        except Exception as e:
            print(f"Error fetching quest {quest_id}: {e}")
            return None
        finally:
            conn.close()

    def get_campaign_progress(self, campaign_name: str, character_guid: str) -> Dict:
        """Get progress for a specific campaign"""
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            # Fetch quests for this campaign (Category)
            # We use LIKE to match partial names e.g. "The War Within" matches "The War Within Campaign"
            cur.execute("""
                SELECT quest_id, title, x_coord, y_coord, map_id 
                FROM quest_definitions 
                WHERE category_name LIKE ? OR area_name LIKE ?
                ORDER BY min_level, quest_id
            """, (f"%{campaign_name}%", f"%{campaign_name}%"))
            
            rows = cur.fetchall()
            
            if not rows:
                return {"error": f"Campaign '{campaign_name}' not found"}
            
            quests = []
            total = len(rows)
            completed_count = 0
            
            for row in rows:
                q_id = row["quest_id"]
                is_completed = False
                
                if character_guid:
                    cur.execute(
                        "SELECT 1 FROM completed_quests WHERE character_guid = ? AND quest_id = ?", 
                        (character_guid, q_id)
                    )
                    if cur.fetchone():
                        is_completed = True
                        completed_count += 1
                
                quests.append({
                    "id": q_id,
                    "title": row["title"],
                    "x": row["x_coord"],
                    "y": row["y_coord"],
                    "map_id": row["map_id"],
                    "completed": is_completed
                })
                        
            return {
                "campaign": campaign_name,
                "progress": f"{completed_count}/{total}",
                "percent": int((completed_count/total)*100) if total > 0 else 0,
                "quests": quests
            }
            
        except Exception as e:
            print(f"Error fetching campaign: {e}")
            return {"error": str(e)}
        finally:
            conn.close()

    def get_all_characters(self) -> List[Dict]:
        """Get all characters from the database"""
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT character_guid, name, realm, class FROM characters ORDER BY name")
            rows = cur.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error fetching characters: {e}")
            return []
        finally:
            conn.close()

if __name__ == "__main__":
    # Test the engine
    print("\n" + "="*70)
    print("THE CODEX - Encounter Guide")
    print("="*70)
    
    engine = CodexEngine()
    engine.load_mock_data()
    
    # Test 1: Get Instance
    print("\n" + "="*70)
    print("INSTANCE: Nerub-ar Palace")
    print("="*70)
    
    instance = engine.get_instance(1273)
    if instance:
        print(f"\nName: {instance['name']} ({instance['type']})")
        print(f"Encounters: {len(instance['encounters'])}")
        for enc in instance['encounters']:
            print(f"  - {enc['name']}")
            
    # Test 2: Get Encounter (Queen Ansurek)
    print("\n" + "="*70)
    print("ENCOUNTER: Queen Ansurek")
    print("="*70)
    
    boss = engine.get_encounter(2922)
    if boss:
        print(f"\nBoss: {boss['name']}")
        print(f"Description: {boss['description']}")
        
        print("\nAbilities:")
        for ab in boss['abilities']:
            print(f"  [{ab['role']}] {ab['name']} ({ab['importance']})")
            print(f"    {ab['description']}")
            
        print("\nLoot Table:")
        for item in boss['loot']:
            print(f"  • {item['name']} ({item['slot']} - {item['ilvl']})")
            
    print("\n" + "="*70)
    print("✓ All tests complete!")
    print("="*70)
