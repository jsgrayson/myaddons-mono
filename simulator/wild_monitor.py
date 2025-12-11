import json
import os
from typing import Dict, List, Optional

import time

class WildPetMonitor:
    def __init__(self):
        self.wanted_pets = {} # pet_id -> {reason, priority}
        self.owned_pets = set()
        self.mythical_pets = {150381, 150385, 154832} # Known high value
        self.current_alert = None # {alert, level, message, timestamp}
        self._load_data()

    def _load_data(self):
        """Load strategies and collection to build wanted list"""
        try:
            # 1. Load Owned Pets
            if os.path.exists('my_pets.json'):
                with open('my_pets.json', 'r') as f:
                    data = json.load(f)
                    for pet in data.get('pets', []):
                        if 'species' in pet:
                            self.owned_pets.add(pet['species']['id'])

            # 2. Load Strategies to find needed pets
            if os.path.exists('strategies_enhanced.json'):
                with open('strategies_enhanced.json', 'r') as f:
                    strategies = json.load(f)
                    self._parse_strategies(strategies)
                    
        except Exception as e:
            print(f"Error loading WildPetMonitor data: {e}")

    def _parse_strategies(self, data: Dict):
        """Extract needed pets from strategies"""
        for exp in data.values():
            if not isinstance(exp, dict): continue
            for cat in exp.values():
                for encounter in cat:
                    for strat in encounter.get('strategies', []):
                        for slot in strat.get('pet_slots', []):
                            for option in slot:
                                pid = option.get('id')
                                if not pid: continue
                                
                                # If we don't own it, it's wanted
                                if pid not in self.owned_pets:
                                    if pid not in self.wanted_pets:
                                        self.wanted_pets[pid] = {
                                            'reason': 'Strategy Requirement',
                                            'priority': 'HIGH',
                                            'encounters': []
                                        }
                                    self.wanted_pets[pid]['encounters'].append(encounter.get('encounter_name'))

    def check_wild_pet(self, pet_id: int, rarity: str = 'COMMON') -> Dict:
        """
        Check if a wild pet is worth capturing.
        Returns: { 'alert': bool, 'level': 'CRITICAL'|'INFO', 'message': str }
        """
        alert = {'alert': False, 'level': 'NONE', 'message': ''}
        
        # 1. Check if it's a Mythical/Special pet
        if pet_id in self.mythical_pets:
            alert = {
                'alert': True,
                'level': 'CRITICAL',
                'message': 'MYTHICAL PET DETECTED! CAPTURE IMMEDIATELY!'
            }

        # 2. Check if it's needed for a strategy
        elif pet_id in self.wanted_pets:
            info = self.wanted_pets[pet_id]
            alert = {
                'alert': True,
                'level': 'CRITICAL',
                'message': f"NEEDED FOR STRATEGY! Used in: {', '.join(info['encounters'][:2])}"
            }

        # 3. Check for Rares (Blue) that we don't have
        elif rarity == 'RARE' and pet_id not in self.owned_pets:
             alert = {
                'alert': True,
                'level': 'INFO',
                'message': 'Rare quality wild pet detected. You do not own this species.'
            }
        
        if alert['alert']:
            self.current_alert = alert
            self.current_alert['timestamp'] = time.time()
            
        return alert
