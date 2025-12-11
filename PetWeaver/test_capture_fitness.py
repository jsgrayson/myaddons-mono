#!/usr/bin/env python3
"""
Test script for Capture Strategy fitness evaluation.

Goal: Find a team that can:
1. Reduce target pet to < 35% HP (capture threshold)
2. Kill all other enemy pets
3. Not kill the target pet
"""

import json
from simulator import Team, Pet, PetStats, PetFamily, PetQuality, Ability, BattleSimulator
from genetic.genome import TeamGenome

def calculate_capture_fitness(state, target_slot=0):
    """
    Calculate fitness for a capture strategy.
    
    Args:
        state: Final battle state
        target_slot: Which enemy slot is the capture target (0, 1, or 2)
    
    Returns:
        fitness score (higher is better)
    """
    score = 0
    
    # Check if we won
    player_alive = sum(1 for p in state.player_team.pets if p.stats.is_alive())
    enemy_alive = sum(1 for p in state.enemy_team.pets if p.stats.is_alive())
    
    if player_alive == 0:
        # We lost - very bad
        return 0
    
    # Check target pet status
    target_pet = state.enemy_team.pets[target_slot]
    target_hp_pct = target_pet.stats.current_hp / target_pet.stats.max_hp
    
    # Check if target is alive
    if not target_pet.stats.is_alive():
        # We killed the target - bad, but not as bad as losing
        score += 1000
    elif target_hp_pct < 0.35:
        # Target is in capture range and alive - PERFECT!
        score += 100000
        # Bonus for being closer to 35% (not too low)
        closeness_to_35 = 1.0 - abs(target_hp_pct - 0.35)
        score += closeness_to_35 * 10000
    else:
        # Target is alive but not in capture range
        # Reward getting it lower
        score += (1.0 - target_hp_pct) * 50000
    
    # Check non-target pets are dead
    for i, pet in enumerate(state.enemy_team.pets):
        if i == target_slot:
            continue
        if not pet.stats.is_alive():
            score += 20000  # Killed a non-target pet
        else:
            # Penalize leaving non-target pets alive
            hp_pct = pet.stats.current_hp / pet.stats.max_hp
            score -= hp_pct * 10000
    
    # Reward our pet survival
    for pet in state.player_team.pets:
        if pet.stats.is_alive():
            hp_pct = pet.stats.current_hp / pet.stats.max_hp
            score += hp_pct * 5000
    
    return score

if __name__ == "__main__":
    print("Capture Strategy Fitness Test")
    print("=" * 60)
    
    # TODO: Create a test battle with a target pet
    # TODO: Test the fitness function with different outcomes
    
    print("\nFitness function created successfully!")
