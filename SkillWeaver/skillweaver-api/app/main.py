"""
SkillWeaver API - Main Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

# Configure logging
logger.remove()
logger.add(sys.stdout, level="INFO")

# Import routers
from app.routers import auth, characters, talents, gear, integration

# Create FastAPI app
app = FastAPI(
    title="SkillWeaver API",
    description="Character optimization and talent planning for World of Warcraft",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lock down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(characters.router, prefix="/api/characters", tags=["Characters"])
app.include_router(talents.router, prefix="/api/talents", tags=["Talents"])
app.include_router(gear.router, prefix="/api/gear", tags=["Gear"])
app.include_router(integration.router, prefix="/api/integration", tags=["Goblin Integration"])

@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "SkillWeaver API",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
