import os
import psycopg2
import json

def verify_data():
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cur = conn.cursor()
        
        print("📊 Recipe Data Verification")
        print("===========================")
        
        # 1. Overall Counts
        cur.execute("SELECT COUNT(*) FROM goblin.recipe_reference")
        total = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM goblin.recipe_reference WHERE materials IS NOT NULL")
        with_mats = cur.fetchone()[0]
        
        print(f"Total Recipes:    {total}")
        print(f"With Materials:   {with_mats}")
        print(f"Completion Rate:  {(with_mats/total)*100:.1f}%")
        print("-" * 30)
        
        # 2. Profession Distribution
        print("\n📚 Recipes by Profession:")
        cur.execute("""
            SELECT profession_name, COUNT(*), COUNT(materials) 
            FROM goblin.recipe_reference 
            GROUP BY profession_name 
            ORDER BY COUNT(*) DESC
        """)
        for row in cur.fetchall():
            prof, count, completed = row
            print(f"  {prof:20} : {completed}/{count}")
            
        # 3. Sample Data
        print("\n🔍 Sample Recipe Data:")
        cur.execute("""
            SELECT recipe_name, profession_name, materials 
            FROM goblin.recipe_reference 
            WHERE materials IS NOT NULL 
            ORDER BY RANDOM() 
            LIMIT 3
        """)
        for row in cur.fetchall():
            name, prof, mats = row
            print(f"\n  Recipe: {name} ({prof})")
            print(f"  Materials: {json.dumps(mats, indent=2)}")

        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_data()
