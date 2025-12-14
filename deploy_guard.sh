#!/bin/bash
WOW="/Applications/World of Warcraft/_retail_/Interface/AddOns"
REPO="/Users/jgrayson/Documents/MyAddons-Mono"

echo "== Guard: abort if stale/duplicate DeepPockets exists =="
echo "-- DeepPockets.toc locations in AddOns:"
find "$WOW" -iname "DeepPockets.toc" -print

echo "-- DeepPockets 0.1.0-backend banner locations in AddOns:"
grep -R --line-number --fixed-strings "0.1.0-backend" "$WOW" || true

echo ""
echo "== Hard clean DeepPockets targets =="
rm -rf "$WOW/DeepPockets" \
       "$WOW/DeepPocketsBB" \
       "$WOW/DeepPocketsBB_Categories" \
       "$WOW"/*DeepPockets*

echo ""
echo "== Deploy canonical copies ONLY from MyAddons-Mono =="
cp -R "$REPO/DeepPockets" "$WOW/DeepPockets"
if [ -d "$REPO/DeepPocketsBB_Categories" ]; then
    cp -R "$REPO/DeepPocketsBB_Categories" "$WOW/DeepPocketsBB_Categories"
fi

echo ""
echo "== Verify deployed banner exists in WoW AddOns =="
grep -R --line-number --fixed-strings "0.1.0-backend" "$WOW/DeepPockets" || {
  echo "ERROR: backend banner not found in deployed DeepPockets"; exit 1;
}

echo "OK: DeepPockets backend deployed cleanly."
