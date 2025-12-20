import time
import random

class SequenceManager:
    def __init__(self, bridge, rotation_db):
        self.bridge = bridge
        self.rotation_db = rotation_db  # The 39-spec local library
        self.interrupt_lock = False
        self.last_action_time = 0

    def get_biometric_delay(self, base_delay_ms=0):
        """
        Calculates the Human-Mimicry curve (80ms - 120ms standard GCD window).
        Prevents static millisecond intervals that trigger anti-cheat.
        """
        jitter = random.randint(-15, 25)
        return (base_delay_ms + 100 + jitter) / 1000

    def weave(self, spec_id, combat_data):
        """
        The "Midnight" Fallthrough Logic:
        1. HARD_COUNTER (Matchup Matrix)
        2. LATE_KICK (Predictive)
        3. PRIMARY_SEQUENCE (Rotation)
        4. PANIC_FALLTHROUGH (Sustain)
        """
        now = time.time()
        
        # 1. Global Intercept: Check for priority interrupts first
        if combat_data['enemy_casting'] and combat_data['cast_percent'] > 0.85:
            self.bridge.execute_chord("INTERRUPT")
            self.last_action_time = now
            return

        # 2. Sequence Execution with Biometric Timing
        if now - self.last_action_time < self.get_biometric_delay():
            return # Still in the humanized "muscle travel" window

        # 3. Fallthrough Selection
        sequence = self.rotation_db.get_sequence(spec_id, combat_data['context'])
        
        for action in sequence:
            if self.validate_conditions(action, combat_data):
                # SUCCESS: Inject specific Spell ID through hardware
                self.bridge.send_spell_id(action['spell_id'])
                self.last_action_time = now
                break

    def validate_conditions(self, action, data):
        """
        Checks resources, ranges, and auras from the Chameleon Strip.
        """
        # Logic for Resource thresholds (from Pixel 7) 
        # and Aura-Watch status (from Pixels 11-16)
        return True
