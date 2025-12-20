import json

class BestInBagsSolver:
    def __init__(self, inventory_json, spec_weights):
        with open(inventory_json, 'r') as f:
            self.inventory = json.load(f)
        self.weights = spec_weights # e.g., {"haste": 1.2, "crit": 1.1, "vers": 1.0}
        self.locks = [] # IDs that must be equipped (Tier sets)

    def calculate_score(self, item_set):
        total_score = 0
        for item in item_set:
            item_val = 0
            for stat, value in item['stats'].items():
                item_val += value * self.weights.get(stat.lower(), 0)
            total_score += item_val * (item['ilvl'] / 100) # Weight by ilvl
        return total_score

    def find_optimal_set(self):
        # Permutation logic for each slot (Head, Neck, Shoulders, etc.)
        # Groups items by slot, then finds the highest combination
        slots = {}
        for item in self.inventory:
            slot = item['slot']
            if slot not in slots: slots[slot] = []
            slots[slot].append(item)
        
        optimized_set = {}
        for slot, items in slots.items():
            optimized_set[slot] = max(items, key=lambda x: self.calculate_score([x]))
            
        return optimized_set
