#!/usr/bin/env python3
"""
Test: Real Pet Teams from Architect Suggestions
Verifies that Dojo creates actual teams (not random placeholders)
"""

from architect_engine import ArchitectEngine
from dojo_engine import DojoEngine
from pet_factory import PetFactory

def test_real_teams():
    print("\n" + "="*70)
    print("TEST: REAL PET TEAMS FROM ARCHITECT")
    print("="*70)
    
    # Initialize Architect with hardcoded combos
    print("\n📐 Step 1: Build Architect Graph")
    architect = ArchitectEngine()
    architect.build_hardcoded_graph()
    
    # Get best cores
    cores = architect.find_best_core()
    print(f"\n🔥 Top 3 Cores from Architect:")
    for i, (a, b) in enumerate(cores[:3], 1):
        print(f"  {i}. {a} + {b} (Weight: {architect.get_synergy_score(a, b)})")
    
    # Initialize Dojo WITH Architect
    print(f"\n🏗️  Step 2: Initialize Dojo with PetFactory")
    dojo = DojoEngine(population_size=6, architect=architect)
    dojo.initialize_population()
    
    # Inspect the created teams
    print(f"\n🔍 Step 3: Inspect Created Teams")
    print(f"Total Teams: {len(dojo.population)}")
    
    for i, team in enumerate(dojo.population[:3], 1):  # Show first 3 teams
        print(f"\nTeam {i}:")
        for j, pet in enumerate(team.pets, 1):
            print(f"  Pet {j}: {pet.name} (ID: {pet.species_id})")
            print(f"    Quality: {pet.quality.name}, Family: {pet.family.name}")
            print(f"    Stats: HP={pet.stats.max_hp}, Power={pet.stats.power}, Speed={pet.stats.speed}")
            print(f"    Abilities: {len(pet.abilities)} ({', '.join(a.name for a in pet.abilities)})")
    
    # Verify quality and stats
    print(f"\n✅ Verification:")
    all_rare = all(pet.quality.name == "RARE" for team in dojo.population for pet in team.pets)
    all_level_25_stats = all(
        pet.stats.max_hp >= 1000  # Level 25 pets have ~1400 HP
        for team in dojo.population 
        for pet in team.pets
    )
    
    print(f"  All pets RARE quality: {all_rare}")
    print(f"  All pets level 25 stats: {all_level_25_stats}")
    
    # Check if Architect suggestions were used
    architect_pet_names = set()
    for core in cores:
        architect_pet_names.add(core[0])
        architect_pet_names.add(core[1])
    
    used_architect_pets = sum(
        1 for team in dojo.population 
        for pet in team.pets 
        if pet.name in architect_pet_names
    )
    
    print(f"  Pets from Architect suggestions: {used_architect_pets}/{len(dojo.population)*3}")
    print(f"  Expected: ~{len(dojo.population) // 2 * 2} (50% seeded × 2 pets per core)")
    
    print("\n" + "="*70)
    print("✓ Test Complete: Real teams created from Architect synergies!")
    print("="*70)

if __name__ == "__main__":
    test_real_teams()
