"""
goblin_training.py - ML Model Training on Historical Data

Trains the prediction model by correlating:
- Historical news events (buffs, nerfs, patches)
- Historical AH price data (actual price movements)

Example Training Data:
  Event: "Fire Mage buffed" (Patch 11.0.2, Aug 15)
  Result: Fire enchants +280%, Fire gems +190% within 48 hours
  
  Event: "Mythic raid release" (Weekly reset, Tuesday)
  Result: Flasks +150%, Potions +120%, Food +95%

Process:
1. Load historical news from database
2. Load historical AH scans from database
3. Correlate events with price movements (time-window matching)
4. Train classification model: Event Type → Price Impact
5. Save trained model for predictions
"""

import json
import pickle
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from collections import defaultdict
import psycopg2
import os

# ============================================================================
# Historical Data Loader
# ============================================================================

class HistoricalDataLoader:
    def __init__(self, db_connection):
        self.conn = db_connection
    
    def load_news_events(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """
        Load historical news events from database
        
        Schema: auctionhouse.news_events
        - event_id SERIAL
        - timestamp TIMESTAMP
        - source TEXT (wowhead, mmochampion, blizzard)
        - title TEXT
        - event_type TEXT (class_change, raid, patch, holiday)
        - affected_classes TEXT[]
        - affected_items INT[]
        """
        cur = self.conn.cursor()
        
        cur.execute("""
            SELECT event_id, timestamp, source, title, event_type, 
                   affected_classes, affected_items
            FROM auctionhouse.news_events
            WHERE timestamp BETWEEN %s AND %s
            ORDER BY timestamp
        """, (start_date, end_date))
        
        events = []
        for row in cur.fetchall():
            events.append({
                "event_id": row[0],
                "timestamp": row[1],
                "source": row[2],
                "title": row[3],
                "event_type": row[4],
                "affected_classes": row[5],
                "affected_items": row[6],
            })
        
        cur.close()
        return events
    
    def load_price_history(self, item_id: int, start_date: datetime, 
                          end_date: datetime) -> List[Dict]:
        """
        Load historical price data for an item
        
        Schema: auctionhouse.scan_items
        - scan_id INT
        - item_id INT
        - price INT (copper)
        - quantity INT
        - timestamp TIMESTAMP (from scans table)
        """
        cur = self.conn.cursor()
        
        cur.execute("""
            SELECT s.timestamp, si.price, si.quantity
            FROM auctionhouse.scan_items si
            JOIN auctionhouse.scans s ON si.scan_id = s.scan_id
            WHERE si.item_id = %s
              AND s.timestamp BETWEEN %s AND %s
            ORDER BY s.timestamp
        """, (item_id, start_date, end_date))
        
        history = []
        for row in cur.fetchall():
            history.append({
                "timestamp": row[0],
                "price": row[1],
                "quantity": row[2],
            })
        
        cur.close()
        return history

# ============================================================================
# Event-Price Correlation Engine
# ============================================================================

class EventPriceCorrelator:
    def __init__(self, historical_loader: HistoricalDataLoader):
        self.loader = historical_loader
    
    def correlate_event_to_prices(self, event: Dict, window_hours: int = 72) -> Dict:
        """
        Correlate a news event to actual price movements
        
        Args:
            event: News event dict
            window_hours: Time window after event to measure impact
        
        Returns:
            {
                "event_id": ...,
                "item_impacts": [
                    {"item_id": ..., "price_change_pct": 280, "peak_time_hours": 48},
                    ...
                ]
            }
        """
        event_time = event['timestamp']
        window_end = event_time + timedelta(hours=window_hours)
        
        item_impacts = []
        
        for item_id in event.get('affected_items', []):
            # Get price history before and after event
            before_start = event_time - timedelta(days=7)
            
            history = self.loader.load_price_history(item_id, before_start, window_end)
            
            if len(history) < 10:
                continue  # Not enough data
            
            # Calculate baseline (7 days before event)
            baseline_prices = [h['price'] for h in history 
                             if h['timestamp'] < event_time]
            
            if not baseline_prices:
                continue
            
            baseline_avg = np.mean(baseline_prices)
            
            # Find peak after event
            after_prices = [h for h in history if h['timestamp'] >= event_time]
            
            if not after_prices:
                continue
            
            peak_price = max(p['price'] for p in after_prices)
            peak_time = next(p['timestamp'] for p in after_prices 
                           if p['price'] == peak_price)
            
            # Calculate impact
            price_change_pct = ((peak_price - baseline_avg) / baseline_avg) * 100
            peak_time_hours = (peak_time - event_time).total_seconds() / 3600
            
            item_impacts.append({
                "item_id": item_id,
                "baseline_price": int(baseline_avg),
                "peak_price": peak_price,
                "price_change_pct": round(price_change_pct, 1),
                "peak_time_hours": round(peak_time_hours, 1),
            })
        
        return {
            "event_id": event['event_id'],
            "event_type": event['event_type'],
            "event_time": event_time.isoformat(),
            "item_impacts": item_impacts,
        }
    
    def build_training_dataset(self, start_date: datetime, 
                               end_date: datetime) -> List[Dict]:
        """
        Build complete training dataset from historical data
        
        Returns:
            List of correlated event-price pairs
        """
        print(f"Loading news events from {start_date} to {end_date}...")
        events = self.loader.load_news_events(start_date, end_date)
        
        print(f"Found {len(events)} historical events")
        
        training_data = []
        
        for i, event in enumerate(events):
            print(f"Correlating event {i+1}/{len(events)}: {event['title'][:50]}...")
            
            correlation = self.correlate_event_to_prices(event)
            
            if correlation['item_impacts']:
                training_data.append(correlation)
        
        print(f"\nBuilt training dataset: {len(training_data)} correlated events")
        
        return training_data

# ============================================================================
# ML Model Trainer
# ============================================================================

class MarketPredictionModel:
    def __init__(self):
        self.event_type_weights = {}
        self.trained = False
    
    def train(self, training_data: List[Dict]):
        """
        Train the model on historical correlations
        
        Learns:
        - Average price impact per event type
        - Time-to-peak per event type
        - Confidence scores based on consistency
        """
        print("Training market prediction model...")
        
        # Group by event type
        by_event_type = defaultdict(list)
        
        for event in training_data:
            event_type = event['event_type']
            
            for impact in event['item_impacts']:
                by_event_type[event_type].append({
                    "price_change": impact['price_change_pct'],
                    "peak_time": impact['peak_time_hours'],
                })
        
        # Calculate statistics per event type
        for event_type, impacts in by_event_type.items():
            price_changes = [i['price_change'] for i in impacts]
            peak_times = [i['peak_time'] for i in impacts]
            
            self.event_type_weights[event_type] = {
                "avg_price_change": np.mean(price_changes),
                "std_price_change": np.std(price_changes),
                "avg_peak_time": np.mean(peak_times),
                "confidence": min(len(impacts) / 20, 1.0),  # More data = higher confidence
                "sample_count": len(impacts),
            }
        
        self.trained = True
        
        print("\nTraining complete!")
        print("\nLearned Patterns:")
        for event_type, weights in self.event_type_weights.items():
            print(f"\n{event_type}:")
            print(f"  Avg Price Impact: {weights['avg_price_change']:.1f}%")
            print(f"  Peak Time: {weights['avg_peak_time']:.1f} hours")
            print(f"  Confidence: {weights['confidence']:.2f}")
            print(f"  Samples: {weights['sample_count']}")
    
    def predict(self, event_type: str, item_ids: List[int]) -> List[Dict]:
        """
        Predict price impact for a new event
        
        Returns:
            Predictions with expected price change and timeframe
        """
        if not self.trained:
            raise Exception("Model not trained yet!")
        
        weights = self.event_type_weights.get(event_type)
        
        if not weights:
            return []
        
        predictions = []
        
        for item_id in item_ids:
            predictions.append({
                "item_id": item_id,
                "predicted_change_pct": round(weights['avg_price_change'], 1),
                "expected_peak_hours": round(weights['avg_peak_time'], 1),
                "confidence": weights['confidence'],
                "action": "BUY NOW" if weights['avg_price_change'] > 20 else "MONITOR",
            })
        
        return predictions
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        with open(filepath, 'wb') as f:
            pickle.dump({
                "weights": self.event_type_weights,
                "trained": self.trained,
            }, f)
        
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load trained model from disk"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        self.event_type_weights = data['weights']
        self.trained = data['trained']
        
        print(f"Model loaded from {filepath}")

# ============================================================================
# Training Script
# ============================================================================

def get_mock_training_data():
    """Generate mock training data for dev environment"""
    print("Generating mock training data...")
    return [
        {
            "event_id": 1,
            "event_type": "class_change",
            "item_impacts": [
                {"price_change_pct": 250.0, "peak_time_hours": 48.0},
                {"price_change_pct": 180.0, "peak_time_hours": 36.0}
            ]
        },
        {
            "event_id": 2,
            "event_type": "raid",
            "item_impacts": [
                {"price_change_pct": 150.0, "peak_time_hours": 12.0},
                {"price_change_pct": 120.0, "peak_time_hours": 24.0}
            ]
        },
        {
            "event_id": 3,
            "event_type": "patch",
            "item_impacts": [
                {"price_change_pct": 300.0, "peak_time_hours": 72.0},
                {"price_change_pct": 200.0, "peak_time_hours": 48.0}
            ]
        },
        {
            "event_id": 4,
            "event_type": "holiday",
            "item_impacts": [
                {"price_change_pct": 50.0, "peak_time_hours": 6.0},
                {"price_change_pct": 40.0, "peak_time_hours": 12.0}
            ]
        },
        {
            "event_id": 5,
            "event_type": "profession",
            "item_impacts": [
                {"price_change_pct": 400.0, "peak_time_hours": 24.0},
                {"price_change_pct": 350.0, "peak_time_hours": 12.0}
            ]
        }
    ]

def train_model():
    """
    Main training script
    
    Usage:
        python goblin_training.py
    """
    training_data = []
    
    try:
        # Connect to database
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            raise Exception("DATABASE_URL not set")
            
        conn = psycopg2.connect(db_url)
        
        # Load historical data
        loader = HistoricalDataLoader(conn)
        correlator = EventPriceCorrelator(loader)
        
        # Build training dataset (last 6 months)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        
        training_data = correlator.build_training_dataset(start_date, end_date)
        conn.close()
        
    except Exception as e:
        print(f"⚠️ Database connection failed: {e}")
        print("Falling back to MOCK training data for development...")
        training_data = get_mock_training_data()
    
    # Save training data
    with open('training_data.json', 'w') as f:
        json.dump(training_data, f, indent=2, default=str)
    
    print(f"Saved training data to training_data.json")
    
    # Train model
    model = MarketPredictionModel()
    model.train(training_data)
    
    # Save model
    model.save_model('market_prediction_model.pkl')
    
    print("\nTraining complete! Model ready for predictions.")

if __name__ == "__main__":
    train_model()
