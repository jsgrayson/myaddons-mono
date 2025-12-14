#!/bin/bash
REPO="/Users/jgrayson/Documents/MyAddons-Mono"
WOW="/Applications/World of Warcraft/_retail_/Interface/AddOns"

set -euo pipefail

echo "==[1] Repo cleanup: remove legacy/experimental DP junk =="

# Kill obvious legacy folders
rm -rf "$REPO/DeepPockets/DeepPocketsDISABLED" 2>/dev/null || true
rm -rf "$REPO/DeepPocketsBB" 2>/dev/null || true
rm -rf "$REPO/DeepPocketsBB_Categories_DISABLED" 2>/dev/null || true
rm -rf "$REPO/DeepPockets_Fork" 2>/dev/null || true
rm -rf "$REPO/BetterBags" 2>/dev/null || true 
rm -rf "$REPO/Holocron/release/DeepPockets" 2>/dev/null || true
rm -rf "$REPO/Holocron/DeepPockets" 2>/dev/null || true

# Remove backend-root junk files (excluding TOC/Lua)
find "$REPO/DeepPockets" -maxdepth 1 -type f \
  ! -name "DeepPockets.toc" \
  ! -name "DeepPockets.lua" \
  -print -delete || true

# Kill legacy UI folders (PRESERVING dp_ext which contains our actual code now)
# Removed dp_ext from this list to protect authoritative backend modules.
for d in assets core frames themes views templates libs animations forms bags data util integrations CategoryMap.lua DeepPockets.xml Bindings.xml; do
  rm -rf "$REPO/DeepPockets/$d" 2>/dev/null || true
done

echo "==[2] Addon Verification (Skipping TOC overwrite to preserve dp_ext) =="
if [ ! -d "$REPO/DeepPockets/dp_ext" ]; then
    echo "WARNING: dp_ext missing! Backend logic might be incomplete."
fi

echo "==[3] WoW AddOns cleanup: remove all DP junk =="
rm -rf "$WOW/DeepPockets" 2>/dev/null || true
rm -rf "$WOW/DeepPocketsBB" 2>/dev/null || true
rm -rf "$WOW/DeepPocketsBB_Categories" 2>/dev/null || true
rm -rf "$WOW/DeepPocketsDISABLED" 2>/dev/null || true
# rm -rf "$WOW/BetterBags" # Commented out as requested

echo "==[4] Deploy the clean minimal addons =="
mkdir -p "$WOW/DeepPockets"
cp -R "$REPO/DeepPockets/"* "$WOW/DeepPockets/"

if [ -d "$REPO/DeepPocketsBB_Categories" ]; then
  mkdir -p "$WOW/DeepPocketsBB_Categories"
  cp -R "$REPO/DeepPocketsBB_Categories/"* "$WOW/DeepPocketsBB_Categories/"
fi

echo "==[5] Guard check =="
bad=$(find "$WOW/DeepPockets" -name "*.toc" -not -path "*/libs/*" | wc -l | tr -d ' ')
if [ "$bad" -ne 1 ]; then
  echo "ERROR: DeepPockets has $bad toc files (expected 1)."
  find "$WOW/DeepPockets" -name "*.toc"
  exit 1
fi

echo "DONE. Cleanup and Deploy Complete."
