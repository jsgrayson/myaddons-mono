"""
Goblin AI - Automated Setup Script
Run this to install dependencies, configure the app, and install the WoW Addon.
"""
import os
import shutil
import sys
import subprocess

def print_step(msg):
    print(f"\n[+] {msg}")

def install_dependencies():
    print_step("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("Error installing dependencies. Please install manually.")

def find_wow_directory():
    print_step("Locating World of Warcraft...")
    # Common paths on Mac
    common_paths = [
        "/Applications/World of Warcraft",
        "/Users/Shared/Battle.net/World of Warcraft",
        "/Volumes/World of Warcraft"
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            print(f"Found WoW at: {path}")
            return path
            
    # Ask user if not found
    while True:
        path = input("Could not auto-detect WoW. Please enter the path to your 'World of Warcraft' folder: ").strip()
        if os.path.exists(path):
            return path
        print("Path does not exist. Try again.")

def install_addon(wow_path):
    print_step("Installing WoW Addon...")
    retail_path = os.path.join(wow_path, "_retail_")
    if not os.path.exists(retail_path):
        print("Could not find '_retail_' folder. Is this a retail installation?")
        return None

    addons_path = os.path.join(retail_path, "Interface", "AddOns", "GoblinAI")
    
    # Create directory
    if os.path.exists(addons_path):
        shutil.rmtree(addons_path)
    os.makedirs(addons_path)
    
    # Copy files
    source_dir = os.path.join(os.path.dirname(__file__), "GoblinAI")
    
    # Create .toc file content
    toc_content = """## Interface: 100200
## Title: Goblin AI
## Notes: Godlike Gold Making Automation
## Author: GoblinAI
## Version: 1.0
## SavedVariables: GoblinAIDB

Core.lua
CharacterData.lua
Scanner.lua
SavedVariablesExport.lua
Materials/InventoryTracker.lua
Materials/CraftingManager.lua
UI/OpportunityFrame.lua
UI/CraftingQueue.lua
UI/IntelligenceFrame.lua
Automation/AssistedTrader.lua
"""
    
    # Write .toc
    with open(os.path.join(addons_path, "GoblinAI.toc"), "w") as f:
        f.write(toc_content)
        
    # Copy Lua files
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".lua"):
                src_file = os.path.join(root, file)
                # Calculate relative path to keep structure
                rel_path = os.path.relpath(src_file, source_dir)
                dest_file = os.path.join(addons_path, rel_path)
                
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                shutil.copy2(src_file, dest_file)
                
    print(f"Addon installed to: {addons_path}")
    return retail_path

def configure_companion(retail_path):
    print_step("Configuring Companion App...")
    
    # Try to find account
    wtf_path = os.path.join(retail_path, "WTF", "Account")
    if os.path.exists(wtf_path):
        accounts = [d for d in os.listdir(wtf_path) if not d.startswith(".") and d != "SavedVariables"]
        if len(accounts) == 1:
            account_name = accounts[0]
        else:
            print("Found multiple accounts: " + ", ".join(accounts))
            account_name = input("Enter your Account Name (folder name in WTF/Account/): ").strip()
    else:
        account_name = input("Enter your Account Name (folder name in WTF/Account/): ").strip()
        
    full_wtf_path = os.path.join(wtf_path, account_name, "SavedVariables")
    
    # Update app.py
    app_py_path = os.path.join(os.path.dirname(__file__), "companion", "app.py")
    
    with open(app_py_path, "r") as f:
        lines = f.readlines()
        
    with open(app_py_path, "w") as f:
        for line in lines:
            if line.strip().startswith("WTF_PATH ="):
                f.write(f'WTF_PATH = "{full_wtf_path}"\n')
            else:
                f.write(line)
                
    print(f"Companion app configured to watch: {full_wtf_path}")

def main():
    print("========================================")
    print("   Goblin AI - Automated Setup Wizard   ")
    print("========================================")
    
    install_dependencies()
    
    wow_path = find_wow_directory()
    retail_path = install_addon(wow_path)
    
    if retail_path:
        configure_companion(retail_path)
        
    print("\n[SUCCESS] Setup Complete! 🚀")
    print("You can now run 'python main.py' to start the brain.")

if __name__ == "__main__":
    main()
