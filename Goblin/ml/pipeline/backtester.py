"""
Backtesting Framework - Test ML strategies on historical data
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from loguru import logger
from typing import Dict, List, Tuple
import json
import os

class Backtester:
    """Backtest trading strategies on historical data."""
    
    def __init__(self):
        self.trades = []
        self.portfolio = {'gold': 1000000, 'items': {}}  # Start with 100g
        self.initial_gold = self.portfolio['gold']
        
    def load_historical_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Load historical auction data for backtesting."""
        # In production, load from saved CSVs
        data_dir = os.path.join(os.path.dirname(__file__), "../data/raw")
        
        import glob
        all_files = sorted(glob.glob(os.path.join(data_dir, "blizzard_*.csv")))
        
        dfs = []
        for file in all_files:
            df = pd.read_csv(file)
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                dfs.append(df)
        
        if not dfs:
            logger.warning("No historical data found")
            return pd.DataFrame()
        
        combined = pd.concat(dfs, ignore_index=True)
        combined = combined.sort_values('timestamp')
        
        # Filter date range
        combined = combined[
            (combined['timestamp'] >= start_date) &
            (combined['timestamp'] <= end_date)
        ]
        
        logger.info(f"Loaded {len(combined)} historical records")
        return combined
    
    def simulate_trade(self, timestamp: datetime, item_id: int, action: str,
                      price: float, quantity: int) -> bool:
        """
        Simulate a buy or sell trade.
        
        Returns True if trade successful, False if insufficient funds/items
        """
        if action == 'buy':
            cost = price * quantity
            if self.portfolio['gold'] >= cost:
                self.portfolio['gold'] -= cost
                self.portfolio['items'][item_id] = self.portfolio['items'].get(item_id, 0) + quantity
                
                self.trades.append({
                    'timestamp': timestamp,
                    'action': 'buy',
                    'item_id': item_id,
                    'price': price,
                    'quantity': quantity,
                    'cost': cost
                })
                return True
            else:
                return False
                
        elif action == 'sell':
            if self.portfolio['items'].get(item_id, 0) >= quantity:
                ah_cut = 0.05
                revenue = price * quantity * (1 - ah_cut)
                self.portfolio['gold'] += revenue
                self.portfolio['items'][item_id] -= quantity
                
                self.trades.append({
                    'timestamp': timestamp,
                    'action': 'sell',
                    'item_id': item_id,
                    'price': price,
                    'quantity': quantity,
                    'revenue': revenue
                })
                return True
            else:
                return False
    
    def run_strategy(self, predictions: pd.DataFrame, strategy: str = 'simple') -> Dict:
        """
        Backtest a strategy on predictions.
        
        Strategies:
        - 'simple': Buy when predicted > current, sell when predicted < current
        - 'threshold': Only trade if confidence > X and margin > Y%
        - 'kelly': Use Kelly criterion for position sizing
        """
        logger.info(f"Running backtest with strategy: {strategy}")
        
        for idx, row in predictions.iterrows():
            timestamp = row['timestamp']
            item_id = row['item_id']
            current_price = row['price']
            predicted_price = row.get('predicted_price', current_price)
            confidence = row.get('confidence', 0.5)
            
            # Simple strategy
            if strategy == 'simple':
                if predicted_price > current_price * 1.2:  # 20% margin
                    # Buy signal
                    quantity = min(10, int(self.portfolio['gold'] * 0.1 / current_price))
                    if quantity > 0:
                        self.simulate_trade(timestamp, item_id, 'buy', current_price, quantity)
                        
                elif item_id in self.portfolio['items'] and self.portfolio['items'][item_id] > 0:
                    if current_price > predicted_price * 1.1:  # Price above prediction, sell
                        quantity = self.portfolio['items'][item_id]
                        self.simulate_trade(timestamp, item_id, 'sell', current_price, quantity)
            
            # Threshold strategy
            elif strategy == 'threshold':
                margin = (predicted_price - current_price) / current_price
                if margin > 0.3 and confidence > 0.8:  # 30% margin, 80% confidence
                    quantity = min(5, int(self.portfolio['gold'] * 0.05 / current_price))
                    if quantity > 0:
                        self.simulate_trade(timestamp, item_id, 'buy', current_price, quantity)
        
        # Calculate final value
        final_value = self.portfolio['gold']
        for item_id, qty in self.portfolio['items'].items():
            # Use last known price
            last_price = predictions[predictions['item_id'] == item_id]['price'].iloc[-1] if len(predictions[predictions['item_id'] == item_id]) > 0 else 0
            final_value += last_price * qty * 0.95  # Account for AH cut
        
        total_return = final_value - self.initial_gold
        roi = (total_return / self.initial_gold) * 100
        
        return {
            'strategy': strategy,
            'initial_gold': self.initial_gold,
            'final_gold': self.portfolio['gold'],
            'final_portfolio_value': final_value,
            'total_return': total_return,
            'roi_pct': roi,
            'num_trades': len(self.trades),
            'num_buys': len([t for t in self.trades if t['action'] == 'buy']),
            'num_sells': len([t for t in self.trades if t['action'] == 'sell'])
        }
    
    def performance_metrics(self) -> Dict:
        """Calculate detailed performance metrics."""
        if not self.trades:
            return {'error': 'No trades executed'}
        
        df = pd.DataFrame(self.trades)
        
        # Win rate
        profitable_trades = 0
        total_pairs = 0
        
        # Match buys with sells
        buys = df[df['action'] == 'buy'].groupby('item_id')
        sells = df[df['action'] == 'sell'].groupby('item_id')
        
        for item_id in buys.groups.keys():
            if item_id in sells.groups.keys():
                buy_avg = buys.get_group(item_id)['price'].mean()
                sell_avg = sells.get_group(item_id)['price'].mean()
                if sell_avg > buy_avg:
                    profitable_trades += 1
                total_pairs += 1
        
        win_rate = profitable_trades / total_pairs if total_pairs > 0 else 0
        
        # Sharpe ratio (simplified)
        if len(self.trades) > 1:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Daily returns
            daily_value = df.groupby(df['timestamp'].dt.date).apply(
                lambda x: x[x['action'] == 'sell']['revenue'].sum() - x[x['action'] == 'buy']['cost'].sum()
            )
            
            if len(daily_value) > 1:
                returns = daily_value.pct_change().dropna()
                sharpe = returns.mean() / returns.std() if returns.std() > 0 else 0
            else:
                sharpe = 0
        else:
            sharpe = 0
        
        return {
            'win_rate': round(win_rate * 100, 1),
            'sharpe_ratio': round(sharpe, 2),
            'avg_trade_profit': round(df[df['action'] == 'sell']['revenue'].mean() - df[df['action'] == 'buy']['cost'].mean()) if len(df) > 0 else 0,
            'total_pairs': total_pairs,
            'profitable_pairs': profitable_trades
        }
    
    def save_results(self, path: str):
        """Save backtest results."""
        results = {
            'portfolio': self.portfolio,
            'trades': self.trades,
            'summary': self.run_strategy(pd.DataFrame(), 'simple'),  # Recalc summary
            'metrics': self.performance_metrics()
        }
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.success(f"Backtest results saved to {path}")


if __name__ == "__main__":
    # Example
    backtester = Backtester()
    
    # Would load real historical data
    # historical = backtester.load_historical_data('2024-01-01', '2024-11-01')
    
    # Would load predictions
    # results = backtester.run_strategy(predictions_df, strategy='threshold')
    
    print("Backtester ready!")
