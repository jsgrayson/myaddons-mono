"""
AI Agents for Pet Battle Simulation

This module contains strategic AI agents used in battle simulations,
particularly for the genetic algorithm fitness evaluation.
"""

from typing import Optional
from simulator import BattleState, TurnAction, Pet, Ability
from simulator.smart_agent import SmartAgent as NewSmartAgent


class SmartEnemyAgent:
    """
    Wrapper for the new SmartAgent (Module 5) to maintain backward compatibility.
    """
    
    def __init__(self, difficulty: float = 1.0, ability_priorities: dict = None):
        """
        Initialize the smart enemy agent.
        
        Args:
            difficulty: Multiplier for strategic behavior (0.0-1.0)
            ability_priorities: Legacy argument, ignored by new SmartAgent.
        """
        self.agent = NewSmartAgent(difficulty=difficulty)
        # ability_priorities is ignored as SmartAgent uses advanced logic
    
    def decide(self, state: BattleState) -> TurnAction:
        """Make a strategic decision."""
        return self.agent.decide(state)


# Convenience function for backward compatibility
def create_smart_enemy_agent(difficulty: float = 1.0, ability_priorities: dict = None):
    """Create a smart enemy agent callable."""
    agent = SmartEnemyAgent(difficulty=difficulty, ability_priorities=ability_priorities)
    return lambda state: agent.decide(state)
