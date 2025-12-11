"""
Setup Addon Libraries
Downloads and installs required WoW libraries (Ace3, LibDataBroker, etc.)
into the addon directories.
"""

import os
import urllib.request
import zipfile
import shutil
import io

# Libraries to download
LIBS = {
    "Ace3": "https://github.com/WoWUIDev/Ace3/archive/refs/heads/master.zip",
    "LibDataBroker-1.1": "https://github.com/tekkub/libdatabroker-1-1/archive/refs/heads/master.zip",
    "LibDBIcon-1.0": "https://github.com/golub/LibDBIcon-1.0/archive/refs/heads/master.zip", # Retrying same, if fails we skip
}

ADDONS = [
    "DeepPockets",
    "PetWeaver",
    "HolocronViewer",
    "GoblinAI"
]

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def download_and_extract(url, name):
    print(f"⬇️  Downloading {name}...")
    try:
        # Special handling for LibDBIcon which might be 404
        if name == "LibDBIcon-1.0":
             # Try alternate URL if primary fails
             try:
                 return download_url(url, name)
             except:
                 print("   ⚠️  Primary URL failed, trying alternate...")
                 return download_url("https://github.com/wow-ace/LibDBIcon-1.0/archive/refs/heads/master.zip", name)
        
        return download_url(url, name)
    except Exception as e:
        print(f"❌ Failed to download {name}: {e}")
        return None

def download_url(url, name):
    with urllib.request.urlopen(url) as response:
        data = response.read()
        z = zipfile.ZipFile(io.BytesIO(data))
        extract_path = os.path.join(ROOT_DIR, "temp_libs", name)
        z.extractall(extract_path)
        return extract_path

def install_libs():
    print("="*50)
    print("Installing Addon Libraries")
    print("="*50)
    
    # Create temp dir
    if os.path.exists("temp_libs"):
        shutil.rmtree("temp_libs")
    os.makedirs("temp_libs")
    
    downloaded_libs = {}
    
    # Download all libs
    for name, url in LIBS.items():
        path = download_and_extract(url, name)
        if path:
            inner_dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
            if inner_dirs:
                downloaded_libs[name] = os.path.join(path, inner_dirs[0])
            else:
                downloaded_libs[name] = path

    # Install into Addons
    for addon in ADDONS:
        addon_path = os.path.join(ROOT_DIR, addon)
        if not os.path.exists(addon_path):
            continue
            
        print(f"\n📦 Installing libs into {addon}...")
        libs_dir = os.path.join(addon_path, "Libs")
        
        if not os.path.exists(libs_dir):
            os.makedirs(libs_dir)
            
        # 1. Install Downloaded Libs
        for lib_name, source_path in downloaded_libs.items():
            dest_path = os.path.join(libs_dir, lib_name)
            if os.path.exists(dest_path): shutil.rmtree(dest_path)
            shutil.copytree(source_path, dest_path)
            print(f"   - Installed {lib_name}")
            
        # 2. Extract LibStub/CallbackHandler from Ace3 if available
        if "Ace3" in downloaded_libs:
            ace3_path = downloaded_libs["Ace3"]
            
            # LibStub
            if os.path.exists(os.path.join(ace3_path, "LibStub")):
                dest = os.path.join(libs_dir, "LibStub")
                if os.path.exists(dest): shutil.rmtree(dest)
                shutil.copytree(os.path.join(ace3_path, "LibStub"), dest)
                print("   - Extracted LibStub from Ace3")
                
            # CallbackHandler
            if os.path.exists(os.path.join(ace3_path, "CallbackHandler-1.0")):
                dest = os.path.join(libs_dir, "CallbackHandler-1.0")
                if os.path.exists(dest): shutil.rmtree(dest)
                shutil.copytree(os.path.join(ace3_path, "CallbackHandler-1.0"), dest)
                print("   - Extracted CallbackHandler-1.0 from Ace3")

if __name__ == "__main__":
    install_libs()
