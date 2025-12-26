import json
import os

class LogicProcessor:
    def __init__(self, spec_id):
        self.spec_id = spec_id
        self.spec_data = self._load_spec(spec_id)
        self.matchups = self._load_matchups(spec_id)
        self.matchup_data = {}
        self.last_known_state = {}
        self.last_pulse_time = 0
        self.manual_override_until = 0
        self.lethal_spells = set() 
        self.pve_mechanics = {} # Load from pve_mechanics.json # To be loaded from json
        self.racials = self._load_json("brain/data/config/racials.json")

    def _load_spec(self, spec_id):
        path = f"brain/data/specs/{spec_id}_arms.json" 
        if spec_id == 70: path = f"brain/data/specs/{spec_id}_ret.json" # Temp map
        
        data = self._load_json(path)
        
        # DYNAMIC INJECTION: Racials
        # In real engine, we detect player_race_id from state
        # For template hardcoding, we assume user config
        race_id = self.last_known_state.get('player_race_id', "2") # Default Orc
        if str(race_id) in self.racials:
            racial = self.racials[str(race_id)]
            target_slot = racial['slot']
            # Append Racial to the Burst/Utility slot conditions
            # OR simple override? Integration is better.
            # "Blood Fury" aligns with "Avatar" (Slot 07).
            # We add it to the 'macro_list' of that slot if supported, 
            # or we ensure the keybind fires it via in-game macro.
            # For "War Stomp" (Slot 12), it replaces "Intimidating Shout" if shout is on CD?
            # Or serves as a fallback.
            pass

        return data

    def _load_json(self, path):
         # Helper to load json safely
         import json
         try:
             with open(path, 'r') as f: return json.load(f)
         except: return {}

    def _load_matchups(self, spec_id):
        path = f"brain/matchups/{spec_id}_vs_all.json"
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}

    def get_pulse_action(self, game_state):
        """
        The 4-Stage Priority Vertical Scan:
        1. Matchup Reaction (High Alert)
        2. Life Safety (Defensives)
        3. Tactical Interruption (Kicks/CC)
        4. Optimal Rotation (SequenceForge Logic)
        """
        
        # STAGE 1: Matchup Reaction
        # Checks if an enemy SpecID is doing something lethal
        enemy_spec = game_state.get('enemy_spec')
        # Simplified aura check (assuming enemy_aura_id available in game_state)
        
        # STAGE 1.5: Proc Override (High Priority Offense)
        # Checks Chameleon Pixel 5/12 for Specific Aura IDs
        active_proc_id = game_state.get('active_proc_id')
        proc_config = self.spec_data.get('proc_priority', {}).get(str(active_proc_id))
        
        if proc_config:
            print(f"PROC OVERRIDE: {proc_config['name']}")
            return proc_config['slot']

        # STAGE 2: Life Safety (Slots 15-18)
        # Panic threshold check
        panic_val = self.spec_data.get('logic_overrides', {}).get('panic_threshold', 30)
        if game_state['health'] < panic_val:
            return "SLOT_15"

        # STAGE 3: Tactical Interruption (Slots 11-14)
        if game_state.get('enemy_casting') and game_state.get('cast_percent', 0) > 0.85:
            return "SLOT_11"

        # STAGE 4: Optimal Rotation (Slots 01-10)
        return self._solve_rotation(game_state)

    def _solve_rotation(self, state):
        # Sorts universal slots by priority and validates conditions
        slots = self.spec_data.get('universal_slots', {})
        # Sort by priority descending
        sorted_slots = sorted(slots.items(), key=lambda x: x[1].get('priority', 0), reverse=True)
        
        current_resource = state.get('resource', 0)

        for slot_id, config in sorted_slots:
            # Resource Gate validation
            cost = config.get('min_resource', 0)
            if current_resource < cost:
                continue

    def execute_single_pulse(self):
        """
        The Main Event Loop Triggered by the Keypad.
        """
        # 0. PULSE GUARD (Spam Protection)
        if (time.time() - self.last_pulse_time) < 0.150:
            return 
        self.last_pulse_time = time.time()
        
        state = self._capture_state()
        
        # 0.1 DETERMINISTIC INTEGRITY (GCD/Clip Guard)
        gcd_rem = state.get('gcd_remaining', 0)
        if gcd_rem > 0 and gcd_rem <= 0.1:
            time.sleep(gcd_rem + 0.01)

        # 0.1 SENTINEL CHECK (Fail-Safe)
        if not self.sentinel.check_safety(state):
            return

        # 0.2 MECHANIC GUARD (PvE Safety)
        # Check for Stop Attack Debuffs (Reflects, Shields, Phase Transitions)
        if self._check_mechanic_guard(state):
            print("MECHANIC GUARD: HOLDING FIRE")
            return

        # 1. INTELLIGENT ANCHOR (Auto-Focus) - Only in PvP Mode
        mode = self._determine_mode(state)
        if mode == "PVP":
            self._manage_focus(state)

        # 2. PRIORITY OVERRIDES (Focus Kick & Matchups)
        # Check for Lethal Focus Cast -> Override to Slot 26 (Only meaningful if Focus exists)
        if self._check_focus_lethal(state):
             # Force Focus Pummel
             self.bridge.send_input(self.spec_data['universal_slots']['slot_26']['key'])
             return

        # 3. MATCHUP REACTION (Vertical Scan Stage 1)
        # ... (Rest of logic)
    
    def _determine_mode(self, state):
        """
        Detects environment: PVP (Arena/BG), DUNGEON, RAID, or WORLD.
        """
        # In real implementation: checks 'zone_type' or 'instance_type' from state
        # state['instance_type'] values: 'arena', 'pvp', 'party', 'raid', 'none'
        inst_type = state.get('instance_type', 'none')
        if inst_type in ['arena', 'pvp']: return "PVP"
        if inst_type == 'party': return "DUNGEON"
        if inst_type == 'raid': return "RAID"
        return "WORLD"

    def _check_mechanic_guard(self, state):
        """
        Returns True if a 'Stop Attack' mechanic is active.
        """
        debuffs = state.get('active_debuff_ids', [])
        target_buffs = state.get('target_buff_ids', [])
        
        # Check Configured Stop IDs (Reflects, Immunities that shouldn't be hit)
        for d in debuffs:
             if d in self.pve_mechanics['stop_attack_ids']: return True
        
        for b in target_buffs:
             if b in self.pve_mechanics['stop_attack_ids']: return True # Target Reflecting?
             
        return False
        # ... (Rest of logic)
    
    def _manage_focus(self, state):
        """
        Handles Auto-Setting Focus on Healers/Casters.
        Respects Manual Override (30s suspension).
        """
        # Check Manual Override
        if time.time() < self.manual_override_until:
            return

        # Detect User Manual Change (simplistic check: if focus changed and we didn't do it)
        # In real engine, we'd track last_set_focus_guid. 
        # For now, we assume if Focus exists and is NOT a Priority Target, user set it manually?
        # Or simply: If Focus exists, we leave it alone unless it's dead.
        
        current_focus = state.get('focus_guid')
        if current_focus:
            return # Respect existing focus
            
        # If No Focus, Scan for Priority Targets
        # (This is usually done via Arena Frames 1-3)
        priority_unit = self._find_priority_enemy(state)
        if priority_unit:
            # Set Focus Command (Macro or Keybind)
            print(f"AUTO-FOCUS: Setting Anchor on {priority_unit}")
            # We need a slot for "Set Focus" or use a dedicated macro command
            # self.bridge.send_input("Shift+F10")  # hypothetical 'Set Focus' bind
            pass

    def _check_focus_lethal(self, state):
        """
        Returns True if Focus is casting a spell in 'lethal_spells.json'.
        """
        if not state.get('focus_casting'): return False
        
        spell_id = state.get('focus_cast_id')
        # Check against loaded Lethal List
        if spell_id in self.lethal_spells:
            # Check Interruptible
            return state.get('focus_interruptible')
            
        return False

    def _find_priority_enemy(self, state):
        """
        Scans available Unit Frames for Healers/Casters.
        Returns GUID or UnitID (e.g. 'arena1').
        """
        # In real implementation: checks state['arena_specs'] against HighValue list
        return None

    def _has_external_defensive(self, state):
        """
        Checks if player has a Healer/Support defensive active.
        IDs: 33206 (Pain Supp), 47788 (Guardian Spirit), 6940 (Sacrifice), 116849 (Life Cocoon)
        """
        external_ids = {33206, 47788, 6940, 116849, 1022} # 1022 BoP
        active_buffs = state.get('active_buff_ids', [])
        for buff in active_buffs:
            if buff in external_ids:
                return True
        return False


        # ... (Rest of logic)
    
    # ...

    def _solve_rotation(self, state):
        # ...
        
        for slot_id, config in sorted_slots:
            # ...
            if self._check_conditions(config.get('conditions', []), state):
                # AIM ASSIST LOGIC
                if config.get('requires_aim'):
                     feet_coords = self.vision.get_feet_coordinates(state.get('target_rect'), state.get('screen_height', 1080))
                     if feet_coords:
                         center_x = state.get('screen_width', 1920) // 2
                         center_y = state.get('screen_height', 1080) // 2
                         
                         # VELOCITY PREDICTION (Slot 17 Heroic Leap)
                         if config.get('action') == "Heroic Leap" and state.get('target_moving'):
                             # Predict pos in 150ms
                             v_x = state.get('target_velocity_x', 0)
                             aim_x = feet_coords[0] + (v_x * 0.15)
                             dx = int(aim_x) - center_x
                         else:
                             dx = feet_coords[0] - center_x
                             
                         dy = feet_coords[1] - center_y
                         
                         # Send Aim Command (0xFD) - Zero Sum Flick
                         self.bridge.send_flick(dx, dy)
                         
                return slot_id
        return "SLOT_01" # Default filler

    def _check_conditions(self, conditions, state):
        """
        Validates the 'Truth' of the current frame.
        Handles Procs, Range, and Resource gating.
        """
        for cond in conditions:
            # 1. RANGE CHECK (Pixel 3)
            if cond == "in_melee" and not state.get('in_melee_range'):
                return False
                
            # 2. OLD RESOURCE CHECK (Pixel 4) - Deprecated by min_resource, keeping for overrides
            if cond == "rage_gt_60" and state.get('resource', 0) < 60:
                return False
                
            # 3. PROC CHECK (Pixel 5/12)
            if cond == "proc_tactician" and not state.get('has_tactician_proc'):
                return False
                
            # 4. HP Checks
            if cond == "target_hp_lt_35" and state.get('target_health', 100) > 35:
                return False
                
            if cond == "ms_off_cd" and not state.get('ms_ready'):
                 return False

            # 5. TARGET SAFETY (Pixel 6 Flags)
            if cond == "target_valid":
                # Must be Enemy AND Alive
                if not state.get('target_is_enemy') or not state.get('target_is_alive'):
                    return False
            
            # 7. DR CHECK (Pixel 7 Flags)
            if "target_not_dr_stun" in cond and state.get('target_dr_stun_state') > 0.5:
                 return False # Stun DR is active/full
                 
        return True

    def _execute_ghost_sync(self, primary_slot):
        """
        Handles Macro-Simulation.
        If Slot 07 fires, check if Slot 08 should follow instantly.
        """
        if primary_slot == "slot_07":
            # Check slot 08 conditions manually
            if self._check_conditions(self.spec_data['universal_slots']['slot_08']['conditions'], self.last_known_state):
                print("GHOST SYNC: Firing Slot 08 (Avatar)")
                self.bridge.send_input(self.spec_data['universal_slots']['slot_08']['key'])

    def _apply_rage_economy(self, slot_config, current_rage, threat_level):
        """
        Enforces a 'Safety Buffer' if a lethal threat is active.
        """
        cost = slot_config.get('min_resource', 0)
        
        # If High Threat (Matchup Detected) -> Hold 30 Rage backup for Ignore Pain
        if threat_level == "HIGH" and slot_config.get('action') in ["Slam", "Whirlwind"]:
            if current_rage < (cost + 30):
                return False # Starve this spender to save for defense
        
        return True

    def get_gcd_status(self, spec_type='Melee'):
        """
        Calculates the 'Golden Window' for queuing.
        """
        haste_pct = self.last_known_state.get('haste_percent', 0)
        haste_multiplier = haste_pct / 100.0
        
        base_gcd = 1.5 if spec_type == 'Caster' else (1.0 if spec_type == 'Energy' else 1.5) # Arms is 1.5 base
        
        # Calculate dynamic floor
        current_gcd_limit = max(0.75, base_gcd / (1 + haste_multiplier))
        
        time_since = self.last_known_state.get('time_since_last_cast', 999)
        
        # Golden Window: Last 100ms of GCD
        return time_since >= (current_gcd_limit - 0.1)

    def _check_conditions(self, conditions, state):
        # ... (Existing checks)
        
        for cond in conditions:
             # FOCUS LOGIC
             if cond == "focus_valid":
                 if not (state.get('focus_exists') and state.get('focus_is_enemy')): return False
                 
             if cond == "focus_casting":
                 if not state.get('focus_casting'): return False
                 
             if cond == "focus_interruptible":
                 if not (state.get('focus_casting') and state.get('focus_interruptible')): return False

        # 4. SURVIVAL & DEFENSE LOGIC
        if "survival_critical" in conditions:
            # Check HP < 35% OR Matchup-defined Lethal Incoming
            if state.get('health_percent', 100) > 35: return False
            
        if "no_external_defensive" in conditions:
            # Check for Pain Supp (33206), Sac (6940), Cocoon (116849), etc.
            # Using a loaded set of External IDs similar to lethal_spells
            if self._has_external_defensive(state): return False
            
        if "no_forbearance" in conditions:
            # Aura 25771
            if 25771 in state.get('active_debuff_ids', []): return False

        # 5. BURST ALIGNMENT
        if "burst_aligned" in conditions:
            # Factor A: Rage (>60) or Holy Power (>=3) or Energy/CP
            # Generic resource check including Secondary
            current_res = state.get('current_resource', 0)
            current_sec = state.get('current_secondary_resource', 0)
            
            min_res = 60 
            if self.spec_id == 70: min_res = 3 # Ret
            if self.spec_id == 261: min_res = 80 # Rogue Energy
            
            # Secondary check for Rogue (CP >= 5 for efficient burst start)
            if self.spec_id == 261 and current_sec < 5: return False
            
            if self.spec_id != 70 and current_res < min_res: return False # Ret uses HoPo as primary logic in json
            pass

        # ROGUE SPECIFIC STATES
        if "is_stealthed_or_dance" in conditions:
            # Check Aura: Stealth (1784), Shadow Dance (185313), Subterfuge (115192)
            stealth_ids = {1784, 185313, 115192, 11327} # 11327 Vanish buff
            has_stealth = any(b in stealth_ids for b in state.get('active_buff_ids', []))
            if not has_stealth: return False

        if "not_stealthed_or_dance" in conditions:
            stealth_ids = {1784, 185313, 115192, 11327}
            has_stealth = any(b in stealth_ids for b in state.get('active_buff_ids', []))
            if has_stealth: return False
            
        if "target_debuff_absent_rupture" in conditions:
            # ID 1943
            if 1943 in state.get('target_debuff_ids', []): return False

        # 6. SMART EXECUTE (TTD)


        # 6. SMART EXECUTE (TTD)
        if "ttd_critical" in conditions:
            # "Execute Phase" override if Boss is dying FAST (< 10s TTD)
            # even if HP > 35% (e.g. 40% but melting)
            ttd = self._calculate_ttd(state)
            if ttd > 0 and ttd < 10: return True
            return False

        if "interruptible_late_stage" in conditions:
            # 5. DETERMINISTIC INTEGRITY: The "Interrupt Guard"
            # Logic: Kick ONLY between 88% and 94% cast progress
            # Ensures lag-compensation (server thinks you kicked early-ish, but prevents baits)
            cast_progress = state.get('target_cast_progress', 0.0) # 0.0 to 100.0
            if cast_progress < 88 or cast_progress > 94: return False
            if not state.get('target_casting') or not state.get('target_interruptible'): return False

        if "proc_brain_freeze" in conditions:
            # ID 190446
            if 190446 not in state.get('active_buff_ids', []): return False

        if "trigger_shatter_or_fingers" in conditions:
            # Check Fingers of Frost (44544) OR Winter's Chill (228358) on target
            has_fingers = 44544 in state.get('active_buff_ids', [])
            has_shatter_debuff = 228358 in state.get('target_debuff_ids', [])
            has_freeze_root = 122 in state.get('target_debuff_ids', []) # Frost Nova
            if not (has_fingers or has_shatter_debuff or has_freeze_root): return False

        if "not_moving" in conditions:
            # Check player velocity
            if state.get('is_moving', False): 
                # Exception: Ice Floes (108839) allows casting while moving
                if 108839 in state.get('active_buff_ids', []): return True
                return False

        if "icicles_gte_5" in conditions:
            # Secondary check for Mage
            if state.get('current_secondary_resource', 0) < 5: return False

        # HEALING / GRID LOGIC (Druid/Paladin)
        if "lowest_friendly_hp" in conditions:
            # Determines if we should target a friendly unit
            # Uses Vision data (party_frames)
            target = self._get_healing_target(state)
            if not target: return False
            # Ideally we would setup the "Aim" here for proper 0xFD coords
            # For now, simplistic boolean check
            return True

        if "multidot_needed" in conditions:
            # MULTI-DOT ENGINE: Return True if current target has DoTs and we should tab
            if self._should_tab_target(state):
                return True  # DoTs are up on current target, time to spread
            return False  # Need to apply DoTs to current target first

        # SHADOW PRIEST LOGIC
        if "refresh_dot_swp" in conditions:
            # ID 589
            return self._needs_dot_refresh(state, 589, 16.0)
            
        if "refresh_dot_vt" in conditions:
            # ID 34914
            return self._needs_dot_refresh(state, 34914, 21.0)
            
        if "combo_strikes_valid" in conditions:
            # Monk Mastery Logic
            # ideally check vs self.last_cast_id
            return True 

        # SHAMAN LOGIC
        if "grounding_needed" in conditions:
            if state.get('target_casting') and state.get('target_targeting_player'):
                return True
            return False

        # HUNTER LOGIC
        if "frenzy_maintenance_needed_or_cap" in conditions:
            # Check Frenzy Stacks (Pet Buff)
            # ID 272790 usually? Or internal tracker
            # Logic: If stacks < 3 OR duration < 1.5s (Pandemic for Barbed Shot refresh)
            # OR charges == 2 (Don't cap)
            if state.get('current_charges_slot_02', 0) >= 1.8: return True
            
            # Need strict duration tracking of Frenzy on Pet
            frenzy_rem = state.get('pet_buff_rem', {}).get(272790, 0)
            if frenzy_rem > 0 and frenzy_rem < 2.0: return True
            if state.get('pet_buff_stacks', {}).get(272790, 0) < 3: 
                # If we aren't at 3 stacks, we want to build them, but prioritizing KC usually unless charges high
                # Simplified: Build to 3 ASAP
                return True
            return False

        if "frenzy_maintenance_needed_or_cap" in conditions:
            # Check Frenzy Stacks (Pet Buff)
            if state.get('current_charges_slot_02', 0) >= 1.8: return True
            frenzy_rem = state.get('pet_buff_rem', {}).get(272790, 0)
            if frenzy_rem > 0 and frenzy_rem < 2.0: return True
            if state.get('pet_buff_stacks', {}).get(272790, 0) < 3: 
                return True
            return False

        if "focus_safe_for_next_kc" in conditions:
            kc_cd = state.get('cooldown_rem_slot_01', 99)
            if kc_cd < 1.5:
                # 30 focus for KC
                if state.get('resource', 0) < 30: return False
            return True

        # UNHOLY DK LOGIC
        if "disease_missing_virulent" in conditions:
            # ID 55078
            rem = state.get('target_debuff_rem', {}).get(55078, 0)
            if rem < 1.5: return True
            return False

        # DESTRUCTION LOGIC
        if "refresh_dot_immolate" in conditions:
            # ID 157736
            return self._needs_dot_refresh(state, 157736, 18.0)

        if "not_moving_or_burn" in conditions:
            if not state.get('is_moving'): return True
            # Check Burning Rush toggled logic? No, Burning doesn't allow cast while moving
            # Destro cannot cast while moving unless specific procs (rare) 
            # or KJC talent (if active). Assuming default: No cast.
            return False
            
        if "backdraft_needed" in conditions:
            # Pulse Conflagrate if we are out of Backdraft stacks and not capped on charges
            # Backdraft ID: 117828
            stacks = state.get('active_buff_stacks', {}).get(117828, 0)
            if stacks == 0: return True
            return False
            
        if "backdraft_active" in conditions:
            # Optimize Chaos Bolt cast time
            if 117828 in state.get('active_buff_ids', []): return True
            # If we don't have backdraft, maybe we still cast if shards are high?
            # Handled by "resource_gte_45" usually
            return False
            
        if "resource_gte_45_or_infernal" in conditions:
            # Infernal active means RAPID generation. Lower threshold to 3.5 or 3.0
            # Infernal ID: 266091 (Summon Infernal) - wait, infernal is a guardian
            # Check for "Lord of Flames" or similar, or just trust shard count velocity
            # Simple check: Shards
            shards = state.get('current_resource', 0) # 10 fragments = 1 shard
            # Warlock resources are typically 0-50 (fragments) or 0-5.
            # Assuming 0-50 scale from Vision:
            if shards >= 45: return True
            
            # Infernal check (Guardian presence not usually in active_buff_ids, but maybe a buff on player?)
            # Or use Cooldown status: if Slot 07 is Active (duration)
            # Placeholder:
            if shards >= 30 and "infernal_mode" in state.get('active_modes', []): return True
            return False
            
        if "two_target_cleave" in conditions:
            # Havoc Logic
            if state.get('nearby_enemies_count', 1) >= 2: return True
            return False

        # COMMON / WARLOCK SOULBURN GATE
        if "soulburn_optimization" in conditions:
            # Check if Soulburn (ID 385855) is active
            # If active, return TRUE (allow the spell to cast)
            # If NOT active, this condition likely implies we should pulse Soulburn first
            # But here we are checking if we CAN cast the main spell.
            # Implementation: If urgency is high, we might skip soulburn?
            # Or: Return False if missing soulburn, and let the Engine pulse Slot 20 via a separate mechanism?
            # SkillWeaver Architecture: 'conditions' gate the button.
            # If specific logic requires Soulburn, we should have a 'prepare_soulburn' slot 
            # or treating this as 'modifier_active'.
            # For now, simplistic check:
            if 385855 in state.get('active_buff_ids', []): return True
            return False

        # ENHANCEMENT SHAMAN LOGIC
        if "maelstrom_gte_5_instant" in conditions:
            # Maelstrom Weapon ID: 344179
            stacks = state.get('active_buff_stacks', {}).get(344179, 0)
            if stacks >= 5: return True
            return False

        if "maelstrom_overflow_priority" in conditions:
            # Pulse Spender if >= 8 stacks to avoid capping
            stacks = state.get('active_buff_stacks', {}).get(344179, 0)
            if stacks >= 8: return True
            return False
            
        if "cooldown_ready_or_reset" in conditions:
            # Stormstrike reset check (Stormbringer proc - ID 201846)
            if 201846 in state.get('active_buff_ids', []): return True
            if state.get('cooldown_rem_slot_01', 99) <= 0.1: return True
            return False
            
        if "feral_lunge_safe" in conditions:
            # Check path for hazards/unpulled mobs
            if state.get('path_danger_rating', 0) > 20: return False
            return True

        if "cc_window_active" in conditions:
            # Check if target is stunned/incapacitated
             if state.get('target_is_cc', False): return True
             return False

        # FURY WARRIOR LOGIC
        if "enrage_active" in conditions:
            # Enrage Buff ID: 184362
            if 184362 in state.get('active_buff_ids', []): return True
            return False
            
        if "enrage_down_or_slaughterhouse" in conditions:
            # If NOT enraged, true
            # Or if Slaughterhouse (PvP) stacks need refreshing
            if 184362 not in state.get('active_buff_ids', []): return True
            
            # Slaughterhouse: ID 202472 (on target usually? Or buff on self? It's a debuff on target for MS effect)
            # Assuming we want to maintain stacks
            stacks = state.get('target_debuff_stacks', {}).get(288330, 0) # Slaughterhouse debuff
            # If stacks > 0 and rem < 2s, refresh
            rem = state.get('target_debuff_rem', {}).get(288330, 0)
            if stacks > 0 and rem < 2.0: return True
            return False

        if "rage_gte_80_or_enrage_soon_expire" in conditions:
            # Cast Rampage if Rage > 80 OR Enrage is about to fall off
            if state.get('resource', 0) >= 80: return True
            
            rem = state.get('active_buff_rem', {}).get(184362, 0) # Enrage rem
            if rem > 0 and rem < 1.0 and state.get('resource', 0) >= 80: # Wait, Rampage costs 80.
                # Logic: If we have 80 rage, we usually cast it.
                # But if we are enraged, we might delay until end?
                # User says: "delay Rampage until the last 0.2s of the buff"
                # So if Enraged: Return False unless rem < 0.5?
                # But we also don't want to overcap rage.
                if state.get('resource', 0) > 90: return True # Panic dump
                if rem > 1.0: return False # Hold if enraged and plenty time
                return True # Cast if expiring
            
            # If not enraged, cast to get enraged (requires 80 rage)
            if rem == 0 and state.get('resource', 0) >= 80: return True
            return False

        if "buff_missing_meat_cleaver" in conditions:
            # Meat Cleaver (Whirlwind) ID: 85739 or similar (tracking 2 stacks usually)
            # If 0 stacks, Pulse Whirlwind (Slot 05)
            stacks = state.get('active_buff_stacks', {}).get(85739, 0)
            if stacks == 0: return True
            return False

        if "trigger_disarm" in conditions:
            # Check 39x39 logic or burst detection
             if state.get('enemy_bursting_physical', False): return True
             return False

        if "wound_on_target" in conditions:
            # Refuse Scourge Strike unless 1+ wound
            # Needs Vision stack tracking for 194310
            stacks = state.get('target_debuff_stacks', {}).get(194310, 0)
            if stacks >= 1: return True
            return False
            
        if "wounds_lt_4" in conditions:
            # Festering Strike prevention if we are capped (6 max, usually don't cast > 4)
            stacks = state.get('target_debuff_stacks', {}).get(194310, 0)
            if stacks < 4: return True
            return False
            
        if "wounds_gte_4" in conditions:
            # Apocalypse Requirement
            stacks = state.get('target_debuff_stacks', {}).get(194310, 0)
            if stacks >= 4: return True
            return False

        if "runic_power_high_or_proc" in conditions:
            # Death Coil Logic
            # Proc: Sudden Doom (81340)
            if 81340 in state.get('active_buff_ids', []): return True
            if state.get('resource', 0) > 80: return True # Dump to avoid cap
            return False

        if "safe_landing_zone" in conditions:
            # Disengage Safety
            # In Midnight Engine, this would check 'rear_zone_danger' from Vision
            # Placeholder:
            if state.get('rear_zone_danger', False): return False
            return True
            
        if "unsafe_landing_zone" in conditions:
            if state.get('rear_zone_danger', False): return True
            return False

        if "tremor_needed" in conditions:
            # Check "Fear", "Charm", "Sleep" state
            # Player debuff check
            # IDs: 8122 (Psychic Scream), 5782 (Fear), etc.
            # Tremor works while feared? Yes.
            fear_ids = {8122, 5782, 5484, 5246} 
            active_debuffs = state.get('active_debuff_ids', [])
            if any(d in fear_ids for d in active_debuffs):
                return True
            return False

        if "refresh_dot_flameshock" in conditions:
            # ID 188389
            return self._needs_dot_refresh(state, 188389, 24.0)

        # FERAL DRUID LOGIC
        if "refresh_bleed_rake_snapshot" in conditions:
            # Rake ID 1822
            # Check for Tiger's Fury (5217) or Stealth/Shadowmeld (58984/102543)
            # If TF is UP and Rake was applied WITHOUT TF -> Refresh
            tf_active = 5217 in state.get('active_buff_ids', [])
            stealth_active = any(b in state.get('active_buff_ids', []) for b in [5215, 102543]) # Prowl, Meld
            
            current_rake_strong = state.get('target_debuff_snapshots', {}).get(1822, 1.0) > 1.0 # Placeholder for tracked strength
            
            # Simple Logic: If TF active and Dot has < 30% or was applied weak -> Refresh
            if tf_active or stealth_active:
                 return True # Always optimize snapshot
            
            return self._needs_dot_refresh(state, 1822, 15.0)

        if "refresh_bleed_rip_snapshot" in conditions:
            # Rip ID 1079
            tf_active = 5217 in state.get('active_buff_ids', [])
            if tf_active:
                return True
            return self._needs_dot_refresh(state, 1079, 24.0)
            
        if "pool_energy_50_or_apex" in conditions:
            # Apex Predator (Free Bite) ID: 135700 ? (Check specific ID)
            if 135700 in state.get('active_buff_ids', []): return True # Proc -> Cast
            # Else Pool to 50
            if state.get('resource', 0) >= 50: return True
            return False
            
        if "aoe_needed_or_bloodtalons_gen" in conditions:
            # Thrash/Swipe
            # If BT (Bloodtalons) needs a generator, cast it once
            # BT Logic: Cast Rake, Shred, Thrash to proc.
            if 145152 in state.get('active_buff_ids', []): return False # BT already active
            # Check internal tracker for 'spells_cast_last_4s'?
            # Simplifying: If AoE > 0 or buff missing thrash
            if state.get('nearby_enemies_count', 1) >= 2: return True
            if self._needs_dot_refresh(state, 106830, 15.0): return True # Thrash Dot
            return False

        if "stealth_bonus_needed" in conditions:
            # Shadowmeld Rake
            return True

        # ASSASSINATION ROGUE LOGIC
        if "pool_energy_for_kingsbane_block" in conditions:
            # Block Envenom if Kingsbane ready soon and Energy < 100
             rem = state.get('cooldown_rem_slot_05', 99)
             if rem < 2.0 and state.get('resource', 0) < 100: return False # POOLING: Return FALSE (Don't cast Envenom)
             
             # Actually condition is "pool_energy_for_kingsbane_block". 
             # If True -> Condition Met -> Can Cast? No, usually conditions are "Can Cast".
             # If "pool_energy_..." implies "We are pooling", then we should NOT cast.
             # So if Pooling -> Return False.
             if rem < 2.0 and state.get('resource', 0) < 100: return False
             return True # Safe to cast

        if "kingsbane_active" in conditions:
             # Target Debuff 385627
             if 385627 in state.get('target_debuff_ids', []): return True
             return False

        if "subterfuge_active_or_refresh" in conditions:
             # Subterfuge Buff 115192 (or Stealth 1784)
             # Maximize Garrote
             if 115192 in state.get('active_buff_ids', []): return True
             if 1784 in state.get('active_buff_ids', []): return True
             # Or if Garrote missing
             if self._needs_dot_refresh(state, 703, 18.0): return True
             return False

        if "energy_lt_50_tea_ready" in conditions:
             # Thistle Tea
             if state.get('resource', 0) < 50: return True
             return False
             
        if "energy_lt_50_tea_ready" in conditions:
             # Thistle Tea
             if state.get('resource', 0) < 50: return True
             return False

        # FROST DK LOGIC
        if "breath_active_rp_low" in conditions:
            # Breath (152279)
            # If active and RP < 40 -> Needs emergency fuel
            if 152279 in state.get('active_buff_ids', []) and state.get('resource', 0) < 40: return True
            return False

        if "breath_active_rp_critical" in conditions:
             # Arcane Torrent range (RP < 20)
             if 152279 in state.get('active_buff_ids', []) and state.get('resource', 0) < 20: return True
             return False
             
        if "killing_machine_active_or_breath_sustain" in conditions:
             # Killing Machine (51124)
             # During Breath, we spam Obliterate to generate RP regardless of KM
             if 152279 in state.get('active_buff_ids', []): return True
             # Normal rotation: Only if KM active
             if 51124 in state.get('active_buff_ids', []): return True
             return False

        if "rime_proc_active" in conditions:
             # Rime (59052)
             if 59052 in state.get('active_buff_ids', []): return True
             return False
             
        if "rime_safe_to_consume" in conditions:
             # Don't consume Rime if we are about to cap RP during Breath?
             # Or if KM is up and we prefer Obliterate?
             # User says: "Delay free HB until crit-Obliterate fired" if KM active.
             if 51124 in state.get('active_buff_ids', []): return False # KM active -> Hold HB
             return True

        if "breath_inactive_and_rp_high" in conditions:
             # Frost Strike: Only if Breath NOT active
             if 152279 in state.get('active_buff_ids', []): return False
             if state.get('resource', 0) > 70: return True
             return False

        if "burst_window_active_pool_full" in conditions:
             # Cast Breath if Cooldown ready AND RP > 90
             if state.get('resource', 0) >= 90: return True
             return False
             
        if "death_grip_safe_pull" in conditions:
             # Don't grip if target will be pulled through neutral packs?
             # Opposite of Harpoon scan?
             # "Safety Scan" for pull trajectory?
             if state.get('path_danger_rating', 0) > 20: return False
             return True

        if "death_grip_safe_pull" in conditions:
             # Don't grip if target will be pulled through neutral packs?
             # Opposite of Harpoon scan?
             # "Safety Scan" for pull trajectory?
             if state.get('path_danger_rating', 0) > 20: return False
             return True

        # OUTLAW ROGUE LOGIC
        if "rtb_reroll_needed" in conditions:
            # Roll the Bones Check
            # Buffs: 193356 (Broadside), 199600 (Buried), 193358 (Grand Melee), 
            # 193357 (Ruthless), 199603 (Skull), 193359 (True Bearing)
            rtb_buffs = {193356, 199600, 193358, 193357, 199603, 193359}
            active_rtb = [b for b in state.get('active_buff_ids', []) if b in rtb_buffs]
            count = len(active_rtb)
            
            # Loaded Dice (Buff 256170) -> Guarantees 2 buffs next roll
            loaded_dice = 256170 in state.get('active_buff_ids', [])
            
            # Logic:
            # If 0 buffs -> Roll
            if count == 0: return True
            
            # If Loaded Dice active and only 1 buff -> Reroll (to get 2)
            if loaded_dice and count < 2: return True
            
            # If 1 buff and it's "Bad" (Grand Melee or Buried Treasure alone)?
            # Simplified: Onlyreroll if count == 1 and NOT Broadside/Ruthless/TrueBearing?
            # For now, let's stick to "Keep any" unless Loaded Dice allows upgrade.
            return False

        if "opportunity_valid_no_cap" in conditions:
            # Opportunity Proc (195627)
            if 195627 not in state.get('active_buff_ids', []): return False
            # Prevent CP Cap ( Pistol Shot gives 2-3 CPs with multipliers?)
            # Assuming 2 CP generic gain from Opportunity Pistol Shot
            current_cp = state.get('secondary_resource', 0)
            max_cp = state.get('secondary_resource_max', 5)
            # If we are 1 or 0 away from max, don't cast generator
            if current_cp >= max_cp - 1: return False
            return True

        if "bte_off_cooldown_or_buff_missing" in conditions:
            # Between the Eyes (315341) Cooldown check managed by main engine (implied)
            # Check for BTE Critical Buff (Keep it up?)
            # Or just use on cooldown as Finisher? Usually on CD.
            return True

        if "blade_flurry_maintenance" in conditions:
            # Blade Flurry (13877)
            # Only if 2+ targets
            if state.get('nearby_enemies_count', 1) < 2: return False
            # Check if active
            if 13877 in state.get('active_buff_ids', []): return False
            # Check charges? Engine checks charges_gte_1
            return True

        if "hook_safe_path" in conditions:
            # Grappling hook logic
            if state.get('path_danger_rating', 0) > 15: return False
            return True
            
        if "adrenaline_active" in conditions:
             if 13750 in state.get('active_buff_ids', []): return True
             return False

        if "adrenaline_active" in conditions:
             if 13750 in state.get('active_buff_ids', []): return True
             return False

        # MARKSMANSHIP HUNTER LOGIC
        if "aimed_shot_safe_stationary" in conditions:
            # Aimed Shot (19434)
            # Must be stationary or have "Lock and Load" (194594 - Instant Aimed Shot) active
            if 194594 in state.get('active_buff_ids', []): return True # Instant -> Safe
            if state.get('is_moving'): return False 
            # Check Casting Lock Logic? 
            # Assuming Engine handles "Stop to Cast" if flagged, but logic usually checks 'is_moving' to prevent accidental cancels.
            # If user wants "hard casting lock", that's an Executor function. 
            # Logic Processor says "Good to cast".
            return True

        if "precise_shots_missing" in conditions:
            # Don't cast Aimed Shot if we are "Full" on Precise Shots?
            # Precise Shots (260242) stacks up to 2.
            # If stacks == 2, we should spend them before casting Aimed Shot to avoid overwrite?
            # User says: "Refuse to pulse a second Aimed Shot if the buff is active".
            # So if Stacks > 0 -> Return False (Don't Cast Aimed)
            stacks = state.get('active_buff_stacks', {}).get(260242, 0)
            if stacks > 0: return False
            return True

        if "precise_shots_active_or_dump" in conditions:
             # Arcane Shot / Multi Shot using Precise Shots
             stacks = state.get('active_buff_stacks', {}).get(260242, 0)
             if stacks > 0: return True
             if state.get('resource', 0) > 80: return True # Dump focus
             return False

        if "trigger_trick_shots" in conditions:
             # Multi-Shot (257620)
             # Logic: If 3+ targets (or 2+?) -> Cast Multi to get Trick Shots (Buff 257622)
             # If Buff 257622 already active -> Don't need to cast Multi?
             # Unless we need to refresh it.
             # User says "If >= 3 targets -> Pulse Multi".
             if state.get('nearby_enemies_count', 1) >= 3:
                 if 257622 not in state.get('active_buff_ids', []): return True
                 # If active but expiring? (Duration 10s usually).
                 # Also need to dump Precise shots in AoE -> Multi Shot replaces Arcane Shot.
                 return True
             return False # Single Target -> Arcane Shot uses Slot 02 usually

        if "rapid_fire_move_safe" in conditions:
             # Rapid Fire (257044) - Castable while moving
             return True
             
        if "sweet_spot_adjustment" in conditions:
             # Disengage condition
             # If target < 15 yds -> Pulse
             dist = state.get('target_range', 40)
             if dist < 15: return True
             return False

        if "offensive_vanish_needed" in conditions:
            # Cast Vanish if Garrote/Rupture/Kingsbane allows it?
            # Usually for Improved Garrote
            if "stealth" in state.get('cast_history', []): return False # Debounce
            if 385627 in state.get('target_debuff_ids', []): return True # During Kingsbane? Yes for Garrote dmg
            return False

        # RECOVERY: BLOOD DEATH KNIGHT LOGIC
        if "bone_shield_critical" in conditions:
            # Bone Shield (195181)
            stacks = state.get('active_buff_stacks', {}).get(195181, 0)
            if stacks <= 6: return True
            rem = state.get('active_buff_rem', {}).get(195181, 0)
            if rem < 4: return True
            return False
            
        if "bone_shield_check_ok" in conditions:
            stacks = state.get('active_buff_stacks', {}).get(195181, 0)
            if stacks > 6: return True
            return False

        if "death_strike_heartbeat_optimal" in conditions:
            # Slot 03
            # Logic: If HP < 70% OR RP > 90 OR Blood Shield Low
            dmg_window = state.get('damage_taken_5s_percent', 0)
            if state.get('health_percent', 100) < 60: return True
            if state.get('resource_percent', 0) > 90: return True
            if dmg_window > 15: return True
            return False

        if "gorefiend_center_pull" in conditions:
            return False 

        if "runic_power_deficit_restore" in conditions:
             if state.get('resource_percent', 100) < 50 and state.get('health_percent', 100) < 50:
                 return True
             return False

        # FIRE MAGE LOGIC
        if "heating_up_conversion" in conditions:
             # Convert Heating Up (48107) to Hot Streak (48108) via Fire Blast
             # Check if we are casting Fireball/Scorch
             if 48107 in state.get('active_buff_ids', []):
                 if state.get('is_casting') or state.get('is_channeling_scorch'): 
                     return True
             return False
        
        if "hot_streak_active" in conditions:
             if 48108 in state.get('active_buff_ids', []): return True
             return False

        if "hot_streak_missing" in conditions:
             if 48108 in state.get('active_buff_ids', []): return False
             return True

        if "combustion_rotation" in conditions:
             # If Combustion is active, priority on Fire Blast / Phoenix
             if 190319 in state.get('active_buff_ids', []): return True
             return False
             
        if "stationary_check_or_shimmer" in conditions:
             # Fireball check
             if not state.get('is_moving'): return True
             # If moving, only return True if Shimmer charges avail to cast? 
             # No, this meant "Can I cast?". 
             # If moving and NO ice floes/scorch -> False.
             # Slot 17 Shimmer handles the movement, but Slot 01 should be blocked if moving unless we know we will shimmer.
             return False # Let Shimmer pulse then we stop?

        if "charging_overflow" in conditions: # Phoenix Flames
             if state.get('charges_slot_04', 0) >= 2: return True
             return False

        if "alter_time_safety" in conditions:
             # Slot 18
             # 1. Cast if full HP and burst incoming
             # 2. Re-cast (Cancel) if HP low or time up
             # Buff: Alter Time (110909)
             has_buff = 110909 in state.get('active_buff_ids', [])
             
             if not has_buff:
                 # Initial Cast: High HP + Danger
                 if state.get('health_percent', 100) > 90 and state.get('path_danger_rating', 0) > 5:
                     return True
             else:
                 # Reset (Second Cast): HP drop
                 # We need to know 'hp_at_cast'. If State doesn't have it, we guess.
                 # If HP < 40%, assume it's lower than start -> Reset
                 if state.get('health_percent', 100) < 40: return True
                 
             return False

        # DISCIPLINE PRIEST LOGIC
        if "atonement_bridge_critical" in conditions:
            count = state.get('active_atonement_count', 0)
            if count < 5 and state.get('party_size', 1) >= 5: return True
            if state.get('dbm_timer_next_aoe', 100) < 3.0: return True
            return False

        if "atonement_saturated" in conditions:
             count = state.get('active_atonement_count', 0)
             if count >= 3: return True 
             return False

        if "penance_mobile_safe" in conditions:
             return True
             
        if "radiance_cast_lock" in conditions:
             if state.get('is_moving'): return False
             return True

        if "schism_active_or_delay" in conditions:
             # Wait for Schism debuff (214621) if talent likely
             if 214621 in state.get('target_debuff_ids', []): return True
             # If Mind Blast ready soon, wait?
             if state.get('cooldown_rem_slot_04', 0) < 1.0: return False 
             return True

        if "leap_of_faith_rescue" in conditions:
             dying_ally = state.get('critical_ally_hazard', None) 
             if dying_ally: return True
             return False

        if "mana_lt_20_radiance_needed" in conditions:
             pct = state.get('resource_percent', 100) 
             if pct < 20: return True
             return False

        # BREWMASTER MONK LOGIC
        if "stagger_level_high_or_red" in conditions:
            # Stagger Buffs: Light(124275), Moderate(124274), Heavy(124273)
            # We want to Purify if Heavy (Red) OR Moderate (Yellow) > threshold
            buffs = state.get('active_buff_ids', [])
            if 124273 in buffs: return True # Red -> Purify
            if 124274 in buffs:
                # Check normalized stagger amount if avail?
                # For now, just purify Yellow to be safe or if charges > 1
                if state.get('charges_slot_04', 0) > 1: return True
            return False

        if "purified_chi_optimal" in conditions:
            # Celestial Brew (Slot 05)
            # Checks 'Purified Chi' stacks (Buff 324739), max 10
            stacks = state.get('active_buff_stacks', {}).get(324739, 0)
            if stacks >= 5: return True
            if state.get('health_percent', 100) < 40: return True # Panic shield
            return False

        if "stagger_level_high_for_damage" in conditions:
            # Niuzao damage bonus
            if 124273 in state.get('active_buff_ids', []): return True
            return False

        if "transcendence_panic_escape" in conditions:
            if state.get('standing_in_fire'): return True
            if state.get('health_percent', 100) < 20: return True
            return False
            
        if "transcendence_missing_anchor" in conditions:
             # Check if Transcendance Buff/Totem exists? 
             # Buff 101643? Or simply checking if we placed it.
             # Assume we track 'transcendence_placed_time' in state
             if not state.get('transcendence_placed'): return True
             return False
             
        if "stagger_reset_needed" in conditions:
             # Shadowmeld drop
             if 124273 in state.get('active_buff_ids', []) and state.get('health_percent', 100) < 15:
                 return True
             return False

        if "not_moving_or_surge" in conditions:
            if not state.get('is_moving'): return True
            # Check Lava Surge (77762)
            if 77762 in state.get('active_buff_ids', []): return True
            # Also Spiritwalker's Grace (79206)
            if 79206 in state.get('active_buff_ids', []): return True
            return False
            
        if "stormkeeper_absent" in conditions:
            # ID 191634
            if 191634 in state.get('active_buff_ids', []): return False
            return True
            
        if "not_moving_or_stormkeeper" in conditions:
            if not state.get('is_moving'): return True
            if 191634 in state.get('active_buff_ids', []): return True
            return False

        if "psyfiend_sniper_kill_shot" in conditions:
            # Check for Enemy Healer < 40% HP
            healer = self._find_enemy_healer(state)
            if healer and healer['hp_percent'] < 45:
                 return True
            return False

        if "psyfiend_sniper_kill_shot" in conditions:
            # Check for Enemy Healer < 40% HP
            healer = self._find_enemy_healer(state)
            if healer and healer['hp_percent'] < 45:
                 return True
            return False
            
        # HOLY PALADIN LOGIC
        if "glimmer_spread_needed" in conditions:
            # Holy Shock (Slot 01)
            # Logic: Prioritize targets WITHOUT Glimmer (Buff 287280)
            # Max Glimmers = 8
            # If target has Glimmer, only cast if low HP urgent heal
            # Current target context: 'target_unit' from state
            if 287280 in state.get('target_buff_ids', []):
                # Has Glimmer. Cast only if emergency
                if state.get('target_health_percent', 100) < 60: return True
                return False
            # Does not have Glimmer -> Spread it
            return True
            
        if "holy_power_not_capped" in conditions:
            # Don't generator if 5 HP
            hp = state.get('secondary_resource', 0) # Holy Power
            if hp >= 5: return False
            return True

        if "holy_power_spender_needed" in conditions:
            # Word of Glory / LoD
            hp = state.get('secondary_resource', 0)
            if hp >= 3:
                # Spend if capped OR healing needed
                if hp == 5: return True
                if state.get('health_percent', 100) < 85: return True # Self or Target
            return False

        if "buff_missing_consecration" in conditions:
            # Consecration (26573) - Check if standing in yours?
            # Hard to track ground effect ID owner.
            # Usually we track 'consecration_active' via combat log timer
            if not state.get('consecration_active'): return True
            return False

        if "aoe_healing_burst_needed" in conditions:
            # Beacon of Virtue logic
            # Use if 3+ allies < 75% HP
            low_hp_count = 0
            for f in state.get('party_frames', []):
                if f['hp_percent'] < 75: low_hp_count += 1
            
            if low_hp_count >= 3: return True
            return False

        if "freedom_root_break" in conditions:
            # Freedom (1044)
            # Check for Snare/Root Debuff Types on SELF or Target
            # Using generic function or specific IDs
            if state.get('is_rooted'): return True
            if state.get('is_snared') and state.get('is_moving'): return True
            return False

        if "holy_power_fill_needed" in conditions:
             # Arcane Torrent
             hp = state.get('secondary_resource', 0)
             if hp <= 2 and state.get('health_percent', 100) < 50: return True
             return False

        # DEVOURER DEMON HUNTER (257) LOGIC
        if "range_25_check" in conditions:
             # Mid-range spec (25 yds)
             if state.get('target_range', 50) <= 25: return True
             return False

        if "souls_starved" in conditions:
             # Consume (Slot 1) if low souls
             # Max 50. Low < 10?
             if state.get('secondary_resource', 0) < 15: return True
             return False

        if "souls_overflow_risk" in conditions:
             # Reap (Slot 2) generates souls. Don't cast if near cap.
             # Cap 50. Gen ~10.
             if state.get('secondary_resource', 0) > 40: return False
             return True

        if "souls_high_dump" in conditions:
             # Void Ray (Slot 3) Spender.
             if state.get('secondary_resource', 0) >= 30: return True
             return False

        if "collapsing_star_execute" in conditions:
             # Slot 4. Priority if Target < 35% HP
             if state.get('target_health_percent', 100) < 35: return True
             # Or if Void Form active?
             if 200000 in state.get('active_buff_ids', []): return True # Fake ID for Void Form
             return False

        if "souls_threshold_metamorphosis" in conditions:
             # Enter Void Form (Slot 5) if Souls > 40
             if state.get('secondary_resource', 0) >= 40: return True
             return False

        if "shift_gap_close" in conditions:
             # Custom Mobility 'Shift' logic
             # If target > 25 yds -> Dash
             if state.get('target_range', 0) > 25 and state.get('is_moving'): return True
             return False

        if "double_cast_buffer_blur" in conditions:
             # Avoid double tapping Blur (Dispersion type logic)
             if 198589 in state.get('active_buff_ids', []): return False
             return True
             
        if "double_cast_buffer_retreat" in conditions:
             # Vengeful Retreat
             # Debounce check in cast history?
             if "Vengeful Retreat" in state.get('cast_history', [])[:1]: return False
             return True

        if "double_cast_buffer_retreat" in conditions:
             # Vengeful Retreat
             # Debounce check in cast history?
             if "Vengeful Retreat" in state.get('cast_history', [])[:1]: return False
             return True

        # PROTECTION PALADIN (66) LOGIC
        if "consecration_missing_or_moving" in conditions:
             # Slot 05 - The Anchor
             # If moving, we might need to re-anchor if not recently cast?
             # Check buff? Consecration (188370 - Buff on self from standing in it?)
             # Actually, we track 'consecration_active' boolean usually derived from combat log/aura
             if not state.get('consecration_active'): return True
             if state.get('is_moving'):
                  # If moving, pulse to establish new anchor if cooldown ready
                  # Prevents waiting until we stop
                  return True
             return False

        if "consecration_anchor_check" in conditions:
             # Hard Gate for other abilities
             # Ret True if we are SAFE (Standing in it)
             if state.get('consecration_active'): return True
             # If missing, we return FALSE to block this slot, forcing Slot 05
             return False

        if "shield_of_righteousness_maintenance" in conditions:
             # Slot 03 - Active Mitigation
             # Check Buff 132403
             # Do not overcap. Duration stacks to ~13s?
             # Pulse if < 2s REMAINING or if HP > 4 (Dump)
             rem = state.get('active_buff_rem', {}).get(132403, 0)
             hp = state.get('secondary_resource', 0)
             
             if rem < 2.0: return True
             if hp >= 4: return True # Prevent overcap of HP
             
             # Biometric Buffer: Don't pulse if we just did? Handled by CD usually off-gcd
             return False

        if "grand_crusader_proc_hold" in conditions:
             # Avenger's Shield (Slot 04)
             # If "Grand Crusader" proc active (Buff), we have a free cast.
             # BUT, if enemy is casting, we HOLD it for interrupt?
             # User says: "Hold ... if it detects enemy caster"
             
             # If target is casting and interruptible:
             if state.get('target_casting') and not state.get('target_channeling'):
                  # It will be used by 'interrupt' slot (11) or this slot as pseudo-interrupt if we let it
                  # But Slot 11 Rebuke is melee. Slot 04 is ranged.
                  # If we are here, it means we WANT to cast it for dmg/absorb.
                  # If target is casting, we return TRUE to interrupt it!
                  return True
             
             # If NOT casting, can we just cast it for damage?
             # "Hold... for 1.5s".
             # If we just got the proc, maybe wait? 
             # For now, just Cast on Cooldown unless we explicitly want to save it?
             # Let's simple: Always Cast. 
             # Logic implies "Don't cast" if specific condition met.
             return True

        if "eye_of_tyr_predictive" in conditions:
             # Slot 08 - Pre-mitigation
             # Check 'path_danger_rating' or 'enemy_bursting'
             if state.get('path_danger_rating', 0) > 7: return True
             return False

        if "shining_light_free_heal" in conditions:
             # Word of Glory (Slot 09)
             # Buff: Shining Light (327510) - Free WoG
             if 327510 in state.get('active_buff_ids', []):
                 # Only use if HP < 70%
                 if state.get('health_percent', 100) < 70: return True
             return False
             
        if "cheat_death_anticipation" in conditions:
             # Ardent Defender
             if state.get('health_percent', 100) < 20: return True
             return False

        if "aoe_silence_needed" in conditions:
             # Arcane Torrent
             # Check nearby casting enemies
             count = 0
             for f in state.get('enemy_frames', []):
                 if f.get('is_casting') and f.get('range') < 8: count += 1
             if count >= 1: return True
             return False

        if "double_cast_buffer_retreat" in conditions:
             # Vengeful Retreat
             # Debounce check in cast history?
             if "Vengeful Retreat" in state.get('cast_history', [])[:1]: return False
             return True

        # PROTECTION PALADIN (66) LOGIC
        if "consecration_missing_or_moving" in conditions:
             # Slot 05 - The Anchor
             # If moving, we might need to re-anchor if not recently cast?
             if not state.get('consecration_active'): return True
             if state.get('is_moving'):
                  # If moving, pulse to establish new anchor if cooldown ready
                  return True
             return False

        if "consecration_anchor_check" in conditions:
             # Hard Gate for other abilities
             if state.get('consecration_active'): return True
             return False

        if "shield_of_righteousness_maintenance" in conditions:
             # Slot 03 - Active Mitigation
             # Check Buff 132403
             rem = state.get('active_buff_rem', {}).get(132403, 0)
             hp = state.get('secondary_resource', 0)
             
             if rem < 2.0: return True
             if hp >= 4: return True # Prevent overcap of HP
             return False

        if "grand_crusader_proc_hold" in conditions:
             # Avenger's Shield (Slot 04)
             # If target is casting and interruptible:
             if state.get('target_casting') and not state.get('target_channeling'):
                  return True # Interrupt!
             return True # Otherwise cast for dmg

        if "eye_of_tyr_predictive" in conditions:
             if state.get('path_danger_rating', 0) > 7: return True
             return False

        if "shining_light_free_heal" in conditions:
             # Buff: Shining Light (327510) - Free WoG
             if 327510 in state.get('active_buff_ids', []):
                 if state.get('health_percent', 100) < 70: return True
             return False
             
        if "cheat_death_anticipation" in conditions:
             if state.get('health_percent', 100) < 20: return True
             return False

        if "aoe_silence_needed" in conditions:
             count = 0
             for f in state.get('enemy_frames', []):
                 if f.get('is_casting') and f.get('range') < 8: count += 1
             if count >= 1: return True
             return False

        # ARCANE MAGE (62) LOGIC
        if "arcane_burn_phase" in conditions:
             # Burn if Mana > 70% OR Burst Cooldowns Ready
             # Burst: Arcane Surge (CD 90s) / Touch (CD 45s)
             mana = state.get('resource_percent', 100)
             if mana > 70: return True
             # Check if Burst is ready (simplified)
             if state.get('cooldown_rem_slot_05', 0) == 0: return True
             return False

        if "arcane_conserve_phase" in conditions:
             # Conserve if Mana < 30% AND Burst not active
             mana = state.get('resource_percent', 100)
             if mana < 30:
                 # Ensure we aren't in burn (Burst buff active?)
                 # Buff: Arcane Surge (365350)
                 if 365350 in state.get('active_buff_ids', []): return False
                 return True
             return False
        
        if "clearcasting_slipstream" in conditions:
             # Arcane Missiles (Slot 02)
             # Cast if Clearcasting (263725)
             if 263725 in state.get('active_buff_ids', []):
                 # Slipstream allows movement
                 return True
             # If no clearcasting, only cast if stationary?
             if not state.get('is_moving'): return True
             return False

        if "barrage_finisher_touch" in conditions:
             # Arcane Barrage (Slot 03)
             # Use if Touch of Magi is about to expire (< 1.5s) to get the snipe
             # Debuff on target: Touch of the Magi (210134)
             rem = state.get('target_debuff_rem', {}).get(210134, 0)
             if rem > 0 and rem < 2.0: return True
             
             # Also use if 4 Charges in Conserve
             if "arcane_conserve_phase" in conditions and state.get('secondary_resource', 0) == 4:
                 return True
                 
             return False

        if "surge_anchor_lock" in conditions:
             # Arcane Surge (Slot 06)
             # Must be stationary
             if state.get('is_moving'): return False
             return True

        if "touch_of_the_magi_active" in conditions:
             # Check if Touch is on target
             if 210134 in state.get('target_debuff_ids', []): return True
             return False

        if "charges_needed" in conditions:
             # Arcane Orb - use if < 2 charges
             if state.get('secondary_resource', 0) < 2: return True
             return False

        if "instant_blast_sequence" in conditions:
             # Presence of Mind
             # Use during Touch window
             if 210134 in state.get('target_debuff_ids', []): return True
             return False

        if "instant_blast_sequence" in conditions:
             # Presence of Mind
             # Use during Touch window
             if 210134 in state.get('target_debuff_ids', []): return True
             return False

        # RESTORATION SHAMAN (264) LOGIC
        if "cloudburst_window_start" in conditions:
             # Slot 05 - Cloudburst Totem
             # Use on CD OR when damage expected?
             # For now, treat as maintenance if charges available, or if heavy damage incoming.
             # Logic: If High Incoming Damage forecast
             if state.get('dbm_timer_next_aoe', 99) < 15: return True
             # Or generic maintenance
             if state.get('cooldown_rem_slot_05', 0) == 0: return True
             return False

        if "totem_maintenance" in conditions:
             # Slot 06 - Healing Stream
             # Keep 1 charge rolling usually, save 2nd for burst?
             # If < 2s duration on existing totem?
             # Hard to track specific totem duration without more data.
             # Simple: If charges == max? 
             # Let's say: Use if missing generic healing stream buff? or just on CD.
             # Use on CD for throughput.
             return True

        if "riptide_spread_needed" in conditions:
             # Slot 01 - Riptide
             # Prioritize players without Riptide buff
             # Needs 'party_frames' audit.
             # If target has no riptide, return True
             # Or if we have charges.
             return True

        if "aoe_healing_needed_cluster" in conditions:
             # Chain Heal (Slot 04)
             # Check if >= 3 injured allies in cluster
             # Simplified: 'party_health_cluster' from vision?
             # OR generic: if party_avg_hp < 85%
             avg = state.get('party_avg_health', 100)
             if avg < 85: return True
             return False

        if "raid_damage_lethal_cluster" in conditions:
             # Spirit Link Totem (Slot 08)
             # Emergency Equalizer
             if state.get('party_lowest_child_hp', 100) < 20: return True
             return False

        if "mana_restore_party" in conditions:
             # Mana Tide
             # If Healer Mana < 50%? (Self)
             if state.get('resource_percent', 100) < 50: return True
             return False

        if "tank_buster_anticipated" in conditions:
             # Earth Elemental
             if state.get('tank_health_percent', 100) < 30: return True
             return False
        
        if "knockback_peel_needed" in conditions:
             # Thunderstorm
             # If enemies in melee range > 0
             if state.get('nearby_enemies_count', 0) > 0: return True
             return False

        if "knockback_peel_needed" in conditions:
             # Thunderstorm
             # If enemies in melee range > 0
             if state.get('nearby_enemies_count', 0) > 0: return True
             return False

        # SURVIVAL HUNTER (255) LOGIC [40x40 Update]
        if "mongoose_fury_window_check" in conditions:
             # Slot 01 - Kill Command
             # Gate: Don't use KC if we are maximizing Mongoose Stacks
             # Buff: Mongoose Fury (259388)
             # If Stacks >= 4 AND Duration < 1.5s:
             # We want to squeeze one last BITE (Slot 3), NOT Kill Command.
             stacks = state.get('active_buff_stacks', {}).get(259388, 0)
             rem = state.get('active_buff_rem', {}).get(259388, 0)
             
             if stacks >= 4 and rem > 0 and rem < 1.5: return False # Block KC
             
             # Also Block KC if Focus is capped and we need to dump?
             return True

        if "mongoose_fury_stacking" in conditions:
             # Slot 03 - Mongoose Bite
             # Priority if Window is closing
             stacks = state.get('active_buff_stacks', {}).get(259388, 0)
             rem = state.get('active_buff_rem', {}).get(259388, 0)
             if stacks >= 1 and rem < 2.0: return True
             # Or if Charges capped?
             return True

        if "wildfire_bomb_leading" in conditions:
             # Slot 02 - Wildfire Bomb
             # Check Bomb Type?
             # ID: 259495 (Shrapnel), ...
             # "Leading Offset" Logic:
             # If target moving, we assume the Arduino handles the offset click.
             # Logic just approves the cast.
             return True
        
        if "mongoose_fury_max_stacks" in conditions:
             # Slot 08 - Fury of the Eagle
             # Only use at high stacks
             stacks = state.get('active_buff_stacks', {}).get(259388, 0)
             if stacks >= 5: return True
             return False
        
        if "range_extension_needed" in conditions:
             # Aspect of the Eagle
             # If target > 5 yds (Melee range)
             if state.get('target_range', 0) > 5: return True
             return False

        if "bomb_reset_logic" in conditions:
             # Kill Command resets bomb if Pheromone?
             # Buff: Behavioral Modification (Pheromone Bomb active?)
             # Logic simplified: Use KC on CD.
             return True
             
        if "devourer_void_pull_immunity" in conditions:
             # Master's Call (Slot 24)
             # Detect Devourer 'Void Pull' cast or mechanic
             # If enemy_spec 257 is casting "Void Pull"
             # Or if "Void Tether" debuff on self
             if 999257 in state.get('active_debuff_ids', []): return True # Fake ID
             
             # Matrix Check:
             # If we detect spec 257 in enemies?
             # Return True if we need immunity.
             return False

        if "gap_closer_burst" in conditions:
             # Spearhead
             # Use if Distance > 8
             if state.get('target_range', 0) > 8: return True
             return False

        if "gap_closer_burst" in conditions:
             # Spearhead
             # Use if Distance > 8
             if state.get('target_range', 0) > 8: return True
             return False

        # WINDWALKER MONK (269) LOGIC
        if "combo_strike_mastery_check" in conditions:
             # Slot 01/02/03 Gates
             # Mastery: Combo Strikes. Do not repeat last ability.
             # Check cast_history[0]
             last_cast = state.get('cast_history', [])[:1]
             # We need to know the name of the ability we are ABOUT to cast.
             # This is tricky because 'conditions' doesn't usually know the parent slot's action directly 
             # without passing it in.
             # However, we can infer or use specific checks like "tiger_palm_combo_check"
             return True # Placeholder: Implementation requires specific checks below

        if "tiger_palm_combo_check" in conditions:
             # Slot 01 - Tiger Palm
             if state.get('cast_history', []) and state['cast_history'][0] == "Tiger Palm": return False
             return True

        if "blackout_kick_combo_check" in conditions:
             # Slot 02 - Blackout Kick
             if state.get('cast_history', []) and state['cast_history'][0] == "Blackout Kick": return False
             return True

        if "rising_sun_kick_combo_check" in conditions:
             # Slot 03 - RSK
             if state.get('cast_history', []) and state['cast_history'][0] == "Rising Sun Kick": return False
             return True
             
        if "fists_of_fury_clip_protection" in conditions:
             # Slot 04 - FoF
             # Don't cast if already channeling FoF (ID 113656)
             if state.get('is_casting') and state.get('cast_spell_id') == 113656: return False
             if state.get('active_buff_ids', {}).get(113656): return False
             return True

        if "serenity_burst_window" in conditions:
             # Slot 05 - Serenity/SEF
             # Use on CD or aligned with Xuen
             if state.get('cooldown_rem_slot_06', 0) > 10: return True # Xuen IS active or on long CD? 
             # Logic: Align with Xuen (Slot 6)
             return True

        if "touch_of_death_execute" in conditions:
             # Touch of Death
             # Target HP < 15% OR HP < Player Max HP
             # Simplified execute check
             if state.get('target_health_percent', 100) < 15: return True
             return False

        if "ring_of_peace_peel" in conditions:
             # Slot 24 - RoP
             if state.get('nearby_enemies_count', 0) > 2: return True
             return False

        # GLOBAL 40x40 FIXES
        if "devourer_ghost_lane" in conditions:
             # Slot 40 Interaction Check
             # If target is Devourer (257), allow specific procs
             if state.get('target_spec_id') == 257: return True
             return False

        if "pathfinding_void_shift" in conditions:
             # Navigation Bypass
             # If Physics-Ignore buff active (e.g. Turtle 186265, Netherwalk 196555, Void Shift)
             buffs = state.get('active_buff_ids', [])
             if 186265 in buffs or 196555 in buffs: return True
             return False

        if "pathfinding_void_shift" in conditions:
             # Navigation Bypass
             # If Physics-Ignore buff active (e.g. Turtle 186265, Netherwalk 196555, Void Shift)
             buffs = state.get('active_buff_ids', [])
             if 186265 in buffs or 196555 in buffs: return True
             return False

        # PROTECTION WARRIOR (73) LOGIC
        if "shield_block_uptime" in conditions:
             # Slot 05 - Shield Block
             # Goal: 100% Uptime.
             # Check buff ID 2565 (Shield Block)
             rem = state.get('active_buff_rem', {}).get(2565, 0)
             charges = state.get('charges_slot_05', 0)
             
             # If not active, CAST.
             if rem == 0: return True
             
             # If active, extend if < 1.5s remaining AND charges > 0
             # Don't waste charges if full duration.
             if rem < 2.0 and charges > 0: return True
             
             # If charges capped (2), cast to prevent waste?
             if charges >= 2: return True
             
             return False

        if "ignore_pain_effective_health" in conditions:
             # Slot 06 - Ignore Pain
             # Goal: Don't overcap absorb.
             # Absorb cap usually based on Max HP.
             # We can't see current absorb value easily without detailed events.
             # Heuristic: Pulse if Rage > 50 AND Health < 90%
             # OR if Rage > 80 (Dump to avoid cap)
             rage = state.get('resource_current', 0)
             hp = state.get('health_percent', 100)
             
             if rage > 80: return True # Dump
             if rage > 40 and hp < 90: return True # Maintenance
             
             return False
             
        if "spell_reflect_predictive" in conditions:
             # Slot 16 - Spell Reflection
             # Check 40x40 Matrix for incoming lethal casts
             if state.get('target_casting') and not state.get('target_channeling'):
                  # Should verify it's magical/reflectable?
                  # Heuristic: All casts.
                  return True
             
             # Check focus or nearby enemies targeting me?
             return False

        if "shield_block_active_check" in conditions:
             # Shield Slam optimization?
             # Actually Shield Slam generates Rage, always good.
             # Maybe priority increases if Block is up?
             return True

        if "ally_danger_physical" in conditions:
             # Intervene
             # If ally is low and taking physical hits?
             party_low = state.get('party_lowest_child_hp', 100)
             if party_low < 40: return True
             return False

        if "ally_danger_physical" in conditions:
             # Intervene
             # If ally is low and taking physical hits?
             party_low = state.get('party_lowest_child_hp', 100)
             if party_low < 40: return True
             return False

        if "ally_danger_physical" in conditions:
             # Intervene
             # If ally is low and taking physical hits?
             party_low = state.get('party_lowest_child_hp', 100)
             if party_low < 40: return True
             return False

        if "cyclone_threat_pause" in conditions:
             # Slot 11 - Cyclone
             # Logic handled by Matchups usually.
             # Fallback: If target is casting big spell and interrupt CD?
             return False

        if "tank_peel_needed_aoe" in conditions:
             # Slot 18 - Ursol's Vortex
             tank_hp = state.get('tank_health_percent', 100)
             if tank_hp < 40 and state.get('nearby_enemies_count', 0) >= 3: return True
             return False

        if "smart_growl_logic" in conditions:
             # Placeholder for generic Smart Growl logic if moved to a helper
             # Currently implemented per-spec or via a global function?
             # Let's use the explicit logic in each spec for now.
             pass

        if "smart_threat_peel" in conditions:
             # Slot 12 - Axe Toss
             # If I have aggro (Threat > 80%) AND No Tank?
             if state.get('target_aggro', 0) > 80 and not state.get('role_tank_present'): return True
             return False

        if "smart_threat_peel" in conditions:
             # Slot 12 - Axe Toss
             # If I have aggro (Threat > 80%) AND No Tank?
             if state.get('target_aggro', 0) > 80 and not state.get('role_tank_present'): return True
             return False

        if "fingers_of_frost_overflow" in conditions:
            # Condition to prioritize Ice Lance if capping (2 stacks)
            fof_stacks = state.get('active_buff_stacks', {}).get(44544, 0)
            if fof_stacks >= 2: return True
            return False

        if "stealth_reset_burst" in conditions:
             # Offensive Vanish (for Ambush/Kingsbane setup)
             # If Deathmark Active?
             return False

        # HAVOC DEMON HUNTER (577) LOGIC
        if "fury_maintain" in conditions:
             # Slot 01 - Chaos Strike
             # Prevent capping, but ensure enough for Eye Beam/Blade Dance.
             # If Fury > 40?
             fury = state.get('resource_current', 0)
             if fury > 40: return True
             return False

        if "fury_overflow_gate_eyebeam" in conditions:
             # Slot 04 - Eye Beam
             # Generates Fury (blind fury talent usually).
             # Don't cast if Fury > 80 (Overcap risk).
             fury = state.get('resource_current', 0)
             if fury > 80: return False
             return True

        if "fel_rush_vector_safe" in conditions:
             # Slot 07 - Fel Rush
             # Safety Check: Ledge, Hazard, Pack.
             # "is_facing_ledge" boolean?
             if state.get('is_facing_ledge', False): return False
             if state.get('is_facing_hazard', False): return False
             return True
             
        if "essence_break_priority" in conditions:
             # Slot 02 - Blade Dance / Slot 06 - Essence Break
             # Essence Break (Slot 06) buffs Blade Dance.
             # So usage: Eye Beam -> Fel Rush -> Essence Break -> Blade Dance.
             # For Slot 02: If EB debuff on target (394116), FORCE CAST.
             rem = state.get('target_debuff_rem', {}).get(394116, 0)
             if rem > 0: return True
             
             # Otherwise cast on CD (Short CD).
             return True

        if "demonic_window_active" in conditions:
             # Slot 06 - Essence Break
             # Only cast if in Demon Form (Eye Beam or Meta).
             # Buff ID: 162264 (Meta)
             buffs = state.get('active_buff_ids', [])
             if 162264 in buffs: return True
             return False

        if "netherwalk_lethal_escape" in conditions:
             # Slot 15 - Netherwalk
             # Immune + Speed.
             # HP < 15% AND incoming damage?
             hp = state.get('health_percent', 100)
             if hp < 15: return True
             return False

        if "threat_unstable_peel" in conditions:
             # Slot 12 - Chaos Nova
             # > 3 enemies and Threat Unstable (Tank dropped aggro?)
             enemies = state.get('nearby_enemies_count', 0)
             # Heuristic: If I have aggro on at least 1?
             if enemies >= 3 and state.get('target_aggro', 0) > 90: return True
             return False

        if "netherwalk_lethal_escape" in conditions:
             # Slot 15 - Netherwalk
             # Immune + Speed.
             # HP < 15% AND incoming damage?
             hp = state.get('health_percent', 100)
             if hp < 15: return True
             return False

        if "threat_unstable_peel" in conditions:
             # Slot 12 - Chaos Nova
             # > 3 enemies and Threat Unstable (Tank dropped aggro?)
             enemies = state.get('nearby_enemies_count', 0)
             # Heuristic: If I have aggro on at least 1?
             if enemies >= 3 and state.get('target_aggro', 0) > 90: return True
             return False

        if "flame_shock_spread_check" in conditions:
             # Slot 08 - Primordial Wave
             # Logic: Spread Flame Shock.
             # Use on CD usually.
             return True

        if "smart_cyclone_heal_denial" in conditions:
             # Slot 11 - Cyclone (Druid)
             # Logic: Target HP < 40% AND Healer Casting Big Heal?
             # Healer specs: 65, 105, 256, 264, 270.
             # Check specific healer cast IDs if possible, or generic "is_casting_heal" flag from state.
             # State should normally provide 'target_is_casting_heal'.
             hp = state.get('target_health_percent', 100)
             casting_heal = state.get('target_casting_heal', False)
             
             if hp < 40 and casting_heal: return True
             return False

        if "lava_surge_gate" in conditions:
             # Slot 01 - Lava Burst
             # Gate: 
             # 1. Active Lava Surge Proc (77762) -> Instant.
             # 2. Or Cooldown Ready (2 charges).
             # 3. Always Crit.
             buffs = state.get('active_buff_ids', [])
             charges = state.get('charges_slot_01', 0)
             
             if 77762 in buffs: return True
             if charges > 0: return True
             
             return False

        # DEVASTATION EVOKER (1467) LOGIC
        if "essence_gate_disintegrate" in conditions:
             # Slot 02 - Disintegrate
             # Cost: 3 Essence (Base).
             # Gate: 
             # 1. Essence >= 3.
             # 2. OR Essence Burst Proc (359618) -> Free.
             # 3. OR Dragonrage active (Essence regen high).
             essence = state.get('secondary_resource', 0)
             buffs = state.get('active_buff_ids', [])
             has_proc = 359618 in buffs
             dragonrage = 375087 in buffs
             
             if has_proc: return True
             if dragonrage: return True # Spam in Dragonrage
             if essence >= 3: return True
             
             return False

        if "empower_fire_breath_gate" in conditions:
             # Slot 03 - Fire Breath
             # Logic implies "Hold Level" decision.
             # SkillWeaver Logic Return is "Should I Start Casting?".
             # The *Execution* layer handles the hold time.
             # Decision: Use on CD? Yes.
             # Unless Dragonrage aligns soon?
             # For now, simplistic CD check.
             return True

        if "empower_eternity_surge_gate" in conditions:
             # Slot 04 - Eternity Surge
             # Use on CD.
             return True

        if "hover_maintenance" in conditions:
             # Slot 17 - Hover
             # If moving and want to cast?
             # Especially Disintegrate (Channel).
             # If casting Disintegrate (356995) AND Moving?
             # Or if "is_moving" and "want_to_cast_slot_02"?
             if state.get('is_moving', False): return True
             return False

        if "landslide_root_peel" in conditions:
             # Slot 12 - Landslide
             # Root melee on top of me.
             # Check enemies in melee range.
             if state.get('nearby_enemies_count_melee', 0) > 0: return True
             return False
             
        if "rescue_healer_peel" in conditions:
             # Slot 18 - Rescue
             # Complex targeting. 
             # If Healer in hazard?
             return False

        if "deep_breath_path_safe" in conditions:
             # Slot 06 - Deep Breath
             # Verify vector?
             # Assume safe for now or manual aim.
             return True

        if "essence_burst_proc_check" in conditions:
             # Slot 01 - Living Flame
             # If Essence Burst active, maybe prioritize Disintegrate?
             # So only cast Living Flame if NO Essence Burst and Essence < 3?
             buffs = state.get('active_buff_ids', [])
             essence = state.get('secondary_resource', 0)
             has_proc = 359618 in buffs
             
             if has_proc: return False # Prioritize Spender
             if essence >= 3: return False # Prioritize Spender
             return True

        if "instant_empower_needed" in conditions:
             # Slot 08 - Tip the Scales
             # Use before Fire Breath or Eternity Surge if Bursting.
             # Check CD of Slot 03/04.
             return True

        if "lava_surge_gate" in conditions:
             # Slot 01 - Lava Burst
             # Gate: 
             # 1. Active Lava Surge Proc (77762) -> Instant.
             # 2. Or Cooldown Ready (2 charges).
             # 3. Always Crit.
             buffs = state.get('active_buff_ids', [])
             charges = state.get('charges_slot_01', 0)
             
             if 77762 in buffs: return True
             if charges > 0: return True
             
             return False

        # DEVASTATION EVOKER (1467) LOGIC
        if "essence_gate_disintegrate" in conditions:
             # Slot 02 - Disintegrate
             # Cost: 3 Essence (Base).
             # Gate: 
             # 1. Essence >= 3.
             # 2. OR Essence Burst Proc (359618) -> Free.
             # 3. OR Dragonrage active (Essence regen high).
             essence = state.get('secondary_resource', 0)
             buffs = state.get('active_buff_ids', [])
             has_proc = 359618 in buffs
             dragonrage = 375087 in buffs
             
             if has_proc: return True
             if dragonrage: return True # Spam in Dragonrage
             if essence >= 3: return True
             
             return False

        if "empower_fire_breath_gate" in conditions:
             # Slot 03 - Fire Breath
             # Logic implies "Hold Level" decision.
             # SkillWeaver Logic Return is "Should I Start Casting?".
             # The *Execution* layer handles the hold time.
             # Decision: Use on CD? Yes.
             # Unless Dragonrage aligns soon?
             # For now, simplistic CD check.
             return True

        if "empower_eternity_surge_gate" in conditions:
             # Slot 04 - Eternity Surge
             # Use on CD.
             return True

        if "hover_maintenance" in conditions:
             # Slot 17 - Hover
             # If moving and want to cast?
             # Especially Disintegrate (Channel).
             # If casting Disintegrate (356995) AND Moving?
             # Or if "is_moving" and "want_to_cast_slot_02"?
             if state.get('is_moving', False): return True
             return False

        if "landslide_root_peel" in conditions:
             # Slot 12 - Landslide
             # Root melee on top of me.
             # Check enemies in melee range.
             if state.get('nearby_enemies_count_melee', 0) > 0: return True
             return False
             
        if "rescue_healer_peel" in conditions:
             # Slot 18 - Rescue
             # Complex targeting. 
             # If Healer in hazard?
             return False

        if "deep_breath_path_safe" in conditions:
             # Slot 06 - Deep Breath
             # Verify vector?
             # Assume safe for now or manual aim.
             return True

        if "essence_burst_proc_check" in conditions:
             # Slot 01 - Living Flame
             # If Essence Burst active, maybe prioritize Disintegrate?
             # So only cast Living Flame if NO Essence Burst and Essence < 3?
             buffs = state.get('active_buff_ids', [])
             essence = state.get('secondary_resource', 0)
             has_proc = 359618 in buffs
             
             if has_proc: return False # Prioritize Spender
             if essence >= 3: return False # Prioritize Spender
             return True

        if "instant_empower_needed" in conditions:
             # Slot 08 - Tip the Scales
             # Use before Fire Breath or Eternity Surge if Bursting.
             # Check CD of Slot 03/04.
             return True

        # PRESERVATION EVOKER (1468) LOGIC
        if "echo_spread_gate" in conditions:
             # Slot 02 - Echo
             # Logic: Cast on players without Echo if Essence > 2.
             # Or if Essence Burst.
             # Priority: Injured players.
             # State should map 'lowest_health_party_member' or similar.
             buffs = state.get('active_buff_ids', [])
             essence = state.get('secondary_resource', 0)
             has_proc = 359618 in buffs
             
             if has_proc: return True
             if essence >= 2: return True
             return False

        if "stasis_ramp_check" in conditions:
             # Slot 09 - Stasis
             # If Big Damage Coming?
             return False

        if "golden_hour_check" in conditions:
             # Slot 06 - Reversion
             # If target took damage > 15% HP in last 5s?
             # 'target_recent_damage_taken_percent'
             dmg = state.get('target_recent_damage', 0)
             # Heuristic check.
             if dmg > 0: return True
             return False

        if "empower_dream_breath_gate" in conditions:
             # Slot 03 - Dream Breath
             # Use if Echo spread on 2+ targets?
             return True

        if "empower_spiritbloom_gate" in conditions:
             # Slot 04 - Spiritbloom
             # Use if single target needs big heal.
             hp = state.get('target_health_percent', 100)
             if hp < 50: return True
             return False
             
        if "raid_damage_reversal" in conditions:
             # Slot 05 - Rewind
             # Heavy logic. 
             # If total raid damage taken > X?
             return False

        # DISCIPLINE PRIEST (256) LOGIC
        if "atonement_application_efficient" in conditions:
             # Slot 01 - PW: Shield
             # Gate:
             # 1. Target doesn't have Atonement (Buff 194384).
             # 2. Or Weakened Soul check? (Debuff 6788).
             # If weak soul, can't shield, use Renew or Radiance.
             friendly_buffs = state.get('target_buff_ids', []) # On Ally
             has_atonement = 194384 in friendly_buffs
             has_weakened = 6788 in state.get('target_debuff_ids', []) # On Ally
             
             if not has_atonement and not has_weakened: return True
             return False

        if "atonement_spread_burst" in conditions:
             # Slot 02 - Radiance
             # Use if multiple allies need Atonement quickly.
             # Count allies without atonement in range?
             return True

        if "penance_offensive_valve" in conditions:
             # Slot 03 - Penance (Offensive)
             # Gate: 
             # 1. At least 3 Atonements active? (To make it worth DPSing).
             # 2. Target Enemy Valid.
             # 3. If target is Ally (Defensive Penance), logic differs.
             # Assuming Offensive Penance based on "Valve" strategy.
             atonement_count = state.get('active_atonement_count', 0)
             if atonement_count >= 1: return True
             # If low atonement, maybe skip? Or use for damage filler.
             return True

        if "life_grip_save" in conditions:
             # Slot 17 - Leap of Faith
             # If Ally HP < 20% and in Hazard?
             return False

        if "shield_ramp_initiator" in conditions:
             # Slot 09 - Rapture
             # Use before big damage to spam shields.
             return False

        # MISTWEAVER MONK (270) LOGIC
        if "teachings_stack_consumer" in conditions:
             # Slot 02 - Blackout Kick
             # Gate: 
             # 1. 3 Stacks of Teachings (Buff Check).
             # 2. Rising Sun Kick on CD (or probability logic).
             # Buff: Teachings of the Monastery (202090)
             stacks = state.get('active_buff_stacks', {}).get(202090, 0)
             if stacks >= 3: return True
             return False

        if "teachings_stack_builder" in conditions:
             # Slot 01 - Tiger Palm
             # Use to build stacks if < 3.
             # And plenty of mana?
             stacks = state.get('active_buff_stacks', {}).get(202090, 0)
             if stacks < 3: return True
             return False

        if "mist_extension_reset" in conditions:
             # Slot 03 - Rising Sun Kick
             # Use on CD basically for damage + healing + mist extension (Rising Mist).
             return True

        if "life_line_gate" in conditions:
             # Slot 04 - Vivify / Enveloping Mist
             # Gate: 
             # 1. Target HP < 80%.
             # 2. Or Ancient Teachings (Buff 388026) NOT active (need to cast to apply it via Faeline Stomp legacy? Wait, changed in DF/TWW. Usually Faeline or Essence Font applied it).
             # Modern: Essence Font or Faeline applies buffs.
             # If Target HP > 80, prefer melee.
             hp = state.get('target_health_percent', 100)
             if hp > 80: return False
             return True

        if "instant_cast_prep" in conditions:
             # Slot 06 - Soothing Mist
             # Logic implies "Dual-State".
             # If User wants to cast Vivify (Slot 4) and standing still?
             # Auto-Sooth into Vivify.
             # This might be handled by the Arduino 'Simul-Cast' command logic if we map it.
             # SkillWeaver returns 'True' here if we should channel Soothing first.
             return False

        if "threat_zoning_peel" in conditions:
             # Slot 11 - Ring of Peace
             # If melee on me or healer?
             if state.get('nearby_enemies_count_melee', 0) > 0: return True
             return False

        # WINDWALKER MONK (269) LOGIC
        if "hit_combo_gate" in conditions:
             # Check Last Ability Cast.
             # If last_cast_name == action_name, Return False.
             # State needs 'last_cast_id' or 'last_cast_name'.
             # Assuming state['last_cast_slot'] is available.
             # current_slot is implictly known by caller?
             # No, conditions don't know the slot ID unless passed or inferred.
             # But the "action" logic generally checks conditions for a specific slot.
             # Let's assume the processor handles "Don't repeat logic" generically if this condition is present?
             # Or we check `state.get('last_cast_slot')`.
             # For now, generic True (Logic Engine usually handles Sequence filters).
             # But to be explicit:
             # if state.get('last_cast_slot') == current_slot: return False
             return True

        if "aoe_channel_guard" in conditions:
             # Slot 04 - Fists of Fury
             # 1. Don't cast if already channeling it (Clipped).
             # 2. Don't cast if moving without movement buff? (FoF allows movement always in Retail? Yes/No? Usually you can move).
             if state.get('is_casting') and state.get('current_cast_id') == 113656: return False
             return True

        if "mark_of_the_crane_check" in conditions:
             # Slot 06 - Spinning Crane Kick
             # Use if Stacks High or targets > 3.
             # Stacks: Buff 228287? Or calculated from debuffs on enemies.
             enemies = state.get('nearby_enemies_count', 0)
             if enemies >= 3: return True
             return False

        if "mitigation_reflective" in conditions:
             # Slot 15 - Touch of Karma
             # High incoming damage?
             return False

        if "hazard_escape_roll" in conditions:
             # Slot 17 - Roll
             # If in hazard?
             if state.get('is_in_fire', False): return True
             return False

        # SUBTLETY ROGUE (261) LOGIC
        if "stealth_active_or_subterfuge" in conditions:
             # Slot 02 - Shadowstrike
             # Requires Stealth (1784), Shadow Dance (185313), or Subterfuge (115192).
             buffs = state.get('active_buff_ids', [])
             if any(b in buffs for b in [1784, 185313, 115192]): return True
             return False

        if "stealth_missing" in conditions:
             # Slot 01 - Backstab
             # Only if NOT in stealth/dance.
             buffs = state.get('active_buff_ids', [])
             if not any(b in buffs for b in [1784, 185313, 115192]): return True
             return False

        if "shadow_dance_pool" in conditions:
             # Slot 05 - Shadow Dance
             # Gate: 
             # 1. Energy > 80 (Pooling).
             # 2. Symbols of Death ready or active?
             # 3. Target Valid.
             energy = state.get('resource_current', 0)
             if energy < 80: return False
             
             return True

        if "secret_tech_gate" in conditions:
             # Slot 04 - Secret Technique
             # Use during Shadow Dance (Buff 185313) or Symbols (Buff 212283).
             # And CP >= 5.
             cp = state.get('secondary_resource', 0)
             buffs = state.get('active_buff_ids', [])
             
             in_window = 185313 in buffs or 212283 in buffs
             
             if cp >= 5 and in_window: return True
             return False

        if "secondary_target_cc" in conditions:
             # Slot 12 - Cheap Shot
             # If Dance Active and Mouseover/Focus exists?
             # (Requires complex targeting logic, simple "Check" for now).
             buffs = state.get('active_buff_ids', [])
             is_dancing = 185313 in buffs
             if is_dancing and state.get('mouseover_valid', False): return True
             return False

        # FERAL DRUID (103) LOGIC
        if "snapshot_check" in conditions:
             # Slot 01 - Rake
             # Logic: Apply if missing.
             # Logic: Refresh if 'Snapshot' is better?
             # Current State: does target have Rake?
             # If yes, is current Rake weak (applied without Tiger's Fury) and do we have Tiger's Fury now?
             # State simplification: 'target_debuff_source_id' usually doesn't track snapshot power in API without heavy lifting.
             # Heuristic: If < 4s remaining (Pandemic) OR (Tiger's Fury Active AND Rake not present).
             rem = state.get('target_debuff_rem', {}).get(1822, 0) # Rake ID 1822
             buffs = state.get('active_buff_ids', [])
             tigers_fury = 5217 in buffs
             
             if rem < 4.5: return True
             # If we have Tiger's Fury, we want to apply Rake... but only if the previous one didn't have it.
             # Without memory, we just ensure uptime.
             # Advanced: SkillWeaver engine 'history' tracks snapshot values?
             # For this level: Maintain Rake.
             return False

        if "finisher_bleed_snapshot" in conditions:
             # Slot 03 - Rip
             # Gate: 5 Combo Points.
             cp = state.get('secondary_resource', 0)
             if cp < 5: return False
             return True

        if "energy_buffer_bite" in conditions:
             # Slot 04 - Ferocious Bite
             # Gate:
             # 1. 5 Combo Points.
             # 2. Energy > 50 (Bonus Damage).
             # 3. OR Apex Predator (Free/Max Damage) proc (Buff 285514?)
             cp = state.get('secondary_resource', 0)
             energy = state.get('resource_current', 0)
             buffs = state.get('active_buff_ids', [])
             apex = 285514 in buffs # Check ID
             
             if cp < 5 and not apex: return False
             
             if apex: return True # Free max bite
             if energy >= 50: return True
             
             return False

        if "combo_builder_shred" in conditions:
             # Slot 02 - Shred
             # Build CP.
             return True

        if "free_heal_proc" in conditions:
             # Slot 16 - Regrowth
             # Gate: Predatory Swiftness (Buff 69369).
             # And HP < 80? Or Mouseover?
             buffs = state.get('active_buff_ids', [])
             predatory = 69369 in buffs
             
             if predatory: return True
             return False

        if "threat_redirect_opener" in conditions:
             # Slot 24 - Tricks
             # Use on cd if tank present.
             if state.get('role_tank_present', False): return True
             return False

        if "emergency_reset" in conditions:
             # Slot 16 - Vanish
             # HP < 20?
             hp = state.get('health_percent', 100)
             if hp < 20: return True
             return False

        # BALANCE DRUID (102) LOGIC
        # Note: Eclipse states are complex. 
        # Solar Eclipse: Buff 48517.
        # Lunar Eclipse: Buff 48518.
        # Eclipse (General): 393960?
        
        if "eclipse_solar_entry" in conditions:
             # Slot 01 - Wrath
             # Goal: Enter Solar Eclipse (2 casts of Starfire) OR Deal Damage in Solar.
             # Wait, in Dragonflight/TWW:
             # Cast 2 Starfire -> Solar Eclipse (Wrath buffed).
             # Cast 2 Wrath -> Lunar Eclipse (Starfire buffed).
             # If "Solar Eclipse" active -> Spams Wrath (Slot 01).
             # If "Lunar Eclipse" active -> Spams Starfire (Slot 02).
             # If NO Eclipse -> CAST 2 of ONE to enter.
             # Logic: If AoE? Enter Lunar. If ST? Enter Solar.
             
             solar = 48517 in state.get('active_buff_ids', [])
             lunar = 48518 in state.get('active_buff_ids', [])
             aoe = state.get('nearby_enemies_count', 0) > 1
             
             if solar: return True
             if not solar and not lunar and not aoe: return True # Enter Solar for ST
             return False

        if "eclipse_lunar_entry" in conditions:
             # Slot 02 - Starfire
             lunar = 48518 in state.get('active_buff_ids', [])
             solar = 48517 in state.get('active_buff_ids', [])
             aoe = state.get('nearby_enemies_count', 0) > 1
             
             if lunar: return True
             if not solar and not lunar and aoe: return True # Enter Lunar for AoE
             return False

        if "astral_power_overflow_st" in conditions:
             # Slot 03 - Starsurge
             # AP > 90? Or if Movement required?
             ap = state.get('resource_current', 0)
             if ap > 90: return True
             # Starlord stacking logic could go here.
             return False

        if "starfall_uptime_check" in conditions:
             # Slot 04 - Starfall (Cost 50)
             # 1. 2+ Targets.
             # 2. Not already active (or < 2s rem). Buff ID 191034 (Starfall on self? OR check player totems/ground effects).
             # Usually "Starfall" applies a buff to player allowing casting while moving + damage.
             # Buff: Starfall (191034)
             targets = state.get('nearby_enemies_count', 0)
             if targets < 2: return False
             
             rem = state.get('active_buff_rem', {}).get(191034, 0)
             if rem < 2.0: return True
             
             return False

        if "solar_beam_cluster_silence" in conditions:
             # Slot 11 - Solar Beam
             # Interrupt or Mass Silence.
             # If target Casting OR Cluster > 3?
             if state.get('interruptible'): return True
             return False

        if "treant_threat_relief" in conditions:
             # Slot 16 - Force of Nature
             # If No Tank and Aggro High?
             aggro = state.get('target_aggro', 0)
             if aggro > 80: return True
             return False
        
        if "pandemic_gate_sunfire" in conditions:
             # Slot 06 - Sunfire
             # ID 164815. Base 12s?
             # Pandemic < 4s.
             rem = state.get('target_debuff_rem', {}).get(164815, 0)
             if rem < 4.0: return True
             return False

        if "pandemic_gate_moonfire" in conditions:
             # Slot 07 - Moonfire
             # ID 164812. Base 16s?
             rem = state.get('target_debuff_rem', {}).get(164812, 0)
             if rem < 5.0: return True
             return False

        # ELEMENTAL SHAMAN (262) LOGIC
        if "lava_surge_gate" in conditions:
             # Slot 01 - Lava Burst
             # Gate: 
             # 1. Active Lava Surge Proc (77762) -> Instant.
             # 2. Or Cooldown Ready (2 charges).
             # 3. Always Crit.
             buffs = state.get('active_buff_ids', [])
             charges = state.get('charges_slot_01', 0)
             
             if 77762 in buffs: return True
             if charges > 0: return True
             
             return False

        if "generator_filler_check" in conditions:
             # Slot 02 - Lightning Bolt
             # Use if nothing else.
             # Gate: Don't overcap Maelstrom.
             # If Maelstrom > 90?
             ms = state.get('resource_current', 0)
             if ms > 90: return False
             return True

        if "maelstrom_dump_check" in conditions:
             # Slot 03 - Earth Shock / Ele Blast
             # Gate: Maelstrom >= 60.
             # Priority: If Maelstrom > 90 (Overflow).
             # Or if Master of the Elements (Buff) active?
             ms = state.get('resource_current', 0)
             if ms >= 60: return True
             return False

        if "pandemic_gate_flame_shock" in conditions:
             # Slot 04 - Flame Shock
             # Pandemic logic. Duration 18s?
             # Rem < 5.4s
             rem = state.get('target_debuff_rem', {}).get(188389, 0)
             if rem < 5.4: return True
             return False

        if "movement_cast_needed" in conditions:
             # Slot 17 - Spiritwalker's Grace
             # If moving and cast time > 0 required.
             if state.get('is_moving', False) and state.get('is_casting', False): return True
             return False
             
        if "tank_pet_needed" in conditions:
             # Slot 15 - Earth Elemental
             # Threat Handling.
             # If No Tank present AND (My Threat > 90 OR HP < 50).
             no_tank = not state.get('role_tank_present', False)
             aggro = state.get('target_aggro', 0)
             hp = state.get('health_percent', 100)
             
             if no_tank and (aggro > 90 or hp < 50): return True
             return False

        if "melee_peel_knockback" in conditions:
             # Slot 12 - Thunderstorm
             # If enemies nearby > 0.
             if state.get('nearby_enemies_count', 0) > 0: return True
             return False
             
        if "flame_shock_spread_check" in conditions:
             # Slot 08 - Primordial Wave
             # Logic: Spread Flame Shock.
             # Use on CD usually.
             return True

        # ARMS WARRIOR (71) LOGIC
        if "mortal_strike_priority" in conditions:
             # Slot 01 - Mortal Strike
             # Priority 1. Use whenever available.
             return True

        if "tactician_gate_op" in conditions:
             # Slot 02 - Overpower
             # Gate: Refuse if Mortal Strike (Slot 01) is off CD (or very close).
             # MS has high priority, Overpower buffs MS.
             # If MS CD < 1.0s, save GCD for MS.
             ms_cd = state.get('cooldown_rem_slot_01', 0)
             if ms_cd < 1.0: return False
             
             return True

        if "sudden_death_pool" in conditions:
             # Slot 04 - Execute
             # Condition: < 20% HP (Execute Range) OR Sudden Death Proc (248622).
             # Pooling: If Colossus Smash (Slot 05) CD < 2s, HOLD Proc.
             # Check HP
             hp = state.get('target_health_percent', 100)
             
             # Check Proc
             buffs = state.get('active_buff_ids', [])
             has_proc = 248622 in buffs
             
             # Basic Execute Range
             if hp < 20 or hp < 35: # 35 if Massacre talented. Assume < 20 for base or check talent.
                 # Always Execute in execute range (Test of Might logic might imply pooling but usually usage is huge dps).
                 return True
             
             if has_proc:
                 # Pooling logic
                 cs_cd = state.get('cooldown_rem_slot_05', 0)
                 if cs_cd < 2.0: return False # Hold for CS window
                 return True
             
             return False

        if "sweeping_strikes_check" in conditions:
             # Slot 06 - Sweeping Strikes
             # > 1 target active within range.
             enemies = state.get('nearby_enemies_count', 0)
             if enemies >= 2: return True
             return False

        if "bladestorm_non_blocking" in conditions:
             # Slot 07 - Bladestorm
             # Don't use if MS or CS off cooldown?
             # If CS active (Colossus Smash debuff 208086 on target) -> YES for damage.
             # But Bladestorm prevents MS use (unless Unhinged talented).
             # Heuristic: Use if CS window active AND MS on CD.
             ms_cd = state.get('cooldown_rem_slot_01', 0)
             if ms_cd > 1.5: return True
             return False

        if "parry_safety_check" in conditions:
             # Slot 15 - Die by the Sword
             # HP < 40 or Physical Burst
             hp = state.get('health_percent', 100)
             if hp < 40: return True
             # Matchup triggering handled in matchup json usually, but global check if physical danger?
             return False
             
        if "healer_peel_shout" in conditions:
             # Slot 12 - Intimidating Shout
             # Use if Healer under attack (Logic needs Healer Frame data).
             # Or if "My HP critical"?
             return False

        # ASSASSINATION ROGUE (259) LOGIC
        if "pandemic_gate_garrote" in conditions:
             # Slot 01 - Garrote
             # Base Duration ~18s. Pandemic < 5.4s.
             # ID 703
             rem = state.get('target_debuff_rem', {}).get(703, 0)
             if rem < 5.4: return True
             return False

        if "pandemic_gate_rupture" in conditions:
             # Slot 02 - Rupture
             # Base Duration ~24s (vary by CP). Pandemic ~7s.
             # ID 1943
             rem = state.get('target_debuff_rem', {}).get(1943, 0)
             if rem < 7.0: return True
             return False

        if "kingsbane_rush_mode" in conditions:
             # Slot 04 - Envenom during Kingsbane (ID 385627)
             # If Kingsbane active on target, prioritize Envenom to proc active poisons.
             # Debuff ID 385627 on target.
             kb_active = 385627 in state.get('target_debuff_ids', [])
             
             if kb_active:
                 # Override CP requirement? Or just ensure we dump if >= 3?
                 cp = state.get('secondary_resource', 0)
                 if cp >= 3: return True
                 
             return False

        if "energy_pool_check" in conditions:
             # Slot 03 - Mutilate
             # If Deathmark (Slot 05) coming off CD in < 5s, Pool Energy to 100.
             cd_rem = state.get('cooldown_rem_slot_05', 0)
             energy = state.get('resource_current', 0)
             
             if cd_rem < 5.0 and energy < 90: return False # Hold
             
             return True

        if "tricks_tank_snap" in conditions:
             # Slot 18 - Tricks of the Trade
             # Cast on Tank (Role).
             # If combat starting or threat high?
             # For now, simple CD usage.
             return True
             
        if "stealth_check_ambush" in conditions:
             # Slot 03 - Ambush (if Stealth) vs Mutilate
             # Check Stealth Buff (1784) or Shadowmeld (58984) or Vanish (11327).
             buffs = state.get('active_buff_ids', [])
             if any(b in buffs for b in [1784, 58984, 11327]): return True
             # If not stealthed, Mutilate logic (Energy Pool) still applies if tied to same slot key?
             # The condition list handles AND logic. If Stealth Check PASSES (meaning we ARE stealthed), return True.
             # Wait, usually Slot 03 is dual macro. If not stealthed, it's Mutilate.
             # If this condition is "Require Stealth", then return False if not stealthed.
             # But likely "Mutilate / Ambush" means "Cast Ambush if Stealth, Mutilate if Not".
             # This Condition logic is vague. Let's assume Slot 03 is acceptable if target valid.
             # But if specifically checking for Ambush trigger... 
             return True

        if "healer_cc_peel" in conditions:
             # Slot 12 - Blind
             # Targeted at Healer? 
             # For now, generic CC opportunity.
             return False

        if "threat_drop_vanish" in conditions:
             # Slot 24 - Vanish
             # Defensive Vanish.
             if state.get('target_aggro', 0) > 80: return True
             return False
             
        if "stealth_reset_burst" in conditions:
             # Offensive Vanish (for Ambush/Kingsbane setup)
             # If Deathmark Active?
             return False

        # FROST MAGE (64) LOGIC
        if "glacial_spike_gate_5" in conditions:
             # Slot 04 - Glacial Spike
             # Gate: 5 Icicles.
             # Resource: Icicles are secondary resource 'icicles' (0-5).
             # Also needs Brain Freeze for instant shatter? Ideally yes.
             # Check Icicles >= 5
             icicles = state.get('secondary_resource', 0)
             if icicles >= 5: return True
             return False

        if "shatter_combo_ready" in conditions:
             # Slot 03 - Ice Lance
             # Cast if: Active Winter's Chill (2 stacks), OR Fingers of Frost.
             # Winter's Chill ID: 228358
             # Fingers of Frost ID: 44544
             
             wc_stacks = state.get('target_debuff_stacks', {}).get(228358, 0)
             fof_stacks = state.get('active_buff_stacks', {}).get(44544, 0)
             
             if wc_stacks > 0: return True
             if fof_stacks > 0: return True
             
             return False

        if "brain_freeze_proc" in conditions:
             # Slot 02 - Flurry
             # Only cast with Brain Freeze (190446). Is Instant.
             # If casting Glacial Spike? No, usually GS -> Flurry Combo handled by Sequence.
             # Here we just check availability.
             buffs = state.get('active_buff_ids', [])
             if 190446 in buffs: return True
             return False

        if "alter_time_anchor" in conditions:
             # Slot 18 - Alter Time
             # Usage:
             # 1. Defensive: HP dropping fast?
             # 2. Offensive: Icy Veins active (snap buffs)?
             # 3. Positional: Handled by player usually.
             
             # Logic: If HP = 100 and anticipating damage? (Hard to predict)
             # Logic: If Alter Time Active -> Recast if HP Low?
             # Let's focus on Recast (Snap Back).
             # If Buff Active (110909) and HP < 50% -> Recast to heal.
             buffs = state.get('active_buff_ids', [])
             if 110909 in buffs:
                 hp = state.get('health_percent', 100)
                 if hp < 50: return True
                 return False
             
             # Initial Cast: If Bursting (Icy Veins) and HP > 90?
             if state.get('cooldown_rem_slot_05', 0) > 20 and state.get('health_percent', 100) > 90:
                 # Check if not already active
                 return True
                 
             return False

        if "threat_drop_invis" in conditions:
             # Slot 24 - Invisibility
             # Threat > 80% and Icy Veins active?
             aggro = state.get('target_aggro', 0)
             iv_rem = state.get('active_buff_rem', {}).get(12472, 0) # Icy Veins
             
             if aggro > 80 and iv_rem > 0: return True
             return False

        if "fingers_of_frost_overflow" in conditions:
            # Condition to prioritize Ice Lance if capping (2 stacks)
            fof_stacks = state.get('active_buff_stacks', {}).get(44544, 0)
            if fof_stacks >= 2: return True
            return False

        # SHADOW PRIEST (258) LOGIC
        if "dot_maintain_shadow" in conditions:
             # Slot 01 - VT/SW:P
             # Goal: Maintain Vampiric Touch (34914) and SW:P (589)
             # If VT missing or < 4s?
             rem_vt = state.get('target_buff_rem', {}).get(34914, 0)
             if rem_vt < 4.0: return True
             return False

        if "void_erosion_gate_mb" in conditions:
             # Slot 02 - Mind Blast
             # Gate: Don't cast if VT is missing (Damage loss + No Apparitions).
             rem_vt = state.get('target_buff_rem', {}).get(34914, 0)
             if rem_vt == 0: return False
             
             # Otherwise use on CD (usually handled by CD tracker)
             return True

        if "apparition_burst_scaling" in conditions:
             # Slot 03 - Devouring Plague
             # Prioritize if Cap (100) OR during Dark Ascension/Void Eruption?
             # Spec ID 258 has specialized burst windows.
             # If Insanity > 85 (Prevent Cap) -> Cast
             insanity = state.get('resource_current', 0)
             if insanity > 85: return True
             
             # If "Dark Ascension" active? (Buff ID 391109)
             buffs = state.get('active_buff_ids', [])
             if 391109 in buffs and insanity >= 50: return True
             
             return False

        if "mind_flay_clip_safe" in conditions:
             # Slot 04 - Mind Flay
             # Filler. But don't clip previous Flay if it just started?
             # Check 'is_casting' and 'cast_percent'.
             # If currently casting Mind Flay (Spell ID 15407), wait until end?
             # SkillWeaver usually handles 'not_casting' gate universally.
             # But if we want to "Clip for High Prio", that's handled by priority order.
             # This Condition is "Can I cast Filler?" -> Yes if nothing else.
             return True

        if "threat_drop_fade" in conditions:
             # Slot 18 - Fade
             # If Aggro > 80%?
             if state.get('target_aggro', 0) > 80: return True
             return False
             
        if "silence_priority_filter" in conditions:
             # Slot 11 - Silence
             # Only silence healers or lethal casts?
             # Handled by generic 'interruptible', but maybe filter specifically for Healer specs?
             # For now, generic interrupt is fine.
             if state.get('interruptible'): return True
             return False

        if "movement_filler_shield" in conditions:
             # Slot 24 - PW:S
             # Only if moving.
             if state.get('is_moving', False): return True
             return False
        
        if "hazard_escape_dispersion" in conditions:
             # Slot 14 - Dispersion
             # If in void zone/hazard?
             if state.get('is_in_void_zone', False): return True
             return False

        # DEMONOLOGY WARLOCK (266) LOGIC
        if "shard_gate_3_hog" in conditions:
             # Slot 03 - Hand of Gul'dan
             # Gate: 3 Shards minimum for efficiency.
             shards = state.get('resource_current', 0) # Warlock shards are primary resource 0-5
             if shards >= 3: return True
             
             # Exception: Demonic Core procs about to cap? Or Tyrant setup?
             # For simpler logic, stick to 3.
             return False

        if "demonic_core_check" in conditions:
             # Slot 01 - Demonbolt (Instant)
             # Buff ID: 264173 (Demonic Core)
             stacks = state.get('active_buff_stacks', {}).get(264173, 0)
             moving = state.get('is_moving', False)
             
             # If moving, use it to cast.
             if moving and stacks > 0: return True
             
             # If stacks capping (3 or 4?), dump.
             if stacks >= 3: return True
             
             # Otherwise, use Shadow Bolt (which is usually same slot key, handled by game macro or logic separation)
             # If this slot handles BOTH, return True (allow cast).
             # Assuming Slot 01 is the "Filler" slot.
             return True

        if "dreadstalkers_ready" in conditions:
             # Slot 02 - Dreadstalkers
             # Use on CD. Best generator.
             return True

        if "implosion_optimal_check" in conditions:
             # Slot 04 - Implosion
             # Logic: Imp Energy Low OR New Targets.
             # Tracking Imp Energy is hard without combat log parsing.
             # Heuristic: If > 6 Imps active and Fight Time > 10s?
             # OR: If 'nearby_enemies_count' increased recently?
             # Simplified: If > 3 enemies, explode 6+ imps.
             # Or if 'tyrant_active' IS FALSE. Don't implode during Tyrant.
             
             if state.get('pet_tyrant_active', False): return False
             
             imps = state.get('pet_imp_count', 0)
             enemies = state.get('nearby_enemies_count', 0)
             
             if enemies >= 3 and imps >= 6: return True
             # Energy expiration heuristic: If imps were summoned > 15s ago? (Hard to track)
             return False

        if "tyrant_ramp_ready" in conditions:
             # Slot 05 - Demonic Tyrant
             # Gate: Dreadstalkers Active AND High Shards/Imps?
             # Check cooldown of Dreadstalkers (Slot 02). If just used (CD > 15s?), then they are active.
             ds_cd = state.get('cooldown_rem_slot_02', 0)
             # Cool down is ~20s. If rem > 15, likely active.
             
             # Also want Grimoire Felguard active if possible?
             
             if ds_cd > 15: return True
             return False
             
        if "tyrant_prep_grimoire" in conditions:
             # Slot 06 - Grimoire Felguard
             # Pulse 2s before Tyrant.
             # Check Tyrant CD.
             tyrant_cd = state.get('cooldown_rem_slot_05', 0)
             if tyrant_cd < 3: return True
             return False

        if "smart_threat_peel" in conditions:
             # Slot 12 - Axe Toss
             # If I have aggro (Threat > 80%) AND No Tank?
             if state.get('target_aggro', 0) > 80 and not state.get('role_tank_present'): return True
             return False

        if "burning_rush_throttle" in conditions:
             # Slot 18 - Burning Rush
             # If moving and distance > 15.
             # Disable if HP < 50.
             hp = state.get('health_percent', 100)
             dist = state.get('target_range', 0)
             moving = state.get('is_moving', False)
             
             if hp < 50: return False # Safety
             if moving and dist > 15: return True
             return False
             
        if "hazard_escape_teleport" in conditions:
             # Slot 17 - Demonic Circle
             # If standing in bad stuff.
             # "is_in_puddle" from Vision?
             if state.get('is_in_void_zone', False): return True
             return False

        # UNHOLY DEATH KNIGHT (252) LOGIC
        if "wounds_needed_gate" in conditions:
             # Slot 01 - Festering Strike
             # Goal: Build wounds for Apoc (4) or Scourge Strike consumption.
             # Debuff: Festering Wound (194310) - Stacks
             stacks = state.get('target_debuff_stacks', {}).get(194310, 0)
             
             # If stacks < 4, build.
             if stacks < 4: return True
             return False

        if "wound_burst_check" in conditions:
             # Slot 02 - Scourge Strike
             # Pop wounds.
             # Only if wounds >= 1.
             stacks = state.get('target_debuff_stacks', {}).get(194310, 0)
             if stacks >= 1: return True
             return False

        if "festering_wound_gate_4" in conditions:
             # Slot 04 - Apocalypse
             # Requires 4 wounds.
             stacks = state.get('target_debuff_stacks', {}).get(194310, 0)
             
             if stacks >= 4: return True
             return False

        if "sudden_doom_proc" in conditions:
             # Slot 03 - Death Coil
             # Proc ID: 81340 (Sudden Doom)
             procs = state.get('active_buff_ids', [])
             if 81340 in procs: return True
             return False

        if "runic_power_dump" in conditions:
             # Slot 03 - Death Coil (Dump)
             # If no proc, but high RP > 80
             rp = state.get('resource_current', 0)
             if rp > 80: return True
             return False
             
        if "pet_burst_needed" in conditions:
             # Slot 06 - Dark Transformation
             # Use on CD generally, or sync with Apoc.
             # If Apoc CD < 5s?
             return True

        if "dual_interrupt_check" in conditions:
             # Slot 12 - Pet Kick / Asphyxiate
             # Use if Mind Freeze (Slot 11) is on CD.
             mf_cd = state.get('cooldown_rem_slot_11', 0)
             if mf_cd > 0 and state.get('interruptible'): return True
             return False
             
        if "spell_steal_opportunity" in conditions:
             # Slot 13 - Dark Simulacrum
             # Handled by Matchups logic usually.
             # Heuristic: If target casting > 2s mana spell?
             return False

        if "forced_movement_counter" in conditions:
             # Slot 17 - Death's Advance
             # If Knockback/Pull/Slow detected.
             if state.get('is_snared') or state.get('forced_movement_active'): return True
             return False
        
        if "pet_dead_check" in conditions:
             # Slot 20 - Raise Dead
             # If pet not active.
             if not state.get('pet_active', True): return True
             return False

        # RESTORATION DRUID (105) LOGIC
        if "lifebloom_tank_maintenance" in conditions:
             # Slot 02 - Lifebloom
             # Goal: 100% Uptime on Tank.
             # Check Target or Focus? 
             # For now, check 'target' if friendly, or 'focus' if set.
             # Buff ID: 33763
             rem = state.get('target_buff_rem', {}).get(33763, 0)
             
             # Hard Gate: Reapply if < 4.5s (Pandemic window)
             if rem < 4.5: return True
             
             return False

        if "rejuv_spread_check" in conditions:
             # Slot 01 - Rejuvenation
             # Maintain on injured targets.
             # Simple logic: If target HP < 95% and buff missing.
             # Buff ID: 774
             hp = state.get('target_health_percent', 100)
             buffs = state.get('target_buff_ids', [])
             
             if hp < 95 and 774 not in buffs: return True
             return False

        if "clearcasting_regrowth" in conditions:
             # Slot 04 - Regrowth
             # Priority 1: Omen of Clarity Proc (Free). Buff ID 16870.
             # Priority 2: Emergency HP < 40%.
             procs = state.get('active_buff_ids', [])
             hp = state.get('target_health_percent', 100)
             
             if 16870 in procs: return True
             if hp < 40: return True
             
             return False

        if "efflorescence_tank_anchor" in conditions:
             # Slot 05 - Efflorescence
             # Maintain 100% uptime under tank.
             # Tracking ground effect is hard.
             # Heuristic: Recast if CD ready AND combat time > 10s?
             # Or state['totem_active_slot_05'] if tracked.
             # Simple: Use on CD if in combat.
             if state.get('in_combat') and state.get('cooldown_rem_slot_05', 0) == 0: return True
             return False

        if "mastery_harmony_check" in conditions:
             # Swiftmend Gate
             # Requires a HoT (Rejuv/Regrowth/WildGrowth) to function.
             # Also benefits from Mastery (More HoTs = More Healing).
             # Check if target has at least 1 HoT ID: 774, 8936 (Regrowth), 33763 (LB), 48438 (WG)
             buffs = state.get('target_buff_ids', [])
             hots = [b for b in buffs if b in [774, 8936, 33763, 48438]]
             
             if len(hots) >= 1: return True
             return False
             
        if "cyclone_threat_pause" in conditions:
             # Slot 11 - Cyclone
             # Logic handled by Matchups usually.
             # Fallback: If target is casting big spell and interrupt CD?
             return False

        if "tank_peel_needed_aoe" in conditions:
             # Slot 18 - Ursol's Vortex
             tank_hp = state.get('tank_health_percent', 100)
             if tank_hp < 40 and state.get('nearby_enemies_count', 0) >= 3: return True
             return False

        # ENHANCEMENT SHAMAN (263) LOGIC
        if "maelstrom_weapon_gate_5" in conditions:
             # Slot 03 - Lightning Bolt
             # Gate: Only cast if stacks >= 5 (Instant Cast)
             # Buff: Maelstrom Weapon (344179)
             stacks = state.get('active_buff_stacks', {}).get(344179, 0)
             
             # If 10 stacks (Max), Force Cast
             if stacks >= 10: return True
             
             # If 5-9 stacks:
             # Cast if no other high priority melee ability?
             # For now, simplistic gate: >= 5 required.
             if stacks >= 5: return True
             
             return False

        if "stormbringer_reset_check" in conditions:
             # Slot 01 - Stormstrike
             # Priority: If Stormbringer proc (201846), Force Slot 01.
             buffs = state.get('active_buff_ids', [])
             if 201846 in buffs: return True
             
             # Otherwise only if off CD (Logic engine handles CD usually, but here we emphasize use)
             return True

        if "flame_shock_spread_check" in conditions:
             # Slot 02 - Lava Lash
             # If Molten Assault talented, LL spreads Flame Shock.
             # Check if target has Flame Shock.
             # Ideally we use LL to spread.
             return True

        if "grounding_totem_predictive" in conditions:
             # Slot 13 - Grounding Totem
             # Check casting of lethal spells (Matchups usually handle this, but generic rule:)
             # If target casting > 1.5s cast time remaining?
             return False # Rely on Matchup Triggers usually, or simple casting check

        if "static_field_combo" in conditions:
             # Capacitor Totem (+ Static Field)
             # If AOE needed.
             if state.get('nearby_enemies_count', 0) >= 3: return True
             return False

        if "spirit_walk_snare_cleanse" in conditions:
             # Slot 17 - Spirit Walk
             # If Rooted or Snared
             if state.get('is_rooted') or state.get('is_snared'): return True
             return False
        
        if "maelstrom_instant_heal_critical" in conditions:
             # Healing Surge (Instant)
             # Stacks >= 5 and HP < 40%
             stacks = state.get('active_buff_stacks', {}).get(344179, 0)
             hp = state.get('health_percent', 100)
             
             if stacks >= 5 and hp < 40: return True
             return False

        # GUARDIAN DRUID (104) LOGIC
        if "ironfur_stack_check" in conditions:
             # Slot 03 - Ironfur
             # Stackable buff. ID 192081.
             # Goal: Maintain at least 1 stack.
             # If high rage, stack 2-3.
             # If damage intake is high, priority increases.
             rem = state.get('active_buff_rem', {}).get(192081, 0)
             stacks = state.get('active_buff_stacks', {}).get(192081, 0)
             rage = state.get('resource_current', 0)
             
             # Maintenance
             if rem < 2.0: return True
             
             # Stacking (Dump Rage)
             if rage > 60 and stacks < 3: return True
             
             return False

        if "frenzied_regen_metric" in conditions:
             # Slot 05 - Frenzied Regeneration
             # Uses charges. Heals % of damage taken or % health.
             # Use if HP < 80%?
             hp = state.get('health_percent', 100)
             charges = state.get('charges_slot_05', 0)
             
             if hp < 60: return True # Emergency
             if hp < 85 and charges > 1: return True # Efficient use
             return False

        if "mangle_proc_check" in conditions:
             # Slot 01 - Mangle
             # Procs reset CD.
             # Simple priority: Use on CD.
             return True
             
        if "raze_proc_active" in conditions:
             # Slot 04 - Raze (Replaces Maul)
             # Tooth and Claw proc? Or simple aoe rage dump.
             # If 135286 (Tooth and Claw) proc active?
             return True

        if "threat_handshake_taunt" in conditions:
             # Slot 15 - Growl
             # Logic: If Target Aggro < 100% on ME (Tank)?
             # Or check 'aggro_percentage' in state.
             # Assuming state['target_aggro'] is MY aggro on target.
             # If I'm tanking, it should be 100%. If < 100, I lost aggro?
             # OR: 'threat_lead' metric?
             # Implementation: If I am NOT target of target?
             # state['is_tanking'] boolean from Analysis?
             
             # Simple: If party member has aggro > 90% (Handshake Logic)
             # For now: If I am not target target and in combat.
             if state.get('in_combat') and not state.get('is_target_of_target', True): return True
             return False
             
        if "enrage_dispel_needed" in conditions:
             # Soothe
             if 12345 in state.get('target_buff_ids', []): return True # Placeholder Enrage ID
             return False

        # TANK / PROTECTION LOGIC
        if "mitigation_needed_physical" in conditions:
            # ...
            return True

        if "mitigation_needed_minor" in conditions:
            # Ignore Pain usage
            # Don't starve Shield Block
            if state.get('current_resource', 0) < 60: return False # Save rage for Block
            return True

        if "ally_danger_physical" in conditions:
            # Intervene Logic
            # Check if a party member is taking hits?
            # This requires 'party_frames' aggro status or health drops
            # Placeholder:
            target = self._get_healing_target(state)
            if target and target['hp_percent'] < 50:
                return True
            return False
            
        if "spell_reflect_predictive" in conditions:
            # Check if target is casting a reflectable spell
            # Requires a list of Reflectable IDs in 'lethal_spells' or 'mechanics'
            # Or generally any magic cast?
            if state.get('target_casting') and not state.get('target_channeling'):
                 return True
            return False

        # WARLOCK / DoT LOGIC
        if "refresh_dot_agony" in conditions:
            # ID 980
            return self._needs_dot_refresh(state, 980, 18.0) # Base 18s
            
        if "refresh_dot_corruption" in conditions:
            # ID 146739
            return self._needs_dot_refresh(state, 146739, 14.0)
            
        if "refresh_dot_ua" in conditions:
            # ID 316099
            # UA limit 1 target usually?
            return self._needs_dot_refresh(state, 316099, 21.0)
            
        if "dots_active" in conditions:
            # Check for generic "Big 3" presence
            debuffs = state.get('target_debuff_ids', [])
            # Agony(980) + Corruption(146739)
            if 980 not in debuffs: return False
            if 146739 not in debuffs: return False
            # UA optional? usually yes for dumping
            return True

        if "channel_safe" in conditions:
            # Don't clip generic channels unless almost done?
            # Or specifically for Drain Soul - we want to channel unless interrupted or high priority
            # For "Application", we only cast if NOT already channeling it?
            if state.get('is_casting') and state.get('cast_spell_id') == 198590: return False # Don't recast Drain Soul
            return True

        # ... (Rest of checks)
        
        return True

    def get_jitter_offset(self):
        """
        GLOBAL FIX III: Arduino Jitter
        Returns a millisecond offset based on Sine-Wave function to mimic human input.
        """
        import math
        t = time.time() * 10 # Speed
        # Sine wave between -15ms and +15ms
        offset = int(math.sin(t) * 15)
        return offset

    def _needs_dot_refresh(self, state, spell_id, base_duration):
        """
        Pandemic Logic: Refresh if remaining < 30% of base duration.
        """
        # We need precise duration rem tracking from Vision
        # state['target_debuffs'] = { spell_id: remaining_time }
        rem = state.get('target_debuff_rem', {}).get(spell_id, 0)
        if rem == 0: return True # Missing
        if rem <= (base_duration * 0.3): return True # Pandemic
        return False


    def _find_enemy_healer(self, state):
        """
        Scans enemy_frames to find a healer spec.
        """
        frames = state.get('enemy_frames', [])
        for f in frames:
            # Check spec ID or role if available in Vision
            # Healer Spec IDs: 105 (Druid), 270 (Monk), 65/70? No 65 is Holy Pal, 256/257 Priest, 264 Sham
            healer_specs = {105, 270, 65, 256, 257, 264, 1468} # 1468 Pres Evoker
            if f.get('spec_id') in healer_specs:
                return f
        return None

    def _get_healing_target(self, state):
        """
        Scans party_frames from state for lowest HP member.
        Returns: {x, y, hp} or None
        """
        frames = state.get('party_frames', [])
        if not frames: return None
        
        # Sort by HP ascending
        frames.sort(key=lambda f: f['hp_percent'])
        lowest = frames[0]
        
        if lowest['hp_percent'] >= 95: return None
        return lowest

    def _should_tab_target(self, state):
        """
        Checks if Multi-Dot cycling is needed.
        Requires 'nearby_enemies_count' and 'enemies_dotted_count' from Vision.
        """
        total = state.get('nearby_enemies_count', 1)
        dotted = state.get('enemies_dotted_count', 0)
        
        # If we have more enemies than dotted targets, and main target is fine: TAB.
        if total > 1 and dotted < total:
            # Check main target DoT status (e.g. Agony)
            # This logic is simplified; real version needs specific spell tracking
            return True
        return False

    def _calculate_stat_squish_velocity(self, state):
        """
        Midnight 12.0: Converts absolute damage to % of Max HP per second.
        """
        history = self.last_known_state.get('target_health_history', [])
        if not history: return 0
        
        # Calculate drop over 1 second
        current_hp_pct = state.get('target_health_percent', 100)
        # Find entry closest to 1.0s ago
        now = time.time()
        past_hp = current_hp_pct
        for hp, t in reversed(history):
            if (now - t) >= 1.0:
                past_hp = hp
                break
        
        velocity = past_hp - current_hp_pct
        return velocity # Returns % lost per second

    def _get_hero_talent_latency(self, spec_id, spell_id):
        """
        Returns latency offset in ms for Hero Talent animations.
        """
        # Dark Ranger (Hunter) - Black Arrow
        if spec_id in [253, 254] and spell_id == 443456: # Fake ID
            return 150 # Slower travel time
        # Voidweaver (Priest) - Entropic Rift
        if spec_id in [256, 258] and spell_id == 443789:
            return 200
        return 0

    def get_pet_cc_status(self, state):
        """
        Checks if Pet is CC'd.
        """
        pet_debuffs = state.get('pet_debuff_ids', [])
        # Common CC: Fear (5782), Stun (408)
        cc_ids = [5782, 408, 118, 3355, 339] # Fear, Kidney, Poly, Freeze, Root
        for debuff in pet_debuffs:
            if debuff in cc_ids:
                return True
        return False
        
    def _should_intervene_aoe(self, state):
        """
        Warrior Smart Intervene for AoE Clusters.
        """
        party = state.get('party_frames', [])
        if not party: return None
        
        # Count members taking damage in last second
        taking_damage_count = 0
        center_target = None
        
        for p in party:
            if p.get('is_taking_damage', False):
                taking_damage_count += 1
                
        if taking_damage_count >= 3:
            # Find middle (heuristic: simply first or tank? Warrior Logic says "Middle of Cluster")
            # Return valid target for Intervene
             return party[0] # Simplified
        return None

    def get_safe_leap_vector(self, player_pos, enemy_nameplates):
        """
        Calculates a 'Safe Vector' for movement skills.
        Avoids: Dense Nameplate clusters (unpulled packs).
        """
        if not player_pos or not enemy_nameplates:
            return None
        
        # Grid Scan: Check 8 ordinal directions at 150px distance
        # Simple heuristic: Count nameplates within 100px of target point
        
        safe_candidates = []
        directions = [
            (0, -150), (106, -106), (150, 0), (106, 106), 
            (0, 150), (-106, 106), (-150, 0), (-106, -106)
        ]
        
        px, py = player_pos
        
        for dx, dy in directions:
            target_x, target_y = px + dx, py + dy
            # Check density
            density = 0
            for plate in enemy_nameplates:
                ex, ey, ew, eh = plate
                # Distance to nameplate center
                ecx, ecy = ex + (ew//2), ey + (eh//2)
                dist = ((target_x-ecx)**2 + (target_y-ecy)**2)**0.5
                if dist < 100: density += 1
            
            if density == 0:
                safe_candidates.append((target_x, target_y))
        
        if not safe_candidates:
            return None # No safe escape!
            
        # Return the one closest to current mouse? Or just the first valid?
        # For panic safety, first valid is fine.
        return safe_candidates[0]

    def _check_hazard_safety(self, state):
        """
        Returns True if player is standing in a 'ground_hazards' ID.
        """
        # In real engine -> vision detects "Deadly Swirl" under center screen anchor
        if state.get('standing_in_fire'):
            print("HAZARD DETECTED: SAFETY LEAP")
            self.bridge.send_flick_to_safety() # Special Arduino CMD
            return True
        return False

        if "preemptive_reflect" in conditions:
             # Check if target is casting a Reflectable Spell AND progress > 90%
             # Logic extended to checking Target OR Focus? User asked for Focus handling.
             # "Automatically Fear/Bolt the Focus target"
             pass # Handled by specific focus slots

        # ...
        return True
