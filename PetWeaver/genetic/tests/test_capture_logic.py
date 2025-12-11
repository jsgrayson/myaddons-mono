import unittest
from simulator.battle_state import Ability, PetFamily, PetStats, Pet, PetQuality, BattleState, Team
from simulator.damage_calculator import DamageCalculator
from simulator.capture_agent import CaptureAgent
from genetic.evolution import EvolutionEngine
from genetic.fitness import FitnessEvaluator

class MockEvaluator(FitnessEvaluator):
    def evaluate(self, genome):
        return 100

class TestCaptureLogic(unittest.TestCase):
    def setUp(self):
        self.dmg_calc = DamageCalculator()
        
    def test_cannot_kill_flag(self):
        """Verify that abilities with cannot_kill=True leave at least 1 HP"""
        # Create ability with cannot_kill=True
        false_swipe = Ability(
            id=408, name="Weakening Blow", power=20, accuracy=100, speed=1, cooldown=0,
            family=PetFamily.BEAST, cannot_kill=True
        )
        
        # Create pets
        attacker = Pet(
            species_id=1, name="Attacker", family=PetFamily.BEAST, quality=PetQuality.RARE,
            stats=PetStats(max_hp=100, current_hp=100, power=100, speed=10), abilities=[false_swipe]
        )
        defender = Pet(
            species_id=2, name="Defender", family=PetFamily.CRITTER, quality=PetQuality.RARE,
            stats=PetStats(max_hp=100, current_hp=5, power=10, speed=10), abilities=[]
        )
        
        # Calculate damage (should be lethal normally, but capped)
        dmg, _ = self.dmg_calc.calculate_damage(false_swipe, attacker, defender)
        
        # Should deal 4 damage (leaving 1 HP)
        self.assertEqual(dmg, 4)
        self.assertEqual(defender.stats.current_hp - dmg, 1)
        
    def test_capture_agent_behavior(self):
        """Verify CaptureAgent avoids killing low HP targets"""
        agent = CaptureAgent(self.dmg_calc)
        
        # Ability that deals damage
        smack = Ability(id=1, name="Smack", power=20, accuracy=100, speed=1, cooldown=0, family=PetFamily.HUMANOID)
        
        # Attacker
        attacker = Pet(
            species_id=1, name="Attacker", family=PetFamily.HUMANOID, quality=PetQuality.RARE,
            stats=PetStats(max_hp=100, current_hp=100, power=100, speed=10), abilities=[smack]
        )
        
        # Defender with low HP (in capture range)
        defender = Pet(
            species_id=2, name="Defender", family=PetFamily.CRITTER, quality=PetQuality.RARE,
            stats=PetStats(max_hp=100, current_hp=10, power=10, speed=10), abilities=[]
        )
        
        state = BattleState(
            player_team=Team([attacker]),
            enemy_team=Team([defender])
        )
        
        # Agent should choose to PASS because attacking would kill
        action = agent.get_action(state)
        self.assertEqual(action.action_type, 'pass')
        
    def test_ga_capture_seeding(self):
        """Verify GA seeds capture teams in capture mode"""
        evaluator = MockEvaluator(target_team=None, ability_db={}, species_db={})
        engine = EvolutionEngine(evaluator, population_size=10)
        
        # Mock ability DB
        ability_db = {
            1180: [1, 2, 3], # Turnip
            1563: [4, 5, 6], # Corgi
            1204: [7, 8, 9]  # Snobold
        }
        
        # Add many dummy species to avoid random collision with seed
        available_species = [1180, 1563, 1204] + list(range(2000, 2100))
        
        engine.initialize_population(
            available_species, 
            ability_db, 
            capture_mode=True
        )
        
        # Check for Capture Seed (1180, 1563, 1204)
        # We added 3 copies
        capture_seeds = 0
        for genome in engine.population:
            pids = [p.species_id for p in genome.pets]
            if pids == [1180, 1563, 1204]:
                capture_seeds += 1
                
        self.assertEqual(capture_seeds, 2)
        
    def test_alternative_teams_generation(self):
        """Verify GA biases random generation towards safe pets in capture mode"""
        evaluator = MockEvaluator(target_team=None, ability_db={}, species_db={})
        engine = EvolutionEngine(evaluator, population_size=20)
        
        # Mock ability DB
        # 408 is Weakening Blow (Safe)
        # 1 is Smack (Unsafe)
        ability_db = {
            1001: [408], # Safe Pet 1
            1002: [408], # Safe Pet 2
            2001: [1],   # Unsafe Pet 1
            2002: [1]    # Unsafe Pet 2
        }
        
        available_species = [1001, 1002, 2001, 2002]
        
        # Run in capture mode
        engine.initialize_population(
            available_species, 
            ability_db, 
            capture_mode=True
        )
        
        # Check how many teams have a safe pet in slot 1
        safe_teams = 0
        for genome in engine.population:
            # Skip seeds (we know they work from previous test)
            # But wait, we didn't define the specific capture seeds (1180, etc) in available_species
            # So initialize_population won't add the hardcoded seeds.
            # It will only add random teams.
            
            # Check if first pet is safe (1001 or 1002)
            if genome.pets[0].species_id in [1001, 1002]:
                safe_teams += 1
                
        # We expect ~70% of teams to have a safe pet
        # With 20 teams, expected ~14.
        # Let's assert at least 50% (10) to be safe, accounting for RNG
        self.assertGreaterEqual(safe_teams, 10, f"Expected at least 10 safe teams, got {safe_teams}")

if __name__ == '__main__':
    unittest.main()
