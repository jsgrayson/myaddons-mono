"""
Profession Leveling Guide Generator - Optimal leveling paths
"""
import os
import json
from loguru import logger
from typing import Dict, List, Any
from ml.pipeline.recipe_database import RecipeDatabase
from ml.pipeline.crafting_analyzer import CraftingAnalyzer

class LevelingGuideGenerator:
    """Generate optimized profession leveling guides."""
    
    def __init__(self):
        self.recipe_db = RecipeDatabase()
        self.crafting_analyzer = CraftingAnalyzer()
        
    def generate_guide(self, profession: str, current_skill: int, 
                       target_skill: int, character_gold: int) -> Dict[str, Any]:
        """
        Generate leveling guide for a profession.
        
        Args:
            profession: Profession name (e.g., "Blacksmithing")
            current_skill: Current skill level
            target_skill: Desired skill level
            character_gold: Available gold
        
        Returns:
            Leveling guide with steps, costs, and recommendations
        """
        logger.info(f"Generating {profession} guide: {current_skill} → {target_skill}")
        
        # Load profession recipes
        prof_id = self._get_profession_id(profession)
        recipes = self.recipe_db.load_profession_recipes(prof_id)
        
        if not recipes:
            logger.warning(f"No recipes found for {profession}")
            return self._generate_fallback_guide(profession, current_skill, target_skill)
        
        # Generate leveling path
        path = self._calculate_optimal_path(recipes, current_skill, target_skill, character_gold)
        
        return {
            "profession": profession,
            "current_skill": current_skill,
            "target_skill": target_skill,
            "path": path,
            "total_cost": sum(step['cost'] for step in path),
            "estimated_time": self._estimate_time(path),
            "summary": {
                "total_steps": len(path),
                "total_crafts": sum(step['quantity'] for step in path),
                "profit_loss": sum(step.get('profit_loss', 0) for step in path)
            }
        }
    
    def _get_profession_id(self, profession_name: str) -> int:
        """Map profession name to Blizzard API ID."""
        mapping = {
            "blacksmithing": 164,
            "leatherworking": 165,
            "alchemy": 171,
            "herbalism": 182,
            "mining": 186,
            "tailoring": 197,
            "engineering": 202,
            "enchanting": 333,
            "jewelcrafting": 755,
            "inscription": 773
        }
        return mapping.get(profession_name.lower(), 0)
    
    def _calculate_optimal_path(self, recipes: List[Dict], current: int, 
                                target: int, budget: int) -> List[Dict]:
        """Calculate optimal crafting path (cheapest or profitable)."""
        path = []
        skill = current
        
        # Sort recipes by skill requirement
        sorted_recipes = sorted(recipes, key=lambda r: r.get('rank', 1))
        
        while skill < target:
            # Find recipes in current skill range
            available = [r for r in sorted_recipes 
                        if self._get_recipe_skill(r) <= skill + 5]
            
            if not available:
                break
            
            # Pick cheapest recipe that still gives skill-ups
            best_recipe = self._find_cheapest_recipe(available, skill)
            
            if not best_recipe:
                break
            
            # Calculate how many to craft
            skill_per_craft = self._calculate_skill_gain(best_recipe, skill)
            quantity = min(10, (target - skill) // skill_per_craft + 1)
            
            # Get cost
            item_id = best_recipe.get('crafted_item', {}).get('id', 0)
            cost_per_craft = self.crafting_analyzer.calculate_material_cost(item_id)[0]
            
            path.append({
                "step": len(path) + 1,
                "recipe": best_recipe.get('name', 'Unknown'),
                "item_id": item_id,
                "quantity": quantity,
                "cost": cost_per_craft * quantity / 10000,  # Convert to gold
                "skill_gain": skill_per_craft * quantity,
                "skill_after": skill + (skill_per_craft * quantity)
            })
            
            skill += skill_per_craft * quantity
        
        return path
    
    def _find_cheapest_recipe(self, recipes: List[Dict], current_skill: int) -> Dict:
        """Find cheapest recipe that gives skill-ups."""
        # In production, would calculate actual costs from auction data
        # For now, return first available
        return recipes[0] if recipes else {}
    
    def _get_recipe_skill(self, recipe: Dict) -> int:
        """Extract skill requirement from recipe."""
        # In production, parse from recipe data
        return recipe.get('rank', 1) * 10
    
    def _calculate_skill_gain(self, recipe: Dict, current_skill: int) -> int:
        """Calculate skill points per craft."""
        # Simplified: 1 point per craft if within range
        recipe_skill = self._get_recipe_skill(recipe)
        if current_skill < recipe_skill:
            return 1
        elif current_skill < recipe_skill + 10:
            return 1
        else:
            return 0  # Grey, no skill-up
    
    def _estimate_time(self, path: List[Dict]) -> str:
        """Estimate time to complete leveling."""
        total_crafts = sum(step['quantity'] for step in path)
        # Assume 5 seconds per craft
        minutes = (total_crafts * 5) // 60
        if minutes < 60:
            return f"{minutes} minutes"
        hours = minutes // 60
        return f"{hours} hours {minutes % 60} minutes"
    
    def _generate_fallback_guide(self, profession: str, current: int, target: int) -> Dict:
        """Fallback guide when no recipe data available."""
        return {
            "profession": profession,
            "current_skill": current,
            "target_skill": target,
            "path": [],
            "total_cost": 0,
            "error": "Recipe data not available. Please load recipe database first."
        }

if __name__ == "__main__":
    generator = LevelingGuideGenerator()
    generator.crafting_analyzer.load_current_prices()
    
    guide = generator.generate_guide(
        profession="Alchemy",
        current_skill=1,
        target_skill=100,
        character_gold=10000
    )
    
    print("\n" + "="*60)
    print(f"LEVELING GUIDE: {guide['profession']}")
    print("="*60)
    print(f"Total Cost: {guide['total_cost']:.2f}g")
    print(f"Estimated Time: {guide.get('estimated_time', 'Unknown')}")
    print(f"\nSteps: {guide['summary']['total_steps']}")
