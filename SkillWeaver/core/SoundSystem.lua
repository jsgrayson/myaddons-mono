local ADDON_NAME, SkillWeaver = ...

SkillWeaver.SoundSystem = {}
local Sounds = SkillWeaver.SoundSystem

-- Sound file IDs (Blizzard built-in sounds)
Sounds.ALERT_HIGH = 8959      -- Important proc/cooldown
Sounds.ALERT_MED = 569593     -- Medium priority event
Sounds.ALERT_LOW = 567490     -- Low priority notification
Sounds.ACHIEVEMENT = 888      -- Success sound
Sounds.ERROR = 846            -- Error/warning

-- Configuration
Sounds.Config = {
    enabled = true,
    volume = 0.5,  -- 0.0 to 1.0
    cooldownReady = true,
    procAlert = true,
    lowHealth = true,
}

-- Cooldown tracking
Sounds.trackedCooldowns = {}

-- Play a sound
function Sounds:Play(soundID)
    if not self.Config.enabled then return end
    PlaySound(soundID, "Master", false, false)
end

-- Track important cooldowns
function Sounds:TrackCooldown(spellName, soundID)
    if not self.Config.cooldownReady then return end
    
    soundID = soundID or self.ALERT_HIGH
    self.trackedCooldowns[spellName] = {
        sound = soundID,
        wasOnCD = false,
    }
end

-- Check cooldowns (called periodically)
-- Check cooldowns (called periodically)
function Sounds:CheckCooldowns()
    if not self.Config.cooldownReady then return end
    
    for spell, data in pairs(self.trackedCooldowns) do
        local start, duration = 0, 0
        local spellID = tonumber(spell)
        
        -- Resolve Name to ID if needed
        if not spellID then
             local sInfo = C_Spell and C_Spell.GetSpellInfo and C_Spell.GetSpellInfo(spell)
             if sInfo then 
                spellID = sInfo.spellID 
             else
                -- Fallback for Classic/Era where C_Spell might not exist or behave differently?
                -- Assuming Retail 11.0+. If GetSpellInfo global is gone, strictly depend on C_Spell
             end
        end
        
        -- Get Cooldown Info
        if spellID and C_Spell and C_Spell.GetSpellCooldown then
             local info = C_Spell.GetSpellCooldown(spellID)
             if info then
                 start = info.startTime
                 duration = info.duration
             end
        elseif _G.GetSpellCooldown then
            -- Legacy Fallback
            start, duration = _G.GetSpellCooldown(spell)
        end
        
        if start and duration then
            local isOnCD = (start > 0 and duration > 1.5)
            
            -- Cooldown just finished
            if data.wasOnCD and not isOnCD then
                self:Play(data.sound)
            end
            
            data.wasOnCD = isOnCD
        end
    end
end

-- Alert for low health
function Sounds:AlertLowHealth(threshold)
    if not self.Config.lowHealth then return end
    threshold = threshold or 30
    
    local health = UnitHealth("player")
    local maxHealth = UnitHealthMax("player")
    if maxHealth > 0 then
        local percent = (health / maxHealth) * 100
        if percent < threshold and percent > 0 then
            self:Play(self.ALERT_HIGH)
        end
    end
end

-- Alert for proc
function Sounds:AlertProc(buffName)
    if not self.Config.procAlert then return end
    
    if AuraUtil and AuraUtil.FindAuraByName then
        local hasAura = AuraUtil.FindAuraByName(buffName, "player")
        if hasAura then
            self:Play(self.ALERT_MED)
        end
    end
end

-- Initialize
local frame = CreateFrame("Frame")
frame.elapsed = 0
frame:SetScript("OnUpdate", function(self, elapsed)
    self.elapsed = self.elapsed + elapsed
    if self.elapsed > 0.5 then  -- Check every 0.5s
        Sounds:CheckCooldowns()
        self.elapsed = 0
    end
end)

-- Auto-track common important cooldowns for each class
frame:RegisterEvent("PLAYER_LOGIN")
frame:SetScript("OnEvent", function()
    local class = select(2, UnitClass("player"))
    
    if class == "WARRIOR" then
        Sounds:TrackCooldown("Avatar")
        Sounds:TrackCooldown("Recklessness")
    elseif class == "PALADIN" then
        Sounds:TrackCooldown("Avenging Wrath")
        Sounds:TrackCooldown("Crusade")
    elseif class == "PRIEST" then
        Sounds:TrackCooldown("Power Infusion")
    end
end)
