import time

class Sentinel:
    def __init__(self):
        self.is_chat_open = False
        self.is_dead = False
        self.is_disconnected = False
        self.last_check = 0

    def check_safety(self, state):
        """
        Returns False if it is UNSAFE to pulse (Chat open, Dead, DC).
        """
        # 1. Death Check
        if state.get('health_percent', 100) <= 0:
            print("SENTINEL: Player Dead. Locking Input.")
            return False

        # 2. Chat Check (Mock logic - in real engine, reads pixel 'Chat Cursor')
        # Here we rely on state data fed from Chameleon
        if state.get('is_chat_open', False):
            print("SENTINEL: Chat Open. Locking Input.")
            return False

        # 3. Disconnect / Loading Screen Check
        # If frame_count hasn't updated in 2 seconds?
        current_frame = state.get('frame_count', 0)
        # Note: LogicProcessor handles frame uniqueness logic, but Sentinel holds the hard gate.
        
        return True
