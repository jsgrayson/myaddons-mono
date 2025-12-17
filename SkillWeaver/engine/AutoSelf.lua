-- engine/AutoSelf.lua
local AutoSelf = {}
local Defaults = require("policies.healing.AutoSelfDefaults")
local Buttons = require("core.BindableButtons")
local SpecProfiles = require("policies.healing.SpecProfiles")

local lastFire = 0
local ICD = 2.0 -- prevent double-firing too quickly

function AutoSelf:Check()
    -- Global gate
    if not SkillWeaverDB or not SkillWeaverDB.AutoSelfEnabled then return end
    
    -- Cooldown gate
    local now = GetTime()
    if now - lastFire < ICD then return end

    -- Combat gate (usually you only want this in combat? User implied emergency)
    -- "This is exactly how many tank addons auto-fire defensives."
    -- We'll check combat to be safe/sane, but technically emergency could happen outside?
    -- Keeping it simple for now: Always check if enabled.

    -- Get Threshold
    local specKey = (SkillWeaver and SkillWeaver.GetCurrentSpecKey and SkillWeaver:GetCurrentSpecKey())
    if not specKey then return end

    local threshold = 0
    
    -- 1. Try Profile override
    local profile = SpecProfiles[specKey]
    if profile and profile.SELF and profile.SELF.auto and profile.SELF.auto.enabled then
        threshold = profile.SELF.auto.healthBelow or 0
    else
        -- 2. Fallback to Defaults
        local def = Defaults:GetDefaultsForSpec(specKey)
        if def and def.enabled then
            threshold = def.healthBelow or 0
        end
    end

    if threshold <= 0 then return end

    -- Check Health
    local hp = UnitHealth("player")
    local hpMax = UnitHealthMax("player")
    if hpMax <= 0 then return end
    local pct = (hp / hpMax) * 100

    if pct < threshold then
        -- Alert! (Cannot Click() in combat due to WoW API restrictions)
        -- We provide a "Driver Assist" warning instead.
        
        -- Flash screen or text
        if RaidWarningFrame then
            RaidNotice_AddMessage(RaidWarningFrame, "USE SELF SAVE!", ChatTypeInfo["RAID_WARNING"])
        end
        
        -- Audible Warning
        PlaySound(SOUNDKIT.ALARM_CLOCK_WARNING_2 or 12867) 
        
        lastFire = now
        
        -- Optional: Flash the frame if possible (requires LibButtonGlow or similar, skipping for now)
        if SkillWeaver then
             SkillWeaver:Print("|cffff0000CRITICAL HEALTH! USE SELF SAVE!|r")
        end
    end
end

-- Wire up events
local f = CreateFrame("Frame")
f:RegisterEvent("UNIT_HEALTH")
f:RegisterEvent("PLAYER_REGEN_DISABLED")

f:SetScript("OnEvent", function(_, event, unit)
    if event == "UNIT_HEALTH" then
        if unit == "player" then
            AutoSelf:Check()
        end
    elseif event == "PLAYER_REGEN_DISABLED" then
        -- Check immediately on entering combat
        AutoSelf:Check()
    end
end)

-- Throttle checker (heartbeat) just in case UNIT_HEALTH misses or massive damage spikes frame-perfect
C_Timer.NewTicker(0.5, function()
    AutoSelf:Check()
end)

return AutoSelf
