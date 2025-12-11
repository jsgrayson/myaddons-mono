from typing import List, Dict, Any, Optional
try:
    from simulator import BattleSimulator, BattleState, Team, Pet, Ability, TurnAction, PetStats, PetFamily, PetQuality
except ImportError:
    from simulator import BattleSimulator, BattleState, Team, Pet, Ability, TurnAction, PetStats, PetFamily
    class PetQuality:
        POOR=0; COMMON=1; UNCOMMON=2; RARE=3; EPIC=4; LEGENDARY=5

from .genome import TeamGenome

class FitnessEvaluator:
    def __init__(self, target_team: Team, ability_db: Dict, species_db: Dict, npc_priorities: Dict = None, target_name: str = "Unknown", capture_mode: bool = False, target_slot: int = 0):
        self.target_team = target_team
        self.ability_db = ability_db
        self.species_db = species_db
        self.npc_priorities = npc_priorities or {}
        self.target_name = target_name
        self.capture_mode = capture_mode
        self.target_slot = target_slot  # Which enemy slot to capture (0, 1, or 2)
        self.simulator = BattleSimulator(rng_seed=None) 
        print("[SYSTEM] Fitness Evaluator: SAFETY_PATCH Loaded.")

    def _create_agents(self, genome: TeamGenome):
        player_team = self._genome_to_team(genome)
        
        # Enemy agent with ability priorities for synergy (e.g., Wind-Up -> Shock and Awe)
        from simulator.npc_ai import create_npc_agent
        from simulator.smart_agent import create_smart_enemy_agent
        
        # Handle Priority Script (New Format - List) vs Ability Priorities (Old Format - Dict)
        priority_script = None
        ability_priorities = None
        
        if isinstance(self.npc_priorities, list):
            priority_script = self.npc_priorities
        elif isinstance(self.npc_priorities, dict):
            # Convert keys to int if possible (Old format)
            try:
                ability_priorities = {int(k): v for k, v in self.npc_priorities.items()}
            except ValueError:
                # Might be the huge dict of scripts? We shouldn't be passing the huge dict here anymore.
                pass

        base_agent = create_smart_enemy_agent(difficulty=1.0, ability_priorities=ability_priorities)
        enemy_agent = create_npc_agent(self.target_name, base_agent, priority_script=priority_script)
        
        def genome_agent(state: BattleState) -> TurnAction:
            active_idx = state.player_team.active_pet_index
            if active_idx >= len(state.player_team.pets): return TurnAction(actor='player', action_type='pass')
            active_pet = state.player_team.pets[active_idx]
            enemy_pet = state.enemy_team.get_active_pet()
            
            # 1. Mandatory Swap
            if not active_pet.stats.is_alive():
                for i, p in enumerate(state.player_team.pets):
                    if p.stats.is_alive(): return TurnAction(actor='player', action_type='swap', target_pet_index=i)
                return TurnAction(actor='player', action_type='pass')

            if enemy_pet and enemy_pet.stats.is_alive():
                # 2. DEFENSIVE REFLEXES
                predicted_action = None
                try: predicted_action = enemy_agent(state.copy())
                except: pass

                if predicted_action and predicted_action.action_type == 'ability':
                    ab_name = predicted_action.ability.name
                    nuke_keywords = ["Wind-Up", "Ion Cannon", "Surge", "Pump", "Lock-On", "Shock and Awe"]
                    has_nuke_buff = any("Wind-Up" in b.name or "Pump" in b.name for b in enemy_pet.active_buffs)
                    
                    if any(k in ab_name for k in nuke_keywords) or has_nuke_buff:
                        defensives = ["Dodge", "Decoy", "Deflection", "Burrow", "Lift-Off", "Evanescence", "Bubble"]
                        for ab in active_pet.abilities:
                            if active_pet.can_use_ability(ab) and any(d in ab.name for d in defensives):
                                if "Burrow" in ab.name or "Lift-Off" in ab.name:
                                    if active_pet.stats.speed > enemy_pet.stats.speed:
                                        return TurnAction(actor='player', action_type='ability', ability=ab)
                                else:
                                    return TurnAction(actor='player', action_type='ability', ability=ab)

                # 3. EXECUTE
                for ab in active_pet.abilities:
                    if active_pet.can_use_ability(ab):
                        fam_mod = self.simulator.damage_calc.get_family_multiplier(ab.family, enemy_pet.family)
                        if (ab.power * fam_mod) >= enemy_pet.stats.current_hp:
                            return TurnAction(actor='player', action_type='ability', ability=ab)

            # 4. STANDARD PRIORITY
            try:
                pet_gene = genome.pets[active_idx]
                for slot in pet_gene.strategy.priority:
                    idx = slot - 1
                    if 0 <= idx < len(active_pet.abilities):
                        abil = active_pet.abilities[idx]
                        if active_pet.can_use_ability(abil): return TurnAction(actor='player', action_type='ability', ability=abil)
            except: pass
            
            best_ab = None
            best_pwr = -1
            for ab in active_pet.abilities:
                if active_pet.can_use_ability(ab):
                    if ab.power > best_pwr:
                        best_pwr = ab.power
                        best_ab = ab
            if best_ab: return TurnAction(actor='player', action_type='ability', ability=best_ab)
            
            return TurnAction(actor='player', action_type='pass')

        return player_team, genome_agent, enemy_agent

    def evaluate(self, genome: TeamGenome, num_battles: int = 5) -> float:
        player_team, genome_agent, enemy_agent = self._create_agents(genome)
        if not player_team or not player_team.pets: return 0.0

        total_score = 0
        wins = 0
        enemy_max_hp = sum(p.stats.max_hp for p in self.target_team.pets)
        slot_kills = [True, True, True]

        total_turns = 0
        min_turns = 999
        max_turns = 0
        
        for _ in range(num_battles):
            battle_state = BattleState(player_team.copy(), self.target_team.copy(), 1)
            result = self.simulator.simulate_battle(battle_state, genome_agent, enemy_agent, max_turns=45, enable_logging=False)
            
            turns = result['turns']
            total_turns += turns
            if turns < min_turns: min_turns = turns
            if turns > max_turns: max_turns = turns

            if result['turns'] >= 40:
                for i in range(3): slot_kills[i] = False
                continue

            if result.get('final_state'):
                enemy_team = result['final_state'].enemy_team
                for i, p in enumerate(enemy_team.pets):
                    if p.stats.is_alive(): slot_kills[i] = False

            battle_score = 0
            if result.get('final_state'):
                # CAPTURE MODE SCORING
                if self.capture_mode:
                    target_pet = result['final_state'].enemy_team.pets[self.target_slot]
                    target_hp_pct = target_pet.stats.current_hp / max(1, target_pet.stats.max_hp)
                    
                    # Check if target is alive
                    if not target_pet.stats.is_alive():
                        # Killed target - bad, but not as bad as losing
                        battle_score += 1000
                    elif target_hp_pct < 0.35:
                        # Target in capture range - PERFECT!
                        battle_score += 100000
                        # Bonus for being close to 35%
                        closeness = 1.0 - abs(target_hp_pct - 0.35)
                        battle_score += closeness * 10000
                    else:
                        # Target alive but not in range - reward progress
                        battle_score += (1.0 - target_hp_pct) * 50000
                   
                    # Check non-target pets are dead
                    for i, pet in enumerate(result['final_state'].enemy_team.pets):
                        if i == self.target_slot:
                            continue
                        if not pet.stats.is_alive():
                            battle_score += 20000
                        else:
                            hp_pct = pet.stats.current_hp / max(1, pet.stats.max_hp)
                            battle_score -= hp_pct * 10000
                    
                    # Reward our pet survival
                    for pet in result['final_state'].player_team.pets:
                        if pet.stats.is_alive():
                            hp_pct = pet.stats.current_hp / max(1, pet.stats.max_hp)
                            battle_score += hp_pct * 5000
                
                # NORMAL MODE SCORING
                else:
                    enemy_rem = sum(p.stats.current_hp for p in result['final_state'].enemy_team.pets)
                    dmg_pct = (enemy_max_hp - enemy_rem) / max(1, enemy_max_hp)
                    battle_score += (dmg_pct * 5000)
                    
                    for i, enemy_p in enumerate(result['final_state'].enemy_team.pets):
                        if not enemy_p.stats.is_alive():
                             battle_score += 2000 * (2 ** i)
                
                # Common scoring for both modes
                surviving = sum(1 for p in result['final_state'].player_team.pets if p.stats.is_alive())
                battle_score += (surviving * 500)
            
            if result['winner'] == 'player':
                wins += 1
                battle_score += 50000
                battle_score += (40 - min(result['turns'], 40)) * 100

            total_score += battle_score

        if wins < num_battles:
            total_score *= 0.5
            
        status_chars = []
        for k in slot_kills: status_chars.append("W" if k else "L")
        genome.win_status = "".join(status_chars)
        
        # Attach detailed stats to genome for UI
        if not hasattr(genome, 'stats'): genome.stats = {}
        genome.stats['win_rate'] = wins / num_battles
        genome.stats['avg_turns'] = total_turns / num_battles
        genome.stats['min_turns'] = min_turns
        genome.stats['max_turns'] = max_turns
        
        return total_score / num_battles

    def play_battle(self, genome: TeamGenome, enable_logging: bool = True) -> Dict:
        player_team, genome_agent, enemy_agent = self._create_agents(genome)
        battle_state = BattleState(player_team.copy(), self.target_team.copy(), 1)
        return self.simulator.simulate_battle(battle_state, genome_agent, enemy_agent, max_turns=50, enable_logging=enable_logging)

    def _genome_to_team(self, genome: TeamGenome) -> Team:
        pets = []
        for pet_gene in genome.pets:
            if pet_gene.species_id == -1:
                # Level 1 Carry Pet
                try: fam = PetFamily.CRITTER
                except: fam = PetFamily(4)
                
                stats = PetStats(max_hp=150, current_hp=150, power=0, speed=0)
                pets.append(Pet(species_id=-1, name="Level 1 Carry", family=fam, stats=stats, abilities=[], quality=PetQuality.POOR))
                continue

            species_data = self.species_db.get(str(pet_gene.species_id)) or self.species_db.get(pet_gene.species_id)
            
            base = {'health': 8, 'power': 8, 'speed': 8}
            if species_data and 'base_stats' in species_data: base = species_data['base_stats']
            hp = int((base.get('health', 8) * 5 * 25 * 1.3) + 100)
            power = int(base.get('power', 8) * 25 * 1.3)
            speed = int(base.get('speed', 8) * 25 * 1.3)
            
            name = species_data.get('name', f"Pet {pet_gene.species_id}") if species_data else f"Pet {pet_gene.species_id}"
            family_id = species_data.get('family_id', 7) if species_data else 7
            stats = PetStats(max_hp=hp, current_hp=hp, power=power, speed=speed)
            
            abilities = []
            for ab_id in pet_gene.abilities:
                ab_info = self.ability_db.get(str(ab_id)) or self.ability_db.get(ab_id)
                if ab_info:
                    if isinstance(ab_info, list):
                        ab_info = {'id': ab_id, 'name': str(ab_info[1]) if len(ab_info)>1 else "Unknown", 'family_id': 7, 'power': 20, 'accuracy': 100, 'cooldown': 0, 'speed': 0}
                    
                    # CRITICAL FIX: Handle Family ID 0
                    fam_val = ab_info.get('family_id', 7)
                    try:
                        fam = PetFamily(fam_val)
                    except ValueError:
                        # If 0 or invalid, fallback to BEAST (7)
                        fam = PetFamily(7)

                    abilities.append(Ability(
                        id=ab_id, 
                        name=ab_info.get('name', 'Unknown'), 
                        power=ab_info.get('power', 20), 
                        accuracy=ab_info.get('accuracy', 100), 
                        speed=ab_info.get('speed', 0), 
                        cooldown=ab_info.get('cooldown', 0), 
                        family=fam, 
                        effect_type=ab_info.get('effect_type'), 
                        is_heal=ab_info.get('is_heal', False),
                        priority=ab_info.get('priority', 0)
                    ))
                else:
                    abilities.append(Ability(id=ab_id, name="Unknown", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.BEAST))

            try: pet_family = PetFamily(family_id)
            except: pet_family = PetFamily.BEAST
            pets.append(Pet(species_id=pet_gene.species_id, name=name, family=pet_family, stats=stats, abilities=abilities, quality=PetQuality.RARE))
        
        return Team(pets=pets)