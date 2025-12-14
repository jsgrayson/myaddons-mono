#!/bin/bash
set -euo pipefail

# Hardcoded absolute path for safety
DP_DIR="/Users/jgrayson/Documents/MyAddons-Mono/DeepPockets"

ts="$(date +%Y%m%d-%H%M%S)"
TRASH="$DP_DIR/_TRASH/$ts"
mkdir -p "$TRASH"

echo "== DeepPockets cleanup in: $DP_DIR"
echo "== Trash target: $TRASH"

# --- 1) Ensure backend-only TOC exists (no bindings, no bag hooks, no UI) ---
# UPDATED: Including dp_ext modules to prevent breakage of current backend logic
cat > "$DP_DIR/DeepPockets.toc" <<'EOF'
## Interface: 110200
## Title: DeepPockets (Backend)
## Notes: Backend-only companion for BetterBags. No UI, no bindings, no bag hooks.
## Author: DeepPockets Team
## Version: 0.1.0-backend
## SavedVariables: DeepPocketsDB
## OptionalDeps: BetterBags

DeepPockets.lua
dp_ext/api.lua
dp_ext/scan.lua
dp_ext/index.lua
dp_ext/commands.lua
dp_ext/migrate.lua
EOF

# --- 2) Define what we KEEP in-place ---
KEEP_NAMES=(
  "DeepPockets.lua"
  "DeepPockets.toc"
  "dp_ext"
  "_TRASH"
)

is_keep() {
  local name="$1"
  for k in "${KEEP_NAMES[@]}"; do
    [[ "$name" == "$k" ]] && return 0
  done
  return 1
}

# --- 3) Move everything else to trash ---
shopt -s dotglob nullglob

moved=0
for item in "$DP_DIR"/*; do
  base="$(basename "$item")"
  if is_keep "$base"; then
    continue
  fi

  # Safety: don’t trash the trash
  if [[ "$base" == "_TRASH" ]]; then
    continue
  fi

  mv "$item" "$TRASH/"
  moved=$((moved+1))
done

echo "== Moved $moved items into $TRASH"
echo "== Remaining in DeepPockets/:"
ls -la "$DP_DIR"

echo ""
echo "Sanity: TOCs now present:"
find "$DP_DIR" -maxdepth 1 -name "*.toc" -print
