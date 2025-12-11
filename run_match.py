from match_strategies import StrategyMatcher
import json

def run_matching():
    print("Running matcher with strategies_cleaned.json...")
    matcher = StrategyMatcher(strategies_file='strategies_cleaned.json')
    results = matcher.match_strategies()
    
    total_encounters = 0
    ready_count = 0
    
    for exp, cats in results.items():
        for cat, encounters in cats.items():
            ready_count += len(encounters)
            # Total encounters isn't returned by match_strategies, only matches
    
    print(f"\nReady Encounters: {ready_count}")
    
    # Save results
    with open('my_ready_strategies.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("Saved results to my_ready_strategies.json")

if __name__ == "__main__":
    run_matching()
