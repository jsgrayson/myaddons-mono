import os
import psycopg2
import subprocess
import sys

# 1. Check Recipe Counts
print("--- Recipe Database Status ---")
try:
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM goblin.recipe_reference")
    total = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM goblin.recipe_reference WHERE materials IS NOT NULL")
    processed = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM goblin.recipe_reference WHERE materials IS NULL")
    remaining = cur.fetchone()[0]
    
    print(f"Total Recipes: {total}")
    print(f"Processed:     {processed}")
    print(f"Remaining:     {remaining}")
    print(f"Progress:      {(processed/total)*100:.1f}%")
    
    conn.close()
except Exception as e:
    print(f"DB Error: {e}")

# 2. Check SimC
print("\n--- SimC Binary Status ---")
simc_path = "/usr/local/bin/simc"
if os.path.exists(simc_path):
    real_path = os.path.realpath(simc_path)
    print(f"Symlink: {simc_path}")
    print(f"Target:  {real_path}")
    
    # Check quarantine status
    print("Checking quarantine status...")
    subprocess.run(["xattr", "-p", "com.apple.quarantine", real_path], capture_output=False)
else:
    print("SimC binary not found at /usr/local/bin/simc")
