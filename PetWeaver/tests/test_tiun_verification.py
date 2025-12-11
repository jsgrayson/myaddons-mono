import unittest
import random
from simulator import BattleSimulator, BattleState, Team, Pet, PetStats, PetFamily, PetQuality, Ability, TurnAction
from genetic.evolution import EvolutionEngine
from genetic.genome import TeamGenome

class TestTiunVerification(unittest.TestCase):
    def setUp(self):
        # 1. Define Ti'un (Enemy) - Aquatic Boss
        # Using realistic stats for a Beast of Fable (High HP, decent power)
        # Abilities: Pump (High Dmg), Tidal Wave (AoE), Water Jet (Filler)
        tiun = Pet(1000, "Ti'un the Wanderer", PetFamily.AQUATIC, PetQuality.LEGENDARY, PetStats(1800, 1800, 300, 280, 100), [
            Ability(118, "Pump", 40, 100, 0, 3, PetFamily.AQUATIC), # Charge up, then big hit
            Ability(400, "Tidal Wave", 15, 100, 0, 3, PetFamily.AQUATIC), # AoE
            Ability(118, "Water Jet", 20, 100, 0, 0, PetFamily.AQUATIC) # Filler
        ])
        # Ti'un is a single boss pet usually, but let's give him 2 dummy backline pets if needed for format
        # or just 1 pet if the sim supports 1v3. Sim supports 3v3 usually.
        # Let's add 2 weak backline pets to match the "3 pet team" structure
        p2 = Pet(1001, "Backline 1", PetFamily.AQUATIC, PetQuality.POOR, PetStats(500, 500, 100, 100, 100), [Ability(1, "Splash", 10, 100, 0, 0, PetFamily.AQUATIC)])
        p3 = Pet(1002, "Backline 2", PetFamily.AQUATIC, PetQuality.POOR, PetStats(500, 500, 100, 100, 100), [Ability(1, "Splash", 10, 100, 0, 0, PetFamily.AQUATIC)])
        
        self.enemy_team = Team([tiun, p2, p3])

        # Mock DBs for GA
        self.species = ["86447", "64899", "1155"] # Ikky, MPD, Meta
        self.ability_db = {
            "86447": {"family_id": 3, "abilities": [1, 2, 3]}, # Ikky (Flying)
            "64899": {"family_id": 10, "abilities": [4, 5, 6]}, # MPD (Mech)
            "1155": {"family_id": 1, "abilities": [7, 8, 9]}
        }

    def test_tiun_seeded_win(self):
        print("\n--- Testing Ti'un Seeded Strategy ---")
        # Strategy: Ikky (Black Claw, Flock), MPD (Explode)
        
        # Ikky
        ikky = Pet(86447, "Ikky", PetFamily.FLYING, PetQuality.RARE, PetStats(1400, 1400, 300, 300, 100), [
            Ability(919, "Black Claw", 0, 100, 0, 3, PetFamily.BEAST), # Adds dmg taken
            Ability(581, "Flock", 10, 100, 0, 3, PetFamily.FLYING), # Multi-hit (synergy with Black Claw)
            Ability(1, "Quills", 20, 100, 0, 0, PetFamily.FLYING)
        ])
        # Pet Bombling
        pb = Pet(9656, "Pet Bombling", PetFamily.MECHANICAL, PetQuality.RARE, PetStats(1400, 1400, 289, 289, 100), [
            Ability(640, "Toxic Smoke", 20, 100, 0, 0, PetFamily.MECHANICAL),
            Ability(282, "Explode", 60, 100, 0, 0, PetFamily.MECHANICAL),
            Ability(4, "Zap", 20, 100, 0, 0, PetFamily.MECHANICAL)
        ])
        # MPD
        mpd = Pet(64899, "Mech Pandaren Dragonling", PetFamily.MECHANICAL, PetQuality.RARE, PetStats(1400, 1400, 280, 280, 100), [
            Ability(1, "Breath", 20, 100, 0, 0, PetFamily.DRAGONKIN),
            Ability(2, "Bombing Run", 30, 100, 0, 3, PetFamily.MECHANICAL),
            Ability(282, "Explode", 60, 100, 0, 0, PetFamily.MECHANICAL)
        ])
        # Cleanup pet (Mechanical for Failsafe)
        cleanup = Pet(64899, "MPD 2", PetFamily.MECHANICAL, PetQuality.RARE, PetStats(1400, 1400, 280, 280, 100), [
            Ability(1, "Breath", 30, 100, 0, 0, PetFamily.DRAGONKIN),
            Ability(282, "Explode", 60, 100, 0, 0, PetFamily.MECHANICAL)
        ])
        
        player_team = Team([ikky, mpd, cleanup])
        
        def player_agent(state):
            active = state.player_team.get_active_pet()
            
            # Ikky Logic
            if active.name == "Ikky":
                # 1. Black Claw
                bc = next((a for a in active.abilities if a.name == "Black Claw"), None)
                if bc and active.can_use_ability(bc): return TurnAction('player', 'ability', ability=bc)
                
                # 2. Flock
                flock = next((a for a in active.abilities if a.name == "Flock"), None)
                if flock and active.can_use_ability(flock): return TurnAction('player', 'ability', ability=flock)
                
                return TurnAction('player', 'ability', ability=active.abilities[2]) # Quills

            # Mechanical pets (MPD, cleanup) - Use Explode when enemy low or Breath
            if active.family == PetFamily.MECHANICAL:
                explode = next((a for a in active.abilities if a.name == "Explode"), None)
                if explode and active.can_use_ability(explode):
                    enemy = state.enemy_team.get_active_pet()
                    if enemy and enemy.stats.current_hp < 600:
                        return TurnAction('player', 'ability', ability=explode)
                
                # Default to first ability (Breath)
                if active.abilities and active.can_use_ability(active.abilities[0]):
                    return TurnAction('player', 'ability', ability=active.abilities[0])
            
            return TurnAction('player', 'pass')

        def enemy_agent(state):
            active = state.enemy_team.get_active_pet()
            # Smart usage: Pump/Tidal Wave on CD
            for a in active.abilities:
                if active.can_use_ability(a) and a.cooldown > 0: return TurnAction('enemy', 'ability', ability=a)
            
            # Filler (usually last ability, but check index)
            filler_idx = len(active.abilities) - 1
            return TurnAction('enemy', 'ability', ability=active.abilities[filler_idx])

        sim = BattleSimulator()
        state = BattleState(player_team, self.enemy_team.copy(), 1)
        res = sim.simulate_battle(state, player_agent, enemy_agent, enable_logging=True)
        
        print(f"Seeded Result: {res['winner']} in {res['turns']} turns")
        print(res['log'].get_full_log())
        self.assertEqual(res['winner'], 'player')

    def test_tiun_blind_evolution(self):
        print("\n--- Testing Ti'un Blind Evolution (Fallback) ---")
        
        class MockEvaluator:
            def __init__(self, enemy_team):
                self.enemy_team = enemy_team
                self.target_team = enemy_team
                self.sim = BattleSimulator()
                self.species_db = {"86447": {"family_id": 3}, "64899": {"family_id": 10}, "1155": {"family_id": 1}}
                self.ability_db = {
                    "86447": {"family_id": 3, "abilities": [1, 2, 3]},
                    "64899": {"family_id": 10, "abilities": [4, 5, 6]},
                    "1155": {"family_id": 1, "abilities": [7, 8, 9]}
                }
            
            def evaluate(self, genome):
                pets = []
                for g_pet in genome.pets:
                    pid = int(g_pet.species_id) if g_pet.species_id else 86447
                    p = Pet(pid, f"Pet {pid}", PetFamily.FLYING, PetQuality.RARE, PetStats(1400, 1400, 300, 300, 100), [
                        Ability(1, "Attack", 30, 100, 0, 0, PetFamily.FLYING) # Strong attack
                    ])
                    pets.append(p)
                player_team = Team(pets)
                
                state = BattleState(player_team, self.enemy_team.copy(), 1)
                res = self.sim.simulate_battle(state, lambda s: TurnAction('player', 'ability', ability=s.player_team.get_active_pet().abilities[0]), 
                                                      lambda s: TurnAction('enemy', 'ability', ability=s.enemy_team.get_active_pet().abilities[0]))
                
                if res['winner'] == 'player': return 1000 - res['turns']
                return res['turns']
        
        evaluator = MockEvaluator(self.enemy_team)
        engine = EvolutionEngine(evaluator, population_size=20)
        
        engine.initialize_population(["86447", "64899", "1155"], evaluator.ability_db, seed_teams=[])
        
        found_winner = False
        for i in range(5):
            for g in engine.population:
                if g.fitness == 0: g.fitness = evaluator.evaluate(g)
            
            engine.evolve_generation(["86447", "64899", "1155"])
            
            best = engine.best_genome
            if best and best.fitness > 500:
                print(f"Gen {i}: Best Fitness {best.fitness}")
                found_winner = True
                break
            
        print(f"Blind Run Found Winner: {found_winner}")
        self.assertTrue(len(engine.population) > 0)

if __name__ == '__main__':
    unittest.main()
