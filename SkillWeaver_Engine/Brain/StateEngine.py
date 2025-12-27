"""
StateEngine.py - 3-Tier Priority State Machine

Priority Order:
  1. REACTIVE: Enemy triggers (Glacial Spike, Chaos Bolt, etc.) -> Counter response
  2. GATED: Abilities with conditions (procs, resources, buffs)
  3. UNGATED: Fillers with no conditions (last resort)

This replaces the flat priority list with intelligent state-aware decision making.
"""

import os
import json
import glob
import time
import random
from ConditionEngine import ConditionEngine


# Master Map of Universal Reactive Slots
REACTION_MAP = {
    "INTERRUPT": ["slot_11"],
    "STUN_PEEL": ["slot_12", "slot_13"],
    "MAJOR_DEF": ["slot_14", "slot_15", "slot_24"],
    "GAP_CLOSER": ["slot_17", "slot_18"],
    "DISPEL": ["slot_12", "slot_13"],  # Mass Dispel, Purge
}

# High-priority enemy casts/auras that trigger instant reactions
HIGH_PRIORITY_TRIGGERS = [
    # Big Damage Casts
    'Glacial Spike', 'Chaos Bolt', 'Greater Pyroblast', 'Aimed Shot',
    # Burst Windows
    'Shadow Blades', 'Avenging Wrath', 'Metamorphosis', 'Combustion', 
    'Arcane Power', 'Colossus Smash', 'Bladestorm', 'Bestial Wrath',
    # CC Casts (interrupt priority)
    'Polymorph', 'Cyclone', 'Fear', 'Hex', 'Repentance',
    # Healer Saves
    'Tranquility', 'Divine Hymn', 'Revival',
    # Immunities (to dispel)
    'Divine Shield', 'Ice Block', 'Blessing of Protection',
    # Rogue Windows
    'Shadow Dance', 'Vendetta',
]

# Spec-specific mobility tools (slot that enables casting while moving)
MOBILITY_TOOLS = {
    62: "slot_17",   # Arcane Mage - Shimmer
    63: "slot_17",   # Fire Mage - Shimmer
    64: "slot_17",   # Frost Mage - Shimmer
}

# =============================================================================
# KNOWN COOLDOWNS - Auto-detect major CDs by ability name
# These cooldowns are applied even if not defined in JSON
# =============================================================================
KNOWN_COOLDOWNS = {
    # Major DPS Cooldowns (2-3 min)
    "celestial alignment": 180, "incarnation": 180, "convoke the spirits": 120,
    "avatar": 90, "recklessness": 90, "colossus smash": 45, "warbreaker": 45,
    "avenging wrath": 120, "crusade": 120,
    "vendetta": 120, "shadow blades": 120, "shadow dance": 60,
    "combustion": 120, "icy veins": 180, "arcane power": 120,
    "metamorphosis": 180, "the hunt": 90,
    "summon infernal": 180, "summon demonic tyrant": 90,
    "feral frenzy": 45, "berserk": 180, "tigers fury": 30,
    "pillar of frost": 60, "empower rune weapon": 120, "abomination limb": 120,
    "dark ascension": 60, "void eruption": 120,
    "storm earth and fire": 90, "invoke xuen": 120,
    "fury of elune": 60, "force of nature": 60,
    "ascendance": 180, "primordial wave": 45, "stormkeeper": 60,
    "bestial wrath": 90, "trueshot": 120, "coordinated assault": 120,
    
    # Major Defensive Cooldowns (1-3 min)
    "barkskin": 60, "survival instincts": 180, "ironbark": 60,
    "shield wall": 240, "last stand": 180, "demoralizing shout": 45,
    "divine shield": 300, "guardian of ancient kings": 300, "ardent defender": 120,
    "icebound fortitude": 180, "anti magic shell": 60, "vampiric blood": 90,
    "fortifying brew": 180, "dampen harm": 120, "diffuse magic": 90,
    "cloak of shadows": 120, "evasion": 120, "vanish": 120,
    "blur": 60, "darkness": 180, "netherwalk": 180,
    "astral shift": 90, "spirit link totem": 180,
    "desperate prayer": 90, "fade": 30, "dispersion": 120,
    "ice block": 240, "greater invisibility": 120, "mirror image": 120,
    "unending resolve": 180, "dark pact": 60,
    
    # Offensive Cooldowns (30-60s)
    "new moon": 20, "touch of death": 180, "spear hand strike": 15,
    "marked for death": 60, "shiv": 25,
    
    # Utility with meaningful CDs
    "solar beam": 60, "mighty bash": 60, "typhoon": 30,
    "heroic leap": 45, "charge": 20, "intervene": 30,
    "death grip": 25, "gorefiends grasp": 120,
    "ring of peace": 45, "leg sweep": 60,
}

# Additional MOBILITY_TOOLS entries
MOBILITY_TOOLS.update({
    93: "slot_18",   # Destruction - Demonic Circle
    91: "slot_18",   # Affliction - Demonic Circle
    92: "slot_18",   # Demonology - Demonic Circle
    131: "slot_17",  # Devastation Evoker - Hover
    132: "slot_17",  # Preservation Evoker - Hover
    133: "slot_17",  # Augmentation Evoker - Hover
    102: "slot_17",  # Balance Druid - (none, pivot to instants)
    32: "slot_17",   # Marksmanship - (none, pivot to instants)
})

# Instant-cast alternatives when moving (spec_id -> filler_slot -> instant_slot)
INSTANT_ALTERNATIVES = {
    63: {"slot_01": "slot_02"},   # Fire Mage: Fireball -> Scorch
    102: {"slot_01": "slot_04"},  # Balance: Wrath -> Sunfire/Moonfire
    32: {"slot_01": "slot_03"},   # Marks: Aimed Shot -> Arcane Shot
    64: {"slot_01": "slot_03"},   # Frost: Frostbolt -> Ice Lance
}

