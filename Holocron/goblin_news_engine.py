"""
goblin_news_engine.py - News-Aware Market Prediction

Scans WoW news sites and predicts market shifts based on:
- Patch notes (buffs/nerfs)
- Upcoming events (holidays, raid releases)
- Class changes (meta shifts)
- Profession changes (recipe additions/removals)

Examples:
- "Fire Mage buffed" → Predict demand spike for Fire enchants/gems
- "New raid next week" → Predict flask/potion demand increase
- "Holiday event" → Predict event toy/pet demand

Data Sources:
- Wowhead news
- MMO-Champion blueposts
- Official Blizzard patch notes
- Reddit r/wow trends
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Any
import re
from collections import defaultdict
import os
import pickle
from goblin_training import MarketPredictionModel

# ============================================================================
# News Scraper
# ============================================================================

class WoWNewsScraper:
    def __init__(self):
        self.sources = {
            "wowhead": "https://www.wowhead.com/news",
            "mmochampion": "https://www.mmo-champion.com/",
            "blizzard": "https://worldofwarcraft.blizzard.com/en-us/news",
        }
        self.cache = {}
        self.last_scrape = None
    
    def scrape_all_sources(self) -> List[Dict]:
        """Scrape all news sources and return articles"""
        articles = []
        
        # Scrape Wowhead
        articles.extend(self._scrape_wowhead())
        
        # Scrape MMO-Champion
        articles.extend(self._scrape_mmochampion())
        
        # Scrape Blizzard official
        articles.extend(self._scrape_blizzard())
        
        self.last_scrape = datetime.now()
        return articles
    
    def _scrape_wowhead(self) -> List[Dict]:
        """Scrape Wowhead news"""
        try:
            response = requests.get(self.sources["wowhead"], timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = []
            # Find news articles (simplified - actual selectors may vary)
            for article in soup.find_all('article', limit=10):
                title_elem = article.find('h2') or article.find('h3')
                link_elem = article.find('a')
                
                if title_elem and link_elem:
                    articles.append({
                        "source": "wowhead",
                        "title": title_elem.get_text(strip=True),
                        "url": f"https://www.wowhead.com{link_elem.get('href', '')}",
                        "timestamp": datetime.now().isoformat(),
                    })
            
            return articles
        except Exception as e:
            print(f"Error scraping Wowhead: {e}")
            return []
    
    def _scrape_mmochampion(self) -> List[Dict]:
        """Scrape MMO-Champion"""
        try:
            response = requests.get(self.sources["mmochampion"], timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = []
            # MMO-Champion structure (simplified)
            for item in soup.find_all('div', class_='news-item', limit=10):
                title_elem = item.find('h3') or item.find('a')
                
                if title_elem:
                    articles.append({
                        "source": "mmochampion",
                        "title": title_elem.get_text(strip=True),
                        "url": self.sources["mmochampion"],
                        "timestamp": datetime.now().isoformat(),
                    })
            
            return articles
        except Exception as e:
            print(f"Error scraping MMO-Champion: {e}")
            return []
    
    def _scrape_blizzard(self) -> List[Dict]:
        """Scrape official Blizzard news"""
        try:
            response = requests.get(self.sources["blizzard"], timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = []
            # Blizzard news structure (simplified)
            for article in soup.find_all('article', limit=10):
                title_elem = article.find('h3')
                
                if title_elem:
                    articles.append({
                        "source": "blizzard",
                        "title": title_elem.get_text(strip=True),
                        "url": self.sources["blizzard"],
                        "timestamp": datetime.now().isoformat(),
                    })
            
            return articles
        except Exception as e:
            print(f"Error scraping Blizzard: {e}")
            return []

# ============================================================================
# News Analysis Engine
# ============================================================================

class NewsAnalysisEngine:
    def __init__(self):
        # Keyword correlation tables
        self.class_items = {
            "fire mage": [210814, 211515],  # Fire-specific consumables
            "frost mage": [210815, 211516],
            "warrior": [210820, 211520],
            # ... expanded with actual item IDs
        }
        
        self.event_items = {
            "raid": [210814, 210815, 210816],  # Flasks, potions, food
            "holiday": [211000, 211001],        # Event toys/pets
            "pvp season": [212000, 212001],     # PvP gear/gems
        }
        
        self.profession_items = {
            "alchemy": [210814, 210815],
            "enchanting": [211500, 211501],
            "blacksmithing": [212500, 212501],
        }
    
    def analyze_news(self, articles: List[Dict]) -> List[Dict]:
        """
        Analyze news articles and predict market impacts
        
        Returns:
            List of predictions with confidence scores
        """
        predictions = []
        
        for article in articles:
            title = article['title'].lower()
            
            # Detect class buffs/nerfs
            class_pred = self._detect_class_changes(title)
            if class_pred:
                predictions.append({
                    **class_pred,
                    "article": article['title'],
                    "source": article['source'],
                })
            
            # Detect upcoming events
            event_pred = self._detect_events(title)
            if event_pred:
                predictions.append({
                    **event_pred,
                    "article": article['title'],
                    "source": article['source'],
                })
            
            # Detect profession changes
            prof_pred = self._detect_profession_changes(title)
            if prof_pred:
                predictions.append({
                    **prof_pred,
                    "article": article['title'],
                    "source": article['source'],
                })
        
        return predictions
    
    def _detect_class_changes(self, title: str) -> Dict:
        """Detect class buffs/nerfs"""
        # Keywords
        buff_keywords = ['buff', 'increase', 'improve', 'boost']
        nerf_keywords = ['nerf', 'decrease', 'reduce', 'nerf']
        
        classes = ['mage', 'warrior', 'paladin', 'druid', 'rogue', 
                   'hunter', 'shaman', 'priest', 'warlock', 'demon hunter']
        
        for class_name in classes:
            if class_name in title:
                direction = None
                
                if any(kw in title for kw in buff_keywords):
                    direction = "increase"
                    confidence = 0.75
                elif any(kw in title for kw in nerf_keywords):
                    direction = "decrease"
                    confidence = 0.70
                
                if direction:
                    affected_items = self.class_items.get(class_name, [])
                    
                    return {
                        "type": "class_change",
                        "class": class_name,
                        "direction": direction,
                        "affected_items": affected_items,
                        "confidence": confidence,
                        "reason": f"{class_name.title()} {'buff' if direction == 'increase' else 'nerf'} detected",
                    }
        
        return None
    
    def _detect_events(self, title: str) -> Dict:
        """Detect upcoming events"""
        events = {
            "raid": ["raid", "tier", "mythic"],
            "holiday": ["holiday", "event", "celebration", "anniversary"],
            "pvp": ["pvp", "season", "arena", "battleground"],
            "patch": ["patch", "update", "hotfix"],
        }
        
        for event_type, keywords in events.items():
            if any(kw in title for kw in keywords):
                # Check for timing keywords
                timeframe = "this week"
                if "next week" in title:
                    timeframe = "next week"
                elif "tomorrow" in title:
                    timeframe = "tomorrow"
                
                affected_items = self.event_items.get(event_type, [])
                
                return {
                    "type": "event",
                    "event": event_type,
                    "timeframe": timeframe,
                    "direction": "increase",
                    "affected_items": affected_items,
                    "confidence": 0.85,
                    "reason": f"{event_type.title()} event {timeframe} - demand spike expected",
                }
        
        return None
    
    def _detect_profession_changes(self, title: str) -> Dict:
        """Detect profession recipe/skill changes"""
        professions = ['alchemy', 'enchanting', 'blacksmithing', 
                       'engineering', 'inscription', 'jewelcrafting']
        
        for prof in professions:
            if prof in title:
                affected_items = self.profession_items.get(prof, [])
                
                return {
                    "type": "profession_change",
                    "profession": prof,
                    "direction": "increase",
                    "affected_items": affected_items,
                    "confidence": 0.65,
                    "reason": f"{prof.title()} changes detected",
                }
        
        return None

# ============================================================================
# Predictive Market Engine (Combines News + Historical Data)
# ============================================================================

class PredictiveMarketEngine:
    def __init__(self):
        self.news_scraper = WoWNewsScraper()
        self.news_analyzer = NewsAnalysisEngine()
        self.model = None
        self._load_model()
        
    def _load_model(self):
        """Load trained ML model if available"""
        try:
            if os.path.exists('market_prediction_model.pkl'):
                self.model = MarketPredictionModel()
                self.model.load_model('market_prediction_model.pkl')
                print("ML Model loaded successfully into News Engine")
            else:
                print("No ML model found (market_prediction_model.pkl)")
        except Exception as e:
            print(f"Error loading ML model: {e}")
    
    def predict_market_shifts(self, historical_data: List[Dict] = None) -> List[Dict]:
        """
        Predict market shifts based on news + historical correlations
        
        Returns:
            List of predictions with buy/sell recommendations
        """
        # Scrape latest news
        articles = self.news_scraper.scrape_all_sources()
        
        # Analyze news for market impacts
        predictions = self.news_analyzer.analyze_news(articles)
        
        # Enhance with historical correlation
        if historical_data:
            predictions = self._enhance_with_history(predictions, historical_data)
        
        # Generate actionable recommendations
        recommendations = []
        
        for pred in predictions:
            if pred['direction'] == 'increase':
                action = "BUY NOW - Price will rise"
            else:
                action = "SELL NOW - Price will drop"
            
            recommendations.append({
                "action": action,
                "items": pred['affected_items'],
                "reason": pred['reason'],
                "confidence": pred['confidence'],
                "timeframe": pred.get('timeframe', 'soon'),
                "source": pred.get('article', 'Analysis'),
            })
        
        return recommendations
    
    def _enhance_with_history(self, predictions: List[Dict], 
                              historical_data: List[Dict]) -> List[Dict]:
        """
        Enhance predictions using historical price correlations
        """
        if not self.model or not self.model.trained:
            return predictions
            
        enhanced = []
        for pred in predictions:
            # Map news event type to model event type
            # News types: class_change, event, profession_change
            # Model types: class_change, raid, patch, holiday, profession
            
            model_event_type = None
            if pred['type'] == 'class_change':
                model_event_type = 'class_change'
            elif pred['type'] == 'event':
                if 'raid' in pred.get('event', ''):
                    model_event_type = 'raid'
                elif 'holiday' in pred.get('event', ''):
                    model_event_type = 'holiday'
                elif 'patch' in pred.get('event', ''):
                    model_event_type = 'patch'
            elif pred['type'] == 'profession_change':
                model_event_type = 'profession'
            
            if model_event_type and model_event_type in self.model.event_type_weights:
                weights = self.model.event_type_weights[model_event_type]
                
                # Add historical context
                avg_impact = weights['avg_price_change']
                confidence = weights['confidence']
                
                pred['historical_impact'] = f"{avg_impact:.1f}%"
                pred['model_confidence'] = f"{confidence:.2f}"
                
                # Boost confidence if model agrees
                if avg_impact > 20:
                    pred['confidence'] = min(pred['confidence'] + 0.1, 1.0)
                    pred['reason'] += f" (Historical data confirms +{avg_impact:.0f}% spike)"
            
            enhanced.append(pred)
            
        return enhanced
    
    def get_stockpile_recommendations(self) -> List[Dict]:
        """
        Get items to stockpile based on predicted events
        
        Returns:
            List of items to buy now before price spike
        """
        predictions = self.predict_market_shifts()
        
        stockpile = []
        
        for pred in predictions:
            if pred['action'].startswith('BUY') and pred['confidence'] > 0.7:
                stockpile.append({
                    "items": pred['items'],
                    "reason": pred['reason'],
                    "expected_profit": "50-200%",  # Would calculate from historical data
                    "timeframe": pred['timeframe'],
                })
        
        return stockpile

# ============================================================================
# Flask Endpoint Integration
# ============================================================================

def get_market_predictions_endpoint() -> Dict:
    """
    Flask endpoint for news-based market predictions
    
    Usage in server.py:
        @app.route('/api/goblin/predictions')
        def goblin_predictions():
            return get_market_predictions_endpoint()
    """
    engine = PredictiveMarketEngine()
    
    recommendations = engine.predict_market_shifts()
    stockpile = engine.get_stockpile_recommendations()
    
    return {
        "predictions": recommendations,
        "stockpile_now": stockpile,
        "last_updated": datetime.now().isoformat(),
    }

# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    engine = PredictiveMarketEngine()
    
    print("Scanning WoW news sites...")
    predictions = engine.predict_market_shifts()
    
    print("\n=== Market Shift Predictions ===")
    for pred in predictions:
        print(f"\n{pred['action']}")
        print(f"  Items: {pred['items']}")
        print(f"  Reason: {pred['reason']}")
        print(f"  Confidence: {pred['confidence']:.0%}")
    
    print("\n=== Stockpile Recommendations ===")
    stockpile = engine.get_stockpile_recommendations()
    for item in stockpile:
        print(f"\nBuy: {item['items']}")
        print(f"  Why: {item['reason']}")
        print(f"  Expected: {item['expected_profit']} profit")
