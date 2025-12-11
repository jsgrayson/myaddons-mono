import platform

# Try to import cuesdk, but don't crash if missing (e.g. on Mac)
try:
    from cuesdk import CueSdk
    CUESDK_AVAILABLE = True
except ImportError:
    CUESDK_AVAILABLE = False

class iCUEManager:
    def __init__(self):
        self.sdk = None
        self.connected = False
        self.enabled = False
        
        # Only attempt on Windows
        if platform.system() == "Windows" and CUESDK_AVAILABLE:
            self.sdk = CueSdk()
            self.connected = self.sdk.connect()
            if self.connected:
                print(f"[iCUE] Connected. Found {self.sdk.get_device_count()} devices.")
                for i in range(self.sdk.get_device_count()):
                    info = self.sdk.get_device_info(i)
                    print(f"  - Device {i}: {info.model}")
                self.enabled = True
            else:
                print("[iCUE] Failed to connect. Is iCUE running?")
        else:
            print("[iCUE] Disabled (Not on Windows or SDK missing).")

    def update(self, health_pct, status, is_casting=False):
        if not self.enabled or not self.connected:
            return

        # 1. Determine Color based on Health
        # Green -> Yellow -> Red
        if health_pct > 0.5:
            r = int(255 * (1 - health_pct) * 2)
            g = 255
            b = 0
        else:
            r = 255
            g = int(255 * health_pct * 2)
            b = 0
            
        # 2. Status Override
        if status == "PAUSED":
            r, g, b = 50, 0, 0 # Dim Red
        elif is_casting:
            r, g, b = 0, 0, 255 # Blue flash for action

        # 3. Apply to Devices
        # Ideally we map F-Keys, but for simplicity we set the whole device
        # or use available SDK methods to set colors.
        # Note: cuesdk requires setting specific LEDs. 
        # We will iterate a generic range for now as a "best effort" 
        # to light up keyboards/mice without complex device mapping.
        
        try:
        try:
            for device_index in range(self.sdk.get_device_count()):
                device_info = self.sdk.get_device_info(device_index)
                # Get LED positions to know which LEDs exist
                led_positions = self.sdk.get_led_positions_by_device_index(device_index)
                if not led_positions:
                    continue
                
                # Create a color map for all LEDs
                # cuesdk expects a dict {led_id: (r, g, b)}
                led_colors = {}
                for led_id in led_positions:
                    led_colors[led_id] = (r, g, b)
                
                # Apply colors
                self.sdk.set_led_colors(device_index, led_colors)
                
        except Exception as e:
            print(f"[iCUE] Error updating lights: {e}")

# Singleton
icue = iCUEManager()
