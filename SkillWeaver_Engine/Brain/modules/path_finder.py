import platform
import os
import sys
import psutil

# Logic:
# 1. OS Detection (Win/Mac)
# 2. Preferred Path Check (Registry/AppDir)
# 3. Process Scan (Wow.exe/World of Warcraft.app)

def get_wow_path():
    system = platform.system()
    
    if system == "Windows":
        return _get_windows_path()
    elif system == "Darwin": # macOS
        return _get_mac_path()
    else:
        return None

def _get_windows_path():
    # 1. Registry (Requires winreg, only avail on Windows)
    try:
        import winreg
        key_path = r"SOFTWARE\WOW6432Node\Blizzard Entertainment\World of Warcraft"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            install_path = winreg.QueryValueEx(key, "InstallPath")[0]
            if install_path:
                retail = os.path.join(install_path, "_retail_")
                if os.path.exists(retail): return retail
    except Exception:
        pass
        
    # 2. Standard Fallback
    fallback = r"C:\Program Files (x86)\World of Warcraft\_retail_"
    if os.path.exists(fallback): return fallback
    
    # 3. Process Scan
    return _scan_process("Wow.exe")

def _get_mac_path():
    # 1. Standard App Directory
    paths = [
        "/Applications/World of Warcraft/_retail_",
        os.path.expanduser("~/Applications/World of Warcraft/_retail_")
    ]
    for p in paths:
        if os.path.exists(p): return p
        
    # 2. Process Scan
    return _scan_process("World of Warcraft")

def _scan_process(proc_name):
    # Fallback: Check running processes
    try:
        for proc in psutil.process_iter(['name', 'exe']):
            if proc.info['name'] == proc_name:
                exe_path = proc.info['exe']
                if exe_path:
                    # exe_path might be .../_retail_/Wow.exe
                    # We want the folder containing _retail_ or just _retail_
                    # Usually: /.../World of Warcraft/_retail_/World of Warcraft.app/Contents/MacOS/...
                    # Let's try to find "_retail_" in the path
                    parts = exe_path.split(os.sep)
                    if "_retail_" in parts:
                        # Reconstruct up to _retail_
                        idx = parts.index("_retail_")
                        return os.sep.join(parts[:idx+1])
    except Exception:
        pass
    return None

if __name__ == "__main__":
    found_path = get_wow_path()
    if found_path:
        print(f"FOUND: {found_path}")
    else:
        print("NOT_FOUND")
