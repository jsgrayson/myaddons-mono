#!/usr/bin/env python3
"""
Holocron Suite - Deployment Verification
"""

import os
import subprocess
import time

GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

def check_file(path, name):
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"  {GREEN}✓{NC} {name} ({size:,} bytes)")
        return True
    else:
        print(f"  {RED}✗{NC} {name} - NOT FOUND")
        return False

def check_port(port, service):
    try:
        result = subprocess.run(
            f"lsof -i :{port} 2>/dev/null | grep LISTEN",
            shell=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(f"  {GREEN}✓{NC} {service} running on port {port}")
            return True
        else:
            print(f"  {YELLOW}⚠{NC} {service} not running on port {port}")
            return False
    except:
        return False

def main():
    print("=" * 70)
    print(f"{BLUE}HOLOCRON SUITE - DEPLOYMENT VERIFICATION{NC}")
    print("=" * 70)
    
    # Check WoW installation
    print(f"\n{BLUE}📍 WoW Installation{NC}")
    print("-" * 70)
    wow_path = "/Applications/World of Warcraft/_retail_"
    if os.path.exists(wow_path):
        print(f"  {GREEN}✓{NC} WoW installed at {wow_path}")
    else:
        print(f"  {RED}✗{NC} WoW not found!")
        return
    
    # Check addons
    print(f"\n{BLUE}🎮 Installed Addons{NC}")
    print("-" * 70)
    addons_path = os.path.join(wow_path, "Interface/AddOns")
    
    addons = {
        'PetWeaver': 'PetWeaver/PetWeaver.toc',
        'DeepPockets': 'DeepPockets/DeepPockets.toc',
        'HolocronViewer': 'HolocronViewer/HolocronViewer.toc',
        'SkillWeaver': 'SkillWeaver/SkillWeaver.toc'
    }
    
    addon_status = {}
    for name, toc_file in addons.items():
        path = os.path.join(addons_path, toc_file)
        addon_status[name] = check_file(path, name)
    
    # Check SavedVariables
    print(f"\n{BLUE}💾 SavedVariables{NC}")
    print("-" * 70)
    saved_vars = "/Applications/World of Warcraft/_retail_/WTF/Account/NIGHTHWK77/SavedVariables"
    
    vars_to_check = {
        'DeepPockets.lua': 'DeepPockets',
        'PetWeaver.lua': 'PetWeaver',
        'HolocronViewer.lua': 'HolocronViewer',
        'PetTracker.lua': 'PetTracker',
        'DataStore_Reputations.lua': 'DataStore (Reputations)',
        'SavedInstances.lua': 'SavedInstances'
    }
    
    data_status = {}
    for filename, name in vars_to_check.items():
        path = os.path.join(saved_vars, filename)
        data_status[name] = check_file(path, name)
    
    # Check web services
    print(f"\n{BLUE}🌐 Web Services{NC}")
    print("-" * 70)
    
    backend_running = check_port(5005, "Backend API")
    frontend_running = check_port(3000, "Frontend")
    
    # Check project files
    print(f"\n{BLUE}📂 Project Files{NC}")
    print("-" * 70)
    
    project_files = {
        '/Users/jgrayson/Documents/holocron/server.py': 'Backend Server',
        '/Users/jgrayson/Documents/holocron/frontend/package.json': 'Frontend Package',
        '/Users/jgrayson/Documents/holocron/deploy_all.sh': 'Deployment Script',
        '/Users/jgrayson/Documents/holocron/sync_addon_data.py': 'Sync Script',
        '/Users/jgrayson/Documents/holocron/FEATURES.md': 'Documentation'
    }
    
    for path, name in project_files.items():
        check_file(path, name)
    
    # Summary
    print(f"\n{BLUE}📊 Summary{NC}")
    print("=" * 70)
    
    total_addons = len(addons)
    installed_addons = sum(addon_status.values())
    
    total_data = len(vars_to_check)
    available_data = sum(data_status.values())
    
    print(f"  Addons: {installed_addons}/{total_addons} installed")
    print(f"  Data Files: {available_data}/{total_data} available")
    print(f"  Backend API: {'Running' if backend_running else 'Not running'}")
    print(f"  Frontend: {'Running' if frontend_running else 'Not running'}")
    
    # Overall status
    print("\n" + "=" * 70)
    
    all_addons_ok = installed_addons == total_addons
    services_ok = backend_running and frontend_running
    
    if all_addons_ok and services_ok:
        print(f"{GREEN}✅ SYSTEM READY!{NC}")
        print(f"\n{BLUE}Next steps:{NC}")
        print("  1. Launch World of Warcraft")
        print("  2. Type /reload in-game")
        print("  3. Open http://localhost:3000 in browser")
    elif all_addons_ok:
        print(f"{YELLOW}⚠️ ADDONS READY, SERVICES NOT RUNNING{NC}")
        print(f"\n{BLUE}To start services:{NC}")
        print("  ./deploy_all.sh")
    else:
        print(f"{RED}❌ DEPLOYMENT INCOMPLETE{NC}")
        print(f"\n{BLUE}To deploy:{NC}")
        print("  ./deploy_all.sh")
    
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
