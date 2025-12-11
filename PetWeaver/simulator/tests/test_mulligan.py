
import unittest
from simulator.battle_state import Pet, PetStats, Ability, PetFamily, PetQuality, Buff, BuffType, BattleState, Team, TurnAction
from simulator.simulator import BattleSimulator

class TestMulligan(unittest.TestCase):
    def setUp(self):
        self.sim = BattleSimulator()
        
        # Define dummy agents
        self.player_agent = lambda state: TurnAction('player', 'ability', ability=state.player_team.get_active_pet().abilities[0])
        self.enemy_agent = lambda state: TurnAction('enemy', 'ability', ability=state.enemy_team.get_active_pet().abilities[0])

    def test_mulligan_type_advantage(self):
        """Test that Mulligan chooses pet with type advantage"""
        # Enemy: Elemental (Weak to Aquatic, Strong vs Mechanical)
        enemy_pet = Pet(
            species_id=1, name="Elemental Enemy", 
            stats=PetStats(100, 100, 10, 10),
            family=PetFamily.ELEMENTAL, quality=PetQuality.RARE, 
            abilities=[Ability(id=1, name="Burn", power=10, accuracy=100, speed=0, family=PetFamily.ELEMENTAL, cooldown=0)]
        )
        
        # Player Team:
        # 0. Mechanical (Weak vs Elemental)
        # 1. Aquatic (Strong vs Elemental)
        # 2. Critter (Neutral)
        
        p0 = Pet(
            species_id=2, name="Mech (Weak)", 
            stats=PetStats(100, 100, 10, 10),
            family=PetFamily.MECHANICAL, quality=PetQuality.RARE, 
            abilities=[Ability(id=2, name="Hit", power=10, accuracy=100, speed=0, family=PetFamily.MECHANICAL, cooldown=0)]
        )
        p1 = Pet(
            species_id=3, name="Aqua (Strong)", 
            stats=PetStats(100, 100, 10, 10),
            family=PetFamily.AQUATIC, quality=PetQuality.RARE, 
            abilities=[Ability(id=3, name="Splash", power=10, accuracy=100, speed=0, family=PetFamily.AQUATIC, cooldown=0)]
        )
        p2 = Pet(
            species_id=4, name="Critter (Neutral)", 
            stats=PetStats(100, 100, 10, 10),
            family=PetFamily.CRITTER, quality=PetQuality.RARE, 
            abilities=[Ability(id=4, name="Scratch", power=10, accuracy=100, speed=0, family=PetFamily.CRITTER, cooldown=0)]
        )
        
        state = BattleState(Team([p0, p1, p2]), Team([enemy_pet]))
        
        # Run Mulligan
        best_idx = self.sim.simulate_mulligan(state, self.player_agent, self.enemy_agent, depth=3)
        
        # Should choose index 1 (Aquatic) because it deals more damage (Strong) and takes less (Weak)
        # Elemental deals 1.0 to Aquatic (Wait, Aquatic takes 1.0 from Elemental? No.)
        # Aquatic takes 0.67 from Elemental? No.
        # Elemental > Mechanical (1.5).
        # Aquatic > Elemental (1.5).
        # Elemental vs Aquatic:
        # Elemental attacks Aquatic: 1.0 (Neutral).
        # Aquatic attacks Elemental: 1.5 (Strong).
        
        # Mechanical vs Elemental:
        # Mech attacks Elemental: 0.67 (Weak).
        # Elemental attacks Mech: 1.5 (Strong).
        
        # So Aquatic is clearly better.
        self.assertEqual(best_idx, 1, "Mulligan should choose Aquatic (Type Advantage)")

    def test_mulligan_kill_potential(self):
        """Test that Mulligan chooses pet that can kill quickly"""
        # Enemy: Low HP
        enemy_pet = Pet(
            species_id=1, name="Weak Enemy", 
            stats=PetStats(20, 100, 10, 10), # 20 HP
            family=PetFamily.BEAST, quality=PetQuality.RARE, 
            abilities=[Ability(id=1, name="Bite", power=5, accuracy=100, speed=0, family=PetFamily.BEAST, cooldown=0)]
        )
        
        # Player Team:
        # 0. Weak Hitter (10 dmg) - Needs 2 turns
        # 1. Strong Hitter (20 dmg) - Needs 1 turn
        
        p0 = Pet(
            species_id=2, name="Weak Hitter", 
            stats=PetStats(100, 100, 10, 10),
            family=PetFamily.BEAST, quality=PetQuality.RARE, 
            abilities=[Ability(id=2, name="Weak Hit", power=10, accuracy=100, speed=0, family=PetFamily.BEAST, cooldown=0)]
        )
        p1 = Pet(
            species_id=3, name="Strong Hitter", 
            stats=PetStats(100, 100, 10, 10),
            family=PetFamily.BEAST, quality=PetQuality.RARE, 
            abilities=[Ability(id=3, name="Strong Hit", power=20, accuracy=100, speed=0, family=PetFamily.BEAST, cooldown=0)]
        )
        
        state = BattleState(Team([p0, p1]), Team([enemy_pet]))
        
        # Run Mulligan
        best_idx = self.sim.simulate_mulligan(state, self.player_agent, self.enemy_agent, depth=2)
        
        # Should choose index 1 (Strong Hitter) because it kills in 1 turn -> less damage taken
        self.assertEqual(best_idx, 1, "Mulligan should choose Strong Hitter (Kill Potential)")

if __name__ == '__main__':
    unittest.main()