# Atomic Burst Sequences (spec_id -> trigger_slot -> chain)
# When trigger fires, lock into this sequence for max burst
ATOMIC_SEQUENCES = {
    41: {  # Assassination Rogue
        "slot_10": ["slot_05", "slot_10", "slot_08", "slot_04", "slot_04", "slot_04"],  # Kingsbane chain
    },
    103: {  # Windwalker
        "slot_05": ["slot_05", "slot_06", "slot_07", "slot_02", "slot_02"],  # Storm, Earth, Fire burst
    },
    71: {  # Elemental Shaman
        "slot_05": ["slot_05", "slot_04", "slot_03", "slot_03"],  # Stormkeeper chain
    },
    102: {  # Balance Druid
        "slot_07": ["slot_07", "slot_04", "slot_05", "slot_01", "slot_01"],  # Convoke setup
    },
    72: {  # Fury Warrior
        "slot_06": ["slot_06", "slot_05", "slot_02", "slot_01"],  # Colossus Smash push
    },
}

# =============================================================================
# MAJOR COOLDOWNS - Per-spec CD pooling groups
# These CDs should fire TOGETHER when burst window is good
# Format: spec_id -> list of slot_ids that are major CDs
# =============================================================================
MAJOR_COOLDOWNS = {
    # Balance Druid
    111: ["slot_05", "slot_06", "slot_08"],  # Celestial Alignment, Force of Nature, Convoke
    # Shadow Priest
    53: ["slot_05", "slot_06"],  # Dark Ascension, Power Infusion
    # Fire Mage
    82: ["slot_05", "slot_06"],  # Combustion, Mirror Image
    # Ret Paladin
    23: ["slot_05", "slot_06"],  # Avenging Wrath, Wake of Ashes
    # Fury Warrior
    12: ["slot_05", "slot_06"],  # Recklessness, Avatar
    # Arms Warrior
    11: ["slot_05", "slot_06", "slot_07"],  # Colossus Smash, Avatar, Warbreaker
    # Havoc DH
    121: ["slot_05", "slot_06"],  # Metamorphosis, The Hunt
    # Assassination Rogue
    41: ["slot_05", "slot_06"],  # Vendetta, Deathmark
    # Subtlety Rogue
    43: ["slot_05", "slot_06", "slot_28"],  # Shadow Blades, Secret Technique, Shadow Dance
    # Windwalker Monk
    103: ["slot_05", "slot_06"],  # Storm, Earth and Fire, Invoke Xuen
    # Devastation Evoker
    131: ["slot_05", "slot_06"],  # Dragonrage, Fire Breath
    # Elemental Shaman
    71: ["slot_05", "slot_06"],  # Ascendance, Stormkeeper
    # Marksmanship Hunter
    32: ["slot_05", "slot_06"],  # Trueshot, Volley
    # BM Hunter
    31: ["slot_05", "slot_06"],  # Bestial Wrath, Call of the Wild
    # Affliction Warlock
    91: ["slot_05", "slot_06"],  # Summon Darkglare, Dark Soul
    # Demonology Warlock
    92: ["slot_05", "slot_06"],  # Summon Demonic Tyrant, Nether Portal
    # Destruction Warlock
    93: ["slot_05", "slot_06"],  # Summon Infernal, Dark Soul
    # Unholy DK
    63: ["slot_05", "slot_06"],  # Unholy Assault, Apocalypse
    # Frost DK
    62: ["slot_05", "slot_06"],  # Pillar of Frost, Empower Rune Weapon
    # Arcane Mage
    81: ["slot_05", "slot_06"],  # Arcane Power, Touch of the Magi
    # Frost Mage
    83: ["slot_05", "slot_06"],  # Icy Veins, Frozen Orb
    # Feral Druid
    112: ["slot_05", "slot_06"],  # Berserk, Tiger's Fury
    # Enhancement Shaman
    72: ["slot_05", "slot_06"],  # Feral Spirit, Ascendance
    # Survival Hunter
    33: ["slot_05", "slot_06"],  # Coordinated Assault, Spearhead
}

# Burst window requirements
BURST_MIN_TARGET_HP = 40  # Don't burst if target below this %
BURST_MIN_CDS_READY = 1   # At least this many CDs ready to trigger burst (1 = any CD ready)

# DR Thresholds: Block high-cost stuns if target DR is active
DR_STUN_SLOTS = ["slot_12", "slot_13"]  # HoJ, Kidney Shot
DR_FALLBACK_SLOTS = {
    41: "slot_14",   # Rogue: Kidney -> Gouge
    11: "slot_14",   # Druid: Maim -> Bash
    66: "slot_15",   # Paladin: HoJ -> Blinding Light
}

# Snapshot Power Buffs (spec_id -> buff_name -> power_multiplier)
SNAPSHOT_BUFFS = {
    41: {"Vendetta": 1.3, "Stealth": 1.5, "Subterfuge": 1.5},  # Assassination
    103: {"Tiger's Fury": 1.15, "Bloodtalons": 1.25},  # Feral (uses 103 as example)
    11: {"Tiger's Fury": 1.15, "Bloodtalons": 1.25, "Stealth": 1.5},  # Feral
}

# Healer Spec IDs for Party Scan logic
HEALER_SPECS = {65, 105, 256, 257, 264, 270, 132}  # Holy Pal, Resto Druid, Disc/Holy Priest, Resto Shaman, MW Monk, Pres Evoker

