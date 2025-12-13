#!/bin/bash
set -e

ADDONS_DIR="/Applications/World of Warcraft/_retail_/Interface/AddOns"
REPO_ROOT="$(pwd)"

# Helper: Check for nested TOCs (Depth > 1)
check_nested_toc() {
    local src="$1"
    local ignore_path="$2" # Optional path pattern to ignore (e.g. */HolocronViewer/*)
    
    echo "Checking $src for nested definition anomalies..."
    
    CMD="find \"$src\" -mindepth 2 -name \"*.toc\" -not -path \"*/.*\" -not -path \"*/Libs/*\" -not -path \"*/libs/*\""
    if [ -n "$ignore_path" ]; then
        CMD="$CMD -not -path \"$ignore_path\""
    fi
    
    # Use eval to handle the dynamic command construction safely-ish here
    if eval "$CMD -print -quit" | grep -q .; then
        echo "Error: Nested .toc detected in $src!"
        eval "$CMD"
        exit 1
    fi
}

deploy_addon() {
    local src="$1"
    local dest_name="$2"
    local excludes="$3"

    echo "Deploying $src -> $dest_name"
    check_nested_toc "$src"

    mkdir -p "$ADDONS_DIR/$dest_name"
    rsync -av --delete --exclude='.*' --exclude='*.py' --exclude='*.sh' \
        --exclude='*DISABLED*' --exclude='*_old*' --exclude='*(1)*' \
        --exclude='*-web*' --exclude='*-api*' --exclude='*-sync*' \
        --exclude='node_modules' --exclude='target' --exclude='dist' \
        $excludes \
        "$src/" "$ADDONS_DIR/$dest_name/"
}

# 1. DeepPockets
deploy_addon "DeepPockets" "DeepPockets" ""

# 2. PetWeaver
deploy_addon "PetWeaver" "PetWeaver" ""

# 3. SkillWeaver
deploy_addon "SkillWeaver" "SkillWeaver" ""

# 4. Goblin
deploy_addon "Goblin" "Goblin" ""

# 5. HolocronViewer
# Nested inside Holocron repo dir, but checks are strictly for SUB-nested TOCS
deploy_addon "Holocron/HolocronViewer" "HolocronViewer" ""

# 6. Holocron (Base)
# Special handling because it has HolocronViewer sibling/child in source
echo "Deploying Holocron (Base) -> Holocron"
# Strict include list for base addon
# skipping check_nested_toc because Holocron source repo contains other projects (DeepPockets etc) 
# but we are using strict --include so it is safe.
rsync -av \
    --include='Holocron.toc' \
    --include='Holocron.lua' \
    --include='Holocron.xml' \
    --include='HolocronCore/***' \
    --exclude='*' \
    "Holocron/" "$ADDONS_DIR/Holocron/"

echo "--------------------------------------------------------"
echo "Deployment Complete. Verifying LIVE folders..."
echo "If any output appears below, verification FAILED:"
find "$ADDONS_DIR/DeepPockets" -mindepth 2 -name "*.toc" -print
find "$ADDONS_DIR/PetWeaver" -mindepth 2 -name "*.toc" -print
find "$ADDONS_DIR/SkillWeaver" -mindepth 2 -name "*.toc" -print
find "$ADDONS_DIR/Holocron" -mindepth 2 -name "*.toc" -print
find "$ADDONS_DIR/HolocronViewer" -mindepth 2 -name "*.toc" -print
echo "End of verification."
