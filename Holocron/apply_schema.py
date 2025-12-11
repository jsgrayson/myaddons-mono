import psycopg2
import os

# Database connection parameters
# Using the URL found in .env
DB_URL = "postgresql://holocron:password@localhost:5432/holocron_db"

def apply_schema():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        with open("schema_phase4.sql", "r") as f:
            schema_sql = f.read()
            
        print("Applying schema_phase4.sql...")
        cur.execute(schema_sql)
        conn.commit()
        print("Schema applied successfully.")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error applying schema: {e}")

if __name__ == "__main__":
    apply_schema()
