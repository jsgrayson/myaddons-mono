
import unittest
from simulator.battle_state import Pet, PetStats, Buff, BuffType, BattleState, Team, PetFamily
from simulator.simulator import BattleSimulator

class TestTurnOrder(unittest.TestCase):
    def setUp(self):
        self.sim = BattleSimulator()
        
        # Create dummy pets
        self.p1 = Pet(
            species_id=1, 
            name="P1", 
            stats=PetStats(100, 100, 10, 10),
            family=PetFamily.HUMANOID,
            quality=3,
            abilities=[1, 2, 3]
        )
        self.p2 = Pet(
            species_id=2, 
            name="P2", 
            stats=PetStats(100, 100, 10, 10),
            family=PetFamily.BEAST,
            quality=3,
            abilities=[1, 2, 3]
        )
        
        self.team1 = Team([self.p1])
        self.team2 = Team([self.p2])
        self.state = BattleState(self.team1, self.team2)

    def test_dot_kills_before_hot(self):
        """Test that DoT damage kills a low HP pet before HoT can heal it"""
        # Set HP to 10
        self.p1.stats.current_hp = 10
        
        # Add DoT (20 damage)
        dot = Buff(
            type=BuffType.DOT,
            duration=3,
            magnitude=20,
            source_ability="Test DoT"
        )
        self.sim.buff_tracker.add_buff(self.p1, dot)
        
        # Add HoT (50 heal)
        hot = Buff(
            type=BuffType.HOT,
            duration=3,
            magnitude=50,
            source_ability="Test HoT"
        )
        self.sim.buff_tracker.add_buff(self.p1, hot)
        
        # Execute end of turn
        self.sim.process_end_of_turn(self.state, self.p1, self.p2)
        
        # Assertions
        self.assertFalse(self.p1.stats.is_alive(), "Pet should be dead from DoT")
        self.assertEqual(self.p1.stats.current_hp, 0, "HP should be 0")
        
        # Check log to verify order
        events = [e['type'] for e in self.sim.log.events]
        self.assertIn('dot_damage', events)
        # HoT might not even fire if pet is dead, or it might fire but have no effect?
        # In my implementation: "if not pet.stats.is_alive(): continue" for HoTs.
        # So 'hot_heal' should NOT be in events.
        self.assertNotIn('hot_heal', events, "HoT should not trigger on dead pet")

    def test_weather_kills_before_hot(self):
        """Test that Weather damage kills before HoT"""
        # Set HP to 10
        self.p1.stats.current_hp = 10
        # Set family to Dragonkin (takes damage from Scorched Earth)
        self.p1.family = PetFamily.DRAGONKIN
        
        # Set Weather: Scorched Earth (35 damage to Dragonkin)
        weather = Buff(
            type=BuffType.WEATHER,
            duration=5,
            magnitude=0,
            source_ability=0,
            stat_affected="scorched_earth"
        )
        self.state.weather = weather
        
        # Add HoT (50 heal)
        hot = Buff(
            type=BuffType.HOT,
            duration=3,
            magnitude=50,
            source_ability="Test HoT"
        )
        self.sim.buff_tracker.add_buff(self.p1, hot)
        
        # Execute end of turn
        self.sim.process_end_of_turn(self.state, self.p1, self.p2)
        
        # Assertions
        self.assertFalse(self.p1.stats.is_alive(), "Pet should be dead from Weather")
        self.assertEqual(self.p1.stats.current_hp, 0)
        
        events = [e['type'] for e in self.sim.log.events]
        self.assertIn('weather_dot', events)
        self.assertNotIn('hot_heal', events)

    def test_hot_saves_if_dot_doesnt_kill(self):
        """Control test: HoT should work if DoT doesn't kill"""
        self.p1.stats.current_hp = 30
        
        # DoT: 20 dmg (HP -> 10)
        dot = Buff(type=BuffType.DOT, duration=3, magnitude=20, source_ability="Test DoT")
        self.sim.buff_tracker.add_buff(self.p1, dot)
        
        # HoT: 50 heal (HP -> 60)
        hot = Buff(type=BuffType.HOT, duration=3, magnitude=50, source_ability="Test HoT")
        self.sim.buff_tracker.add_buff(self.p1, hot)
        
        self.sim.process_end_of_turn(self.state, self.p1, self.p2)
        
        self.assertTrue(self.p1.stats.is_alive())
        self.assertEqual(self.p1.stats.current_hp, 60)
        
        events = [e['type'] for e in self.sim.log.events]
        self.assertIn('dot_damage', events)
        self.assertIn('hot_heal', events)

if __name__ == '__main__':
    unittest.main()
