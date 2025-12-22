-- SkillWeaver_Addon.lua
-- AUTOMATICALLY GENERATED FOR: DESTRUCTION
-- PROTOCOL v22.0 (STEALTH PHANTOM)
local ADDON_NAME = "SkillWeaver"
local f = CreateFrame("Frame", ADDON_NAME .. "Frame", UIParent)
f:SetSize(32, 1) 
f:SetPoint("BOTTOMLEFT", UIParent, "BOTTOMLEFT", 0, 0)
f:SetFrameStrata("BACKGROUND") 

local DANGEROUS = { ["Polymorph"]=true, ["Cyclone"]=true, ["Hex"]=true, ["Fear"]=true, ["Chaos Bolt"]=true, ["Convoke the Spirits"]=true, ["The Hunt"]=true, ["Mind Control"]=true, ["Repentance"]=true, ["Sleep Walk"]=true, ["Divine Hymn"]=true, ["Ray of Hope"]=true, ["Greater Pyroblast"]=true, ["Void Torrent"]=true, ["Penance"]=true, ["Tranquility"]=true }

local pixels = {}
for i = 0, 31 do
    local t = f:CreateTexture(nil, "OVERLAY")
    t:SetSize(1, 1)
    t:SetPoint("LEFT", f, "LEFT", i, 0)
    -- BASELINE: 10% Gray. This is our "Zero".
    t:SetColorTexture(0.1, 0.1, 0.1)
    pixels[i] = t
end

-- STEALTH PROTOCOL: Encode data in Blue channel offset
local function SetPixel(index, value)
    local base = 0.1
    local diff = value / 255
    -- R=Base, G=Base, B=Base + Data
    -- The "Reading" engine will subtract R from B to get Data.
    -- This cancels out Gamma/Brightness/NightLight settings.
    pixels[index]:SetColorTexture(base, base, base + diff)
end

