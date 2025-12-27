import re
import json
import os

class WarbankParser:
    def __init__(self, db_path):
        self.db_path = db_path
        self.item_pattern = re.compile(r'\[(\d+)\] = \{.*?id = (\d+),.*?ilvl = (\d+),.*?slot = "(.*?)".*?\}', re.S)
        self.stat_pattern = re.compile(r'stats = \{(.*?)\}', re.S)

    def extract_inventory(self):
        if not os.path.exists(self.db_path):
            return {"error": "DATABASE_NOT_FOUND"}

        with open(self.db_path, 'r') as f:
            content = f.read()

        items = []
        for match in self.item_pattern.finditer(content):
            item_data = {
                "uid": match.group(1),
                "id": match.group(2),
                "ilvl": int(match.group(3)),
                "slot": match.group(4),
                "stats": self._parse_stats(match.group(0))
            }
            items.append(item_data)
        
        return items

    def _parse_stats(self, item_block):
        stat_match = self.stat_pattern.search(item_block)
        if not stat_match:
            return {}
        
        stats = {}
        pairs = re.findall(r'(\w+) = (\d+)', stat_match.group(1))
        for key, val in pairs:
            stats[key] = int(val)
        return stats

    def export_to_json(self, output_path):
        data = self.extract_inventory()
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"SUCCESS: {len(data)} items exported to {output_path}")

# To execute: 
# parser = WarbankParser('WTF/Account/USER/SavedVariables/PetWeaver.lua')
# parser.export_to_json('data/inventory.json')
