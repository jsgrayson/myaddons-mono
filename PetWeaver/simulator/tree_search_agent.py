
from typing import List, Optional, Tuple
from .battle_state import BattleState, TurnAction, Pet, Ability
from .simulator import BattleSimulator

class TreeSearchAgent:
    """
    AI Agent using Minimax Lookahead to choose optimal moves.
    """
    
    def __init__(self, depth: int = 2, player_idx: str = 'player'):
        self.depth = depth
        self.player_idx = player_idx # 'player' or 'enemy'
        self.simulator = BattleSimulator() # Use default seed for deterministic lookahead? Or random?
        # Ideally, we want deterministic lookahead for Minimax, but the game has RNG.
        # Expectimax is better but expensive.
        # We'll use a fixed seed for the simulator to ensure consistency during search?
        # No, we want to simulate "average" outcomes.
        # For now, we'll just let RNG happen and maybe run multiple simulations per node if needed.
        # But for MVP, single simulation per node (Standard Minimax with "sample" outcome).
        
    def decide(self, state: BattleState) -> TurnAction:
        """
        Decide the best action for the current state.
        """
        best_value = -float('inf')
        best_action = None
        
        # Get legal actions
        actions = self._get_legal_actions(state, self.player_idx)
        
        if not actions:
            return TurnAction(self.player_idx, 'pass')
            
        for action in actions:
            # Simulate this action against opponent's best response (Minimax)
            # Or just simulate against a random/heuristic opponent (simplifies to 1-ply lookahead with heuristic eval)
            # Let's do full Minimax: Minimize opponent's gain.
            
            value = self._min_value(state, action, self.depth - 1)
            
            print(f"DEBUG: Root Action {action.ability.name if action.ability else action.action_type} Value: {value}")
            
            # Prefer higher value, and break ties by preferring healing abilities
            if (value > best_value) or (
                value == best_value and action.ability and action.ability.is_heal
            ):
                best_value = value
                best_action = action
                
        return best_action if best_action else TurnAction(self.player_idx, 'pass')

    def _max_value(self, state: BattleState, depth: int) -> float:
        if depth == 0 or state.is_battle_over():
            return self.evaluate_state(state)
            
        value = -float('inf')
        actions = self._get_legal_actions(state, self.player_idx)
        
        if not actions:
             # Force pass
             return self._min_value(state, TurnAction(self.player_idx, 'pass'), depth)

        for action in actions:
            # We need to pair this with an enemy action to advance state.
            # This structure is slightly wrong for simultaneous turns.
            # In simultaneous turns, we pick Action A, Enemy picks Action B -> Result.
            # We want Max_A ( Min_B ( Result(A, B) ) )
            
            # So _max_value should iterate A, and call _min_value(state, A, depth)
            # But _min_value needs to iterate B, and call _max_value(Result(A,B), depth-1)
            
            val = self._min_value(state, action, depth)
            value = max(value, val)
            
        return value
        
    def _min_value(self, state: BattleState, my_action: TurnAction, depth: int) -> float:
        # Opponent (Minimizer) chooses their action
        opponent_idx = 'enemy' if self.player_idx == 'player' else 'player'
        
        value = float('inf')
        actions = self._get_legal_actions(state, opponent_idx)
        
        if not actions:
            actions = [TurnAction(opponent_idx, 'pass')]
            
        for opp_action in actions:
            # Execute turn
            # Note: execute_turn expects player_action first arg, enemy_action second arg
            if self.player_idx == 'player':
                new_state = self.simulator.execute_turn(state, my_action, opp_action, state.turn_number)
            else:
                new_state = self.simulator.execute_turn(state, opp_action, my_action, state.turn_number)
                
            val = self._max_value(new_state, depth - 1) # Decrement depth here
            
            value = min(value, val)
            
        return value



    def evaluate_state(self, state: BattleState) -> float:
        """
        Evaluate state favorability for self.player_idx.
        Higher is better.
        """
        if self.player_idx == 'player':
            my_team = state.player_team
            opp_team = state.enemy_team
        else:
            my_team = state.enemy_team
            opp_team = state.player_team
            
        # 1. HP Percentage Difference
        my_hp_pct = sum(p.stats.current_hp for p in my_team.pets) / sum(p.stats.max_hp for p in my_team.pets)
        opp_hp_pct = sum(p.stats.current_hp for p in opp_team.pets) / sum(p.stats.max_hp for p in opp_team.pets)
        
        score = (my_hp_pct - opp_hp_pct) * 100
        
        # 2. Alive Pets Difference
        my_alive = sum(1 for p in my_team.pets if p.stats.is_alive())
        opp_alive = sum(1 for p in opp_team.pets if p.stats.is_alive())
        
        score += (my_alive - opp_alive) * 50
        
        # 3. Survival penalty: heavily penalize if active pet is low on HP
        active_my = my_team.get_active_pet()
        if active_my:
            hp_ratio = active_my.stats.current_hp / active_my.stats.max_hp
            if hp_ratio < 0.2:
                score -= 200  # large penalty for being near death
        
        # 4. Secure kill bonus: reward if we can kill the opponent's active pet this turn
        active_opp = opp_team.get_active_pet()
        if active_my and active_opp:
            # Estimate max damage we could deal this turn (simple heuristic)
            max_damage = 0
            for ab in active_my.abilities:
                if not getattr(ab, 'is_heal', False):
                    # Approximate damage using ability power and attacker power
                    dmg = ab.power * (active_my.stats.power / 20)
                    if dmg > max_damage:
                        max_damage = dmg
            if max_damage >= active_opp.stats.current_hp:
                score += 100  # bonus for a guaranteed kill
        
        # 5. Healing incentive: if we have a heal ability and are low on HP, add modest bonus
        if active_my:
            has_heal = any(ab.is_heal for ab in active_my.abilities)
            if has_heal and hp_ratio < 0.5:
                score += 50
        
        return score

    def _get_legal_actions(self, state: BattleState, actor: str) -> List[TurnAction]:
        team = state.player_team if actor == 'player' else state.enemy_team
        active_pet = team.get_active_pet()
        
        actions = []
        
        # If pet is dead, MUST swap
        if not active_pet or not active_pet.stats.is_alive():
            for i, p in enumerate(team.pets):
                if p.stats.is_alive():
                    actions.append(TurnAction(actor, 'swap', target_pet_index=i))
            return actions
            
        # Abilities
        # Check CC
        can_act = True
        for buff in active_pet.active_buffs:
            if buff.type.value in ['stun', 'frozen', 'sleep']:
                can_act = False
                break
        
        if can_act:
            for ab in active_pet.abilities:
                if active_pet.can_use_ability(ab):
                    actions.append(TurnAction(actor, 'ability', ability=ab))
        
        # Swaps (Strategic) - Limit to avoid branching factor explosion?
        # For now, maybe skip strategic swaps in lookahead unless necessary
        # Or only swap if active pet is low HP?
        
        if not actions:
            actions.append(TurnAction(actor, 'pass'))
            
        return actions
