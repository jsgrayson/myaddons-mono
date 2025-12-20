import time

class PriorityEngine:
    def __init__(self, bridge, matchups, gear_profile):
        self.bridge = bridge
        self.matchups = matchups
        self.gear_profile = gear_profile # From GearOptimizer data
        self.interrupt_lock = False
        self.bait_window_start = 0
        self.is_baiting = False

    def handle_bait_continuation(self, state_data):
        """
        Uses the dedicated Interrupt Sector (Pixels 16-30 approx in Retina?)
        Updated indices for Retina (2x): 8->16, 9->18, 10->20
        """
        try:
            cast_progress = state_data[0, 16, 1]  # Pixel 8 (Log) -> 16 (Phys)
            is_bait = state_data[0, 18, 0] > 128   # Pixel 9 (Log) -> 18 (Phys) - Bait Flag
            school_lock = state_data[0, 20, 2] > 128 # Pixel 10 (Log) -> 20 (Phys) - Nature?

            if is_bait:
                # If it's a bait, we only kick if it's > 85% finished (Pixel value 216/255)
                return cast_progress > 216
            
            # Non-bait: Kick instantly if it's a priority school (Nature/Holy)
            if school_lock and cast_progress > 30:
                return True
                
            return cast_progress > 50 # Standard 20% threshold
        except (IndexError, TypeError):
            return False

    def check_lethal_anchor(self, packet):
        # Physical index 32 = Logical Pixel 16
        try:
            anchor_pixel = packet[0, 32]
            # If the Red channel (Index 0 in BGRA or RGB? user said "Red channel (Index 0)"). 
            # In previous logic we used Index 0 for Red in BGRA? No, Blue is 0, Green 1, Red 2 usually in OpenCV/MSS.
            # BUT the user explicitly wrote: "if anchor_pixel[0] > 160:".
            # AND "Based on your RGB Data [173, 35, 23], Red is index 0". 
            # Wait. RGB data [173, 35, 23] means Red is 173. If it's index 0, then the array is RGB.
            # MSS usually returns BGRA. 
            # In vision.py: `img = np.array(sct.grab(monitor))`. `sct.grab` returns BGRA.
            # So Index 0 is Blue, 1 is Green, 2 is Red.
            # However, the user said "Red is index 0". 
            # If I follow instructions blindly, I check index 0. 
            # BUT earlier `main.py` check: `spec_id_red = raw_pixel[2] # In BGRA, index 2 is Red`.
            # User previously approved that.
            # NOW user says "Based on your RGB Data... Red is index 0". 
            # This contradicts the BGRA nature of MSS unless they converted it?
            # `vision.py` does NOT convert. 
            # If the user says "Red is index 0", they might be mistaken about the array order OR they want me to allow "160" on the Blue channel (which might be the red channel in their mind?).
            # "pixel_zero = current_packet[0, 0]; red_channel = pixel_zero[0]" -> This was user request in Step 6786.
            # I implemented it in `main.py`? 
            # Let me check my `main.py` implementation in Step 6792:
            # `pixel_zero = current_packet[0, 0]; red_channel = pixel_zero[0]`
            # Wait, did I implement index 0 or 2?
            # Step 6792: `red_channel = pixel_zero[0]`
            # So main.py IS CHECKING INDEX 0.
            # If that works, then MSS is returning RGB?? Or the user is colorblind/confused but "it works".
            # Or MSS on Mac returns RGB? (Docs say BGRA).
            # I will follow the User's Code Snippet strictly: `anchor_pixel[0] > 160`.
            if anchor_pixel[0] > 160: 
                return True
            return False
        except:
            return False

    def solve_collision(self, state_data):
        """
        INGESTS FULL 40-PIXEL MATRIX (Retina 80px Width)
        state_data[0, x] maps to the horizontal data row.
        Scaled 2x for Retina Indices.
        """
        try:
            # 1. Update Internal Resource State
            # Pixel 3 -> 6, Pixel 4 -> 8
            self.energy = state_data[0, 6, 1] # Green channel of pixel 3 (Log) -> 6 (Phys)
            self.combo_points = state_data[0, 8, 1] 
            
            # 2. Check for "Emergency" Bait resolution
            if self.handle_bait_continuation(state_data):
                return {"action": "kick", "priority": 100, "signal": "K"}

            # 3. Proc Check (Pixels 16-25 -> 32-50)
            # Pixel 16 -> 32 (Checks Index 0 > 160)
            lethal_anchor_active = self.check_lethal_anchor(state_data)
            if lethal_anchor_active and self.energy > 35:
                # Eviscerate Signal 'E' (or '5', 'V' depending on keymap. Defaulting E)
                return {"action": "eviscerate", "priority": 95, "signal": "E"}

            # 4. Fallback to Standard Rotation
            return self.execute_standard_rotation(state_data)

        except (IndexError, TypeError):
            return {"action": "wait", "priority": 0, "signal": "0"}

        # PRIORITY 2: HARD-COUNTER (39x39 Matchup Matrix)
        # Check if enemy just popped a lethal CD defined in matchups.json
        if state_data['enemy_lethal_active']:
            counter_chord = self.matchups.get_counter(state_data['enemy_spec'])
            if counter_chord:
                self.bridge.execute_chord(counter_chord)
                return

        # PRIORITY 3: PRECOG-BAITING (Stealth Jitter & Humanized Intercepts)
        if state_data['precog_sensor'] == "READY":
            self.execute_bait_sequence()
            return

        # PRIORITY 4: STANDARD ROTATION (matrix.json)
        self.execute_standard_rotation(state_data)

    def execute_standard_rotation(self, state):
        # Implementation of the 6-button model (ST/AOE/HEAL/SELF/INT/UTIL)
        pass
