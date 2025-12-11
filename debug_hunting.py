import sqlite3

def debug_hunting():
    conn = sqlite3.connect('petweaver.db')
    cursor = conn.cursor()
    
    print("--- DEBUG HUNTING LOGIC ---")
    
    # 1. Unique pet names in strategies
    cursor.execute('''
        SELECT COUNT(DISTINCT pet_name) FROM (
            SELECT pet1_name as pet_name FROM strategies WHERE pet1_name IS NOT NULL AND pet1_name != ''
            UNION ALL
            SELECT pet2_name FROM strategies WHERE pet2_name IS NOT NULL AND pet2_name != ''
            UNION ALL
            SELECT pet3_name FROM strategies WHERE pet3_name IS NOT NULL AND pet3_name != ''
        )
    ''')
    strat_pets = cursor.fetchone()[0]
    print(f"Unique pets in strategies: {strat_pets}")
    
    # 2. How many match species table?
    cursor.execute('''
        SELECT COUNT(DISTINCT s.species_id) 
        FROM species s
        JOIN (
            SELECT pet1_name as pet_name FROM strategies WHERE pet1_name IS NOT NULL AND pet1_name != ''
            UNION ALL
            SELECT pet2_name FROM strategies WHERE pet2_name IS NOT NULL AND pet2_name != ''
            UNION ALL
            SELECT pet3_name FROM strategies WHERE pet3_name IS NOT NULL AND pet3_name != ''
        ) sp ON s.name = sp.pet_name
    ''')
    matched_species = cursor.fetchone()[0]
    print(f"Strategy pets matching species DB: {matched_species}")
    
    # 3. How many are owned?
    cursor.execute('SELECT COUNT(DISTINCT species_id) FROM pets')
    owned_species = cursor.fetchone()[0]
    print(f"Owned unique species: {owned_species}")
    
    # 4. The intersection (Strategy pets that are owned)
    cursor.execute('''
        SELECT COUNT(DISTINCT s.species_id) 
        FROM species s
        JOIN (
            SELECT pet1_name as pet_name FROM strategies WHERE pet1_name IS NOT NULL AND pet1_name != ''
            UNION ALL
            SELECT pet2_name FROM strategies WHERE pet2_name IS NOT NULL AND pet2_name != ''
            UNION ALL
            SELECT pet3_name FROM strategies WHERE pet3_name IS NOT NULL AND pet3_name != ''
        ) sp ON s.name = sp.pet_name
        WHERE s.species_id IN (SELECT species_id FROM pets)
    ''')
    owned_strat_pets = cursor.fetchone()[0]
    print(f"Strategy pets that are OWNED: {owned_strat_pets}")
    
    print(f"Missing strategy pets: {matched_species - owned_strat_pets}")

    if matched_species - owned_strat_pets == 0:
        print("\nCONCLUSION: You own every pet used in the strategies!")
    else:
        print("\nCONCLUSION: There should be missing pets showing up.")

if __name__ == "__main__":
    debug_hunting()
