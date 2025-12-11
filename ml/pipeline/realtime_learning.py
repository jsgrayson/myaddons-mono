"""
Real-Time Learning System - Online learning for instant model updates
"""
import pandas as pd
import numpy as np
from loguru import logger
import joblib
import os
from typing import Dict, List, Any

class RealTimeLearner:
    """
    Implements online learning capabilities to update models incrementally.
    
    Note: Not all models support true online learning (partial_fit).
    - XGBoost: Supports incremental training via xgb.train with xgb_model parameter.
    - RandomForest: Does NOT support incremental learning easily (requires retraining).
    - SGDRegressor / PassiveAggressiveRegressor: Support partial_fit (good for online).
    
    Strategy:
    1. Use a lightweight "Online Corrector" model (SGD/PassiveAggressive) that learns the *error* of the main ensemble.
    2. Update this corrector instantly with every new data point.
    3. Apply the correction to the main ensemble's prediction.
    4. Periodically (e.g., daily) retrain the heavy ensemble.
    """
    
    def __init__(self, model_dir: str = "ml/models"):
        self.model_dir = model_dir
        self.corrector_model = None
        self.corrector_path = os.path.join(model_dir, "online_corrector.pkl")
        self._load_or_create_corrector()
        
    def _load_or_create_corrector(self):
        """Load existing corrector or create a new one."""
        from sklearn.linear_model import PassiveAggressiveRegressor
        
        if os.path.exists(self.corrector_path):
            try:
                self.corrector_model = joblib.load(self.corrector_path)
                logger.info("Loaded online corrector model.")
            except Exception as e:
                logger.error(f"Failed to load corrector: {e}")
                self.corrector_model = PassiveAggressiveRegressor(C=0.1, random_state=42)
        else:
            self.corrector_model = PassiveAggressiveRegressor(C=0.1, random_state=42)
            logger.info("Initialized new online corrector model.")

    def update(self, features: pd.DataFrame, actual_prices: pd.Series, predicted_prices: pd.Series):
        """
        Update the corrector model with new ground truth.
        
        Args:
            features: The features used for prediction.
            actual_prices: The actual market prices observed.
            predicted_prices: What the main ensemble predicted.
        """
        if features.empty:
            return
            
        # We want to learn the Residual (Error) = Actual - Predicted
        residuals = actual_prices - predicted_prices
        
        # Update the model
        # Note: partial_fit requires X and y
        try:
            self.corrector_model.partial_fit(features, residuals)
            self._save_corrector()
            logger.info(f"Updated online corrector with {len(features)} samples.")
        except Exception as e:
            logger.error(f"Online update failed: {e}")

    def predict_correction(self, features: pd.DataFrame) -> np.ndarray:
        """
        Predict the error correction for new samples.
        """
        try:
            # Check if model is fitted (has coef_)
            if hasattr(self.corrector_model, "coef_"):
                return self.corrector_model.predict(features)
            else:
                return np.zeros(len(features))
        except Exception as e:
            logger.warning(f"Corrector prediction failed (might be untrained): {e}")
            return np.zeros(len(features))

    def _save_corrector(self):
        """Save the corrector model to disk."""
        try:
            os.makedirs(self.model_dir, exist_ok=True)
            joblib.dump(self.corrector_model, self.corrector_path)
        except Exception as e:
            logger.error(f"Failed to save corrector: {e}")

    def apply_correction(self, ensemble_prediction: float, features: pd.DataFrame) -> float:
        """
        Apply the learned correction to a prediction.
        """
        correction = self.predict_correction(features)[0]
        
        # Damping factor to prevent wild swings from online learning
        damping = 0.5 
        
        final_pred = ensemble_prediction + (correction * damping)
        return max(0, final_pred) # Ensure no negative prices
