import serial
import time
from typing import Optional

class SerialLink:
    def __init__(self, port: str = "/dev/cu.usbmodemHIDPC1", baudrate: int = 250000):
        self.port = port
        self.baudrate = baudrate
        self.ser: Optional[serial.Serial] = None

    def connect(self) -> bool:
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2) 
            
            # Simple Handshake (Send 0xFF, Expect 0xAA)
            self.ser.write(bytes([0xFF])) 
            time.sleep(0.1)
            
            response = self.ser.read(1)
            # The Arduino code you uploaded sends 0xAA on 0xFF
            if response == b'\xaa':
                print("[SUCCESS] Hardware Linked.")
                return True
            else:
                print(f"[WARN] Handshake Mismatch: Received {response.hex() if response else 'None'}")
                return True # Proceeding anyway for debug
                
        except Exception as e:
            print(f"[ERROR] Serial Link Failure: {e}")
            return False

    def send_pulse(self, signal: str):
        """
        Receives a raw byte char (e.g. '\x01') from LogicEngine
        and sends it directly to the Arduino.
        """
        if self.ser and self.ser.is_open:
            if isinstance(signal, str) and len(signal) == 1:
                self.ser.write(bytes([ord(signal)]))
            elif isinstance(signal, int):
                self.ser.write(bytes([signal]))
