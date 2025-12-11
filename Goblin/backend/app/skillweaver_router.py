"""
SkillWeaver Integration API - Connect character optimization with gold-making
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from loguru import logger

router = APIRouter(prefix="/api/skillweaver", tags=["SkillWeaver"])

# Data models
class CharacterOptimization(BaseModel):
    character_name: str
    realm: str
    gear_score: int
    optimization_status: str  # "optimal", "needs_upgrade", "pending"
    current_content: str  # "raid", "mythic_plus", "pvp", etc.
    
class ProfessionRecommendation(BaseModel):
    profession: str
    current_skill: int
    profit_potential: int  # gold per week
    reason: str

# Integration endpoints

@router.post("/sync-character")
async def sync_character_from_skillweaver(optimization: CharacterOptimization):
    """
    Receives character optimization data from SkillWeaver.
    Updates Goblin's character DB and returns gold-making recommendations.
    """
    try:
        # Update character in Goblin's DB
        from backend.app.character_router import char_db
        
        char = char_db.get(optimization.character_name, optimization.realm)
        if not char:
            return {"status": "error", "message": "Character not found in Goblin DB"}
        
        # Update optimization status
        char_db.update(
            optimization.character_name,
            optimization.realm,
            {
                "gear_score": optimization.gear_score,
                "optimization_status": optimization.optimization_status,
                "current_content": optimization.current_content
            }
        )
        
        # Generate gold-making recommendations based on character state
        recommendations = await _generate_gold_recommendations(char)
        
        return {
            "status": "ok",
            "character": f"{optimization.character_name}-{optimization.realm}",
            "recommendations": recommendations
        }
        
    except Exception as e:
        logger.error(f"SkillWeaver sync error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/best-professions/{character_name}/{realm}")
async def get_best_professions(character_name: str, realm: str) -> List[ProfessionRecommendation]:
    """
    Returns most profitable professions for a character.
    SkillWeaver calls this to suggest profession changes.
    """
    try:
        from backend.app.character_router import char_db
        
        char = char_db.get(character_name, realm)
        if not char:
            raise HTTPException(status_code=404, detail="Character not found")
        
        # Calculate profession profitability (mock for now - integrate with ML later)
        professions = [
            ProfessionRecommendation(
                profession="Alchemy",
                current_skill=char.get("professions", [{}])[0].get("skill_level", 0),
                profit_potential=50000,
                reason="High demand for raid consumables this season"
            ),
            ProfessionRecommendation(
                profession="Herbalism",
                current_skill=0,
                profit_potential=45000,
                reason="Pairs with Alchemy, easy to level while farming"
            )
        ]
        
        return professions
        
    except Exception as e:
        logger.error(f"Profession recommendation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/item-values")
async def get_item_values(item_ids: str):
    """
    Returns current AH prices for items.
    SkillWeaver uses this for gear value recommendations.
    """
    try:
        # Parse comma-separated item IDs
        ids = [int(x.strip()) for x in item_ids.split(",")]
        
        # Get prices from ML predictions (mock for now)
        prices = {}
        for item_id in ids:
            prices[item_id] = {
                "current_price": 10000,  # From latest AH scan
                "predicted_price": 12000,  # From ML model
                "trend": "rising"
            }
        
        return prices
        
    except Exception as e:
        logger.error(f"Item value lookup error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# SkillWeaver Data Management

class BuildCreate(BaseModel):
    character_name: str
    realm: str
    name: str
    talent_string: str
    rotation_settings: Dict[str, Any]

@router.post("/builds")
async def save_build(build: BuildCreate):
    """Save a talent build."""
    try:
        from ..database import DatabaseManager
        db = DatabaseManager()
        
        # Get character ID
        char = db.get_character(build.character_name, build.realm)
        if not char:
            raise HTTPException(status_code=404, detail="Character not found")
            
        build_id = db.save_build(
            char['id'], 
            build.name, 
            build.talent_string, 
            build.rotation_settings
        )
        return {"status": "success", "build_id": build_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/builds/{character_name}/{realm}")
async def get_builds(character_name: str, realm: str):
    """Get all builds for a character."""
    try:
        from ..database import DatabaseManager
        db = DatabaseManager()
        
        char = db.get_character(character_name, realm)
        if not char:
            raise HTTPException(status_code=404, detail="Character not found")
            
        return db.get_builds(char['id'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions

async def _generate_gold_recommendations(character: Dict) -> List[Dict]:
    """Generate gold-making recommendations based on character data."""
    recommendations = []
    
    # Check professions
    profs = character.get("professions", [])
    if len(profs) < 2:
        recommendations.append({
            "type": "profession",
            "priority": "high",
            "message": "You have empty profession slots. Consider Alchemy + Herbalism for 50k gold/week."
        })
    
    # Check gold level
    gold = character.get("gold", 0)
    if gold < 100000:
        recommendations.append({
            "type": "farming",
            "priority": "medium",
            "message": "Run Delves for 20k gold/hour and upgrade materials."
        })
    
    return recommendations
