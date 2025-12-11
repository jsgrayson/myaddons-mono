import unittest
from simulator.battle_state import Pet, PetStats, PetFamily, Buff, BuffType, Ability, PetQuality
from simulator.buff_tracker import BuffTracker
from simulator.damage_calculator import DamageCalculator

class TestAbilityUpdates(unittest.TestCase):
    
    def setUp(self):
        # Create dummy pets
        self.pet = Pet(
            species_id=1, name="TestPet", family=PetFamily.BEAST,
            quality=PetQuality.RARE,
            stats=PetStats(1000, 1000, 300, 300),
            abilities=[]
        )
        self.attacker = Pet(
            species_id=2, name="Attacker", family=PetFamily.BEAST,
            quality=PetQuality.RARE,
            stats=PetStats(1000, 1000, 300, 300),
            abilities=[]
        )
        self.damage_calc = DamageCalculator(rng_seed=42)
        
    def test_cleansing_rain(self):
        """Test that Cleansing Rain reduces DoT duration by 1"""
        # Create a DoT buff (duration 3)
        dot = Buff(type=BuffType.DOT, name="Poison", duration=3, magnitude=10, source_ability="Poison Spit", stat_affected="hp")
        
        # Create Cleansing Rain weather buff
        rain = Buff(type=BuffType.WEATHER, name="Cleansing Rain", duration=9, magnitude=0, source_ability="Cleansing Rain", stat_affected="none")
        
        # Add DoT with Rain active
        BuffTracker.add_buff(self.pet, dot, weather=rain)
        
        # Verify duration is 2 (3 - 1)
        self.assertEqual(self.pet.active_buffs[0].duration, 2)
        
        # Test reducing duration to 0 prevents addition
        short_dot = Buff(type=BuffType.DOT, name="Short Poison", duration=1, magnitude=10, source_ability="Poison Spit", stat_affected="hp")
        BuffTracker.add_buff(self.pet, short_dot, weather=rain)
        
        # Should NOT be added
        self.assertEqual(len(self.pet.active_buffs), 1) # Only the previous one
        
    def test_decoy(self):
        """Test that Decoy blocks damage and consumes a stack"""
        # Add Decoy buff (2 stacks)
        decoy = Buff(type=BuffType.BLOCK, name="Decoy", duration=5, magnitude=0, source_ability="Decoy", stat_affected="none")
        decoy.stacks = 2
        self.pet.active_buffs.append(decoy)
        
        # Calculate damage
        ability = Ability(1, "Attack", 100, 100, 0, 0, PetFamily.BEAST)
        damage, details = self.damage_calc.calculate_damage(ability, self.attacker, self.pet)
        
        # Verify blocked
        self.assertEqual(damage, 0)
        self.assertTrue(details['blocked'])
        
        # Verify stack consumed
        self.assertEqual(self.pet.active_buffs[0].stacks, 1)
        
        # Hit again
        damage, details = self.damage_calc.calculate_damage(ability, self.attacker, self.pet)
        self.assertEqual(damage, 0)
        
        # Verify buff removed (stacks 0)
        self.assertEqual(len(self.pet.active_buffs), 0)
        
    def test_howl(self):
        """Test that Howl doubles damage taken"""
        # Add Howl buff (damage_taken * 2.0)
        howl = Buff(type=BuffType.STAT_MOD, name="Howl", duration=2, magnitude=2.0, source_ability="Howl", stat_affected="damage_taken")
        self.pet.active_buffs.append(howl)
        
        # Calculate damage
        ability = Ability(1, "Attack", 20, 100, 0, 0, PetFamily.BEAST)
        # Base damage approx: 20 * (300/20) = 300
        # With Howl: 600
        
        damage, details = self.damage_calc.calculate_damage(ability, self.attacker, self.pet)
        
        # Check if damage is roughly double base
        # Base damage in details is before multipliers
        base = details['base_damage']
        expected = base * 2.0
        
        # Allow for variance and other multipliers (Family 1.0, Quality 1.0)
        # We just want to see the damage reduction multiplier was applied
        # But calculate_damage applies it at the end.
        
        # Let's check if final damage is > base * 1.8
        self.assertGreater(damage, base * 1.8)
        
    def test_delayed_effect(self):
        """Test Geyser delayed stun and damage"""
        # Add Delayed Effect (Geyser)
        geyser = Buff(type=BuffType.DELAYED_EFFECT, name="Delayed: Geyser", duration=1, magnitude=100, source_ability="Geyser", stat_affected="none")
        self.pet.active_buffs.append(geyser)
        
        # Tick buffs (decrement duration)
        # Duration 1 -> 0 -> Trigger
        events = BuffTracker.decrement_durations(self.pet)
        
        # Verify events
        damage_event = next((e for e in events if e['type'] == 'delayed_damage'), None)
        cc_event = next((e for e in events if e.get('type') == 'cc_applied'), None)
        
        self.assertIsNotNone(damage_event)
        self.assertEqual(damage_event['amount'], 100)
        
        self.assertIsNotNone(cc_event)
        self.assertEqual(cc_event['cc'], 'Stun')
        
        # Verify Stun buff applied
        self.assertTrue(any(b.type == BuffType.STUN for b in self.pet.active_buffs))

if __name__ == '__main__':
    unittest.main()
