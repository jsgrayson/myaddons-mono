"""
Blizzard OAuth Authentication Router
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import httpx
import os
from typing import Optional
from loguru import logger

router = APIRouter()
security = HTTPBearer()

# Blizzard API credentials (from environment)
BLIZZARD_CLIENT_ID = os.getenv("BLIZZARD_CLIENT_ID")
BLIZZARD_CLIENT_SECRET = os.getenv("BLIZZARD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("BLIZZARD_REDIRECT_URI", "https://skillweaver.gg/auth/callback")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class UserInfo(BaseModel):
    battle_tag: str
    sub: str  # Blizzard account ID

@router.get("/login")
async def get_login_url():
    """
    Returns the Blizzard OAuth2 login URL.
    Frontend redirects user here to start auth flow.
    """
    auth_url = (
        f"https://oauth.battle.net/authorize"
        f"?client_id={BLIZZARD_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=wow.profile openid"
    )
    return {"login_url": auth_url}

@router.get("/callback")
async def auth_callback(code: str):
    """
    Blizzard OAuth callback handler.
    Exchanges authorization code for access token.
    """
    try:
        async with httpx.AsyncClient() as client:
            # Exchange code for token
            response = await client.post(
                "https://oauth.battle.net/token",
                auth=(BLIZZARD_CLIENT_ID, BLIZZARD_CLIENT_SECRET),
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": REDIRECT_URI
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get access token")
            
            token_data = response.json()
            
            # Get user info
            user_response = await client.get(
                "https://oauth.battle.net/userinfo",
                headers={"Authorization": f"Bearer {token_data['access_token']}"}
            )
            
            if user_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get user info")
            
            user_data = user_response.json()
            
            return {
                "access_token": token_data["access_token"],
                "battle_tag": user_data.get("battletag"),
                "account_id": user_data.get("sub")
            }
            
    except Exception as e:
        logger.error(f"OAuth error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get current user's Blizzard account info.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://oauth.battle.net/userinfo",
                headers={"Authorization": f"Bearer {credentials.credentials}"}
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid token")
            
            return response.json()
            
    except Exception as e:
        logger.error(f"User info error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
