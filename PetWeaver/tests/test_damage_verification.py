import unittest
from simulator import BattleState, Team, Pet, PetStats, Ability, PetFamily, PetQuality
from simulator.damage_calculator import DamageCalculator

class TestDamageVerification(unittest.TestCase):
    def setUp(self):
        self.calc = DamageCalculator(rng_seed=42)
        
        # Standard Level 25 Rare Pet Stats (approximate)
        # Power 300 is typical for a P/P breed
        self.attacker_stats = PetStats(max_hp=1400, current_hp=1400, power=300, speed=280)
        self.attacker = Pet(
            species_id=1, name="Attacker", family=PetFamily.BEAST, quality=PetQuality.RARE,
            stats=self.attacker_stats, abilities=[]
        )
        
        self.defender_stats = PetStats(max_hp=1400, current_hp=1400, power=300, speed=280)
        self.defender = Pet(
            species_id=2, name="Defender", family=PetFamily.CRITTER, quality=PetQuality.RARE,
            stats=self.defender_stats, abilities=[]
        )
        
    def test_basic_damage(self):
        # Ability with 20 power
        # Formula: Power * (PetPower / 20)
        # 20 * (300 / 20) = 300 damage
        ability = Ability(id=1, name="Test Attack", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.BEAST)
        
        damage, details = self.calc.calculate_damage(ability, self.attacker, self.defender)
        
        # Beast vs Critter is 1.5x
        expected_base = 300
        expected_damage = int(expected_base * 1.5) # 450
        
        # Allow for variance +/- 30% (accounting for RNG and quality multipliers)
        min_dmg = int(expected_damage * 0.70)
        max_dmg = int(expected_damage * 1.30)
        
        print(f"Damage: {damage} (Expected ~{expected_damage})")
        self.assertTrue(min_dmg <= damage <= max_dmg, f"Damage {damage} not in range {min_dmg}-{max_dmg}")
        
        # Verify quality multiplier is 1.0 (not applied)
        self.assertEqual(details['quality_multiplier'], 1.0)

if __name__ == '__main__':
    unittest.main()
