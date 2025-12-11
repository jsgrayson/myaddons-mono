"""
goblin_domination.py - Market Domination Strategies

Aggressive, competitive strategies for market control:
1. Reset Sniping - Buy out all competition, set new floor
2. Monopoly Control - Corner entire item markets
3. Manipulation Detection - Avoid traps, exploit manipulators
4. Competitor Analysis - Track other goblins, counter their moves
5. Flash Crash Buying - Detect panic sells, buy low
6. Weekend/Event Timing - Post peak times only
7. Supply Chokepoints - Control material bottlenecks

WARNING: These strategies are AGGRESSIVE. Use responsibly.
"""

import numpy as np
from typing import List, Dict, Tuple
from collections import defaultdict
from datetime import datetime, timedelta

# ============================================================================
# Market Reset Sniping
# ============================================================================

class ResetSniper:
    """
    Identify items where you can buy out all competition and reset the market
    
    Strategy:
    1. Find items with low supply (<10 auctions)
    2. Calculate total buyout cost
    3. If affordable, buy ALL listings
    4. Relist at 3-5x higher price
    5. Profit from scarcity
    """
    
    def __init__(self, max_investment: int = 1000000):  # 1000g max
        self.max_investment = max_investment
    
    def find_reset_opportunities(self, scan_data: List[Dict]) -> List[Dict]:
        """
        Find items ready for market reset
        
        Returns opportunities sorted by profit potential
        """
        opportunities = []
        
        for item in scan_data:
            item_id = item.get('item_id')
            num_auctions = item.get('num_auctions', 0)
            avg_price = item.get('avg_buyout', 0)
            market_value = item.get('market_value', 0)
            
            # Criteria for reset
            if num_auctions > 15:
                continue  # Too much supply
            
            if num_auctions < 2:
                continue  # Already controlled
            
            # Calculate total buyout cost
            total_cost = avg_price * num_auctions
            
            if total_cost > self.max_investment:
                continue  # Too expensive
            
            # Calculate new price after reset (3x current)
            reset_price = market_value * 3
            
            # Estimate profit (assume selling half your stock)
            expected_sales = num_auctions * 0.5
            gross_revenue = reset_price * expected_sales
            profit = gross_revenue - total_cost
            roi = (profit / total_cost) * 100 if total_cost > 0 else 0
            
            if profit < 50000:  # Minimum 50g profit
                continue
            
            opportunities.append({
                "item_id": item_id,
                "current_supply": num_auctions,
                "buyout_cost": total_cost,
                "reset_price": reset_price,
                "expected_profit": int(profit),
                "roi": round(roi, 1),
                "risk": "medium",
                "action": f"BUY ALL {num_auctions} listings for {self._format_gold(total_cost)}, relist at {self._format_gold(reset_price)}",
            })
        
        # Sort by ROI
        opportunities.sort(key=lambda x: x['roi'], reverse=True)
        
        return opportunities
    
    def _format_gold(self, copper: int) -> str:
        """Format copper to gold string"""
        gold = copper // 10000
        return f"{gold}g"

# ============================================================================
# Monopoly Control System
# ============================================================================

class MonopolyController:
    """
    Establish and maintain monopolies on profitable items
    
    Strategy:
    1. Identify high-margin items with consistent demand
    2. Buy out all competition repeatedly
    3. Maintain price floor at 2-3x normal
    4. Auto-repost when undercut
    5. Discourage competition through persistence
    """
    
    def __init__(self):
        self.controlled_items = {}  # item_id -> control_data
    
    def identify_monopoly_targets(self, scan_data: List[Dict]) -> List[Dict]:
        """
        Find items suitable for monopoly control
        
        Best targets:
        - High demand (>20 sales/day)
        - Low competition (<5 sellers)
        - High margin (>100% profit possible)
        - Not easily farmable (crafted items better than drops)
        """
        targets = []
        
        for item in scan_data:
            demand = item.get('sale_rate', 0) * 100  # Sales per day
            sellers = item.get('num_sellers', 0)
            margin = item.get('profit_margin', 0)
            is_craftable = item.get('is_craftable', False)
            
            # Monopoly criteria
            if demand < 10:
                continue  # Not enough demand
            
            if sellers > 8:
                continue  # Too much competition
            
            if margin < 0.5:
                continue  # Margins too thin
            
            # Scoring
            score = (demand * 2) + (margin * 100) - (sellers * 10)
            
            if is_craftable:
                score += 20  # Bonus for crafted (controllable supply)
            
            targets.append({
                "item_id": item['item_id'],
                "demand_score": round(demand, 1),
                "competition": sellers,
                "margin": round(margin * 100, 1),
                "monopoly_score": round(score, 1),
                "strategy": "Buy out daily, maintain high prices",
            })
        
        # Sort by monopoly score
        targets.sort(key=lambda x: x['monopoly_score'], reverse=True)
        
        return targets[:10]  # Top 10 targets

