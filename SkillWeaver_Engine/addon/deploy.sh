#!/bin/bash
set -e

REPO="/Users/jgrayson/Documents/MyAddons-Mono/SkillWeaver_Engine/addon"
WOW="/Applications/World of Warcraft/_retail_/Interface/AddOns/ColorProfile_Lib"

echo "== Deploying ColorProfile_Lib =="
echo "Source: $REPO"
echo "Target: $WOW"

# Ensure target directory exists
mkdir -p "$WOW"

# Copy files
cp "$REPO/ColorProfile_Lib.lua" "$WOW/"
cp "$REPO/ColorProfile_Lib.toc" "$WOW/"

echo "== Deployment Complete =="
