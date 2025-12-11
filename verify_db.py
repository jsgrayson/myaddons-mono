import psycopg2
import os
import sys

# Default from start_all.sh
DEFAULT_DB_URL = 'postgresql://holocron:password@localhost:5432/holocron_db'
DB_URL = os.environ.get('DATABASE_URL', DEFAULT_DB_URL)

try:
    print(f"Connecting to {DB_URL}...")
    conn = psycopg2.connect(DB_URL)
    print("Successfully connected to database!")
    conn.close()
    sys.exit(0)
except Exception as e:
    print(f"Failed to connect: {e}")
    sys.exit(1)
