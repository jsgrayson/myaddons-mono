
import unittest
from simulator.battle_state import Pet, PetStats, Ability, PetFamily, PetQuality, Buff, BuffType
from simulator.damage_calculator import DamageCalculator
from simulator.racial_passives import RacialPassives

class TestDamageMath(unittest.TestCase):
    def setUp(self):
        self.calc = DamageCalculator(rng_seed=42)
        
        # Create dummy pets
        self.attacker = Pet(
            species_id=1, name="Attacker", 
            stats=PetStats(100, 100, 10, 10),
            family=PetFamily.HUMANOID, quality=PetQuality.RARE, abilities=[]
        )
        self.defender = Pet(
            species_id=2, name="Defender", 
            stats=PetStats(100, 100, 10, 10),
            family=PetFamily.BEAST, quality=PetQuality.RARE, abilities=[]
        )

    def test_magic_cap_single_hit(self):
        """Test Magic racial cap on single hit"""
        # Magic Pet with 100 HP
        self.defender.family = PetFamily.MAGIC
        self.defender.stats.max_hp = 100
        self.defender.stats.current_hp = 100
        
        # Ability dealing 50 damage (50% HP)
        # We need to force the damage calculator to output 50 before cap.
        # Base damage = power * (attacker_power / 20)
        # 100 * (10 / 20) = 50
        ability = Ability(
            id=1, name="Big Hit", power=100, accuracy=100, speed=10, cooldown=0,
            family=PetFamily.HUMANOID, hits=1
        )
        
        # Mock family multiplier to 1.0 (Humanoid vs Magic is neutral)
        # Mock racial/quality to 1.0
        # Mock variance to 1.0 (by seeding or mocking)
        # Actually, let's just use the calculator and check if result is <= 35
        
        # Note: Variance is random.uniform(0.95, 1.05).
        # Even with variance, 50 * 0.95 = 47.5 > 35.
        # So it should always be capped at 35.
        
        damage, details = self.calc.calculate_damage(ability, self.attacker, self.defender)
        
        self.assertEqual(damage, 35, f"Damage should be capped at 35, got {damage}")

    def test_magic_cap_multi_hit(self):
        """Test Magic racial cap on multi-hit ability"""
        # Magic Pet with 100 HP
        self.defender.family = PetFamily.MAGIC
        self.defender.stats.max_hp = 100
        
        # Ability dealing 50 damage TOTAL (2 hits of 25)
        # Each hit is 25 (25% HP), which is < 35% cap.
        # So total damage should be 50 (uncapped).
        
        # Wait, calculate_damage returns TOTAL damage.
        # Does it handle multi-hit logic internally?
        # Currently, calculate_damage calculates ONE damage value based on power.
        # If ability.hits > 1, does it mean "Power is per hit" or "Power is total"?
        # Standard WoW convention: Power is usually per hit for multi-hit moves in data,
        # OR the ability description says "Hits 3 times for X".
        # In this simulator, I need to decide or check usage.
        # Looking at `calculate_damage`:
        # `base_damage = ability.power * ...`
        # It doesn't loop for hits. It just calculates once.
        # So `calculate_damage` returns damage for ONE hit instance?
        # OR does it return total?
        # If `simulator.py` calls it once per ability use, and `calculate_damage` doesn't loop,
        # then `calculate_damage` is calculating the TOTAL damage if `ability.power` is total,
        # OR it's calculating PER HIT damage if `ability.power` is per hit.
        
        # Let's assume `ability.power` is TOTAL damage for now, as is common in simple sims,
        # UNLESS `hits` is used to split it.
        # BUT, `calculate_damage` currently ignores `hits`.
        # So if I pass power=100, it calculates ~50 damage.
        # If I say `hits=2`, it still calculates ~50 damage.
        # The Magic Cap logic I'm testing needs to know this.
        
        # If I implement the fix, `calculate_damage` should use `hits` to apply cap per hit.
        # So if power=100 (50 dmg), hits=2 -> 25 dmg per hit.
        # Cap is 35. 25 < 35. So total = 50.
        # If I didn't split it, 50 > 35, so cap = 35.
        # So the test expects 50 (uncapped total) because per-hit is low.
        
        ability = Ability(
            id=2, name="Multi Hit", power=100, accuracy=100, speed=10, cooldown=0,
            family=PetFamily.HUMANOID, hits=2
        )
        
        damage, details = self.calc.calculate_damage(ability, self.attacker, self.defender)
        
        # With variance, 50 +/- 5%. All below 35? No.
        # 50 total -> 25 per hit. 25 is well below 35.
        # So result should be around 50.
        # If capped blindly, it would be 35.
        
        self.assertGreater(damage, 40, f"Damage {damage} should not be capped at 35")

    def test_multiplicative_modifiers(self):
        """Test that modifiers stack multiplicatively"""
        # Base damage 50 (Power 100)
        ability = Ability(
            id=3, name="Mod Hit", power=100, accuracy=100, speed=10, cooldown=0,
            family=PetFamily.HUMANOID, hits=1
        )
        
        # Add +50% damage buff to attacker (1.5x)
        buff1 = Buff(type=BuffType.STAT_MOD, duration=3, magnitude=1.5, stat_affected='power') # Actually power buff affects attacker_power
        # Wait, power buff affects `attacker.get_effective_power()`.
        # `base_damage = ability.power * (attacker_power / 20)`
        # So 1.5x power -> 1.5x damage. Correct.
        self.attacker.active_buffs.append(buff1)
        
        # Add -50% damage taken buff to defender (0.5x)
        buff2 = Buff(type=BuffType.STAT_MOD, duration=3, magnitude=0.5, stat_affected='damage_taken')
        self.defender.active_buffs.append(buff2)
        
        # Expected: 50 * 1.5 * 0.5 = 37.5
        # If additive: 1 + 0.5 - 0.5 = 1.0 -> 50? No, they are different stats.
        # Power buff increases base damage. Damage taken reduces final.
        # They are naturally multiplicative in the formula.
        
        # Let's try two damage taken buffs?
        # Buff 1: 0.5 (Shield)
        # Buff 2: 0.5 (Another Shield)
        # Multiplicative: 0.5 * 0.5 = 0.25
        # Additive: 1 - 0.5 - 0.5 = 0? Or 0.5 + 0.5 reduction?
        
        self.defender.active_buffs = []
        buff_shield1 = Buff(type=BuffType.STAT_MOD, duration=3, magnitude=0.5, stat_affected='damage_taken')
        buff_shield2 = Buff(type=BuffType.STAT_MOD, duration=3, magnitude=0.5, stat_affected='damage_taken')
        self.defender.active_buffs.append(buff_shield1)
        self.defender.active_buffs.append(buff_shield2)
        
        # Reset attacker buff
        self.attacker.active_buffs = []
        
        damage, details = self.calc.calculate_damage(ability, self.attacker, self.defender)
        
        # Base ~50.
        # Multiplicative: 50 * 0.25 = 12.5.
        # Additive (if implemented wrong): 50 * 0 = 0? Or 50 * (1 - 0.5 - 0.5)?
        
        # The current code loops and does `damage_reduction *= buff.magnitude`.
        # So it IS multiplicative.
        # This test just confirms it.
        
        self.assertLess(damage, 20, f"Damage {damage} should be heavily reduced (approx 12.5)")
        self.assertGreater(damage, 5, "Damage should not be 0")

if __name__ == '__main__':
    unittest.main()
