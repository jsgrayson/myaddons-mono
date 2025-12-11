#!/bin/bash
set -e

################################################################################
# UI Setup Script (SAFE VERSION — no heredocs)
################################################################################

BASE_DIR="$HOME/Documents/goblin-clean/ui"

echo "[UI] Creating UI directories ..."

mkdir -p "$BASE_DIR/mobile"
mkdir -p "$BASE_DIR/web"

################################################################################
# Helper write function
################################################################################
write_file() {
    FILE="$1"
    shift
    printf "%s\n" "$@" > "$FILE"
}

################################################################################
# MOBILE README
################################################################################

write_file "$BASE_DIR/mobile/README.md" \
"# Goblin Mobile UI" \
"" \
"This folder is reserved for the future Goblin mobile application." \
"" \
"Recommended stacks:" \
"- SwiftUI (iOS)" \
"- Kotlin + Jetpack Compose (Android)" \
"- Flutter (cross-platform)" \
"- React Native (cross-platform)" \
"" \
"Mobile UI will eventually serve as a controller for:" \
"- Agent status" \
"- ML predictions" \
"- Task scheduling" \
"- Backend health" \
"- Logs and notifications"

################################################################################
# WEB README
################################################################################

write_file "$BASE_DIR/web/README.md" \
"# Goblin Web UI" \
"" \
"The Goblin Web UI will provide a browser-based dashboard for:" \
"- System overview" \
"- Agent control" \
"- ML prediction views" \
"- AH scanning dashboards" \
"- TSM Brain insights" \
"- Task automation" \
"" \
"This is intentionally empty until the dashboard is implemented."

################################################################################
# Done
################################################################################

echo "[UI] UI subsystem created successfully."

