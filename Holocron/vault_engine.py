#!/usr/bin/env python3
"""
Vault Visualizer - Great Vault Progress Tracker
Tracks weekly progress for Raids, Dungeons, and World activities
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import datetime

class VaultCategory(Enum):
    RAID = "Raid"
    DUNGEON = "Dungeons"
    WORLD = "World"

class VaultState(Enum):
    LOCKED = "Locked"
    UNLOCKED = "Unlocked"
    CLAIMED = "Claimed"

@dataclass
class VaultSlot:
    id: int  # 1, 2, 3
    category: VaultCategory
    requirement_text: str  # e.g. "Defeat 2 Raid Bosses"
    current_progress: int
    max_progress: int
    state: VaultState
    reward_ilvl: int = 0
    reward_track: str = ""  # e.g. "Heroic", "Mythic", "Veteran"

class VaultEngine:
    """
    Engine for tracking Great Vault progress
    """
    
    def __init__(self):
        self.slots = {}  # {category: [VaultSlot]}
        self._initialize_slots()
        
    def _initialize_slots(self):
        """Initialize empty vault slots"""
        # Raid Slots (2, 4, 6 bosses)
        self.slots[VaultCategory.RAID] = [
            VaultSlot(1, VaultCategory.RAID, "Defeat 2 Raid Bosses", 0, 2, VaultState.LOCKED),
            VaultSlot(2, VaultCategory.RAID, "Defeat 4 Raid Bosses", 0, 4, VaultState.LOCKED),
            VaultSlot(3, VaultCategory.RAID, "Defeat 6 Raid Bosses", 0, 6, VaultState.LOCKED)
        ]
        
        # Dungeon Slots (1, 4, 8 dungeons)
        self.slots[VaultCategory.DUNGEON] = [
            VaultSlot(1, VaultCategory.DUNGEON, "Complete 1 Heroic, Mythic, or Timewalking Dungeon", 0, 1, VaultState.LOCKED),
            VaultSlot(2, VaultCategory.DUNGEON, "Complete 4 Heroic, Mythic, or Timewalking Dungeons", 0, 4, VaultState.LOCKED),
            VaultSlot(3, VaultCategory.DUNGEON, "Complete 8 Heroic, Mythic, or Timewalking Dungeons", 0, 8, VaultState.LOCKED)
        ]
        
        # World Slots (2, 4, 8 delves/world activities)
        self.slots[VaultCategory.WORLD] = [
            VaultSlot(1, VaultCategory.WORLD, "Complete 2 Delves or World Activities", 0, 2, VaultState.LOCKED),
            VaultSlot(2, VaultCategory.WORLD, "Complete 4 Delves or World Activities", 0, 4, VaultState.LOCKED),
            VaultSlot(3, VaultCategory.WORLD, "Complete 8 Delves or World Activities", 0, 8, VaultState.LOCKED)
        ]

    def load_mock_data(self):
        """Load mock progress data"""
        # Mock Raid Progress: 3/8 Heroic Bosses killed
        # Slot 1 (2 bosses): Unlocked
        # Slot 2 (4 bosses): Locked (3/4)
        # Slot 3 (6 bosses): Locked (3/6)
        raid_slots = self.slots[VaultCategory.RAID]
        raid_slots[0].current_progress = 3
        raid_slots[0].state = VaultState.UNLOCKED
        raid_slots[0].reward_ilvl = 619
        raid_slots[0].reward_track = "Heroic"
        
        raid_slots[1].current_progress = 3
        raid_slots[2].current_progress = 3
        
        # Mock Dungeon Progress: 5 runs
        # Run 1: +10 (Mythic Track)
        # Run 2: +8 (Heroic Track)
        # Run 3: +8 (Heroic Track)
        # Run 4: +4 (Champion Track)
        # Run 5: +2 (Veteran Track)
        
        # Slot 1 (1 run): Unlocked (Best run: +10) -> Mythic Track (623)
        dungeon_slots = self.slots[VaultCategory.DUNGEON]
        dungeon_slots[0].current_progress = 5
        dungeon_slots[0].state = VaultState.UNLOCKED
        dungeon_slots[0].reward_ilvl = 623
        dungeon_slots[0].reward_track = "Mythic"
        
        # Slot 2 (4 runs): Unlocked (4th best run: +4) -> Champion Track (606)
        dungeon_slots[1].current_progress = 5
        dungeon_slots[1].state = VaultState.UNLOCKED
        dungeon_slots[1].reward_ilvl = 606
        dungeon_slots[1].reward_track = "Champion"
        
        # Slot 3 (8 runs): Locked (5/8)
        dungeon_slots[2].current_progress = 5
        
        # Mock World Progress: 8/8 Delves (Tier 8)
        # All slots unlocked at Heroic/Champion track
        world_slots = self.slots[VaultCategory.WORLD]
        for slot in world_slots:
            slot.current_progress = 8
            slot.state = VaultState.UNLOCKED
            slot.reward_ilvl = 616
            slot.reward_track = "Heroic"
            
        print("✓ Loaded mock Vault progress")

    def get_status(self) -> Dict:
        """Get full vault status"""
        return {
            "raid": [self._serialize_slot(s) for s in self.slots[VaultCategory.RAID]],
            "dungeon": [self._serialize_slot(s) for s in self.slots[VaultCategory.DUNGEON]],
            "world": [self._serialize_slot(s) for s in self.slots[VaultCategory.WORLD]],
            "summary": self._get_summary()
        }
        
    def _serialize_slot(self, slot: VaultSlot) -> Dict:
        return {
            "id": slot.id,
            "requirement": slot.requirement_text,
            "progress": f"{slot.current_progress}/{slot.max_progress}",
            "percent": int((slot.current_progress / slot.max_progress) * 100),
            "state": slot.state.value,
            "reward_ilvl": slot.reward_ilvl,
            "reward_track": slot.reward_track
        }
        
    def _get_summary(self) -> Dict:
        """Get high-level summary of unlocked rewards"""
        unlocked_count = 0
        max_ilvl = 0
        
        for category in self.slots.values():
            for slot in category:
                if slot.state == VaultState.UNLOCKED:
                    unlocked_count += 1
                    if slot.reward_ilvl > max_ilvl:
                        max_ilvl = slot.reward_ilvl
                        
        return {
            "unlocked_slots": unlocked_count,
            "total_slots": 9,
            "max_reward_ilvl": max_ilvl,
            "next_reset": self._get_next_reset()
        }
        
    def _get_next_reset(self) -> str:
        """Calculate time until next Tuesday 10am"""
        now = datetime.datetime.now()
        today = now.weekday() # 0=Mon, 1=Tue, ...
        
        # Calculate days until Tuesday (1)
        days_until = (1 - today) % 7
        if days_until == 0 and now.hour >= 10:
            days_until = 7
            
        reset_date = now + datetime.timedelta(days=days_until)
        reset_date = reset_date.replace(hour=10, minute=0, second=0, microsecond=0)
        
        remaining = reset_date - now
        days = remaining.days
        hours = remaining.seconds // 3600
        
        return f"{days}d {hours}h"

if __name__ == "__main__":
    # Test the engine
    print("\n" + "="*70)
    print("VAULT VISUALIZER - Great Vault Tracker")
    print("="*70)
    
    engine = VaultEngine()
    engine.load_mock_data()
    
    status = engine.get_status()
    
    # Test 1: Summary
    print("\n" + "="*70)
    print("WEEKLY SUMMARY")
    print("="*70)
    summary = status['summary']
    print(f"Unlocked Slots: {summary['unlocked_slots']}/9")
    print(f"Max Reward: {summary['max_reward_ilvl']} ilvl")
    print(f"Reset In: {summary['next_reset']}")
    
    # Test 2: Categories
    for cat_name, slots in status.items():
        if cat_name == "summary": continue
        
        print(f"\n{cat_name.upper()} PROGRESS:")
        for slot in slots:
            status_icon = "🔓" if slot['state'] == "Unlocked" else "🔒"
            reward_text = f"- {slot['reward_ilvl']} ({slot['reward_track']})" if slot['reward_ilvl'] > 0 else ""
            print(f"  {status_icon} Slot {slot['id']}: {slot['progress']} {reward_text}")
            
    print("\n" + "="*70)
    print("✓ All tests complete!")
    print("="*70)
