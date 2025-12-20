import time
from pynput import keyboard

# Data structure to hold intervals
intervals = []
last_time = time.time()

def on_press(key):
    global last_time
    current_time = time.time()
    # Calculate delay since last keypress in milliseconds
    delay = (current_time - last_time) * 1000
    intervals.append(round(delay, 2))
    last_time = current_time
    
    # Stop recording after 500 inputs or by pressing 'ESC'
    if key == keyboard.Key.esc or len(intervals) >= 500:
        return False

print("Recording started... Play your rotation naturally.")
print("Press ESC to stop early.")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

# Output the raw data to be fed back to Gemini
print("\n--- BIOMETRIC DATA START ---")
print(intervals)
print("--- BIOMETRIC DATA END ---")
print(f"Captured {len(intervals)} data points.")
