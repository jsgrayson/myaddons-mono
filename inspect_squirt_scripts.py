import json

def main():
    try:
        with open('strategies_enhanced.json', 'r') as f:
            data = json.load(f)
    except:
        with open('strategies.json', 'r') as f:
            data = json.load(f)
            
    for expansion, categories in data.items():
        if not isinstance(categories, dict): continue
        for category, encounters in categories.items():
            if not isinstance(encounters, list): continue
            for encounter in encounters:
                if 'squirt' in encounter.get('encounter_name', '').lower():
                    print(f"--- Strategy for {encounter['encounter_name']} ---")
                    for strategy in encounter.get('strategies', []):
                        print(f"Script:\n{strategy.get('script', '')[:500]}...\n")

if __name__ == "__main__":
    main()
