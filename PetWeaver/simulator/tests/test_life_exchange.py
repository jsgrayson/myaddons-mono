
import unittest
from simulator.battle_state import Pet, PetStats, Ability, PetFamily, PetQuality, Buff, BuffType
from simulator.simulator import BattleSimulator
from simulator.special_encounters import SpecialEncounterHandler

class TestLifeExchange(unittest.TestCase):
    def setUp(self):
        self.sim = BattleSimulator(rng_seed=42)
        
        # Attacker: Magic Pet (1000 HP)
        self.attacker = Pet(
            species_id=1, name="MagicAttacker", 
            stats=PetStats(1000, 1000, 10, 10),
            family=PetFamily.MAGIC, quality=PetQuality.RARE, abilities=[]
        )
        
        # Defender: Beast Pet (100 HP)
        self.defender = Pet(
            species_id=2, name="BeastDefender", 
            stats=PetStats(100, 100, 10, 10),
            family=PetFamily.BEAST, quality=PetQuality.RARE, abilities=[]
        )

    def test_life_exchange_ignores_magic_cap(self):
        """Test Life Exchange ignores Magic racial cap (35% max HP)"""
        # Setup:
        # Attacker (Magic): 1000/1000 HP (100%)
        # Defender (Beast): 10/100 HP (10%)
        
        self.attacker.stats.current_hp = 1000
        self.defender.stats.current_hp = 10
        
        # Life Exchange should swap percentages:
        # Attacker becomes 10% -> 100 HP (Loss of 900 HP)
        # Defender becomes 100% -> 100 HP (Gain of 90 HP)
        
        # If Magic cap applied to Attacker (who is losing HP), 
        # max damage would be 35% of 1000 = 350.
        # So Attacker would drop to 650 HP instead of 100.
        
        SpecialEncounterHandler.apply_life_exchange(self.attacker, self.defender)
        
        self.assertEqual(self.attacker.stats.current_hp, 100, 
                         f"Attacker HP should be 100 (10%), got {self.attacker.stats.current_hp}. Magic cap likely applied incorrectly.")
        self.assertEqual(self.defender.stats.current_hp, 100,
                         f"Defender HP should be 100 (100%), got {self.defender.stats.current_hp}")

    def test_life_exchange_ignores_shields(self):
        """Test Life Exchange ignores damage reduction shields"""
        # Setup:
        # Attacker: 1000/1000 HP (100%)
        # Defender: 10/100 HP (10%)
        # Attacker has 50% damage reduction shield
        
        self.attacker.stats.current_hp = 1000
        self.defender.stats.current_hp = 10
        
        shield = Buff(type=BuffType.STAT_MOD, duration=3, magnitude=0.5, stat_affected='damage_taken')
        self.attacker.active_buffs.append(shield)
        
        # Life Exchange swap:
        # Attacker loses 900 HP.
        # If shield applied, loss would be 450 HP -> 550 HP remaining.
        # Should be 100 HP remaining (shield ignored).
        
        SpecialEncounterHandler.apply_life_exchange(self.attacker, self.defender)
        
        self.assertEqual(self.attacker.stats.current_hp, 100,
                         f"Attacker HP should be 100 (shield ignored), got {self.attacker.stats.current_hp}")

    def test_simulator_integration(self):
        """Test that Simulator correctly routes Life Exchange"""
        # Setup similar to above
        self.attacker.stats.current_hp = 1000
        self.defender.stats.current_hp = 10
        
        # Create Life Exchange ability
        ability = Ability(
            id=284, name="Life Exchange", power=0, accuracy=100, speed=10, cooldown=0,
            family=PetFamily.MAGIC, hits=1
        )
        
        # Mock action
        from simulator.battle_state import TurnAction, BattleState, Team
        
        # Manually call execute_action
        # We need a dummy state
        state = BattleState(Team([self.attacker]), Team([self.defender]))
        action = TurnAction('player', 'ability', ability=ability)
        
        self.sim.execute_action(action, self.attacker, self.defender, state.player_team, state, None, 1)
        
        self.assertEqual(self.attacker.stats.current_hp, 100, "Simulator did not apply Life Exchange correctly")

if __name__ == '__main__':
    unittest.main()
