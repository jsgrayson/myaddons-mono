from simulator.strategy_manager import StrategyManager

def test_lookup():
    sm = StrategyManager('strategies_master.json')
    name = "Squirt (WoD Garrison)"
    print(f"Looking up strategy for: {name}")
    
    strategy = sm.get_strategy(name)
    if strategy:
        print("✅ Strategy Found!")
        print(f"Strategy Name: {strategy.get('strategy_name')}")
        print(f"Pet Slots: {strategy.get('pet_slots')}")
        
        team = sm.get_recommended_team(name)
        print(f"Recommended Team IDs: {team}")
    else:
        print("❌ No strategy found.")
        
        # Debug fuzzy match
        print("\nDebugging Fuzzy Match:")
        import difflib
        best_ratio = 0
        best_name = ""
        for expansion, categories in sm.strategies.items():
            for category, encounters in categories.items():
                for encounter in encounters:
                    enc_name = encounter.get('encounter_name', '')
                    ratio = difflib.SequenceMatcher(None, name.lower(), enc_name.lower()).ratio()
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_name = enc_name
        print(f"Best Match: '{best_name}' with ratio {best_ratio}")

if __name__ == "__main__":
    test_lookup()
