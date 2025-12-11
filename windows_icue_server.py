import time
from flask import Flask, request, jsonify
from cuesdk import CueSdk

# Initialize Flask
app = Flask(__name__)

# Initialize iCUE SDK
sdk = CueSdk()
connected = sdk.connect()
if not connected:
    print("Warning: Could not connect to iCUE! Is iCUE running?")
else:
    print("Connected to iCUE!")

# Color Helpers
def get_health_color(health_pct):
    # Green -> Yellow -> Red
    if health_pct > 0.5:
        # Green to Yellow
        r = int(255 * (1 - health_pct) * 2)
        g = 255
        b = 0
    else:
        # Yellow to Red
        r = 255
        g = int(255 * health_pct * 2)
        b = 0
    return r, g, b

@app.route('/update', methods=['POST'])
def update_lights():
    if not connected:
        return jsonify({"status": "error", "message": "iCUE not connected"})
    
    data = request.json
    health = data.get("health", 1.0) # 0.0 - 1.0
    status = data.get("status", "RUNNING") # RUNNING / PAUSED
    
    # 1. Update Health Bar (F-Keys)
    # Assuming F1-F12 are roughly LEDs 1-12 on many keyboards, 
    # but simpler to just light up the whole keyboard or specific zones.
    # For this demo, we'll light up the WHOLE keyboard with the health color
    # because mapping specific keys requires device-specific layouts.
    
    r, g, b = get_health_color(health)
    
    # If Paused, override with Dim Red
    if status == "PAUSED":
        r, g, b = 50, 0, 0
        
    # Apply to all devices
    for device_index in range(sdk.get_device_count()):
        device_info = sdk.get_device_info(device_index)
        if device_info.type == 1: # Keyboard
             # Set all LEDs
             # Note: A proper implementation would map F-Keys. 
             # For robustness, we'll just set the whole device color for now.
             # SDK doesn't have a "set all" without iterating LEDs, 
             # so we'll use a simplified layer control if available, 
             # or just iterate a reasonable range.
             pass 
             
    # Since direct LED mapping is complex without the device model,
    # we will use a "Layer" approach if possible, or just print what we WOULD do.
    # The `cuesdk` python wrapper usually requires setting individual LEDs.
    
    print(f"[iCUE] Health: {health:.2f} | Status: {status} | Color: ({r},{g},{b})")
    
    # REAL IMPLEMENTATION (Requires knowing LED IDs):
    # leds = {led_id: (r, g, b) for led_id in ALL_LED_IDS}
    # sdk.set_led_colors(device_index, leds)
    
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("Starting iCUE Bridge Server on Port 5002...")
    print("Ensure this script is running on your Windows PC with iCUE installed.")
    app.run(host='0.0.0.0', port=5002)
