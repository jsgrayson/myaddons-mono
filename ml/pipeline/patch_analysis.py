"""
Patch Analysis - Predict market shifts from game updates
"""
import re
from typing import List, Dict
from loguru import logger

class PatchAnalyzer:
    """Analyze patch notes and game updates for market impacts."""
    
    def __init__(self):
        self.keywords = {
            'buff': {'sentiment': 'positive', 'impact': 'high'},
            'nerf': {'sentiment': 'negative', 'impact': 'high'},
            'new recipe': {'sentiment': 'positive', 'impact': 'medium'},
            'drop rate increased': {'sentiment': 'negative', 'impact': 'medium'}, # Supply up, price down
            'drop rate decreased': {'sentiment': 'positive', 'impact': 'medium'}, # Supply down, price up
            'removed': {'sentiment': 'positive', 'impact': 'extreme'}, # Unobtainable
        }
        
    def analyze_text(self, text: str) -> List[Dict]:
        """
        Analyze text (patch notes) for market signals.
        """
        signals = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.lower()
            for keyword, info in self.keywords.items():
                if keyword in line:
                    # Found a signal
                    signal = {
                        'keyword': keyword,
                        'sentiment': info['sentiment'],
                        'impact': info['impact'],
                        'context': line.strip(),
                        'affected_items': self._extract_items(line)
                    }
                    signals.append(signal)
                    
        return signals

    def _extract_items(self, text: str) -> List[str]:
        """
        Extract item names from text.
        In a real system, this would use Named Entity Recognition (NER) or a database lookup.
        """
        # Placeholder: Look for capitalized words in the original text (passed as lower here, so this is mock)
        # Real implementation would need the original case text or a list of known items
        return [] 

    def predict_impact(self, signals: List[Dict]) -> List[Dict]:
        """
        Convert signals into specific market predictions.
        """
        predictions = []
        
        for signal in signals:
            if signal['sentiment'] == 'positive':
                action = 'BUY/HOLD'
                reason = f"Positive update: {signal['keyword']}"
            else:
                action = 'SELL'
                reason = f"Negative update: {signal['keyword']}"
                
            predictions.append({
                'signal': signal,
                'action': action,
                'reason': reason,
                'confidence': 0.7 # Base confidence for text analysis
            })
            
        return predictions

if __name__ == "__main__":
    # Example
    analyzer = PatchAnalyzer()
    notes = """
    - Draconic Augment Rune drop rate increased in LFR.
    - Nerfed damage of Shadowmourne.
    - Added new recipe: Feast of the Divine Day.
    """
    
    signals = analyzer.analyze_text(notes)
    preds = analyzer.predict_impact(signals)
    
    for p in preds:
        print(f"Action: {p['action']} | Reason: {p['reason']} | Context: {p['signal']['context']}")
