#!/bin/bash
set -euo pipefail

REPO="/Users/jgrayson/Documents/MyAddons-Mono"
WOW="/Applications/World of Warcraft/_retail_/Interface/AddOns"

echo "== Deploying DeepPockets (Strict Backend Only) =="
# Strict allowlist
rsync -av --delete \
  --include 'money_flow.lua' \
  --include 'eventlog_retention.lua' \
  --include 'autoscan.lua' \
  --include 'item_cache.lua' \
  --include 'new_item_tracker.lua' \
  --include 'upgrade_reason.lua' \
  --include 'item_source.lua' \
  --include 'item_age.lua' \
  --include='tooltip_guard.lua' \
  --include='tooltip_trace.lua' \
  --include='DeepPockets.toc' \
  --include='event_guard.lua' \
  --include='scan_backend.lua' \
  --include='dump_backend.lua' \
  --include='sanity.lua' \
  --include 'item_lifecycle.lua' \
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
