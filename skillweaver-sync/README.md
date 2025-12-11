# SkillWeaver Sync - Desktop Companion

Syncs your WoW addon data with the SkillWeaver web portal.

## Features

- **Auto-Sync**: Watches SavedVariables and uploads instantly on change
- **Periodic Sync**: Background upload every 5min, download every 10min
- **Download Recommendations**: Pull talent/gear recommendations from web
- **Smart Queuing**: Waits for WoW to close before writing recommendations
- **System Tray**: Runs quietly in background with status icon
- **Manual Control**: Right-click icon to sync on demand
- **Cross-Platform**: Auto-detects WoW path on Windows/Mac/Linux

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run (auto-detects OS and WoW path)
python main.py

# Or specify custom path:
# macOS:
python main.py --wow-path "/Applications/World of Warcraft"

# Windows:
python main.py --wow-path "C:\Program Files (x86)\World of Warcraft"

# Linux (Wine):
python main.py --wow-path "$HOME/.wine/drive_c/Program Files (x86)/World of Warcraft"
```

## Usage

### Command Line
```bash
python main.py \
  --wow-path "/Applications/World of Warcraft" \
  --api-url "https://skillweaver.gg" \
  --token "your-auth-token"
```

### System Tray (Recommended)
```bash
python ui/tray.py
```

Right-click the tray icon for options:
- **Sync Now**: Upload current character data
- **Download Recommendations**: Get latest optimizations
- **Quit**: Stop the app

## How It Works

1. **Monitors** `WTF/Account/[ACCOUNT]/SavedVariables/SkillWeaverDB.lua`
2. **Uploads** character data when file changes
3. **Downloads** recommendations from web portal
4. **Writes** recommendations back to SavedVariables
5. Addon reads recommendations on `/reload`

## Configuration

Edit config at the top of `main.py`:
- WoW installation path
- API URL
- Authentication token (from web portal)

## Building Installers

### macOS
```bash
./build_mac.sh
# Creates: dist/WoWSuiteSync.app and WoWSuiteSync-Installer.dmg
```

### Windows
```bat
build_windows.bat
REM Creates: dist\WoWSuiteSync.exe and Output\WoWSuiteSync-Setup.exe
```

**Requirements:**
- macOS: `brew install create-dmg` (for DMG creation)
- Windows: [Inno Setup](https://jrsoftware.org/isdl.php) (for installer)
