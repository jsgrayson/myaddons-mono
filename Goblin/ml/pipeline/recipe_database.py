"""
Recipe Database Loader - Fetch and cache WoW profession recipes from Blizzard API
"""
import os
import json
import requests
from loguru import logger
from typing import Dict, List, Any
from ml.pipeline.blizzard_api import BlizzardAPI

class RecipeDatabase:
    """Load and manage profession recipes."""
    
    def __init__(self):
        self.api = BlizzardAPI()
        self.cache_dir = os.path.join(os.path.dirname(__file__), "../data/recipes")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.recipes = {}
        
    def load_profession_recipes(self, profession_id: int) -> List[Dict]:
        """Load recipes for a specific profession."""
        cache_file = os.path.join(self.cache_dir, f"profession_{profession_id}.json")
        
        # Check cache first
        if os.path.exists(cache_file):
            logger.info(f"Loading cached recipes for profession {profession_id}")
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        # Fetch from API
        logger.info(f"Fetching recipes for profession {profession_id} from Blizzard API...")
        token = self.api._get_access_token()
        
        if not token:
            logger.error("Failed to get access token")
            return []
        
        url = f"https://{self.api.region}.api.blizzard.com/data/wow/profession/{profession_id}"
        params = {
            "namespace": f"static-{self.api.region}",
            "locale": self.api.locale
        }
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Extract recipes from skill tiers
                all_recipes = []
                for tier in data.get('skill_tiers', []):
                    tier_id = tier['id']
                    tier_recipes = self._load_tier_recipes(tier_id, token)
                    all_recipes.extend(tier_recipes)
                
                # Cache the results
                with open(cache_file, 'w') as f:
                    json.dump(all_recipes, f, indent=2)
                
                logger.success(f"Loaded {len(all_recipes)} recipes for profession {profession_id}")
                return all_recipes
            else:
                logger.error(f"Failed to load profession: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error loading recipes: {e}")
            return []
    
    def _load_tier_recipes(self, tier_id: int, token: str) -> List[Dict]:
        """Load recipes from a specific skill tier."""
        url = f"https://{self.api.region}.api.blizzard.com/data/wow/profession-skill-tier/{tier_id}"
        params = {
            "namespace": f"static-{self.api.region}",
            "locale": self.api.locale
        }
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                tier_data = response.json()
                recipes = []
                
                for category in tier_data.get('categories', []):
                    for recipe_ref in category.get('recipes', []):
                        recipe_id = recipe_ref.get('id')
                        recipe_detail = self._load_recipe_detail(recipe_id, token)
                        if recipe_detail:
                            recipes.append(recipe_detail)
                
                return recipes
            return []
        except Exception as e:
            logger.warning(f"Error loading tier {tier_id}: {e}")
            return []
    
    def _load_recipe_detail(self, recipe_id: int, token: str) -> Dict:
        """Load detailed recipe information."""
        url = f"https://{self.api.region}.api.blizzard.com/data/wow/recipe/{recipe_id}"
        params = {
            "namespace": f"static-{self.api.region}",
            "locale": self.api.locale
        }
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            logger.warning(f"Error loading recipe {recipe_id}: {e}")
            return {}
    
    def build_recipe_tree(self, recipe: Dict) -> Dict[str, Any]:
        """Build dependency tree for a recipe (recursive)."""
        crafted_item = recipe.get('crafted_item', {})
        item_id = crafted_item.get('id')
        item_name = crafted_item.get('name', f'Item {item_id}')
        
        reagents = recipe.get('reagents', [])
        dependencies = []
        
        for reagent in reagents:
            reagent_item_id = reagent.get('reagent', {}).get('id')
            quantity = reagent.get('quantity', 1)
            
            # Check if this reagent can also be crafted
            sub_recipe = self._find_recipe_for_item(reagent_item_id)
            if sub_recipe:
                # Recursive sub-craft
                sub_tree = self.build_recipe_tree(sub_recipe)
                dependencies.append({
                    "item_id": reagent_item_id,
                    "quantity": quantity,
                    "craftable": True,
                    "sub_recipe": sub_tree
                })
            else:
                # Raw material (buy or farm)
                dependencies.append({
                    "item_id": reagent_item_id,
                    "quantity": quantity,
                    "craftable": False
                })
        
        return {
            "item_id": item_id,
            "item_name": item_name,
            "recipe_id": recipe.get('id'),
            "dependencies": dependencies
        }
    
    def _find_recipe_for_item(self, item_id: int) -> Dict:
        """Find if an item can be crafted (check all loaded recipes)."""
        for profession_recipes in self.recipes.values():
            for recipe in profession_recipes:
                crafted_item = recipe.get('crafted_item', {})
                if crafted_item.get('id') == item_id:
                    return recipe
        return {}
    
    def load_all_professions(self):
        """Load recipes for all major professions."""
        # Blizzard Profession IDs (retail)
        professions = {
            164: "Blacksmithing",
            165: "Leatherworking",
            171: "Alchemy",
            182: "Herbalism",
            186: "Mining",
            197: "Tailoring",
            202: "Engineering",
            333: "Enchanting",
            755: "Jewelcrafting",
            773: "Inscription"
        }
        
        logger.info("Loading all profession recipes...")
        for prof_id, prof_name in professions.items():
            logger.info(f"Loading {prof_name}...")
            recipes = self.load_profession_recipes(prof_id)
            self.recipes[prof_name] = recipes
        
        logger.success(f"Loaded recipes for {len(professions)} professions")

if __name__ == "__main__":
    db = RecipeDatabase()
    
    # Load just one profession for testing (Alchemy)
    recipes = db.load_profession_recipes(171)
    
    if recipes:
        print(f"\nLoaded {len(recipes)} Alchemy recipes")
        print(f"Example: {recipes[0].get('name', 'Unknown')}")
