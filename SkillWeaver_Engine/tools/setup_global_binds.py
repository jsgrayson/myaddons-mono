#!/usr/bin/env python3
"""
setup_global_binds.py - Account-Wide F13-F24 Hardware Bridge Setup

Writes F13-F24 bindings to WoW's global account file so every character
inherits the same hardware bridge mapping:
  - Bar 6 (F13-F24)     -> MultiBar5Button1-12
  - Bar 7 (SHIFT+F13-F24) -> MultiBar6Button1-12  
  - Bar 8 (CTRL+F13-F24)  -> MultiBar7Button1-12
"""

import os
import sys

# Default WoW path on Mac
DEFAULT_WOW_PATH = "/Applications/World of Warcraft"


def setup_global_hardware_bridge(wow_path: str, account_id: str):
    """
    Writes the F13-F24 bridge to the global account file.
    Every character will inherit these by default.
    """
    # Target the GLOBAL account binding file
    global_file = os.path.join(
        wow_path, "_retail_", "WTF", "Account", account_id, "bindings-cache.wtf"
    )

    # Check if path exists
    account_dir = os.path.dirname(global_file)
    if not os.path.exists(account_dir):
        print(f"[!] Account directory not found: {account_dir}")
        print("[!] Available accounts:")
        wtf_accounts = os.path.join(wow_path, "_retail_", "WTF", "Account")
        if os.path.exists(wtf_accounts):
            for d in os.listdir(wtf_accounts):
                if os.path.isdir(os.path.join(wtf_accounts, d)):
                    print(f"    - {d}")
        return False

    # Bars 6, 7, and 8 mapping logic
    mapping = {
        "": "MultiBar5Button",       # Bar 6 -> F13-F24
        "SHIFT-": "MultiBar6Button", # Bar 7 -> SHIFT+F13-F24
        "CTRL-": "MultiBar7Button"   # Bar 8 -> CTRL+F13-F24
    }

    # BINDINGMODE 0 = Account-wide / Out-of-combat default
    content = ["BINDINGMODE 0"]
    
    for mod, bar in mapping.items():
        for i in range(1, 13):
            f_key = i + 12  # F13 through F24
            # Syntax: bind [KEY] CLICK [UI_BUTTON]:LeftButton
            content.append(f"bind {mod}F{f_key} CLICK {bar}{i}:LeftButton")

    # Backup existing file
    if os.path.exists(global_file):
        backup = global_file + ".bak"
        os.rename(global_file, backup)
        print(f"[*] Backed up existing bindings to: {os.path.basename(backup)}")

    # Write the file
    try:
        with open(global_file, "w") as f:
            f.write("\n".join(content))
        print(f"[*] Global Master Bridge synced for Account: {account_id}")
        print(f"[*] File: {global_file}")
        print(f"[*] Wrote {len(content)} bindings (Bars 6, 7, 8 -> F13-F24)")
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False


def list_accounts(wow_path: str):
    """List all available WoW accounts."""
    wtf_accounts = os.path.join(wow_path, "_retail_", "WTF", "Account")
    if not os.path.exists(wtf_accounts):
        print(f"[!] WTF folder not found: {wtf_accounts}")
        return []
    
    accounts = []
    for d in os.listdir(wtf_accounts):
        if os.path.isdir(os.path.join(wtf_accounts, d)) and d != "SavedVariables":
            accounts.append(d)
    return accounts


def main():
    wow_path = DEFAULT_WOW_PATH
    
    if len(sys.argv) > 1:
        account_id = sys.argv[1]
    else:
        # List accounts and prompt
        accounts = list_accounts(wow_path)
        if not accounts:
            print("[!] No accounts found")
            return
        
        print("\nAvailable WoW Accounts:")
        for i, acc in enumerate(accounts, 1):
            print(f"  {i}. {acc}")
        
        choice = input("\nSelect account number (or enter account ID): ").strip()
        
        try:
            idx = int(choice) - 1
            account_id = accounts[idx]
        except (ValueError, IndexError):
            account_id = choice
    
    print(f"\n[*] Setting up hardware bridge for: {account_id}")
    setup_global_hardware_bridge(wow_path, account_id)


if __name__ == "__main__":
    main()
