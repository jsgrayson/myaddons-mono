import time
import cProfile
import pstats
from simulator.simulator import BattleSimulator
from simulator.battle_state import BattleState, Team, Pet, PetStats, PetFamily, PetQuality, Ability
from simulator.npc_ai import create_npc_agent

def create_benchmark_teams():
    # Create complex teams to stress the simulator
    # Team 1: Multi-hit, Weather, Buffs
    p1 = Pet(
        species_id=1, name="Attacker", family=PetFamily.MECHANICAL, quality=PetQuality.RARE,
        stats=PetStats(max_hp=1500, current_hp=1500, power=300, speed=300),
        abilities=[
            Ability(id=1, name="Multi-Hit", power=10, accuracy=100, speed=0, cooldown=0, family=PetFamily.MECHANICAL, hits=3),
            Ability(id=2, name="Buff", power=0, accuracy=100, speed=0, cooldown=3, family=PetFamily.MECHANICAL, stat_buffs={'power': (1.5, 3)}),
            Ability(id=3, name="Weather", power=20, accuracy=100, speed=0, cooldown=5, family=PetFamily.MECHANICAL, effect_type='weather_lightning')
        ]
    )
    
    # Team 2: Healing, DoTs, Shields
    p2 = Pet(
        species_id=2, name="Defender", family=PetFamily.ELEMENTAL, quality=PetQuality.RARE,
        stats=PetStats(max_hp=1800, current_hp=1800, power=250, speed=250),
        abilities=[
            Ability(id=4, name="Heal", power=0, accuracy=100, speed=0, cooldown=3, family=PetFamily.ELEMENTAL, is_heal=True),
            Ability(id=5, name="DoT", power=10, accuracy=100, speed=0, cooldown=0, family=PetFamily.ELEMENTAL, is_dot=True, dot_duration=5),
            Ability(id=6, name="Shield", power=0, accuracy=100, speed=0, cooldown=4, family=PetFamily.ELEMENTAL, effect_type='shield')
        ]
    )
    
    t1 = Team(pets=[p1])
    t2 = Team(pets=[p2])
    return t1, t2

def run_benchmark(iterations=1000, profile=False):
    sim = BattleSimulator(rng_seed=42)
    t1, t2 = create_benchmark_teams()
    state = BattleState(t1, t2, 1, rng_seed=42)
    
    # Simple AI
    def ai(s):
        active = s.player_team.get_active_pet() if s.player_team.active_pet_index is not None else None
        if active:
            return s.player_team.get_valid_actions(s, 'player')[0] # Just pick first valid
        return None

    def enemy_ai(s):
        active = s.enemy_team.get_active_pet() if s.enemy_team.active_pet_index is not None else None
        if active:
            return s.enemy_team.get_valid_actions(s, 'enemy')[0]
        return None

    print(f"🚀 Starting Benchmark ({iterations} iterations)...")
    
    start_time = time.time()
    
    if profile:
        pr = cProfile.Profile()
        pr.enable()
        
    for _ in range(iterations):
        # Reset state for each iteration to keep it fair
        # We clone the initial state to avoid overhead of creating new objects every time if possible,
        # but deepcopy is part of the simulation cost usually. 
        # Actually, simulate_battle takes a state.
        # Let's create a fresh state copy each time to simulate a new battle start.
        current_state = state.copy()
        sim.simulate_battle(current_state, ai, enemy_ai, max_turns=20, enable_logging=False)
        
    if profile:
        pr.disable()
        ps = pstats.Stats(pr).sort_stats('cumulative')
        ps.print_stats(20)
        
    duration = time.time() - start_time
    battles_per_sec = iterations / duration
    
    print(f"✅ Completed in {duration:.4f}s")
    print(f"⚡ Speed: {battles_per_sec:.2f} battles/sec")
    
    return battles_per_sec

if __name__ == "__main__":
    run_benchmark(iterations=1000, profile=True)
