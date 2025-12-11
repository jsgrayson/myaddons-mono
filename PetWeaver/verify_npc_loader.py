import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from simulator.npc_move_loader import load_npc_move_orders, get_move_orders
from simulator.npc_ai import create_npc_agent
from simulator.battle_state import BattleState, Team, Pet, Ability, PetStats, PetFamily, TurnAction, PetQuality

def test_loader():
    print("Testing NPC Move Loader...")
    orders = get_move_orders()
    
    if "Rocko" not in orders:
        print("FAIL: Rocko not found in orders")
        return
    
    rocko_moves = orders["Rocko"][0] # Pet 0
    if rocko_moves.get(1) != "Smash":
        print(f"FAIL: Rocko round 1 expected Smash, got {rocko_moves.get(1)}")
        return
        
    if "Blingtron 4000" not in orders:
        print("FAIL: Blingtron 4000 not found")
        return
        
    bling_moves = orders["Blingtron 4000"][0]
    if bling_moves.get(1) != "Extra Plating":
        print(f"FAIL: Blingtron round 1 expected Extra Plating, got {bling_moves.get(1)}")
        return
        
    print("PASS: Loader works correctly")

def test_agent():
    print("\nTesting NPC Agent...")
    
    # Setup Mock State
    # Rocko has Smash (ID 1)
    smash = Ability(id=1, name="Smash", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.ELEMENTAL)
    rocko_pet = Pet(
        species_id=1, name="Rocko", family=PetFamily.ELEMENTAL,
        quality=PetQuality.RARE,
        stats=PetStats(100, 100, 10, 10),
        abilities=[smash]
    )
    
    enemy_team = Team(pets=[rocko_pet])
    player_team = Team(pets=[rocko_pet]) # Mirror match
    
    state = BattleState(player_team, enemy_team, turn_number=1)
    
    # Default AI just passes
    def default_ai(s): return TurnAction('enemy', 'pass')
    
    # Create Agent
    agent = create_npc_agent("Rocko", default_ai)
    
    # Test Round 1
    action = agent(state)
    print(f"Round 1 Action: {action}")
    
    if action.action_type == 'ability' and action.ability.name == "Smash":
        print("PASS: Agent chose Smash")
    else:
        print(f"FAIL: Agent chose {action}")

    # Test Fallback (Round 100, no data)
    state.turn_number = 100
    action = agent(state)
    print(f"Round 100 Action: {action}")
    if action.action_type == 'pass':
        print("PASS: Agent fell back to default")
    else:
        print(f"FAIL: Agent did not fall back, chose {action}")

if __name__ == "__main__":
    test_loader()
    test_agent()
