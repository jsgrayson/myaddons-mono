"""
Ensemble ML Predictor - Combines multiple models for maximum accuracy
"""
import os
import json
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
from loguru import logger
from typing import Dict, List, Tuple

# ML models
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
import xgboost as xgb

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    logger.warning("Prophet not available - install with: pip install prophet")

try:
    from tensorflow import keras
    from tensorflow.keras import layers
    KERAS_AVAILABLE = True
except ImportError:
    KERAS_AVAILABLE = False
    logger.warning("TensorFlow not available - install for LSTM support")


class EnsemblePredictor:
    """Advanced ensemble predictor with 95%+ accuracy target."""
    
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.feature_names = []
        self.model_weights = {
            'random_forest': 0.2,
            'xgboost': 0.3,
            'gradient_boosting': 0.2,
            'lstm': 0.2,
            'prophet': 0.1
        }
        
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer advanced features for maximum prediction power."""
        logger.info("Engineering advanced features...")
        
        # Ensure timestamp
        if 'timestamp' not in df.columns and 'date' in df.columns:
            df['timestamp'] = pd.to_datetime(df['date'])
        
        # Time-based features
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['day_of_month'] = df['timestamp'].dt.day
        df['week_of_year'] = df['timestamp'].dt.isocalendar().week
        df['month'] = df['timestamp'].dt.month
        
        # Cyclical encoding (hours, days)
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        
        # Rolling statistics (per item)
        for window in [7, 14, 30]:
            df[f'price_ma_{window}'] = df.groupby('item_id')['price'].transform(
                lambda x: x.rolling(window, min_periods=1).mean()
            )
            df[f'price_std_{window}'] = df.groupby('item_id')['price'].transform(
                lambda x: x.rolling(window, min_periods=1).std()
            )
            df[f'quantity_ma_{window}'] = df.groupby('item_id')['quantity'].transform(
                lambda x: x.rolling(window, min_periods=1).mean()
            )
        
        # Price momentum
        df['price_change_1d'] = df.groupby('item_id')['price'].pct_change(1)
        df['price_change_7d'] = df.groupby('item_id')['price'].pct_change(7)
        
        # Volatility
        df['volatility'] = df['price_std_7'] / (df['price_ma_7'] + 1)
        
        # Supply/demand proxy
        df['supply_score'] = np.log1p(df['quantity'])
        df['listing_frequency'] = df.groupby('item_id').cumcount()
        
        # Fill NaNs
        df = df.fillna(0)
        
        logger.success(f"Engineered {len(df.columns)} features")
        return df
    
    def train(self, df: pd.DataFrame, target_col: str = 'price_next'):
        """Train all ensemble models."""
        logger.info("Training ensemble models...")
        
        # Prepare features
        df = self.prepare_features(df)
        
        # Select feature columns
        exclude_cols = ['timestamp', 'date', 'item_id', target_col, 'price']
        self.feature_names = [col for col in df.columns if col not in exclude_cols]
        
        X = df[self.feature_names].values
        y = df[target_col].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Random Forest
        logger.info("Training Random Forest...")
        self.models['random_forest'] = RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=10,
            n_jobs=-1,
            random_state=42
        )
        self.models['random_forest'].fit(X_scaled, y)
        
        # Train XGBoost
        logger.info("Training XGBoost...")
        self.models['xgboost'] = xgb.XGBRegressor(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            n_jobs=-1,
            random_state=42
        )
        self.models['xgboost'].fit(X_scaled, y)
        
        # Train Gradient Boosting
        logger.info("Training Gradient Boosting...")
        self.models['gradient_boosting'] = GradientBoostingRegressor(
            n_estimators=150,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            random_state=42
        )
        self.models['gradient_boosting'].fit(X_scaled, y)
        
        # Train LSTM (if available)
        if KERAS_AVAILABLE:
            logger.info("Training LSTM...")
            self.models['lstm'] = self._train_lstm(X_scaled, y)
        else:
            self.model_weights['lstm'] = 0
            # Redistribute weight
            self.model_weights['xgboost'] += 0.1
            self.model_weights['gradient_boosting'] += 0.1
        
        # Train Prophet (if available and data suitable)
        if PROPHET_AVAILABLE:
            logger.info("Training Prophet...")
            try:
                self.models['prophet'] = self._train_prophet(df, target_col)
            except Exception as e:
                logger.warning(f"Prophet training failed: {e}")
                self.model_weights['prophet'] = 0
                self.model_weights['xgboost'] += 0.05
                self.model_weights['random_forest'] += 0.05
        
        # Normalize weights
        total_weight = sum(self.model_weights.values())
        self.model_weights = {k: v/total_weight for k, v in self.model_weights.items()}
        
        logger.success("Ensemble training complete!")
        return self
    
    def _train_lstm(self, X, y, sequence_length=7):
        """Train LSTM neural network."""
        # Reshape for LSTM [samples, time steps, features]
        # This is simplified - in production, use proper sequence data
        model = keras.Sequential([
            layers.Dense(128, activation='relu', input_shape=(X.shape[1],)),
            layers.Dropout(0.2),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        model.fit(X, y, epochs=50, batch_size=32, verbose=0, validation_split=0.2)
        
        return model
    
    def _train_prophet(self, df: pd.DataFrame, target_col: str):
        """Train Prophet model for time series forecasting."""
        # Aggregate by day for Prophet
        prophet_df = df.groupby(df['timestamp'].dt.date).agg({
            target_col: 'mean'
        }).reset_index()
        prophet_df.columns = ['ds', 'y']
        
        model = Prophet(
            changepoint_prior_scale=0.05,
            seasonality_prior_scale=10,
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False
        )
        model.fit(prophet_df)
        
        return model
    
    def predict(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate ensemble predictions with confidence intervals.
        
        Returns:
            predictions, confidence_scores
        """
        logger.info("Generating ensemble predictions...")
        
        # Prepare features
        df = self.prepare_features(df)
        X = df[self.feature_names].values
        X_scaled = self.scaler.transform(X)
        
        # Collect predictions from all models
        predictions = []
        
        # Random Forest
        if 'random_forest' in self.models:
            pred_rf = self.models['random_forest'].predict(X_scaled)
            predictions.append((pred_rf, self.model_weights['random_forest']))
        
        # XGBoost
        if 'xgboost' in self.models:
            pred_xgb = self.models['xgboost'].predict(X_scaled)
            predictions.append((pred_xgb, self.model_weights['xgboost']))
        
        # Gradient Boosting
        if 'gradient_boosting' in self.models:
            pred_gb = self.models['gradient_boosting'].predict(X_scaled)
            predictions.append((pred_gb, self.model_weights['gradient_boosting']))
        
        # LSTM
        if 'lstm' in self.models and KERAS_AVAILABLE:
            pred_lstm = self.models['lstm'].predict(X_scaled, verbose=0).flatten()
            predictions.append((pred_lstm, self.model_weights['lstm']))
        
        # Ensemble: weighted average
        ensemble_pred = np.zeros(len(X))
        for pred, weight in predictions:
            ensemble_pred += pred * weight
        
        # Confidence: 1 - std of predictions
        all_preds = np.array([p[0] for p in predictions])
        pred_std = np.std(all_preds, axis=0)
        pred_mean = np.mean(all_preds, axis=0)
        confidence = 1 - (pred_std / (pred_mean + 1))
        confidence = np.clip(confidence, 0, 1)
        
        logger.success(f"Generated {len(ensemble_pred)} ensemble predictions")
        logger.info(f"Average confidence: {confidence.mean():.2%}")
        
        return ensemble_pred, confidence
    
    def save(self, path: str):
        """Save ensemble models."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'wb') as f:
            pickle.dump({
                'models': self.models,
                'scaler': self.scaler,
                'feature_names': self.feature_names,
                'model_weights': self.model_weights
            }, f)
        
        logger.success(f"Ensemble saved to {path}")
    
    def load(self, path: str):
        """Load ensemble models."""
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        self.models = data['models']
        self.scaler = data['scaler']
        self.feature_names = data['feature_names']
        self.model_weights = data['model_weights']
        
        logger.success(f"Ensemble loaded from {path}")
        return self


if __name__ == "__main__":
    # Example usage
    logger.info("Testing ensemble predictor...")
    
    # This would be replaced with real data
    # ensemble = EnsemblePredictor()
    # ensemble.train(training_data)
    # predictions, confidence = ensemble.predict(test_data)
    
    print("Ensemble predictor ready!")
