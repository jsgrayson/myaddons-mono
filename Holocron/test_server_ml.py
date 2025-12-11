import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from goblin_news_engine import get_market_predictions_endpoint
    
    print("Testing Market Predictions Endpoint...")
    result = get_market_predictions_endpoint()
    
    print("\nPredictions generated successfully!")
    print(f"Count: {len(result['predictions'])}")
    
    for pred in result['predictions']:
        print(f"\nPrediction: {pred['reason']}")
        if 'historical_impact' in pred:
            print(f"  Historical Impact: {pred['historical_impact']}")
            print(f"  Model Confidence: {pred['model_confidence']}")
        else:
            print("  (No historical data match)")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
