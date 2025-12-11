# Database Setup Complete

## PostgreSQL Installation
- ✅ Installed PostgreSQL@14 via Homebrew
- ✅ Initialized default database cluster
- ✅ Started PostgreSQL service (auto-starts on login)

## Database Creation
- ✅ Created `holocron` database
- ✅ Loaded core schema (`schema.sql`)
  - Created schemas: `holocron`, `goblin`, `skillweaver`, `petweaver`
  - Created tables: `characters`, `storage_locations`, `items`, `gear`, `professions`, `recipes`, `profiles`
  - Created indexes for optimized searching

## Sample Data
- ✅ Inserted 4 sample characters with specs and item levels:
  - Thunderfist (Shaman - Enhancement - ilvl 489)
  - Shadowmend (Priest - Shadow - ilvl 476)
  - Moonfire (Druid - Balance - ilvl 492)
  - Firestorm (Mage - Fire - ilvl 485)

## Configuration
- ✅ Created `.env` file with `DATABASE_URL`
- ✅ Updated `start_servers_background.sh` to export `DATABASE_URL`
- ✅ Connection verified: `postgresql://jgrayson@localhost/holocron`

## Next Steps
1. Run `bridge.py` to import real WoW addon data from SavedVariables
2. Navigate to SkillWeaver dashboard to see live character data
3. Set up additional schemas as needed (pathfinder, codex, diplomat, etc.)

## Database Access
```bash
# Connect to database
psql holocron

# View characters
SELECT name, class, spec, item_level FROM holocron.characters;

# Restart servers with DB access
./start_servers_background.sh
```
