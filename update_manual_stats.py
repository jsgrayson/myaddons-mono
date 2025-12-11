import json

# Top 20 abilities from strategies
# format: id: {name, power, accuracy, speed, cooldown}
new_abilities = {
    "218": {"name": "Curse of Doom", "power": 0, "accuracy": 100, "speed": 0, "cooldown": 5, "description": "Deals massive damage after 4 rounds"},
    "919": {"name": "Black Claw", "power": 0, "accuracy": 100, "speed": 0, "cooldown": 0, "description": "Adds damage to every attack"},
    "282": {"name": "Explode", "power": 60, "accuracy": 100, "speed": 0, "cooldown": 0, "description": "Kills self to deal massive damage"},
    "624": {"name": "Ice Tomb", "power": 0, "accuracy": 100, "speed": 0, "cooldown": 5, "description": "Stuns and deals damage after 3 rounds"},
    "786": {"name": "Blistering Cold", "power": 15, "accuracy": 100, "speed": 0, "cooldown": 3, "description": "Deals damage and chills"},
    "602": {"name": "Time Bomb", "power": 50, "accuracy": 100, "speed": 0, "cooldown": 4, "description": "Deals damage after 3 rounds"},
    "490": {"name": "Magma Trap", "power": 0, "accuracy": 100, "speed": 0, "cooldown": 0, "description": "Trap that triggers on attack"},
    "334": {"name": "Decoy", "power": 0, "accuracy": 100, "speed": 0, "cooldown": 8, "description": "Blocks 2 attacks"},
    "1112": {"name": "Tough n' Cuddly", "power": 0, "accuracy": 100, "speed": 0, "cooldown": 0, "description": "Reduces damage taken"},
    "934": {"name": "Bone Bite", "power": 25, "accuracy": 100, "speed": 0, "cooldown": 0, "description": "Standard attack"},
    "586": {"name": "Blackout Kick", "power": 30, "accuracy": 100, "speed": 0, "cooldown": 3, "description": "High damage kick"},
    "542": {"name": "Predatory Strike", "power": 40, "accuracy": 100, "speed": 0, "cooldown": 4, "description": "Deals double damage if kills"},
    "488": {"name": "Quake", "power": 35, "accuracy": 100, "speed": 0, "cooldown": 4, "description": "Deals damage to underground pets"},
    "466": {"name": "Ghostly Bite", "power": 45, "accuracy": 90, "speed": 0, "cooldown": 3, "description": "High damage but stuns self"},
    "459": {"name": "Wind-Up", "power": 50, "accuracy": 100, "speed": 0, "cooldown": 0, "description": "First use charges, second deals massive damage"},
    "369": {"name": "Acidic Goo", "power": 10, "accuracy": 100, "speed": 0, "cooldown": 0, "description": "Deals DoT and increases damage taken"},
    "277": {"name": "Deep Freeze", "power": 10, "accuracy": 100, "speed": 0, "cooldown": 4, "description": "Stuns chilled target"},
    "2237": {"name": "Razor Talons", "power": 25, "accuracy": 100, "speed": 0, "cooldown": 0, "description": "Standard attack"},
    "208": {"name": "Supercharge", "power": 0, "accuracy": 100, "speed": 0, "cooldown": 3, "description": "Increases next attack damage by 125%"},
    "1760": {"name": "Meteor Strike", "power": 55, "accuracy": 85, "speed": 0, "cooldown": 5, "description": "Massive damage to all enemies"}
}

try:
    with open('ability_stats_manual.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {"abilities": {}}

# Update/Add new abilities
for aid, stats in new_abilities.items():
    data['abilities'][aid] = stats

with open('ability_stats_manual.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Updated ability_stats_manual.json with {len(new_abilities)} new abilities")
