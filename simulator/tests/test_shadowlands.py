import unittest
from simulator.battle_state import Pet, Team, PetStats, Ability, PetFamily, Buff, BuffType, TurnAction
from simulator.simulator import BattleSimulator
from simulator.special_encounters import SpecialEncounterHandler

class TestShadowlandsMechanics(unittest.TestCase):
    def setUp(self):
        self.simulator = BattleSimulator(rng_seed=42)
        
        # Create dummy pets
        self.p1 = Pet(name="Attacker", species_id=1, stats=PetStats(max_hp=1000, current_hp=1000, power=300, speed=300), 
                     abilities=[Ability(id=1, name="Strike", power=20, accuracy=100, speed=0, family=PetFamily.HUMANOID, cooldown=0)],
                     family=PetFamily.HUMANOID, quality=3)
        self.p2 = Pet(name="Defender", species_id=2, stats=PetStats(max_hp=1000, current_hp=1000, power=250, speed=250), 
                     abilities=[Ability(id=1, name="Strike", power=20, accuracy=100, speed=0, family=PetFamily.HUMANOID, cooldown=0)],
                     family=PetFamily.HUMANOID, quality=3)
        
        self.team1 = Team(pets=[self.p1])
        self.team2 = Team(pets=[self.p2])

    def test_mind_games(self):
        """Test Mind Games deals 25% Max HP to entire enemy team"""
        # Add a backline pet to team 2
        p3 = Pet(name="Backline", species_id=3, stats=PetStats(max_hp=800, current_hp=800, power=200, speed=200), abilities=[], family=PetFamily.CRITTER, quality=3)
        self.team2.pets.append(p3)
        
        mind_games = Ability(id=2388, name="Mind Games", power=0, accuracy=100, speed=0, family=PetFamily.MAGIC, cooldown=0)
        
        # Apply Mind Games manually to verify handler logic first
        SpecialEncounterHandler.apply_mind_games(self.team2, self.p1)
        
        # P2 (Active): 1000 Max HP -> 250 damage -> 750 Current HP
        self.assertEqual(self.p2.stats.current_hp, 750)
        # P3 (Backline): 800 Max HP -> 200 damage -> 600 Current HP
        self.assertEqual(p3.stats.current_hp, 600)

    def test_bone_prison(self):
        """Test Bone Prison applies stun"""
        bone_prison = Ability(id=650, name="Bone Prison", power=0, accuracy=100, speed=0, family=PetFamily.UNDEAD, cooldown=0)
        
        SpecialEncounterHandler.apply_bone_prison(self.p2)
        
        self.assertTrue(any(b.type == BuffType.STUN for b in self.p2.active_buffs))
        stun_buff = next(b for b in self.p2.active_buffs if b.type == BuffType.STUN)
        self.assertEqual(stun_buff.duration, 2)

    def test_toxic_skin_reflection(self):
        """Test Toxic Skin reflects 25% damage"""
        damage_dealt = 400
        
        # Apply Toxic Skin manually
        reflected = SpecialEncounterHandler.apply_toxic_skin(self.p1, damage_dealt)
        
        # 25% of 400 is 100
        self.assertEqual(reflected, 100)
        self.assertEqual(self.p1.stats.current_hp, 900) # 1000 - 100

    def test_undead_racial(self):
        """Test Undead racial resurrection via Simulator"""
        # Create an Undead pet with low HP
        undead = Pet(name="UndeadPet", species_id=4, stats=PetStats(max_hp=100, current_hp=10, power=100, speed=100), 
                    abilities=[Ability(id=1, name="Strike", power=20, accuracy=100, speed=0, family=PetFamily.UNDEAD, cooldown=0)], 
                    family=PetFamily.UNDEAD, quality=3)
        
        # Create a killer pet
        killer = Pet(name="Killer", species_id=5, stats=PetStats(max_hp=1000, current_hp=1000, power=1000, speed=1000),
                    abilities=[Ability(id=2, name="Kill", power=100, accuracy=100, speed=0, family=PetFamily.HUMANOID, cooldown=0)],
                    family=PetFamily.HUMANOID, quality=3)
        
        team_undead = Team(pets=[undead])
        team_killer = Team(pets=[killer])
        
        from simulator.battle_state import BattleState
        state = BattleState(team_undead, team_killer, 1)
        
        # Killer attacks Undead
        # We need to construct a turn where Killer uses ability and Undead passes (or uses ability)
        # Since Killer is faster (speed 1000 vs 100), Killer goes first.
        
        # Define scripts
        def killer_script(s): return TurnAction('enemy', 'ability', ability=killer.abilities[0])
        def undead_script(s): return TurnAction('player', 'pass')
        
        # Run one turn
        result = self.simulator.simulate_battle(state, undead_script, killer_script, max_turns=1, enable_logging=True)
        final_state = result['final_state']
        final_undead = final_state.player_team.pets[0]
        
        # Undead should have taken fatal damage but revived
        # Check logs for "racial" event
        events = result['events']
        racial_triggered = any(e.get('type') == 'racial' and e.get('racial') == 'Undead' for e in events)
        
        self.assertTrue(racial_triggered, "Undead racial should trigger in logs")
        self.assertTrue(final_undead.stats.is_alive(), "Undead pet should be alive after fatal damage")
        self.assertEqual(final_undead.stats.current_hp, 1, "Undead pet should have 1 HP")
        self.assertTrue(final_undead.has_undead_revive, "Undead pet should have revive flag set")

if __name__ == '__main__':
    unittest.main()
