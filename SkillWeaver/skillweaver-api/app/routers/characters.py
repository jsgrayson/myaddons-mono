"""
Character Management Router
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os
from loguru import logger

router = APIRouter()

BLIZZARD_REGION = "us"
BLIZZARD_LOCALE = "en_US"

class Character(BaseModel):
    name: str
    realm: str
    faction: str
    level: int
    class_name: str
    spec_name: str
    item_level: int
    gold: Optional[int] = 0

@router.post("/import")
async def import_character(name: str, realm: str, access_token: str):
    """
    Import a character from Blizzard API.
    """
    try:
        async with httpx.AsyncClient() as client:
            # Get character profile
            url = f"https://{BLIZZARD_REGION}.api.blizzard.com/profile/wow/character/{realm.lower()}/{name.lower()}"
            params = {
                "namespace": f"profile-{BLIZZARD_REGION}",
                "locale": BLIZZARD_LOCALE
            }
            headers = {"Authorization": f"Bearer {access_token}"}
            
            response = await client.get(url, params=params, headers=headers)
            
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="Character not found")
            
            data = response.json()
            
            # Get equipment summary for ilvl
            equip_url = f"{url}/equipment"
            equip_response = await client.get(equip_url, params=params, headers=headers)
            equip_data = equip_response.json() if equip_response.status_code == 200 else {}
            
            character = Character(
                name=data["name"],
                realm=data["realm"]["name"],
                faction=data["faction"]["name"],
                level=data["level"],
                class_name=data["character_class"]["name"],
                spec_name=data.get("active_spec", {}).get("name", "Unknown"),
                item_level=equip_data.get("equipped_item_level", 0)
            )
            
            return character
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Character import error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{name}/{realm}")
async def get_character(name: str, realm: str):
    """
    Get stored character data (from local DB in future).
    For now, mock response.
    """
    # TODO: Integrate with PostgreSQL database
    return {
        "name": name,
        "realm": realm,
        "message": "Character data storage coming soon"
    }

@router.get("/")
async def list_characters():
    """
    List all characters for current user.
    """
    # TODO: Integrate with PostgreSQL database
    return []
