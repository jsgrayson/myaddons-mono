
import unittest
from simulator.battle_state import BattleState, Team, Pet, Ability, PetFamily, PetStats, TurnAction, Buff, BuffType
from simulator.simulator import BattleSimulator
from simulator.special_encounters import SpecialEncounterHandler

class TestSpecialMechanics(unittest.TestCase):
    def setUp(self):
        self.sim = BattleSimulator()
        
    def test_rocko_immunity(self):
        # Create Rocko (ID 1811)
        rocko = Pet(species_id=1811, name="Rocko", family=PetFamily.ELEMENTAL, 
                   stats=PetStats(max_hp=1000, current_hp=1000, power=300, speed=250),
                   abilities=[], quality=4)
        rocko.stats.current_hp = 1000
        
        # Create dummy opponent
        enemy = Pet(species_id=1, name="Enemy", family=PetFamily.CRITTER,
                   stats=PetStats(max_hp=1000, current_hp=1000, power=300, speed=250),
                   abilities=[], quality=4)
        enemy.stats.current_hp = 1000
        
        # Setup teams
        player_team = Team([rocko])
        enemy_team = Team([enemy])
        state = BattleState(player_team, enemy_team)
        
        # Test rounds 1-10 (Immune)
        # We need to simulate a turn where Rocko takes damage.
        # But wait, Rocko is the *enemy* usually.
        # SpecialEncounterHandler checks if *any* pet has the ID.
        
        # Let's simulate a turn where enemy attacks Rocko.
        # We need to manually trigger the immunity check or run a full turn.
        # The simulator calls apply_rocko_immunity inside execute_turn.
        
        # We need to pass 'rocko_immunity' as special_encounter_id to simulate_battle
        # OR the simulator should detect it?
        # Simulator.simulate_battle takes special_encounter_id as arg.
        # But does it auto-detect?
        # Let's check simulator.py.
        # It takes `special_encounter_id` as an argument.
        # It does NOT auto-detect from species ID at the start.
        # Wait, lines 150-153 in simulator.py:
        # if special_encounter_id == 'rocko_immunity': ...
        # So we MUST pass the ID.
        
        # But wait, how does the main app know to pass it?
        # The main app (app.py) likely needs to look up the encounter ID and pass the special ID.
        # I should check app.py later.
        
        # For now, let's test with the ID passed.
        
        # Create a dummy ability for enemy
        smash = Ability(id=1, name="Smash", power=20, accuracy=100, speed=0, family=PetFamily.HUMANOID, cooldown=0)
        enemy.abilities = [smash]
        
        # Script: Enemy uses Smash
        # ... (rest of rocko test)
        
        # Turn 1
        action_p = TurnAction('player', 'pass')
        action_e = TurnAction('enemy', 'ability', ability=smash)
        
        # Execute turn 1 with special_encounter_id
        new_state = self.sim.execute_turn(state, action_p, action_e, turn_number=1, special_encounter_id='rocko_immunity')
        
        # Rocko should take 0 damage (Immune)
        rocko_after = new_state.player_team.pets[0]
        self.assertEqual(rocko_after.stats.current_hp, 1000)
        
        # Turn 11 (Death)
        # We need to advance turn number.
        new_state = self.sim.execute_turn(state, action_p, action_e, turn_number=11, special_encounter_id='rocko_immunity')
        rocko_after = new_state.player_team.pets[0]
        self.assertEqual(rocko_after.stats.current_hp, 0)

    def test_jawbone_bone_prison(self):
        # Create Jawbone (ID 1400)
        jawbone = Pet(species_id=1400, name="Jawbone", family=PetFamily.UNDEAD,
                     stats=PetStats(max_hp=1000, current_hp=1000, power=300, speed=250),
                     abilities=[], quality=4)
        
        # Create dummy opponent
        opponent = Pet(species_id=1, name="Opponent", family=PetFamily.CRITTER,
                      stats=PetStats(max_hp=1000, current_hp=1000, power=300, speed=250),
                      abilities=[], quality=4)
        
        # Give Jawbone Bone Prison ability (ID 650)
        bone_prison = Ability(id=650, name="Bone Prison", power=20, accuracy=100, speed=0, family=PetFamily.UNDEAD, cooldown=0)
        jawbone.abilities = [bone_prison]
        
        state = BattleState(Team([jawbone]), Team([opponent]))
        
        from simulator.battle_state import TurnAction
        action_p = TurnAction('player', 'ability', ability=bone_prison)
        action_e = TurnAction('enemy', 'pass')
        
        # Execute turn
        # Note: special_encounter_id='bone_prison' is NOT needed for the ABILITY to work if it's implemented in execute_action.
        # But wait, execute_action checks special_encounter_id for "Bone Prison" ability name!
        # Line 270 in simulator.py: if ability.name == "Bone Prison": ...
        # AND it checks if special_encounter_id is set.
        # So we MUST pass special_encounter_id='bone_prison' (or whatever ID enables it).
        # Actually, the ID passed to simulate_battle is the Encounter ID (e.g. 'rocko_immunity').
        # But for Bone Prison, is there a special encounter ID?
        # In special_encounters.py registry: 1400: 'bone_prison'.
        # So we should pass 'bone_prison'.
        
        new_state = self.sim.execute_turn(state, action_p, action_e, turn_number=1, special_encounter_id='bone_prison')
        
        # Opponent should be stunned
        opponent_after = new_state.enemy_team.pets[0]
        stun_buff = next((b for b in opponent_after.active_buffs if b.type.name == 'STUN'), None)
        self.assertIsNotNone(stun_buff)
        self.assertEqual(stun_buff.source_ability, 77777) # Special ID from handler
        
    def test_gorespine_gore(self):
        # Create Gorespine (ID 1187)
        gorespine = Pet(species_id=1187, name="Gorespine", family=PetFamily.BEAST,
                       stats=PetStats(max_hp=1000, current_hp=1000, power=300, speed=250),
                       abilities=[], quality=4)
        gorespine.stats.current_hp = 1000
        
        opponent = Pet(species_id=1, name="Opponent", family=PetFamily.CRITTER,
                      stats=PetStats(max_hp=1000, current_hp=1000, power=300, speed=250),
                      abilities=[], quality=4)
        
        state = BattleState(Team([gorespine]), Team([opponent]))
        
        from simulator.battle_state import TurnAction
        action = TurnAction('player', 'pass')
        
        # Turn 1: Should apply Gore stack
        new_state = self.sim.execute_turn(state, action, action, turn_number=1, special_encounter_id='gore_stacks')
        
        gorespine_after = new_state.player_team.pets[0]
        # Check buffs
        gore_buff = next((b for b in gorespine_after.active_buffs if b.source_ability == 99999), None)
        self.assertIsNotNone(gore_buff)
        self.assertEqual(gore_buff.stacks, 1)
        
        # Turn 2: Should increase stack
        new_state = self.sim.execute_turn(new_state, action, action, turn_number=2, special_encounter_id='gore_stacks')
        gorespine_after = new_state.player_team.pets[0]
        gore_buff = next((b for b in gorespine_after.active_buffs if b.source_ability == 99999), None)
        self.assertEqual(gore_buff.stacks, 2)

    def test_life_exchange(self):
        """Test Life Exchange health swap mechanics"""
        # Attacker: 100/1000 HP (10%)
        attacker = Pet(species_id=1, name="Attacker", family=PetFamily.HUMANOID,
                      stats=PetStats(max_hp=1000, current_hp=100, power=300, speed=300),
                      abilities=[], quality=4)
        
        # Defender: 1000/1000 HP (100%)
        defender = Pet(species_id=2, name="Defender", family=PetFamily.BEAST,
                      stats=PetStats(max_hp=1000, current_hp=1000, power=300, speed=250),
                      abilities=[], quality=4)
        
        # Add Shield to Defender (should be ignored)
        shield = Buff(type=BuffType.SHIELD, duration=3, magnitude=1000, stat_affected='damage_taken')
        defender.active_buffs.append(shield)
        
        # Ability: Life Exchange
        life_exchange = Ability(id=1300, name="Life Exchange", power=0, accuracy=100, speed=0, family=PetFamily.MAGIC, cooldown=0)
        attacker.abilities = [life_exchange]
        
        state = BattleState(Team([attacker]), Team([defender]))
        
        action_p = TurnAction('player', 'ability', ability=life_exchange)
        action_e = TurnAction('enemy', 'pass')
        
        # Execute turn
        # Pass special_encounter_id='life_exchange' (though logic is triggered by ability name)
        new_state = self.sim.execute_turn(state, action_p, action_e, turn_number=1, special_encounter_id='life_exchange')
        
        attacker_after = new_state.player_team.pets[0]
        defender_after = new_state.enemy_team.pets[0]
        
        # Attacker should have 100% HP (1000)
        self.assertEqual(attacker_after.stats.current_hp, 1000, "Attacker should have swapped to 100% HP")
        
        # Defender should have 10% HP (100)
        self.assertEqual(defender_after.stats.current_hp, 100, "Defender should have swapped to 10% HP")
    
    def test_healing_reduction_debuff(self):
        """Test Shadowlands healing reduction debuff (common mechanic)"""
        # Create pet with healing ability
        heal_ability = Ability(id=1, name="Heal", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.BEAST, is_heal=True)
        pet = Pet(species_id=1, name="Healer", family=PetFamily.BEAST,
                 stats=PetStats(max_hp=1000, current_hp=500, power=300, speed=250),
                 abilities=[heal_ability], quality=4)
        
        # Apply 50% healing reduction debuff
        SpecialEncounterHandler.apply_healing_reduction(pet, reduction_pct=0.5, duration=3)
        
        # Verify debuff was applied
        healing_debuff = None
        for buff in pet.active_buffs:
            if buff.stat_affected == 'healing_received':
                healing_debuff = buff
                break
        
        self.assertIsNotNone(healing_debuff, "Healing reduction debuff should be applied")
        self.assertEqual(healing_debuff.magnitude, 0.5, "Debuff should be 50% reduction")
        self.assertEqual(healing_debuff.duration, 3, "Debuff should last 3 rounds")
        
        # Create a simple state to test healing
        enemy = Pet(species_id=2, name="Enemy", family=PetFamily.CRITTER,
                   stats=PetStats(max_hp=1000, current_hp=1000, power=300, speed=250),
                   abilities=[], quality=4)
        
        player_team = Team([pet])
        enemy_team = Team([enemy])
        state = BattleState(player_team, enemy_team)
        
        # Execute heal action
        action = TurnAction('player', 'ability', ability=heal_ability)
        enemy_action = TurnAction('enemy', 'pass')
        
        new_state = self.sim.execute_turn(state, action, enemy_action, turn_number=1)
        
        # Check that healing was reduced
        # Normal heal would be ~300 HP (20 power * 15 from calculation)
        # With 50% reduction, it should be ~150 HP
        # So from 500 HP, should be around 650 HP (not full 800 HP)
        healer_after = new_state.player_team.pets[0]
        self.assertLess(healer_after.stats.current_hp, 700, "Healing should be reduced by debuff")
        self.assertGreater(healer_after.stats.current_hp, 500, "Should still heal some amount")
    
    def test_massive_team_heal(self):
        """Test The Impossible Boss massive team healing mechanic"""
        # Create team with multiple low-HP pets
        pet1 = Pet(species_id=1, name="Pet1", family=PetFamily.BEAST,
                  stats=PetStats(max_hp=1000, current_hp=200, power=300, speed=250),
                  abilities=[], quality=4)
        pet2 = Pet(species_id=2, name="Pet2", family=PetFamily.FLYING,
                  stats=PetStats(max_hp=1000, current_hp=300, power=300, speed=250),
                  abilities=[], quality=4)
        pet3 = Pet(species_id=3, name="Pet3", family=PetFamily.MAGIC,
                  stats=PetStats(max_hp=1000, current_hp=100, power=300, speed=250),
                  abilities=[], quality=4)
        
        team = Team([pet1, pet2, pet3])
        
        # Apply massive heal (500 HP to all pets)
        SpecialEncounterHandler.apply_massive_team_heal(team, heal_amount=500)
        
        # Verify all pets were healed
        self.assertEqual(pet1.stats.current_hp, 700, "Pet1 should heal from 200 to 700")
        self.assertEqual(pet2.stats.current_hp, 800, "Pet2 should heal from 300 to 800")
        self.assertEqual(pet3.stats.current_hp, 600, "Pet3 should heal from 100 to 600")

if __name__ == '__main__':
    unittest.main()
