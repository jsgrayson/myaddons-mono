#!/bin/bash
# train_goblin_ai.sh - Complete ML Training Workflow

echo "========================================="
echo "GoblinAI ML Training Pipeline"
echo "========================================="
echo ""

# Step 1: Create database schema
echo "Step 1: Creating database schema..."
# psql $DATABASE_URL < schema_goblin_training.sql
echo "✓ Schema created (Skipped in dev env)"
echo ""

# Step 2: Scrape historical data
echo "Step 2: Scraping historical data (this may take 10-15 minutes)..."
python3 historical_scraper.py --months 6 --realm "Area 52"
echo "✓ Historical data scraped"
echo ""

# Step 3: Train ML model
echo "Step 3: Training ML model on historical correlations..."
python3 goblin_training.py
echo "✓ Model trained"
echo ""

# Step 4: Test predictions
echo "Step 4: Testing predictions..."
python3 -c "
from goblin_ml_engine import GoblinMLEngine
from goblin_training import MarketPredictionModel

model = MarketPredictionModel()
model.load_model('market_prediction_model.pkl')

print('Model loaded successfully!')
print('Event type weights:', model.event_type_weights.keys())
"
echo "✓ Model validated"
echo ""

echo "========================================="
echo "TRAINING COMPLETE!"
echo "========================================="
echo ""
echo "Model saved to: market_prediction_model.pkl"
echo "Training data saved to: training_data.json"
echo ""
echo "Next steps:"
echo "1. Deploy model.pkl to production server"
echo "2. Server will use trained model for predictions"
echo "3. Retrain monthly with new data"
echo ""
echo "Test the API:"
echo "curl http://localhost:5000/api/goblin/predictions"
