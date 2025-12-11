"""
Risk Assessment Engine - Evaluate trade risk and optimal position sizing
"""
import numpy as np
import pandas as pd
from loguru import logger
from typing import Dict, Tuple

class RiskAssessment:
    """Assess risk for trades and calculate optimal bet sizes."""
    
    def __init__(self):
        self.risk_free_rate = 0.0  # WoW has no "risk-free" investment
        
    def calculate_volatility(self, price_history: pd.Series, window: int = 30) -> float:
        """Calculate price volatility (standard deviation of returns)."""
        returns = price_history.pct_change().dropna()
        volatility = returns.rolling(window).std().iloc[-1]
        return volatility if not np.isnan(volatility) else 0
    
    def liquidity_score(self, volume_history: pd.Series, window: int = 7) -> float:
        """
        Score how easy it is to sell this item.
        1.0 = very liquid (sells fast)
        0.0 = illiquid (might take weeks)
        """
        avg_volume = volume_history.rolling(window).mean().iloc[-1]
        
        # Normalize: 100+ sales/day = 1.0, 1 sale/day = 0.1
        if avg_volume >= 100:
            return 1.0
        elif avg_volume >= 10:
            return 0.7
        elif avg_volume >= 1:
            return 0.3
        else:
            return 0.1
    
    def competition_risk(self, seller_count: int, avg_seller_count: int) -> float:
        """
        Higher competition = higher risk (price wars).
        Returns risk score 0-1 (0=low risk, 1=high risk)
        """
        if avg_seller_count == 0:
            return 0.5  # Unknown
        
        ratio = seller_count / avg_seller_count
        if ratio > 2.0:
            return 0.9  # Very high competition
        elif ratio > 1.5:
            return 0.7
        elif ratio > 1.0:
            return 0.5
        else:
            return 0.2  # Low competition
    
    def kelly_criterion(self, win_prob: float, win_amount: float, loss_amount: float) -> float:
        """
        Calculate optimal bet size using Kelly Criterion.
        
        Formula: f = (p * b - q) / b
        where:
          f = fraction of bankroll to bet
          p = probability of win
          b = win/loss ratio
          q = probability of loss (1-p)
        
        Returns: Fraction of bankroll to invest (0-1)
        """
        if loss_amount == 0:
            return 0
        
        b = win_amount / loss_amount
        q = 1 - win_prob
        
        kelly_fraction = (win_prob * b - q) / b
        
        # Apply half-Kelly for safety
        kelly_fraction = max(0, min(kelly_fraction * 0.5, 0.25))  # Cap at 25%
        
        return kelly_fraction
    
    def assess_trade(self, item_data: Dict) -> Dict:
        """
        Complete risk assessment for a trade opportunity.
        
        Input: {
            'current_price': float,
            'predicted_price': float,
            'confidence': float,
            'price_history': pd.Series,
            'volume_history': pd.Series,
            'seller_count': int,
            'avg_seller_count': int,
            'bankroll': float
        }
        
        Output: {
            'risk_score': 0-1 (0=safe, 1=risky),
            'liquidity': 0-1,
            'recommended_quantity': int,
            'max_investment': float,
            'expected_roi': float,
            'risk_category': str
        }
        """
        current_price = item_data['current_price']
        predicted_price = item_data['predicted_price']
        confidence = item_data['confidence']
        bankroll = item_data.get('bankroll', 1000000)  # 100g default
        
        # Calculate components
        volatility = self.calculate_volatility(item_data['price_history'])
        liquidity = self.liquidity_score(item_data['volume_history'])
        competition = self.competition_risk(
            item_data['seller_count'],
            item_data['avg_seller_count']
        )
        
        # Overall risk score
        risk_score = (
            (1 - confidence) * 0.4 +
            volatility * 0.3 +
            competition * 0.2 +
            (1 - liquidity) * 0.1
        )
        risk_score = np.clip(risk_score, 0, 1)
        
        # Expected profit
        profit_per_item = predicted_price - current_price
        expected_roi = profit_per_item / current_price
        
        # Kelly criterion for position sizing
        win_prob = confidence
        win_amount = profit_per_item
        loss_amount = current_price * 0.3  # Assume 30% max loss
        
        kelly_fraction = self.kelly_criterion(win_prob, win_amount, loss_amount)
        
        # Adjust for risk
        risk_adjusted_fraction = kelly_fraction * (1 - risk_score * 0.5)
        
        # Calculate investment
        max_investment = bankroll * risk_adjusted_fraction
        recommended_quantity = int(max_investment / current_price)
        
        # Risk category
        if risk_score < 0.3:
            risk_category = "LOW - Safe trade"
        elif risk_score < 0.5:
            risk_category = "MEDIUM - Moderate risk"
        elif risk_score < 0.7:
            risk_category = "HIGH - Risky, reduce size"
        else:
            risk_category = "EXTREME - Avoid or tiny position"
        
        return {
            'risk_score': round(risk_score, 2),
            'liquidity': round(liquidity, 2),
            'volatility': round(volatility, 2),
            'competition': round(competition, 2),
            'recommended_quantity': recommended_quantity,
            'max_investment': round(max_investment),
            'expected_roi': round(expected_roi * 100, 1),
            'risk_category': risk_category,
            'kelly_fraction': round(kelly_fraction, 3)
        }
    
    def portfolio_diversification(self, positions: list) -> Dict:
        """
        Analyze portfolio diversification.
        Warns if too much capital in one item/category.
        """
        total_value = sum(p['value'] for p in positions)
        
        if total_value == 0:
            return {'warning': 'No positions'}
        
        # Check concentration
        max_position = max(p['value'] for p in positions)
        concentration = max_position / total_value
        
        # Category concentration
        categories = {}
        for p in positions:
            cat = p.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + p['value']
        
        max_category_pct = max(categories.values()) / total_value if categories else 0
        
        warnings = []
        if concentration > 0.3:
            warnings.append(f"⚠️ {concentration*100:.0f}% in single item - reduce concentration!")
        if max_category_pct > 0.5:
            warnings.append(f"⚠️ {max_category_pct*100:.0f}% in one category - diversify!")
        if len(positions) < 5:
            warnings.append("⚠️ Too few positions - increase diversity")
        
        return {
            'total_positions': len(positions),
            'total_value': total_value,
            'concentration': round(concentration, 2),
            'max_category_pct': round(max_category_pct, 2),
            'warnings': warnings,
            'diversification_score': 1 - concentration
        }


if __name__ == "__main__":
    # Example
    risk = RiskAssessment()
    
    # Mock data
    item = {
        'current_price': 10000,
        'predicted_price': 15000,
        'confidence': 0.85,
        'price_history': pd.Series([9000, 9500, 10000, 10500, 10000]),
        'volume_history': pd.Series([50, 60, 55, 50, 52]),
        'seller_count': 10,
        'avg_seller_count': 8,
        'bankroll': 1000000
    }
    
    assessment = risk.assess_trade(item)
    print("Risk Assessment:")
    for k, v in assessment.items():
        print(f"  {k}: {v}")
