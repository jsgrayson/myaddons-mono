import serial
import time
from typing import Optional

class SerialLink:
    """
    The 'Finger' Communication Handler.
    Implements 11.2.7 'Midnight' Handshake Protocol.
    """
    def __init__(self, port: str = "/dev/cu.usbmodemHIDPC1", baudrate: int = 250000):
        self.port = port
        self.baudrate = baudrate
        self.ser: Optional[serial.Serial] = None
        self.connected = False

    def connect(self) -> bool:
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2) # Wait for Arduino reboot
            
            # --- 11.2.7 HANDSHAKE PROTOCOL (XOR ENCRYPTED) ---
            # Python sends XOR'd 0xFF (Status Request)
            handshake_req = 0xFF ^ 0x42
            self.ser.write(bytes([handshake_req]))
            time.sleep(0.1)
            
            # Pro Micro should respond with XOR'd 0xAA (System Ready)
            # Pro Micro should respond with 'K' (Keepalive/Killswitch Active)
            response = self.ser.read(1)
            if response == b'K' or response.hex() == '4b':
                print("[SUCCESS] Handshake Verified. Logitech Ghost Online.")
                self.connected = True
                return True
            else:
                print(f"[WARN] Hardware Desync. Response: {response.hex() if response else 'None'}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Serial Link Failure: {e}")
            return False

    def write_signal(self, signal: str):
        if self.ser and self.ser.is_open:
            # XOR Encryption for Stealth (Key 0x42)
            encrypted = ord(signal) ^ 0x42
            self.ser.write(bytes([encrypted]))

    def send_pulse(self, signal: str):
        """Alias for write_signal to match logic engine requests."""
        return self.write_signal(signal)

    def write_mouse_warp(self, signal: str, x: int, y: int):
        """Sends a signal followed by XOR-encrypted X, Y coordinates (2 bytes each)"""
        if self.ser and self.ser.is_open:
            # 1. Signal
            self.ser.write(bytes([ord(signal) ^ 0x42]))
            
            # 2. X High/Low
            self.ser.write(bytes([(x >> 8) ^ 0x42]))
            self.ser.write(bytes([(x & 0xFF) ^ 0x42]))
            
            # 3. Y High/Low
            self.ser.write(bytes([(y >> 8) ^ 0x42]))
            self.ser.write(bytes([(y & 0xFF) ^ 0x42]))

    def write_mouse_delta(self, dx: int, dy: int):
        """Sends a relative mouse movement signal (dx, dy as signed chars)."""
        if self.ser and self.ser.is_open:
            # 1. Signal (SIG_MOUSE_DELTA = 0xF9)
            self.ser.write(bytes([0xF9 ^ 0x42]))
            
            # 2. DX/DY (Clamped to signed char range)
            dx_clamped = max(-127, min(127, dx))
            dy_clamped = max(-127, min(127, dy))
            
            # Pack as unsigned bytes after XOR (0x00-0xFF)
            # Python's bytes() handles uint8. Signed char -127 is 0x81 (129).
            # But the Pro Micro expects a signed char. 
            # We'll send the raw bit pattern.
            self.ser.write(bytes([(dx_clamped & 0xFF) ^ 0x42]))
            self.ser.write(bytes([(dy_clamped & 0xFF) ^ 0x42]))

    def close(self):
        if self.ser:
            self.ser.close()
            self.connected = False
