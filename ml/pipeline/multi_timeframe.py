"""
Multi-Timeframe Predictions - Forecast at different time horizons
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from loguru import logger
from typing import Dict, List
from ml.pipeline.ensemble_predictor import EnsemblePredictor

class MultiTimeframePredictor:
    """Generate predictions across multiple time horizons."""
    
    def __init__(self):
        self.predictors = {
            '1h': EnsemblePredictor(),
            '1d': EnsemblePredictor(),
            '7d': EnsemblePredictor(),
            '30d': EnsemblePredictor()
        }
        
    def prepare_targets(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create target variables for each timeframe."""
        df = df.sort_values(['item_id', 'timestamp'])
        
        # 1-hour ahead
        df['price_1h'] = df.groupby('item_id')['price'].shift(-1)
        
        # 1-day ahead (assuming hourly data)
        df['price_1d'] = df.groupby('item_id')['price'].shift(-24)
        
        # 7-day ahead
        df['price_7d'] = df.groupby('item_id')['price'].shift(-168)
        
        # 30-day ahead
        df['price_30d'] = df.groupby('item_id')['price'].shift(-720)
        
        return df
    
    def train_all_horizons(self, df: pd.DataFrame):
        """Train separate models for each time horizon."""
        logger.info("Training multi-timeframe models...")
        
        df = self.prepare_targets(df)
        
        for horizon, predictor in self.predictors.items():
            target_col = f'price_{horizon}'
            
            # Filter out rows without target
            train_df = df[df[target_col].notna()].copy()
            
            if len(train_df) < 100:
                logger.warning(f"Insufficient data for {horizon} model")
                continue
            
            logger.info(f"Training {horizon} model on {len(train_df)} samples...")
            predictor.train(train_df, target_col=target_col)
        
        logger.success("Multi-timeframe training complete")
    
    def predict_all_horizons(self, df: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Generate predictions for all time horizons."""
        predictions = {}
        
        for horizon, predictor in self.predictors.items():
            try:
                pred, conf = predictor.predict(df)
                predictions[horizon] = {
                    'predictions': pred,
                    'confidence': conf
                }
                logger.info(f"{horizon} predictions: avg={pred.mean()/10000:.2f}g, conf={conf.mean():.2%}")
            except Exception as e:
                logger.error(f"Error predicting {horizon}: {e}")
                predictions[horizon] = None
        
        return predictions
    
    def get_trading_signals(self, current_price: float, predictions: Dict) -> Dict:
        """
        Generate trading signals based on multi-timeframe analysis.
        
        Returns recommended action and reasoning.
        """
        signals = []
        
        for horizon, pred_data in predictions.items():
            if pred_data is None:
                continue
            
            pred = pred_data['predictions'][0]  # First item
            conf = pred_data['confidence'][0]
            
            change_pct = ((pred - current_price) / current_price) * 100
            
            if horizon == '1h':
                # Short-term signal
                if change_pct > 10 and conf > 0.7:
                    signals.append({
                        'horizon': '1h',
                        'signal': 'BUY - Quick flip',
                        'strength': conf,
                        'expected_return': change_pct
                    })
            
            elif horizon == '1d':
                # Daily signal
                if change_pct > 20 and conf > 0.75:
                    signals.append({
                        'horizon': '1d',
                        'signal': 'BUY - Hold overnight',
                        'strength': conf,
                        'expected_return': change_pct
                    })
            
            elif horizon == '7d':
                # Weekly signal
                if change_pct > 50 and conf > 0.8:
                    signals.append({
                        'horizon': '7d',
                        'signal': 'BUY - Week-long investment',
                        'strength': conf,
                        'expected_return': change_pct
                    })
            
            elif horizon == '30d':
                # Long-term signal
                if change_pct > 100 and conf > 0.85:
                    signals.append({
                        'horizon': '30d',
                        'signal': 'BUY - Long-term hold',
                        'strength': conf,
                        'expected_return': change_pct
                    })
        
        # Determine overall recommendation
        if not signals:
            recommendation = "HOLD - No clear opportunity"
        elif len(signals) >= 3:
            recommendation = "STRONG BUY - Multiple timeframes aligned"
        else:
            recommendation = signals[0]['signal']
        
        return {
            'recommendation': recommendation,
            'signals': signals,
            'num_aligned': len(signals)
        }


class MarketRegimeDetector:
    """Detect current market regime (bull/bear/volatile/stable)."""
    
    def __init__(self):
        self.regimes = ['bull', 'bear', 'volatile', 'stable']
        
    def detect_regime(self, price_history: pd.Series, volume_history: pd.Series = None) -> str:
        """
        Detect current market regime.
        
        Returns: 'bull', 'bear', 'volatile', or 'stable'
        """
        if len(price_history) < 30:
            return 'unknown'
        
        # Calculate metrics
        returns = price_history.pct_change().dropna()
        recent_returns = returns.tail(14)  # Last 2 weeks
        
        # Trend
        trend = recent_returns.mean()
        
        # Volatility
        volatility = recent_returns.std()
        
        # Volume trend (if available)
        if volume_history is not None and len(volume_history) >= 30:
            vol_trend = volume_history.tail(14).mean() / volume_history.head(14).mean()
        else:
            vol_trend = 1.0
        
        # Classification
        if trend > 0.02 and volatility < 0.1:
            return 'bull'  # Rising prices, low volatility
        elif trend < -0.02 and volatility < 0.1:
            return 'bear'  # Falling prices, low volatility
        elif volatility > 0.2:
            return 'volatile'  # High volatility regardless of trend
        else:
            return 'stable'  # Low volatility, no strong trend
    
    def regime_strategy(self, regime: str) -> Dict:
        """Recommend strategy based on market regime."""
        strategies = {
            'bull': {
                'action': 'AGGRESSIVE',
                'description': 'Buy dips, ride the trend',
                'risk_tolerance': 'High',
                'position_size': '20-30% of bankroll',
                'hold_time': 'Medium to long'
            },
            'bear': {
                'action': 'DEFENSIVE',
                'description': 'Sell rallies, reduce exposure',
                'risk_tolerance': 'Low',
                'position_size': '5-10% of bankroll',
                'hold_time': 'Very short'
            },
            'volatile': {
                'action': 'CAUTIOUS',
                'description': 'Small positions, quick exits',
                'risk_tolerance': 'Low',
                'position_size': '5-15% of bankroll',
                'hold_time': 'Very short (day trading)'
            },
            'stable': {
                'action': 'NORMAL',
                'description': 'Standard flipping, moderate risk',
                'risk_tolerance': 'Medium',
                'position_size': '15-20% of bankroll',
                'hold_time': 'Medium'
            }
        }
        
        return strategies.get(regime, strategies['stable'])


if __name__ == "__main__":
    # Example
    mtf = MultiTimeframePredictor()
    detector = MarketRegimeDetector()
    
    # Mock data
    price_history = pd.Series([10000, 10500, 11000, 11200, 10800] * 6)
    
    regime = detector.detect_regime(price_history)
    strategy = detector.regime_strategy(regime)
    
    print(f"Market Regime: {regime}")
    print(f"Strategy: {strategy['action']}")
    print(f"Description: {strategy['description']}")
