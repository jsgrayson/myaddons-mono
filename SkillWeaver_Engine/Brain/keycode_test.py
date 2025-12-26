#!/usr/bin/env python3
"""
keycode_test.py - Suppresses '2' and prints debug info
"""

import Quartz

def callback(proxy, event_type, event, refcon):
    keycode = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
    
    # Keycode 19 = '2' on number row
    if keycode == 19:
        print(f"[SUPPRESSED] '2' key detected (keycode {keycode})")
        return None  # SUPPRESS - WoW won't see it
    
    print(f"[PASS] Keycode: {keycode}")
    return event

tap = Quartz.CGEventTapCreate(
    Quartz.kCGSessionEventTap,
    Quartz.kCGHeadInsertEventTap,
    Quartz.kCGEventTapOptionDefault,
    Quartz.CGEventMaskBit(Quartz.kCGEventKeyDown),
    callback, None
)

if tap:
    print("Tap created! Press '2' - it should be SUPPRESSED")
    print("Press other keys to see their keycodes")
    print("Press Ctrl+C to exit\n")
    source = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
    Quartz.CFRunLoopAddSource(Quartz.CFRunLoopGetCurrent(), source, Quartz.kCFRunLoopDefaultMode)
    Quartz.CGEventTapEnable(tap, True)
    try:
        Quartz.CFRunLoopRun()
    except KeyboardInterrupt:
        print("\nDone.")
else:
    print("!!! TAP FAILED - Check permissions!")
