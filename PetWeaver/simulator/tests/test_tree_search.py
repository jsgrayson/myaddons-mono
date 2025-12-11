
import unittest
from simulator.battle_state import Pet, PetStats, Ability, PetFamily, PetQuality, Buff, BuffType, BattleState, Team, TurnAction
from simulator.tree_search_agent import TreeSearchAgent

class TestTreeSearch(unittest.TestCase):
    def setUp(self):
        self.agent = TreeSearchAgent(depth=2, player_idx='player')
        
    def test_avoid_death(self):
        """Test that agent chooses to heal if attacking leads to death"""
        # Player: 15 HP. 
        # Abilities: 
        # 1. Attack (10 dmg)
        # 2. Heal (20 heal)
        
        # Enemy: 100 HP.
        # Abilities:
        # 1. Big Hit (20 dmg) - Will kill player if player doesn't heal
        
        p1 = Pet(
            species_id=1, name="Player", 
            stats=PetStats(100, 8, 10, 10), # 100 Max, 8 Current - Will die to 20 dmg hit
            family=PetFamily.HUMANOID, quality=PetQuality.RARE, 
            abilities=[
                Ability(id=1, name="Attack", power=10, accuracy=100, speed=0, family=PetFamily.HUMANOID, cooldown=0),
                Ability(id=2, name="Heal", power=20, accuracy=100, speed=0, family=PetFamily.HUMANOID, cooldown=0, is_heal=True)
            ]
        )
        
        p2 = Pet(
            species_id=2, name="Enemy", 
            stats=PetStats(100, 100, 10, 10),
            family=PetFamily.BEAST, quality=PetQuality.RARE, 
            abilities=[
                Ability(id=3, name="Big Hit", power=20, accuracy=100, speed=0, family=PetFamily.BEAST, cooldown=0)
            ]
        )
        
        state = BattleState(Team([p1]), Team([p2]))
        
        # Decision
        action = self.agent.decide(state)
        
        # Should choose Heal
        self.assertEqual(action.action_type, 'ability')
        self.assertEqual(action.ability.name, "Heal", "Agent should choose Heal to survive")

    def test_secure_kill(self):
        """Test that agent chooses ability that secures a kill"""
        # Player: 100 HP
        # Abilities:
        # 1. Small Hit (10 dmg)
        # 2. Big Hit (20 dmg)
        
        # Enemy: 15 HP
        
        p1 = Pet(
            species_id=1, name="Player", 
            stats=PetStats(100, 100, 10, 10),
            family=PetFamily.HUMANOID, quality=PetQuality.RARE, 
            abilities=[
                Ability(id=1, name="Small Hit", power=10, accuracy=100, speed=0, family=PetFamily.HUMANOID, cooldown=0),
                Ability(id=2, name="Big Hit", power=20, accuracy=100, speed=0, family=PetFamily.HUMANOID, cooldown=0)
            ]
        )
        
        p2 = Pet(
            species_id=2, name="Enemy", 
            stats=PetStats(15, 100, 10, 10), # 15 HP
            family=PetFamily.BEAST, quality=PetQuality.RARE, 
            abilities=[
                Ability(id=3, name="Scratch", power=5, accuracy=100, speed=0, family=PetFamily.BEAST, cooldown=0)
            ]
        )
        
        state = BattleState(Team([p1]), Team([p2]))
        
        # Decision
        action = self.agent.decide(state)
        
        # Should choose Big Hit to kill (Enemy has 15 HP, Small Hit does 10, Big Hit does 20)
        # Note: Damage calculation might vary slightly due to variance/modifiers, but 20 vs 10 is big enough gap.
        # Assuming standard damage calc: 20 power * (10/20) = 10 dmg? 
        # Wait, damage formula: power * (attacker_power / 20).
        # Attacker power is 10. 
        # Small Hit: 10 * (10/20) = 5 dmg.
        # Big Hit: 20 * (10/20) = 10 dmg.
        # Enemy has 15 HP. Neither kills in one hit?
        # Let's bump up Attacker Power to 20.
        # Small Hit: 10 * (20/20) = 10 dmg.
        # Big Hit: 20 * (20/20) = 20 dmg.
        # Enemy 15 HP. Big Hit kills. Small Hit doesn't.
        
        p1.stats.power = 20
        
        action = self.agent.decide(state)
        
        self.assertEqual(action.action_type, 'ability')
        self.assertEqual(action.ability.name, "Big Hit", "Agent should choose Big Hit to secure kill")

if __name__ == '__main__':
    unittest.main()
