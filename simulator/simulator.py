from typing import List, Dict, Optional, Union, Callable
from .battle_state import BattleState, TurnAction, BuffType
from .damage_calculator import DamageCalculator
from .turn_system import TurnSystem
from .buff_tracker import BuffTracker
from .special_encounters import SpecialEncounterHandler

class BattleLog:
    def __init__(self):
        self.events: List[Dict] = []
        self.turn_summaries: List[str] = []
    def add_event(self, event: Dict):
        self.events.append(event)
    def add_turn_summary(self, turn: int, summary: str):
        self.turn_summaries.append(f"Turn {turn}: {summary}")
    def get_full_log(self) -> str:
        return "\n".join(self.turn_summaries)

class NullLog:
    def __init__(self): self.events = [] 
    def add_event(self, event: Dict):
        if event.get('type') == 'death': self.events.append(event)
    def add_turn_summary(self, turn: int, summary: str): pass 
    def get_full_log(self) -> str: return ""

class BattleSimulator:
    def __init__(self, rng_seed: Optional[int] = None):
        self.damage_calc = DamageCalculator(rng_seed)
        self.turn_system = TurnSystem(rng_seed)
        self.buff_tracker = BuffTracker()
        self.log = BattleLog()
    
    def simulate_battle(self, initial_state: BattleState, player_script, enemy_script, max_turns=50, special_encounter_id=None, enable_logging=True):
        state = initial_state.copy()
        self.log = BattleLog() if enable_logging else NullLog()
        
        turn = 0
        while not state.is_battle_over() and turn < max_turns:
            turn += 1
            if enable_logging: self.log.add_turn_summary(turn, f"Turn {turn}")
            
            player_action = self._get_action(player_script, state, turn, 'player')
            enemy_action = self._get_action(enemy_script, state, turn, 'enemy')
            
            # VALIDATE DEATH SWAPS
            player_action = self._validate_action(state.player_team, player_action, 'player')
            enemy_action = self._validate_action(state.enemy_team, enemy_action, 'enemy')
            
            state = self.execute_turn(state, player_action, enemy_action, turn, special_encounter_id)
            if state.is_battle_over(): break
        
        winner = state.get_winner() or 'draw'
        return {'winner': winner, 'turns': turn, 'log': self.log, 'final_state': state, 'events': self.log.events}
    
    def _validate_action(self, team, action, actor):
        active = team.get_active_pet()
        if not active or not active.stats.is_alive():
            # FORCE SWAP ON DEATH
            for i, p in enumerate(team.pets):
                if p.stats.is_alive():
                    # Log the forced swap so we know WHY it happened
                    if isinstance(self.log, BattleLog):
                        # self.log.add_event({'type': 'info', 'msg': f"{actor} forced to swap (Active Dead)"})
                        pass
                    return TurnAction(actor=actor, action_type='swap', target_pet_index=i)
            return TurnAction(actor=actor, action_type='pass')
        return action

    def _get_action(self, script, state, turn, actor):
        if callable(script):
            try: return script(state)
            except: return TurnAction(actor=actor, action_type='pass')
        else:
            idx = min(turn - 1, len(script) - 1)
            return script[idx]
    
    def execute_turn(self, state, player_action, enemy_action, turn_number, special_encounter_id=None):
        # DO NOT process_end_of_turn here - buffs must persist through the turn!
        if state.is_battle_over(): return state
        
        player_pet = state.player_team.get_active_pet()
        enemy_pet = state.enemy_team.get_active_pet()
        
        # Validate Cooldowns
        if player_action.action_type == 'ability' and player_action.ability:
             if not player_pet.can_use_ability(player_action.ability): player_action = TurnAction('player', 'pass')
        if enemy_action.action_type == 'ability' and enemy_action.ability:
             if not enemy_pet.can_use_ability(enemy_action.ability): enemy_action = TurnAction('enemy', 'pass')

        action_order = self.turn_system.determine_turn_order(player_pet, player_action, enemy_pet, enemy_action)
        
        for actor, action in action_order:
            attacker = player_pet if actor == 'player' else enemy_pet
            defender = enemy_pet if actor == 'player' else player_pet
            attacker_team = state.player_team if actor == 'player' else state.enemy_team
            
            if not attacker.stats.is_alive() and action.action_type != 'swap': continue
            if not defender.stats.is_alive() and action.action_type == 'ability': continue 

            # print(f"\n[EXEC] {actor} action: {action.action_type} {action.ability.name if action.ability else ''}")
            # if actor == 'player':
            #     print(f"  Player buffs BEFORE action: {[b.name for b in attacker.active_buffs]}")
            # else:
            #     enemy_acting_on = player_pet if actor == 'enemy' else enemy_pet
            #     print(f"  Defender ({enemy_acting_on.name}) buffs BEFORE enemy action: {[b.name for b in enemy_acting_on.active_buffs]}")
            
            self.execute_action(action, attacker, defender, attacker_team, state, special_encounter_id, turn_number)
            
            # if actor == 'player':
            #     print(f"  Player buffs AFTER action: {[b.name for b in attacker.active_buffs]}")
            # else:
            #     print(f"  Defender ({enemy_acting_on.name}) buffs AFTER enemy action: {[b.name for b in enemy_acting_on.active_buffs]}")
            if state.is_battle_over(): break
        
        if player_pet: player_pet.tick_cooldowns()
        if enemy_pet: enemy_pet.tick_cooldowns()
        
        # Process end of turn AFTER all actions complete
        self.process_end_of_turn(state, state.player_team.get_active_pet(), state.enemy_team.get_active_pet(), special_encounter_id)
        
        state.turn_number = turn_number + 1
        return state
    
    def execute_action(self, action, attacker, defender, attacker_team, state, special_encounter_id, turn_number):
        if action.action_type == 'swap':
            if action.target_pet_index is not None:
                attacker_team.active_pet_index = action.target_pet_index
                self.log.add_event({'type': 'swap', 'actor': action.actor, 'turn': turn_number, 'new_index': action.target_pet_index})
        elif action.action_type == 'ability' and action.ability:
            ability = action.ability
            attacker.use_ability(ability)
            
            is_immune = False
            if special_encounter_id == 'rocko_immunity' and SpecialEncounterHandler.apply_rocko_immunity(defender, state.turn_number): is_immune = True
            for buff in defender.active_buffs:
                if buff.type in [BuffType.INVULNERABILITY, BuffType.IMMUNITY] or "Decoy" in buff.name: is_immune = True
            
            if is_immune:
                self.log.add_event({'type': 'immune', 'turn': turn_number, 'actor': action.actor, 'ability': ability.name})
                # Even if immune, self-effects (Explode/Haunt suicide, Lift-Off buff) should trigger.
                # Pass is_hit=False so enemy debuffs aren't applied.
                self.apply_ability_effects(ability, attacker, defender, turn_number, is_hit=False, attacker_team=attacker_team)
                return 

            if ability.is_heal:
                heal = self.damage_calc.calculate_healing(ability, attacker)
                attacker.stats.heal(heal)
                self.log.add_event({'type': 'heal', 'actor': action.actor, 'ability': ability.name, 'amount': heal, 'turn': turn_number})
            else:
                # Life Exchange Special Handling (Bypass damage calc, ignore shields/caps)
                if ability.name == "Life Exchange" or ability.id == 284:
                    SpecialEncounterHandler.apply_life_exchange(attacker, defender)
                    self.log.add_event({'type': 'life_exchange', 'actor': action.actor, 'turn': turn_number})
                    # Apply ability effects (like cooldowns) then return
                    self.apply_ability_effects(ability, attacker, defender, turn_number)
                    return

                # Mind Games Special Handling (Team Damage)
                if ability.name == "Mind Games" or ability.id == 2388:
                    SpecialEncounterHandler.apply_mind_games(state.player_team if action.actor == 'enemy' else state.enemy_team, attacker)
                    self.log.add_event({'type': 'mind_games', 'actor': action.actor, 'turn': turn_number})
                    self.apply_ability_effects(ability, attacker, defender, turn_number)
                    return

                # Bone Prison Special Handling (Stun)
                if ability.name == "Bone Prison" or ability.id == 650:
                    SpecialEncounterHandler.apply_bone_prison(defender)
                    self.log.add_event({'type': 'bone_prison', 'actor': action.actor, 'target': defender.name, 'turn': turn_number})
                    self.apply_ability_effects(ability, attacker, defender, turn_number)
                    return

                damage, details = self.damage_calc.calculate_damage(ability, attacker, defender, state.weather)
                if details['hit']:
                    remaining = self.buff_tracker.consume_shield(defender, damage)
                    defender.stats.take_damage(remaining)
                    
                    # Toxic Skin Reflection (Glitterdust)
                    # Check if defender has Toxic Skin buff (ID 1086/1087 or name "Toxic Skin")
                    has_toxic_skin = False
                    for buff in defender.active_buffs:
                        if buff.name == "Toxic Skin" or buff.source_ability in [1086, 1087]:
                            has_toxic_skin = True
                            break
                    
                    if has_toxic_skin:
                        reflected = SpecialEncounterHandler.apply_toxic_skin(attacker, remaining)
                        if reflected > 0:
                            self.log.add_event({'type': 'damage', 'actor': 'reflection', 'ability': 'Toxic Skin', 'amount': reflected, 'turn': turn_number})

                    self.log.add_event({'type': 'damage', 'actor': action.actor, 'ability': ability.name, 'amount': remaining, 'turn': turn_number})
                    if not defender.stats.is_alive():
                         # Check Undead Racial
                         from simulator.racial_passives import RacialPassives
                         from simulator.battle_state import PetFamily
                         
                         if defender.family == PetFamily.UNDEAD and RacialPassives.apply_undead_passive(defender):
                             defender.stats.current_hp = 1 # Keep alive
                             self.log.add_event({'type': 'racial', 'pet': defender.name, 'racial': 'Undead', 'turn': turn_number})
                         else:
                             self.log.add_event({'type': 'death', 'pet': defender.name, 'turn': turn_number})
                else:
                    self.log.add_event({'type': 'miss', 'actor': action.actor, 'ability': ability.name, 'turn': turn_number})
            
            # Apply ability-specific buffs and effects
            # Pass hit status (default True if no details, e.g. Life Exchange)
            is_hit = details.get('hit', True) if 'details' in locals() else True
            self.apply_ability_effects(ability, attacker, defender, turn_number, is_hit, attacker_team)

    def apply_ability_effects(self, ability, attacker, defender, turn_number, is_hit=True, attacker_team=None):
        """Apply status effects, buffs, and debuffs based on ability"""
        from simulator.battle_state import Buff
        
        # Explode (282) - Kills user immediately (even on miss)
        if ability.name == "Explode" or ability.id == 282 or ability.effect_type == 'explode':
            attacker.stats.current_hp = 0
            self.log.add_event({'type': 'death', 'pet': attacker.name, 'reason': 'Explode', 'turn': turn_number})
            
        # Haunt (652) - Kills user immediately (even on miss)
        elif ability.name == "Haunt" or ability.id == 652 or ability.effect_type == 'haunt':
            # Capture HP for resurrection (before killing)
            # Note: Haunt restores the SAME health the user had.
            snapshot_hp = attacker.stats.current_hp
            source_index = attacker_team.pets.index(attacker) if attacker_team else None
            
            attacker.stats.current_hp = 0
            self.log.add_event({'type': 'death', 'pet': attacker.name, 'reason': 'Haunt', 'turn': turn_number})
            
            # If hit, apply Haunt buff to defender
            if is_hit:
                buff = Buff(
                    type=BuffType.DOT, # Haunt acts like a DoT/Debuff
                    name="Haunt",
                    duration=5, # usually 4-5 rounds? Let's assume 5 based on standard
                    magnitude=0, # Damage handled by DoT logic if any, or special effect
                    source_ability=ability.name,
                    stat_affected='haunt', # Special marker
                    source_pet_index=source_index,
                    snapshot_hp=snapshot_hp
                )
                defender.active_buffs.append(buff)
                self.log.add_event({'type': 'buff_applied', 'target': defender.name, 'buff': 'Haunt', 'turn': turn_number})

        # Dodge (312) - Duration 2 because WoW "lasts 1 round" = current round + next
        if ability.name == "Dodge" or ability.id == 312:
            buff = Buff(
                type=BuffType.INVULNERABILITY,
                name="Dodge",
                duration=2,  # 2 rounds to survive process_end_of_turn and block next attack
                magnitude=0,
                source_ability=ability.name,
                stat_affected='none'
            )
            self.buff_tracker.add_buff(attacker, buff)
            self.log.add_event({'type': 'buff_applied', 'target': attacker.name, 'buff': 'Dodge', 'turn': turn_number})

        # Burrow (159) - Underground lasts 2 rounds, attack triggers next turn
        elif ability.name == "Burrow" or ability.id == 159:
            buff_underground = Buff(
                type=BuffType.INVULNERABILITY,
                name="Underground",
                duration=2,  # 2 rounds to survive end-of-turn and block next attack
                magnitude=0,
                source_ability=ability.name,
                stat_affected='none'
            )
            self.buff_tracker.add_buff(attacker, buff_underground)
            
            buff_attack = Buff(
                type=BuffType.DELAYED_EFFECT,
                name="Burrow Attack",
                duration=2,  # Triggers at start of turn 2 (after 1 decrement)
                magnitude=ability.power if ability.power > 0 else 20,
                source_ability=ability.name,
                stat_affected='none'
            )
            self.buff_tracker.add_buff(attacker, buff_attack)
            self.log.add_event({'type': 'buff_applied', 'target': attacker.name, 'buff': 'Underground', 'turn': turn_number})

        # Lift-Off (170) - Flying lasts 2 rounds, attack triggers next turn
        elif ability.name == "Lift-Off" or ability.id == 170:
            buff_flying = Buff(
                type=BuffType.INVULNERABILITY,
                name="Flying",
                duration=2,
                magnitude=0,
                source_ability=ability.name,
                stat_affected='none'
            )
            self.buff_tracker.add_buff(attacker, buff_flying)
            
            buff_attack = Buff(
                type=BuffType.DELAYED_EFFECT,
                name="Lift-Off Attack",
                duration=2,
                magnitude=ability.power if ability.power > 0 else 30, # Lift-Off usually stronger?
                source_ability=ability.name,
                stat_affected='none'
            )
            self.buff_tracker.add_buff(attacker, buff_attack)
            self.log.add_event({'type': 'buff_applied', 'target': attacker.name, 'buff': 'Flying', 'turn': turn_number})

        # Black Claw (919)
        elif ability.name == "Black Claw" or ability.id == 919:
            if is_hit:
                buff = Buff(
                    type=BuffType.STAT_MOD,
                    name="Black Claw",
                    duration=3,
                    magnitude=144,
                    source_ability=ability.name,
                    stat_affected='damage_taken_flat'
                )
                self.buff_tracker.add_buff(defender, buff)
                self.log.add_event({'type': 'buff_applied', 'target': defender.name, 'buff': 'Black Claw', 'turn': turn_number})

        # Hunting Party (921)
        elif ability.name == "Hunting Party" or ability.id == 921:
            if is_hit:
                buff = Buff(
                    type=BuffType.STAT_MOD,
                    name="Shattered Defenses",
                    duration=2,
                    magnitude=2.0,
                    source_ability=ability.name,
                    stat_affected='damage_taken_mult'
                )
                self.buff_tracker.add_buff(defender, buff)
            self.log.add_event({'type': 'buff_applied', 'target': defender.name, 'buff': 'Shattered Defenses', 'turn': turn_number})

    def process_end_of_turn(self, state, p1, p2, special_encounter_id=None):
        """
        Process end-of-turn effects in STRICT order:
        1. Weather damage
        2. DoT damage
        3. Death checks (if DoT kills, stop here)
        4. HoT healing (only if alive)
        5. Buff duration decrement
        """
        # 0. Special Encounter Mechanics (Start of End Phase)
        if special_encounter_id == 'gore_stacks':
            # Apply Gore Stacks to player's pet (p1 is usually player if called with player_pet first)
            # We assume p1 is player pet based on call in execute_turn
            if p1 and p1.stats.is_alive():
                SpecialEncounterHandler.apply_gorespine_gore(p1, state.turn_number)

        for p in [p1, p2]:
            if not p:
                continue
                
            # 1. Weather damage (if any active weather)
            if state.weather and p.stats.is_alive():
                self.buff_tracker.process_weather_damage(state.weather, p)
                
            # 2. DoT damage
            if p.stats.is_alive():
                self.buff_tracker.process_dots(p)
                
            # 3. Death check - if DoT killed pet, skip HoT
            if not p.stats.is_alive():
                # Check Undead Racial (for DoT deaths)
                from simulator.racial_passives import RacialPassives
                from simulator.battle_state import PetFamily
                
                if p.family == PetFamily.UNDEAD and RacialPassives.apply_undead_passive(p):
                    p.stats.current_hp = 1 # Keep alive
                    self.log.add_event({'type': 'racial', 'pet': p.name, 'racial': 'Undead', 'turn': state.turn_number})
                else:
                    self.log.add_event({'type': 'death', 'pet': p.name, 'reason': 'DoT'})
                    # Do not process HoT for dead pets
                    events = self.buff_tracker.decrement_durations(p)
                    for event in events:
                        if event['type'] == 'buff_expired' and event['buff'].stat_affected == 'haunt':
                            self.handle_haunt_resurrection(state, p, event['buff'])
                    continue
                
            # 4. HoT healing (only if still alive after DoT)
            if p.stats.is_alive():
                self.buff_tracker.process_hots(p)
                
            # 5. Decrement buff durations
            events = self.buff_tracker.decrement_durations(p)
            for event in events:
                if event['type'] == 'buff_expired' and event['buff'].stat_affected == 'haunt':
                    self.handle_haunt_resurrection(state, p, event['buff'])
            
            # 6. Handle Undead Racial Expiration
            if hasattr(p, 'has_undead_revive') and p.has_undead_revive:
                p.revive_turns_remaining -= 1
                if p.revive_turns_remaining < 0:
                    p.has_undead_revive = False
                    p.stats.current_hp = 0
                    self.log.add_event({'type': 'death', 'pet': p.name, 'reason': 'Undead Racial Expired'})

    def handle_haunt_resurrection(self, state, host_pet, buff):
        """Handle resurrection when Haunt buff expires/removed"""
        # Determine source team (opposite of host)
        if host_pet in state.player_team.pets:
            source_team = state.enemy_team
        else:
            source_team = state.player_team
            
        if buff.source_pet_index is not None and 0 <= buff.source_pet_index < len(source_team.pets):
            source_pet = source_team.pets[buff.source_pet_index]
            
            # Revive if dead
            if not source_pet.stats.is_alive():
                hp_to_restore = buff.snapshot_hp if buff.snapshot_hp else 1
                source_pet.stats.current_hp = hp_to_restore
                self.log.add_event({'type': 'resurrect', 'pet': source_pet.name, 'hp': hp_to_restore, 'reason': 'Haunt'})