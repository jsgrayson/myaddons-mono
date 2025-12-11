"""
NPC AI Script Loader

Loads and parses enhanced enemy AI scripts from enhanced_enemy_npc_scripts.json
Converts them into executable combat logic for the battle simulator.
"""

import json
import re
from pathlib import Path

class NPCAILoader:
    def __init__(self, scripts_path='enhanced_enemy_npc_scripts.json'):
        self.scripts_path = Path(scripts_path)
        self.ai_scripts = {}
        self.load_scripts()
    
    def load_scripts(self):
        """Load all enemy AI scripts from JSON."""
        if not self.scripts_path.exists():
            print(f"⚠️  AI scripts not found: {self.scripts_path}")
            return
        
        with open(self.scripts_path, 'r') as f:
            data = json.load(f)
        
        self.ai_scripts = data.get('npc_scripts', {})
        print(f"✅ Loaded {len(self.ai_scripts)} enemy AI scripts")
    
    def get_ai_for_encounter(self, encounter_name):
        """Get parsed AI for a specific encounter."""
        if encounter_name not in self.ai_scripts:
            return None
        
        script_data = self.ai_scripts[encounter_name]
        raw_script = script_data.get('ai_script', '')
        
        if not raw_script:
            return None
        
        return self.parse_ai_script(raw_script, encounter_name)
    
    def parse_ai_script(self, script_text, encounter_name):
        """Parse AI script text into structured combat logic."""
        
        lines = script_text.replace('\\n', '\n').split('\n')
        
        parsed = {
            'encounter_name': encounter_name,
            'characteristics': [],
            'priority_abilities': [],  # [round=1]
            'hp_conditionals': [],     # [enemy.hp>X]
            'general_rotation': []    # Default moves
        }
        
        for line in lines:
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                # Extract characteristics from comments
                if '[' in line and '%]' in line:
                    char_match = re.search(r'\[(\d+)%\]\s*(.+)', line)
                    if char_match:
                        confidence = int(char_match.group(1))
                        description = char_match.group(2)
                        parsed['characteristics'].append({
                            'confidence': confidence,
                            'description': description
                        })
                continue
            
            # Parse use() commands
            use_match = re.match(r'use\(([^:]+):(\d+)\)\s*(.*)$', line)
            if not use_match:
                continue
            
            ability_name = use_match.group(1)
            ability_id = int(use_match.group(2))
            condition = use_match.group(3).strip()
            
            ability = {
                'name': ability_name,
                'id': ability_id,
                'condition': condition
            }
            
            # Categorize by condition type
            if '[round=' in condition:
                parsed['priority_abilities'].append(ability)
            elif '[enemy.hp' in condition:
                parsed['hp_conditionals'].append(ability)
            else:
                parsed['general_rotation'].append(ability)
        
        return parsed
    
    def has_ai_for_encounter(self, encounter_name):
        """Check if AI exists for encounter."""
        return encounter_name in self.ai_scripts

# Global loader instance
_ai_loader = None

def get_ai_loader():
    """Get global AI loader instance."""
    global _ai_loader
    if _ai_loader is None:
        _ai_loader = NPCAILoader()
    return _ai_loader

def load_encounter_ai(encounter_name):
    """Convenience function to load AI for an encounter."""
    loader = get_ai_loader()
    return loader.get_ai_for_encounter(encounter_name)
