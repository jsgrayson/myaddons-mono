import json
import os
from simulator.simulator import BattleSimulator
from simulator.battle_state import BattleState, Team, Pet, PetStats, Ability, PetFamily
from simulator.npc_ai import create_npc_agent

def load_data():
    with open('variations_with_scripts.json', 'r') as f:
        variations = json.load(f)
    with open('species_data.json', 'r') as f:
        species_db = json.load(f)
    with open('abilities.json', 'r') as f:
        ability_db = json.load(f)
    return variations, species_db, ability_db

def create_pet(species_id, species_db, ability_db):
    if species_id == 0: return None
    
    s_data = species_db.get(str(species_id))
    if not s_data: return None
    
    # Create stats (assume level 25 rare B/B for now)
    stats = PetStats(max_hp=1400, current_hp=1400, power=289, speed=289)
    
    # Create abilities
    abilities = []
    # Just pick first 3 for now, real validation needs exact slots
    # But for script validation, we just need the ability IDs to exist
    possible_abilities = ability_db.get(str(species_id), {}).get('abilities', [])
    for aid in possible_abilities:
        a_data = ability_db.get(str(aid))
        if a_data:
            abilities.append(Ability(
                id=aid,
                name=a_data.get('name', 'Unknown'),
                power=a_data.get('power', 0),
                accuracy=a_data.get('accuracy', 100),
                speed=0,
                family=PetFamily(a_data.get('family_id', 1)),
                cooldown=a_data.get('cooldown', 0)
            ))
            
    return Pet(
        name=s_data.get('name', 'Unknown'),
        species_id=species_id,
        stats=stats,
        abilities=abilities,
        family=PetFamily(s_data.get('family_id', 1))
    )

def validate_strategies():
    variations, species_db, ability_db = load_data()
    simulator = BattleSimulator()
    
    total = 0
    wins = 0
    
    print("Validating strategies...")
    
    # Test a subset (e.g., Rock Collector)
    target_encounter = "Rock Collector"
    if target_encounter in variations:
        print(f"Testing {target_encounter}...")
        for variant in variations[target_encounter]:
            team_ids = variant['team']
            
            # Construct Player Team (The Strategy)
            p1 = create_pet(team_ids[0], species_db, ability_db)
            p2 = create_pet(team_ids[1], species_db, ability_db)
            p3 = create_pet(team_ids[2], species_db, ability_db)
            player_team_pets = [p for p in [p1, p2, p3] if p]
            if not player_team_pets:
                print(f"  Variant {team_ids}: SKIPPED (Empty Team)")
                continue
            player_team = Team(player_team_pets)
            
            # Construct Enemy Team (Dummy for now, or load real encounter)
            # For validation, we really want to see if the script executes without crashing
            # and if it beats a dummy enemy
            e1 = create_pet(68662, species_db, ability_db) # Chrominius
            if not e1:
                # Fallback if Chrominius not found
                e1 = create_pet(1155, species_db, ability_db) # Curiously checking if 1155 exists (generic)
                if not e1:
                     # Create a dummy pet manually if DB is missing
                     stats = PetStats(1400, 1400, 289, 289)
                     e1 = Pet(68662, "Dummy Enemy", PetFamily.MAGIC, PetQuality.RARE, stats, [])
            
            enemy_team = Team([e1])
            
            # Setup Battle
            # Swap teams for simulation: Player=Dummy, Enemy=Strategy
            # We want the Strategy Team to be the ENEMY in the sim because create_npc_agent is for enemies
            sim_state = BattleState(enemy_team, player_team, 1)
            
            # Agent for Strategy Team (Enemy in sim)
            strategy_agent = create_npc_agent("StrategyTester")
            
            # Dummy Agent for Dummy Team (Player in sim)
            def dummy_agent(s): return TurnAction('player', 'pass')
            
            # Run
            try:
                result = simulator.simulate_battle(sim_state, dummy_agent, strategy_agent, max_turns=20)
                if result['winner'] == 'enemy': # Strategy team won
                    wins += 1
                total += 1
                print(f"  Variant {team_ids}: {result['winner']} ({result['turns']} turns)")
            except Exception as e:
                print(f"  Variant {team_ids}: CRASH - {e}")

    print(f"Validation Complete: {wins}/{total} Wins")

if __name__ == "__main__":
    validate_strategies()
