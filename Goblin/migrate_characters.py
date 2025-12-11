from backend.database import DatabaseManager
import os

def migrate():
    db = DatabaseManager()
    json_path = "shared_characters.json"
    if os.path.exists(json_path):
        print(f"Migrating characters from {json_path}...")
        db.migrate_characters_from_json(json_path)
        
        # Verify
        chars = db.get_all_characters()
        print(f"\nTotal characters in DB: {len(chars)}")
        for c in chars:
            print(f"- {c['name']} ({c['realm']}): Level {c['level']}, {c['gold']}g")
    else:
        print(f"File not found: {json_path}")

if __name__ == "__main__":
    migrate()
