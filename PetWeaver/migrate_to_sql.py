#!/usr/bin/env python3
"""
PetWeaver Database Migration Script
Migrates all JSON data to SQLite database for better performance
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path

# Color output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.ENDC}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.ENDC}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.ENDC}")

def print_info(msg):
    print(f"{Colors.CYAN}ℹ️  {msg}{Colors.ENDC}")

def create_database():
    """Create SQLite database and schema"""
    print_info("Creating database schema...")
    
    conn = sqlite3.connect('petweaver.db')
    cursor = conn.cursor()
    
    # Read and execute schema
    with open('schema.sql', 'r') as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)
    
    conn.commit()
    print_success("Database schema created")
    return conn

def migrate_pet_collection(conn):
    """Migrate my_pets.json to pets table"""
    if not os.path.exists('my_pets.json'):
        print_warning("my_pets.json not found, skipping...")
        return
    
    print_info("Migrating pet collection...")
    
    with open('my_pets.json', 'r') as f:
        data = json.load(f)
    
    pets = data.get('pets', [])
    cursor = conn.cursor()
    
    # Quality type mapping 
    quality_map = {
        'POOR': 1,
        'COMMON': 2,
        'UNCOMMON': 3,
        'RARE': 4,
        'EPIC': 5,
        'LEGENDARY': 6
    }
    
    count = 0
    for pet in pets:
        # Extract species info
        species_data = pet.get('species', {})
        species_id = species_data.get('id')
        species_name_obj = species_data.get('name', {})
        name = species_name_obj.get('en_US', 'Unknown') if isinstance(species_name_obj, dict) else 'Unknown'
        
        # Extract quality - handle both old and new API formats
        quality_data = pet.get('quality', {})
        if isinstance(quality_data, dict):
            quality = quality_map.get(quality_data.get('type', 'COMMON'), 2)
        else:
            quality = quality_data or 1
        
        # Extract stats
        stats = pet.get('stats', {})
        
        cursor.execute('''
            INSERT INTO pets (species_id, name, level, quality, breed_id, health, power, speed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            species_id,
            name,
            pet.get('level', 1),
            quality,
            stats.get('breed_id'),
            stats.get('health'),
            stats.get('power'),
            stats.get('speed')
        ))
        count += 1
    
    conn.commit()
    print_success(f"Migrated {count} pets")

def migrate_strategies(conn):
    """Migrate strategies.json to strategies table"""
    if not os.path.exists('strategies.json'):
        print_warning("strategies.json not found, skipping...")
        return
    
    print_info("Migrating strategies...")
    
    with open('strategies.json', 'r') as f:
        data = json.load(f)
    
    cursor = conn.cursor()
    count = 0
    
    for expansion, categories in data.items():
        for category, encounters in categories.items():
            for encounter in encounters:
                encounter_name = encounter.get('encounter_name', 'Unknown')
                
                for strategy in encounter.get('strategies', []):
                    team = strategy.get('team', [])
                    cursor.execute('''
                        INSERT INTO strategies (
                            encounter_id, encounter_name, expansion, category,
                            pet1_name, pet2_name, pet3_name, win_rate, script
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        encounter.get('npc_id', 0),
                        encounter_name,
                        expansion,
                        category,
                        team[0] if len(team) > 0 else None,
                        team[1] if len(team) > 1 else None,
                        team[2] if len(team) > 2 else None,
                        strategy.get('win_rate', 0.0),
                        strategy.get('script', '')
                    ))
                    count += 1
    
    conn.commit()
    print_success(f"Migrated {count} strategies")

def migrate_ready_strategies(conn):
    """Migrate my_ready_strategies.json to ready_strategies table"""
    if not os.path.exists('my_ready_strategies.json'):
        print_warning("my_ready_strategies.json not found, skipping...")
        return
    
    print_info("Migrating ready strategies...")
    
    with open('my_ready_strategies.json', 'r') as f:
        data = json.load(f)
    
    cursor = conn.cursor()
    count = 0
    
    for expansion, encounters in data.items():
        for encounter_list in encounters.values():
            for encounter in encounter_list:
                # Find matching strategy in strategies table
                encounter_name = encounter.get('encounter_name')
                cursor.execute('''
                    SELECT strategy_id FROM strategies 
                    WHERE encounter_name = ? 
                    LIMIT 1
                ''', (encounter_name,))
                
                result = cursor.fetchone()
                if result:
                    strategy_id = result[0]
                    cursor.execute('''
                        INSERT INTO ready_strategies (strategy_id, is_complete, priority)
                        VALUES (?, 1, ?)
                    ''', (strategy_id, count % 10))  # Simple priority based on order
                    count += 1
    
    conn.commit()
    print_success(f"Migrated {count} ready strategies")

def create_indexes(conn):
    """Ensure all indexes are created for performance"""
    print_info("Creating performance indexes...")
    # Indexes are created in schema.sql, just verify
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
    indexes = cursor.fetchall()
    print_success(f"Created {len(indexes)} indexes")

def show_stats(conn):
    """Show database statistics"""
    print_info("\nDatabase Statistics:")
    cursor = conn.cursor()
    
    # Pet stats
    cursor.execute("SELECT * FROM collection_stats")
    stats = cursor.fetchone()
    if stats:
        print(f"  Total Pets: {stats[0]}")
        print(f"  Unique Species: {stats[1]}")
        print(f"  Level 25: {stats[2]}")
        print(f"  Rare or Better: {stats[3]}")
        print(f"  Average Level: {stats[4]:.1f}")
    
    # Strategy stats
    cursor.execute("SELECT COUNT(*) FROM strategies")
    strat_count = cursor.fetchone()[0]
    print(f"  Total Strategies: {strat_count}")
    
    cursor.execute("SELECT COUNT(*) FROM ready_strategies")
    ready_count = cursor.fetchone()[0]
    print(f"  Ready Strategies: {ready_count}")

def main():
    print(f"\n{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}PetWeaver Database Migration{Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*60}{Colors.ENDC}\n")
    
    print_info("This will migrate all JSON data to SQLite database")
    print_info("Existing petweaver.db will be backed up\n")
    
    # Backup existing database
    if os.path.exists('petweaver.db'):
        backup_name = f'petweaver_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        os.rename('petweaver.db', backup_name)
        print_success(f"Backed up existing database to {backup_name}")
    
    # Create new database
    conn = create_database()
    
    # Migrate data
    migrate_pet_collection(conn)
    migrate_strategies(conn)
    migrate_ready_strategies(conn)
    
    # Create indexes
    create_indexes(conn)
    
    # Show stats
    show_stats(conn)
    
    conn.close()
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}✨ Migration Complete!{Colors.ENDC}\n")
    print_info("Database: petweaver.db")
    print_info("Schema: schema.sql")
    print_info("\nNext steps:")
    print_info("  1. Update app.py to use SQL queries")
    print_info("  2. Test all endpoints")
    print_info("  3. Benchmark performance improvements")
    print("\n")

if __name__ == "__main__":
    main()
