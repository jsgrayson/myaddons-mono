import serial
import serial.tools.list_ports
import time
from typing import Optional
import glob

class SerialLink:
    def __init__(self, port: str = None, baudrate: int = 250000):
        self.port = port or self._find_arduino()
        self.baudrate = baudrate
        self.ser: Optional[serial.Serial] = None
    
    def _find_arduino(self) -> str:
        """Auto-detect Arduino by scanning USB modem ports."""
        ports = glob.glob("/dev/cu.usbmodem*")
        if ports:
            print(f"[AUTO] Found Arduino at: {ports[0]}")
            return ports[0]
        return "/dev/cu.usbmodemC1"  # Fallback

    def connect(self) -> bool:
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2) 
            
            # --- v6.0 XOR HANDSHAKE PROTOCOL ---
            # Arduino expects 0xBD (0xFF ^ 0x42) and responds with 'K'
            handshake_byte = 0xFF ^ 0x42  # = 0xBD
            self.ser.write(bytes([handshake_byte])) 
            time.sleep(0.1)
            
            response = self.ser.read(1)
            if response == b'K':
                print("[SUCCESS] Hardware Linked (XOR Handshake Verified).")
                return True
            else:
                print(f"[WARN] Handshake Mismatch: Received {response.hex() if response else 'None'}")
                return True  # Proceeding anyway for debug
                
        except Exception as e:
            print(f"[ERROR] Serial Link Failure: {e}")
            return False

    def send_pulse(self, signal):
        """
        Receives a raw byte (int like 0xF0) from LogicEngine
        and sends it directly to the Arduino.
        """
        if self.ser and self.ser.is_open:
            if isinstance(signal, str) and len(signal) == 1:
                self.ser.write(bytes([ord(signal)]))
                print(f"[SERIAL] Sent byte: 0x{ord(signal):02X}")
            elif isinstance(signal, int):
                self.ser.write(bytes([signal]))
                print(f"[SERIAL] Sent byte: 0x{signal:02X}")
            else:
                print(f"[SERIAL ERROR] Unknown signal type: {type(signal)} = {signal}")
        else:
            print("[SERIAL ERROR] Serial port not open!")

    def send_flick(self, slot_id: int, dx: int, dy: int):
        """
        Send 0xFD flick command for ground-targeted spells.
        
        Protocol: [0xFD] [slot_id] [x_high] [x_low] [y_high] [y_low]
        
        The Arduino will:
        1. Move mouse by (dx, dy) to target
        2. Press the spell key for slot_id
        3. Click to confirm ground target
        4. Move mouse back by (-dx, -dy)
        
        Args:
            slot_id: The slot byte (0x01-0x30) for the spell
            dx: Horizontal offset from screen center (can be negative)
            dy: Vertical offset from screen center (can be negative)
        """
        if not self.ser or not self.ser.is_open:
            print("[SERIAL ERROR] Serial port not open for flick!")
            return
        
        # Convert signed int16 to two bytes (big-endian)
        # Clamp to int16 range (cast to int first to handle floats)
        dx = max(-32768, min(32767, int(dx)))
        dy = max(-32768, min(32767, int(dy)))
        
        # Convert to unsigned for byte packing
        dx_unsigned = dx & 0xFFFF
        dy_unsigned = dy & 0xFFFF
        
        packet = bytes([
            0xFD,                           # Flick command
            slot_id,                        # Which spell to cast
            (dx_unsigned >> 8) & 0xFF,      # X high byte
            dx_unsigned & 0xFF,             # X low byte
            (dy_unsigned >> 8) & 0xFF,      # Y high byte
            dy_unsigned & 0xFF              # Y low byte
        ])
        
        self.ser.write(packet)
        print(f"[SERIAL] Flick: slot=0x{slot_id:02X}, dx={dx}, dy={dy}")

