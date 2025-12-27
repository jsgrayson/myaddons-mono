-- SKILLWEAVER OPTICAL UPLINK v24.0 (DARK MATTER)
-- VISION MODULE: WARLOCK - DESTRUCTION
-- PROTOCOL: LOW-OBSERVABLE STEALTH

local ADDON_NAME = "SkillWeaver"
local f = CreateFrame("Frame", ADDON_NAME .. "Frame", UIParent)
f:SetSize(32, 1)
f:SetPoint("BOTTOMLEFT", UIParent, "BOTTOMLEFT", 0, 0)
f:SetFrameStrata("BACKGROUND") -- Hidden behind UI

-- BASELINE GRAY (DARK MATTER)
-- RGB ~20 (Very Dark Gray)
local BASE = 0.08

local pixels = {}
for i = 0, 31 do
    local t = f:CreateTexture(nil, "OVERLAY")
    t:SetSize(1, 1)
    t:SetPoint("LEFT", f, "LEFT", i, 0)
    t:SetColorTexture(BASE, BASE, BASE)
    pixels[i] = t
end

-- DIFFERENTIAL ENCODER
-- Scaling: 0.0-0.3 Offset.
-- Base(0.08) + Offset(0.3) = 0.38 Max Brightness (RGB ~97).
-- This keeps the strip very dark and hard to see.
local function SetPixel(index, value)
    local offset = (value / 255) * 0.3
    pixels[index]:SetColorTexture(BASE, BASE, BASE + offset)
end

-- SNAPSHOT BUFFS
local SNAP_BUFFS = { [113860]=true, [10060]=true }

f:SetScript("OnUpdate", function()
    -- 0: PILOT SIGNAL (DARK BLUE)
    -- RGB(20, 20, 102). Distinct Blue tint, but dark.
    -- Computer sees Blue > Red + 80.
    pixels[0]:SetColorTexture(BASE, BASE, 0.4)

    -- 1: SPEC HASH
    local _, _, classID = UnitClass("player")
    local specIndex = GetSpecialization() or 1
    SetPixel(1, (classID * 10) + specIndex)

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

    -- 7: PRIMARY RESOURCE (Mana)
    local power = UnitPower("player")
    local max = UnitPowerMax("player")
    SetPixel(7, (max > 0) and (power / max * 255) or 0)

    -- 8: SECONDARY RESOURCE (Soul Shards)
    SetPixel(8, math.min(255, UnitPower("player", 7) * 25))

    -- 16: DEBUFF MASK (Root/Snare/Scatter)
    local debuffState = 0
    if C_UnitAuras then
        for i=1,40 do
            local aura = C_UnitAuras.GetAuraDataByIndex("player", i, "HARMFUL")
            if not aura then break end
            if aura.spellId == 339 then debuffState = bit.bor(debuffState, 1) end -- Root example
            if aura.spellId == 213691 then debuffState = bit.bor(debuffState, 4) end -- Scatter
        end
    end
    SetPixel(16, debuffState * 10)

    -- 22: PET STATUS
    local php = 0
    if UnitExists("pet") then
        php = UnitHealth("pet") / UnitHealthMax("pet")
    end
    SetPixel(22, php * 255)

    -- 30: SNAPSHOT (DoT Power)
    local snap = 0
    if C_UnitAuras then
        for i=1,40 do
            local aura = C_UnitAuras.GetAuraDataByIndex("player", i, "HELPFUL")
            if not aura then break end
            if SNAP_BUFFS[aura.spellId] then snap = 255 break end
        end
    end
    SetPixel(30, snap)

end)
