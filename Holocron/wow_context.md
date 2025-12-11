# WoW Retail (11.x) API Cheat Sheet

## Critical Rules
- **Version:** Retail 11.0.7 (The War Within)
- **No Globals:** Do not use `getglobal`. Use `_G[]` or local variables.
- **Bags:** Use `C_Container` (e.g., `C_Container.GetContainerNumSlots`). DO NOT use `GetContainerNumSlots`.
- **Timer:** Use `C_Timer.After(seconds, func)` instead of `OnUpdate` frames for simple delays.

## Basic Structure
Every addon needs:
1. `AddonName.toc` (Metadata)
2. `core.lua` (Logic)

## Hello World Pattern
```lua
local addonName, addonTable = ...
local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_LOGIN")
f:SetScript("OnEvent", function(self, event)
    print("|cff00ff00" .. addonName .. " loaded!|r")
end)
