"""
News Sentiment Analysis - Predict market shifts from WoW news and patch notes
"""
import os
import json
import requests
from datetime import datetime, timedelta
from loguru import logger
from typing import List, Dict, Any
import re

class NewsAnalyzer:
    """Analyze WoW news to predict market trends."""
    
    def __init__(self):
        self.cache_dir = os.path.join(os.path.dirname(__file__), "../data/news")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.news_sources = {
            "wowhead": "https://www.wowhead.com/news",
            "blizzard": "https://worldofwarcraft.blizzard.com/en-us/news"
        }
        
    def scrape_wowhead_news(self, days: int = 30) -> List[Dict]:
        """Scrape recent news from Wowhead."""
        cache_file = os.path.join(self.cache_dir, "wowhead_news.json")
        
        # Check cache (refresh daily)
        if os.path.exists(cache_file):
            mod_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if datetime.now() - mod_time < timedelta(days=1):
                logger.info("Loading cached Wowhead news")
                with open(cache_file, 'r') as f:
                    return json.load(f)
        
        logger.info("Scraping Wowhead news...")
        # In production, would use BeautifulSoup to scrape
        # For now, return placeholder structure
        news_items = [
            {
                "source": "wowhead",
                "title": "Patch 10.2: Class Balance Changes",
                "date": (datetime.now() - timedelta(days=5)).isoformat(),
                "content": "Holy Paladin healing increased 15%. Protection Warrior defensives buffed.",
                "url": "https://www.wowhead.com/news/patch-10-2-class-changes"
            }
        ]
        
        with open(cache_file, 'w') as f:
            json.dump(news_items, f, indent=2)
        
        return news_items
    
    def extract_mentions(self, news_item: Dict) -> Dict[str, Any]:
        """Extract class/spec/item mentions from news."""
        text = f"{news_item['title']} {news_item['content']}".lower()
        
        # Classes
        classes = ["paladin", "warrior", "mage", "priest", "warlock", "hunter", 
                  "rogue", "druid", "shaman", "monk", "demon hunter", "death knight", "evoker"]
        
        # Specs (examples)
        specs = ["holy", "protection", "retribution", "arms", "fury", "fire", "frost", "arcane"]
        
        # Buff/nerf keywords
        buff_keywords = ["buff", "increase", "improved", "stronger", "boost"]
        nerf_keywords = ["nerf", "decrease", "reduced", "weaker", "nerf"]
        
        mentions = {
            "classes": [cls for cls in classes if cls in text],
            "specs": [spec for spec in specs if spec in text],
            "is_buff": any(kw in text for kw in buff_keywords),
            "is_nerf": any(kw in text for kw in nerf_keywords)
        }
        
        return mentions
    
    def predict_market_impact(self, mentions: Dict, historical_data: Dict = None) -> Dict[str, Any]:
        """Predict which items will spike based on news."""
        predictions = []
        
        # Simple rule-based predictions (in production, use ML on historical correlations)
        if mentions['is_buff']:
            for cls in mentions['classes']:
                for spec in mentions['specs']:
                    # Predict gear for this class/spec will spike
                    predictions.append({
                        "category": f"{cls.capitalize()} {spec.capitalize()} gear",
                        "prediction": "price_spike",
                        "confidence": 0.75,
                        "expected_change": "+150% to +200%",
                        "timeline": "2-3 weeks after patch release",
                        "reason": f"{cls.capitalize()} {spec} buffed - higher demand expected"
                    })
        
        if mentions['is_nerf']:
            for cls in mentions['classes']:
                predictions.append({
                    "category": f"{cls.capitalize()} gear",
                    "prediction": "price_drop",
                    "confidence": 0.60,
                    "expected_change": "-20% to -40%",
                    "timeline": "1-2 weeks after patch",
                    "reason": f"{cls.capitalize()} nerfed - lower demand expected"
                })
        
        return {
            "predictions": predictions,
            "total_opportunities": len([p for p in predictions if p['prediction'] == 'price_spike'])
        }
    
    def generate_actionable_recommendations(self, predictions: Dict) -> List[Dict]:
        """Convert predictions into buy/sell recommendations."""
        recommendations = []
        
        for pred in predictions.get('predictions', []):
            if pred['prediction'] == 'price_spike':
                recommendations.append({
                    "action": "BUY",
                    "category": pred['category'],
                    "timing": "NOW (before patch)",
                    "expected_roi": pred['expected_change'],
                    "timeline": pred['timeline'],
                    "confidence": pred['confidence'],
                    "strategy": f"Buy {pred['category']} at current prices, hold until patch release, sell at peak"
                })
            elif pred['prediction'] == 'price_drop':
                recommendations.append({
                    "action": "SELL",
                    "category": pred['category'],
                    "timing": "ASAP (before price drops)",
                    "expected_loss_avoided": pred['expected_change'],
                    "timeline": pred['timeline'],
                    "confidence": pred['confidence'],
                    "strategy": f"Liquidate {pred['category']} inventory now to avoid losses"
                })
        
        return recommendations
    
    def analyze_recent_news(self, days: int = 30) -> Dict[str, Any]:
        """Full analysis pipeline."""
        logger.info(f"Analyzing news from last {days} days...")
        
        # Scrape news
        news_items = self.scrape_wowhead_news(days)
        
        all_predictions = []
        all_recommendations = []
        
        for item in news_items:
            # Extract mentions
            mentions = self.extract_mentions(item)
            
            if mentions['classes'] or mentions['specs']:
                # Predict impact
                impact = self.predict_market_impact(mentions)
                
                # Generate recommendations
                recommendations = self.generate_actionable_recommendations(impact)
                
                all_predictions.extend(impact.get('predictions', []))
                all_recommendations.extend(recommendations)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "news_items_analyzed": len(news_items),
            "predictions": all_predictions,
            "recommendations": all_recommendations,
            "summary": {
                "buy_opportunities": len([r for r in all_recommendations if r['action'] == 'BUY']),
                "sell_warnings": len([r for r in all_recommendations if r['action'] == 'SELL'])
            }
        }
        
        # Save results
        output_path = os.path.join(self.cache_dir, "news_analysis.json")
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        logger.success(f"News analysis complete. {result['summary']['buy_opportunities']} opportunities found.")
        return result

if __name__ == "__main__":
    analyzer = NewsAnalyzer()
    result = analyzer.analyze_recent_news()
    
    print("\n" + "="*60)
    print("NEWS SENTIMENT ANALYSIS")
    print("="*60)
    print(f"\nBuy Opportunities: {result['summary']['buy_opportunities']}")
    print(f"Sell Warnings: {result['summary']['sell_warnings']}")
    
    if result['recommendations']:
        print("\nTop Recommendations:")
        for i, rec in enumerate(result['recommendations'][:5], 1):
            print(f"\n{i}. {rec['action']}: {rec['category']}")
            print(f"   Timing: {rec['timing']}")
            print(f"   Expected ROI: {rec.get('expected_roi', rec.get('expected_loss_avoided'))}")
