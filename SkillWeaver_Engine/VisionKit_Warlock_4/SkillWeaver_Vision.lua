-- SKILLWEAVER OPTICAL UPLINK v25.7 (STEALTH-STABLE)
-- VISION MODULE: WARLOCK - DESTRUCTION
-- PROTOCOL: DARK MATTER (GAIN 0.5)

local ADDON_NAME = "SkillWeaver"
local f = CreateFrame("Frame", ADDON_NAME .. "Frame", UIParent)
f:SetSize(32, 1)
f:SetPoint("BOTTOMLEFT", UIParent, "BOTTOMLEFT", 0, 0)
f:SetFrameStrata("BACKGROUND") -- SAFE: Behind UI/Chat

-- PIXEL PERFECT SCALING
-- Ensure 1px frame = 1 physical pixel, regardless of UI Scale
f:SetScale(1 / UIParent:GetEffectiveScale())

-- BASELINE GRAY (DARK MATTER)
local BASE = 0.08
local TARGET_HASH = 91

local pixels = {}
for i = 0, 31 do
    local t = f:CreateTexture(nil, "OVERLAY")
    t:SetSize(1, 1)
    t:SetPoint("LEFT", f, "LEFT", i, 0)
    t:SetColorTexture(BASE, BASE, BASE)
    pixels[i] = t
end

-- DIFFERENTIAL ENCODER (HIGH GAIN)
-- Gain increased to 0.5 to fix reading errors on some panels
-- Max Brightness = 0.08 + 0.5 = 0.58 (~148 RGB) - Still Dark Gray
local function SetPixel(index, value)
    local offset = (value / 255) * 0.5
    pixels[index]:SetColorTexture(BASE, BASE, BASE + offset)
end

-- SNAPSHOT BUFFS
local SNAP_BUFFS = { [113860]=true, [10060]=true }

f:SetScript("OnUpdate", function()
    -- 0: PILOT SIGNAL (DARK BLUE)
    -- RGB(20, 20, 102). Diff > 60.
    pixels[0]:SetColorTexture(BASE, BASE, 0.4)

    -- 1: SPEC HASH (STABILIZED)
    -- Added 0.5 rounding buffer
    SetPixel(1, TARGET_HASH + 0.5)

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
    for i=1,40 do
        local _, _, _, _, _, _, _, _, _, id = UnitDebuff("player", i)
        if not id then break end
        if id == 339 then debuffState = bit.bor(debuffState, 1) end -- Root example
        if id == 213691 then debuffState = bit.bor(debuffState, 4) end -- Scatter
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
    for i=1,40 do
        local _, _, _, _, _, _, _, _, _, id = UnitBuff("player", i)
        if not id then break end
        if SNAP_BUFFS[id] then snap = 255 break end
    end
    SetPixel(30, snap)

end)
