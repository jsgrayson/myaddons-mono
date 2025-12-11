import os
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from loguru import logger

def train_model():
    data_path = os.path.join(os.path.dirname(__file__), "../data/processed/training_data.csv")
    model_dir = os.path.join(os.path.dirname(__file__), "../models")
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "price_predictor.pkl")
    
    # Load from Database
    try:
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
        from backend.database import DatabaseManager
        
        db_path = os.path.join(os.path.dirname(__file__), "../../goblin_ai.db")
        db = DatabaseManager(db_path)
        
        # Fetch all history (or limit to recent for training)
        # For training, we'd ideally want a specific query to construct features
        # For now, we'll fetch a large chunk of history
        # Note: In a real scenario, we'd need a more complex query to reconstruct the training set
        # This is a simplified integration
        conn = db._init_db() # Re-init to get connection or just use sqlite3 directly here for custom query
        import sqlite3
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM price_history ORDER BY timestamp DESC LIMIT 10000", conn)
        conn.close()
        
        logger.info(f"Loaded {len(df)} records from database.")
    except Exception as e:
        logger.error(f"Failed to load from database: {e}")
        return

    if df.empty:
        logger.error("Training data is empty.")
        return
        
    # Features and Target
    # We exclude 'timestamp' and 'source'
    features = ['price', 'quantity', 'ma_1h', 'ma_6h', 'ma_24h', 'volatility_24h', 'price_change_1h']
    target = 'target_next_price'
    
    X = df[features]
    y = df[target]
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    logger.info(f"Training Random Forest Regressor on {len(X_train)} samples...")
    model = RandomForestRegressor(n_estimators=10, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    rmse = mean_squared_error(y_test, predictions, squared=False) if hasattr(mean_squared_error, 'squared') else mean_squared_error(y_test, predictions) ** 0.5
    mae = mean_absolute_error(y_test, predictions)
    
    logger.info(f"Model Evaluation - RMSE: {rmse:.2f}, MAE: {mae:.2f}")
    
    # Save
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
        
    logger.info(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
