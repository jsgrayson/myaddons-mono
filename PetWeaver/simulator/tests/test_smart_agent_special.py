import unittest
from simulator.battle_state import BattleState, Team, Pet, PetStats, PetFamily, PetQuality, Ability, Buff, BuffType
from simulator.smart_agent import SmartAgent
from simulator.special_encounters import SpecialEncounterHandler

class TestSmartAgentSpecial(unittest.TestCase):
    def setUp(self):
        self.agent = SmartAgent(difficulty=1.0)
        
        # Create dummy pets
        self.pet1 = Pet(1, "Pet1", PetFamily.BEAST, PetQuality.RARE, PetStats(1000, 200, 300, 300), []) # Low HP
        self.enemy1 = Pet(2, "Enemy1", PetFamily.CRITTER, PetQuality.RARE, PetStats(1000, 1000, 300, 300), [])
        
        self.team_player = Team([self.enemy1]) # From agent's perspective, player is enemy
        self.team_enemy = Team([self.pet1]) # Agent controls enemy team
        
        self.state = BattleState(
            player_team=self.team_player,
            enemy_team=self.team_enemy,
            weather=None,
            turn_number=1
        )
        
    def test_healing_reduction_logic(self):
        """Test that agent avoids healing when reduced"""
        # Abilities: Weak Attack (10 dmg), Strong Heal (500 heal)
        attack = Ability(1, "Attack", 10, 100, 0, 0, PetFamily.BEAST)
        heal = Ability(2, "Heal", 100, 100, 0, 0, PetFamily.BEAST, is_heal=True)
        self.pet1.abilities = [attack, heal]
        
        # Case 1: No reduction. Should Heal because HP is low (200/1000)
        action = self.agent.decide(self.state)
        self.assertEqual(action.action_type, 'ability')
        self.assertEqual(action.ability.name, "Heal", "Should heal when low HP and no debuff")
        
        # Case 2: 100% Reduction. Should Attack because Heal value is 0
        SpecialEncounterHandler.apply_healing_reduction(self.pet1, reduction_pct=1.0, duration=3)
        
        action = self.agent.decide(self.state)
        self.assertEqual(action.action_type, 'ability')
        self.assertEqual(action.ability.name, "Attack", "Should attack when healing is 100% reduced")

    def test_futile_heal(self):
        """Test that agent avoids healing if it will die anyway"""
        # Pet has 10 HP. Enemy does ~450 dmg (300 power * 1.5).
        # Heal does 100 * 5 = 500.
        # If we heal, we have 510 HP. We survive. Should Heal.
        
        # Scenario 1: Heal saves us
        attack = Ability(1, "Attack", 10, 100, 0, 0, PetFamily.BEAST)
        heal = Ability(2, "Heal", 100, 100, 0, 0, PetFamily.BEAST, is_heal=True)
        self.pet1.abilities = [attack, heal]
        self.pet1.stats.current_hp = 10
        
        # Enemy power is 300. Est dmg = 450.
        # Heal = 500. New HP = 510 > 450. Survive.
        
        action = self.agent.decide(self.state)
        self.assertEqual(action.ability.name, "Heal", "Should heal to survive")
        
        # Scenario 2: Heal is too weak (Futile)
        # Reduce heal power to 10 (Heal = 50).
        # New HP = 60 < 450. Die anyway.
        weak_heal = Ability(2, "Weak Heal", 10, 100, 0, 0, PetFamily.BEAST, is_heal=True)
        self.pet1.abilities = [attack, weak_heal]
        
        action = self.agent.decide(self.state)
        self.assertEqual(action.ability.name, "Attack", "Should attack if heal is futile")

    def test_faster_kill_priority(self):
        """Test that agent prioritizes killing if faster, even if low HP"""
        # Pet has 10 HP. Enemy has 10 HP.
        # Pet Speed 300 > Enemy Speed 250.
        # We can kill with Attack.
        # We can also Heal.
        # Logic should choose Attack because we are faster and it kills.
        
        attack = Ability(1, "Attack", 20, 100, 0, 0, PetFamily.BEAST) # Kills enemy (10 HP)
        heal = Ability(2, "Heal", 100, 100, 0, 0, PetFamily.BEAST, is_heal=True)
        self.pet1.abilities = [attack, heal]
        self.pet1.stats.current_hp = 10
        self.pet1.stats.speed = 300
        
        self.enemy1.stats.current_hp = 10
        self.enemy1.stats.speed = 250
        
        # Ensure we are faster
        self.assertTrue(self.pet1.stats.speed > self.enemy1.stats.speed)
        
        action = self.agent.decide(self.state)
        self.assertEqual(action.ability.name, "Attack", "Should choose Attack to secure kill because faster")

if __name__ == '__main__':
    unittest.main()
