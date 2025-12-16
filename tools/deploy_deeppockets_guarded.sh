#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   tools/deploy_deeppockets_guarded.sh /path/to/WoW/_retail_/Interface/AddOns
#
# This script ONLY deploys ./DeepPockets into the target AddOns folder.
# It refuses to deploy if it detects stale “DeepPockets” copies in obvious places (Holocron/release, etc).

TARGET="${1:?Give WoW AddOns folder, e.g. /Applications/World of Warcraft/_retail_/Interface/AddOns}"
SRC_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$SRC_ROOT/DeepPockets"

fail(){ echo "DEPLOY_FAIL: $*" >&2; exit 1; }

[[ -d "$SRC" ]] || fail "Source not found: $SRC"
[[ -d "$TARGET" ]] || fail "Target not found: $TARGET"

# Refuse deploy if repo contains other DeepPockets copies outside ./DeepPockets
copies=()
while IFS= read -r line; do
  copies+=("$line")
done < <(find "$SRC_ROOT" -maxdepth 4 -type f -name "DeepPockets.toc" | sed "s|^$SRC_ROOT/||")

for c in "${copies[@]}"; do
  if [[ "$c" != "DeepPockets/DeepPockets.toc" ]]; then
    fail "Stale DeepPockets.toc copy found at: $c (delete it or exclude it from deploy)"
  fi
done

echo "DEPLOY_INFO: Source of truth is: $SRC"
echo "DEPLOY_INFO: Target AddOns is:    $TARGET"

# Run guards
"$SRC_ROOT/tools/guard_repo.sh" "$SRC_ROOT"
"$SRC_ROOT/tools/validate_toc.sh" "$SRC/DeepPockets.toc"

# Clean target
rm -rf "$TARGET/DeepPockets"

# Copy DeepPockets (exclude trash + build artifacts)
rsync -a --delete \
  --exclude "_TRASH/" \
  --exclude "cache/" \
  --exclude ".git/" \
  --exclude "node_modules/" \
  --exclude "* 2/" \
  "$SRC/" "$TARGET/DeepPockets/"






# BetterBags integration disabled/removed (Pure Backend Mode)







echo "DEPLOY_OK: DeepPockets deployed to $TARGET/DeepPockets"
