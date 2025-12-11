#!/usr/bin/env python3
"""
The Scout - Push Alert System
Tracks time-sensitive events and generates alerts
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import datetime

class EventType(Enum):
    WORLD_BOSS = "World Boss"
    RARE = "Rare Spawn"
    EVENT = "World Event"
    RESET = "Reset"

class Urgency(Enum):
    CRITICAL = "Critical"  # < 5 mins
    HIGH = "High"         # < 15 mins
    MEDIUM = "Medium"     # < 30 mins
    LOW = "Low"          # > 30 mins

@dataclass
class GameEvent:
    id: int
    name: str
    event_type: EventType
    zone: str
    next_spawn: datetime.datetime
    duration_minutes: int
    location_coords: str  # "45.2, 33.1"
    
    @property
    def is_active(self) -> bool:
        now = datetime.datetime.now()
        end_time = self.next_spawn + datetime.timedelta(minutes=self.duration_minutes)
        return self.next_spawn <= now <= end_time

@dataclass
class Alert:
    event_name: str
    type: str
    message: str
    urgency: Urgency
    time_remaining: str
    action_link: str

class ScoutEngine:
    """
    Engine for tracking events and generating alerts
    """
    
    def __init__(self):
        self.events = []
        
    def load_mock_data(self):
        """Load mock event data"""
        now = datetime.datetime.now()
        
        # 1. World Boss: Kordac (Spawning in 5 mins)
        kordac = GameEvent(
            1, "Kordac", EventType.WORLD_BOSS, "Isle of Dorn",
            now + datetime.timedelta(minutes=5),
            15, "48.2, 22.5"
        )
        
        # 2. Rare: Alunira (Active for 10 more mins)
        alunira = GameEvent(
            2, "Alunira", EventType.RARE, "Isle of Dorn",
            now - datetime.timedelta(minutes=5),
            15, "22.1, 55.3"
        )
        
        # 3. Event: Theater Troupe (Starts in 2 mins)
        theater = GameEvent(
            3, "Theater Troupe", EventType.EVENT, "Isle of Dorn",
            now + datetime.timedelta(minutes=2),
            20, "55.5, 44.2"
        )
        
        # 4. Reset: Daily Reset (Tomorrow)
        reset = GameEvent(
            4, "Daily Reset", EventType.RESET, "Global",
            now + datetime.timedelta(hours=14),
            0, ""
        )
        
        self.events = [kordac, alunira, theater, reset]
        print(f"✓ Loaded {len(self.events)} tracked events")
        
    def get_alerts(self) -> List[Dict]:
        """Get active and upcoming alerts"""
        alerts = []
        now = datetime.datetime.now()
        
        for event in self.events:
            time_diff = event.next_spawn - now
            minutes_until = time_diff.total_seconds() / 60
            
            # Logic: Alert if active OR starting within 30 mins
            if event.is_active:
                alert = Alert(
                    event.name,
                    event.event_type.value,
                    f"Active Now! ({event.zone})",
                    Urgency.CRITICAL,
                    "Active",
                    f"/api/pathfinder/route?dest={event.zone}"
                )
                alerts.append(alert)
                
            elif 0 < minutes_until <= 30:
                urgency = Urgency.LOW
                if minutes_until < 5: urgency = Urgency.CRITICAL
                elif minutes_until < 15: urgency = Urgency.HIGH
                elif minutes_until < 30: urgency = Urgency.MEDIUM
                
                alert = Alert(
                    event.name,
                    event.event_type.value,
                    f"Spawning in {int(minutes_until)}m ({event.zone})",
                    urgency,
                    f"{int(minutes_until)}m",
                    f"/api/pathfinder/route?dest={event.zone}"
                )
                alerts.append(alert)
                
        # Sort by urgency (Critical first)
        urgency_order = {Urgency.CRITICAL: 1, Urgency.HIGH: 2, Urgency.MEDIUM: 3, Urgency.LOW: 4}
        alerts.sort(key=lambda x: urgency_order[x.urgency])
        
        return [
            {
                "event": a.event_name,
                "type": a.type,
                "message": a.message,
                "urgency": a.urgency.value,
                "time": a.time_remaining,
                "action": a.action_link
            }
            for a in alerts
        ]

if __name__ == "__main__":
    # Test the engine
    print("\n" + "="*70)
    print("THE SCOUT - Push Alert System")
    print("="*70)
    
    engine = ScoutEngine()
    engine.load_mock_data()
    
    alerts = engine.get_alerts()
    
    print("\n" + "="*70)
    print("ACTIVE ALERTS")
    print("="*70)
    
    for alert in alerts:
        icon = "🚨" if alert['urgency'] == "Critical" else "⚠️"
        print(f"\n{icon} {alert['event']} ({alert['type']})")
        print(f"   {alert['message']}")
        print(f"   Urgency: {alert['urgency']}")
        print(f"   Action: {alert['action']}")
            
    print("\n" + "="*70)
    print("✓ All tests complete!")
    print("="*70)
