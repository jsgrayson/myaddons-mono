from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

import os

app = FastAPI(title="GoblinStack AI")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.normpath(os.path.join(BASE_DIR, "../static"))

print(f"DEBUG: GoblinStack Base Dir: {BASE_DIR}")
print(f"DEBUG: GoblinStack Static Dir: {STATIC_DIR}")

# Mount static files and templates
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=BASE_DIR)

import sys
# Ensure we can import from parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from goblin_engine import GoblinEngine

# Initialize Engine
engine = GoblinEngine()
engine.load_mock_data() # Loads the "realistic" mock data from the engine

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Get fresh analysis
    analysis = engine.analyze_market()
    
    # Format opportunities for UI
    recommendations = []
    colors = ["success", "warning", "info", "primary"]
    
    for i, opp in enumerate(analysis.get('opportunities', [])[:3]): # Top 3
        recommendations.append({
            "name": f"{opp['output_item']} Opportunity",
            "desc": f"Craft for {opp['crafting_cost']}g, Sell for {opp['market_value']}g ({opp['recommendation']})",
            "roi": opp['profit_margin'],
            "color": colors[i % len(colors)]
        })
        
    # Get alerts (mock for now as engine doesn't have alerts yet)
    alerts = [
        {"type": "success", "title": "Market Update", "message": f"Identified {len(analysis.get('opportunities', []))} profitable crafts", "time": "Just now"},
        {"type": "warning", "title": "Trend Alert", "message": "Draconium Ore prices rising", "time": "10m ago"}
    ]

    return templates.TemplateResponse("goblinstack_dashboard.html", {
        "request": request,
        "recommendations": recommendations,
        "alerts": alerts
    })

@app.get("/markets", response_class=HTMLResponse)
async def markets(request: Request):
    return templates.TemplateResponse("goblinstack_markets.html", {"request": request})

@app.get("/predictions", response_class=HTMLResponse)
async def predictions(request: Request):
    return templates.TemplateResponse("goblinstack_predictions.html", {"request": request})

@app.get("/alerts", response_class=HTMLResponse)
async def alerts(request: Request):
    return templates.TemplateResponse("goblinstack_alerts.html", {"request": request})

@app.get("/settings", response_class=HTMLResponse)
async def settings(request: Request):
    return templates.TemplateResponse("goblinstack_settings.html", {"request": request})

# API Endpoints
@app.get("/api/market-data")
async def get_market_data():
    return {
        "items": [
            {"name": "Eternal Crystal", "price": 850, "change": -15.2, "volume": 1250},
            {"name": "Elethium Ore", "price": 425, "change": 8.5, "volume": 3400},
            {"name": "Shadowghast Ingot", "price": 1200, "change": -2.1, "volume": 890}
        ]
    }

@app.get("/api/predictions")
async def get_predictions():
    return {
        "predictions": [
            {"item": "Eternal Crystal", "current": 850, "predicted": 1200, "confidence": 87, "timeframe": "3 days"},
            {"item": "Heavy Callous Hide", "current": 65, "predicted": 95, "confidence": 76, "timeframe": "2 days"}
        ]
    }

@app.get("/api/alerts")
async def get_alerts():
    return {
        "alerts": [
            {"type": "success", "title": "Target Hit", "message": "Umbral Aether dropped below 500g", "time": "2m ago"},
            {"type": "warning", "title": "Spike Warning", "message": "Enchant prices rising +15%", "time": "15m ago"},
            {"type": "danger", "title": "Crash Alert", "message": "Herb market oversaturated", "time": "1h ago"}
        ]
    }

@app.get("/api/goblin/history")
async def get_history(days: int = 7):
    # Mock data for the last 7 days
    import datetime
    base_time = datetime.datetime.now()
    history = []
    for i in range(days):
        timestamp = base_time - datetime.timedelta(days=days-i-1)
        history.append({
            "timestamp": timestamp.isoformat(),
            "total_gold": 150000 + (i * 12000) + (i % 2 * 5000), # fluctuating growth
            "active_auctions": 45 + (i * 2),
            "flips_today": 5 + (i % 3)
        })
    return history

if __name__ == "__main__":
    print("🚀 Starting GoblinStack AI on http://127.0.0.1:5004")
    uvicorn.run(app, host="0.0.0.0", port=5004)
