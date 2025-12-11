import os
import psycopg2
import sys

db_url = os.environ.get('DATABASE_URL')
print(f"Testing connection to: {db_url}")

try:
    conn = psycopg2.connect(db_url, connect_timeout=5)
    print("Successfully connected!")
    cur = conn.cursor()
    cur.execute("SELECT 1")
    print("Query executed successfully.")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
    sys.exit(1)
