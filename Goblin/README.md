# Goblin - WoW AI Gold Making System

An end-to-end AI-powered gold-making system for World of Warcraft that ingests real auction house data, trains machine learning models, and identifies profitable flip opportunities.

## Features

- **Live Data Ingestion**: Connects to Blizzard's official API to fetch real-time auction house data
- **ML Price Prediction**: Random Forest model predicts fair market value for items
- **Opportunity Detection**: Automatically identifies items selling below predicted value
- **Docker-Ready**: Fully containerized for easy deployment to Proxmox or any Docker host
- **Modular Architecture**: Independent agents for different tasks (TSM Brain, Warden, AH Runner)

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (for production)
- Blizzard API credentials ([Get them here](https://develop.battle.net/access/clients))

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd goblin-project
   ```

2. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configure secrets**
   ```bash
   # Add your Blizzard API credentials
   nano backend/config/secrets.env
   ```

4. **Run the ML pipeline**
   ```bash
   # Fetch latest auction data
   python3 -m ml.pipeline.ingest
   
   # Preprocess data (requires multiple snapshots)
   python3 -m ml.pipeline.preprocess
   
   # Train the model
   python3 -m ml.pipeline.train
   
   # Generate predictions
   python3 -m ml.pipeline.predict
   ```

### Docker Deployment

See [`deployment_guide.md`](/.gemini/antigravity/brain/7628bec8-0298-44ab-a031-0ed9d5b035b2/deployment_guide.md) for full Proxmox deployment instructions.

```bash
docker-compose up -d --build
```

## Project Structure

```
goblin-project/
├── backend/          # FastAPI backend
│   ├── config/       # Configuration files
│   └── agents/       # Agent modules
├── ml/               # Machine Learning pipeline
│   ├── pipeline/     # Data processing scripts
│   ├── models/       # Trained models
│   └── data/         # Raw and processed data
├── scripts/          # Utility scripts
└── docker-compose.yml
```

## How It Works

1. **Data Collection**: Hourly snapshots of auction house data via Blizzard API
2. **Feature Engineering**: Calculate moving averages, volatility, and price trends
3. **Model Training**: Random Forest Regressor learns item price patterns
4. **Prediction**: Identifies items currently undervalued by 20%+ compared to predicted fair value
5. **Action**: Outputs JSON reports for manual review or automated trading

## Configuration

- **Realm**: Configured in `backend/config/core.yaml` (default: Dalaran-US, Alliance)
- **API Keys**: Stored in `backend/config/secrets.env` (gitignored)
- **Model Parameters**: Adjustable in `ml/pipeline/train.py`

## Next Steps

- Set up automated data ingestion (cron job)
- Configure Discord webhook for opportunity alerts
- Implement agent trading automation
- Expand to multiple realms/factions

## License

MIT
