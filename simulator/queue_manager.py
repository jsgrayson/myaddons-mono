from typing import List, Dict, Optional
import json
import os
# Remove relative imports if running standalone, but keep for app integration
# Assuming this runs within the petweaver package context
try:
    from .battle_state import Team, Pet, PetStats, PetFamily, PetQuality, Ability
except ImportError:
    # Fallback for standalone testing
    class PetFamily:
        BEAST = 8
    class PetQuality:
        RARE = 4

class QueueManager:
    def __init__(self, species_db: Dict, ability_db: Dict):
        self.species_db = species_db
        self.ability_db = ability_db
        self.history = [] # List of battle results
        self.encounters = {}
        self.my_pets = []
        self._load_data()

    def _load_data(self):
        """Load necessary data files"""
        try:
            # Try absolute paths or relative to CWD
            base_dir = os.getcwd()
            # If running from app.py, we are in petweaver root usually
            # Check common locations
            paths = [
                'encounters_complete.json',
                'petweaver/encounters_complete.json',
                '../encounters_complete.json'
            ]
            
            for p in paths:
                if os.path.exists(p):
                    with open(p, 'r') as f:
                        self.encounters = json.load(f)
                    break
            
            pet_paths = [
                'my_pets.json',
                'petweaver/my_pets.json',
                '../my_pets.json'
            ]
            
            for p in pet_paths:
                if os.path.exists(p):
                    with open(p, 'r') as f:
                        data = json.load(f)
                        self.my_pets = data.get('pets', [])
                    break
                    
        except Exception as e:
            print(f"Error loading queue data: {e}")

    def get_optimal_carry_team(self, leveling_pet_data: Dict, target_id: str) -> Dict:
        """
        Selects 2 max-level pets to carry the leveling pet against a specific target.
        """
        # 1. Get Target Encounter
        target_encounter = self.encounters.get(target_id)
        if not target_encounter:
            # Try fuzzy match
            for key, val in self.encounters.items():
                if target_id.lower() in key.lower() or key.lower() in target_id.lower():
                    target_encounter = val
                    break
        
        if not target_encounter:
            return {"error": f"Encounter '{target_id}' not found"}

        target_pets = target_encounter.get('npc_pets', [])
        if not target_pets:
            return {"error": "Target has no pets defined"}

        # 2. Identify Threats & Find Counters
        # Find counter for Enemy 1 (Primary Threat)
        enemy1 = target_pets[0] if len(target_pets) > 0 else None
        carry_1 = self._find_best_counter(enemy1, exclude_ids=[])
        
        # Find counter for Enemy 2 or 3 (Secondary Threat)
        enemy2 = target_pets[1] if len(target_pets) > 1 else (target_pets[0] if target_pets else None)
        carry_2 = self._find_best_counter(enemy2, exclude_ids=[carry_1['id']] if carry_1 else [])

        # Fallbacks
        if not carry_1: carry_1 = self._get_generic_strong_pet([])
        if not carry_2: carry_2 = self._get_generic_strong_pet([carry_1['id']] if carry_1 else [])

        # Construct Team
        return {
            "leveling_slot": 0,
            "pets": [
                leveling_pet_data,
                carry_1,
                carry_2
            ],
            "strategy_hint": f"Vs {target_encounter.get('name', 'Unknown')}: Start with Leveling Pet, then Swap to {carry_1['name']}."
        }

    def _find_best_counter(self, enemy_pet_data: Optional[Dict], exclude_ids: List[int]) -> Optional[Dict]:
        """Find the best counter from my_pets collection."""
        if not enemy_pet_data: return None
        
        # Hardcoded "Best Generic Counters" list for now
        strong_candidates = [
            1155, # Iron Starlette (Mech > Beast)
            1238, # Ikky (Flying > Aquatic)
            339,  # Unborn Val'kyr (Undead > Humanoid)
            118,  # Worg Pup (Beast > Critter)
            383,  # Snail (Elemental > Mech)
            844,  # Dah'da (Elemental)
            1387, # Twilight Clutch-Sister (Dragonkin)
            68662, # Anubisath Idol (Humanoid - Tank)
            1167, # Emerald Proto-Whelp (Dragonkin - Tank)
        ]
        
        # Filter my_pets for these IDs first
        for pet in self.my_pets:
            if not pet.get('species'): continue
            sid = pet['species']['id']
            if sid in exclude_ids: continue
            
            if sid in strong_candidates:
                # Check if it's battle-ready (Level 25)
                if pet.get('level', 0) == 25:
                    return self._format_pet_for_ui(pet)
                    
        # If no specific strong counter found, return any L25 Rare
        for pet in self.my_pets:
            if not pet.get('species'): continue
            sid = pet['species']['id']
            if sid in exclude_ids: continue
            
            if pet.get('level', 0) == 25 and pet.get('quality', {}).get('type') == 'RARE':
                 return self._format_pet_for_ui(pet)
                 
        return None

    def _get_generic_strong_pet(self, exclude_ids: List[int]) -> Dict:
        """Return a fallback strong pet (mock if not found)"""
        # Try to find one in collection
        for pet in self.my_pets:
            if not pet.get('species'): continue
            sid = pet['species']['id']
            if sid in exclude_ids: continue
            if pet.get('level', 0) == 25:
                return self._format_pet_for_ui(pet)
                
        return {'id': 0, 'name': 'Any Level 25 Pet', 'icon': 'inv_misc_questionmark'}

    def _format_pet_for_ui(self, pet_data: Dict) -> Dict:
        return {
            'id': pet_data['species']['id'],
            'name': pet_data.get('name', pet_data['species']['name']),
            'level': pet_data.get('level', 1),
            'quality': pet_data.get('quality', {}).get('type', 'COMMON'),
            'icon': pet_data.get('creature_display', {}).get('key', {}).get('href', '') 
        }

    def record_result(self, result: Dict):
        """
        Record the result of a battle to adjust future recommendations.
        result: { 'win': bool, 'turns': int, 'hp_remaining': float }
        """
        self.history.append(result)

    def calculate_bandage_efficiency(self) -> float:
        """Returns a score 0-100 representing how 'efficient' recent battles were."""
        if not self.history: return 100.0
        
        total_hp_loss = 0
        for res in self.history[-10:]: # Look at last 10
            if not res.get('win', False):
                total_hp_loss += 100 # Penalty for loss
            else:
                total_hp_loss += (100 - res.get('hp_remaining', 0))
                
        avg_loss = total_hp_loss / len(self.history[-10:])
        return max(0, 100 - avg_loss)
