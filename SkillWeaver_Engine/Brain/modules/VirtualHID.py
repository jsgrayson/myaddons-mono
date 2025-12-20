# Updated to avoid ALL physical hardware conflicts
class StealthInjector:
    def __init__(self):
        # The engine is restricted to this 'Virtual Tactical' range
        # to ensure it never interferes with WASD or your Scimitar.
        self.tactical_keys = ['f13', 'f14', 'f15', 'f16', 'f17', 'f18'] 

    def inject_combat_chord(self, chord_id):
        """
        Injected directly into the input buffer.
        Zero interference with manual mouse/keyboard movement.
        """
        # Logic to send F13-F24 chords
        # In a real implementation, this would interface with the OS input stream
        # or send a specific signal to the Arduino to act as a "Virtual Keyboard"
        pass