f:SetScript("OnUpdate", function()
    -- 0: Calibration (Always 0, used as noise floor)
    SetPixel(0, 0)

    -- 1: Hash
    local _, _, classID = UnitClass("player")
    local specID = GetSpecialization() or 0
    SetPixel(1, (classID * 10) + specID)

    -- 2: Combat
    SetPixel(2, UnitAffectingCombat("player") and 255 or 0)

    -- 3: Player HP
    SetPixel(3, (UnitHealth("player") / UnitHealthMax("player")) * 255)

    -- 4: Target HP
    local thp = 0
    if UnitExists("target") then thp = UnitHealth("target") / UnitHealthMax("target") end
    SetPixel(4, thp * 255)

    -- 5: Target Valid
    SetPixel(5, (UnitExists("target") and UnitCanAttack("player", "target")) and 255 or 0)

    -- 6: Smart Interrupt (Target)
    local name, _, _, startTime, endTime, _, _, notInterruptible = UnitCastingInfo("target")
    if not name then name, _, _, startTime, endTime, _, notInterruptible = UnitChannelInfo("target") end
    local castVal = 0
    if name and not notInterruptible and DANGEROUS[name] then
        local now = GetTime() * 1000
        local duration = endTime - startTime
        local progress = (now - startTime) / duration
        castVal = 1 + (progress * 254)
    end
    SetPixel(6, castVal)

    -- 7: Primary Resource
    local power = UnitPower("player")
    local max = UnitPowerMax("player")
    SetPixel(7, (max > 0) and (power / max * 255) or 0)

    -- 8: Secondary Resource
    SetPixel(8, UnitPower("player", 7) * 25)

    -- 9: Range (Legacy)
    SetPixel(9, (IsSpellInRange("Unending Resolve", "target") == 1) and 255 or 0)

    -- 10: GCD
    local start, duration = GetSpellCooldown(61304) 
    SetPixel(10, (duration == 0) and 255 or 0) 
    
    -- 11 & 12: Focus Logic
    
    local fName, _, _, fStart, fEnd, _, _, fNoInt = UnitCastingInfo("focus")
    if not fName then fName, _, _, fStart, fEnd, _, fNoInt = UnitChannelInfo("focus") end
    local fCastVal = 0
    if fName and not fNoInt and DANGEROUS[fName] then
        local now = GetTime() * 1000
        local duration = fEnd - fStart
        fCastVal = 1 + ((now - fStart) / duration * 254)
    end
    SetPixel(11, fCastVal)

    local fStatus = 0
    if UnitExists("focus") then
        fStatus = fStatus + 1 
        local id = GetInspectSpecialization("focus")
        local healers = {[105]=true, [270]=true, [65]=true, [256]=true, [257]=true, [264]=true, [1468]=true}
        if healers[id] then fStatus = fStatus + 2 end
        if IsSpellInRange("Immolate", "focus") == 1 then fStatus = fStatus + 4 end
        for i=1,40 do
            local _, _, _, _, duration, expirationTime, _, _, _, spellId = UnitDebuff("focus", i)
            if not spellId then break end
            fStatus = fStatus + 8 
            if expirationTime and (expirationTime - GetTime() < 1.5) then fStatus = fStatus + 16 end
        end
    end
    SetPixel(12, fStatus * 5)
    

    -- 13: Immunity State
    
    local immunityState = 0
    if UnitExists("target") then
        local buffs = { [642] = 3, [45438] = 3, [1022] = 1, [186265] = 1, [31224] = 2 }
        for i=1,40 do
            local _, _, _, _, _, _, _, _, _, spellId = UnitBuff("target", i)
            if not spellId then break end
            if buffs[spellId] then immunityState = buffs[spellId] break end
        end
    end
    SetPixel(13, immunityState * 50)
    

    -- 14: Focus Targets Me
    SetPixel(14, (UnitExists("focus") and UnitIsUnit("focustarget", "player")) and 255 or 0)

    -- 15: Totem Active
    
    local totemActive = 0
    -- In real Lua this would scan Nameplates
    SetPixel(15, totemActive * 255)
    
    
    -- 16: Player Debuffs (Roots/Snare/Scatter)
    
    local pState = 0
    for i=1,40 do
        local name, _, _, type, _, _, _, _, _, id = UnitDebuff("player", i)
        if not id then break end
        if id == 213691 then pState = pState + 4 end -- Scatter
    end
    local speed = GetUnitSpeed("player")
    if speed > 0 and speed < 7 then pState = pState + 2 end 
    SetPixel(16, pState * 10)
    

    -- 17: Targeting Me
    SetPixel(17, UnitIsUnit("targettarget", "player") and 255 or 0)

    -- 18: Target Class
    local _, _, targetClassID = UnitClass("target")
    SetPixel(18, (targetClassID or 0) * 10) 
    
    -- 19: Enemy Count
    local enemyCount = 0
    if C_NamePlate then
        for _, plate in pairs(C_NamePlate.GetNamePlates()) do
            local unit = plate.UnitFrame and plate.UnitFrame.unit
            if unit and UnitCanAttack("player", unit) and UnitAffectingCombat(unit) then enemyCount = enemyCount + 1 end
        end
    end
    SetPixel(19, math.min(255, enemyCount * 10))

    -- 20: CC State
    SetPixel(20, 0) 

    -- 21: Range Tier
    
    local rangeVal = 0
    if IsSpellInRange("Shadowburn", "target") == 1 then
        rangeVal = 10 -- Melee Range (<5-8yd)
    elseif IsSpellInRange("Immolate", "target") == 1 then
        rangeVal = 20 -- Mid Range (<30-40yd)
    else
        rangeVal = 30 -- Out of Range
    end
    SetPixel(21, rangeVal * 8)
    
    
    -- 22: Pet Health
    
    local php = 0
    if UnitExists("pet") then 
        php = UnitHealth("pet") / UnitHealthMax("pet") 
    elseif (GetNumGroupMembers() == 0) then
        -- Solo logic: if no pet and not dead/dismissed on purpose
        -- php = 0 (Dead/Missing)
    end
    SetPixel(22, php * 255)
    

    -- 23: Purgeable Count
    local pCount = 0
    if UnitExists("target") then
        for i=1,40 do
            local _, _, _, _, _, _, _, _, _, _, spellId, _, isStealable = UnitBuff("target", i)
            if not spellId then break end
            if isStealable then pCount = pCount + 1 end
        end
    end
    SetPixel(23, math.min(255, pCount * 10))

    -- 24, 25, 26: Arena Interrupts
    
    for i=1,3 do
        local unit = "arena"..i
        local cName, _, _, cStart, cEnd, _, _, cNoInt = UnitCastingInfo(unit)
        if not cName then cName, _, _, cStart, cEnd, _, cNoInt = UnitChannelInfo(unit) end
        local cVal = 0
        if cName and not cNoInt and DANGEROUS[cName] then cVal = 255 end
        SetPixel(23+i, cVal) 
    end
    

    -- 27: Target Spec ID
    local targetSpecID = 0
    if UnitIsPlayer("target") then
        targetSpecID = GetInspectSpecialization("target")
    end
    SetPixel(27, math.min(255, (targetSpecID or 0) / 2))

    -- 28: Player Moving
    SetPixel(28, (GetUnitSpeed("player") > 0) and 255 or 0)

    -- 29: Buff Stacks
    SetPixel(29, 0)

    -- 30: Snapshot / DoT Logic
    
    local snap = 0
    -- Dark Soul, Power Infusion, Tiger's Fury, etc
    local buffs = { [113860]=true, [10060]=true, [5217]=true } 
    for i=1,40 do
        local _, _, _, _, _, _, _, _, _, spellId = UnitBuff("player", i)
        if not spellId then break end
        if buffs[spellId] then snap = 255 break end
    end
    SetPixel(30, snap)
    
    
    -- 31: GTFO
    SetPixel(31, 0)

end)
