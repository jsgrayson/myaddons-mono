#!/usr/bin/env bash
set -euo pipefail

TOC="${1:?Usage: tools/validate_toc.sh path/to/AddOn.toc}"
ADDON_DIR="$(cd "$(dirname "$TOC")" && pwd)"
TOC_ABS="$(cd "$(dirname "$TOC")" && pwd)/$(basename "$TOC")"

fail(){ echo "TOC_FAIL: $*" >&2; exit 1; }

[[ -f "$TOC_ABS" ]] || fail "TOC not found: $TOC_ABS"

# Create temp file for tracking seen files (bash 3.2 compat)
seen_file=$(mktemp -t dp_toc_validate)
trap 'rm -f "$seen_file"' EXIT

lineno=0

while IFS= read -r line || [[ -n "$line" ]]; do
  lineno=$((lineno+1))
  # strip CR
  line="${line%$'\r'}"
  # ignore comments/metadata/blank
  [[ -z "$line" ]] && continue
  [[ "$line" =~ ^\# ]] && continue
  [[ "$line" =~ ^\#\# ]] && continue

  # normalize slashes
  file="${line//\\//}"

  # dedupe check
  if grep -Fxq "$file" "$seen_file"; then
    fail "Duplicate file load: [$file] at line $lineno"
  fi
  echo "$file" >> "$seen_file"

  # existence check (only for .lua/.xml/.toc referenced files)
  if [[ "$file" =~ \.(lua|xml|toc)$ ]]; then
    if [[ ! -f "$ADDON_DIR/$file" ]]; then
      fail "Missing referenced file: $ADDON_DIR/$file (from line $lineno)"
    fi
  fi
done < "$TOC_ABS"

echo "TOC_OK: $TOC (no dupes, all referenced files exist)"
