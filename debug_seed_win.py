from simulator import BattleSimulator, BattleState, Team, Pet, Ability, PetStats, PetFamily, PetQuality, TurnAction
from simulator.smart_agent import create_smart_enemy_agent
from simulator.npc_ai import create_npc_agent
from genetic.genome import TeamGenome
import json

def debug_seed():
    # Load abilities
    with open('abilities.json', 'r') as f:
        abilities_root = json.load(f)
        species_abilities = abilities_root.get('species_abilities', {})
        ability_stats = abilities_root.get('abilities', {})

    # Seed IDs: Ravenous Prideling (150381), Widget the Departed (86067), Carry (-1)
    seed_ids = [150381, 86067, -1]
    
    print(f"Testing Seed Team: {seed_ids}")
    
    # Create Genome using species_abilities
    genome = TeamGenome.from_team_ids(seed_ids, species_abilities)
    
    print("Genome Pets:")
    for p in genome.pets:
        print(f"  ID: {p.species_id}, Abilities: {p.abilities}")
    
    # Convert to Team
    # We need to replicate _genome_to_team logic roughly
    pets = []
    for gene in genome.pets:
        if gene.species_id == -1:
            pets.append(Pet(
                species_id=-1, name="Level 1 Carry", family=PetFamily.CRITTER,
                stats=PetStats(150, 150, 0, 0), abilities=[], quality=PetQuality.POOR
            ))
            continue
            
        # Mock stats for now
        stats = PetStats(1400, 1400, 300, 300)
        
        # Abilities
        pet_abilities = []
        for aid in gene.abilities:
            ab_data = ability_stats.get(str(aid))
            if ab_data:
                pet_abilities.append(Ability(
                    id=aid, name=ab_data.get('name'), 
                    power=ab_data.get('power', 20), 
                    cooldown=ab_data.get('cooldown', 0),
                    accuracy=ab_data.get('accuracy', 100),
                    speed=ab_data.get('speed', 0),
                    family=PetFamily(ab_data.get('family_id', 7))
                ))
        
        pets.append(Pet(
            species_id=gene.species_id, name=f"Pet {gene.species_id}",
            family=PetFamily.BEAST, stats=stats, abilities=pet_abilities, quality=PetQuality.RARE
        ))
        
    player_team = Team(pets)
    print("Player Team Created:")
    for p in player_team.pets:
        print(f"  - {p.name} (ID: {p.species_id}): {[a.name for a in p.abilities]}")

    # Create Enemy Team (Squirt)
    # Deebs, Tyri, Puzzle
    enemy_team = Team(pets=[
        Pet(species_id=1, name="Deebs", family=PetFamily.MAGIC, stats=PetStats(1600, 1600, 280, 280), abilities=[], quality=PetQuality.RARE),
        Pet(species_id=2, name="Tyri", family=PetFamily.DRAGONKIN, stats=PetStats(1600, 1600, 280, 280), abilities=[], quality=PetQuality.RARE),
        Pet(species_id=3, name="Puzzle", family=PetFamily.HUMANOID, stats=PetStats(1600, 1600, 280, 280), abilities=[], quality=PetQuality.RARE)
    ])
    
    # Run Simulation
    sim = BattleSimulator()
    
    # Simple agents
    def player_agent(state):
        active = state.player_team.get_active_pet()
        if not active or not active.stats.is_alive():
            for i, p in enumerate(state.player_team.pets):
                if p.stats.is_alive(): return TurnAction('player', 'swap', target_pet_index=i)
            return TurnAction('player', 'pass')
        for ab in active.abilities:
            if active.can_use_ability(ab): return TurnAction('player', 'ability', ability=ab)
        return TurnAction('player', 'pass')

    def enemy_agent(state):
        return TurnAction('enemy', 'pass')

    print("\nStarting Simulation...")
    state = BattleState(player_team, enemy_team, 1)
    result = sim.simulate_battle(state, player_agent, enemy_agent, max_turns=30, enable_logging=True)
    print(f"Result: {result['winner']}")
    print(f"Turns: {result['turns']}")
    print(f"Survivors: {sum(1 for p in state.player_team.pets if p.stats.is_alive())}")

if __name__ == "__main__":
    debug_seed()
