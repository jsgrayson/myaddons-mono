"""
Goblin Integration Router - Cross-system communication
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os
from loguru import logger

router = APIRouter()

GOBLIN_API_URL = os.getenv("GOBLIN_API_URL", "http://goblin-backend:8000")

class ProfessionRecommendation(BaseModel):
    profession: str
    profit_potential: int
    reason: str

@router.post("/sync-to-goblin")
async def sync_character_to_goblin(character_name: str, realm: str, gear_score: int):
    """
    Sync character optimization status to Goblin.
    Goblin responds with gold-making recommendations.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{GOBLIN_API_URL}/api/skillweaver/sync-character",
                json={
                    "character_name": character_name,
                    "realm": realm,
                    "gear_score": gear_score,
                    "optimization_status": "optimal",
                    "current_content": "raid"
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Goblin sync failed")
            
            return response.json()
            
    except Exception as e:
        logger.error(f"Goblin sync error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profession-recommendations/{character_name}/{realm}")
async def get_profession_recommendations(character_name: str, realm: str) -> List[ProfessionRecommendation]:
    """
    Get profession recommendations from Goblin AI.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{GOBLIN_API_URL}/api/skillweaver/best-professions/{character_name}/{realm}"
            )
            
            if response.status_code == 404:
                # Character not in Goblin DB yet
                return []
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to get professions")
            
            return response.json()
            
    except Exception as e:
        logger.error(f"Profession recommendation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/item-prices")
async def get_item_prices(item_ids: str):
    """
    Get AH prices from Goblin for gear value calculation.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{GOBLIN_API_URL}/api/skillweaver/item-values",
                params={"item_ids": item_ids}
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to get prices")
            
            return response.json()
            
    except Exception as e:
        logger.error(f"Item price error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
