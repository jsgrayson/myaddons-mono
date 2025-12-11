# PetWeaver - Teams & Scripts Not Populating - FIXED

## Issues Found and Fixed

### 1. **TOC File Comment Syntax Error** ✓ FIXED
**Problem:** The `.toc` file was using `#` symbols as comments within the file list:
```
# Data Files (load first)
encounters_data.lua
# Core Addon
PetWeaver.lua
```

**Fix:** Removed improper comment syntax. WoW TOC files only use `##` for metadata headers, not `#` for inline comments.

### 2. **Load Timing Issue** ✓ FIXED  
**Problem:** `LoadDefaultTeams()` was being called on `PLAYER_LOGIN` event, which fires BEFORE the addon's Lua files are fully loaded. This meant `PetWeaver_DefaultTeams` and `PetWeaver_Encounters` tables didn't exist yet!

**Fix:** Moved `LoadDefaultTeams()` to the `ADDON_LOADED` event for PetWeaver itself. Event order is now:
1. `ADDON_LOADED` (PetWeaver) → Load data files → Call `LoadDefaultTeams()`
2. `PLAYER_LOGIN` → Initialize Battle UI

### 3. **Added Debug Logging** ✓ ADDED
Added comprehensive debug output to help diagnose issues:
- Checks if data files exist
- Shows how many teams/encounters were found
- Shows current team count
- Reports success/failure of loading

## What You Should See In-Game

When you log in or reload UI (`/reload`), you should now see these messages in chat:

```
PetWeaver: Native Core Loaded.
PetWeaver: Addon loaded, checking data files...
PetWeaver: PetWeaver_DefaultTeams exists: true
PetWeaver: PetWeaver_Encounters exists: true
PetWeaver: Found 5 default teams in data file
PetWeaver: LoadDefaultTeams() called
PetWeaver: Current teams count: 0
PetWeaver: PetWeaver_DefaultTeams available: true
PetWeaver: Loading default teams...
PetWeaver: Loaded 5 default teams
PetWeaver: Loading encounter database...
PetWeaver: Loaded 6 encounters
PetWeaver: Ready. Current teams: 5
PetWeaver: Battle UI initialized
```

## Testing Steps

1. **Reload the addon in WoW:**
   - Type `/reload` in-game on any Dalaran character

2. **Check the chat log** for the debug messages above

3. **Open the Pet Journal** and look for the PetWeaver toggle

4. **If teams still don't show:**
   - Delete your saved variables: Find `WTF/Account/YOUR_ACCOUNT/SavedVariables/PetWeaver.lua` and delete it
   - Do a `/reload` to start fresh
   - The addon should auto-populate with 5 default teams

## Data Included

### Teams (5 total):
1. **Squirt Leveling (Ikky + MPD)** - 2-pet carry for leveling
2. **Major Payne (Mechanical)** - Family Familiar encounter
3. **Gargra (Dragonkin)** - Family Familiar encounter  
4. **All-Purpose Strong Team** - Generic strong team
5. **Stitches Jr. (Undead)** - World Quest encounter

### Encounters (6 total):
1. Squirt (Garrison, Daily)
2. Major Payne (Tanaan Jungle, Family Familiar)
3. Gargra (Frostfire Ridge, Family Familiar)
4. Grixis Tinypop (Dalaran, World Quest)
5. Stitches Jr. Jr. (Highmountain, World Quest)
6. Nightwatcher Merayl (Suramar, World Quest)

## Files Updated
- `/PetWeaver/PetWeaver.toc` - Fixed comment syntax
- `/PetWeaver/PetWeaver.lua` - Fixed load timing, added debug logging
- `/release/PetWeaver/` - Updated with latest fixes

## If Still Not Working

If you still don't see teams after `/reload`, check:
1. Make sure you're looking at the right WoW installation (Classic vs Retail)
2. Look for any Lua errors (install BugSack addon to catch them)
3. Share the exact output from the chat log so I can diagnose further
