import sqlite3

DB_FILE = "/Users/jgrayson/Documents/holocron/holocron.db"

def migrate():
    print("Migrating Codex Schema...")
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    
    try:
        # Check if columns exist
        cur.execute("PRAGMA table_info(quest_definitions)")
        columns = [info[1] for info in cur.fetchall()]
        
        if "category_id" not in columns:
            print("Adding category_id column...")
            cur.execute("ALTER TABLE quest_definitions ADD COLUMN category_id INTEGER")
            
        if "category_name" not in columns:
            print("Adding category_name column...")
            cur.execute("ALTER TABLE quest_definitions ADD COLUMN category_name TEXT")
            
        conn.commit()
        print("✅ Migration complete.")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
