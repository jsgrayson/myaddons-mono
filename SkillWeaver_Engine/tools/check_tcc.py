#!/usr/bin/env python3
"""
TCC Permission Checker - macOS Privacy Database Inspector

Checks which apps have Screen Recording, Accessibility, and Input Monitoring
permissions. Run with sudo for full access.
"""

import subprocess
import sqlite3
import os

def check_tcc_permissions():
    """Query the TCC database for app permissions."""
    
    print("\n" + "=" * 60)
    print("       macOS TCC Permission Checker")
    print("=" * 60 + "\n")
    
    # TCC database location
    tcc_db = os.path.expanduser("~/Library/Application Support/com.apple.TCC/TCC.db")
    system_tcc_db = "/Library/Application Support/com.apple.TCC/TCC.db"
    
    # Services we care about
    services = {
        "kTCCServiceScreenCapture": "Screen Recording",
        "kTCCServiceAccessibility": "Accessibility",
        "kTCCServiceListenEvent": "Input Monitoring",
        "kTCCServiceMicrophone": "Microphone",
    }
    
    def query_db(db_path, label):
        if not os.path.exists(db_path):
            print(f"[SKIP] {label}: Database not found")
            return
        
        print(f"\n[{label}]")
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            for service_id, service_name in services.items():
                cursor.execute("""
                    SELECT client, auth_value 
                    FROM access 
                    WHERE service = ?
                """, (service_id,))
                
                results = cursor.fetchall()
                if results:
                    print(f"\n  {service_name}:")
                    for client, auth in results:
                        status = "✓ ALLOWED" if auth == 2 else ("○ DENIED" if auth == 0 else f"? ({auth})")
                        # Shorten client path for readability
                        client_short = client.split("/")[-1] if "/" in client else client
                        print(f"    {status}: {client_short}")
            
            conn.close()
        except Exception as e:
            print(f"  Error reading database: {e}")
    
    # Check user database
    query_db(tcc_db, "User Permissions")
    
    # Check system database (needs sudo)
    if os.geteuid() == 0:
        query_db(system_tcc_db, "System Permissions")
    else:
        print("\n[TIP] Run with sudo to see system-level permissions")
    
    # Quick checks
    print("\n" + "=" * 60)
    print("Quick Fixes:")
    print("=" * 60)
    print("""
1. Screen Recording:
   System Settings > Privacy > Screen & System Audio Recording
   Add: Terminal AND /usr/local/bin/python3

2. Accessibility:
   System Settings > Privacy > Accessibility
   Add: Terminal

3. Input Monitoring:
   System Settings > Privacy > Input Monitoring
   Add: Terminal

4. To reset all permissions for Terminal:
   tccutil reset All com.apple.Terminal
""")


if __name__ == "__main__":
    check_tcc_permissions()