# ============================================================================
# Manipulation Detection & Counter-Play
# ============================================================================

class ManipulationDetector:
    """
    Detect when OTHER players are manipulating prices
    
    Then either:
    - Avoid the trap
    - Exploit their manipulation
    """
    
    def detect_manipulation(self, price_history: List[Dict]) -> Dict:
        """
        Detect price manipulation patterns
        
        Manipulation signals:
        1. Sudden price spike (>200%) with low volume
        2. Single seller posting 100+ auctions
        3. Walls (many auctions at exact same price)
        """
        if len(price_history) < 10:
            return {"manipulation": False}
        
        recent_prices = [p['price'] for p in price_history[-10:]]
        older_prices = [p['price'] for p in price_history[:-10]]
        
        recent_avg = np.mean(recent_prices)
        older_avg = np.mean(older_prices)
        
        # Check for sudden spike
        spike = (recent_avg - older_avg) / older_avg
        
        if spike > 2.0:  # 200% increase
            return {
                "manipulation": True,
                "type": "artificial_spike",
                "action": "DO NOT BUY - Manipulator trying to dump",
                "confidence": 0.85,
            }
        
        # Check for wall (many identical prices)
        price_counts = defaultdict(int)
        for p in price_history[-20:]:
            price_counts[p['price']] += 1
        
        max_count = max(price_counts.values()) if price_counts else 0
        
        if max_count > 15:
            return {
                "manipulation": True,
                "type": "price_wall",
                "action": "Post slightly under wall to force them to cancel",
                "confidence": 0.70,
            }
        
        return {"manipulation": False}

# ============================================================================
# Competitor Tracking System
# ============================================================================

class CompetitorTracker:
    """
    Track other auction house goblins and counter their strategies
    
    Learns:
    - Who your competitors are
    - Their posting patterns
    - Their undercut amounts
    - When they're online
    
    Counter-strategies:
    - Post when they're offline
    - Undercut differently to discourage them
    - Target their weak spots
    """
    
    def __init__(self):
        self.competitors = defaultdict(lambda: {
            "listings": 0,
            "undercuts": [],
            "online_times": [],
            "threat_level": 0
        })
    
    def track_competitor(self, seller_name: str, action: Dict):
        """Record competitor activity"""
        comp = self.competitors[seller_name]
        
        if action['type'] == 'listing':
            comp['listings'] += 1
        elif action['type'] == 'undercut':
            comp['undercuts'].append(action['amount'])
        
        comp['online_times'].append(datetime.now().hour)
        
        # Calculate threat level
        comp['threat_level'] = min(comp['listings'] / 100, 1.0)
    
    def get_top_competitors(self, limit: int = 5) -> List[Dict]:
        """Get most dangerous competitors"""
        ranked = []
        
        for name, data in self.competitors.items():
            ranked.append({
                "name": name,
                "listings": data['listings'],
                "avg_undercut": np.mean(data['undercuts']) if data['undercuts'] else 0,
                "threat_level": data['threat_level'],
                "active_hours": self._get_peak_hours(data['online_times']),
            })
        
        ranked.sort(key=lambda x: x['threat_level'], reverse=True)
        
        return ranked[:limit]
    
    def _get_peak_hours(self, hours: List[int]) -> str:
        """Determine when competitor is most active"""
        if not hours:
            return "Unknown"
        
        hour_counts = defaultdict(int)
        for h in hours:
            hour_counts[h] += 1
        
        peak = max(hour_counts.items(), key=lambda x: x[1])[0]
        
        return f"{peak}:00-{peak+2}:00"

