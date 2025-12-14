#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p _TRASH/dupes_backup

echo "[DP] Scanning for duplicate '* 2' directories/files..."

# Move any "name 2" dirs/files into _TRASH/dupes_backup while preserving paths
# Examples: "frames 2", "frames 2/", "data 2", "integrations 2", etc.
# Also handles "name 2/" and "name 2" (file).
while IFS= read -r -d '' p; do
  rel="${p#"$ROOT"/}"
  dest="_TRASH/dupes_backup/$rel"
  mkdir -p "$(dirname "$dest")"
  echo "  - MOVING: $rel -> $dest"
  mv "$p" "$dest"
done < <(find "$ROOT" -maxdepth 2 \
  \( -name "* 2" -o -name "* 2/" \) \
  -print0)

echo "[DP] Also moving obvious scratch dirs (if present): cache/, examples/, tools 2/, animations 2/, templates 2/, textures 2/"
for d in "cache" "examples" "tools 2" "animations 2" "templates 2" "textures 2"; do
  if [ -e "$d" ]; then
    mkdir -p "_TRASH/dupes_backup/$(dirname "$d")"
    echo "  - MOVING: $d -> _TRASH/dupes_backup/$d"
    mv "$d" "_TRASH/dupes_backup/$d"
  fi
done

echo "[DP] Done. Review _TRASH/dupes_backup/ and confirm nothing important is there."
echo "[DP] Next step: git status; then commit cleanup."
