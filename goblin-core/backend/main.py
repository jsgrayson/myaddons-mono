from fastapi import FastAPI, HTTPException
import psycopg2
import os

app = FastAPI(title="Goblin Financial Engine", version="1.0.0")
DB_DSN = os.getenv("DATABASE_URL", "postgresql://goblin:goldcap@localhost:5432/goblin_ledger")

@app.get("/valuation/{item_id}")
def get_item_valuation(item_id: int):
    """
    Returns the Real-Time 'Goblin Value' of an item.
    """
    conn = psycopg2.connect(DB_DSN)
    cur = conn.cursor()
    
    # Get Market Value
    cur.execute("SELECT market_value, source FROM item_pricing WHERE item_id = %s", (item_id,))
    row = cur.fetchone()
    
    if not row:
        return {"status": "NO_DATA", "value": 0}
        
    market_value = row[0]
    
    # GOBLIN LOGIC:
    # 5% AH Cut + 10% Risk Margin = 15% reduction
    liquid_value = int(market_value * 0.85)
    
    return {
        "item_id": item_id,
        "market_value": market_value,
        "liquid_value": liquid_value,
        "recommendation": "SELL" if liquid_value > 10000 else "DISENCHANT"
    }
