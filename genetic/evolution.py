import random
import copy
from typing import List
from .genome import TeamGenome, PetGene, StrategyGene
from .fitness import FitnessEvaluator

class EvolutionEngine:
    def __init__(self, fitness_evaluator, population_size=50, mutation_rate=0.3, elitism_rate=0.2):
        self.evaluator = fitness_evaluator
        self.pop_size = population_size
        self.mutation_rate = mutation_rate
        self.elitism_count = int(population_size * elitism_rate)
        self.population = []
        self.generation = 0
        self.best_genome = None
        self.locked_slots = [False, False, False]
        self.slot_pools = [[], [], []]
        self.available_species = []
        self.ability_db = {}

    def get_type_effectiveness(self, attack_family, defend_family):
        strong_against = {
            1: {2, 4}, 2: {6, 3}, 3: {9, 5}, 4: {1, 5}, 5: {4}, 
            6: {3, 10}, 7: {10, 5}, 8: {5, 10}, 9: {7, 4}, 10: {8, 7}
        }
        # Remap values if using Enums or 0-9 scale (User uses 0-9 scale)
        # 0:Humanoid, 1:Dragon, 2:Flying, 3:Undead, 4:Critter, 5:Magic, 6:Elem, 7:Beast, 8:Aquatic, 9:Mech
        # Correct Mapping for 0-9 scale:
        strong_map_09 = {
            0: {1, 3}, 1: {5, 2}, 2: {8, 4}, 3: {0, 4}, 4: {3},
            5: {2, 9}, 6: {9, 4}, 7: {4, 9}, 8: {6, 3}, 9: {7, 6}
        }
        
        att = attack_family.value if hasattr(attack_family, 'value') else attack_family
        defn = defend_family.value if hasattr(defend_family, 'value') else defend_family
        
        if defn in strong_map_09.get(att, {}): return 1.5
        return 1.0

    def build_slot_pools(self, available_species, ability_db, is_carry_battle=False):
        """Builds optimized pools for each specific 1v1 fight."""
        enemy_team = getattr(self.evaluator, 'target_team', None)
        species_db = getattr(self.evaluator, 'species_db', {})
        ability_info_db = getattr(self.evaluator, 'ability_db', {})
        
        # Synergy Enablers: Abilities that make the whole team better
        # Priority order: Haunt first (most important), then damage amplifiers, then multi-hit
        SYNERGY_ABILITIES = {
            279,  # Haunt (Undead) - THE meta ability, DoT persists after death
            919,  # Black Claw (increases damage taken by 100%)
            581,  # Flock (multi-hit that synergizes with Black Claw)
            362,  # Howl (team-wide damage boost)
            492,  # Illusionary Barrier (strong defensive setup)
            706,  # Swarm (DoT + debuff)
            921,  # Hunting Party (team damage boost)
            593,  # Moonfire/Wild Magic (good for cleave)
            208,  # Supercharge (burst damage setup)
            284,  # Curse of Doom (execute mechanic)
        }
        synergy_pets = []
        
        # Pre-scan for synergy pets
        for sid in available_species:
            my_ability_ids = ability_db.get(sid, [])
            if isinstance(my_ability_ids, dict): my_ability_ids = my_ability_ids.get('abilities', [])
            if any(aid in SYNERGY_ABILITIES for aid in my_ability_ids):
                synergy_pets.append(sid)
        
        if not enemy_team: return
        self.slot_pools = [[], [], []]
        
        if not enemy_team: return
        self.slot_pools = [[], [], []]
        
        print(f"    [AI] Building {'Carry' if is_carry_battle else '1v1'} Counter Pools...")
        
        # For Carry Battles, we need a unified pool of strong pets for slots 1 & 2
        carry_pool = set()
        
        for i, enemy_pet in enumerate(enemy_team.pets):
            counters = []
            candidates = available_species if len(available_species) < 2000 else random.sample(available_species, 2000)
            
            for sid in candidates:
                score = 0
                s_data = species_db.get(str(sid)) or species_db.get(sid)
                my_ability_ids = ability_db.get(sid, [])
                if isinstance(my_ability_ids, dict): my_ability_ids = my_ability_ids.get('abilities', [])
                if not my_ability_ids: continue

                # 1. Strong Attack vs This Specific Enemy
                for aid in my_ability_ids:
                    ainfo = ability_info_db.get(str(aid)) or ability_info_db.get(aid)
                    if ainfo and isinstance(ainfo, dict):
                        atk_type = ainfo.get('family_id', 7)
                        if self.get_type_effectiveness(atk_type, enemy_pet.family) > 1.0:
                            score += 10; break
                
                # 2. Resistance vs This Specific Enemy
                if s_data:
                    my_fam = s_data.get('family_id', 7)
                    if self.get_type_effectiveness(enemy_pet.family, my_fam) < 1.0: score += 5
                
                # 3. Synergy Bonus (Always include synergy pets)
                if sid in synergy_pets: score += 5

                if score >= 10: counters.append(sid)
            
            # Ensure synergy pets are always available in the pool
            # (Unless pool is huge, then maybe just some? For now, add all unique)
            counters = list(set(counters + synergy_pets))
            
            if not counters: counters = available_species 
            
            if is_carry_battle:
                # Add to unified carry pool
                carry_pool.update(counters)
            else:
                self.slot_pools[i] = counters
                print(f"    [AI] Fight {i+1} Pool: {len(counters)} candidates (inc. {len(synergy_pets)} synergy).")

        if is_carry_battle:
            # Assign unified pool to slots 1 and 2
            # Slot 3 is the carry pet (handled by locking, but pool should be empty or irrelevant)
            final_pool = list(carry_pool)
            self.slot_pools[0] = final_pool
            self.slot_pools[1] = final_pool
            self.slot_pools[2] = [] # Should be locked anyway
            print(f"    [AI] Carry Pool (Slots 1&2): {len(final_pool)} candidates.")

    def initialize_population(self, available_species, ability_db, npc_name=None, strategy_manager=None, capture_mode=False, is_carry_battle=False):
        self.available_species = available_species
        self.ability_db = ability_db
        self.population = []
        self.build_slot_pools(available_species, ability_db, is_carry_battle=is_carry_battle)
        self.locked_slots = [False, False, False]
        
        # Initial Draft: Random picks from the correct pools
        for _ in range(self.pop_size):
            p1 = random.choice(self.slot_pools[0])
            p2 = random.choice(self.slot_pools[1])
            # For carry battles, p3 will be overwritten, but we need a valid ID for now
            p3 = random.choice(self.slot_pools[2]) if self.slot_pools[2] else random.choice(available_species)
            genome = TeamGenome.from_team_ids([p1, p2, p3], ability_db)
            self.population.append(genome)
        self.generation = 0

    def evolve_generation(self, available_species: List[int]):
        # 1. Evaluate
        for genome in self.population:
            if genome.fitness == 0:
                genome.fitness = self.evaluator.evaluate(genome)
        
        # Sort by Win Rate then Fitness
        self.population.sort(key=lambda g: (getattr(g, 'stats', {}).get('win_rate', 0), g.fitness), reverse=True)
        
        # Update Best (Always trust the latest run to catch regressions)
        self.best_genome = copy.deepcopy(self.population[0])
            
        # 2. Check Win Status
        status = getattr(self.best_genome, 'win_status', "LLL")
        while len(status) < 3: status += "L"
        
        # Sequential Locking
        if status[0] == "W": self.locked_slots[0] = True
        if status[1] == "W" and self.locked_slots[0]: self.locked_slots[1] = True
        if status[2] == "W" and self.locked_slots[1]: self.locked_slots[2] = True
        
        # DEBUG
        # print(f"DEBUG: Best Fitness: {self.best_genome.fitness}, Status: {status}, Locked: {self.locked_slots}")
        # print(f"DEBUG: Best Pet 0 Species: {self.best_genome.pets[0].species_id}")
        
        # Determine which Fight we are on
        active_slot = 0
        for i, locked in enumerate(self.locked_slots):
            if not locked:
                active_slot = i
                break

        # 3. Reproduction
        new_pop = []
        
        # Elitism: Keep top N
        for i in range(self.elitism_count):
            if i < len(self.population):
                elite = copy.deepcopy(self.population[i])
                # Enforce locks on elites too (in case lock status just changed)
                for j, is_locked in enumerate(self.locked_slots):
                    if is_locked:
                        elite.pets[j] = copy.deepcopy(self.best_genome.pets[j])
                new_pop.append(elite)
        
        # Fill the rest with bred children
        pool = self.slot_pools[active_slot] if active_slot < 3 else available_species
        
        while len(new_pop) < self.pop_size:
            # Selection
            parent_a = self._tournament_select()
            parent_b = self._tournament_select()
            
            # Crossover
            child = parent_a.crossover(parent_b)
            
            # Mutation
            # We always try to mutate to maintain diversity, especially in the active slot
            if random.random() < self.mutation_rate:
                # Mutate Pet (Swap species) - Higher chance if fitness is low
                if random.random() < 0.4:
                    # Mutate the Active Slot specifically
                    if active_slot < 3:
                        new_id = random.choice(pool)
                        possible_abs = self.ability_db.get(new_id, [])
                        selected_abs = []
                        if possible_abs:
                            if isinstance(possible_abs, list):
                                selected_abs = possible_abs[:3] if len(possible_abs)>=3 else possible_abs
                        
                        child.pets[active_slot] = PetGene(
                            species_id=new_id, 
                            abilities=selected_abs, 
                            strategy=StrategyGene()
                        )
                        child.fitness = 0
                else:
                    # Standard mutation (Abilities, Breeds, Strategy)
                    child.mutate(available_species, self.ability_db, self.mutation_rate, getattr(self.evaluator, 'species_db', None))
            
            # Enforce Locks (CRITICAL: Overwrite locked slots with the BEST known solution)
            # This ensures we don't "breed out" the winning pets for previous fights
            # MUST be done AFTER mutation to prevent accidental changes
            for i, is_locked in enumerate(self.locked_slots):
                if is_locked:
                    child.pets[i] = copy.deepcopy(self.best_genome.pets[i])
            
            new_pop.append(child)
            
        avg_fitness = sum(g.fitness for g in self.population) / self.pop_size
        self.population = new_pop
        self.generation += 1
        
        return {
            "generation": self.generation,
            "best_fitness": self.best_genome.fitness,
            "win_status": status,
            "avg_fitness": avg_fitness,
            "top_genomes": self.population[:3]
        }

    def _tournament_select(self, k=3):
        """Select the best individual from k random picks"""
        tournament = random.sample(self.population, k)
        return max(tournament, key=lambda g: (getattr(g, 'stats', {}).get('win_rate', 0), g.fitness))