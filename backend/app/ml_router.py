"""
ML API Router for FastAPI backend.
Exposes ML predictions and control endpoints.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os
import subprocess
import sys
from datetime import datetime
from loguru import logger

router = APIRouter(prefix="/api/ml", tags=["ML"])

# Data models
class Opportunity(BaseModel):
    item_id: int
    price: float
    predicted_price: float
    discount_pct: float
    quantity: int

class OpportunitiesResponse(BaseModel):
    timestamp: str
    count: int
    opportunities: List[Opportunity]

class TaskResponse(BaseModel):
    status: str
    message: str
    started_at: Optional[str] = None

class ModelStatus(BaseModel):
    exists: bool
    path: Optional[str] = None
    size_mb: Optional[float] = None
    last_modified: Optional[str] = None

# Endpoints
@router.get("/opportunities", response_model=OpportunitiesResponse)
async def get_opportunities():
    """Get latest flip opportunities from SQL database."""
    try:
        from ..database import DatabaseManager
        db = DatabaseManager()
        predictions = db.get_latest_predictions()
        
        opportunities = []
        for p in predictions:
            # Convert DB record to Opportunity model
            opportunities.append(Opportunity(
                item_id=p['item_id'],
                price=p['predicted_price'], # Using predicted as current for now
                predicted_price=p['predicted_price'],
                discount_pct=0.0, # Calculate if needed
                quantity=1 # Placeholder
            ))
        
        return OpportunitiesResponse(
            timestamp=datetime.now().isoformat(),
            count=len(opportunities),
            opportunities=opportunities
        )
    except Exception as e:
        logger.error(f"Error loading opportunities: {e}")
        # Return empty if DB fails
        return OpportunitiesResponse(timestamp="", count=0, opportunities=[])

@router.post("/ingest", response_model=TaskResponse)
async def trigger_ingestion():
    """Manually trigger data ingestion."""
    try:
        logger.info("API: Triggering data ingestion...")
        result = subprocess.Popen(
            [sys.executable, "-m", "ml.pipeline.ingest"],
            cwd="/app",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        return TaskResponse(
            status="started",
            message="Data ingestion started in background",
            started_at=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict", response_model=TaskResponse)
async def trigger_predictions():
    """Manually trigger predictions."""
    try:
        logger.info("API: Triggering predictions...")
        result = subprocess.Popen(
            [sys.executable, "-m", "ml.pipeline.predict"],
            cwd="/app",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        return TaskResponse(
            status="started",
            message="Predictions started in background",
            started_at=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/retrain", response_model=TaskResponse)
async def trigger_retraining():
    """Manually trigger model retraining."""
    try:
        logger.info("API: Triggering model retraining...")
        # Start async process
        subprocess.Popen(
            [sys.executable, "-m", "ml.pipeline.train"],
            cwd="/app",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        return TaskResponse(
            status="started",
            message="Model retraining started in background (may take 5-10 minutes)",
            started_at=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model/status", response_model=ModelStatus)
async def get_model_status():
    """Get current model information."""
    model_path = "/app/ml/models/price_predictor.pkl"
    
    if not os.path.exists(model_path):
        return ModelStatus(exists=False)
    
    try:
        stat = os.stat(model_path)
        size_mb = stat.st_size / (1024 * 1024)
        modified = datetime.fromtimestamp(stat.st_mtime).isoformat()
        
        return ModelStatus(
            exists=True,
            path=model_path,
            size_mb=round(size_mb, 2),
            last_modified=modified
        )
    except Exception as e:
        logger.error(f"Error getting model status: {e}")
        return ModelStatus(exists=False)

@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "ml-pipeline"
    }
