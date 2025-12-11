# PetWeaver - WoW Pet Battle Simulator

A comprehensive pet battle simulation engine for World of Warcraft with genetic algorithm team optimization.

## Features

### ✅ Racial Passive Abilities
All 10 pet families have their unique racial passives implemented:
- **Beast**: +25% damage
- **Critter**: +50% damage above 50% HP
- **Dragonkin**: +50% damage after falling below 50% HP
- **Flying**: +50% speed above 50% HP
- **Humanoid**: Heal 4% max HP when dealing damage
- **Magic**: Damage capped at 35% max HP per hit
- **Aquatic**: +25% healing
- **Elemental**: Immune to weather damage
- **Undead**: Revive for 1 turn when killed
- **Mechanical**: Revive once to 20% HP

### ✅ Weather System
Full Pandaren Spirit weather effects:
- **Tidal Wave**: +25% Aquatic damage, +25% healing
- **Scorched Earth**: +25% Elemental damage, 35 Dragonkin DoT/turn
- **Call Lightning**: +25% Mechanical/Flying damage, 30 Elemental DoT/turn
- **Call Darkness**: -50% healing, +accuracy

### ✅ Special Encounter Mechanics
- **Rocko's Immunity**: Immune for 10 rounds, auto-dies turn 11
- **Life Exchange**: Swap health percentages
- **Gore Stacks**: Increasing DoT
- **Mind Games**: Team damage + 5-round stun
- And more...

## Project Structure

```
simulator/
├── battle_state.py          # Core data models
├── damage_calculator.py     # Damage/healing calculations
├── simulator.py             # Main battle engine
├── turn_system.py           # Turn order logic
├── buff_tracker.py          # Buff/debuff management
├── racial_passives.py       # ✨ NEW: 10 family racial abilities
├── special_encounters.py    # ✨ NEW: Gimmick fight mechanics
└── tests/
    └── test_racial_passives.py  # ✨ NEW: Comprehensive tests

genetic/                     # Genetic algorithm team builder
app.py                       # Flask web application
```

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/petweaver.git
cd petweaver

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the Simulator

```python
from simulator import BattleSimulator, BattleState
# ... create battle state and run simulation
```

### Running Tests

```bash
python3 -m pytest simulator/tests/ -v
```

### Web Application

```bash
python3 app.py
# Navigate to http://localhost:5000
```

## Recent Updates

**November 2024**: Major mechanics overhaul
- ✅ Implemented all 10 racial passive abilities
- ✅ Added Pandaren Spirit weather system
- ✅ Created special encounter mechanics module
- ✅ Comprehensive test coverage

## Data Sources

- Pet stats: Blizzard Game Data API
- Encounter data: PetTracker addon data
- Strategies: Xu-Fu's Pet Guides

## License

MIT License

## Contributing

Contributions welcome! Please open an issue first to discuss changes.
