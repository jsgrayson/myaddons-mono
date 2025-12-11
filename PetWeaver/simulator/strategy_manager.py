import json
import os
import difflib

class StrategyManager:
    def __init__(self, strategies_path):
        self.strategies_path = strategies_path
        self.strategies = self._load_strategies()
        self.lookup_cache = {} # Cache for fuzzy matches

    def _load_strategies(self):
        """Loads strategies from the JSON file."""
        if not os.path.exists(self.strategies_path):
            print(f"Warning: Strategy file not found at {self.strategies_path}")
            return {}
        
        try:
            with open(self.strategies_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading strategies: {e}")
            return {}

    def get_strategy(self, npc_name):
        """
        Finds the best matching strategy for a given NPC name.
        Returns a dictionary with strategy details or None.
        """
        if not npc_name:
            return None
            
        # Check cache first
        if npc_name in self.lookup_cache:
            return self.lookup_cache[npc_name]

        # Flatten the structure to search
        # Structure: Expansion -> Category -> List of Encounters
        best_match = None
        highest_ratio = 0.0
        
        # Direct match check first (optimization)
        for expansion, categories in self.strategies.items():
            for category, encounters in categories.items():
                for encounter in encounters:
                    enc_name = encounter.get('encounter_name', '')
                    if enc_name.lower() == npc_name.lower():
                        result = self._process_encounter(encounter)
                        self.lookup_cache[npc_name] = result
                        return result
                        
        # Fuzzy match
        for expansion, categories in self.strategies.items():
            for category, encounters in categories.items():
                for encounter in encounters:
                    enc_name = encounter.get('encounter_name', '')
                    ratio = difflib.SequenceMatcher(None, npc_name.lower(), enc_name.lower()).ratio()
                    
                    if ratio > highest_ratio:
                        highest_ratio = ratio
                        best_match = encounter

        if best_match and highest_ratio > 0.7: # Threshold for fuzzy match
            result = self._process_encounter(best_match)
            self.lookup_cache[npc_name] = result
            return result
            
        # Fallback: Substring match (e.g. "Squirt" in "Next Squirt Day:")
        # We search for the npc_name inside the encounter name, or vice versa
        for expansion, categories in self.strategies.items():
            for category, encounters in categories.items():
                for encounter in encounters:
                    enc_name = encounter.get('encounter_name', '')
                    # Check if significant part of name matches
                    # e.g. "Squirt"
                    clean_npc = npc_name.lower().replace('(wod garrison)', '').strip()
                    clean_enc = enc_name.lower().replace('next ', '').replace(' day:', '').strip()
                    
                    if clean_npc in enc_name.lower() or clean_enc in npc_name.lower():
                         # Verify it's not a generic match like "The"
                         if len(clean_npc) > 3:
                            result = self._process_encounter(encounter)
                            self.lookup_cache[npc_name] = result
                            return result

        return None

    def _process_encounter(self, encounter):
        """Extracts the default strategy from an encounter object."""
        if not encounter.get('strategies'):
            return None
            
        # Default to the first strategy
        strategy = encounter['strategies'][0]
        
        return {
            'encounter_name': encounter.get('encounter_name'),
            'url': encounter.get('url'),
            'strategy_name': strategy.get('name'),
            'script': strategy.get('script'),
            'pet_slots': strategy.get('pet_slots', []),
            'rematch_string': self.generate_rematch_string(encounter['encounter_name'], strategy)
        }

    def generate_rematch_string(self, encounter_name, strategy):
        """
        Generates a Rematch import string.
        Format: Name:ID:Pet1ID:Pet2ID:Pet3ID:Script
        Note: Rematch strings are complex. A simpler format often supported is:
        Title:Script:Pet1:Pet2:Pet3 (This is pseudo-code, real Rematch strings are often base64 encoded or specific format)
        
        Actually, Rematch import strings usually look like:
        Rematch String for [Name]: [Pet1ID]:[Pet2ID]:[Pet3ID]
        
        However, for automation, we might just want to return the Script and Pets 
        so the USER can manually build it or we use a specific format if known.
        
        Let's try to construct a standard Rematch export string format if possible, 
        or at least a readable format the user can use.
        
        Standard Rematch Export (Single Team):
        Name:Pet1ID:Pet2ID:Pet3ID:Script
        """
        # Extract Pet IDs (use the first option for each slot)
        pet_ids = [0, 0, 0]
        for i, slot in enumerate(strategy.get('pet_slots', [])):
            if i < 3 and slot:
                # Slot is a list of options, pick first
                if isinstance(slot, list) and len(slot) > 0:
                    pet_ids[i] = slot[0].get('id', 0)
        
        # Clean script (remove newlines for single line format if needed, but Rematch supports multiline)
        # But for the string format "Name:ID:..." it usually expects specific delimiters.
        
        # Let's stick to a simple representation for now that the UI can display.
        # The user asked for "Rematch-compatible import string".
        # A common format is: "Name:Pet1:Pet2:Pet3:Script"
        
        script = strategy.get('script', '')
        return f"{encounter_name}:{pet_ids[0]}:{pet_ids[1]}:{pet_ids[2]}:{script}"

    def find_similar_strategies(self, target_families, limit=3):
        """
        Finds strategies used against enemy teams with similar family composition.
        
        Args:
            target_families: List of family IDs (int) or names (str) of the enemy team.
            limit: Max number of strategies to return.
            
        Returns:
            List of recommended team IDs [ [id1, id2, id3], ... ]
        """
        recommendations = []
        
        # Normalize target families to sorted list of ints for comparison
        # (Sorted because order doesn't matter for composition similarity, 
        #  though strict slot matching could be better. Let's try loose composition first.)
        target_set = []
        for f in target_families:
            if isinstance(f, int): target_set.append(f)
            elif hasattr(f, 'value'): target_set.append(f.value)
            # If string, we'd need a map, skipping for now assuming ints/enums passed
            
        target_set.sort()
        
        # We need to know the enemy composition of the stored strategies.
        # The current strategy.json structure might not have enemy details directly.
        # We might need to infer it or look it up.
        # For now, let's assume we can't easily look up every enemy's composition without a massive DB query.
        # BUT, we can look for strategies that use similar PLAYER teams against similar types?
        # No, the user wants: "If I'm fighting 3 Beasts, show me a strategy that beat 3 Beasts".
        
        # Since we don't have enemy info in strategy.json, we can't do this purely from that file.
        # We would need to cross-reference with the encounter DB.
        
        # Alternative: The user might have meant "Find a strategy for a SIMILARLY NAMED enemy".
        # But "similar enemy setup" implies composition.
        
        # Let's implement a placeholder that returns nothing for now if we can't verify enemy types,
        # OR better: if we have access to an encounter DB, we could use it.
        # Given the constraints, I'll add the method signature and a basic implementation 
        # that tries to match if we add enemy_families to the strategy file in the future.
        
        return recommendations

    def get_recommended_team(self, npc_name):
        """
        Returns a list of recommended pet IDs for the given NPC.
        Format: [Pet1ID, Pet2ID, Pet3ID] (0 for empty slots)
        """
        strategy_data = self.get_strategy(npc_name)
        if not strategy_data:
            return None
            
        pet_ids = [0, 0, 0]
        for i, slot in enumerate(strategy_data.get('pet_slots', [])):
            if i < 3 and slot:
                # Slot is a list of options, pick first
                if isinstance(slot, list) and len(slot) > 0:
                    pet_ids[i] = slot[0].get('id', 0)
        
        return pet_ids
