-- SKILLWEAVER UNIVERSAL DRIVER (BEFORE-WORK STATE)
-- PROTOCOL: 218.0 | DOTS: BOOLEAN | SPEC: 3-FORCE

if not SW_Frame then
    SW_Frame = CreateFrame("Frame", "SW_Frame", UIParent)
    SW_Frame:SetSize(64, 1)
    SW_Frame:SetPoint("BOTTOMLEFT", 0, 0)
    SW_Frame:SetFrameStrata("BACKGROUND") 
end
SW_Frame:SetScale(1 / UIParent:GetEffectiveScale())

local p = {}
local BASE = 0.08
local DIV = 218 
local FACTOR = DIV / 255

for i = 0, 31 do
    if not p[i] then
        p[i] = SW_Frame:CreateTexture(nil, "OVERLAY")
        p[i]:SetSize(1, 1)
        p[i]:SetPoint("LEFT", i, 0)
    end
    p[i]:SetColorTexture(BASE, BASE, BASE, 1) 
end

local function SetPixel(idx, val)
    if not p[idx] then return end
    local off = (math.max(0, math.min(255, val or 0)) / 255) * FACTOR
    p[idx]:SetColorTexture(BASE, BASE, BASE + off, 1)
end

-- UNIVERSAL DOT MAPPING BY SPEC
-- Format: SPEC_DOTS[spec_id] = { {spellIds={...}, names={...}, pixel=11}, ... }
-- spec_id = classID * 10 + specIndex (e.g. 53 = Priest Shadow)
local SPEC_DOTS = {
    -- Shadow Priest (53)
    [53] = {
        {spellIds={34914, 402668}, names={"Vampiric Touch"}, pixel=11},
        {spellIds={589, 10894}, names={"Shadow Word: Pain"}, pixel=12},
        {spellIds={2944, 402662}, names={"Devouring Plague"}, pixel=13},
    },
    -- Affliction Warlock (91)
    [91] = {
        {spellIds={980}, names={"Agony"}, pixel=11},
        {spellIds={146739, 172}, names={"Corruption"}, pixel=12},
        {spellIds={316099, 30108}, names={"Unstable Affliction"}, pixel=13},
    },
    -- Feral Druid (112)
    [112] = {
        {spellIds={155722, 1822}, names={"Rake"}, pixel=11},
        {spellIds={1079}, names={"Rip"}, pixel=12},
        {spellIds={106830, 77758}, names={"Thrash"}, pixel=13},
    },
    -- Assassination Rogue (41)
    [41] = {
        {spellIds={703}, names={"Garrote"}, pixel=11},
        {spellIds={1943}, names={"Rupture"}, pixel=12},
        {spellIds={2818, 113780}, names={"Deadly Poison"}, pixel=13},
    },
    -- Unholy DK (63)
    [63] = {
        {spellIds={191587}, names={"Virulent Plague"}, pixel=11},
        {spellIds={194310}, names={"Festering Wound"}, pixel=12},
    },
    -- Balance Druid (111)
    [111] = {
        {spellIds={164812}, names={"Moonfire"}, pixel=11},
        {spellIds={164815, 93402}, names={"Sunfire"}, pixel=12},
    },
    -- Elemental Shaman (71)
    [71] = {
        {spellIds={188389}, names={"Flame Shock"}, pixel=11},
    },
    -- Enhancement Shaman (72)
    [72] = {
        {spellIds={188389}, names={"Flame Shock"}, pixel=11},
    },
    -- Destruction Warlock (93)
    [93] = {
        {spellIds={157736}, names={"Immolate"}, pixel=11},
    },
    -- Demonology Warlock (92)
    [92] = {
        {spellIds={603}, names={"Doom"}, pixel=11},
    },
    -- Subtlety Rogue (43)
    [43] = {
        {spellIds={1943}, names={"Rupture"}, pixel=11},
    },
    -- Outlaw Rogue (42) - no maintenance DoTs
    -- Marksmanship Hunter (32)
    [32] = {
        {spellIds={271788}, names={"Serpent Sting"}, pixel=11},
    },
    -- Survival Hunter (33)
    [33] = {
        {spellIds={259491}, names={"Serpent Sting"}, pixel=11},
        {spellIds={270332, 270339}, names={"Pheromone Bomb", "Shrapnel Bomb"}, pixel=12},
    },
}

-- Build reverse lookup: spellId/name -> {specId, pixel}
local currentSpecId = 0
local currentDotConfig = nil


