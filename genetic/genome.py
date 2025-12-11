import random
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import copy

@dataclass
class StrategyGene:
    """Represents the strategy for a single pet"""
    # Priority list of ability slots (e.g., [1, 2, 3])
    # Note: These are 1-based slot numbers. 
    # If a pet has fewer abilities, the agent logic must handle it.
    priority: List[int] = field(default_factory=lambda: [1, 2, 3])
    # Simple conditions: {ability_slot: (condition_type, value)}
    # e.g., {3: ('enemy_hp_lt', 50)}
    conditions: Dict[int, tuple] = field(default_factory=dict)

@dataclass
class PetGene:
    """Represents a single pet in the team"""
    species_id: int
    breed_id: int = 3  # Default to B/B (Balanced)
    abilities: List[int] = field(default_factory=list) # [id1, id2, id3]
    strategy: StrategyGene = field(default_factory=StrategyGene)
    
    @staticmethod
    def get_available_breeds(species_id: int, species_db: Dict = None) -> List[int]:
        """Get available breeds for this species. Returns common breeds if not in DB."""
        if species_db and str(species_id) in species_db:
            species_data = species_db[str(species_id)]
            if 'available_breeds' in species_data:
                return species_data['available_breeds']
        # Default to common breeds (B/B, P/P, S/S, H/H)
        return [3, 4, 5, 6]

