"""
Database Manager - SQLite/PostgreSQL integration for long-term storage
"""
import sqlite3
import pandas as pd
from loguru import logger
import os
import json
from typing import List, Dict, Optional

class DatabaseManager:
    """
    Manages database connections and schema.
    Defaults to SQLite for ease of use, but structure supports PostgreSQL.
    """
    
    def __init__(self, db_path: str = "goblin_ai.db"):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Price History Table
        c.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                price INTEGER,
                quantity INTEGER,
                timestamp INTEGER
            )
        ''')
        
        # Predictions Table
        c.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                predicted_price INTEGER,
                confidence REAL,
                timestamp INTEGER,
                target_date INTEGER
            )
        ''')
        
        # Transactions Table (Accounting)
        c.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                type TEXT, -- BUY or SELL
                price INTEGER,
                quantity INTEGER,
                timestamp INTEGER,
                character TEXT
            )
        ''')

        # Characters Table
        c.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                realm TEXT,
                faction TEXT,
                level INTEGER,
                gold INTEGER,
                professions TEXT, -- JSON string
                updated_at INTEGER,
                UNIQUE(name, realm)
            )
        ''')

        # SkillWeaver: Builds Table
        c.execute('''
            CREATE TABLE IF NOT EXISTS builds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER,
                name TEXT NOT NULL,
                talent_string TEXT,
                rotation_settings TEXT, -- JSON blob
                is_active BOOLEAN DEFAULT 0,
                created_at INTEGER,
                FOREIGN KEY(character_id) REFERENCES characters(id)
            )
        ''')

        # SkillWeaver: Gear Sets Table
        c.execute('''
            CREATE TABLE IF NOT EXISTS gear_sets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER,
                name TEXT NOT NULL,
                items TEXT, -- JSON blob
                stats_snapshot TEXT, -- JSON blob
                sim_dps REAL,
                created_at INTEGER,
                FOREIGN KEY(character_id) REFERENCES characters(id)
            )
        ''')

        # SkillWeaver: Simulation Results Table
        c.execute('''
            CREATE TABLE IF NOT EXISTS sim_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                build_id INTEGER,
                gear_set_id INTEGER,
                dps REAL,
                hps REAL,
                report_url TEXT,
                timestamp INTEGER,
                FOREIGN KEY(build_id) REFERENCES builds(id),
                FOREIGN KEY(gear_set_id) REFERENCES gear_sets(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")

    def save_scan_data(self, df: pd.DataFrame):
        """Save scan data to DB."""
        conn = sqlite3.connect(self.db_path)
        try:
            # Ensure columns match
            df_to_save = df[['item_id', 'price', 'quantity', 'timestamp']].copy()
            df_to_save.to_sql('price_history', conn, if_exists='append', index=False)
            logger.info(f"Saved {len(df)} records to price_history.")
        except Exception as e:
            logger.error(f"Error saving scan data: {e}")
        finally:
            conn.close()

    def get_price_history(self, item_id: int, limit: int = 100) -> pd.DataFrame:
        """Fetch price history for an item."""
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM price_history WHERE item_id = {item_id} ORDER BY timestamp DESC LIMIT {limit}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def save_prediction(self, predictions: List[Dict]):
        """Save predictions."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            for p in predictions:
                c.execute('''
                    INSERT INTO predictions (item_id, predicted_price, confidence, timestamp, target_date)
                    VALUES (?, ?, ?, ?, ?)
                ''', (p['item_id'], p['price'], p['confidence'], p['timestamp'], p['target_date']))
            conn.commit()
        finally:
            conn.close()

    def get_latest_predictions(self, limit: int = 50) -> List[Dict]:
        """Get latest predictions."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM predictions 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    # Character Methods
    def add_character(self, char_data: Dict) -> Dict:
        """Add or update a character."""
        conn = sqlite3.connect(self.db_path)
        try:
            c = conn.cursor()
            import time
            import json
            
            c.execute('''
                INSERT OR REPLACE INTO characters 
                (name, realm, faction, level, gold, professions, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                char_data['name'],
                char_data['realm'],
                char_data['faction'],
                char_data['level'],
                char_data['gold'],
                json.dumps(char_data['professions']),
                int(time.time())
            ))
            conn.commit()
            return char_data
        finally:
            conn.close()

    def get_character(self, name: str, realm: str) -> Optional[Dict]:
        """Get a character by name and realm."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            c = conn.cursor()
            c.execute('SELECT * FROM characters WHERE name = ? AND realm = ?', (name, realm))
            row = c.fetchone()
            if row:
                d = dict(row)
                d['professions'] = json.loads(d['professions']) if d['professions'] else []
                return d
            return None
        finally:
            conn.close()

    def get_all_characters(self) -> List[Dict]:
        """Get all characters."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            c = conn.cursor()
            c.execute('SELECT * FROM characters')
            chars = []
            for row in c.fetchall():
                d = dict(row)
                d['professions'] = json.loads(d['professions']) if d['professions'] else []
                chars.append(d)
            return chars
        finally:
            conn.close()

    # SkillWeaver Methods
    def save_build(self, character_id: int, name: str, talent_string: str, rotation_settings: Dict) -> int:
        """Save a talent build."""
        conn = sqlite3.connect(self.db_path)
        try:
            c = conn.cursor()
            import time
            import json
            
            c.execute('''
                INSERT INTO builds (character_id, name, talent_string, rotation_settings, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (character_id, name, talent_string, json.dumps(rotation_settings), int(time.time())))
            conn.commit()
            return c.lastrowid
        finally:
            conn.close()

    def get_builds(self, character_id: int) -> List[Dict]:
        """Get builds for a character."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            c = conn.cursor()
            c.execute('SELECT * FROM builds WHERE character_id = ? ORDER BY created_at DESC', (character_id,))
            builds = []
            for row in c.fetchall():
                d = dict(row)
                d['rotation_settings'] = json.loads(d['rotation_settings']) if d['rotation_settings'] else {}
                builds.append(d)
            return builds
        finally:
            conn.close()

    def save_gear_set(self, character_id: int, name: str, items: Dict, stats: Dict, sim_dps: float) -> int:
        """Save a gear set."""
        conn = sqlite3.connect(self.db_path)
        try:
            c = conn.cursor()
            import time
            import json
            
            c.execute('''
                INSERT INTO gear_sets (character_id, name, items, stats_snapshot, sim_dps, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (character_id, name, json.dumps(items), json.dumps(stats), sim_dps, int(time.time())))
            conn.commit()
            return c.lastrowid
        finally:
            conn.close()

    def get_gear_sets(self, character_id: int) -> List[Dict]:
        """Get gear sets for a character."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            c = conn.cursor()
            c.execute('SELECT * FROM gear_sets WHERE character_id = ? ORDER BY sim_dps DESC', (character_id,))
            sets = []
            for row in c.fetchall():
                d = dict(row)
                d['items'] = json.loads(d['items']) if d['items'] else {}
                d['stats_snapshot'] = json.loads(d['stats_snapshot']) if d['stats_snapshot'] else {}
                sets.append(d)
            return sets
        finally:
            conn.close()

    def migrate_characters_from_json(self, json_path: str):
        """Migrate characters from JSON to DB."""
        if not os.path.exists(json_path):
            logger.warning(f"Character file not found: {json_path}")
            return
            
        try:
            import json # Ensure json is imported for this method
            with open(json_path, 'r') as f:
                data = json.load(f)
                
            characters = data.get('characters', [])
            count = 0
            for char in characters:
                self.add_character({
                    'name': char['name'],
                    'realm': char['realm'],
                    'faction': 'Unknown', # Default
                    'level': char['level'],
                    'gold': char['gold'],
                    'professions': [] # Default
                })
                count += 1
            logger.info(f"Migrated {count} characters from {json_path}")
        except Exception as e:
            logger.error(f"Character migration failed: {e}")

    def migrate_from_csv(self, csv_path: str):
        """One-time migration from CSV to DB."""
        if os.path.exists(csv_path):
            logger.info(f"Migrating {csv_path} to database...")
            df = pd.read_csv(csv_path)
            # Rename columns if needed to match schema
            # df = df.rename(columns={'marketValue': 'price'}) 
            self.save_scan_data(df)
            logger.success("Migration complete.")

if __name__ == "__main__":
    # Test
    db = DatabaseManager()
    # Mock data
    mock_df = pd.DataFrame({
        'item_id': [123, 456],
        'price': [1000, 5000],
        'quantity': [10, 5],
        'timestamp': [1700000000, 1700000000]
    })
    db.save_scan_data(mock_df)
    print(db.get_price_history(123))
