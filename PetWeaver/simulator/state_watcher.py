"""
Battle State Watcher System

Tracks specific values across battle turns for debugging and analysis.
Supports:
- Variable watching (track specific attributes)
- Conditional alerts (trigger on conditions)
- History tracking (see changes over time)
- Event recording (combat log foundation)
"""

from typing import Any, Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class WatchExpression:
    """A single watched variable expression"""
    name: str
    path: str  # e.g., "player_team.pets[0].stats.current_hp"
    alert_condition: Optional[Callable[[Any], bool]] = None
    alert_message: Optional[str] = None
    history: List[Tuple[int, Any]] = field(default_factory=list)  # (turn, value)
    last_value: Any = None
    
    def evaluate(self, state, turn: int) -> Tuple[bool, Any]:
        """Evaluate expression against current state. Returns (changed, value)"""
        try:
            # Navigate the path
            value = self._get_value(state, self.path)
            changed = value != self.last_value
            
            if changed:
                self.history.append((turn, value))
                self.last_value = value
            
            return changed, value
        except Exception as e:
            return False, f"ERROR: {e}"
    
    def _get_value(self, obj, path: str) -> Any:
        """Navigate a dotted path to get value"""
        parts = path.split('.')
        current = obj
        
        for part in parts:
            # Handle array indexing
            if '[' in part:
                attr_name = part[:part.index('[')]
                index = int(part[part.index('[')+1:part.index(']')])
                current = getattr(current, attr_name)[index]
            else:
                current = getattr(current, part)
        
        return current
    
    def check_alert(self, value: Any) -> bool:
        """Check if alert condition is met"""
        if self.alert_condition is None:
            return False
        try:
            return self.alert_condition(value)
        except:
            return False


@dataclass
class BattleEvent:
    """A single event in the battle"""
    turn: int
    timestamp: datetime
    event_type: str  # 'ability', 'damage', 'buff', 'swap', 'turn_end', etc.
    actor: str  # 'player' or 'enemy'
    data: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return {
            'turn': self.turn,
            'timestamp': self.timestamp.isoformat(),
            'type': self.event_type,
            'actor': self.actor,
            'data': self.data
        }


class StateWatcher:
    """
    Watches battle state changes and records events.
    
    Usage:
        watcher = StateWatcher()
        watcher.watch("player_hp", "player_team.pets[0].stats.current_hp", 
                     alert_on=lambda v: v < 500, message="Player HP critical!")
        
        # In battle loop:
        watcher.update(state, turn_number)
        watcher.print_changes()
    """
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.watches: Dict[str, WatchExpression] = {}
        self.events: List[BattleEvent] = []
        self.current_turn = 0
        self.alerts_triggered: List[Tuple[int, str, str]] = []  # (turn, watch_name, message)
    
    def watch(self, name: str, path: str, 
              alert_on: Optional[Callable[[Any], bool]] = None,
              message: Optional[str] = None):
        """Add a variable to watch"""
        self.watches[name] = WatchExpression(
            name=name,
            path=path,
            alert_condition=alert_on,
            alert_message=message or f"{name} condition triggered"
        )
    
    def record_event(self, turn: int, event_type: str, actor: str, **data):
        """Record a battle event"""
        if not self.enabled:
            return
        
        event = BattleEvent(
            turn=turn,
            timestamp=datetime.now(),
            event_type=event_type,
            actor=actor,
            data=data
        )
        self.events.append(event)
    
    def update(self, state, turn: int):
        """Update all watches for current state"""
        if not self.enabled:
            return
        
        self.current_turn = turn
        changes = []
        
        for watch in self.watches.values():
            changed, value = watch.evaluate(state, turn)
            
            if changed:
                changes.append((watch.name, watch.last_value, value))
                
                # Check alert condition
                if watch.check_alert(value):
                    self.alerts_triggered.append((turn, watch.name, watch.alert_message))
        
        return changes
    
    def print_changes(self, verbose: bool = False):
        """Print recent changes"""
        if not self.enabled or not self.watches:
            return
        
        print(f"\n{'='*60}")
        print(f"Turn {self.current_turn} - State Watch")
        print(f"{'='*60}")
        
        for name, watch in self.watches.items():
            if watch.last_value is not None:
                status = "⚠️ " if any(a[1] == name for a in self.alerts_triggered if a[0] == self.current_turn) else "  "
                print(f"{status}{name}: {watch.last_value}")
                
                if verbose and len(watch.history) > 1:
                    print(f"   History: {watch.history[-5:]}")  # Last 5 values
        
        # Print alerts
        current_alerts = [a for a in self.alerts_triggered if a[0] == self.current_turn]
        if current_alerts:
            print(f"\n🚨 ALERTS:")
            for turn, name, message in current_alerts:
                print(f"   {message}")
    
    def get_history(self, watch_name: str) -> List[Tuple[int, Any]]:
        """Get full history for a watch"""
        if watch_name in self.watches:
            return self.watches[watch_name].history
        return []
    
    def export_combat_log(self, filename: str):
        """Export all events to JSON file (Combat Log)"""
        log_data = {
            'total_turns': self.current_turn,
            'watches': {
                name: {
                    'path': w.path,
                    'history': w.history
                }
                for name, w in self.watches.items()
            },
            'events': [e.to_dict() for e in self.events],
            'alerts': [
                {'turn': t, 'watch': n, 'message': m}
                for t, n, m in self.alerts_triggered
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"✅ Combat log exported to {filename}")
    
    def clear(self):
        """Clear all history and events"""
        for watch in self.watches.values():
            watch.history.clear()
            watch.last_value = None
        self.events.clear()
        self.alerts_triggered.clear()
        self.current_turn = 0
