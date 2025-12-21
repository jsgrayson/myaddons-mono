-- SkillWeaver_Engine/addon/ColorProfile_Lib.lua
-- GRAYSCALE PROTOCOL (Mac/Colorblind Safe)

local f = CreateFrame("Frame", nil, UIParent)
f:SetSize(32, 1)
f:SetPoint("BOTTOMLEFT", 0, 0)
f:SetFrameStrata("BACKGROUND")

local c = {}
for i=0, 32 do
    c[i] = f:CreateTexture(nil, "BACKGROUND")
    c[i]:SetSize(1, 1)
    c[i]:SetPoint("LEFT", f, "LEFT", i, 0)
end

local function GetDebuffTime(spellName)
    local expirationTime = select(5, AuraUtil.FindAuraByName(spellName, "target", "PLAYER|HARMFUL"))
    if not expirationTime then return 0 end
    local remaining = expirationTime - GetTime()
    return (remaining > 0) and remaining or 0
end

f:SetScript("OnUpdate", function()
    -- [0] Handshake: Pure White (Reference)
    c[0]:SetColorTexture(1, 1, 1, 1) 
    
    -- [1] Spec ID: Grayscale (Value / 1000)
    local s = GetSpecializationInfo(GetSpecialization()) or 0
    local sVal = s/1000
    c[1]:SetColorTexture(sVal, sVal, sVal, 1) 

    -- [2] Combat Flag: White = Yes, Black = No
    local inCombat = UnitAffectingCombat("player") and 1 or 0
    c[2]:SetColorTexture(inCombat, inCombat, inCombat, 1)

    -- [3] Stealth Flag: White = Yes
    local isStealthed = IsStealthed() and 1 or 0
    c[3]:SetColorTexture(isStealthed, isStealthed, isStealthed, 1)

    -- [4] Target Exists: White = Yes
    local targetExists = UnitExists("target") and 1 or 0
    c[4]:SetColorTexture(targetExists, targetExists, targetExists, 1)

    -- [5] Garrote Remaining (0-10s mapped to 0-1)
    local garroteRem = GetDebuffTime("Garrote") / 10
    if garroteRem > 1 then garroteRem = 1 end
    c[5]:SetColorTexture(garroteRem, garroteRem, garroteRem, 1)

    -- [6] Rupture Remaining (0-30s mapped to 0-1)
    local ruptureRem = GetDebuffTime("Rupture") / 30
    if ruptureRem > 1 then ruptureRem = 1 end
    c[6]:SetColorTexture(ruptureRem, ruptureRem, ruptureRem, 1)

    -- [7] Energy (0-100% mapped to 0-1)
    local energy = UnitPower("player", 3) or 0
    local energyMax = UnitPowerMax("player", 3) or 100
    local eVal = energy / energyMax
    c[7]:SetColorTexture(eVal, eVal, eVal, 1)

    -- [8] Combo Points (0-100% mapped to 0-1)
    -- Assumes Max CP is 7 for Rogue
    local cp = UnitPower("player", 4) or 0
    local cpVal = cp / 7
    c[8]:SetColorTexture(cpVal, cpVal, cpVal, 1)
end)
