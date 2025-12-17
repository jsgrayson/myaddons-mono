#!/usr/bin/env bash
set -euo pipefail

EXPORT_TXT="${1:-export.txt}"
ROT_OUT="${2:-rotations.json}"
SPELL_OUT="${3:-spellbook.json}"
POL_OUT="${4:-policies.json}"

echo "[1/5] Reassembling export bundle -> $ROT_OUT + $SPELL_OUT"
python tools/reassemble_export_bundle.py "$EXPORT_TXT" "$ROT_OUT" "$SPELL_OUT"

echo "[2/5] Auto-tagging policies -> $POL_OUT"
python tools/policy_autotag.py "$ROT_OUT" "$SPELL_OUT" > "$POL_OUT"

echo "[3/5] Compiling -> policies/spec/*.gen.lua"
python tools/policy_compiler.py "$POL_OUT"

echo "[4/5] Coverage validation"
python tools/policy_merge_check.py --fail-on-missing --require-spender

echo "[5/5] Coverage score (per spec)"
python tools/coverage_score.py

echo "DONE ✅"
