"""
Smart Pet Battle Strategy Finder (Final Version)
Generates XuFuData.lua for the XuFuLoader addon.
"""

import json
import sys
from datetime import datetime

class StrategyFinder:
    def __init__(self, ready_file='my_ready_strategies.json', pets_file='my_pets.json'):
        self.ready_file = ready_file
        self.pets_file = pets_file
        self.my_pets = {} 
        self.my_pet_names = {} 
        
        self.load_pets()
        self.ready_encounters = self.load_ready_encounters()
        
    def load_pets(self):
        """Load user's pet collection with details"""
        try:
            with open(self.pets_file, 'r') as f:
                data = json.load(f)
                for pet in data.get('pets', []):
                    species_id = pet.get('species', {}).get('id')
                    name = pet.get('species', {}).get('name', {}).get('en_US')
                    
                    if species_id:
                        level = pet.get('level', 1)
                        quality = pet.get('quality', {}).get('type', 'COMMON')
                        quality_score = {'POOR': 1, 'COMMON': 2, 'UNCOMMON': 3, 'RARE': 4}.get(quality, 1)
                        
                        pet_info = {
                            'id': species_id,
                            'name': name,
                            'level': level,
                            'quality': quality_score
                        }
                        
                        if species_id in self.my_pets:
                            curr = self.my_pets[species_id]
                            if level > curr['level'] or (level == curr['level'] and quality_score > curr['quality']):
                                self.my_pets[species_id] = pet_info
                        else:
                            self.my_pets[species_id] = pet_info
                            
                        if name:
                            self.my_pet_names[name] = species_id
                            
            print(f"Loaded {len(self.my_pets)} unique owned pets")
        except FileNotFoundError:
            print("Warning: my_pets.json not found. Pet selection may be inaccurate.")

    def load_ready_encounters(self):
        try:
            with open(self.ready_file, 'r') as f:
                data = json.load(f)
            encounters = []
            for exp, cats in data.items():
                for cat, encs in cats.items():
                    for enc in encs:
                        encounters.append({
                            'name': enc['encounter_name'],
                            'strategies': enc['strategies']
                        })
            print(f"Loaded {len(encounters)} ready encounters")
            return encounters
        except FileNotFoundError:
            print(f"Error: {self.ready_file} not found.")
            return []

    def score_strategy(self, strategy):
        score = 100
        required_pets = 0
        for slot in strategy.get('pet_slots', []):
            if slot: required_pets += 1
        score += ((3 - required_pets) * 20)
        
        for slot in strategy.get('pet_slots', []):
            best_pet_score = 0
            for option in slot:
                pid = option.get('id')
                if pid in self.my_pets:
                    pet = self.my_pets[pid]
                    if pet['level'] == 25: best_pet_score = max(best_pet_score, 10)
                    if pet['quality'] == 4: best_pet_score += 5
            score += best_pet_score
            
        name = strategy.get('name', '').lower()
        if 'fast' in name: score += 5
        if 'safe' in name: score += 5
        if 'leveling' in name: score += 15
        if 'rng' in name: score -= 10
        return score

    def select_best_pet_id(self, slot_options):
        if not slot_options: return 0
        best_id = 0
        best_score = -1
        for pet_opt in slot_options:
            pid = pet_opt.get('id')
            found_pet = None
            if pid in self.my_pets: found_pet = self.my_pets[pid]
            elif pet_opt['name'] in self.my_pet_names:
                pid = self.my_pet_names[pet_opt['name']]
                found_pet = self.my_pets[pid]
            
            if found_pet:
                score = found_pet['level'] * 10 + found_pet['quality']
                if score > best_score:
                    best_score = score
                    best_id = pid
        
        if best_id == 0 and slot_options: return slot_options[0]['id']
        return best_id

    def generate_lua_data(self):
        """Generate Lua table for the addon"""
        output = []
        output.append("PetWeaverDB = {")
        
        for enc in self.ready_encounters:
            if enc['strategies']:
                enc['strategies'].sort(key=self.score_strategy, reverse=True)
                strat = enc['strategies'][0]
                
                pet_ids = []
                for slot in strat.get('pet_slots', []):
                    pet_ids.append(self.select_best_pet_id(slot))
                while len(pet_ids) < 3: pet_ids.append(0)
                
                # Escape script for Lua string
                script = strat.get('script', '').replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                
                output.append(f'    ["{enc["name"]}"] = {{')
                output.append(f'        pet1 = {pet_ids[0]},')
                output.append(f'        pet2 = {pet_ids[1]},')
                output.append(f'        pet3 = {pet_ids[2]},')
                output.append(f'        script = "{script}"')
                output.append('    },')
        
        output.append("}")
        return "\n".join(output)

    def export_lua(self, output_file='PetWeaver/PetWeaverData.lua'):
        lua_content = self.generate_lua_data()
        with open(output_file, 'w') as f:
            f.write(lua_content)
        print(f"✓ Exported Lua data to {output_file}")

if __name__ == "__main__":
    finder = StrategyFinder()
    finder.export_lua()
