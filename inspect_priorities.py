import json

def main():
    try:
        with open('npc_ai_priorities.json', 'r') as f:
            data = json.load(f)
            
        print(f"Loaded {len(data)} keys.")
        
        # Search for squirt
        matches = [k for k in data.keys() if 'squirt' in k.lower()]
        print(f"Matches for 'squirt': {matches}")
        
        if not matches:
            print("No matches found. Printing first 10 keys:")
            print(list(data.keys())[:10])
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
