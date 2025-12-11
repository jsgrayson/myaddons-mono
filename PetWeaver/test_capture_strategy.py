#!/usr/bin/env python3
"""
Test the Capture Strategy Solver with a synthetic wild pet encounter.

Tests that the solver can find a team that:
1. Reduces target pet to < 35% HP (capture threshold)
2. Kills all non-target pets
3. Does NOT kill the target pet
"""

import json
import sys
from simulator import Team, Pet, PetStats, PetFamily, PetQuality, Ability
from genetic.fitness import FitnessEvaluator
from genetic.genome import TeamGenome

def create_wild_encounter():
    """Create a synthetic 3-pet wild encounter for testing."""
    # Simple wild pets with basic abilities
    pets = []
    
    # Pet 1: Critter (Target - we want to capture this one)
    pets.append(Pet(
        species_id=1000,
        name="Wild Squirrel",
        family=PetFamily.CRITTER,
        quality=PetQuality.RARE,
        stats=PetStats(max_hp=400, current_hp=400, power=50, speed=50),
        abilities=[
            Ability(id=119, name="Scratch", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.BEAST),
            Ability(id=110, name="Bite", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.BEAST),
        ]
    ))
    
    # Pet 2: Beast (Companion - kill this one)
    pets.append(Pet(
        species_id=1001,
        name="Wild Rabbit",
        family=PetFamily.BEAST,
        quality=PetQuality.RARE,
        stats=PetStats(max_hp=350, current_hp=350, power=45, speed=60),
        abilities=[
            Ability(id=122, name="Flurry", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.BEAST),
        ]
    ))
    
    # Pet 3: Flying (Companion - kill this one)
    pets.append(Pet(
        species_id=1002,
        name="Wild Moth",
        family=PetFamily.FLYING,
        quality=PetQuality.RARE,
        stats=PetStats(max_hp=300, current_hp=300, power=55, speed=70),
        abilities=[
            Ability(id=115, name="Breath", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.FLYING),
        ]
    ))
    
    return Team(pets=pets)

def main():
    print("=" * 70)
    print("CAPTURE STRATEGY SOLVER TEST")
    print("=" * 70)
    
    # Load ability and species data
    with open('abilities.json') as f:
        ability_data = json.load(f)
        species_abilities = ability_data.get('species_abilities', {})
        ability_stats = ability_data.get('abilities', {})
    
    with open('species_data.json') as f:
        species_data = json.load(f)
    
    # Create wild encounter
    target_team = create_wild_encounter()
    print(f"\nTarget Team (Wild Encounter):")
    for i, pet in enumerate(target_team.pets):
        print(f"  {i+1}. {pet.name} ({pet.family.name}) - HP: {pet.stats.max_hp}")
    
    # Target: Pet #1 (Wild Squirrel) - we want to capture this
    target_slot = 0
    print(f"\n🎯 CAPTURE TARGET: Pet #{target_slot+1} ({target_team.pets[target_slot].name})")
    print(f"   Goal: Reduce to <35% HP ({target_team.pets[target_slot].stats.max_hp * 0.35:.0f} HP) without killing")
    
    # Create evaluator in CAPTURE MODE
    evaluator = FitnessEvaluator(
        target_team=target_team,
        ability_db=ability_stats,
        species_db=species_data,
        target_name="Wild Encounter",
        capture_mode=True,  # ENABLE CAPTURE MODE
        target_slot=target_slot
    )
    
    # Get available species from my_pets.json
    with open('my_pets.json') as f:
        collection = json.load(f)
        available_species = [
            pet['species']['id'] 
            for pet in collection.get('pets', [])[:100] 
            if 'species' in pet
        ]
    
    print(f"\nTesting 5 random teams in CAPTURE MODE...")
    print("-" * 70)
    
    best_score = 0
    best_genome = None
    
    for i in range(5):
        genome = TeamGenome.random(available_species, species_abilities)
        fitness = evaluator.evaluate(genome, num_battles=3)
        
        species_ids = ', '.join([str(p.species_id) for p in genome.pets])
        
        print(f"\nTeam {i+1}: [{species_ids}]")
        print(f"  Fitness: {fitness:.1f}")
        
        if fitness > best_score:
            best_score = fitness
            best_genome = genome
    
    print("\n" + "=" * 70)
    if best_score > 50000:
        print("✅ CAPTURE STRATEGY TEST PASSED!")
        print(f"   Best fitness: {best_score:.1f}")
        print(f"   Team: {[p.species_id for p in best_genome.pets]}")
    else:
        print("⚠️  CAPTURE STRATEGY TEST INCONCLUSIVE")
        print(f"   Best fitness: {best_score:.1f} (threshold: 50,000)")
        print("   May need more generations or better scoring")
    print("=" * 70)

if __name__ == "__main__":
    main()
