import mss
import numpy as np
import json
import os
import sys
import time
import random
import glob
import Quartz  # Required: pip install pyobjc-framework-Quartz
from modules.serial_link import SerialLink as ArduinoBridge
from modules.vision import ScreenScanner
from ConditionEngine import ConditionEngine
from StateEngine import StateEngine
from HardwareConfig import get_profile
import signal
import threading
import queue

# Global reference for signal handling
_ENGINE_INSTANCE = None



# v6.0 QUARTZ ENGINE - NO SUDO REQUIRED
# Uses Quartz Event Services for key suppression instead of HID

# Calibration (Adjusted for ~5.5% signal loss: 218 * 0.95 ≈ 207)
DIVISOR_UNIVERSAL = 207.0

# Humanization Constants (Gaussian Distribution)
REACTION_MEAN = 0.08  # Average reaction time (80ms)
REACTION_STD = 0.02   # Standard Deviation (20ms)
INPUT_JITTER = 0.01   # Base hardware jitter (10ms)

# KEY_MAP: Byte codes matching Arduino firmware (ARDUINO_FIRMWARE.md)
# 8 base keys: F13, F16-F19, HOME, END, DELETE
# Bar 1: Base (0x01-0x08)
# Bar 2: Shift (0x09-0x10)
# Bar 3: Ctrl (0x11-0x18)
# Bar 4: Alt (0x19-0x20)
KEY_MAP = {
    # Bar 1: 0x01 - 0x08
    "F13": 0x01, "F16": 0x02, "F17": 0x03, "F18": 0x04,
    "F19": 0x05, "HOME": 0x06, "END": 0x07, "DELETE": 0x08,
    
    # Bar 2: 0x09 - 0x10
    "SHIFT+F13": 0x09, "SHIFT+F16": 0x0A, "SHIFT+F17": 0x0B, "SHIFT+F18": 0x0C,
    "SHIFT+F19": 0x0D, "SHIFT+HOME": 0x0E, "SHIFT+END": 0x0F, "SHIFT+DELETE": 0x10,
    
    # Bar 3: 0x11 - 0x18
    "CTRL+F13": 0x11, "CTRL+F16": 0x12, "CTRL+F17": 0x13, "CTRL+F18": 0x14,
    "CTRL+F19": 0x15, "CTRL+HOME": 0x16, "CTRL+END": 0x17, "CTRL+DELETE": 0x18,
    
    # Bar 4: 0x19 - 0x20
    "ALT+F13": 0x19, "ALT+F16": 0x1A, "ALT+F17": 0x1B, "ALT+F18": 0x1C,
    "ALT+F19": 0x1D, "ALT+HOME": 0x1E, "ALT+END": 0x1F, "ALT+DELETE": 0x20,
    
    "TAB": 0x21,
    "SHIFT+TAB": 0x22
}


def safe_pixel_init() -> bool:
    """Test screen capture before starting."""
    print(">>> [SECURITY] Testing Screen Capture...")
    try:
        with mss.mss() as sct:
            sct.grab({"top": 0, "left": 0, "width": 1, "height": 1})
            print(">>> [SECURITY] Screen Access Granted ✓")
            return True
    except Exception as e:
        print(f"!!! [HALT] Screen Recording Denied: {e}")
        print("!!! Add Terminal to System Settings > Privacy > Screen Recording")
        return False


