"""
Sequential Slot Optimizer for Pet Battles

Strategy:
1. Test random Pet 1 until it survives/wins → Lock it
2. Test random Pet 2 (with locked Pet 1) until combo wins → Lock both  
3. Test random Pet 3 (with locked Pets 1+2) until full team wins → Done

Each slot cycles every generation until successful, then moves to next slot.
"""

import json
import random
from genetic.fitness import FitnessEvaluator
from simulator import Team, Pet, PetFamily, PetQuality, PetStats, Ability

# Load data
print("Loading Data...")
with open('abilities.json') as f:
    ability_data = json.load(f)
species_abilities = {int(k): v for k, v in ability_data.get('species_abilities', {}).items()}
abilities_db = ability_data.get('abilities', {})

with open('species_data.json') as f:
    species_db = json.load(f)

# Boss team (Major Payne)
def create_boss_team():
    # Grizzle abilities from abilities.json
    grizzle = Pet(979, "Grizzle", PetFamily.BEAST, PetQuality.EPIC, 
                  PetStats(1700, 1700, 320, 270), [
        Ability(id=348, name="Bash", power=20, accuracy=100, speed=0, cooldown=5, family=PetFamily.BEAST, hits=1),
        Ability(id=133, name="Hibernate", power=0, accuracy=100, speed=0, cooldown=4, family=PetFamily.BEAST, is_heal=True),
        Ability(id=124, name="Rampage", power=20, accuracy=100, speed=0, cooldown=3, family=PetFamily.BEAST, hits=3)])
    
    # Beakmaster abilities from abilities.json  
    beakmaster = Pet(978, "Beakmaster", PetFamily.MECHANICAL, PetQuality.EPIC,
                     PetStats(1500, 1500, 290, 300), [
        Ability(id=393, name="Batter", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.MECHANICAL, hits=1),
        Ability(id=646, name="Shock and Awe", power=20, accuracy=100, speed=0, cooldown=4, family=PetFamily.MECHANICAL, hits=1),
        Ability(id=459, name="Wind-Up", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.MECHANICAL, hits=2)])
    
    # Bloom abilities from abilities.json
    bloom = Pet(977, "Bloom", PetFamily.ELEMENTAL, PetQuality.EPIC,
                PetStats(1400, 1400, 340, 250), [
        Ability(id=350, name="Lash", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.ELEMENTAL, hits=1),
        Ability(id=335, name="Soothing Mists", power=20, accuracy=100, speed=0, cooldown=3, family=PetFamily.ELEMENTAL, is_heal=True),
        Ability(id=572, name="Entangling Roots", power=20, accuracy=100, speed=0, cooldown=4, family=PetFamily.ELEMENTAL, hits=1)])
    return Team([grizzle, beakmaster, bloom])

target_team = create_boss_team()
evaluator = FitnessEvaluator(target_team, abilities_db, species_db, target_name="Major Payne")

# Load User Collection
try:
    with open('my_pets.json', 'r') as f:
        user_data = json.load(f)
        user_species_ids = set()
        for pet in user_data.get('pets', []):
            if 'species' in pet and 'id' in pet['species']:
                # ONLY USE LEVEL 25 PETS
                if pet.get('level', 0) == 25:
                    user_species_ids.add(pet['species']['id'])
        
        print(f"Loaded {len(user_species_ids)} unique Level 25 species from user collection.")
        
        # Filter available_species
        all_species = list(species_abilities.keys())
        available_species = [sid for sid in all_species if sid in user_species_ids]
        print(f"Filtered to {len(available_species)} available species for optimization.")


        
except FileNotFoundError:
    print("⚠️ my_pets.json not found! Using ALL species.")
    available_species = list(species_abilities.keys())

# Initialize locked pets
# Slot 1: Pricklefury Hare (3272) - Killed Grizzle
locked_pets = [3272, None, None]  # Unlock Slot 2 to find a better counter

current_slot = 1  # Start at Slot 2 (Beakmaster)

# Pre-print locked info
print(f"🔒 Pre-Locked Slot 1: Pricklefury Hare (3272)")
print(f"Starting optimization for Slot 2 (Beakmaster) using USER COLLECTION...")

print(f"\nTarget: Major Payne (Sequential Slot Optimization)")
print(f"Strategy: Lock each Pet slot after it wins, then optimize next slot\n")

