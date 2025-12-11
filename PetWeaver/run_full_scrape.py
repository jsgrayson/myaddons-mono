"""
Simple script to run full strategy scrape and extract seed teams.

Usage:
    python run_full_scrape.py

This will:
1. Scrape all encounters from Xu-Fu
2. Save raw strategies to strategies_enhanced.json
3. Extract team compositions to xufu_seed_teams.json for GA seeding
"""

from scrape_xufu_enhanced import XuFuScraperEnhanced
import time

def main():
    print("="*70)
    print(" XU-FU STRATEGY SCRAPER - FULL RUN ".center(70))
    print("="*70)
    print("\nThis will scrape ALL encounters and extract winning teams.")
    print("Time estimate: 30-60 minutes (respectful 1.5s delays)")
    print("\nPress Ctrl+C at any time to stop.")
    print("="*70 + "\n")
    
    # Wait a moment for user to cancel if needed
    time.sleep(3)
    
    scraper = XuFuScraperEnhanced()
    
    # Run full scrape
    scraper.scrape_all()
    scraper.save_data('strategies_enhanced.json')
    
    # Extract seeds
    print("\n" + "="*70)
    print(" EXTRACTING SEED TEAMS ".center(70))
    print("="*70)
    scraper.extract_seeds_from_strategies('xufu_seed_teams.json')
    
    print("\n" + "="*70)
    print(" COMPLETE! ".center(70))
    print("="*70)
    print("\nFiles created:")
    print("  1. strategies_enhanced.json - Full strategy data")
    print("  2. xufu_seed_teams.json - Team compositions for GA")
    print("\nTo use in genetic algorithm:")
    print("  engine.initialize_population(..., strategy_file='xufu_seed_teams.json')")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Scraping cancelled by user")
        print("Partial data may have been saved.")