class SkillWeaverEngine:
    def __init__(self):
        profile = get_profile()
        self.sct = mss.mss()
        self.bridge = ArduinoBridge()
        self.vision = ScreenScanner()  # Vision for ground targeting
        self.bridge_connected = False
        self.active_spec = None
        self.rotation = {}
        
        # Calibration from HardwareConfig
        self.scale = profile["SCREEN_SCALE"]
        self.uplink_y = profile["START_Y"]
        self.uplink_x = profile["START_X"]
        
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.spec_dir = os.path.join(self.base_dir, "data", "specs")
        self.state_engine = StateEngine(self.base_dir)

        # GCD / Casting State
        self.gcd_until = 0
        self.channel_until = 0
        self.last_action_name = ""
        self.last_action_name = ""
        self.lock = threading.Lock()

        # GCD / Casting State (Using perf_counter for precision)
        self._gcd_until = 0
        self._channel_until = 0

        # Execution Queue (Worker prevents blocking the Quartz callback)
        self.cmd_queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self._execution_worker, daemon=True)
        self.worker_thread.start()

    def _execution_worker(self):
        """Background thread to handle serial pulses and humanization."""
        while True:
            try:
                task = self.cmd_queue.get()
                if not task: break
                
                now = time.time()
                action = task['action']
                byte = task['byte']
                delay = task['delay']
                flick_data = task.get('flick')

                # Humanized reaction wait
                if delay > 0:
                    time.sleep(delay)

                if flick_data:
                    dx, dy = flick_data
                    self.bridge.send_flick(byte, dx, dy)
                    print(f"[TX] {action} (AIMED) | dx={dx}, dy={dy}")
                else:
                    self.bridge.send_pulse(byte)
                    power_val = task.get('power', 0)
                    print(f"[TX] {action} | Res:{power_val:.0f}% | Delay:{delay*1000:.0f}ms")
                
                self.cmd_queue.task_done()
            except Exception as e:
                print(f"[ERROR] Worker Thread: {e}")
                import traceback
                traceback.print_exc()

    def decode_px(self, data_row, idx):
        # PROTOCOL v4: Differential math for Retina calibration
        pos = int(idx)
        if pos >= len(data_row): return 0.0
        px = data_row[pos] # BGR
        diff = max(0, int(px[0]) - int(px[2]))
        return max(0, min(255, (diff / DIVISOR_UNIVERSAL) * 255.0))

    def get_game_state(self):
        """Vision: Triggered when '2' is pressed."""
        
        def capture(y):
            # Capture more pixels to reach the Plater Anchor at P16/P32
            snap = np.array(self.sct.grab({
                "top": int(y), 
                "left": int(self.uplink_x), 
                "width": 256, 
                "height": 1
            }))
            return snap[0]

        row = capture(self.uplink_y)
        
        # HEARTBEAT RE-SYNC (P0 is the blue heartbeat anchor)
        if self.decode_px(row, 0) < 30: # If P0 is blank, we are likely shifted
            for offset in [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5]:
                test_row = capture(self.uplink_y + offset)
                if self.decode_px(test_row, 0) > 40: 
                    row = test_row
                    print(f"[RE-SYNC] Found heartbeat at Y offset {offset}")
                    break

        
        state = {
            "hash": self.decode_px(row, 1),
            "combat": self.decode_px(row, 2) > 128,
            "hp": min(100.0, self.decode_px(row, 3) / 255.0 * 100),
            "thp": min(100.0, self.decode_px(row, 4) / 255.0 * 100),
            "power": min(100.0, self.decode_px(row, 7) / 255.0 * 100),
            "sec": int(round(self.decode_px(row, 8) / 25.0)),
            "target_valid": self.decode_px(row, 5) > 128,
            "range": int(self.decode_px(row, 6) / 4.25),
            "interruptible": self.decode_px(row, 18) > 128,
            "stealthed": self.decode_px(row, 19) > 128,
            "nearby_enemies_count": int(self.decode_px(row, 9) / 25.0),
            # Pure Pixel Dots
            "dots": [self.decode_px(row, i) / 10.0 for i in range(11, 26)],
            "target_dot_remaining": self.decode_px(row, 11) / 10.0,
            "plater_anchor": self.decode_px(row, 16) > 200, 
            "enemies_missing_dots": int(self.decode_px(row, 20) / 25.0),
            "should_tab_target": self.decode_px(row, 21) > 128,
            "_raw_width": len(row),
            "_raw_row": row
        }

        if state["hash"] < 1:
            print(f"[DEBUG] Blind reading from Y={self.uplink_y} | Buf:{len(row)}px")
            samples = [row[i][:3].tolist() for i in range(min(len(row), 40))]
            print(f"[DEBUG] First 40 pixels (BGR): {samples}")
            
        return state

    def tap_callback(self, proxy, event_type, event, refcon):
        """Quartz Handler: Runs as User, Hears '2', and SUPPRESSES."""
        try:
            keycode = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
            
            if keycode == 19:
                # 1. ATOMIC LOCK & GCD CHECK
                with self.lock:
                    now = time.perf_counter()
                    gcd_remaining = self._gcd_until - now
                    if now < self._gcd_until:
                        print(f"[GCD] BLOCKED - {gcd_remaining:.2f}s remaining")
                        return None
                    if now < self._channel_until:
                        return None
                    
                    # PROVISIONALLY set a short busy lock to prevent 
                    # overlapping taps while we read the screen
                    self._gcd_until = now + 0.3 
                    print(f"[GCD] ALLOWED - setting provisional lock")
                
                # SUPPRESS IMMEDIATELY
                try:
                    state = self.get_game_state()
                    dots = state.get('dots', [0,0,0])

                    # Log state for debugging
                    print(f"\n[BRAIN] Spec:{state['hash']:.0f} | HP:{state['hp']:.0f}% | THP:{state['thp']:.0f}% | Anchor:{'YES' if state['plater_anchor'] else 'no'} | Target:{'VALID' if state['target_valid'] else 'absent'}")
                    print(f"[DOTS] VT:{dots[0]:.1f}s | SWP:{dots[1]:.1f}s | DP:{dots[2]:.1f}s")
                    print(f"[CLEAVE] Missing:{state.get('enemies_missing_dots', 0)} | Plates:{int(self.decode_px(state['_raw_row'], 21) / 25)}")
                    
                    if dots[0] == 0:
                        # Extra diagnostics: Show the first 32 physical pixels
                        row = state['_raw_row']
                        samples = []
                        for i in range(32):
                            val = self.decode_px(row, i)
                            samples.append(f"{i}:{val:.0f}")
                        print(f"[DEBUG] physical_strip: {' | '.join(samples)}")
                    
                    # 1. Dynamic spec loading
                    if int(state['hash'] + 0.5) != self.active_spec:
                        self.load_rotation(state['hash'])
                    
                    # 2. CLEAVE / MULTI-DOT (DISABLED - was spamming TAB)
                    # TODO: Re-enable when TAB logic is fixed
                    # now_tab = time.perf_counter()
                    # tab_ready = (now_tab - getattr(self, '_last_tab_time', 0)) > 2.0
                    # if tab_ready and self.active_spec and self.state_engine.check_cleave_snap_back(state, self.active_spec):
                    #     ...
                    pass  # Cleave disabled

                    if self.active_spec:
                        optimal = self.state_engine.get_optimal_action(state)
                        
                        if optimal and self.bridge_connected:
                            byte = KEY_MAP.get(optimal.get('key', '').upper())
                            if byte:
                                with self.lock:
                                    now = time.perf_counter()
                                    lock_padding = random.uniform(0.05, 0.15)
                                    
                                    # SET REAL LOCKS
                                    gcd_dur = 1.4 + lock_padding
                                    self._gcd_until = now + gcd_dur
                                    self.last_action_name = optimal.get('action', '') # Moved here
                                    
                                    cast_dur = (optimal.get('cast_time', 0) or optimal.get('channel_time', 0))
                                    if cast_dur > 0:
                                        self._channel_until = now + cast_dur + lock_padding
                                    elif optimal.get('is_channel', False):
                                        self._channel_until = now + 2.5 + lock_padding
                                    else:
                                        self._channel_until = 0

                                # Queue for worker
                                delay = max(0, random.normalvariate(REACTION_MEAN, REACTION_STD)) + INPUT_JITTER
                                
                                flick_data = None
                                if optimal.get('requires_aim'):
                                    flick_data = self.vision.get_flick_offset(state.get('range', 10))

                                self.cmd_queue.put({
                                    'action': optimal['action'],
                                    'byte': byte,
                                    'delay': delay,
                                    'flick': flick_data,
                                    'power': state['power']
                                })
                            else:
                                print(f"[WARN] No key mapping for: {optimal.get('key')}")
                                with self.lock: self._gcd_until = 0 # Reset provisional lock if no action
                        elif not self.bridge_connected:
                            print("[WARN] Arduino not connected")
                            with self.lock: self._gcd_until = 0 # Reset provisional lock if no action
                    else:
                        if state['hash'] < 1:
                            print(f"[WARN] Brain is blind - reading zeros. Check WoW window focus.")
                        else:
                            print(f"[WARN] No spec loaded for hash {state['hash']:.0f}")
                        with self.lock: self._gcd_until = 0 # Reset provisional lock if no action
                
                except Exception as e:
                    with self.lock: self._gcd_until = 0
                    print(f"[ERROR] Logic internal failure: {e}")
                    import traceback
                    traceback.print_exc()

                return None # ALWAYS suppress '2' once detected
                
        except Exception as e:
            print(f"[ERROR] Global Callback failure: {e}")
            
        return event

    def load_rotation(self, hash_id):
        """Dynamic rotation loader."""
        h_int = int(hash_id + 0.5)
        pattern = os.path.join(self.spec_dir, f"{h_int}_*.json")
        matches = glob.glob(pattern)
        if matches:
            with open(matches[0], 'r') as f:
                data = json.load(f)
                self.active_spec = h_int
                self.state_engine.load_spec(h_int, data)
                print(f"\n[SYSTEM] Spec {h_int} Loaded.")

    def stop(self):
        """Signals the Quartz loop to stop."""
        print("\n[STOP] Stopping Quartz RunLoop...")
        Quartz.CFRunLoopStop(Quartz.CFRunLoopGetCurrent())

    def run(self):
        global _ENGINE_INSTANCE
        _ENGINE_INSTANCE = self
        
        print("\n" + "=" * 50)
        print("    SKILLWEAVER v6.0 (QUARTZ - NO SUDO)")
        print("=" * 50)
        
        self.bridge_connected = self.bridge.connect()
        if not self.bridge_connected:
            print("!!! [WARNING] Arduino not connected - running in monitor mode")
        
        # Signal Setup for Ctrl+C
        def signal_handler(sig, frame):
            if _ENGINE_INSTANCE:
                _ENGINE_INSTANCE.stop()
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Create Quartz Tap (User Session, No Sudo)
        tap = Quartz.CGEventTapCreate(
            Quartz.kCGSessionEventTap,
            Quartz.kCGHeadInsertEventTap,
            Quartz.kCGEventTapOptionDefault,
            Quartz.CGEventMaskBit(Quartz.kCGEventKeyDown),
            self.tap_callback,
            None
        )

        if not tap:
            print("\n!!! [CRITICAL] Quartz Event Tap failed!")
            print("!!! Enable these in System Settings > Privacy & Security:")
            print("!!!   - Accessibility (for Terminal)")
            print("!!!   - Input Monitoring (for Terminal)")
            sys.exit(1)

        loop_source = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
        Quartz.CFRunLoopAddSource(Quartz.CFRunLoopGetCurrent(), loop_source, Quartz.kCFRunLoopDefaultMode)
        Quartz.CGEventTapEnable(tap, True)
        
        print("\n[SYSTEM] Key Suppression Active")
        print("[SYSTEM] Press '2' to engage rotation")
        print("[SYSTEM] Press Ctrl+C to exit\n")
        
        # Start Loop
        Quartz.CFRunLoopRun()
        print("[STOP] Engine halted.")


if __name__ == "__main__":
    if safe_pixel_init():
        SkillWeaverEngine().run()
