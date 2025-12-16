#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

fail() { echo "GUARD_FAIL: $*" >&2; exit 1; }

# A) Kill “folder 2/” and similar copy artifacts
if find . -maxdepth 3 -type d \( -name "* 2" -o -name "* 2/" -o -name "* 2*" \) | grep -q .; then
  echo "Found duplicate-suffixed directories:"
  find . -maxdepth 4 -type d -name "* 2*" | sed 's/^/ - /'
  fail "Remove duplicate-suffixed folders (* 2*)."
fi

# B) No DISABLED/TRASH folders anywhere in addon sources
if find . -type d \( -iname "*disabled*" -o -iname "*_trash*" \) | grep -q .; then
  echo "Found DISABLED/TRASH directories:"
  find . -type d \( -iname "*disabled*" -o -iname "*_trash*" \) | sed 's/^/ - /'
  fail "Remove DISABLED/TRASH directories; they cause nested/duplicate TOCs."
fi

# C) .toc files must only exist at addon roots (DeepPockets.toc etc) OR inside Libs/
# (Adjust allowed paths here if you intentionally keep vendor toc elsewhere.)
TOCS=()
while IFS= read -r line; do
  TOCS+=("$line")
done < <(find . -name "*.toc" -type f)

for toc in "${TOCS[@]}"; do
  # allow Libs/ anywhere
  if [[ "$toc" == *"/Libs/"* ]] || [[ "$toc" == *"/libs/"* ]]; then
    continue
  fi
  # allow addon root toc: ./AddonName/AddonName.toc
  addon_dir="$(dirname "$toc")"
  base="$(basename "$toc")"
  addon_name="$(basename "$addon_dir")"
  if [[ "$base" != "$addon_name.toc" ]]; then
    fail "Unexpected toc location/name: $toc (expected $addon_name/$addon_name.toc or under Libs/)"
  fi
done

# D) Validate DeepPockets.toc exists (optional but nice)
if [[ -f "./DeepPockets/DeepPockets.toc" ]]; then
  echo "OK: DeepPockets.toc present"
fi

echo "GUARD_OK: repo structure looks clean"
