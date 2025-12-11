"""
Character Management API - Track player characters and professions
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os
from loguru import logger

router = APIRouter(prefix="/api/characters", tags=["Characters"])

# Data models
class Profession(BaseModel):
    name: str
    skill_level: int
    max_skill: int = 100
    specialization: Optional[str] = None

class Character(BaseModel):
    name: str
    realm: str
    faction: str
    level: int
    gold: int
    professions: List[Profession]

# Database integration
from ..database import DatabaseManager

# Endpoints
@router.post("/", response_model=Character)
async def create_character(character: Character):
    """Add a new character."""
    try:
        db = DatabaseManager()
        # Convert Pydantic model to dict
        char_data = character.dict()
        result = db.add_character(char_data)
        logger.info(f"Created character: {character.name}-{character.realm}")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Character])
async def list_characters():
    """List all characters."""
    try:
        db = DatabaseManager()
        chars = db.get_all_characters()
        return chars
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{name}/{realm}", response_model=Character)
async def get_character(name: str, realm: str):
    """Get specific character."""
    db = DatabaseManager()
    char = db.get_character(name, realm)
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")
    return char

@router.put("/{name}/{realm}", response_model=Character)
async def update_character(name: str, realm: str, updates: Dict[str, Any]):
    """Update character details."""
    try:
        db = DatabaseManager()
        char = db.get_character(name, realm)
        if not char:
            raise HTTPException(status_code=404, detail="Character not found")
        
        # Update fields
        char.update(updates)
        result = db.add_character(char) # add_character handles update via REPLACE
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{name}/{realm}/crafting-guide")
async def get_crafting_guide(name: str, realm: str, profession: str, target_skill: int = 100):
    """Generate profession leveling guide for character."""
    from ml.pipeline.leveling_guide import LevelingGuideGenerator
    
    db = DatabaseManager()
    char = db.get_character(name, realm)
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")
    
    # Find profession
    prof = next((p for p in char['professions'] if p['name'].lower() == profession.lower()), None)
    if not prof:
        raise HTTPException(status_code=404, detail=f"Character doesn't have {profession}")
    
    # Generate guide
    generator = LevelingGuideGenerator()
    guide = generator.generate_guide(
        profession=profession,
        current_skill=prof['skill_level'],
        target_skill=target_skill,
        character_gold=char['gold']
    )
    
    return guide
