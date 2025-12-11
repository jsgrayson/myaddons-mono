import unittest
from simulator.battle_state import BattleState, Team, Pet, PetStats, PetFamily, PetQuality, Ability, Buff, BuffType
from simulator.smart_agent import SmartAgent

class TestSmartAgent(unittest.TestCase):
    def setUp(self):
        self.agent = SmartAgent(difficulty=1.0)
        
        # Create dummy pets
        self.pet1 = Pet(1, "Pet1", PetFamily.BEAST, PetQuality.RARE, PetStats(1000, 1000, 300, 300), [])
        self.pet2 = Pet(2, "Pet2", PetFamily.FLYING, PetQuality.RARE, PetStats(1000, 1000, 300, 300), [])
        self.enemy1 = Pet(3, "Enemy1", PetFamily.CRITTER, PetQuality.RARE, PetStats(1000, 1000, 300, 300), [])
        
        self.team_player = Team([self.enemy1]) # From agent's perspective, player is enemy
        self.team_enemy = Team([self.pet1, self.pet2]) # Agent controls enemy team
        
        self.state = BattleState(
            player_team=self.team_player,
            enemy_team=self.team_enemy,
            weather=None,
            turn_number=1
        )
        
    def test_level_1_swap_dead(self):
        """Test forced swap when active pet is dead"""
        self.pet1.stats.current_hp = 0
        action = self.agent.decide(self.state)
        self.assertEqual(action.action_type, 'swap')
        self.assertEqual(action.target_pet_index, 1) # Swap to Pet2
        
    def test_level_1_rocko_smash(self):
        """Test Rocko prioritizes Smash"""
        rocko = Pet(99, "Rocko", PetFamily.ELEMENTAL, PetQuality.RARE, PetStats(1000, 1000, 300, 300), [])
        smash = Ability(1, "Smash", 100, 100, 0, 0, PetFamily.ELEMENTAL)
        other = Ability(2, "Other", 10, 100, 0, 0, PetFamily.ELEMENTAL)
        rocko.abilities = [smash, other]
        
        self.team_enemy.pets = [rocko]
        self.state.enemy_team.active_pet_index = 0
        
        action = self.agent.decide(self.state)
        self.assertEqual(action.action_type, 'ability')
        self.assertEqual(action.ability.name, "Smash")
        
    def test_level_2_execute(self):
        """Test Execute logic (kill low HP enemy)"""
        # Enemy (Player's pet) at low HP
        # Max HP 1000. 30% is 300.
        # Set HP to 50 (well below 30% threshold)
        # Both abilities can kill, but we want to test that Execute logic triggers
        self.enemy1.stats.current_hp = 50
        
        # Agent has Kill Shot (100 dmg) and Weak Shot (10 dmg)
        # Put kill_shot first so it's found first by _find_kill_ability
        kill_shot = Ability(1, "Kill", 100, 100, 0, 0, PetFamily.BEAST)
        weak_shot = Ability(2, "Weak", 10, 100, 0, 0, PetFamily.BEAST)
        self.pet1.abilities = [kill_shot, weak_shot]
        
        action = self.agent.decide(self.state)
        self.assertEqual(action.action_type, 'ability')
        self.assertEqual(action.ability.name, "Kill")
        
    def test_level_2_black_claw(self):
        """Test Black Claw usage"""
        black_claw = Ability(1, "Black Claw", 0, 100, 3, 0, PetFamily.BEAST)
        scratch = Ability(2, "Scratch", 10, 100, 0, 0, PetFamily.BEAST)
        self.pet1.abilities = [scratch, black_claw]
        
        # Enemy has NO Black Claw debuff
        action = self.agent.decide(self.state)
        self.assertEqual(action.action_type, 'ability')
        self.assertEqual(action.ability.name, "Black Claw")
        
        # Enemy HAS Black Claw debuff
        debuff = Buff(type=BuffType.STAT_MOD, name="Black Claw", duration=3, magnitude=0, source_ability="Black Claw", stat_affected="damage_taken")
        self.enemy1.active_buffs.append(debuff)
        
        action = self.agent.decide(self.state)
        self.assertEqual(action.action_type, 'ability')
        self.assertEqual(action.ability.name, "Scratch") # Should not re-apply
        
    def test_level_3_damage(self):
        """Test damage priority"""
        # Strong vs Critter (Beast)
        strong = Ability(1, "Strong", 20, 100, 0, 0, PetFamily.BEAST)
        # Weak vs Critter (Elemental)
        weak = Ability(2, "Weak", 20, 100, 0, 0, PetFamily.ELEMENTAL)
        
        self.pet1.abilities = [weak, strong]
        
        action = self.agent.decide(self.state)
        self.assertEqual(action.action_type, 'ability')
        self.assertEqual(action.ability.name, "Strong")

if __name__ == '__main__':
    unittest.main()