@dataclass
class TeamGenome:
    """Represents a full team solution (3 pets + strategies)"""
    pets: List[PetGene] = field(default_factory=list)
    fitness: float = 0.0
    stats: Dict = field(default_factory=dict) # Store win rate, damage, etc.
    
    @staticmethod
    def _select_valid_abilities(possible_abilities: List[int]) -> List[int]:
        """Safely select 3 abilities from the possible list"""
        if not possible_abilities:
            return [1, 2, 3] # Fallback defaults
            
        # Ensure we have enough to pick from, filling with available ones if needed
        # Slot 1 (Indices 0, 3)
        opts1 = []
        if len(possible_abilities) > 0: opts1.append(possible_abilities[0])
        if len(possible_abilities) > 3: opts1.append(possible_abilities[3])
        slot1 = random.choice(opts1) if opts1 else 1
        
        # Slot 2 (Indices 1, 4)
        opts2 = []
        if len(possible_abilities) > 1: opts2.append(possible_abilities[1])
        if len(possible_abilities) > 4: opts2.append(possible_abilities[4])
        # Fallback to slot 1's choice if slot 2 empty
        slot2 = random.choice(opts2) if opts2 else slot1
        
        # Slot 3 (Indices 2, 5)
        opts3 = []
        if len(possible_abilities) > 2: opts3.append(possible_abilities[2])
        if len(possible_abilities) > 5: opts3.append(possible_abilities[5])
        # Fallback to slot 2's choice if slot 3 empty
        slot3 = random.choice(opts3) if opts3 else slot2
        
        return [slot1, slot2, slot3]

    @classmethod
    def random(cls, available_species: List[int], ability_db: Dict):
        """Create a random team from available species"""
        genome = cls()
        
        # Pick 3 random unique pets
        species_picks = random.sample(available_species, 3)
        
        for species_id in species_picks:
            # Get abilities for this species (mock for now)
            # In real impl, look up in ability_db
            possible_abilities = ability_db.get(str(species_id)) or ability_db.get(species_id, [1, 2, 3, 4, 5, 6])
            
            # Pick one for each slot safely
            selected_abilities = cls._select_valid_abilities(possible_abilities)
            
            # Random strategy
            strategy = StrategyGene()
            random.shuffle(strategy.priority)
            
            # Add random conditions (30% chance for each slot)
            for slot in [1, 2, 3]:
                if random.random() < 0.3:
                    # Simple condition: execute if enemy HP < X%
                    strategy.conditions[slot] = ('enemy_hp_lt', random.randint(30, 70))
            
            genome.pets.append(PetGene(
                species_id=species_id,
                abilities=selected_abilities,
                strategy=strategy
            ))
            
        return genome

    @classmethod
    def from_team_ids(cls, team_ids: List[int], ability_db: Dict):
        """Create a genome from a specific list of pet IDs"""
        genome = cls()
        
        for species_id in team_ids:
            if species_id == 0: continue # Skip empty slots
            
            # Get valid abilities
            # Get valid abilities
            possible_abilities = ability_db.get(str(species_id)) or ability_db.get(species_id, [1, 2, 3, 4, 5, 6])
            if isinstance(possible_abilities, dict):
                possible_abilities = possible_abilities.get('abilities', [])
            selected_abilities = cls._select_valid_abilities(possible_abilities)
            
            # Default strategy
            strategy = StrategyGene()
            
            genome.pets.append(PetGene(
                species_id=species_id,
                abilities=selected_abilities,
                strategy=strategy
            ))
            
        return genome

    def mutate(self, available_species: List[int], ability_db: Dict, mutation_rate: float = 0.1, species_db: Dict = None):
        """Randomly modify the genome"""
        mutated = False
        for i in range(len(self.pets)):
            # Mutate Pet (Swap species)
            if random.random() < mutation_rate * 0.5: # Lower chance to swap whole pet
                new_species = random.choice(available_species)
                
                # Get valid abilities for new species
                # Get valid abilities for new species
                possible_abilities = ability_db.get(str(new_species)) or ability_db.get(new_species, [1, 2, 3, 4, 5, 6])
                
                # Pick valid abilities safely
                new_abilities = self._select_valid_abilities(possible_abilities)
                
                # Pick a valid breed for new species
                available_breeds = PetGene.get_available_breeds(new_species, species_db)
                new_breed = random.choice(available_breeds)
                
                # Reset abilities/strategy for new pet
                self.pets[i] = PetGene(species_id=new_species, breed_id=new_breed, abilities=new_abilities)
                mutated = True
            
            # Mutate Breed (Independent from species swap)
            if random.random() < mutation_rate * 0.8:  # High chance to try breed mutations
                pet = self.pets[i]
                available_breeds = PetGene.get_available_breeds(pet.species_id, species_db)
                if len(available_breeds) > 1:  # Only mutate if there are options
                    # Pick a different breed
                    new_breed = random.choice([b for b in available_breeds if b != pet.breed_id])
                    pet.breed_id = new_breed
                    mutated = True
                
            # Mutate Abilities
            if random.random() < mutation_rate:
                # Swap an ability choice (e.g. slot 1 option A -> B)
                pet = self.pets[i]
                # Swap an ability choice (e.g. slot 1 option A -> B)
                pet = self.pets[i]
                possible_abilities = ability_db.get(str(pet.species_id)) or ability_db.get(pet.species_id, [1, 2, 3, 4, 5, 6])
                
                # Pick a random slot to flip (0, 1, or 2)
                slot = random.randint(0, 2)
                
                # Determine the alternative ability for this slot
                # Slot 0: indices 0 or 3
                # Slot 1: indices 1 or 4
                # Slot 2: indices 2 or 5
                idx1 = slot
                idx2 = slot + 3
                
                # Bounds check: ensure pet has enough abilities and slot is valid
                if len(pet.abilities) > slot and len(possible_abilities) > idx2:
                    # Toggle between the two options
                    current = pet.abilities[slot]
                    option1 = possible_abilities[idx1]
                    option2 = possible_abilities[idx2]
                    
                    if current == option1:
                        pet.abilities[slot] = option2
                    elif current == option2:
                        pet.abilities[slot] = option1
                    mutated = True
                
            # Mutate Strategy (Priority)
            if random.random() < mutation_rate:
                random.shuffle(self.pets[i].strategy.priority)
                mutated = True
                
            # Mutate Strategy (Conditions)
            if random.random() < mutation_rate:
                # Add, remove, or change a condition
                strategy = self.pets[i].strategy
                if not strategy.conditions and random.random() < 0.5:
                    # Add new
                    slot = random.choice([1, 2, 3])
                    strategy.conditions[slot] = ('enemy_hp_lt', random.randint(30, 70))
                elif strategy.conditions:
                    if random.random() < 0.5:
                        # Remove random
                        slot = random.choice(list(strategy.conditions.keys()))
                        del strategy.conditions[slot]
                    else:
                        # Change value
                        slot = random.choice(list(strategy.conditions.keys()))
                        strategy.conditions[slot] = ('enemy_hp_lt', random.randint(30, 70))
                mutated = True
        
        # Reset fitness if mutated so it gets re-evaluated
        if mutated:
            self.fitness = 0

    def crossover(self, partner: 'TeamGenome') -> 'TeamGenome':
        """Combine with another genome to create a child"""
        child = TeamGenome()
        child.fitness = 0  # IMPORTANT: Force re-evaluation of children
        
        # Uniform Crossover: Pick each pet from either parent
        for i in range(3):
            if random.random() < 0.5:
                child.pets.append(copy.deepcopy(self.pets[i]))
            else:
                child.pets.append(copy.deepcopy(partner.pets[i]))
                
        return child
