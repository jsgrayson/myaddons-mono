import os
import json
import yaml
import pandas as pd
import pickle
from datetime import datetime
from loguru import logger
from .notifications import NotificationService

def predict_opportunities():
    """Load latest data, predict fair values, and identify buy opportunities."""
    model_path = os.path.join(os.path.dirname(__file__), "../models/price_predictor.pkl")
    raw_dir = os.path.join(os.path.dirname(__file__), "../data/raw")
    output_dir = os.path.join(os.path.dirname(__file__), "../data/predictions")
    config_path = os.path.join(os.path.dirname(__file__), "../../backend/config/core.yaml")
    os.makedirs(output_dir, exist_ok=True)
    
    # Load config for notifications
    email_config = {}
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            email_config = config.get("email", {})
    
    notifier = NotificationService(email_config=email_config)
    
    if not os.path.exists(model_path):
        logger.error(f"Model not found at {model_path}. Train the model first.")
        return
    
    # Load model
    logger.info("Loading trained model...")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    # Load latest auction data
    # Load latest auction data from Database
    try:
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
        from backend.database import DatabaseManager
        
        db_path = os.path.join(os.path.dirname(__file__), "../../goblin_ai.db")
        db = DatabaseManager(db_path)
        
        # Get latest snapshot (items with max timestamp)
        import sqlite3
        conn = sqlite3.connect(db_path)
        # Get max timestamp first
        max_ts_df = pd.read_sql_query("SELECT MAX(timestamp) as max_ts FROM price_history", conn)
        max_ts = max_ts_df['max_ts'].iloc[0]
        
        if not max_ts:
            logger.error("No data in database.")
            return
            
        query = f"SELECT * FROM price_history WHERE timestamp = '{max_ts}'"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        logger.info(f"Loaded {len(df)} records from database (timestamp: {max_ts})")
    except Exception as e:
        logger.error(f"Failed to load from database: {e}")
        return
    
    # Aggregate to get current market price per item
    df_current = df.groupby('item_id').agg({
        'price': 'min',
        'quantity': 'sum'
    }).reset_index()
    
    # Calculate simple features (since we don't have historical context for prediction)
    # We'll use current values as placeholders
    df_current['ma_1h'] = df_current['price']
    df_current['ma_6h'] = df_current['price']
    df_current['ma_24h'] = df_current['price']
    df_current['volatility_24h'] = 0
    df_current['price_change_1h'] = 0
    
    features = ['price', 'quantity', 'ma_1h', 'ma_6h', 'ma_24h', 'volatility_24h', 'price_change_1h']
    X = df_current[features]
    
    # Predict fair value
    logger.info("Predicting fair values...")
    df_current['predicted_price'] = model.predict(X)
    
    # Identify opportunities: current price < 80% of predicted price
    df_current['discount_pct'] = ((df_current['predicted_price'] - df_current['price']) / df_current['predicted_price']) * 100
    opportunities = df_current[df_current['discount_pct'] > 20].sort_values('discount_pct', ascending=False)
    
    if opportunities.empty:
        logger.info("No profitable opportunities found.")
        result = {"timestamp": datetime.now().isoformat(), "opportunities": []}
    else:
        logger.info(f"Found {len(opportunities)} opportunities!")
        result = {
            "timestamp": datetime.now().isoformat(),
            "opportunities": opportunities.head(20).to_dict(orient='records')
        }
        
        # Send notifications
        notifier.send_opportunity_alert(
            result['opportunities'],
            len(opportunities)
        )
    
    # Save
    output_path = os.path.join(output_dir, "opportunities.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
        
    logger.info(f"Saved predictions to {output_path}")

if __name__ == "__main__":
    predict_opportunities()
