
import unittest
from simulator.battle_state import Pet, PetStats, Ability, PetFamily, PetQuality, BattleState, Team, TurnAction
from simulator.simulator import BattleSimulator

class TestSpeedRNG(unittest.TestCase):
    def test_speed_tie_distribution(self):
        """Test that speed ties result in roughly 50/50 distribution"""
        
        # Setup pets with identical speed
        # Ability: One-shot kill to make winner obvious
        nuke = Ability(id=1, name="Nuke", power=1000, accuracy=100, speed=0, family=PetFamily.HUMANOID, cooldown=0)
        
        player_wins = 0
        iterations = 100
        
        for _ in range(iterations):
            # Re-initialize sim to ensure fresh state (though rng is persistent if same sim)
            # We want to test the RNG of the sim.
            # If we use the SAME sim, rng state advances.
            # If we use NEW sim with seed=None, it reseeds from time.
            sim = BattleSimulator(rng_seed=None)
            
            p1 = Pet(species_id=1, name="P1", stats=PetStats(100, 100, 10, 10), family=PetFamily.HUMANOID, quality=PetQuality.RARE, abilities=[nuke])
            p2 = Pet(species_id=2, name="P2", stats=PetStats(100, 100, 10, 10), family=PetFamily.HUMANOID, quality=PetQuality.RARE, abilities=[nuke])
            
            state = BattleState(Team([p1]), Team([p2]))
            
            # Both use Nuke
            action_p = TurnAction('player', 'ability', ability=nuke)
            action_e = TurnAction('enemy', 'ability', ability=nuke)
            
            # Execute ONE turn
            # Whoever goes first kills the other.
            new_state = sim.execute_turn(state, action_p, action_e, turn_number=1)
            
            # Check who is alive
            p1_alive = new_state.player_team.pets[0].stats.is_alive()
            p2_alive = new_state.enemy_team.pets[0].stats.is_alive()
            
            if p1_alive and not p2_alive:
                player_wins += 1
            elif not p1_alive and p2_alive:
                pass # Enemy win
            else:
                # Both died? (Shouldn't happen if one kills first, unless simultaneous?)
                # In my sim, if first kills second, second doesn't act.
                # So only one should die.
                pass
                
        print(f"Player Wins in Speed Ties: {player_wins}/{iterations}")
        
        # Assert roughly 50% (allow variance)
        # 30 to 70 is a safe range for 100 iterations (3 sigma is roughly +/- 15, so 35-65)
        self.assertTrue(30 <= player_wins <= 70, f"Speed tie distribution biased: {player_wins}/{iterations}")

if __name__ == '__main__':
    unittest.main()
