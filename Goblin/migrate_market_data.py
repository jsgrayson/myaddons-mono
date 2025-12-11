#!/usr/bin/env python3
"""
Migrate GoblinStack mock data from JSON to SQL database
"""

import json
import sys
import os

# Add backend to path
sys.path.insert(0, '/Users/jgrayson/Documents/goblin-clean-1')

from backend.database import DatabaseManager
import pandas as pd
from datetime import datetime

print("📚 Migrating GoblinStack mock data to SQL...")

# Initialize database
db = DatabaseManager(db_path='goblin_ai.db')

# Load mock market data
with open('market_data.json', 'r') as f:
    market_data = json.load(f)

items = market_data.get('items', [])
timestamp = int(datetime.now().timestamp())

print(f"Found {len(items)} market items to migrate")

# Convert to DataFrame format for database
records = []
for item in items:
    records.append({
        'item_id': item['item_id'],
        'price': item['current_price'],
        'quantity': item.get('volume_24h', 0),
        'timestamp': timestamp
    })

df = pd.DataFrame(records)

# Save to database
db.save_scan_data(df)

print(f"✅ Migrated {len(records)} market records to price_history table")

# Verify
print("\n📊 Database Status:")
import sqlite3
conn = sqlite3.connect('goblin_ai.db')
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM price_history")
total = cursor.fetchone()[0]
print(f"  Total price_history records: {total}")

cursor.execute("SELECT item_id, price, quantity FROM price_history LIMIT 5")
print(f"\n  Sample data:")
for row in cursor.fetchall():
    print(f"    Item {row[0]}: {row[1]}g, qty {row[2]}")

conn.close()

print("\n✅ GoblinStack database initialized and populated!")