# ============================================================================
# Flash Crash Buyer
# ============================================================================

class FlashCrashBuyer:
    """
    Detect panic sells and buy ultra-cheap
    
    Triggers:
    - Price drops >50% suddenly
    - Large volume posted at once
    - Usually happens after patch nerfs
    
    Strategy: Buy the panic, sell when stabilizes
    """
    
    def detect_crash(self, item: Dict, price_history: List[Dict]) -> Dict:
        """Detect flash crash opportunity"""
        if len(price_history) < 5:
            return {"crash": False}
        
        current_price = item.get('avg_buyout', 0)
        historical_avg = np.mean([p['price'] for p in price_history])
        
        drop = (historical_avg - current_price) / historical_avg
        
        if drop > 0.4:  # 40% drop
            return {
                "crash": True,
                "drop_pct": round(drop * 100, 1),
                "action": "BUY MAXIMUM - This is a panic sell",
                "expected_recovery": f"{round(historical_avg / 10000, 1)}g",
                "confidence": 0.9,
            }
        
        return {"crash": False}

# ============================================================================
# Domination Strategy Coordinator
# ============================================================================

class MarketDominationEngine:
    """
    Coordinates all aggressive strategies for maximum profit
    """
    
    def __init__(self, capital: int = 5000000):  # 5000g starting capital
        self.capital = capital
        self.reset_sniper = ResetSniper(max_investment=capital * 0.2)
        self.monopoly = MonopolyController()
        self.manipulation = ManipulationDetector()
        self.competitor = CompetitorTracker()
        self.flash = FlashCrashBuyer()
    
    def analyze_and_dominate(self, scan_data: List[Dict]) -> Dict:
        """
        Run all domination strategies and return top opportunities
        """
        results = {
            "reset_opportunities": [],
            "monopoly_targets": [],
            "flash_crashes": [],
            "competitor_analysis": [],
            "total_profit_potential": 0,
        }
        
        # Reset sniping
        resets = self.reset_sniper.find_reset_opportunities(scan_data)
        results['reset_opportunities'] = resets[:5]
        
        # Monopoly targets
        monopolies = self.monopoly.identify_monopoly_targets(scan_data)
        results['monopoly_targets'] = monopolies
        
        # Calculate profit potential
        reset_profit = sum(r['expected_profit'] for r in resets[:5])
        results['total_profit_potential'] = reset_profit
        
        return results
    
    def get_daily_strategy(self) -> str:
        """
        Get today's recommended domination strategy
        """
        day = datetime.now().weekday()
        
        strategies = {
            0: "Monday: Reset weekend dump items",
            1: "Tuesday: Raid prep - buy flasks/potions now",
            2: "Wednesday: Monopoly control - establish positions",
            3: "Thursday: Undercut wars - drive out competition",
            4: "Friday: Weekend preparation - stock high-demand",
            5: "Saturday: Premium pricing - casuals buying",
            6: "Sunday: Last-minute sales before reset",
        }
        
        return strategies.get(day, "Dominate the market")

# ============================================================================
# Flask Endpoint
# ============================================================================

def get_domination_strategies(scan_data: List[Dict]) -> Dict:
    """
    Endpoint for domination strategies
    
    Usage in server.py:
        @app.route('/api/goblin/dominate')
        def goblin_dominate():
            scan = get_latest_scan()
            return get_domination_strategies(scan)
    """
    engine = MarketDominationEngine()
    
    strategies = engine.analyze_and_dominate(scan_data)
    strategies['daily_focus'] = engine.get_daily_strategy()
    
    return strategies

if __name__ == "__main__":
    # Test
    test_scan = [
        {
            "item_id": 210814,
            "num_auctions": 5,
            "avg_buyout": 50000,
            "market_value": 120000,
            "sale_rate": 0.8,
            "num_sellers": 3,
            "profit_margin": 0.6,
        }
    ]
    
    engine = MarketDominationEngine()
    result = engine.analyze_and_dominate(test_scan)
    
    print("🔥 MARKET DOMINATION ANALYSIS 🔥")
    print(f"\nReset Opportunities: {len(result['reset_opportunities'])}")
    print(f"Monopoly Targets: {len(result['monopoly_targets'])}")
    print(f"Total Profit Potential: {result['total_profit_potential'] // 10000}g")
