#!/usr/bin/env python3
"""
SkillWeaver Midnight Launcher
=============================

Unified launcher with hardware profile selection.

Usage:
  python launcher.py --mac      # MacBook M2 Pro
  python launcher.py --msi      # MSI Claw 8 AI+
  python launcher.py --right    # Samsung 57" Right Half (default)
  python launcher.py --center   # Samsung 57" Centered
  python launcher.py --left     # Samsung 57" Left Half
  python launcher.py --full     # Samsung 57" Full Screen
  python launcher.py --pbp      # Samsung 57" PBP Mode

Options:
  --sync    Sync keybinds from SavedVariables first
  --anchor  Calibrate to game window anchor before starting
"""

import os
import sys
import argparse

# Add Brain directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BRAIN_DIR = os.path.join(SCRIPT_DIR, "Brain")
sys.path.insert(0, BRAIN_DIR)


def main():
    parser = argparse.ArgumentParser(
        description="SkillWeaver Midnight Engine Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Hardware Profiles:
  --mac      MacBook M2 Pro (Retina 2x)
  --msi      MSI Claw 8 AI+ Handheld
  --right    Samsung 57" Right Half [DEFAULT]
  --center   Samsung 57" Centered Window
  --left     Samsung 57" Left Half
  --full     Samsung 57" Full 7680px
  --pbp      Samsung 57" PBP Mode (Single 4K)
        """
    )
    
    # Hardware profile flags (mutually exclusive)
    hw_group = parser.add_mutually_exclusive_group()
    hw_group.add_argument("--mac", action="store_true", help="MacBook M2 Pro")
    hw_group.add_argument("--msi", action="store_true", help="MSI Claw 8 AI+")
    hw_group.add_argument("--right", action="store_true", help="Samsung 57\" Right Half")
    hw_group.add_argument("--center", action="store_true", help="Samsung 57\" Centered")
    hw_group.add_argument("--left", action="store_true", help="Samsung 57\" Left Half")
    hw_group.add_argument("--full", action="store_true", help="Samsung 57\" Full Screen")
    hw_group.add_argument("--pbp", action="store_true", help="Samsung 57\" PBP Mode")
    
    # Additional options
    parser.add_argument("--sync", action="store_true", help="Sync keybinds first")
    parser.add_argument("--anchor", action="store_true", help="Calibrate to window anchor")
    parser.add_argument("--dry-run", action="store_true", help="Test mode (no keypresses)")
    
    args = parser.parse_args()
    
    # Determine profile
    profile_map = {
        "mac": "MAC_M2_PRO",
        "msi": "MSI_CLAW_8_AI",
        "right": "SAMSUNG_57_RIGHT_HALF",
        "center": "SAMSUNG_57_CENTERED",
        "left": "SAMSUNG_57_LEFT_HALF",
        "full": "SAMSUNG_57_FULL",
        "pbp": "SAMSUNG_57_PBP"
    }
    
    selected_profile = "SAMSUNG_57_RIGHT_HALF"  # Default
    for flag, profile in profile_map.items():
        if getattr(args, flag, False):
            selected_profile = profile
            break
    
    # Banner
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║           SkillWeaver Midnight Engine Launcher               ║")
    print("║                    Master Tier Combat AI                     ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    
    # Import and configure
    from HardwareConfig import set_profile, print_profile_info, calibrate_to_window
    
    set_profile(selected_profile)
    print_profile_info()
    
    # Optional keybind sync
    if args.sync:
        print("\n📋 Syncing keybinds from SavedVariables...")
        sync_path = os.path.join(SCRIPT_DIR, "tools", "dbc_sync.py")
        if os.path.exists(sync_path):
            os.system(f"python3 {sync_path}")
        else:
            print("   ⚠️  dbc_sync.py not found")
        print()
    
    # Optional anchor calibration
    if args.anchor:
        print("🔍 Calibrating to game window anchor...")
        offset = calibrate_to_window()
        if offset != (0, 0):
            print(f"   ✅ Anchor offset: {offset}")
        print()
    
    # Launch engine
    print("🚀 Launching SkillWeaver Engine...")
    print("   Hold '2' to activate rotation")
    print("   Press Ctrl+C to exit\n")
    print("═" * 60 + "\n")
    
    # Import and run main engine
    os.chdir(BRAIN_DIR)
    
    if args.dry_run:
        print("[DRY-RUN] Engine would start here")
    else:
        from main import SkillWeaverEngine
        engine = SkillWeaverEngine()
        engine.run()


if __name__ == "__main__":
    # v6.0: NO SUDO - Run as user to preserve vision
    main()

