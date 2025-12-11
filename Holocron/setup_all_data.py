#!/usr/bin/env python3
"""
Comprehensive Data Setup Script for All Applications
This script sets up data infrastructure across Holocron, PetWeaver, GoblinStack, and SkillWeaver
Works with or without PostgreSQL database
"""

import os
import json
import sys
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(msg):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{msg}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(msg):
    print(f"{Colors.OKGREEN}✅ {msg}{Colors.ENDC}")

def print_warning(msg):
    print(f"{Colors.WARNING}⚠️  {msg}{Colors.ENDC}")

def print_error(msg):
    print(f"{Colors.FAIL}❌ {msg}{Colors.ENDC}")

def print_info(msg):
    print(f"{Colors.OKCYAN}ℹ️  {msg}{Colors.ENDC}")

def check_database():
    """Check if PostgreSQL database is available"""
    try:
        import psycopg2
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            print_warning("DATABASE_URL not set - using JSON fallback mode")
            return False
        
        conn = psycopg2.connect(db_url)
        conn.close()
        print_success("PostgreSQL database is available")
        return True
    except ImportError:
        print_warning("psycopg2 not installed - using JSON fallback mode")
        return False
    except Exception as e:
        print_warning(f"Database unavailable: {e} - using JSON fallback mode")
        return False

def setup_holocron_data(use_db=False):
    """Setup data for Holocron ERP system"""
    print_header("Setting Up Holocron Data")
    
    holocron_path = Path("/Users/jgrayson/Documents/holocron")
    
    # Load sample data
    sample_data_path = holocron_path / "sample_data.json"
    if sample_data_path.exists():
        print_info("Sample data file exists")
    else:
        print_warning("Sample data file not found")
        return
    
    if use_db:
        print_info("Populating PostgreSQL database...")
        # TODO: Run schema files and insert data
        print_warning("Database population not yet implemented - using fallback")
    else:
        print_info("Using JSON file-based data")
    
    print_success("Holocron data setup complete")

def setup_petweaver_data():
    """Setup data for PetWeaver application"""
    print_header("Setting Up PetWeaver Data")
    
    petweaver_path = Path("/Users/jgrayson/Documents/petweaver")
    
    # Create sample pet collection if it doesn't exist
    my_pets_file = petweaver_path / "my_pets.json"
    if not my_pets_file.exists():
        print_info("Creating sample pet collection...")
        sample_pets = {
            "pets": [
                {
                    "speciesId": 39,
                    "name": "Mechanical Squirrel",
                    "level": 25,
                    "quality": 3,
                    "breedId": 5,
                    "health": 1546,
                    "power": 276,
                    "speed": 276
                },
                {
                    "speciesId": 1387,
                    "name": "Ikky",
                    "level": 25,
                    "quality": 3,
                    "breedId": 6,
                    "health": 1400,
                    "power": 305,
                    "speed": 289
                }
            ],
            "timestamp": "2025-11-28T09:00:00Z",
            "total_count": 2
        }
        with open(my_pets_file, 'w') as f:
            json.dump(sample_pets, f, indent=2)
        print_success(f"Created sample pet collection at {my_pets_file}")
    else:
        print_info("Pet collection already exists")
    
    # Create sample strategies file
    strategies_file = petweaver_path / "strategies.json"
    if not strategies_file.exists():
        print_info("Creating sample strategies...")
        sample_strategies = {
            "Legion": {
                "Broken Isles": [
                    {
                        "npc_id": 116789,
                        "name": "Environeer Bert",
                        "strategies": [
                            {
                                "team": ["Ikky", "Mechanical Pandaren Dragonling", "Iron Starlette"],
                                "win_rate": 95.0
                            }
                        ]
                    }
                ]
            }
        }
        with open(strategies_file, 'w') as f:
            json.dump(sample_strategies, f, indent=2)
        print_success(f"Created sample strategies at {strategies_file}")
    else:
        print_info("Strategies file already exists")
    
    print_success("PetWeaver data setup complete")

def setup_goblinstack_data():
    """Setup data for GoblinStack application"""
    print_header("Setting Up GoblinStack Data")
    
    goblin_path = Path("/Users/jgrayson/Documents/goblin-clean-1")
    
    # Create sample market data
    market_data_file = goblin_path / "market_data.json"
    sample_market = {
        "items": [
            {
                "item_id": 171285,
                "name": "Eternal Crystal",
                "current_price": 850,
                "historical_avg": 1000,
                "volume_24h": 1250,
                "price_trend": -15.2,
                "last_updated": "2025-11-28T09:00:00Z"
            },
            {
                "item_id": 171833,
                "name": "Elethium Ore",
                "current_price": 425,
                "historical_avg": 392,
                "volume_24h": 3400,
                "price_trend": 8.5,
                "last_updated": "2025-11-28T09:00:00Z"
            },
            {
                "item_id": 171829,
                "name": "Shadowghast Ingot",
                "current_price": 1200,
                "historical_avg": 1225,
                "volume_24h": 890,
                "price_trend": -2.1,
                "last_updated": "2025-11-28T09:00:00Z"
            }
        ],
        "timestamp": "2025-11-28T09:00:00Z"
    }
    with open(market_data_file, 'w') as f:
        json.dump(sample_market, f, indent=2)
    print_success(f"Created market data at {market_data_file}")
    
    print_success("GoblinStack data setup complete")

