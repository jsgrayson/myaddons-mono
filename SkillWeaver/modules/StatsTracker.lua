--========================================================--
-- SkillWeaver - Statistics Tracker
-- Tracks combat performance and feature usage
--========================================================--

local ADDON_NAME, SkillWeaver = ...
local StatsTracker = {}
SkillWeaver.StatsTracker = StatsTracker

StatsTracker.Session = {
    casts = 0,
    interrupts = 0,
    dispels = 0,
    deaths = 0,
    combatTime = 0,
}

local combatStart = 0

------------------------------------------------------------
-- Track Cast
------------------------------------------------------------
function StatsTracker:TrackCast(spellName)
    self.Session.casts = self.Session.casts + 1
    
    -- Update Persistent Stats
    if SkillWeaver.GlobalSettings and SkillWeaver.GlobalSettings.usageStats then
        SkillWeaver.GlobalSettings.usageStats.totalCasts = (SkillWeaver.GlobalSettings.usageStats.totalCasts or 0) + 1
    end
end

------------------------------------------------------------
-- Combat Tracking
------------------------------------------------------------
local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_REGEN_DISABLED") -- Combat Start
f:RegisterEvent("PLAYER_REGEN_ENABLED")  -- Combat End
f:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")

f:SetScript("OnEvent", function(self, event, ...)
    if event == "PLAYER_REGEN_DISABLED" then
        combatStart = GetTime()
    elseif event == "PLAYER_REGEN_ENABLED" then
        if combatStart > 0 then
            local duration = GetTime() - combatStart
            StatsTracker.Session.combatTime = StatsTracker.Session.combatTime + duration
            
            if SkillWeaver.GlobalSettings and SkillWeaver.GlobalSettings.usageStats then
                SkillWeaver.GlobalSettings.usageStats.timeInCombat = (SkillWeaver.GlobalSettings.usageStats.timeInCombat or 0) + duration
            end
            combatStart = 0
        end
    elseif event == "COMBAT_LOG_EVENT_UNFILTERED" then
        local _, subEvent, _, sourceGUID, _, _, _, _, _, _, _, spellID, spellName = CombatLogGetCurrentEventInfo()
        
        if sourceGUID == UnitGUID("player") then
            if subEvent == "SPELL_INTERRUPT" then
                StatsTracker.Session.interrupts = StatsTracker.Session.interrupts + 1
            elseif subEvent == "SPELL_DISPEL" then
                StatsTracker.Session.dispels = StatsTracker.Session.dispels + 1
            end
        end
    end
end)

------------------------------------------------------------
-- Print Report
------------------------------------------------------------
function StatsTracker:PrintSessionReport()
    print("|cff00FF00SkillWeaver Session Report:|r")
    print("  Casts: " .. self.Session.casts)
    print("  Interrupts: " .. self.Session.interrupts)
    print("  Dispels: " .. self.Session.dispels)
    print("  Combat Time: " .. string.format("%.1f", self.Session.combatTime) .. "s")
end

return StatsTracker
