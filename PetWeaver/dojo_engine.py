import random
import time
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

from simulator import BattleSimulator, BattleState, Team, Pet, Ability, PetStats, PetFamily, PetQuality, TurnAction

# Import PetFactory for creating real pets from names
try:
    from pet_factory import PetFactory
    HAS_PET_FACTORY = True
except ImportError:
    HAS_PET_FACTORY = False
    print("⚠️  PetFactory not available, using random pets")

class DojoEngine:
    """
    Manages Self-Play sessions where the AI plays against itself to learn strategies.
    Uses an evolutionary approach where teams compete against each other.
    NOW WITH ARCHITECT INTEGRATION: Seeds population with proven synergies.
    """
    
    def __init__(self, population_size=20, architect=None):
        self.population_size = population_size
        self.population: List[Team] = []
        self.generation = 0
        self.history = []
        self.is_running = False
        self.simulator = BattleSimulator(rng_seed=None) # Random seed for variety
        self.architect = architect  # The Architect engine for synergy guidance
        
        # Initialize PetFactory for creating real pets
        self.pet_factory = PetFactory() if HAS_PET_FACTORY else None
        
        # Load pet data for random generation
        self.pet_db = self._load_pet_db()
        self.ability_db = self._load_ability_db()

    def _load_pet_db(self):
        # Placeholder: Load from JSON or DB
        # For now, return a small set of mock pets if file missing
        if os.path.exists('pet_db.json'):
            with open('pet_db.json', 'r') as f:
                return json.load(f)
        return []

    def _load_ability_db(self):
        if os.path.exists('ability_db.json'):
            with open('ability_db.json', 'r') as f:
                return json.load(f)
        return {}

    def generate_random_team(self) -> Team:
        """Generates a random team of 3 pets"""
        pets = []
        for _ in range(3):
            # Create random pet
            # In a real implementation, pick from pet_db
            # For MVP, creating dummy pets
            family = random.choice(list(PetFamily))
            pet = Pet(
                species_id=random.randint(1, 1000),
                name=f"Dojo Pet {random.randint(1, 9999)}",
                family=family,
                quality=PetQuality.RARE,
                stats=PetStats(max_hp=1400, current_hp=1400, power=280, speed=280),
                abilities=[
                    Ability(id=1, name="Attack", power=20, accuracy=100, speed=0, cooldown=0, family=family)
                ]
            )
            pets.append(pet)
        return Team(pets=pets)


    def initialize_population(self):
        """
        Initialize population with a mix of:
        - Architect-suggested cores (if available)
        - Random teams (for exploration)
        """
        self.population = []
        
        if self.architect and self.architect.graph.number_of_edges() > 0:
            # Use Architect to seed 50% of population
            architect_count = self.population_size // 2
            
            print(f"🏗️  Architect seeding {architect_count} teams from synergy graph...")
            
            # Get best cores
            cores = self.architect.find_best_core()
            
            for i in range(architect_count):
                # Cycle through top cores
                core = cores[i % len(cores)] if cores else None
                
                if core and self.pet_factory:
                    # Create REAL pets from Architect suggestions!
                    pet_a = self.pet_factory.create_pet(core[0])
                    pet_b = self.pet_factory.create_pet(core[1])
                    pet_c = self.generate_random_team().pets[0]  # Third slot: exploration
                    
                    if pet_a and pet_b:
                        team = Team(pets=[pet_a, pet_b, pet_c])
                        self.population.append(team)
                        continue
                
                # Fallback: Create random team
                self.population.append(self.generate_random_team())
            
            print(f"   ✓ Seeded {architect_count} Architect-guided teams")
        
        # Fill rest with random teams
        while len(self.population) < self.population_size:
            self.population.append(self.generate_random_team())
        
        print(f"   ✓ Added {self.population_size - len(self.population) if self.architect else self.population_size} random teams for exploration")
        
        self.generation = 0
        self.history = []

    def run_generation(self):
        """Runs one generation of self-play (Tournament or Round Robin)"""
        if not self.population:
            self.initialize_population()
            
        scores = {i: 0 for i in range(len(self.population))}
        matches = []
        
        # Simple Tournament: Random Pairings
        # Each team plays 3 games against random opponents
        for i in range(len(self.population)):
            for _ in range(3):
                opponent_idx = random.randint(0, len(self.population) - 1)
                if i == opponent_idx: continue
                
                team1 = self.population[i]
                team2 = self.population[opponent_idx]
                
                winner_idx = self._simulate_match(team1, team2)
                
                if winner_idx == 1:
                    scores[i] += 1
                else:
                    scores[opponent_idx] += 1
                    
        # Selection & Evolution
        sorted_indices = sorted(scores, key=scores.get, reverse=True)
        top_indices = sorted_indices[:self.population_size // 2] # Top 50%
        
        next_gen = []
        
        # Elitism: Keep top 10%
        elite_count = max(1, self.population_size // 10)
        for i in range(elite_count):
            next_gen.append(self.population[top_indices[i]])
            
        # Reproduction: Fill rest
        while len(next_gen) < self.population_size:
            parent1_idx = random.choice(top_indices)
            parent2_idx = random.choice(top_indices)
            child = self._crossover(self.population[parent1_idx], self.population[parent2_idx])
            self._mutate(child)
            next_gen.append(child)
            
        self.population = next_gen
        self.generation += 1
        
        # Record Stats
        avg_score = sum(scores.values()) / len(scores)
        best_score = scores[top_indices[0]]
        self.history.append({
            "generation": self.generation,
            "avg_score": avg_score,
            "best_score": best_score,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "generation": self.generation,
            "avg_score": avg_score,
            "best_score": best_score
        }

    def _simulate_match(self, team1: Team, team2: Team) -> int:
        """Returns 1 if team1 wins, 2 if team2 wins"""
        
        state = BattleState(team1, team2, turn_number=1, rng_seed=random.randint(0, 10000))
        
        # Simple Agents
        def agent(s):
            active = s.player_team.get_active_pet()
            if active and active.can_use_ability(active.abilities[0]):
                return TurnAction('player', 'ability', ability=active.abilities[0])
            return TurnAction('player', 'pass')
            
        def enemy_agent(s):
            active = s.enemy_team.get_active_pet()
            if active and active.can_use_ability(active.abilities[0]):
                return TurnAction('enemy', 'ability', ability=active.abilities[0])
            return TurnAction('enemy', 'pass')

        result = self.simulator.simulate_battle(state, agent, enemy_agent)
        return 1 if result['winner'] == 'player' else 2

    def _crossover(self, parent1: Team, parent2: Team) -> Team:
        # Mix pets from parents
        child_pets = []
        for i in range(3):
            if random.random() < 0.5:
                child_pets.append(parent1.pets[i]) # Should clone
            else:
                child_pets.append(parent2.pets[i]) # Should clone
        return Team(pets=child_pets)

    def _mutate(self, team: Team):
        # Randomly swap a pet
        if random.random() < 0.1:
            team.pets[random.randint(0, 2)] = self.generate_random_team().pets[0]

    def get_status(self):
        return {
            "running": self.is_running,
            "generation": self.generation,
            "history": self.history[-10:] if self.history else []
        }