# Healer Spread Slots (slots with "spread" HoT conditions)
HEALER_SPREAD_SLOTS = {
    105: ["slot_01", "slot_02", "slot_03"],  # Resto Druid: Rejuv, Lifebloom, Wild Growth
    65: ["slot_01", "slot_02"],   # Holy Pal: Beacon maintenance
    256: ["slot_01", "slot_02"],  # Disc Priest: PW:S, Atonement
    270: ["slot_01", "slot_02", "slot_03"],  # MW Monk: Renewing Mist, Enveloping
    132: ["slot_01", "slot_02"],  # Pres Evoker: Echo, Reversion
}


class StateEngine:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.matchups_dir = os.path.join(base_dir, "matchups")
        self.specs_dir = os.path.join(base_dir, "data", "specs")
        
        # Loaded data
        self.current_matchups = []
        self.global_counters = []
        self.spec_data = {}
        
        # Sequence Injection (Atomic Chains)
        self.active_sequence = None
        self.sequence_step = 0
        self.sequence_lock_time = 0
        
        # Wizard Leap Tracking
        self.last_hp = 100.0
        self.last_hp_time = time.time()
        self.last_proc_time = time.time()
        self.proc_drought_threshold = 8.0  # seconds without proc
        
        # Cooldown Tracking: {slot_id: (last_cast_time, cooldown_seconds)}
        self.slot_cooldowns = {}
        self.DEFAULT_GCD = 1.5  # Global cooldown in seconds
        
        # Load global counters
        self._load_global_counters()
    
    def is_on_cooldown(self, slot_id: str, slot: dict, state: dict = None) -> bool:
        """Check if a slot is on cooldown. Respects proc-based resets."""
        if slot_id not in self.slot_cooldowns:
            return False
        
        # Check for proc-based cooldown resets
        if state:
            # Mind Blast (slot_04) - reset by Shadowy Insight / Surge of Insanity
            if slot_id == "slot_04" and state.get('mb_reset_proc', False):
                return False  # Proc active = not on cooldown
        
        # Get cooldown: First check JSON, then fallback to KNOWN_COOLDOWNS by ability name
        cd_duration = slot.get('cooldown', 0)
        if cd_duration <= 0:
            # Try to get cooldown from KNOWN_COOLDOWNS by ability name
            action_name = slot.get('action', '').lower()
            cd_duration = KNOWN_COOLDOWNS.get(action_name, 0)
        
        if cd_duration <= 0:
            return False  # No cooldown = always ready
            
        last_cast, _ = self.slot_cooldowns[slot_id]
        elapsed = time.time() - last_cast
        return elapsed < cd_duration
    
    def mark_slot_used(self, slot_id: str, slot: dict):
        """Mark a slot as used, starting its cooldown."""
        # Get cooldown: First check JSON, then fallback to KNOWN_COOLDOWNS
        cd = slot.get('cooldown', 0)
        if cd <= 0:
            action_name = slot.get('action', '').lower()
            cd = KNOWN_COOLDOWNS.get(action_name, 0)
        
        if cd > 0:
            self.slot_cooldowns[slot_id] = (time.time(), cd)
    
    def is_major_cd(self, slot_id: str, spec_id: int) -> bool:
        """Check if this slot is a major cooldown for this spec."""
        major_cds = MAJOR_COOLDOWNS.get(spec_id, [])
        return slot_id in major_cds
    
    def is_burst_window_good(self, slot_id: str, slot: dict, state: dict) -> bool:
        """
        Smart CD timing: Only use major CDs when burst conditions are good.
        Returns True if CD should be used, False if should be saved.
        """
        spec_id = int(state.get('hash', 0))
        
        # If not a major CD, always allow
        if not self.is_major_cd(slot_id, spec_id):
            return True
        
        # Check 1: Target HP - don't waste CDs on dying targets
        target_hp = state.get('thp', 100)
        if target_hp < BURST_MIN_TARGET_HP:
            return False  # Target too low, save CDs
        
        # Check 2: Count how many major CDs are ready
        slots = self.spec_data.get('universal_slots', {})
        major_cds = MAJOR_COOLDOWNS.get(spec_id, [])
        ready_count = 0
        
        for cd_slot_id in major_cds:
            if cd_slot_id in slots:
                cd_slot = slots[cd_slot_id]
                if not self.is_on_cooldown(cd_slot_id, cd_slot, state):
                    ready_count += 1
        
        # Only burst if enough CDs are ready
        if ready_count >= BURST_MIN_CDS_READY:
            print(f"[BURST] {ready_count} CDs ready, target at {target_hp:.0f}% - BURSTING!")
            return True
        
        return False  # Not enough CDs ready
    
    def _load_global_counters(self):
        """Load counters that apply to all specs."""
        path = os.path.join(self.matchups_dir, "global_counters.json")
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    self.global_counters = data.get('global_counters', [])
                    print(f"[STATE] Loaded {len(self.global_counters)} global counters")
            except Exception as e:
                print(f"[STATE] Failed to load global counters: {e}")
    
    def load_matchups(self, spec_id: int):
        """Load spec-specific matchup counters."""
        pattern = os.path.join(self.matchups_dir, f"{spec_id}_vs_*.json")
        matches = glob.glob(pattern)
        
        self.current_matchups = []
        for path in matches:
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    counters = data.get('counters', [])
                    self.current_matchups.extend(counters)
            except Exception as e:
                print(f"[STATE] Failed to load matchup {path}: {e}")
        
        if self.current_matchups:
            print(f"[STATE] Loaded {len(self.current_matchups)} matchup counters for spec {spec_id}")
    
    def load_spec(self, spec_id: int, spec_data: dict):
        """Store spec rotation data for tier analysis."""
        self.spec_data = spec_data
    
    def check_immunity_cancellation(self, state: dict) -> bool:
        """
        LAYER 0: Immunity Cancellation (Click-off)
        
        If player is immune but the threat has cleared, cancel the immunity
        to resume DPS. This is the "Elite Move" for optimal uptime.
        
        Returns True if immunity should be canceled.
        """
        # Only check if player is currently immune
        if not state.get('is_immune', False):
            return False
        
        # Check if threat has cleared
        enemy_nuke_active = state.get('enemy_nuke_active', False)
        player_hp = state.get('hp', 0)
        
        # Cancel if: no active threat AND HP is above safety threshold
        if not enemy_nuke_active and player_hp > 75:
            print(">>> [LAYER 0] Threat Neutralized: Canceling Immunity")
            return True
        
        return False
    
    def weigh_movement_utility(self, state: dict, slot: dict, spec_id: int) -> dict:
        """
        Smart Movement Weighing: Decide whether to spend mobility tools or save them.
        
        Returns:
            dict with keys:
                'should_cast': bool - whether to proceed with the cast
                'use_mobility': bool - whether to spend mobility tool first
                'pivot_to': str|None - alternative slot to use instead
        """
        result = {'should_cast': True, 'use_mobility': False, 'pivot_to': None}
        
        # If not moving, proceed normally
        if not state.get('is_moving', False):
            return result
        
        # Determine if this is a high-value (gated) spell
        is_high_value = slot.get('conditions') is not None and len(slot.get('conditions', [])) > 0
        is_burst_active = state.get('burst_window_active', False)
        
        # Get mobility tool for this spec
        mobility_slot = MOBILITY_TOOLS.get(spec_id)
        slots = self.spec_data.get('universal_slots', {})
        mobility_ready = False
        
        if mobility_slot and mobility_slot in slots:
            # Simple ready check (no CD tracking yet, assume ready if exists)
            mobility_ready = True
        
        slot_id = slot.get('slot_id', '')
        
        # Decision Matrix:
        
        # 1. During Burst: Uptime is everything - spend the tool
        if is_burst_active and mobility_ready:
            print(f">>> [MOVE] Burst active: Spending mobility for {slot.get('action')}")
            result['use_mobility'] = True
            return result
        
        # 2. High-Value Gated Spells: Spend tool to land the big hit
        if is_high_value and mobility_ready:
            print(f">>> [MOVE] High-value cast: Spending mobility for {slot.get('action')}")
            result['use_mobility'] = True
            return result
        
        # 3. Low-Value Fillers: Check for instant alternative first
        if not is_high_value:
            alternatives = INSTANT_ALTERNATIVES.get(spec_id, {})
            if slot_id in alternatives:
                pivot_slot = alternatives[slot_id]
                if pivot_slot in slots:
                    print(f">>> [MOVE] Pivoting filler {slot.get('action')} -> instant {pivot_slot}")
                    result['should_cast'] = False
                    result['pivot_to'] = pivot_slot
                    return result
            
            # No alternative: skip the filler to save mobility
            print(f">>> [MOVE] Saving mobility: Skipping filler {slot.get('action')}")
            result['should_cast'] = False
            return result
        
        return result
    
    def execute_midnight_matchups(self, state: dict) -> dict | None:
        """
        PRIORITY 0: Reactive Overrides - runs BEFORE the standard rotation.
        Returns immediately if a counter-trigger is detected.
        """
        slots = self.spec_data.get('universal_slots', {})
        if not slots:
            return None
        
        all_counters = self.global_counters + self.current_matchups
        
        for counter in all_counters:
            trigger = counter.get('trigger', '')
            response_slot = counter.get('response_slot', '').lower()
            
            # Check: Is enemy casting this OR is this aura active?
            trigger_active = (
                state.get('enemy_casting') == trigger or 
                trigger in state.get('enemy_buffs', []) or
                (trigger in HIGH_PRIORITY_TRIGGERS and state.get('enemy_burst_detected', False))
            )
            
            if trigger_active and response_slot in slots:
                slot = slots[response_slot]
                # Resource check
                if state.get('power', 0) >= slot.get('min_resource', 0):
                    print(f">>> [REACTION] Trigger: {trigger} | Response: {counter.get('desc', slot.get('action'))}")
                    return {'slot_id': response_slot, 'priority': 0, **slot}
        
        return None
    
    def is_slot_known(self, slot_id: str, state: dict) -> bool:
        """Check if the ability in this slot is learned (via talent bitmask from P22-P25)."""
        # If talent masks are all 0 (addon not updated), assume all known
        if state.get('talent_mask_1_8', 255) == 0 and state.get('talent_mask_9_16', 255) == 0:
            return True  # Likely addon hasn't loaded yet, don't block
        
        try:
            slot_num = int(slot_id.replace('slot_', '').lstrip('0') or '0')
        except:
            return True
        
        if slot_num <= 0 or slot_num > 32:
            return True
        
        if slot_num <= 8:
            mask = state.get('talent_mask_1_8', 255)
            return bool(mask & (1 << (slot_num - 1)))
        elif slot_num <= 16:
            mask = state.get('talent_mask_9_16', 255)
            return bool(mask & (1 << (slot_num - 9)))
        elif slot_num <= 24:
            mask = state.get('talent_mask_17_24', 255)
            return bool(mask & (1 << (slot_num - 17)))
        else:
            mask = state.get('talent_mask_25_32', 255)
            return bool(mask & (1 << (slot_num - 25)))
    
    def check_enemy_trigger(self, trigger_name: str, state: dict) -> bool:
        """
        Check if an enemy trigger condition is active.
        
        Triggers are based on enemy cast detection or buff presence.
        These require telemetry from the addon (enemy_casting, enemy_buff pixels).
        """
        # Enemy casting detection (pixel-based)
        if state.get('enemy_casting') == trigger_name:
            return True
        
        # Enemy buff detection
        if trigger_name in state.get('enemy_buffs', []):
            return True
        
        # High-priority casts that need immediate reaction
        if trigger_name in HIGH_PRIORITY_TRIGGERS:
            if state.get('enemy_burst_detected', False):
                return True
        
        return False
    
    def get_optimal_action(self, state: dict) -> dict | None:
        """
        Main decision function. Returns the optimal slot to execute.
        
        Priority: Reactive > Gated > Ungated
        """
        slots = self.spec_data.get('universal_slots', {})
        if not slots:
            return None
        
        # ============================================
        # TIER 1: REACTIVE MATCHUP LAYER (Highest)
        # ============================================
        all_counters = self.global_counters + self.current_matchups
        for counter in all_counters:
            trigger = counter.get('trigger', '')
            response_slot = counter.get('response_slot', '').lower()
            
            if self.check_enemy_trigger(trigger, state):
                if response_slot in slots:
                    slot = slots[response_slot]
                    # Still check resource requirements
                    if state.get('power', 0) >= slot.get('min_resource', 0):
                        print(f"[REACTIVE] {trigger} detected -> {slot.get('action')}")
                        return {'slot_id': response_slot, **slot}
        
        # ============================================
        # TIER 2: ROTATION LAYER (Priority List)
        # Auto-detect mode from game state, then use priority list
        priorities = self.spec_data.get('priorities', {})
        target_hp = state.get('thp', 100)
        
        # AUTO-DETECT MODE:
        # - mythic: 3+ hostile nameplates (M+ trash)
        # - raid: Single-target or 1-2 targets (boss fight)
        # - delve: Solo (no group) and low hostile count
        # - pvp: PvP flag active (arena/bg)
        plates = state.get('total_hostile_plates', 1)
        is_pvp = state.get('pvp_active', False)
        group_size = state.get('group_size', 1)
        
        if is_pvp:
            mode = 'pvp'
        elif group_size <= 1 and plates <= 2:
            mode = 'delve'
        elif plates >= 3:
            mode = 'mythic'  # M+ AoE mode
        else:
            mode = 'raid'    # Single-target default
        
        rotation_order = []
        if target_hp < 35 and 'execute_phase' in priorities:
            rotation_order = priorities.get('execute_phase', [])
        
        # If no execute rotation, use mode-specific priority list
        if not rotation_order:
            if mode in priorities:
                rotation_order = priorities.get(mode, [])
            elif 'raid' in priorities:
                # Fallback to raid if mode not found
                rotation_order = priorities.get('raid', [])
                mode = 'raid (fallback)'
        
        # Debug: Log mode detection (throttled in production)
        if rotation_order and not getattr(self, '_last_mode_log', None) != mode:
            self._last_mode_log = mode
            print(f"[MODE] {mode.upper()} | Plates:{plates} | Group:{group_size}")
        
        if rotation_order:
            for slot_id in rotation_order:
                if slot_id not in slots:
                    continue
                
                slot = slots[slot_id]

                # Cooldown check
                if self.is_on_cooldown(slot_id, slot, state):
                    continue
                
                # Burst window check for major CDs (smart timing)
                if not self.is_burst_window_good(slot_id, slot, state):
                    continue
                
                # Resource check
                if state.get('power', 0) < slot.get('min_resource', 0):
                    continue
                
                # Conditions
                conditions = slot.get('conditions', [])
                all_pass = True
                for condition in conditions:
                    if not ConditionEngine.evaluate(condition, state):
                        all_pass = False
                        break
                
                if all_pass:
                    return {'slot_id': slot_id, **slot}
        
        # ============================================
        # TIER 2.5: FALLBACK GATED (Dict Order)
        # ============================================
        else:
            gated_slots = []
            ungated_slots = []
            
            for slot_id, slot in slots.items():
                conditions = slot.get('conditions', [])
                if conditions and len(conditions) > 0:
                    gated_slots.append((slot_id, slot))
                else:
                    ungated_slots.append((slot_id, slot))
            
            for slot_id, slot in gated_slots:
                if self.is_on_cooldown(slot_id, slot, state):
                    continue
                if state.get('power', 0) < slot.get('min_resource', 0):

                    continue
                
                all_pass = True
                for condition in slot.get('conditions', []):
                    if not ConditionEngine.evaluate(condition, state):
                        all_pass = False
                        break
                
                if all_pass:
                    return {'slot_id': slot_id, **slot}
            
            # Tier 3 Fallback
            for slot_id, slot in ungated_slots:
                if self.is_on_cooldown(slot_id, slot, state):
                    continue
                if state.get('power', 0) >= slot.get('min_resource', 0):
                    return {'slot_id': slot_id, **slot}
        
        return None
    
    def get_priority_breakdown(self) -> dict:
        """Debug helper: show current priority tiers."""
        slots = self.spec_data.get('universal_slots', {})
        
        gated = []
        ungated = []
        
        for slot_id, slot in slots.items():
            conditions = slot.get('conditions', [])
            entry = f"{slot_id}: {slot.get('action', 'Unknown')}"
            if conditions:
                gated.append(entry)
            else:
                ungated.append(entry)
        
        return {
            'reactive_counters': len(self.global_counters) + len(self.current_matchups),
            'gated_slots': gated,
            'ungated_slots': ungated
        }
    
    # ==========================================================================
    # ELITE LAYER: Sequence Injection (Atomic Chains)
    # ==========================================================================
    
    def check_sequence_trigger(self, state: dict, slot_id: str, spec_id: int) -> bool:
        """Check if this slot should trigger an atomic sequence."""
        if self.active_sequence:
            return False  # Already in a sequence
        
        spec_sequences = ATOMIC_SEQUENCES.get(spec_id, {})
        if slot_id in spec_sequences:
            self.active_sequence = spec_sequences[slot_id].copy()
            self.sequence_step = 0
            print(f">>> [SEQUENCE] Locking into {len(self.active_sequence)}-step chain")
            return True
        return False
    
    def run_sequence_step(self, state: dict) -> dict | None:
        """Execute the next step in the active sequence."""
        if not self.active_sequence or self.sequence_step >= len(self.active_sequence):
            self.active_sequence = None
            self.sequence_step = 0
            return None
        
        slot_id = self.active_sequence[self.sequence_step]
        slots = self.spec_data.get('universal_slots', {})
        
        if slot_id not in slots:
            self.sequence_step += 1
            return self.run_sequence_step(state)  # Skip missing slots
        
        slot = slots[slot_id]
        
        # Resource check (still need resources even in sequence)
        if state.get('power', 0) < slot.get('min_resource', 0):
            return None  # Wait for resources, don't break sequence
        
        self.sequence_step += 1
        print(f">>> [SEQUENCE] Step {self.sequence_step}/{len(self.active_sequence)}: {slot.get('action')}")
        
        if self.sequence_step >= len(self.active_sequence):
            print(">>> [SEQUENCE] Chain complete - resuming normal rotation")
            self.active_sequence = None
        
        return {'slot_id': slot_id, **slot}
    
    # ==========================================================================
    # ELITE LAYER: Diminishing Returns Filter
    # ==========================================================================
    
    def check_diminishing_returns(self, state: dict, slot_id: str, spec_id: int) -> dict:
        """
        Check if a stun/CC should be blocked due to target DR.
        Returns: {'blocked': bool, 'fallback': slot_id or None}
        """
        result = {'blocked': False, 'fallback': None}
        
        if slot_id not in DR_STUN_SLOTS:
            return result
        
        target_dr = state.get('target_stun_dr', 0)  # 0=full, 0.5=half, 1.0=immune
        
        if target_dr > 0.5:
            print(f">>> [DR] Target on DR ({target_dr:.0%}) - blocking {slot_id}")
            result['blocked'] = True
            result['fallback'] = DR_FALLBACK_SLOTS.get(spec_id)
        
        return result
    
    # ==========================================================================
    # ELITE LAYER: Snapshotting (DoT Power Refresh)
    # ==========================================================================
    
    def calculate_power_score(self, state: dict, spec_id: int) -> float:
        """Calculate current power score based on active buffs."""
        score = 1.0
        buffs = SNAPSHOT_BUFFS.get(spec_id, {})
        
        for buff_name, multiplier in buffs.items():
            if state.get(f'{buff_name.lower()}_active', False):
                score *= multiplier
        
        return score
    
    def check_snapshot_opportunity(self, state: dict, spec_id: int) -> str | None:
        """
        Check if DoTs should be refreshed early due to higher power score.
        Returns slot_id to refresh, or None.
        """
        current_score = self.calculate_power_score(state, spec_id)
        dot_score = state.get('active_dot_power_score', 1.0)
        
        # Refresh if current score is >30% higher than active DoT
        if current_score > dot_score * 1.3:
            print(f">>> [SNAPSHOT] Power surge detected ({current_score:.2f} vs {dot_score:.2f})")
            # Return primary DoT slot for this spec
            dot_slots = {
                41: "slot_06",  # Assassination: Garrote
                11: "slot_05",  # Feral: Rip
            }
            return dot_slots.get(spec_id)
        
        return None
    
    # ==========================================================================
    # ELITE LAYER: Dynamic Resource Scaling
    # ==========================================================================
    
    def get_dynamic_resource_threshold(self, state: dict, slot: dict) -> int:
        """
        Scale resource thresholds based on current regen rate.
        High haste = lower thresholds (GCD cap), low haste = pool to 90.
        """
        base_threshold = slot.get('min_resource', 0)
        regen_rate = state.get('resource_regen_rate', 10)  # Energy/sec
        is_burst = state.get('burst_window_active', False)
        
        # Heroism/Thistle Tea levels of regen
        if regen_rate > 20 or is_burst:
            return 0  # GCD cap - spend everything
        
        # Low regen - pool for burst
        if regen_rate < 8:
            return max(base_threshold, 90)
        
        return base_threshold
    
    # ==========================================================================
    # ELITE LAYER: Healer Party Scan (Multi-Hotting)
    # ==========================================================================
    
    def is_healer_spec(self, spec_id: int) -> bool:
        """Check if current spec is a healer."""
        return spec_id in HEALER_SPECS
    
    def scan_party_hot_needs(self, state: dict, spec_id: int) -> dict | None:
        """
        Healer Party Scan: Cycle through party to maintain HoTs.
        
        Returns slot to cast on specific unit, or None.
        Format: {'slot_id': str, 'target_unit': str, ...slot_data}
        """
        if spec_id not in HEALER_SPECS:
            return None
        
        spread_slots = HEALER_SPREAD_SLOTS.get(spec_id, [])
        if not spread_slots:
            return None
        
        slots = self.spec_data.get('universal_slots', {})
        party_units = ['player', 'party1', 'party2', 'party3', 'party4']
        
        # Check each party member for missing HoTs
        for unit in party_units:
            unit_hp = state.get(f'{unit}_hp', 100)
            unit_hot_active = state.get(f'{unit}_hot_active', True)
            
            # Skip if unit is healthy and has HoT, or is dead
            if unit_hp <= 0 or (unit_hp > 85 and unit_hot_active):
                continue
            
            # Find first available spread slot for this unit
            for slot_id in spread_slots:
                if slot_id not in slots:
                    continue
                slot = slots[slot_id]
                
                # Check resource requirement
                if state.get('power', 0) < slot.get('min_resource', 0):
                    continue
                
                print(f">>> [HEALER] {unit} needs HoT ({unit_hp:.0f}%) -> {slot.get('action')}")
                return {
                    'slot_id': slot_id,
                    'target_unit': unit,
                    **slot
                }
        
        return None
    
    # ==========================================================================
    # WIZARD LEAPS: Predictive Combat Modeling
    # ==========================================================================
    
    def calculate_health_velocity(self, state: dict) -> float:
        """
        LEAP 1: Health Velocity - Track HP drop rate for preemptive defensives.
        Returns HP drop rate as percentage per second.
        """
        current_hp = state.get('hp', 100)
        current_time = time.time()
        
        time_delta = current_time - self.last_hp_time
        if time_delta < 0.1:  # Avoid division by zero
            return 0.0
        
        hp_delta = self.last_hp - current_hp
        velocity = hp_delta / time_delta / 100.0  # Normalize to 0-1
        
        # Update tracking
        self.last_hp = current_hp
        self.last_hp_time = current_time
        
        return max(0.0, velocity)  # Only track damage, not healing
    
    def check_emergency_defensive(self, state: dict, hp_velocity: float) -> bool:
        """
        If taking massive damage (>40%/sec), trigger emergency defensive.
        Returns True if emergency defensive should fire.
        """
        if hp_velocity > 0.4:
            print(f">>> [VELOCITY] HP dropping at {hp_velocity:.0%}/sec - EMERGENCY DEFENSIVE")
            return True
        return False
    
    def check_overkill_protection(self, state: dict) -> bool:
        """
        LEAP 2: TTD (Time To Death) - Block spenders on dying targets.
        Returns True if target will die from existing damage.
        """
        target_hp = state.get('thp', 100)
        dots_active = state.get('target_dots_active', False)
        
        # Target dying and DoTs will finish it
        if target_hp < 5 and dots_active:
            print(f">>> [TTD] Target at {target_hp:.0f}% with DoTs - CONSERVING RESOURCES")
            return True
        
        return False
    
    def get_humanized_kick_window(self, state: dict) -> float:
        """
        LEAP 3: Humanized Jitter - Variable interrupt timing.
        Returns the cast % at which to interrupt.
        """
        target_hp = state.get('thp', 100)
        
        # Low HP = insta-kick to secure kill
        if target_hp < 10:
            return 0.1
        
        # Normal: wait between 60-85% of cast (Late Kick)
        return random.uniform(0.60, 0.85)
    
    def should_kick_now(self, state: dict) -> bool:
        """Check if interrupt should fire based on humanized timing."""
        cast_pct = state.get('enemy_cast_pct', 0)
        threshold = self.get_humanized_kick_window(state)
        
        return cast_pct >= threshold
    
    def check_positional_requirement(self, state: dict, slot_id: str, spec_id: int) -> dict:
        """
        LEAP 5: Positional Gating - Block rear-only abilities from front.
        Returns: {'blocked': bool, 'fallback': slot_id or None}
        """
        result = {'blocked': False, 'fallback': None}
        
        # Rear-only abilities
        rear_only_slots = {
            41: {"slot_01": "slot_03"},   # Rogue: Backstab -> Sinister Strike
            261: {"slot_01": "slot_03"},  # Subtlety: Backstab -> Sinister Strike  
            11: {"slot_02": "slot_05"},   # Feral: Shred -> Swipe
        }
        
        spec_rear = rear_only_slots.get(spec_id, {})
        if slot_id not in spec_rear:
            return result
        
        is_behind = state.get('is_behind_target', True)
        if not is_behind:
            print(f">>> [POSITIONAL] Not behind target - pivoting to front ability")
            result['blocked'] = True
            result['fallback'] = spec_rear[slot_id]
        
        return result
    
    def check_proc_drought(self, state: dict, spec_id: int) -> int:
        """
        LEAP 6: Proc-Due Float - Pool resources when proc is overdue.
        Returns adjusted min_resource threshold.
        """
        # Check if any high-value proc is active
        proc_active = (
            state.get('brain_freeze_active', False) or
            state.get('sudden_death_active', False) or
            state.get('hot_streak_active', False)
        )
        
        if proc_active:
            self.last_proc_time = time.time()
            return 0  # Normal threshold
        
        drought_duration = time.time() - self.last_proc_time
        
        if drought_duration > self.proc_drought_threshold:
            # Proc overdue - pool aggressively
            print(f">>> [PROC-DUE] {drought_duration:.1f}s without proc - POOLING")
            return 85
        
        return 0  # Normal threshold
    
    def check_cleave_snap_back(self, state: dict, spec_id: int) -> bool:
        """
        LEAP 4: Dynamic Cleave - Auto-tab to spread and MAINTAIN DoTs on multiple targets.
        Returns True if should send Tab to switch targets.
        """
        # Multi-dot specs (should spread DoTs across multiple targets)
        dot_specs = {
            41,   # Assassination Rogue
            91,   # Affliction Warlock
            93,   # Destruction Warlock (Immolate)
            11,   # Arms Warrior (Rend, Deep Wounds)
            53,   # Shadow Priest
            111,  # Balance Druid (Moonfire, Sunfire)
            112,  # Feral Druid
            71,   # Elemental Shaman (Flame Shock)
            72,   # Enhancement Shaman (Flame Shock)
        }
        if spec_id not in dot_specs:
            return False
        
        # Get DoT states
        dots = state.get('dots', [0, 0, 0])
        vt_remaining = dots[0] if len(dots) > 0 else 0
        swp_remaining = dots[1] if len(dots) > 1 else 0
        
        # How many other targets are visible?
        total_plates = state.get('total_hostile_plates', 0)
        missing = state.get('enemies_missing_dots', 0)
        target_hp = state.get('thp', 100)
        
        # Don't TAB if we're the only target
        if total_plates == 0:
            return False
        
        # For 2+ targets, always spread DoTs (no focus restriction)
        # Only block if target is about to die
        if target_hp < 10:
            return False  # Don't TAB away from almost-dead target
            
        # Don't TAB if our DoTs need refreshing on current target first
        # Per-spec DoT thresholds and counts
        DOT_THRESHOLDS = {
            111: (4.0, 2),   # Balance Druid: 4s, needs both Moonfire + Sunfire
            53:  (6.0, 2),   # Shadow Priest: 6s, needs both VT + SWP
            91:  (8.0, 3),   # Affliction: 8s, needs all 3 DoTs
            41:  (5.0, 2),   # Assassination: 5s, Rupture + Garrote
            112: (4.0, 2),   # Feral: 4s, Rake + Rip
            71:  (3.0, 1),   # Elemental: 3s, just Flame Shock
            72:  (3.0, 1),   # Enhancement: 3s, just Flame Shock
            93:  (4.0, 1),   # Destruction: 4s, just Immolate
            11:  (5.0, 1),   # Arms: 5s, Deep Wounds/Rend
        }
        threshold, dot_count = DOT_THRESHOLDS.get(spec_id, (6.0, 1))
        
        # Check DoTs are healthy before spreading
        dots_healthy = True
        for i in range(min(dot_count, len(dots))):
            if dots[i] < threshold:
                dots_healthy = False
                break
        
        if not dots_healthy:
            return False
        
        # ONLY TAB if enemies are missing DoTs - spread them
        # Do NOT TAB for "maintenance" cycling - that loses focus on main target
        if missing > 0:
            print(f">>> [CLEAVE] {missing} enemies missing DoTs | D1:{dots[0]:.0f}s D2:{dots[1]:.0f}s - TAB to SPREAD")
            return True
        
        # All enemies have DoTs - stay on main target, don't cycle away
        return False
    
    # ==========================================================================
    # OMEGA LEAPS: Sub-GCD Optimization & Spatial Intelligence
    # ==========================================================================
    
    def is_in_queue_window(self, state: dict) -> bool:
        """
        OMEGA 1: Sub-GCD Clipping - Check if we're in the spell queue window.
        Accounts for latency to push commands at optimal time.
        """
        gcd_remaining = state.get('gcd_remaining', 0)
        latency_ms = state.get('latency_ms', 50)
        
        # Queue window = 100ms + latency compensation
        queue_threshold = 0.1 + (latency_ms / 1000)
        
        return gcd_remaining <= queue_threshold
    
    def check_los_guard(self, state: dict, slot: dict) -> bool:
        """
        OMEGA 2: LoS Vector Gating - Block long casts if target going behind pillar.
        Returns True if should block this cast.
        """
        target_obstructed = state.get('target_obstructed_imminent', False)
        cast_time = slot.get('cast_time', 0)
        
        if target_obstructed and cast_time > 1.0:
            print(f">>> [LoS] Target moving to cover - blocking {cast_time}s cast")
            return True
        
        return False
    
    def check_cc_chain_timing(self, state: dict, slot_id: str) -> bool:
        """
        OMEGA 3: CC Chain Sync - Time stuns to land exactly when current CC ends.
        Returns True if should delay this CC.
        """
        cc_slots = ["slot_12", "slot_13"]  # Stuns/Incaps
        if slot_id not in cc_slots:
            return False
        
        target_cc_remaining = state.get('target_cc_remaining', 0)
        
        # Perfect chain: cast when CC has 0.2-0.5s left
        if target_cc_remaining > 0.5:
            print(f">>> [CC-CHAIN] Target CC has {target_cc_remaining:.1f}s - HOLDING")
            return True  # Hold the stun
        
        return False  # Fire the chain
    
    def check_mitigation_aware_burst(self, state: dict, slot: dict) -> bool:
        """
        OMEGA 4: Throttled Burst - Don't waste CDs on shielded targets.
        Returns True if should hold this cooldown.
        """
        is_major_cd = slot.get('is_major_cd', False) or slot.get('slot_id') in ["slot_05", "slot_06"]
        
        if not is_major_cd:
            return False
        
        # Major mitigation auras
        mitigation_active = state.get('target_has_major_mitigation', False)
        pain_supp = state.get('target_pain_suppression', False)
        shield_wall = state.get('target_shield_wall', False)
        turtle = state.get('target_turtle', False)
        
        if mitigation_active or pain_supp or shield_wall or turtle:
            print(f">>> [BURST] Target in defensive - HOLDING COOLDOWNS")
            return True
        
        return False
    
    def get_instant_filler(self, state: dict, spec_id: int) -> dict | None:
        """Get an instant-cast filler for LoS/movement situations."""
        instant_fillers = {
            93: "slot_02",   # Destro: Conflagrate
            64: "slot_03",   # Frost Mage: Ice Lance
            63: "slot_02",   # Fire Mage: Scorch
            102: "slot_04",  # Balance: Moonfire
        }
        
        filler_slot = instant_fillers.get(spec_id)
        if not filler_slot:
            return None
        
        slots = self.spec_data.get('universal_slots', {})
        if filler_slot in slots:
            return {'slot_id': filler_slot, **slots[filler_slot]}
        
        return None
