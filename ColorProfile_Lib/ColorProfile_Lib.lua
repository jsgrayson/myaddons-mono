-- SKILLWEAVER UNIVERSAL DRIVER v4.2 (FIXED)
-- SUPPORTS ALL CLASSES & SPECS
-- PROTOCOL: DARK MATTER

-- 1. Setup Frame
if not SW_Frame then
    SW_Frame = CreateFrame("Frame", "SW_Frame", UIParent)
    SW_Frame:SetSize(64, 1)
    SW_Frame:SetPoint("BOTTOMLEFT", 0, 0)
    SW_Frame:SetFrameStrata("BACKGROUND") 
end

-- 2. PIXEL-PERFECT SCALING
SW_Frame:SetScale(1 / UIParent:GetEffectiveScale())

-- 3. Initialize the Pixel Table (32 Slots)
local p = {}
local BASE = 0.08 -- Base gray to prevent black-screen filtering
for i = 0, 31 do
    if not p[i] then
        p[i] = SW_Frame:CreateTexture(nil, "OVERLAY")
        p[i]:SetSize(1, 1)
        p[i]:SetPoint("LEFT", i, 0)
    end
    p[i]:SetColorTexture(BASE, BASE, BASE, 1) 
end

-- 4. HIGH-GAIN ENCODER
-- Maps 0-255 values into the Blue channel over the BASE gray
local function SetPixel(idx, val)
    local off = (math.max(0, math.min(255, val)) / 255) * 0.90
    p[idx]:SetColorTexture(BASE, BASE, BASE + off, 1)
end

-- 5. DYNAMIC SECONDARY POWER MAP
local SEC_MAP = {
    [2] = 9,  -- Paladin (Holy Power)
    [4] = 4,  -- Rogue (Combo Points)
    [5] = 13, -- Priest (Insanity)
    [6] = 5,  -- Death Knight (Runes)
    [8] = 16, -- Mage (Arcane Charges)
    [9] = 7,  -- Warlock (Soul Shards)
    [10] = 12, -- Monk (Chi)
    [11] = 4,  -- Druid (Combo Points)
    [13] = 22, -- Evoker (Essence)
}

-- 6. MAJOR BUFF SNAPSHOT LIST
local SNAPS = { 
    [32645]=true, [185422]=true, [113860]=true, [10060]=true, [5217]=true,
    [113858]=true, [121471]=true, [13750]=true
} 

