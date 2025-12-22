-- SKILLWEAVER UNIVERSAL DRIVER v4.0
-- SUPPORTS ALL 13 CLASSES & 40 SPECS (Dynamic Detection)
-- PROTOCOL: DARK MATTER (GAIN 0.90)

local ADDON_NAME = "SkillWeaver"
local f = CreateFrame("Frame", ADDON_NAME .. "Frame", UIParent)
f:SetSize(32, 1)
f:SetPoint("BOTTOMLEFT", UIParent, "BOTTOMLEFT", 0, 0)
f:SetFrameStrata("BACKGROUND") 
f:SetScale(1 / UIParent:GetEffectiveScale())

-- BASELINE GRAY
local BASE = 0.08

local pixels = {}
for i = 0, 31 do
    local t = f:CreateTexture(nil, "OVERLAY")
    t:SetSize(1, 1)
    t:SetPoint("LEFT", f, "LEFT", i, 0)
    t:SetColorTexture(BASE, BASE, BASE)
    pixels[i] = t
end

-- ENCODER (0.90 GAIN)
local function SetPixel(index, value)
    local offset = (value / 255) * 0.90
    pixels[index]:SetColorTexture(BASE, BASE, BASE + offset)
end

-- DYNAMIC SECONDARY POWER MAP
local SEC_MAP = {
    [2] = 9, -- Paladin (Holy Power)
    [4] = 4, -- Rogue (Combo Points)
    [5] = 13, -- Priest (Insanity)
    [6] = 5, -- Death Knight (Runes)
    [8] = 16, -- Mage (Arcane Charges)
    [9] = 7, -- Warlock (Soul Shards)
    [10] = 12, -- Monk (Chi)
    [11] = 4, -- Druid (Combo Points)
    [13] = 22, -- Evoker (Essence)
}

-- GENERIC SNAPSHOT LIST (Major Buffs Only)
local SNAP_BUFFS = {
    [32645]=true, [185422]=true, [113860]=true, [10060]=true, [5217]=true
}

f:SetScript("OnUpdate", function()
    -- 0: PILOT SIGNAL
    pixels[0]:SetColorTexture(BASE, BASE, 0.4)

    -- 1: DYNAMIC SPEC HASH
    -- Automatically detects current Spec & Class
    local specIdx = GetSpecialization() or 0
    local _, _, classId = UnitClass("player")
    local hash = (classId * 10) + specIdx
    SetPixel(1, hash + 0.5)

    -- 2: COMBAT
    SetPixel(2, UnitAffectingCombat("player") and 255 or 0)

    -- 3: PLAYER HP
    SetPixel(3, (UnitHealth("player") / UnitHealthMax("player")) * 255)

    -- 4: TARGET HP
    local thp = 0
    if UnitExists("target") then thp = UnitHealth("target") / UnitHealthMax("target") end
    SetPixel(4, thp * 255)

    -- 5: TARGET VALID
    SetPixel(5, (UnitExists("target") and UnitCanAttack("player", "target")) and 255 or 0)

    -- 7: PRIMARY RESOURCE
    local power = UnitPower("player")
    local max = UnitPowerMax("player")
    SetPixel(7, (max > 0) and (power / max * 255) or 0)

    -- 8: UNIVERSAL SECONDARY RESOURCE
    local secId = SEC_MAP[classId]
    if secId then
        local secVal = UnitPower("player", secId)
        -- Scaled x25 (Max 10 points = 250)
        SetPixel(8, math.min(255, secVal * 25))
    else
        SetPixel(8, 0)
    end

    -- 16: DEBUFF MASK (Sample)
    local debuffState = 0
    -- (Logic omitted for brevity, add generic debuff checks here)
    SetPixel(16, debuffState * 10)

    -- 22: PET STATUS
    local php = 0
    if UnitExists("pet") then php = UnitHealth("pet") / UnitHealthMax("pet") end
    SetPixel(22, php * 255)

    -- 30: SNAPSHOT
    local snap = 0
    for i=1,40 do
        local _, _, _, _, _, _, _, _, _, id = UnitBuff("player", i)
        if not id then break end
        if SNAP_BUFFS[id] then snap = 255 break end
    end
    SetPixel(30, snap)
end)
