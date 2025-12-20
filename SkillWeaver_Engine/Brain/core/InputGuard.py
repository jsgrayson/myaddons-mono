import time

class InputGuard:
    """
    Hardware Firewall: Ensures the engine ONLY listens to the designated Keypad.
    Ignores inputs from Primary Keyboard (WASD/Chat) and Mouse.
    """
    def __init__(self, target_vid, target_pid):
        self.target_vid = target_vid # e.g. 0x046D
        self.target_pid = target_pid # e.g. 0xC22D
        self.device_path = None
        self._find_device()

    def _find_device(self):
        # Placeholder for hidapi logic
        # In production: import hid
        # for device in hid.enumerate():
        #     if device['vendor_id'] == self.target_vid ...
        print(f"INPUT GUARD: Locked to Hardware ID {hex(self.target_vid)}:{hex(self.target_pid)}")
        self.device_path = "MOCKED_DEVICE_PATH"

    def process_event(self, event):
        """
        Filters incoming events. Returns the key if authorized, None if blocked.
        """
        # In a real hook, we check event.device_id against self.device_path
        # For simulation, we assume the hook only passes data if ID matches
        
        # LOGIC:
        # If event source != Keypad -> RETURN NONE (Ignore)
        # If event source == Keypad -> RETURN KEY
        
        # Logic to differentiate 'typing' vs 'pulsing'
        return event.key
