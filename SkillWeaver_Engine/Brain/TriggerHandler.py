import pynput
import threading

class TriggerHandler:
    def __init__(self, engine):
        self.engine = engine
        self.trigger_key = 'num_7' # Default Keypad key, config can override

    def on_press(self, key):
        try:
            # Check if the key pressed is your 'Go' signal
            # Supports both Numpad 7 and F13 (common foot pedal mapping)
            if hasattr(key, 'char') and key.char == self.trigger_key:
                self.engine.execute_single_pulse()
            elif key == pynput.keyboard.Key.f13:
                self.engine.execute_single_pulse()
        except AttributeError:
            pass

    def start_listener(self):
        # Non-blocking listener in a separate thread if needed, 
        # or main thread depending on architecture.
        with pynput.keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()