def setup_skillweaver_data():
    """Setup data for SkillWeaver application"""
    print_header("Setting Up SkillWeaver Data")
    
    skillweaver_path = Path("/Users/jgrayson/Documents/skillweaver-web")
    
    # Create sample character data
    characters_file = skillweaver_path / "characters.json"
    sample_characters = {
        "characters": [
            {
                "name": "Zephyrmage",
                "realm": "Area 52",
                "class": "Mage",
                "spec": "Frost",
                "level": 80,
                "ilvl": 615,
                "talents": {
                    "class": [1, 1, 2, 1, 3, 2, 1, 2, 1, 3],
                    "spec": [2, 1, 3, 2, 1, 2, 3, 1, 2, 1]
                }
            },
            {
                "name": "Thornheal",
                "realm": "Area 52",
                "class": "Druid",
                "spec": "Restoration",
                "level": 80,
                "ilvl": 608,
                "talents": {
                    "class": [1, 2, 1, 3, 1, 2, 1, 2, 3, 1],
                    "spec": [1, 2, 1, 2, 3, 1, 2, 1, 3, 2]
                }
            }
        ],
        "timestamp": "2025-11-28T09:00:00Z"
    }
    with open(characters_file, 'w') as f:
        json.dump(sample_characters, f, indent=2)
    print_success(f"Created character data at {characters_file}")
    
    print_success("SkillWeaver data setup complete")

def create_shared_character_data():
    """Create shared character data that all apps can access"""
    print_header("Setting Up Shared Character Data")
    
    shared_data = {
        "characters": [
            {
                "guid": "0x0000000012345678",
                "name": "Zephyrmage",
                "realm": "Area 52",
                "class": "Mage",
                "level": 80,
                "gold": 450000,
                "pets_collected": 1428,
                "quests_completed": 12456
            },
            {
                "guid": "0x0000000087654321",
                "name": "Thornheal",
                "realm": "Area 52",
                "class": "Druid",
                "level": 80,
                "gold": 280000,
                "pets_collected": 1312,
                "quests_completed": 11203
            },
            {
                "guid": "0x00000000ABCDEF01",
                "name": "Grimtank",
                "realm": "Area 52",
                "class": "Warrior",
                "level": 70,
                "gold": 125000,
                "pets_collected": 456,
                "quests_completed": 4521
            }
        ],
        "last_sync": "2025-11-28T09:00:00Z",
        "total_gold": 855000,
        "total_pets": 4196
    }
    
    # Save to each app directory
    apps = [
        "/Users/jgrayson/Documents/holocron",
        "/Users/jgrayson/Documents/petweaver",
        "/Users/jgrayson/Documents/goblin-clean-1",
        "/Users/jgrayson/Documents/skillweaver-web"
    ]
    
    for app_path in apps:
        shared_file = Path(app_path) / "shared_characters.json"
        with open(shared_file, 'w') as f:
            json.dump(shared_data, f, indent=2)
        print_success(f"Created shared data at {shared_file}")
    
    print_success("Shared character data setup complete")

def main():
    print_header("🎮 WoW Application Suite - Data Setup")
    print_info("This script sets up data for all four applications")
    print_info("Apps: Holocron, PetWeaver, GoblinStack, SkillWeaver\n")
    
    # Check database availability
    use_db = check_database()
    
    # Setup data for each application
    setup_holocron_data(use_db)
    setup_petweaver_data()
    setup_goblinstack_data()
    setup_skillweaver_data()
    
    # Create shared data
    create_shared_character_data()
    
    print_header("✨ Data Setup Complete!")
    print_info("All applications now have sample data for testing")
    print_info("Data files created:")
    print_info("  - sample_data.json (Holocron)")
    print_info("  - my_pets.json (PetWeaver)")
    print_info("  - market_data.json (GoblinStack)")
    print_info("  - characters.json (SkillWeaver)")
    print_info("  - shared_characters.json (All apps)")
    print("\n")
    
    if not use_db:
        print_warning("Database mode: JSON fallback")
        print_info("To use PostgreSQL:")
        print_info("  1. Start PostgreSQL service")
        print_info("  2. Set DATABASE_URL environment variable")
        print_info("  3. Run: ./populate_database.sh")
    
    print("\n")

if __name__ == "__main__":
    main()
