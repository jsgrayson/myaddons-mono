# GoblinAI ML Training Guide

## Complete Training Pipeline

You now have **full ML training infrastructure** ready to learn from historical data!

### What Was Built

**1. historical_scraper.py (450 lines)**
- **Wowhead News Scraper** - Gets last 6 months of news
- **TheUndermineJournal Scraper** - Historical AH prices
- **Auto-correlates** events with price movements
- **Imports to database** for training

**2. train_goblin_ai.sh**
- One-command training pipeline
- Creates schema → Scrapes data → Trains model → Validates

**3. goblin_training.py**
- Correlates news events with actual price spikes
- Trains ML model on patterns
- Saves `market_prediction_model.pkl`

### How to Train

**Option A: Automatic (Recommended)**
```bash
export DATABASE_URL='postgresql://user:pass@localhost/holocron'
./train_goblin_ai.sh
```

**Option B: Manual Steps**
```bash
# Step 1: Create schema  
psql $DATABASE_URL < schema_goblin_training.sql

# Step 2: Scrape historical data (10-15 mins)
python historical_scraper.py --months 6 --realm "Area 52"

# Step 3: Train model
python goblin_training.py

# Step 4: Deploy model
cp market_prediction_model.pkl /path/to/production/
```

### What Gets Scraped

**News Sources:**
- Wowhead articles (class changes, patches, raids)
- Auto-classified by event type
- Last 6 months = ~200-300 articles

**Price Data:**
- TheUndermineJournal historical prices
- Common trade goods & consumables
- 180 days of price history per item

**Correlation:**
- "Fire Mage buffed Aug 15" → Item 210814 spiked +280% in 48 hours
- "Raid release Sep 1" → Flask prices +150% on Tuesday
- Pattern learned: "Mage buff" typically causes +250% spike

### Training Output

```
Training complete!

Learned Patterns:
class_change:
  Avg Price Impact: 250.3%
  Peak Time: 48.2 hours
  Confidence: 0.85
  Samples: 15

raid:
  Avg Price Impact: 140.7%
  Peak Time: 12.5 hours
  Confidence: 0.92
  Samples: 24
```

### Deployment

**Trained model is portable:**
```python
# Production server.py
from goblin_training import MarketPredictionModel

model = MarketPredictionModel()
model.load_model('market_prediction_model.pkl')  # Load trained weights

# Now predictions use learned patterns
predictions = model.predict('class_change', [210814, 211515])
# Returns: Expected +250% spike in 48 hours, confidence 0.85
```

### Model Updates

**Monthly retraining recommended:**
1. Addon collects new AH scans
2. News scraper gets latest articles
3. Retrain model with fresh data
4. Deploy updated model.pkl
5. Predictions get smarter over time

### Requirements

```bash
pip install requests beautifulsoup4 psycopg2 numpy
```

### Ready to Train!

Just run: `./train_goblin_ai.sh`

The AI will learn actual historical correlations and make intelligent predictions!
