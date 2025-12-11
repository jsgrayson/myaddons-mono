#!/bin/bash
# Build WoW Suite Sync for macOS
# Creates a .app bundle and .dmg installer

echo "Building WoW Suite Sync for macOS..."

# Install PyInstaller if needed
pip3 install pyinstaller pillow --upgrade

# Clean previous builds
rm -rf build dist

# Build .app bundle
pyinstaller build_mac.spec --clean

# Create DMG installer (requires create-dmg: brew install create-dmg)
if command -v create-dmg &> /dev/null; then
    create-dmg \
        --volname "WoW Suite Sync" \
        --window-pos 200 120 \
        --window-size 600 400 \
        --icon-size 100 \
        --app-drop-link 425 120 \
        "dist/WoWSuiteSync-Installer.dmg" \
        "dist/WoWSuiteSync.app"
    
    echo "✓ DMG created: dist/WoWSuiteSync-Installer.dmg"
else
    echo "⚠️  create-dmg not found. Install with: brew install create-dmg"
    echo "✓ .app bundle created: dist/WoWSuiteSync.app"
fi

echo "Done!"
