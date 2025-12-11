#!/bin/bash
# Database Population Script for Holocron
# This script populates all necessary data for the application to function

set -e  # Exit on error

echo "🗄️  Populating Holocron Database..."

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL environment variable is not set"
    echo "Please set it with: export DATABASE_URL='postgresql://user:pass@localhost/dbname'"
    exit 1
fi

# Get database connection details
DB_URL=${DATABASE_URL}

echo "📊 Loading base schema..."
python3 -c "
import psycopg2
import os

conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
cur = conn.cursor()

# Load all schema files in order
schemas = [
    'schema.sql',
    'schema_phase3.sql',
    'schema_phase4.sql',
    'schema_phase5.sql',
    'schema_pathfinder.sql',
    'schema_codex.sql',
    'schema_diplomat.sql'
]

for schema_file in schemas:
    try:
        with open(schema_file, 'r') as f:
            print(f'  Loading {schema_file}...')
            cur.execute(f.read())
            conn.commit()
            print(f'  ✅ {schema_file} loaded')
    except Exception as e:
        print(f'  ⚠️  {schema_file}: {e}')

conn.close()
"

echo ""
echo "📝 Checking current data..."
python3 -c "
import psycopg2
import os

conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
cur = conn.cursor()

# Check Codex
try:
    cur.execute('SELECT count(*) FROM codex.quest_definitions')
    quests = cur.fetchone()[0]
    print(f'  Quest Definitions: {quests}')
    
    cur.execute('SELECT count(*) FROM codex.campaigns')
    campaigns = cur.fetchone()[0]
    print(f'  Campaigns: {campaigns}')
except Exception as e:
    print(f'  ⚠️  Codex tables: {e}')

# Check Pathfinder
try:
    cur.execute('SELECT count(*) FROM pathfinder.zones')
    zones = cur.fetchone()[0]
    print(f'  Pathfinder Zones: {zones}')
    
    cur.execute('SELECT count(*) FROM pathfinder.travel_nodes')
    nodes = cur.fetchone()[0]
    print(f'  Travel Nodes: {nodes}')
except Exception as e:
    print(f'  ⚠️  Pathfinder tables: {e}')

# Check Diplomat
try:
    cur.execute('SELECT count(*) FROM diplomat.factions')
    factions = cur.fetchone()[0]
    print(f'  Diplomat Factions: {factions}')
except Exception as e:
    print(f'  ⚠️  Diplomat tables: {e}')

# Check Characters
try:
    cur.execute('SELECT count(*) FROM holocron.characters')
    chars = cur.fetchone()[0]
    print(f'  Characters: {chars}')
except Exception as e:
    print(f'  ⚠️  Character table: {e}')

conn.close()
"

echo ""
echo "✅ Database population complete!"
echo ""
echo "📌 Next steps:"
echo "   1. Use the bridge.py script to import SavedVariables from WoW"
echo "   2. Or manually add character data via SQL"
echo "   3. Data will sync automatically from in-game addon"
