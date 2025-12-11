#!/usr/bin/env python3
"""
Knowledge Point Tracker - TWW Profession Knowledge Checklist
Tracks weekly/one-time knowledge point sources with auto-reset logic
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

class SourceType(Enum):
    WEEKLY = "Weekly"
    ONE_TIME = "One-Time"

class Profession(Enum):
    BLACKSMITHING = "Blacksmithing"
    ALCHEMY = "Alchemy"
    ENCHANTING = "Enchanting"
    ENGINEERING = "Engineering"
    INSCRIPTION = "Inscription"
    JEWELCRAFTING = "Jewelcrafting"
    LEATHERWORKING = "Leatherworking"
    TAILORING = "Tailoring"

@dataclass
class KnowledgeSource:
    source_id: int
    name: str
    profession: Profession
    source_type: SourceType
    points: int
    category: str  # "First Craft", "Treasure", "Treatise", "Quest", "Rare Drop"
    description: str = ""
    
class KnowledgeTracker:
    """
    Tracks profession knowledge point sources and completion status
    """
    
    def __init__(self):
        self.sources = []
        self.completions = {}  # {character_guid: {source_id: completion_date}}
        
    def load_mock_data(self):
        """Load mock knowledge sources for TWW"""
        
        # Blacksmithing sources
        self.sources = [
            # Weekly Repeatable
            KnowledgeSource(1, "Algari Competitor's Plate", Profession.BLACKSMITHING,
                          SourceType.WEEKLY, 3, "First Craft",
                          "Craft this item for the first time this week"),
            
            KnowledgeSource(2, "Charged Chromed Satchel", Profession.BLACKSMITHING,
                          SourceType.WEEKLY, 2, "First Craft",
                          "Craft this high-quality item"),
            
            KnowledgeSource(3, "Dusty Blacksmith's Diagram", Profession.BLACKSMITHING,
                          SourceType.WEEKLY, 1, "Treasure",
                          "Found in Dornogal or Isle of Dorn"),
            
            KnowledgeSource(4, "Tome of Khaz Algar Blacksmithing", Profession.BLACKSMITHING,
                          SourceType.WEEKLY, 1, "Treatise",
                          "Crafted by Inscriptionists"),
            
            KnowledgeSource(5, "Seared Ore Gathering", Profession.BLACKSMITHING,
                          SourceType.WEEKLY, 1, "Gathering Quest",
                          "Weekly quest in Hallowfall"),
            
            # One-Time
            KnowledgeSource(100, "Ancient Forging Instructions", Profession.BLACKSMITHING,
                          SourceType.ONE_TIME, 10, "Rare Drop",
                          "Rare drop from Dornogal rares"),
            
            KnowledgeSource(101, "The Forgemaster's Wisdom", Profession.BLACKSMITHING,
                          SourceType.ONE_TIME, 15, "Quest",
                          "Complete profession quest chain"),
            
            KnowledgeSource(102, "Master Blacksmith's Techniques", Profession.BLACKSMITHING,
                          SourceType.ONE_TIME, 10, "Quest",
                          "Hidden quest in Earthen city"),
        ]
        
        # Mock completions (for testing)
        self.completions = {
            "GUID-MainWarrior": {
                1: datetime.now() - timedelta(days=2),  # Completed 2 days ago
                3: datetime.now() - timedelta(days=1),  # Completed yesterday
                100: datetime.now() - timedelta(days=30)  # One-time completed
            }
        }
        
        print(f"✓ Loaded {len(self.sources)} knowledge sources")
    
    def get_next_reset(self) -> datetime:
        """Calculate next Tuesday reset (10am server time)"""
        now = datetime.now()
        days_until_tuesday = (1 - now.weekday()) % 7  # Tuesday = 1
        if days_until_tuesday == 0 and now.hour >= 10:
            days_until_tuesday = 7  # Already past reset today
        
        next_reset = now + timedelta(days=days_until_tuesday)
        next_reset = next_reset.replace(hour=10, minute=0, second=0, microsecond=0)
        
        return next_reset
    
    def is_weekly_complete(self, source_id: int, character_guid: str) -> bool:
        """Check if a weekly source has been completed this week"""
        if character_guid not in self.completions:
            return False
        
        if source_id not in self.completions[character_guid]:
            return False
        
        completion_date = self.completions[character_guid][source_id]
        next_reset = self.get_next_reset()
        last_reset = next_reset - timedelta(days=7)
        
        # Completed after last reset = still valid this week
        return completion_date >= last_reset
    
    def get_checklist(self, profession: Profession, character_guid: Optional[str] = None) -> Dict:
        """
        Get knowledge checklist for a profession
        
        Args:
            profession: Which profession to check
            character_guid: Optional character for completion tracking
        
        Returns:
            dict with weekly/one-time sources and progress stats
        """
        weekly_sources = []
        onetime_sources = []
        
        for source in self.sources:
            if source.profession != profession:
                continue
            
            is_complete = False
            if character_guid:
                if source.source_type == SourceType.WEEKLY:
                    is_complete = self.is_weekly_complete(source.source_id, character_guid)
                else:  # ONE_TIME
                    is_complete = source.source_id in self.completions.get(character_guid, {})
            
            source_data = {
                "id": source.source_id,
                "name": source.name,
                "points": source.points,
                "category": source.category,
                "description": source.description,
                "complete": is_complete
            }
            
            if source.source_type == SourceType.WEEKLY:
                weekly_sources.append(source_data)
            else:
                onetime_sources.append(source_data)
        
        # Calculate progress
        weekly_completed = sum(1 for s in weekly_sources if s["complete"])
        onetime_completed = sum(1 for s in onetime_sources if s["complete"])
        
        total_weekly_points = sum(s["points"] for s in weekly_sources)
        earned_weekly_points = sum(s["points"] for s in weekly_sources if s["complete"])
        
        # Reset timer
        next_reset = self.get_next_reset()
        time_until_reset = next_reset - datetime.now()
        
        return {
            "profession": profession.value,
            "weekly": {
                "sources": weekly_sources,
                "completed": weekly_completed,
                "total": len(weekly_sources),
                "percent": int((weekly_completed / len(weekly_sources)) * 100) if weekly_sources else 0,
                "points_earned": earned_weekly_points,
                "points_total": total_weekly_points
            },
            "one_time": {
                "sources": onetime_sources,
                "completed": onetime_completed,
                "total": len(onetime_sources),
                "percent": int((onetime_completed / len(onetime_sources)) * 100) if onetime_sources else 0
            },
            "reset": {
                "next_reset": next_reset.isoformat(),
                "hours_remaining": int(time_until_reset.total_seconds() / 3600),
                "days_remaining": time_until_reset.days
            }
        }
    
    def mark_complete(self, source_id: int, character_guid: str) -> bool:
        """Mark a source as complete for a character"""
        if character_guid not in self.completions:
            self.completions[character_guid] = {}
        
        self.completions[character_guid][source_id] = datetime.now()
        return True
    
    def mark_incomplete(self, source_id: int, character_guid: str) -> bool:
        """Mark a source as incomplete (uncheck)"""
        if character_guid in self.completions:
            if source_id in self.completions[character_guid]:
                del self.completions[character_guid][source_id]
                return True
        return False

if __name__ == "__main__":
    # Test the tracker
    print("\n" + "="*70)
    print("KNOWLEDGE POINT TRACKER")
    print("="*70)
    
    tracker = KnowledgeTracker()
    tracker.load_mock_data()
    
    # Test 1: Get checklist
    print("\n" + "="*70)
    print("BLACKSMITHING CHECKLIST - MainWarrior")
    print("="*70)
    
    checklist = tracker.get_checklist(Profession.BLACKSMITHING, "GUID-MainWarrior")
    
    print(f"\nProfession: {checklist['profession']}")
    print(f"\nWeekly Progress: {checklist['weekly']['completed']}/{checklist['weekly']['total']} ({checklist['weekly']['percent']}%)")
    print(f"Points: {checklist['weekly']['points_earned']}/{checklist['weekly']['points_total']}")
    
    print(f"\nWeekly Sources:")
    for source in checklist['weekly']['sources']:
        status = "✓" if source['complete'] else "☐"
        print(f"  {status} {source['name']} (+{source['points']} points)")
        print(f"     {source['description']}")
    
    print(f"\nOne-Time Progress: {checklist['one_time']['completed']}/{checklist['one_time']['total']} ({checklist['one_time']['percent']}%)")
    print(f"\nOne-Time Sources:")
    for source in checklist['one_time']['sources']:
        status = "✓" if source['complete'] else "☐"
        print(f"  {status} {source['name']} (+{source['points']} points)")
    
    # Test 2: Reset timer
    print(f"\n" + "="*70)
    print("WEEKLY RESET")
    print("="*70)
    print(f"\nNext reset: {checklist['reset']['next_reset']}")
    print(f"Time remaining: {checklist['reset']['days_remaining']}d {checklist['reset']['hours_remaining'] % 24}h")
    
    # Test 3: Mark completion
    print(f"\n" + "="*70)
    print("MARKING COMPLETION")
    print("="*70)
    
    print("\nMarking source #2 as complete...")
    tracker.mark_complete(2, "GUID-MainWarrior")
    
    updated_checklist = tracker.get_checklist(Profession.BLACKSMITHING, "GUID-MainWarrior")
    print(f"New progress: {updated_checklist['weekly']['completed']}/{updated_checklist['weekly']['total']}")
    
    print("\n" + "="*70)
    print("✓ All tests complete!")
    print("="*70)