SW_Frame:SetScript("OnUpdate", function()
    p[0]:SetColorTexture(BASE, BASE, 0.4, 1) -- Heartbeat
    
    local ok, err = pcall(function()
        -- 1. SPEC ID (The Fix that worked)
        -- If priest (5) and spec logic fails/returns 0, default to 3 (Shadow).
        local _, _, classID = UnitClass("player")
        local spec = GetSpecialization()
        if classID == 5 and (not spec or spec == 0) then spec = 3 end
        spec = spec or 1
        
        SetPixel(1, (classID * 10) + spec)
        
        -- 2. BASIC STATE
        SetPixel(2, UnitAffectingCombat("player") and 255 or 0)
        SetPixel(3, (UnitHealth("player") / math.max(1, UnitHealthMax("player"))) * 255)
        
        if UnitExists("target") then
            SetPixel(4, (UnitHealth("target") / math.max(1, UnitHealthMax("target"))) * 255)
            SetPixel(5, UnitCanAttack("player", "target") and 255 or 0)
        end
        
        -- 3. DOTS (DURATION - scaled to 0-255 where 255 = 25.5 seconds)
        -- This enables pandemic refresh (recast at <4.5s remaining)
        
        -- Update spec config if spec changed
        local specId = (classID * 10) + spec
        if specId ~= currentSpecId then
            currentSpecId = specId
            currentDotConfig = SPEC_DOTS[specId]
        end
        
        local dVals = {[11]=0, [12]=0, [13]=0}
        if UnitExists("target") and currentDotConfig then
            -- Helper function to find pixel for a given spellId/name
            local function GetDotPixel(spellId, auraName)
                for _, dotInfo in ipairs(currentDotConfig) do
                    -- Check by spellId first
                    for _, id in ipairs(dotInfo.spellIds) do
                        if id == spellId then return dotInfo.pixel end
                    end
                    -- Fallback to name check
                    for _, name in ipairs(dotInfo.names) do
                        if name == auraName then return dotInfo.pixel end
                    end
                end
                return nil
            end
            
            -- Use AuraUtil.ForEachAura if available (TWW), else legacy UnitAura
            if AuraUtil and AuraUtil.ForEachAura then
                local function CheckAura(aura)
                    if aura.isFromPlayerOrPlayerPet then
                        local idx = GetDotPixel(aura.spellId, aura.name)
                        if idx then
                            -- Calculate remaining duration
                            local remaining = 0
                            if aura.expirationTime and aura.expirationTime > 0 then
                                remaining = aura.expirationTime - GetTime()
                            end
                            -- Scale: 1 second = 10 units (max 25.5s = 255)
                            dVals[idx] = math.max(dVals[idx], math.min(255, remaining * 10))
                        end
                    end
                end
                AuraUtil.ForEachAura("target", "HARMFUL", nil, CheckAura, true)
            else
                -- Legacy API (Classic/Era)
                for i = 1, 40 do
                    local name, _, _, _, _, expirationTime, source, _, _, spellId = UnitAura("target", i, "HARMFUL|PLAYER")
                    if not name then break end
                    if source == "player" or source == "pet" then
                        local idx = GetDotPixel(spellId, name)
                        if idx then
                            local remaining = 0
                            if expirationTime and expirationTime > 0 then
                                remaining = expirationTime - GetTime()
                            end
                            dVals[idx] = math.max(dVals[idx], math.min(255, remaining * 10))
                        end
                    end
                end
            end
        end
        SetPixel(13, dVals[13])
        
        -- CONTENT MODE (P10)
        -- 0=Raid, 1=Mythic+, 2=Delve, 3=PvP
        local modeIdx = 0
        local modeStr = _G.SkillWeaver_SelectedMode or "raid"
        if modeStr == "mythic" then modeIdx = 1
        elseif modeStr == "delve" then modeIdx = 2
        elseif modeStr == "pvp" then modeIdx = 3
        end
        SetPixel(10, modeIdx * 64)

        -- 4. MULTI-DOT NAMEPLATE SCAN (P20-P21)
        local missingCount = 0
        local totalPlates = 0
        if C_NamePlate and C_NamePlate.GetNamePlates then
            for _, nameplate in pairs(C_NamePlate.GetNamePlates()) do
                local unit = nameplate.namePlateUnitToken
                -- Only count: attackable, not dead, not current target
                if unit and UnitCanAttack("player", unit) 
                   and not UnitIsDead(unit)
                   and unit ~= "target" then
                    totalPlates = totalPlates + 1
                    local hasPlayerDot = false
                    if AuraUtil and AuraUtil.ForEachAura then
                        AuraUtil.ForEachAura(unit, "HARMFUL", nil, function(aura)
                            if aura.isFromPlayerOrPlayerPet then
                                hasPlayerDot = true
                                return true
                            end
                        end, true)
                    else
                        for i = 1, 40 do
                            local name, _, _, _, _, _, source = UnitAura(unit, i, "HARMFUL|PLAYER")
                            if not name then break end
                            if source == "player" or source == "pet" then
                                hasPlayerDot = true
                                break
                            end
                        end
                    end
                    if not hasPlayerDot then
                        missingCount = missingCount + 1
                    end
                end
            end
        end
        SetPixel(20, math.min(255, missingCount * 25))  -- 0-10 enemies scaled
        SetPixel(21, totalPlates * 25)  -- Debug: total hostile nameplates visible

        -- 5. RESOURCES
        -- P7: Primary Resource (Health/Mana/Focus/Rage/Energy etc.)
        local pMax = UnitPowerMax("player")
        SetPixel(7, (pMax > 0 and UnitPower("player") / pMax or 0) * 255)
        
        -- P8: Secondary Resource (Combo Points, Holy Power, Chi, Soul Shards, Arcane Charges, Essence)
        local secRes = 0
        if classID == 4 or (classID == 11 and spec == 2) then -- Rogue or Feral Druid: Combo Points
            secRes = UnitPower("player", 4) * 25
        elseif classID == 2 then -- Paladin: Holy Power
            secRes = UnitPower("player", 9) * 25
        elseif classID == 9 then -- Warlock: Soul Shards
            secRes = UnitPower("player", 7) * 25
        elseif classID == 10 then -- Monk: Chi
            secRes = UnitPower("player", 12) * 25
        elseif classID == 8 and spec == 1 then -- Arcane Mage: Arcane Charges
            secRes = UnitPower("player", 16) * 25
        elseif classID == 13 then -- Evoker: Essence
            secRes = UnitPower("player", 19) * 25
        elseif classID == 5 and spec == 3 then -- Shadow Priest: Insanity
            secRes = UnitPower("player", 13) * 2.55 -- 100 Insanity = 255
        end
        SetPixel(8, secRes)

        -- 6. PROC DETECTION (P14-P15)
        -- P14: Mind Blast Reset Procs (Shadowy Insight ONLY - resets Mind Blast CD)
        -- P15: Mind Flay: Insanity procs (Surge of Insanity - empowers Mind Flay)
        local mbResetProc = false
        local mfInsanityProc = false
        if specId == 53 then  -- Shadow Priest
            if AuraUtil and AuraUtil.ForEachAura then
                AuraUtil.ForEachAura("player", "HELPFUL", nil, function(aura)
                    -- Shadowy Insight (resets Mind Blast cooldown)
                    if aura.spellId == 375981 or aura.spellId == 87160 or
                       aura.name == "Shadowy Insight" then
                        mbResetProc = true
                    end
                    -- Surge of Insanity / Mind Flay: Insanity (empowers Mind Flay, not Mind Blast)
                    if aura.spellId == 391401 or aura.spellId == 407468 or
                       aura.name == "Surge of Insanity" or aura.name == "Mind Flay: Insanity" then
                        mfInsanityProc = true
                    end
                end, true)
            else
                for i = 1, 40 do
                    local name, _, _, _, _, _, _, _, _, spellId = UnitAura("player", i, "HELPFUL")
                    if not name then break end
                    if spellId == 375981 or name == "Shadowy Insight" then
                        mbResetProc = true
                    end
                    if spellId == 391401 or name == "Surge of Insanity" then
                        mfInsanityProc = true
                    end
                end
            end
        end
        SetPixel(14, mbResetProc and 255 or 0)
        SetPixel(15, mfInsanityProc and 255 or 0)  -- For future use with Mind Flay: Insanity

        -- 7. SENSORS
        SetPixel(17, IsKeyDown("2") and 255 or 0)
        local _, _, _, _, _, _, _, kick = UnitCastingInfo("target")
        SetPixel(18, (kick == false) and 255 or 0)
        SetPixel(19, IsStealthed() and 255 or 0)
        -- 8. RANGE DETECTION (P6) - Dynamic range for ground-targeting offset
        -- Uses spell range checks to bracket distance
        local range = 40  -- Default to max
        if UnitExists("target") and UnitCanAttack("player", "target") then
            -- Check from close to far, first TRUE sets the bracket
            -- Using common spells that most casters have (adjust per spec if needed)
            if CheckInteractDistance("target", 3) then  -- ~10 yards (duel range)
                range = 8
            elseif CheckInteractDistance("target", 2) then  -- ~11 yards (trade range)
                range = 12
            elseif CheckInteractDistance("target", 4) then  -- ~28 yards (follow range)
                range = 25
            elseif IsSpellInRange("Shadow Word: Pain", "target") == 1 then  -- 40 yards
                range = 35
            end
        end
        SetPixel(6, range * 4.25)
    end)
    
    SetPixel(31, 255)
end)

print("|cff00ffccColorProfile|r: Restore Complete.")
