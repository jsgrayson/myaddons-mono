import json
from collections import Counter

with open('encounters_full.json', 'r') as f:
    encounters = json.load(f)

ability_counts = Counter()
pets_with_more_than_3 = []

for tamer in encounters:
    for pet in tamer['pets']:
        count = len(pet.get('abilities', []))
        ability_counts[count] += 1
        if count > 3:
            pets_with_more_than_3.append(f"{tamer['name']} - {pet['species_id']} ({count})")

print("Ability counts per pet:")
for count, freq in sorted(ability_counts.items()):
    print(f"  {count} abilities: {freq} pets")

if pets_with_more_than_3:
    print(f"\nPets with >3 abilities ({len(pets_with_more_than_3)}):")
    for p in pets_with_more_than_3[:10]:
        print(f"  {p}")
else:
    print("\nNo pets have >3 abilities. All abilities are active!")
