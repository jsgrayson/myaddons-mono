
import unittest
from simulator.battle_state import Pet, PetStats, Ability, PetFamily, PetQuality, Buff, BuffType, TurnAction
from simulator.turn_system import TurnSystem
from simulator.damage_calculator import DamageCalculator

class TestStatConstraints(unittest.TestCase):
    def setUp(self):
        self.turn_system = TurnSystem(rng_seed=42)
        self.damage_calc = DamageCalculator(rng_seed=42)
        
        self.p1 = Pet(
            species_id=1, name="P1", 
            stats=PetStats(100, 100, 10, 10),
            family=PetFamily.HUMANOID, quality=PetQuality.RARE, abilities=[]
        )
        self.p2 = Pet(
            species_id=2, name="P2", 
            stats=PetStats(100, 100, 10, 10),
            family=PetFamily.BEAST, quality=PetQuality.RARE, abilities=[]
        )

    def test_speed_tie_rng(self):
        """Test that equal speed results in ~50/50 turn order"""
        # Set equal speed
        self.p1.stats.speed = 100
        self.p2.stats.speed = 100
        
        p1_first_count = 0
        iterations = 1000
        
        # Create dummy actions
        action1 = TurnAction('player', 'ability', ability=Ability(id=1, name="A1", power=10, accuracy=100, speed=0, family=PetFamily.HUMANOID, cooldown=0))
        action2 = TurnAction('enemy', 'ability', ability=Ability(id=2, name="A2", power=10, accuracy=100, speed=0, family=PetFamily.BEAST, cooldown=0))
        
        # We need a fresh TurnSystem for each iteration to get different RNG?
        # Or just call determine_turn_order repeatedly.
        # The TurnSystem uses self.rng initialized with seed 42.
        # If we keep using the same instance, it will produce a sequence.
        # We want to check the distribution of that sequence.
        
        for _ in range(iterations):
            order = self.turn_system.determine_turn_order(self.p1, action1, self.p2, action2)
            if order[0][0] == 'player':
                p1_first_count += 1
        
        # Check if within 45%-55% range
        percentage = p1_first_count / iterations
        print(f"Speed Tie P1 First: {percentage*100}%")
        self.assertGreater(percentage, 0.45, "P1 should go first > 45% of time")
        self.assertLess(percentage, 0.55, "P1 should go first < 55% of time")

    def test_accuracy_overcap(self):
        """Test that >100% accuracy counters penalties"""
        # Ability with 110% accuracy
        ability = Ability(id=1, name="Precise Hit", power=10, accuracy=110, speed=0, family=PetFamily.HUMANOID, cooldown=0)
        
        # Weather penalty (-10%)
        weather = Buff(type=BuffType.WEATHER, duration=5, magnitude=0, stat_affected='darkness')
        
        # Attacker/Defender setup
        attacker = self.p1
        defender = self.p2
        
        # Run 100 attacks
        hits = 0
        iterations = 100
        
        for _ in range(iterations):
            hit = self.damage_calc.check_hit(ability, attacker, defender, weather)
            if hit:
                hits += 1
        
        # Should be 100% hit rate
        # 110 + (-10) - 0 = 100%
        self.assertEqual(hits, iterations, "Should hit 100% of the time with overcapped accuracy")

    def test_accuracy_penalty(self):
        """Test that normal accuracy is penalized"""
        # Ability with 100% accuracy
        ability = Ability(id=1, name="Normal Hit", power=10, accuracy=100, speed=0, family=PetFamily.HUMANOID, cooldown=0)
        
        # Weather penalty (-10%)
        weather = Buff(type=BuffType.WEATHER, duration=5, magnitude=0, stat_affected='darkness')
        
        attacker = self.p1
        defender = self.p2
        
        hits = 0
        iterations = 1000
        
        for _ in range(iterations):
            hit = self.damage_calc.check_hit(ability, attacker, defender, weather)
            if hit:
                hits += 1
        
        # Should be ~90% hit rate
        percentage = hits / iterations
        print(f"Penalty Hit Rate: {percentage*100}%")
        self.assertGreater(percentage, 0.85, "Should hit > 85% of time")
        self.assertLess(percentage, 0.95, "Should hit < 95% of time")

if __name__ == '__main__':
    unittest.main()
