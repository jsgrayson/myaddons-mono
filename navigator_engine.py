#!/usr/bin/env python3
"""
The Navigator - Intelligent Activity Recommender
Prioritizes farming activities based on value, lockouts, and proximity
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class ActivityType(Enum):
    MOUNT = "Mount"
    PET = "Pet"
    TRANSMOG = "Transmog"
    TOY = "Toy"
    GOLD = "Gold"
    REPUTATION = "Reputation"

# Value scoring for different activity types
ACTIVITY_SCORES = {
    ActivityType.MOUNT: 100,   # Rare mounts are highest priority
    ActivityType.PET: 75,       # Pets are valuable
    ActivityType.TOY: 60,       # Toys are collectible
    ActivityType.TRANSMOG: 50,  # Rare transmog
    ActivityType.GOLD: 30,      # Gold farming
    ActivityType.REPUTATION: 40 # Rep grinding
}

@dataclass
class Activity:
    instance_name: str
    drop_name: str
    drop_type: ActivityType
    expansion: str
    instance_type: str  # "Raid", "Dungeon", "Holiday"
    available_chars: int = 0
    zone_id: Optional[int] = None
    is_owned: bool = False
    rarity: str = "Rare"  # "Rare", "Common", "Epic"
    time_estimate: int = 15 # Minutes
    
    @property
    def ppm(self) -> float:
        """Points Per Minute (Efficiency)"""
        if self.time_estimate <= 0: return 0
        return self.score / self.time_estimate

    @property
    def score(self) -> int:
        """Calculate activity value score"""
        base_score = ACTIVITY_SCORES.get(self.drop_type, 20)
        
        # Boost for rare/epic items
        if self.rarity == "Epic":
            base_score = int(base_score * 1.5)
        elif self.rarity == "Common":
            base_score = int(base_score * 0.7)
        
        # Penalty if already owned
        if self.is_owned:
            base_score = int(base_score * 0.1)
        
        # Penalty if no chars available (locked)
        if self.available_chars == 0:
            base_score = int(base_score * 0.2)
        
        return base_score
    
    @property
    def priority_label(self) -> str:
        """Human-readable priority"""
        # Use PPM for priority label if efficiency matters
        if self.score >= 80:
            return "CRITICAL"
        elif self.score >= 50:
            return "HIGH"
        elif self.score >= 30:
            return "MEDIUM"
        else:
            return "LOW"

class NavigatorEngine:
    """
    Activity recommender that prioritizes farming activities
    """
    
    def __init__(self):
        self.activities = []
        self.owned_items = set()  # Mock collection
        
    def load_mock_data(self):
        """Load mock farming activities"""
        
        # Mock owned items (already collected)
        self.owned_items = {
            "Reins of the Bronze Drake",  # Already have this
            "Anzu's Cursed Talon"  # Already have this
        }
        
        # Mock activities
        self.activities = [
            # High-value rare mounts (unlocked)
            Activity("Icecrown Citadel", "Invincible's Reins", ActivityType.MOUNT,
                    "WotLK", "Raid", available_chars=5, zone_id=125, rarity="Epic", time_estimate=30),
            
            Activity("Firelands", "Flametalon of Alysrazor", ActivityType.MOUNT,
                    "Cataclysm", "Raid", available_chars=4, zone_id=198, rarity="Rare", time_estimate=20),
            
            Activity("The Eye", "Ashes of Al'ar", ActivityType.MOUNT,
                    "TBC", "Raid", available_chars=8, zone_id=109, rarity="Epic", time_estimate=15),
            
            # Already owned (low priority)
            Activity("The Culling of Stratholme", "Reins of the Bronze Drake", ActivityType.MOUNT,
                    "WotLK", "Dungeon", available_chars=8, zone_id=125, 
                    is_owned=True, rarity="Rare", time_estimate=15),
            
            # Locked (no chars available)
            Activity("Vault of the Incarnates", "Renewed Proto-Drake", ActivityType.MOUNT,
                    "Dragonflight", "Raid", available_chars=0, zone_id=2112, rarity="Epic", time_estimate=45),
            
            # Pets
            Activity("Molten Core", "Untamed Hatchling", ActivityType.PET,
                    "Vanilla", "Raid", available_chars=6, zone_id=230, rarity="Rare", time_estimate=25),
            
            # Transmog
            Activity("Throne of Thunder", "Tier 15 Recolor", ActivityType.TRANSMOG,
                    "Pandaria", "Raid", available_chars=3, zone_id=928, rarity="Rare", time_estimate=40),
            
            Activity("Blackrock Foundry", "Tier 17 Set", ActivityType.TRANSMOG,
                    "WoD", "Raid", available_chars=7, zone_id=543, rarity="Common", time_estimate=35),
            
            # Gold farming
            Activity("Freehold", "Gold Farm (3k/hr)", ActivityType.GOLD,
                    "BfA", "Dungeon", available_chars=5, zone_id=1161, rarity="Common", time_estimate=10),
            
            # Reputation
            Activity("Isle of Dorn", "Council of Dornogal WQs", ActivityType.REPUTATION,
                    "TWW", "World Quest", available_chars=1, zone_id=2248, rarity="Common", time_estimate=5),
        ]
        
        print(f"✓ Loaded {len(self.activities)} activities, {len(self.owned_items)} owned items")
    
    def get_prioritized_activities(self, 
                                   include_owned: bool = False,
                                   min_available: int = 1) -> List[Dict]:
        """
        Get activities sorted by priority
        
        Args:
            include_owned: Include already-collected items
            min_available: Minimum available characters
        
        Returns:
            List of activities with scores and metadata
        """
        filtered = []
        
        for activity in self.activities:
            # Filter owned items
            if not include_owned and activity.is_owned:
                continue
            
            # Filter locked instances
            if activity.available_chars < min_available:
                continue
            
            filtered.append({
                "instance": activity.instance_name,
                "drop": activity.drop_name,
                "type": activity.drop_type.value,
                "expansion": activity.expansion,
                "instance_type": activity.instance_type,
                "available_chars": activity.available_chars,
                "score": activity.score,
                "ppm": round(activity.ppm, 2),
                "time": activity.time_estimate,
                "priority": activity.priority_label,
                "rarity": activity.rarity,
                "is_owned": activity.is_owned,
                "zone_id": activity.zone_id
            })
        
        # Sort by PPM (Efficiency) instead of raw score?
        # Let's sort by Score first, then PPM as tiebreaker, or weighted?
        # For "Boredom Buster", maybe Score is better (coolest stuff).
        # For "Efficiency", PPM is better.
        # Let's keep Score as primary sort, but expose PPM.
        filtered.sort(key=lambda x: x["score"], reverse=True)
        
        return filtered
    
    def get_statistics(self) -> Dict:
        """Get summary statistics"""
        total = len(self.activities)
        owned = sum(1 for a in self.activities if a.is_owned)
        available = sum(1 for a in self.activities if a.available_chars > 0 and not a.is_owned)
        locked = sum(1 for a in self.activities if a.available_chars == 0)
        
        # Count by type
        by_type = {}
        for activity in self.activities:
            type_name = activity.drop_type.value
            by_type[type_name] = by_type.get(type_name, 0) + 1
        
        return {
            "total_activities": total,
            "owned": owned,
            "available": available,
            "locked": locked,
            "by_type": by_type,
            "completion_percent": int((owned / total) * 100) if total > 0 else 0
        }
    
    def get_urgent_activities(self, limit: int = 5) -> List[Dict]:
        """Get top priority activities (score >= 80)"""
        activities = self.get_prioritized_activities()
        urgent = [a for a in activities if a["score"] >= 80]
        return urgent[:limit]

if __name__ == "__main__":
    # Test the engine
    print("\n" + "="*70)
    print("THE NAVIGATOR - Activity Recommender")
    print("="*70)
    
    engine = NavigatorEngine()
    engine.load_mock_data()
    
    # Test 1: Get prioritized activities
    print("\n" + "="*70)
    print("PRIORITIZED ACTIVITIES (Top 5)")
    print("="*70)
    
    activities = engine.get_prioritized_activities()[:5]
    for i, act in enumerate(activities, 1):
        print(f"\n  {i}. {act['drop']} ({act['score']} pts - {act['priority']})")
        print(f"     Instance: {act['instance']} ({act['expansion']})")
        print(f"     Type: {act['type']} ({act['rarity']})")
        print(f"     Available: {act['available_chars']} characters")
    
    # Test 2: Statistics
    print("\n" + "="*70)
    print("COLLECTION STATISTICS")
    print("="*70)
    
    stats = engine.get_statistics()
    print(f"\n  Total Activities: {stats['total_activities']}")
    print(f"  Owned: {stats['owned']} ({stats['completion_percent']}%)")
    print(f"  Available: {stats['available']}")
    print(f"  Locked: {stats['locked']}")
    print(f"\n  By Type:")
    for type_name, count in stats['by_type'].items():
        print(f"    - {type_name}: {count}")
    
    # Test 3: Urgent activities
    print("\n" + "="*70)
    print("URGENT ACTIVITIES (Score >= 80)")
    print("="*70)
    
    urgent = engine.get_urgent_activities()
    if urgent:
        print(f"\n  Found {len(urgent)} urgent activities:\n")
        for act in urgent:
            print(f"  • {act['drop']} - {act['instance']}")
            print(f"    Score: {act['score']} | Available: {act['available_chars']} chars")
    else:
        print("\n  No urgent activities found.")
    
    # Test 4: Include owned items
    print("\n" + "="*70)
    print("ALL ACTIVITIES (including owned)")
    print("="*70)
    
    all_activities = engine.get_prioritized_activities(include_owned=True)
    print(f"\n  Total: {len(all_activities)} activities")
    print(f"  Showing owned items with reduced scores...")
    
    owned = [a for a in all_activities if a['is_owned']]
    for act in owned:
        print(f"\n  • {act['drop']} (OWNED)")
        print(f"    Score: {act['score']} (reduced from base)")
    
    print("\n" + "="*70)
    print("✓ All tests complete!")
    print("="*70)
