
import unittest
from simulator.battle_state import Pet, PetStats, Ability, PetFamily, PetQuality, Buff, BuffType, BattleState, Team, TurnAction
from simulator.simulator import BattleSimulator

class TestAccuracyBuffs(unittest.TestCase):
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

    def test_accuracy_buff_counters_dodge(self):
        """Test that an accuracy buff helps counter a dodge penalty"""
        # Ability with 50% accuracy (should miss often)
        low_acc_ability = Ability(
            id=1, name="Low Acc", power=10, accuracy=50, speed=0, 
            family=PetFamily.HUMANOID, cooldown=0
        )
        self.attacker.abilities = [low_acc_ability]
        
        # Add Accuracy Buff (+50%)
        acc_buff = Buff(
            type=BuffType.STAT_MOD,
            name="Accuracy Boost",
            duration=5,
            magnitude=0.5, # +50%
            source_ability="Test",
            stat_affected='accuracy'
        )
        self.attacker.active_buffs.append(acc_buff)
        
        # With +50%, total accuracy should be 100%.
        # Run 100 times, expect ~100 hits.
        
        hits = 0
        iterations = 100
        
        for _ in range(iterations):
            # We need to manually call check_hit because execute_turn involves RNG and full flow
            # But check_hit uses self.sim.damage_calc.rng
            # We can just call check_hit directly.
            
            hit = self.sim.damage_calc.check_hit(low_acc_ability, self.attacker, self.defender, weather=None)
            if hit:
                hits += 1
                
        # If accuracy buff is IGNORED, hit rate is 50%.
        # If accuracy buff is APPLIED, hit rate is 100%.
        
        print(f"Hits with Accuracy Buff: {hits}/{iterations}")
        self.assertGreater(hits, 90, "Accuracy buff should ensure near 100% hit rate")

if __name__ == '__main__':
    unittest.main()
