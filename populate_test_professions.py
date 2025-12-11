import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://jgrayson@localhost/holocron')

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def populate_professions():
    conn = get_db_connection()
    if not conn:
        return

    cur = conn.cursor()
    
    # Test data: Character Name -> [(Profession, Skill)]
    # Note: We need to look up the GUIDs first
    test_data = {
        "Vaxo": [("Leatherworking", 100), ("Skinning", 100)],
        "Bronha": [("Blacksmithing", 100), ("Mining", 100)],
        "Slaythe": [("Alchemy", 100), ("Herbalism", 100)],
        "Vacco": [("Tailoring", 100), ("Enchanting", 100)]
    }

    print("📊 Populating test professions...")

    try:
        for char_name, professions in test_data.items():
            # Get GUID
            cur.execute("SELECT character_guid FROM holocron.characters WHERE name = %s", (char_name,))
            row = cur.fetchone()
            
            if not row:
                print(f"⚠️  Character {char_name} not found, skipping.")
                continue
                
            char_guid = row[0]
            
            for prof_name, skill in professions:
                # Insert profession
                cur.execute("""
                    INSERT INTO goblin.professions 
                    (character_guid, profession_name, skill_level, max_skill)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (character_guid, profession_name) 
                    DO UPDATE SET skill_level = EXCLUDED.skill_level
                """, (char_guid, prof_name, skill, 100))
                
                print(f"✅ Added {prof_name} ({skill}) to {char_name}")

        conn.commit()
        print("\n🎉 Profession population complete!")

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    populate_professions()
