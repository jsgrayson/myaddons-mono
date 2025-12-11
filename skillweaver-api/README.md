# SkillWeaver API

FastAPI backend for character optimization and talent planning.

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your Blizzard API credentials

# Run server
uvicorn app.main:app --reload
```

## API Endpoints

- `GET /` - Health check
- `GET /api/auth/login` - Get Blizzard OAuth URL
- `GET /api/auth/callback` - OAuth callback handler
- `POST /api/characters/import` - Import character from Blizzard API
- `GET /api/talents/recommend/{spec_id}/{content_type}` - Get talent recommendations
- `GET /api/gear/stat-weights/{spec_id}/{content_type}` - Get stat weights
- `POST /api/integration/sync-to-goblin` - Sync character to Goblin AI

## Documentation

Interactive API docs available at `/docs` when running locally.
