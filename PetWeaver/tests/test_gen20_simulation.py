import json
import sys
from simulator import BattleSimulator, BattleState, Team, Pet, Ability, PetFamily, PetQuality, PetStats, TurnAction
from simulator.smart_agent import SmartAgent

def create_boss_team():
    grizzle = Pet(979, "Grizzle (Boss)", PetFamily.BEAST, PetQuality.EPIC, PetStats(1700, 1700, 320, 270), [
        Ability(1, "Bash", 25, 100, 0, 0, PetFamily.BEAST),
        Ability(2, "Hibernate", 0, 100, 0, 4, PetFamily.BEAST),
        Ability(3, "Rampage", 35, 95, 0, 0, PetFamily.BEAST)])
    beakmaster = Pet(978, "Beakmaster (Boss)", PetFamily.MECHANICAL, PetQuality.EPIC, PetStats(1500, 1500, 290, 300), [
        Ability(4, "Batter", 10, 100, 0, 0, PetFamily.MECHANICAL),
        Ability(5, "Shock and Awe", 25, 100, 0, 3, PetFamily.MECHANICAL),
        Ability(6, "Wind-Up", 50, 90, 0, 2, PetFamily.MECHANICAL)])
    bloom = Pet(977, "Bloom (Boss)", PetFamily.ELEMENTAL, PetQuality.EPIC, PetStats(1400, 1400, 340, 250), [
        Ability(7, "Lash", 20, 100, 0, 0, PetFamily.ELEMENTAL),
        Ability(8, "Soothing Mists", 0, 100, 0, 3, PetFamily.ELEMENTAL),
        Ability(9, "Entangling Roots", 15, 100, 0, 4, PetFamily.ELEMENTAL)])
    return Team([grizzle, beakmaster, bloom])

def create_gen20_team():
    # 1. Great Horned Owl (Flying)
    owl = Pet(1155, "Great Horned Owl", PetFamily.FLYING, PetQuality.RARE, PetStats(1400, 1400, 260, 260), [
        Ability(1, "Peck", 20, 100, 0, 0, PetFamily.FLYING),
        Ability(2, "Squawk", 0, 100, 0, 0, PetFamily.FLYING), # Debuff
        Ability(3, "Nocturnal Strike", 40, 90, 0, 3, PetFamily.FLYING)
    ])
    
    # 2. Echo of the Heights (Flying)
    echo = Pet(845, "Echo of the Heights", PetFamily.FLYING, PetQuality.RARE, PetStats(1400, 1400, 260, 260), [
        Ability(4, "Slicing Wind", 20, 100, 0, 0, PetFamily.FLYING),
        Ability(5, "Fly", 0, 100, 0, 4, PetFamily.FLYING, effect_type='fly'),
        Ability(6, "Cyclone", 15, 100, 0, 3, PetFamily.FLYING)
    ])
    
    # 3. Iron Starlette (Mech)
    starlette = Pet(1155, "Iron Starlette", PetFamily.MECHANICAL, PetQuality.RARE, PetStats(1400, 1400, 341, 244), [
        Ability(459, "Wind-Up", 30, 100, 0, 0, PetFamily.MECHANICAL), 
        Ability(208, "Supercharge", 0, 100, 0, 3, PetFamily.MECHANICAL, stat_buffs={'power': (2.25, 1)}),
        Ability(566, "Powerball", 15, 100, 0, 0, PetFamily.MECHANICAL)
    ])
    
    return Team([owl, echo, starlette])

def run_test():
    print("Simulating Gen 20 Team...")
    boss = create_boss_team()
    player = create_gen20_team()
    
    sim = BattleSimulator()
    
    # Use SmartAgent for both sides to approximate GA behavior
    player_ai = SmartAgent(1.0, actor_id='player').decide
    enemy_ai = SmartAgent(1.0, actor_id='enemy').decide
    
    state = BattleState(player, boss, 1)
    
    result = sim.simulate_battle(state, player_ai, enemy_ai, max_turns=50, enable_logging=True)
    
    print(f"\nWinner: {result['winner'].upper()}")
    print(f"Turns: {result['turns']}")
    print("\n--- Battle Log ---")
    print(result['log'].get_full_log())
    
    print("\n--- Event Log ---")
    for event in result['events']:
        print(event)

if __name__ == "__main__":
    run_test()
