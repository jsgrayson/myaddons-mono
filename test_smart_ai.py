#!/usr/bin/env python3
"""
Quick test script to verify the SmartEnemyAgent produces realistic battle outcomes.

This script runs a few sample battles between random teams and Squirt's team to
verify that:
1. Random teams don't always win (showing enemy AI is competent)
2. Win rates vary based on team composition
3. Debug logging is working correctly
"""

import sys
import json
from simulator import Team, Pet, PetStats, PetFamily, PetQuality, Ability, BattleSimulator, BattleState, TurnAction
from genetic.agents import SmartEnemyAgent
from genetic.genome import TeamGenome
from genetic.fitness import FitnessEvaluator

# Load Squirt encounter
with open('encounters.json') as f:
    encounter_data = json.load(f)['squirt']

# Build target team from encounters.json
def build_target_team():
    target_pets = []
    for npc_pet in encounter_data['npc_pets']:
        family_map = {
            'Magic': PetFamily.MAGIC,
            'Humanoid': PetFamily.HUMANOID,
            'Undead': PetFamily.UNDEAD,
            'Beast': PetFamily.BEAST,
            'Aquatic': PetFamily.AQUATIC,
            'Mechanical': PetFamily.MECHANICAL,
            'Elemental': PetFamily.ELEMENTAL,
            'Flying': PetFamily.FLYING,
            'Dragonkin': PetFamily.DRAGONKIN,
            'Critter': PetFamily.CRITTER,
        }
        family = family_map.get(npc_pet['family'], PetFamily.BEAST)
        
        abilities = []
        for ab_data in npc_pet['abilities']:
            abilities.append(Ability(
                id=ab_data['id'],
                name=ab_data['name'],
                power=ab_data['power'],
                accuracy=ab_data['accuracy'],
                speed=ab_data['speed'],
                cooldown=ab_data['cooldown'],
                family=family
            ))
        
        target_pets.append(Pet(
            species_id=npc_pet['species_id'],
            name=npc_pet['name'],
            family=family,
            quality=PetQuality.RARE,
            stats=PetStats(
                max_hp=npc_pet.get('stats', {}).get('health', npc_pet.get('health', 1546)),
                current_hp=npc_pet.get('stats', {}).get('health', npc_pet.get('health', 1546)),
                power=npc_pet.get('stats', {}).get('power', npc_pet.get('power', 273)),
                speed=npc_pet.get('stats', {}).get('speed', npc_pet.get('speed', 273))
            ),
            abilities=abilities
        ))
    
    return Team(pets=target_pets)

# Load ability data
with open('abilities.json') as f:
    ability_data = json.load(f)
    species_abilities = ability_data.get('species_abilities', {})

# Build ability DB
formatted_ability_db = {int(k): v for k, v in species_abilities.items()}

# Create evaluator
target_team = build_target_team()
evaluator = FitnessEvaluator(target_team, formatted_ability_db, {})

print("=" * 60)
print("TESTING SMART ENEMY AI")
print("=" * 60)
print(f"Target: {encounter_data['name']}")
print(f"Enemy Team: {', '.join([p.name for p in target_team.pets])}")
print()

# Test 5 random genomes
print("Testing 5 random genomes (should see varied win rates):")
print("-" * 60)

with open('my_pets.json') as f:
    collection = json.load(f)
    available_species = [pet['species']['id'] for pet in collection.get('pets', [])[:50] if 'species' in pet]

for i in range(5):
    genome = TeamGenome.random(available_species, formatted_ability_db)
    fitness = evaluator.evaluate(genome, num_battles=3)
    
    species_ids = ', '.join([str(p.species_id) for p in genome.pets])
    win_rate = genome.stats.get('win_rate', 0) * 100
    damage_pct = genome.stats.get('avg_damage_pct', 0) * 100
    
    print(f"Genome {i+1}: [{species_ids}]")
    print(f"  Fitness: {fitness:.1f} | Win Rate: {win_rate:.0f}% | Damage: {damage_pct:.0f}%")
    print()

print("=" * 60)
print("EXPECTED: Win rates should vary (not all 100%)")
print("If all teams show 100% win rate, enemy AI is still too weak")
print("=" * 60)
