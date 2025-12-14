#!/bin/bash
set -euo pipefail

REPO="/Users/jgrayson/Documents/MyAddons-Mono"
WOW="/Applications/World of Warcraft/_retail_/Interface/AddOns"

echo "== Deploying DeepPockets (Strict Backend Only) =="
# User Rule: Only copy .toc, .lua, and dp_ext/. Exclude everything else.
rsync -av --delete \
  --exclude '_TRASH/' \
  --include 'DeepPockets.toc' \
  --include 'DeepPockets.lua' \
  --include 'tooltip_guard.lua' \
  --include 'tooltip_trace.lua' \
  --include 'bridge.lua' \
  --include 'dp_ext/***' \
  --exclude '*' \
  "$REPO/DeepPockets/"  "$WOW/DeepPockets/"

echo ""
echo "== Deploying DeepPocketsBB_Categories =="
# This folder is already clean/new, so simple rsync is fine.
if [ -d "$REPO/DeepPocketsBB_Categories" ]; then
    rsync -av --delete \
      "$REPO/DeepPocketsBB_Categories/" "$WOW/DeepPocketsBB_Categories/"
else
    echo "Warning: DeepPocketsBB_Categories not found in repo."
fi

echo ""
echo "== Deployment Complete =="
