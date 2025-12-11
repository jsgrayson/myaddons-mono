"""
Talent Management Router - Get/recommend talent builds
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from loguru import logger

router = APIRouter()

class TalentBuild(BaseModel):
    name: str
    spec_id: int
    content_type: str  # raid, mythic_plus, pvp, delve
    hero_tree: str
    import_string: str
    pvp_talents: Optional[List[str]] = []

# Mock talent database (in production, load from DB or file)
TALENT_DATA = {
    71: {  # Arms Warrior
        "raid": TalentBuild(
            name="Slayer Raid (Single Target)",
            spec_id=71,
            content_type="raid",
            hero_tree="Slayer",
            import_string="CcEAAAAAAAAAAAAAAAAAAAAAAAgtZMjxMzMzmlllZGAAAAMYaYGsZMDMjxMzgZGGGDzwAAAAAAAgHYMLzMzAIwYZbgFwAmhJkhBb",
            pvp_talents=[]
        ),
        "mythic_plus": TalentBuild(
            name="Slayer M+ (Bladestorm)",
            spec_id=71,
            content_type="mythic_plus",
            hero_tree="Slayer",
            import_string="CcEAAAAAAAAAAAAAAAAAAAAAAAYYmZmZMjZmFLLLjZAAAAYw0wMDLDzAjlxMzgZGGz4BYGGAAAAAAAMjZZMGgtAjltBWADYGmQGgN",
            pvp_talents=[]
        ),
        "pvp": TalentBuild(
            name="Slayer PvP",
            spec_id=71,
            content_type="pvp",
            hero_tree="Slayer",
            import_string="CcEAAAAAAAAAAAAAAAAAAAAAAAgtZMjxMzMzmlllZGAAAAMYaYGsZMDMjxMzgZGGGDzwAAAAAAAgHYMLzMzAIwYZbgFwAmhJkhBb",
            pvp_talents=["Sharpen Blade", "Disarm", "Duel"]
        )
    }
}

@router.get("/spec/{spec_id}")
async def get_talent_builds(spec_id: int, content_type: Optional[str] = None):
    """
    Get all talent builds for a spec, optionally filter by content type.
    """
    if spec_id not in TALENT_DATA:
        raise HTTPException(status_code=404, detail="Spec not found")
    
    builds = TALENT_DATA[spec_id]
    
    if content_type:
        build = builds.get(content_type.lower())
        if not build:
            raise HTTPException(status_code=404, detail=f"No build for {content_type}")
        return [build]
    
    return list(builds.values())

@router.get("/recommend/{spec_id}/{content_type}")
async def recommend_build(spec_id: int, content_type: str):
    """
    Get recommended talent build for spec and content.
    """
    if spec_id not in TALENT_DATA:
        raise HTTPException(status_code=404, detail="Spec not found")
    
    build = TALENT_DATA[spec_id].get(content_type.lower())
    if not build:
        # Fallback logic: Delve -> M+ -> Raid
        if content_type.lower() == "delve":
            build = TALENT_DATA[spec_id].get("mythic_plus") or TALENT_DATA[spec_id].get("raid")
        else:
            build = TALENT_DATA[spec_id].get("raid")
    
    if not build:
        raise HTTPException(status_code=404, detail="No build available")
    
    return build
