import json
from pathlib import Path

INPUT_JSON = Path(__file__).resolve().parent / "strategies_enhanced.json"

def inspect_json():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for key, value in data.items():
        print(f"Key: {key}")
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                if isinstance(subvalue, list):
                    print(f"  {subkey}: {len(subvalue)} items")
                else:
                    print(f"  {subkey}: {type(subvalue)}")
        elif isinstance(value, list):
            print(f"  (List of {len(value)} items)")
        else:
            print(f"  {type(value)}")

if __name__ == "__main__":
    inspect_json()
