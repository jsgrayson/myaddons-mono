import json

def main():
    with open('species_data.json', 'r') as f:
        data = json.load(f)
        
    ids = [2544, 393]
    for pid in ids:
        info = data.get(str(pid))
        if info:
            print(f"ID {pid}: {info.get('name')} ({info.get('family_name')})")
        else:
            print(f"ID {pid}: Not found")

if __name__ == "__main__":
    main()
