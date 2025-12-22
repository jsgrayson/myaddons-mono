#!/bin/bash

# SkillWeaver / ColorProfile_Lib Deployment Script (Stealth Protocol)
# Target: macOS Default Path or Auto-Detected

# 1. Define Source Paths
SOURCE_LIB="./ColorProfile_Lib"
SOURCE_ENGINE="./SkillWeaver_Engine"

# 2. Define WoW Path (MacOS Default)
WOW_PATH="/Applications/World of Warcraft/_retail_"
ADDON_PATH="$WOW_PATH/Interface/AddOns"

# 3. Check for Custom Path override
if [ -d "$1" ]; then
    WOW_PATH="$1"
    ADDON_PATH="$WOW_PATH/Interface/AddOns"
fi

echo "--- SKILLWEAVER DEPLOYMENT (STEALTH PROTOCOL) ---"
echo "Target: $ADDON_PATH"

# 4. Safety Checks
if [ ! -d "$ADDON_PATH" ]; then
    echo "ERROR: WoW AddOn directory not found at $ADDON_PATH"
    echo "Usage: ./deploy_skillweaver.sh [Optional: /Path/To/WoW]"
    exit 1
fi

if [ ! -d "$SOURCE_LIB" ]; then
    echo "ERROR: Source 'ColorProfile_Lib' not found in current directory."
    exit 1
fi

# 5. Deployment - ColorProfile_Lib (Stealth Addon)
echo "Deploying ColorProfile_Lib (Stealth Layer)..."
rm -rf "$ADDON_PATH/ColorProfile_Lib"
cp -R "$SOURCE_LIB" "$ADDON_PATH/"

# 6. Deployment - SkillWeaver Core (Optional / Legacy)
# Use existing SkillWeaver folder if present, only update specific files if needed
# For now, we assume ColorProfile_Lib carries the weight.

# 7. Engine Setup (Python)
echo "Verifying Logic Engine Dependencies..."
# Ensure execution bit on tools
chmod +x "$SOURCE_ENGINE/tools/"*.bat
chmod +x "$SOURCE_ENGINE/tools/"*.sh 2>/dev/null

echo "--- DEPLOYMENT COMPLETE ---"
echo ""
echo "NEXT STEPS (MASTER SETUP):"
echo "1. [Hardware] Plug in Arduino (Switch 2 = OPEN)."
echo "2. [Verify ] Run 'tools/Verify_Ghost.bat' (Windows) or check System Report (Mac)."
echo "3. [Game    ] Launch WoW. Enable 'ColorProfile_Lib'."
echo "4. [Logic   ] Run 'python3 SkillWeaver_Engine/Brain/logic_processor.py'."
echo "5. [Active  ] Flip Switch 2 to CLOSED to Activate."
echo ""
echo "Ghost Protocol is Live."
