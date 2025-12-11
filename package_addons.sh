#!/bin/bash

# Addon Packager
# Zips up the addons for distribution.

DIST_DIR="dist"
mkdir -p $DIST_DIR

echo "========================================"
echo "   Holocron Addon Packager"
echo "========================================"

# Install Libraries
echo "⬇️  Fetching Libraries..."
python3 setup_libs.py

# Function to zip an addon
package_addon() {
    local name=$1
    local path=$2
    
    if [ -d "$path" ]; then
        echo "📦 Packaging $name..."
        # Exclude .git, .DS_Store, etc.
        zip -r -q "$DIST_DIR/$name.zip" "$path" -x "*.git*" "*.DS_Store*"
        echo "   ✅ Created $DIST_DIR/$name.zip"
    else
        echo "⚠️  Directory $path not found. Skipping $name."
    fi
}

# Paths (adjust relative to this script)
# Assuming script is in holocron/ and addons are in sibling dirs
ROOT_DIR=".."

package_addon "SkillWeaver" "$ROOT_DIR/skillweaver/SkillWeaver"
package_addon "PetWeaver" "$ROOT_DIR/petweaver/PetWeaver"
package_addon "HolocronViewer" "$ROOT_DIR/holocron/HolocronViewer"
package_addon "DeepPockets" "$ROOT_DIR/holocron/DeepPockets"

echo "----------------------------------------"
echo "🎉 Packaging Complete!"
echo "   Files are in $DIST_DIR/"
