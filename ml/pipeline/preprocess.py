import os
import glob
import pandas as pd
import numpy as np
from loguru import logger

def load_raw_data(data_dir: str) -> pd.DataFrame:
    """Load all raw CSV files from the data directory."""
    all_files = glob.glob(os.path.join(data_dir, "blizzard_*.csv"))
    
    if not all_files:
        logger.warning(f"No data found in {data_dir}")
        return pd.DataFrame()
        
    logger.info(f"Found {len(all_files)} raw data files.")
    df_list = []
    for filename in all_files:
        try:
            df = pd.read_csv(filename)
            df_list.append(df)
        except Exception as e:
            logger.error(f"Error reading {filename}: {e}")
            
    if not df_list:
        return pd.DataFrame()
        
    combined_df = pd.concat(df_list, ignore_index=True)
    logger.info(f"Loaded {len(combined_df)} total records.")
    return combined_df

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate technical indicators and features."""
    if df.empty:
        return df
        
    # Ensure timestamp is datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(['item_id', 'timestamp'])
    
    # Group by item to calculate features
    # We need to resample or handle irregular time intervals. 
    # For simplicity, we'll just use rolling windows on the sorted data 
    # assuming roughly hourly intervals if we run cron hourly.
    
    # However, if we have multiple auctions for the same item at the same time,
    # we should probably aggregate them first (e.g., min buyout, weighted avg).
    # Let's take the minimum buyout price per item per timestamp as the "market price".
    
    df_agg = df.groupby(['item_id', 'timestamp']).agg({
        'price': 'min', # Lowest price is the market floor
        'quantity': 'sum' # Total supply
    }).reset_index()
    
    logger.info(f"Aggregated to {len(df_agg)} item-timestamp records.")
    
    # Calculate Rolling Features
    # We will use 'transform' to keep the original shape
    
    # 1-hour (approx 1 record), 6-hour, 24-hour moving averages
    # Since data might be sparse, we use min_periods=1 to get values early
    
    df_agg['ma_1h'] = df_agg.groupby('item_id')['price'].transform(lambda x: x.rolling(window=1, min_periods=1).mean())
    df_agg['ma_6h'] = df_agg.groupby('item_id')['price'].transform(lambda x: x.rolling(window=6, min_periods=1).mean())
    df_agg['ma_24h'] = df_agg.groupby('item_id')['price'].transform(lambda x: x.rolling(window=24, min_periods=1).mean())
    
    # Volatility (Standard Deviation over 24h)
    df_agg['volatility_24h'] = df_agg.groupby('item_id')['price'].transform(lambda x: x.rolling(window=24, min_periods=2).std()).fillna(0)
    
    # Price Change (1h)
    df_agg['price_change_1h'] = df_agg.groupby('item_id')['price'].pct_change(periods=1).fillna(0)
    
    # Target Variable: Next Hour Price (Shifted -1)
    # We want to predict the price in the future.
    df_agg['target_next_price'] = df_agg.groupby('item_id')['price'].shift(-1)
    
    # Drop the last row per item since it has no target
    df_clean = df_agg.dropna(subset=['target_next_price'])
    
    return df_clean

def main():
    raw_dir = os.path.join(os.path.dirname(__file__), "../data/raw")
    processed_dir = os.path.join(os.path.dirname(__file__), "../data/processed")
    os.makedirs(processed_dir, exist_ok=True)
    
    # 1. Load
    df = load_raw_data(raw_dir)
    
    # 2. Feature Engineering
    df_features = engineer_features(df)
    
    if df_features.empty:
        logger.warning("No data available for training (need at least 2 timestamps).")
        return

    # 3. Save
    output_path = os.path.join(processed_dir, "training_data.csv")
    df_features.to_csv(output_path, index=False)
    logger.info(f"Saved processed data to {output_path} ({len(df_features)} records)")

if __name__ == "__main__":
    main()
