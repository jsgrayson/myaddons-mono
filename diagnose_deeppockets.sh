#!/bin/bash
WOW="/Applications/World of Warcraft/_retail_/Interface/AddOns"

echo "=== 1) Find EVERY DeepPockets.toc anywhere under AddOns ==="
find "$WOW" -iname "DeepPockets.toc" -print

echo ""
echo "=== 2) Find EVERY DeepPockets.lua anywhere under AddOns ==="
find "$WOW" -iname "DeepPockets.lua" -print

echo ""
echo "=== 3) Search for backend banner/version in ALL AddOns (fast grep) ==="
grep -R --line-number --fixed-strings "0.1.0-backend" "$WOW" || echo "NOT FOUND: 0.1.0-backend"

echo ""
echo "=== 4) Show the actual TOC that WoW would load for /Interface/AddOns/DeepPockets ==="
if [ -f "$WOW/DeepPockets/DeepPockets.toc" ]; then
  echo "--- $WOW/DeepPockets/DeepPockets.toc ---"
  sed -n '1,80p' "$WOW/DeepPockets/DeepPockets.toc"
else
  echo "MISSING: $WOW/DeepPockets/DeepPockets.toc"
fi

echo ""
echo "=== 5) Show first 120 lines of the DeepPockets.lua WoW would load ==="
if [ -f "$WOW/DeepPockets/DeepPockets.lua" ]; then
  echo "--- $WOW/DeepPockets/DeepPockets.lua ---"
  sed -n '1,120p' "$WOW/DeepPockets/DeepPockets.lua"
else
  echo "MISSING: $WOW/DeepPockets/DeepPockets.lua"
fi

echo ""
echo "=== 6) HARD NUKE (only do this AFTER you read results above) ==="
echo "If you see >1 DeepPockets.toc OR no 0.1.0-backend anywhere, deployment is wrong."
echo "To fix: delete ALL DeepPockets* folders then deploy ONLY the backend one."
