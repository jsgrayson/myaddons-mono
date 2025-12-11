import json
import os
from datetime import datetime
from typing import List, Dict, Optional

COMBAT_LOG_FILE = 'combat_log.json'

class CombatManager:
    def __init__(self, data_file: str = COMBAT_LOG_FILE):
        self.data_file = data_file
        self.logs = self._load_data()
        
    def _load_data(self) -> List[Dict]:
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
        
    def _save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.logs, f, indent=2)
            
    def log_battle(self, result: str, enemy_name: str, my_team: str, rounds: int):
        """
        Log a battle result.
        result: "WIN" or "LOSS"
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "result": result.upper(),
            "enemy": enemy_name,
            "my_team": my_team,
            "rounds": rounds
        }
        self.logs.insert(0, entry) # Prepend to keep newest first
        
        # Keep last 1000 battles
        if len(self.logs) > 1000:
            self.logs = self.logs[:1000]
            
        self._save_data()
        
    def get_history(self, limit: int = 50) -> List[Dict]:
        return self.logs[:limit]
        
    def get_stats(self) -> Dict:
        total = len(self.logs)
        if total == 0:
            return {"total": 0, "wins": 0, "losses": 0, "win_rate": 0, "avg_rounds": 0}
            
        wins = sum(1 for log in self.logs if log["result"] == "WIN")
        losses = total - wins
        win_rate = int((wins / total) * 100)
        
        total_rounds = sum(log["rounds"] for log in self.logs)
        avg_rounds = round(total_rounds / total, 1)
        
        return {
            "total": total,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "avg_rounds": avg_rounds
        }
