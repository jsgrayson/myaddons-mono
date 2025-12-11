from simulator import BattleSimulator, BattleState, Team, Pet, Ability, PetStats, PetFamily, PetQuality, TurnAction
from simulator.smart_agent import create_smart_enemy_agent
from simulator.npc_ai import create_npc_agent

def test_carry_sim():
    # Create Carry Pet
    carry_pet = Pet(
        species_id=-1,
        name="Level 1 Carry",
        family=PetFamily.CRITTER,
        stats=PetStats(max_hp=150, current_hp=150, power=0, speed=0),
        abilities=[],
        quality=PetQuality.POOR
    )

    # Create Player Team (2 strong pets + Carry)
    # Using known strong pets: Ikky (1532) and Unborn Val'kyr (1155) - Mocked
    ikky = Pet(
        species_id=1532,
        name="Ikky",
        family=PetFamily.FLYING,
        stats=PetStats(max_hp=1400, current_hp=1400, power=300, speed=300),
        abilities=[
            Ability(id=1, name="Black Claw", power=0, cooldown=0, accuracy=100, speed=0, family=PetFamily.BEAST),
            Ability(id=2, name="Flock", power=100, cooldown=0, accuracy=100, speed=0, family=PetFamily.FLYING),
            Ability(id=3, name="Quills", power=200, cooldown=0, accuracy=100, speed=0, family=PetFamily.FLYING)
        ],
        quality=PetQuality.RARE
    )
    
    # Mock Enemy Team (Squirt's team)
    enemy_team = Team(pets=[
        Pet(species_id=1, name="Deebs", family=PetFamily.MAGIC, stats=PetStats(1600, 1600, 280, 280), abilities=[], quality=PetQuality.RARE),
        Pet(species_id=2, name="Tyri", family=PetFamily.DRAGONKIN, stats=PetStats(1600, 1600, 280, 280), abilities=[], quality=PetQuality.RARE),
        Pet(species_id=3, name="Puzzle", family=PetFamily.HUMANOID, stats=PetStats(1600, 1600, 280, 280), abilities=[], quality=PetQuality.RARE)
    ])

    player_team = Team(pets=[ikky, carry_pet]) # Just 2 pets to test swapping to carry

    sim = BattleSimulator()
    
    # Simple agents
    def player_agent(state):
        active = state.player_team.get_active_pet()
        if not active or not active.stats.is_alive():
            # Swap logic
            for i, p in enumerate(state.player_team.pets):
                if p.stats.is_alive(): return TurnAction('player', 'swap', target_pet_index=i)
            return TurnAction('player', 'pass')
        
        # Use first available ability
        for ab in active.abilities:
            if active.can_use_ability(ab): return TurnAction('player', 'ability', ability=ab)
        return TurnAction('player', 'pass')

    def enemy_agent(state):
        return TurnAction('enemy', 'pass')

    print("Starting Simulation...")
    state = BattleState(player_team, enemy_team, 1)
    result = sim.simulate_battle(state, player_agent, enemy_agent, max_turns=20, enable_logging=True)
    print("Simulation Result:", result['winner'])
    print("Turns:", result['turns'])

if __name__ == "__main__":
    test_carry_sim()
