"""
Gear Optimization Router
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from loguru import logger

router = APIRouter()

class GearPiece(BaseModel):
    item_id: int
    name: str
    slot: str
    ilvl: int
    stats: Dict[str, int]  # e.g. {"haste": 100, "crit": 50}

class OptimizationResult(BaseModel):
    current_score: float
    recommended_pieces: List[GearPiece]
    stat_weights: Dict[str, float]

@router.post("/optimize")
async def optimize_gear(spec_id: int, content_type: str, current_gear: List[GearPiece]):
    """
    Optimize gear for a spec and content type.
    Returns recommendations based on stat weights.
    """
    # TODO: Implement actual optimization logic
    # For now, return mock response
    
    stat_weights = _get_stat_weights(spec_id, content_type)
    
    return OptimizationResult(
        current_score=1234.5,
        recommended_pieces=[],
        stat_weights=stat_weights
    )

@router.get("/stat-weights/{spec_id}/{content_type}")
async def get_stat_weights(spec_id: int, content_type: str):
    """
    Get stat weights for a spec and content type.
    """
    weights = _get_stat_weights(spec_id, content_type)
    if not weights:
        raise HTTPException(status_code=404, detail="Stat weights not found")
    
    return weights

def _get_stat_weights(spec_id: int, content_type: str) -> Dict[str, float]:
    """
    Mock stat weights - in production, load from database.
    """
    # Example: Arms Warrior stat weights for raid
    WEIGHTS = {
        71: {  # Arms Warrior
            "raid": {"strength": 1.0, "haste": 0.85, "crit": 0.75, "mastery": 0.65, "vers": 0.60},
            "mythic_plus": {"strength": 1.0, "haste": 0.90, "crit": 0.70, "mastery": 0.60, "vers": 0.65}
        }
    }
    
    return WEIGHTS.get(spec_id, {}).get(content_type, {})
