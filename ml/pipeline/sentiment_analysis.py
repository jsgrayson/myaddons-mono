"""
Sentiment Analysis Engine - Detect market hype from external sources
"""
import re
from typing import List, Dict
from loguru import logger

class SentimentAnalyzer:
    """
    Analyze text from external sources (Reddit, Wowhead, Twitch) to detect market sentiment.
    """
    
    def __init__(self):
        self.hype_keywords = {
            'bis': 2.0, 'best in slot': 2.0, 'op': 1.5, 'broken': 1.5,
            'gold cap': 1.2, 'insane': 1.2, 'huge': 1.1,
            'buy': 1.5, 'invest': 1.5, 'stock up': 1.5,
            'nerf': -1.5, 'trash': -1.5, 'useless': -1.5, 'dead': -2.0
        }
        
    def analyze_sentiment(self, text: str) -> float:
        """
        Calculate a sentiment score for a block of text.
        Range: -5.0 (Extremely Negative) to +5.0 (Extremely Positive)
        """
        score = 0.0
        text = text.lower()
        
        for keyword, weight in self.hype_keywords.items():
            # Count occurrences
            count = text.count(keyword)
            score += count * weight
            
        # Clamp score
        return max(-5.0, min(5.0, score))

    def detect_trends(self, posts: List[Dict]) -> List[Dict]:
        """
        Analyze a list of social media posts to find trending items.
        """
        item_scores = {}
        
        for post in posts:
            text = (post.get('title', '') + " " + post.get('body', '')).lower()
            sentiment = self.analyze_sentiment(text)
            
            # Extract potential item names (Mock extraction)
            # In production, match against a known item DB
            items = self._extract_items(text)
            
            for item in items:
                if item not in item_scores:
                    item_scores[item] = {'score': 0.0, 'mentions': 0}
                
                item_scores[item]['score'] += sentiment
                item_scores[item]['mentions'] += 1
                
        # Convert to list
        trends = []
        for item, data in item_scores.items():
            if data['mentions'] > 2: # Minimum mentions threshold
                trends.append({
                    'item_name': item,
                    'sentiment_score': round(data['score'], 2),
                    'mentions': data['mentions'],
                    'hype_level': self._get_hype_level(data['score'])
                })
                
        trends.sort(key=lambda x: x['sentiment_score'], reverse=True)
        return trends

    def _extract_items(self, text: str) -> List[str]:
        """Mock item extraction."""
        # Real implementation would use Aho-Corasick or similar string matching against item DB
        known_items = ['draconic augment rune', 'khaz algar ore', 'algari weaverline', 'null stone']
        found = []
        for item in known_items:
            if item in text:
                found.append(item)
        return found

    def _get_hype_level(self, score: float) -> str:
        if score > 10: return "INSANE HYPE"
        if score > 5: return "High Hype"
        if score > 2: return "Moderate Interest"
        if score < -5: return "Panic Selling"
        return "Neutral"

if __name__ == "__main__":
    # Test
    analyzer = SentimentAnalyzer()
    mock_posts = [
        {'title': "Draconic Augment Rune is BiS for everyone!", 'body': "You need to stock up now, it's insane."},
        {'title': "Null Stone drop rate is trash", 'body': "Don't farm this, it's useless waste of time."},
        {'title': "Investing in Khaz Algar Ore", 'body': "Prices are low, good time to buy."}
    ]
    
    trends = analyzer.detect_trends(mock_posts)
    print(trends)
