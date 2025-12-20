import time

class PVPEngine:
    def __init__(self, bridge, matrix):
        self.bridge = bridge
        self.matchups = matrix['spec_counters']
        self.juke_window = matrix['global_pvp_logic']['juke_threshold_ms']

    def calculate_optimal_kick(self, enemy_spec_id, cast_time_remaining):
        # Retrieve spec-specific kick timing
        threshold = self.matchups.get(str(enemy_spec_id), {}).get('interrupt_at', 0.85)
        
        if cast_time_remaining <= (1.0 - threshold):
            return True
        return False

    def execute_bait_sequence(self):
        """
        Implements Move-Cancel / 'W' baiting to force enemy interrupts
        into a fake cast (Precognition-Meta Baiting).
        """
        # Start Cast (Hardware Key)
        self.bridge.send_input("CAST_KEY") 
        # Wait for human-like window to bait the kick
        time.sleep(self.juke_window / 1000)
        # Cancel move (W tap)
        self.bridge.send_input("W")
        print("BAIT_SEQUENCE_EXECUTED: PRECOG_READY")

    def handle_priority_collision(self, active_buffs):
        """
        Logic for deciding between a defensive 'Chord' or an offensive 
        rotation when both are triggered simultaneously.
        """
        if "STUNNED" in active_buffs:
            self.bridge.execute_chord("TRINKET_DEFENSIVE")