-- 7. The Update Loop
SW_Frame:SetScript("OnUpdate", function()
    -- P0: Pilot Heartbeat (Steady 0.4 Blue)
    p[0]:SetColorTexture(BASE, BASE, 0.4, 1) 
    
    -- P1: Dynamic Spec Hash (ClassID * 10 + SpecIndex)
    local _, _, classID = UnitClass("player")
    local specIndex = GetSpecialization() or 1
    local customID = (classID * 10) + specIndex
    SetPixel(1, customID)
    
    -- P2: Combat Status
    SetPixel(2, UnitAffectingCombat("player") and 255 or 0)

    -- P3: Player HP
    local hp = UnitHealth("player")
    local hpMax = UnitHealthMax("player")
    SetPixel(3, (hpMax > 0 and (hp / hpMax) or 1) * 255)

    -- P4: Target HP
    local thp = 0
    if UnitExists("target") then 
        local thpVal = UnitHealth("target")
        local thpMax = UnitHealthMax("target")
        if thpMax > 0 then thp = thpVal / thpMax end
    end
    SetPixel(4, thp * 255)

    -- P5: Target Valid
    SetPixel(5, (UnitExists("target") and UnitCanAttack("player", "target")) and 255 or 0)

    -- P7: Primary Resource
    local powMax = UnitPowerMax("player")
    local pow = (powMax > 0 and UnitPower("player") / powMax or 0)
    SetPixel(7, pow * 255)

    -- P8: Universal Secondary Resource (Scaled 25x)
    local secId = SEC_MAP[classID]
    if secId then
        SetPixel(8, math.min(255, UnitPower("player", secId) * 25))
    else
        SetPixel(8, 0)
    end

    -- P6: Target Range (in yards, clamped to 40)
    local range = 0
    if UnitExists("target") and IsSpellInRange("Shadow Word: Pain", "target") == 1 then
        -- Use CheckInteractDistance for rough range or default
        local minRange, maxRange = C_Spell.GetSpellRange and C_Spell.GetSpellRange(589) or nil, nil
        if CheckInteractDistance("target", 3) then range = 10  -- ~10 yards
        elseif CheckInteractDistance("target", 2) then range = 20 -- ~20 yards
        elseif CheckInteractDistance("target", 1) then range = 30 -- ~30 yards  
        else range = 40 end
    end
    SetPixel(6, range * 6.375) -- Scale: 40 yards = 255
    
    -- P9: NEARBY ENEMIES COUNT (from visible nameplates)
    local enemyCount = 0
    local nameplates = C_NamePlate.GetNamePlates() or {}
    for _, plate in ipairs(nameplates) do
        local unit = plate.namePlateUnitToken
        if unit and UnitExists(unit) and UnitCanAttack("player", unit) and not UnitIsDead(unit) then
            enemyCount = enemyCount + 1
        end
    end
    SetPixel(9, math.min(255, enemyCount * 25)) -- Scale: 10 enemies = 250

    -- P10: ENEMIES WITH OUR DOTS (dotted count)
    -- Spec-aware DoT tracking for multidot specs
    local DOT_LIST = {
        -- Shadow Priest (53)
        ["Vampiric Touch"] = true, ["Shadow Word: Pain"] = true,
        -- Affliction Warlock (91)
        ["Agony"] = true, ["Corruption"] = true, ["Unstable Affliction"] = true, ["Siphon Life"] = true,
        -- Assassination Rogue (41)
        ["Rupture"] = true, ["Garrote"] = true, ["Crimson Tempest"] = true,
        -- Feral Druid (11)
        ["Rake"] = true, ["Rip"] = true, ["Thrash"] = true,
    }
    
    local dottedCount = 0
    for _, plate in ipairs(nameplates) do
        local unit = plate.namePlateUnitToken
        if unit and UnitExists(unit) and UnitCanAttack("player", unit) and not UnitIsDead(unit) then
            -- Check if target has ANY of our tracked DoTs
            local hasDot = false
            for dotName, _ in pairs(DOT_LIST) do
                local aura = AuraUtil.FindAuraByName(dotName, unit, "PLAYER|HARMFUL")
                if aura then
                    hasDot = true
                    break
                end
            end
            if hasDot then
                dottedCount = dottedCount + 1
            end
        end
    end
    SetPixel(10, math.min(255, dottedCount * 25)) -- Scale: 10 dotted = 250

    -- P11: TARGET PRIMARY DOT REMAINING (spec-specific)
    -- Uses primary DoT for each spec
    local PRIMARY_DOT = {
        [53] = "Vampiric Touch",    -- Shadow Priest
        [91] = "Agony",              -- Affliction Warlock
        [41] = "Rupture",            -- Assassination Rogue
        [11] = "Rake",               -- Feral Druid
    }
    
    local dotRemaining = 0
    if UnitExists("target") then
        local primaryDot = PRIMARY_DOT[customID] or "Vampiric Touch"
        local aura = C_UnitAuras.GetAuraDataBySpellName("target", primaryDot, "PLAYER|HARMFUL")
        if aura and aura.expirationTime then
            dotRemaining = math.max(0, aura.expirationTime - GetTime())
        end
    end
    SetPixel(11, math.min(255, dotRemaining * 10)) -- Scale: 25.5 sec = 255

    -- P12: TRIGGER SENSOR (Pressed '2')
    SetPixel(12, IsKeyDown("2") and 255 or 0)

    -- P15: STEALTH STATUS
    SetPixel(15, IsStealthed() and 255 or 0)

    -- P30: Snapshot (Buff Tracker using C_UnitAuras)
    local snp = 0
    if C_UnitAuras then
        for i=1, 40 do
            local aura = C_UnitAuras.GetAuraDataByIndex("player", i, "HELPFUL")
            if not aura then break end
            if SNAPS[aura.spellId] then 
                snp = 255 
                break 
            end
        end
    end
    SetPixel(30, snp)
end)

print("|cff00ffccColorProfile_Lib|r: SKILLWEAVER PIXEL DRIVER ACTIVE.")
