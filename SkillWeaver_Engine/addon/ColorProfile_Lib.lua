-- SKILLWEAVER UNIVERSAL DRIVER v4.1 (BOOSTED)
-- SUPPORTS ALL 13 CLASSES & 60 SPECS (Dynamic Detection)
-- PROTOCOL: DARK MATTER (GAIN 0.90)

-- 1. Setup Frame
if not SW_Frame then
    SW_Frame = CreateFrame("Frame", "SW_Frame", UIParent)
    SW_Frame:SetSize(64, 1)
    SW_Frame:SetPoint("BOTTOMLEFT", 0, 0)
    SW_Frame:SetFrameStrata("BACKGROUND") 
end

-- 2. PIXEL-PERFECT SCALING
SW_Frame:SetScale(1 / UIParent:GetEffectiveScale())

-- 3. Initialize the Pixel Table
local p = {}
local BASE = 0.08
for i = 0, 31 do
    if not p[i] then
        p[i] = SW_Frame:CreateTexture(nil, "OVERLAY")
        p[i]:SetSize(1, 1)
        p[i]:SetPoint("LEFT", i, 0)
    end
    p[i]:SetColorTexture(BASE, BASE, BASE, 1) 
end

-- 4. HIGH-GAIN ENCODER (0.90)
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
    
    -- P1: Dynamic Spec Hash (Class * 10 + Spec)
    local _, _, classId = UnitClass("player")
    local specIdx = GetSpecialization() or 3 -- Fallback to 3 if unknown
    if specIdx == 0 then specIdx = 3 end
    SetPixel(1, (classId * 10.0) + specIdx)
    
    -- P2: Combat Status
    SetPixel(2, UnitAffectingCombat("player") and 255 or 0)

    -- P3: Player HP
    SetPixel(3, (UnitHealth("player") / UnitHealthMax("player")) * 255)

    -- P4: Target HP
    local thp = 0
    if UnitExists("target") then thp = UnitHealth("target") / UnitHealthMax("target") end
    SetPixel(4, thp * 255)

    -- P5: Target Valid
    SetPixel(5, (UnitExists("target") and UnitCanAttack("player", "target")) and 255 or 0)

    -- P7: Primary Resource (Mana/Energy/Rage)
    local pow = UnitPower("player") / math.max(1, UnitPowerMax("player"))
    SetPixel(7, pow * 255)

    -- P8: Universal Secondary Resource (Scaled 25x)
    local secId = SEC_MAP[classId]
    if secId then
        SetPixel(8, math.min(255, UnitPower("player", secId) * 25))
    else
        SetPixel(8, 0)
    end

    -- P16: Debuff Mask (Reserved for expansion)
    SetPixel(16, 0)

    -- P22: Pet Status
    local php = 0
    if UnitExists("pet") then php = UnitHealth("pet") / UnitHealthMax("pet") end
    SetPixel(22, php * 255)

    -- P30: Snapshot (Buff Tracker)
    local snp = 0
    for i=1,40 do
        local aura = C_UnitAuras.GetBuffDataByIndex("player", i)
        if not aura then break end
        if SNAPS[aura.spellId] then snp = 255 break end
    end
    SetPixel(30, snp)
end)
