import json
import os

class StrategyMatcher:
    def __init__(self, pets_file='my_pets.json', strategies_file='strategies.json'):
        self.pets_file = pets_file
        self.strategies_file = strategies_file
        self.my_pets = set()
        self.my_pet_names = set() # Fallback for ID mismatch
        self.load_pets()

    def load_pets(self):
        """Load user's pet collection and store species IDs and Names"""
        try:
            with open(self.pets_file, 'r') as f:
                data = json.load(f)
                for pet in data.get('pets', []):
                    species_id = pet.get('species', {}).get('id')
                    if species_id:
                        self.my_pets.add(species_id)
                    
                    # Store English name for fallback matching
                    name = pet.get('species', {}).get('name', {}).get('en_US')
                    if name:
                        self.my_pet_names.add(name)
                        
            print(f"Loaded {len(self.my_pets)} unique pet species and {len(self.my_pet_names)} names")
        except FileNotFoundError:
            print(f"Error: {self.pets_file} not found")

    def load_strategies(self):
        """Load scraped strategies"""
        try:
            with open(self.strategies_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.strategies_file} not found")
            return {}

    def match_strategies(self):
        """Filter strategies against user collection"""
        all_strategies = self.load_strategies()
        ready_strategies = {}

        for expansion, categories in all_strategies.items():
            ready_strategies[expansion] = {}
            
            for category, encounters in categories.items():
                ready_strategies[expansion][category] = []
                
                for encounter in encounters:
                    doable_strategies = []
                    
                    for strategy in encounter.get('strategies', []):
                        missing_pets = []
                        
                        # Handle both old 'pets' format and new 'pet_slots' format
                        pet_slots = strategy.get('pet_slots', [])
                        if not pet_slots and strategy.get('pets'):
                            # Fallback to old format if pet_slots doesn't exist
                            # Treat each pet as its own slot with no alternatives
                            pet_slots = [[pet] for pet in strategy.get('pets', [])]
                        
                        # For each slot, check if user has ANY of the alternatives
                        for slot in pet_slots:
                            has_any_pet_in_slot = False
                            slot_options = []
                            
                            for pet in slot:
                                # Skip empty slots or unknown pets if any
                                if not pet.get('id'):
                                    continue
                                
                                slot_options.append(pet['name'])
                                
                                # Check by ID first, then Name
                                if pet['id'] in self.my_pets or pet['name'] in self.my_pet_names:
                                    has_any_pet_in_slot = True
                                    break
                            
                            if not has_any_pet_in_slot and slot_options:
                                # User doesn't have ANY pet from this slot
                                missing_pets.append(f"Slot needs one of: {slot_options[:3]}")  # Show first 3 options
                        
                        if not missing_pets:
                            # User has at least one pet from each slot!
                            strategy['status'] = 'READY'
                            doable_strategies.append(strategy)
                        else:
                            # Optional: Store missing pets for "shopping list"
                            pass
                    
                    if doable_strategies:
                        ready_strategies[expansion][category].append({
                            'encounter_name': encounter['encounter_name'],
                            'url': encounter['url'],
                            'strategies': doable_strategies
                        })

        return ready_strategies

    def save_matches(self, matches, filename='my_ready_strategies.json'):
        with open(filename, 'w') as f:
            json.dump(matches, f, indent=2)
        print(f"Saved ready strategies to {filename}")

    def export_to_lua(self, matches, output_path='PetWeaver/PetWeaverData.lua'):
        """Export matches to Lua file for the addon"""
        print(f"Exporting to Lua: {output_path}")
        
        lua_content = ["PetWeaverDB = {"]
        
        count = 0
        for expansion, categories in matches.items():
            for category, encounters in categories.items():
                for encounter in encounters:
                    # Use the first available strategy for now
                    if not encounter['strategies']:
                        continue
                        
                    strategy = encounter['strategies'][0]
                    name = encounter['encounter_name'].replace('"', '\\"')
                    
                    # Extract pet IDs
                    pet1_id = 0
                    pet2_id = 0
                    pet3_id = 0
                    
                    # Parse pet_slots
                    pet_slots = strategy.get('pet_slots', [])
                    
                    # Helper to find a valid pet ID from a slot
                    def get_valid_id(slot):
                        for pet in slot:
                            if pet['id'] in self.my_pets:
                                return pet['id']
                        # Fallback: return first ID if we have none (shouldn't happen if filtered correctly)
                        if slot:
                            return slot[0]['id']
                        return 0

                    if len(pet_slots) >= 1: pet1_id = get_valid_id(pet_slots[0])
                    if len(pet_slots) >= 2: pet2_id = get_valid_id(pet_slots[1])
                    if len(pet_slots) >= 3: pet3_id = get_valid_id(pet_slots[2])
                    
                    # Script cleanup
                    script = strategy.get('script', '').replace('"', '\\"').replace('\n', '\\n')
                    
                    lua_entry = f'    ["{name}"] = {{\n'
                    lua_entry += f'        pet1 = {pet1_id},\n'
                    lua_entry += f'        pet2 = {pet2_id},\n'
                    lua_entry += f'        pet3 = {pet3_id},\n'
                    lua_entry += f'        script = "{script}"\n'
                    lua_entry += '    },'
                    
                    lua_content.append(lua_entry)
                    count += 1
        
        lua_content.append("}")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write('\n'.join(lua_content))
            
        print(f"✅ Exported {count} strategies to {output_path}")

def main():
    matcher = StrategyMatcher()
    
    # For testing, let's create a dummy strategies.json if it doesn't exist
    if not os.path.exists('strategies.json'):
        print("Creating dummy strategies.json for testing...")
        dummy_data = {
            "The War Within": {
                "World Quests": [
                    {
                        "encounter_name": "Rock Collector",
                        "url": "/Strategy/21512/Rock_Collector",
                        "strategies": [
                            {
                                "name": "Test Strategy (Doable)",
                                "pets": [{"name": "Unborn Val'kyr", "id": 71163}], # User likely has this
                                "script": "use(1)"
                            },
                            {
                                "name": "Test Strategy (Impossible)",
                                "pets": [{"name": "Nonexistent Pet", "id": 999999}],
                                "script": "use(1)"
                            }
                        ]
                    }
                ]
            }
        }
        with open('strategies.json', 'w') as f:
            json.dump(dummy_data, f)

    matches = matcher.match_strategies()
    matcher.save_matches(matches)
    
    # Print summary
    for exp, cats in matches.items():
        for cat, encounters in cats.items():
            print(f"{exp} - {cat}: {len(encounters)} encounters ready")

if __name__ == "__main__":
    main()
