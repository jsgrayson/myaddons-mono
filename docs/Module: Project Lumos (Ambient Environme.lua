Module: Project Lumos (Ambient Environment)

1. Overview

Uses the Jetson Orin Nano to control room lighting (WLED/Hue) based on in-game context (Zone, Health, Combat Events).

2. Implementation

Step A: The Trigger Addon (Holocron_Status.lua)

A minimal Lua script that writes status to SavedVariables on specific events.

local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_REGEN_DISABLED") -- Combat Start
f:RegisterEvent("PLAYER_REGEN_ENABLED")  -- Combat End
f:RegisterEvent("ZONE_CHANGED_NEW_AREA")
f:RegisterEvent("UNIT_HEALTH")

f:SetScript("OnEvent", function(self, event)
    Holocron_Status = {
        ["combat"] = UnitAffectingCombat("player"),
        ["health"] = UnitHealth("player") / UnitHealthMax("player"),
        ["zone"] = GetRealZoneText(),
        ["timestamp"] = GetTime()
    }
end)


Step B: The Controller Script (Jetson)

The Jetson reads the file update (synced via Bridge) and hits the WLED API.

# Pseudo-code for Jetson
def update_lights(status):
    if status['health'] < 0.20:
        wled.set_effect("Breathe", color="RED", speed="FAST")
    elif status['combat']:
        wled.set_color("WARM_WHITE")
    elif status['zone'] == "Icecrown":
        wled.set_color("ICY_BLUE")
    else:
        wled.set_color("DEFAULT_AMBIENT")


Module: The Timekeeper (Analytics & Backup)

1. Overview

Provides granular version control for UI settings and financial analytics for gameplay sessions.

2. Implementation

Step A: The Git Engine (R720)

Repo: /opt/holocron/backups/user_account

Automation: Every time the Bridge script uploads a file, the Server commits it to Git.

git add .

git commit -m "Auto-Sync: Character Logout - [Timestamp]"

Step B: The Analytics Engine (SQL)

Table: session_history

session_id, start_time, end_time, start_gold, end_gold, items_looted_json.

Logic: Net_Worth_Change = (End_Gold + Value_of_New_Items) - (Start_Gold).

Step C: The Dashboard "Undo"

UI: A timeline slider on the web dashboard.

Action: Selecting a point in time executes a git checkout command on the server, zips the WTF folder, and sends it to the Bridge for download.