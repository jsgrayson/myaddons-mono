
import unittest
from simulator.battle_state import Pet, PetStats, Ability, PetFamily, PetQuality, Buff, BuffType, BattleState, Team, TurnAction
from simulator.simulator import BattleSimulator

class TestHighRisk(unittest.TestCase):
    def setUp(self):
        self.sim = BattleSimulator()
        
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
        
        self.state = BattleState(Team([self.attacker]), Team([self.defender]))

    def test_explode_dies_on_miss(self):
        """Test that Explode kills the user even if it misses"""
        # Explode Ability
        explode = Ability(
            id=1, name="Explode", power=40, accuracy=100, speed=0, 
            family=PetFamily.MECHANICAL, cooldown=0, effect_type='explode'
        )
        self.attacker.abilities = [explode]
        
        # Force Miss (Defender uses Dodge)
        dodge_buff = Buff(type=BuffType.INVULNERABILITY, duration=2, magnitude=0, name="Dodge", stat_affected='none')
        self.defender.active_buffs.append(dodge_buff)
        
        action_p = TurnAction('player', 'ability', ability=explode)
        action_e = TurnAction('enemy', 'pass')
        
        # Execute
        new_state = self.sim.execute_turn(self.state, action_p, action_e, turn_number=1)
        
        # Attacker should be dead
        attacker_after = new_state.player_team.pets[0]
        self.assertEqual(attacker_after.stats.current_hp, 0, "Exploder should die even on miss")
        
        # Log should show death
        events = [e['type'] for e in self.sim.log.events]
        self.assertIn('death', events)

    def test_haunt_dies_on_miss(self):
        """Test that Haunt kills the user even if it misses"""
        # Haunt Ability
        haunt = Ability(
            id=2, name="Haunt", power=20, accuracy=100, speed=0, 
            family=PetFamily.UNDEAD, cooldown=0, effect_type='haunt'
        )
        self.attacker.abilities = [haunt]
        
        # Force Miss (Defender uses Dodge)
        dodge_buff = Buff(type=BuffType.INVULNERABILITY, duration=2, magnitude=0, name="Dodge", stat_affected='none')
        self.defender.active_buffs.append(dodge_buff)
        
        action_p = TurnAction('player', 'ability', ability=haunt)
        action_e = TurnAction('enemy', 'pass')
        
        # Execute
        new_state = self.sim.execute_turn(self.state, action_p, action_e, turn_number=1)
        
        # Attacker should be DEAD
        attacker_after = new_state.player_team.pets[0]
        self.assertEqual(attacker_after.stats.current_hp, 0, "Haunter should die on miss")
        
        # Log should show death
        events = [e['type'] for e in self.sim.log.events]
        self.assertIn('death', events)

    def test_burrow_speed_zero(self):
        """Test that Burrow reduces speed to 0 while underground"""
        # Attacker uses Burrow
        burrow = Ability(
            id=3, name="Burrow", power=20, accuracy=100, speed=0, 
            family=PetFamily.BEAST, cooldown=0, effect_type='burrow'
        )
        self.attacker.abilities = [burrow]
        
        # Execute turn to apply Burrow buff
        action_p = TurnAction('player', 'ability', ability=burrow)
        action_e = TurnAction('enemy', 'pass')
        
        self.sim.execute_turn(self.state, action_p, action_e, turn_number=1)
        
        # Verify Underground buff exists
        underground = next((b for b in self.attacker.active_buffs if b.name == "Underground"), None)
        self.assertIsNotNone(underground)
        
        # Verify speed is 0
        self.assertEqual(self.attacker.get_effective_speed(), 0, "Speed should be 0 while underground")

    def test_lift_off_speed_zero(self):
        """Test that Lift-Off reduces speed to 0 while flying"""
        # Attacker uses Lift-Off
        lift_off = Ability(
            id=170, name="Lift-Off", power=30, accuracy=100, speed=0, 
            family=PetFamily.FLYING, cooldown=0, effect_type='lift_off'
        )
        self.attacker.abilities = [lift_off]
        
        # Execute turn to apply Flying buff
        action_p = TurnAction('player', 'ability', ability=lift_off)
        action_e = TurnAction('enemy', 'pass')
        
        self.sim.execute_turn(self.state, action_p, action_e, turn_number=1)
        
        # Verify Flying buff exists
        flying = next((b for b in self.attacker.active_buffs if b.name == "Flying"), None)
        self.assertIsNotNone(flying)
        
        # Verify speed is 0
        self.assertEqual(self.attacker.get_effective_speed(), 0, "Speed should be 0 while flying")

    def test_haunt_resurrection(self):
        """Test that Haunt revives the user after buff expires"""
        # Haunt Ability
        haunt = Ability(
            id=2, name="Haunt", power=20, accuracy=100, speed=0, 
            family=PetFamily.UNDEAD, cooldown=0, effect_type='haunt'
        )
        self.attacker.abilities = [haunt]
        
        # Execute Haunt
        action_p = TurnAction('player', 'ability', ability=haunt)
        action_e = TurnAction('enemy', 'pass')
        
        self.sim.execute_turn(self.state, action_p, action_e, turn_number=1)
        
        # Attacker should be DEAD
        self.assertEqual(self.attacker.stats.current_hp, 0, "Haunter should die initially")
        
        # Defender should have Haunt buff
        haunt_buff = next((b for b in self.defender.active_buffs if b.name == "Haunt"), None)
        self.assertIsNotNone(haunt_buff, "Defender should have Haunt buff")
        
        # Simulate turns to expire buff (Duration 5)
        # We need to run execute_turn 5 times?
        # Or just manually decrement?
        # Better to run turns to test integration.
        # But attacker is dead, so we need to swap or pass?
        # If attacker is dead, game might end if only 1 pet?
        # Setup: Give player a second pet so game continues.
        
        pet2 = Pet(
            species_id=3, name="Backup", 
            stats=PetStats(100, 100, 10, 10),
            family=PetFamily.CRITTER, quality=PetQuality.RARE, abilities=[]
        )
        self.state.player_team.pets.append(pet2)
        self.state.player_team.active_pet_index = 1 # Swap to backup automatically? 
        # Sim usually handles swap on death? 
        # For this test, let's just manually set active pet to 1
        
        # Run 5 turns
        for i in range(5):
            # Pass turns
            action_p = TurnAction('player', 'pass')
            action_e = TurnAction('enemy', 'pass')
            self.sim.execute_turn(self.state, action_p, action_e, turn_number=2+i)
            
        # Buff should be gone
        haunt_buff = next((b for b in self.defender.active_buffs if b.name == "Haunt"), None)
        self.assertIsNone(haunt_buff, "Haunt buff should expire")
        
        # Attacker should be ALIVE
        self.assertGreater(self.attacker.stats.current_hp, 0, "Haunter should resurrect")
        self.assertEqual(self.attacker.stats.current_hp, 100, "Haunter should have full HP (snapshot)")

if __name__ == '__main__':
    unittest.main()