gen = 0
try:
    while current_slot < 3:
        gen += 1
        
        # Build team: locked pets + random for current slot
        test_species = [None, None, None]
        
        # Get current enemy to counter
        target_enemy = target_team.pets[current_slot]
        enemy_family = target_enemy.family
        
        # Type Advantage Lookup (Attacker Family -> Defender Family)
        # 1: Humanoid, 2: Dragonkin, 3: Flying, 4: Undead, 5: Critter, 
        # 6: Magic, 7: Elemental, 8: Beast, 9: Aquatic, 10: Mechanical
        
        # Target Family -> Best Attacking Family
        counter_map = {
            1: 4,   # Humanoid <- Undead
            2: 1,   # Dragonkin <- Humanoid
            3: 6,   # Flying <- Magic
            4: 5,   # Undead <- Critter
            5: 8,   # Critter <- Beast
            6: 2,   # Magic <- Dragonkin
            7: 9,   # Elemental <- Aquatic
            8: 10,  # Beast <- Mechanical
            9: 3,   # Aquatic <- Flying
            10: 7   # Mechanical <- Elemental
        }
        
        best_family = counter_map.get(enemy_family, None)
        
        # Filter available species for this family
        # We need to look up family in species_db
        candidate_species = []
        target_speed = target_enemy.stats.speed
        
        if best_family:
            for sid in available_species:
                # Check if pet has abilities of the counter type
                has_counter_ability = False
                
                # Get abilities for this species
                possible_abilities = abilities_db.get(str(sid)) or abilities_db.get(sid)
                if not possible_abilities:
                    # Try looking up in species_abilities map
                    ab_ids = species_abilities.get(sid, [])
                    for ab_id in ab_ids:
                        ab_info = abilities_db.get(str(ab_id))
                        if ab_info and ab_info.get('family_id') == best_family:
                            has_counter_ability = True
                            break
                
                # SPECIAL CASE: For Mechanical enemies (Beakmaster), also try Dragonkin
                # They are tanky and worked before (Ironbound Proto-Whelp)
                is_dragonkin = False
                if enemy_family == 10: # Mechanical
                    s_data = species_db.get(str(sid))
                    if s_data and s_data.get('family_id') == 2: # Dragonkin
                        is_dragonkin = True

                if has_counter_ability or is_dragonkin:
                    # Soft Speed Filter: Prefer pets faster than enemy
                    # We don't have exact stats here easily without instantiating, 
                    # but we can check base stats in species_db if available
                    s_data = species_db.get(str(sid))
                    if s_data and 'base_stats' in s_data:
                        # Estimate speed (level 25 rare)
                        base_speed = s_data['base_stats'].get('speed', 8)
                        est_speed = int(base_speed * 25 * 1.3) # Rough estimate
                        if est_speed > target_speed:
                            candidate_species.append(sid)
                        elif random.random() < 0.4: # 40% chance to include slower pets (Dragonkin are often slow)
                            candidate_species.append(sid)
                    else:
                        candidate_species.append(sid)
        
        # Fallback if no specific counters found or random chance to explore
        if not candidate_species or random.random() < 0.2:
            candidate_species = available_species

        # SEEDING INTERCHANGEABLE PETS
        # Prioritize pets that are known good substitutes (e.g. Aquatic for Slot 3)
        # Slot 2 Substitutes (Aquatic) are great for Slot 3 (vs Elemental)
        priority_candidates = [847, 3331, 3332, 340, 4496, 383, 566, 751, 2865]
        
        # Zandalari Raptors for Slot 2 (Beakmaster)
        # IDs: Footslasher (1181), Kneebiter (1182), Anklerender (1180), Toenibbler (1183)
        # Note: Need to verify IDs. Assuming standard IDs based on names.
        # Actually, let's just use the ones we found in grep if possible, or just add them by ID if we knew them.
        # Since we don't have IDs handy, we'll rely on the random search picking them up eventually, 
        # OR we can add a name-based filter in the loop below.
        
        # Better: Add a name-based priority in the candidate selection
        
        # If we are fighting Elemental (Bloom), prioritize Aquatic substitutes
        if enemy_family == 7: # Elemental
             # Filter priority candidates that are in available_species
             valid_priority = [pid for pid in priority_candidates if pid in available_species]
             if valid_priority:
                 # 50% chance to pick from priority list
                 if random.random() < 0.5:
                     candidate_species = valid_priority
        
        # If we are fighting Mechanical (Beakmaster), prioritize Zandalari Raptors
        if enemy_family == 10: # Mechanical
            raptor_candidates = []
            for sid in available_species:
                s_name = species_db.get(str(sid), {}).get('name', '')
                if 'Zandalari' in s_name:
                    raptor_candidates.append(sid)
            
            if raptor_candidates and random.random() < 0.7: # 70% chance to pick raptors
                candidate_species = raptor_candidates

        # DEBUG: Print candidate count
        # if current_slot == 1:
        #    print(f"DEBUG: Found {len(candidate_species)} candidates for family {best_family}")

        for i in range(3):
            if locked_pets[i]:
                test_species[i] = locked_pets[i]
            elif i == current_slot:
                # Pick from candidates (prioritizing counters)
                test_species[i] = random.choice(candidate_species)
            else:
                test_species[i] = random.choice(available_species)
        
        # Create genome and test
        from genetic.genome import TeamGenome
        genome = TeamGenome.from_team_ids(test_species, ability_data)
        
        # FORCE COUNTER ABILITIES
        # Ensure the selected pet actually uses the abilities that counter the enemy
        # OR abilities that match its own family (STAB) if no hard counter exists
        
        pet = genome.pets[current_slot]
        # Get all possible abilities for this pet
        possible_abilities = abilities_db.get(str(pet.species_id)) or abilities_db.get(pet.species_id)
        
        if possible_abilities:
            # Determine target ability types
            # 1. Counter type (best_family)
            # 2. Pet's own family (STAB - Same Type Attack Bonus, though not in WoW pets, usually stronger)
            # 3. Neutral damage (avoid weak types)
            
            target_types = []
            if best_family:
                target_types.append(best_family)
            
            # Add pet's own family as fallback priority
            s_data = species_db.get(str(pet.species_id))
            if s_data:
                target_types.append(s_data.get('family_id'))
            
            # Find abilities that match the target types
            chosen_abilities = {} # slot -> ability_id
            
            # possible_abilities is usually a list of 6 IDs
            # We need to look up their details
            for i, ab_id in enumerate(possible_abilities):
                ab_info = abilities_db.get(str(ab_id))
                if ab_info:
                    ab_type = ab_info.get('family_id')
                    slot = i % 3
                    
                    # Priority 1: Counter Type
                    if best_family and ab_type == best_family:
                        chosen_abilities[slot] = ab_id
                    
                    # Priority 2: Pet's Own Type (if slot not filled by counter)
                    elif slot not in chosen_abilities and ab_type in target_types:
                         chosen_abilities[slot] = ab_id
            
            # Apply these abilities to the genome
            for slot, ab_id in chosen_abilities.items():
                pet.abilities[slot] = ab_id
        
        # Randomize strategy for the current slot to give it a chance
        # (Otherwise it just uses 1, 2, 3 priority which might be bad)
        import random
        for i, pet in enumerate(genome.pets):
            if i == current_slot or not locked_pets[i]:
                random.shuffle(pet.strategy.priority)
                # Add some random conditions
                if random.random() < 0.3:
                    pet.strategy.conditions[random.choice([1,2,3])] = ('enemy_hp_lt', random.randint(30, 70))
        
        # HARDCODE ABILITIES & STRATEGY FOR WINNING PETS (To reproduce win)
        # Pricklefury Hare (3272): Scratch (119), Dodge (312), Burrow (159)
        if genome.pets[0].species_id == 3272:
             genome.pets[0].abilities = [119, 312, 159]
             genome.pets[0].strategy.priority = [2, 3, 1] # Dodge > Burrow > Scratch
        
        # Zandalari Raptors (Black Claw + Hunting Party)
        # IDs: Anklerender(1180), Kneebiter(1181), Footslasher(1182), Toenibbler(1183)
        # Abilities: Black Claw(919), Hunting Party(921), Swarm(706)
        if genome.pets[1].species_id in [1180, 1181, 1182, 1183]:
             # Force the combo abilities
             genome.pets[1].abilities = [919, 921, 706]
             # Force the combo strategy: Black Claw -> Hunting Party -> Swarm
             # Indices: 0=Black Claw, 1=Hunting Party, 2=Swarm
             # Priority: 1 (Black Claw) > 2 (Hunting Party) > 3 (Swarm)
             genome.pets[1].strategy.priority = [1, 2, 3]
        
        # Tiny Goldfish (652): Water Jet (118), Whirlpool (513), Pump (297)
        if genome.pets[1].species_id == 652:
             genome.pets[1].abilities = [118, 513, 297]
        
        # Evaluate
        result = evaluator.play_battle(genome)
        fitness = result.get('fitness', 0)
        winner = result.get('winner', 'npc')
        events = result.get('events', [])
        
        # Get names
        names = [species_db.get(str(sid), {}).get('name', str(sid)) for sid in test_species]
        
        # Check if current enemy pet died
        target_pet_name = target_team.pets[current_slot].name
        enemy_died = False
        
        for e in events:
            if e['type'] == 'death' and e['pet'] == target_pet_name:
                enemy_died = True
                break
        
        # Success criteria: Enemy pet for this slot died
        if enemy_died:
            # VERIFICATION PHASE
            # Run 3 more battles to ensure this isn't a fluke
            print(f"   Potential Winner Found: {names[current_slot]}. Verifying (3 runs)...")
            verified = True
            for v_run in range(3):
                v_result = evaluator.play_battle(genome)
                v_events = v_result.get('events', [])
                v_enemy_died = False
                v_target_pet_name = target_team.pets[current_slot].name
                for ve in v_events:
                    if ve['type'] == 'death' and ve['pet'] == v_target_pet_name:
                        v_enemy_died = True
                        break
                
                if not v_enemy_died:
                    print(f"   ❌ Verification Failed on run {v_run+1}.")
                    verified = False
                    break
            
            if verified:
                locked_pets[current_slot] = test_species[current_slot]
                locked_name = names[current_slot]
                print(f"\n🔒 Gen {gen}: LOCKED Slot {current_slot+1} = {locked_name} (Enemy '{target_pet_name}' killed - Verified 3x)")
                print(f"   Team so far: {names}")
                
                # Print Move Order for the winning pet
                print(f"   [WINNING MOVE ORDER]")
                for e in events:
                    if e['type'] == 'turn_start':
                        print(f"   Turn {e['turn']}:")
                    elif e['type'] == 'ability_use' and e['source'] == locked_name:
                        print(f"     - Used {e['ability']}")
                
                current_slot += 1
                if current_slot >= 3:
                    print(f"\n✅ COMPLETE! Final Team: {names}")
                    # Print full details with abilities
                    print("\n[FINAL STRATEGY DETAILS]")
                    for i, pet in enumerate(genome.pets):
                        pname = names[i]
                        pabilities = pet.abilities
                        print(f"Slot {i+1}: {pname} (ID: {pet.species_id})")
                        print(f"  Abilities: {pabilities}")
                    break
            else:
                # If verification failed, we continue the loop (don't lock)
                pass
        else:
            # DEBUG: Show HP remaining for target
            target_hp = 0
            if result.get('final_state'):
                for p in result['final_state'].enemy_team.pets:
                    if p.name == target_pet_name:
                        target_hp = p.stats.current_hp
            
            # DEBUG: Check Beakmaster (Slot 2) HP
            beak_hp = -1
            if result.get('final_state'):
                 beak_hp = result['final_state'].enemy_team.pets[1].stats.current_hp
            
            print(f"Gen {gen}: Slot {current_slot+1} testing: {names[current_slot]} (Failed vs {target_pet_name}, HP: {target_hp}) [Beakmaster HP: {beak_hp}]")
            
            # DEBUG: Print log for one failure to see what's happening
            # Also print for Zandalari to debug why they fail
            if (current_slot == 1 and gen % 100 == 0) or 'Zandalari' in names[current_slot]:
                 # Re-run with logging enabled to capture events
                 debug_result = evaluator.play_battle(genome, enable_logging=True)
                 debug_events = debug_result.get('events', [])
                 
                 print(f"   [DEBUG FAILURE LOG - {names[current_slot]}]")
                 for e in debug_events:
                    if e['type'] == 'ability_use':
                        print(f"     - {e['source']} used {e['ability']}")
                    elif e['type'] == 'damage':
                        print(f"       -> Took {e.get('amount')} damage from {e.get('actor')}'s {e.get('ability')}")
                    elif e['type'] == 'heal':
                        print(f"       -> Healed {e.get('amount')} from {e.get('actor')}'s {e.get('ability')}")
                    elif e['type'] == 'buff_applied':
                        print(f"       + {e.get('target')} gained {e.get('buff')}")
                    elif e['type'] == 'death':
                        print(f"       X {e.get('pet')} died!")
                    elif e['type'] == 'swap':
                        print(f"       <-> {e.get('actor')} swapped to {e.get('new_index')}")

except KeyboardInterrupt:
    print("\n\nStopped by user")

print(f"\nFinal locked team: {[species_db.get(str(p), {}).get('name', str(p)) if p else 'None' for p in locked_pets]}")
