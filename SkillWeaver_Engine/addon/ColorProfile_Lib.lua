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

-- DOT MAPPING (Simple Boolean)
local DOTS = {
    [34914]=11, [402668]=11, -- VT
    [589]=12, [10894]=12, -- SWP
    [2944]=13, [402662]=13 -- DP
}

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
        
        -- 3. DOTS (BOOLEAN - TWW Compatible via AuraUtil)
        local dVals = {[11]=0, [12]=0, [13]=0}
        if UnitExists("target") then
            -- Use AuraUtil.ForEachAura if available (TWW), else legacy UnitAura
            if AuraUtil and AuraUtil.ForEachAura then
                local function CheckAura(aura)
                    if aura.isFromPlayerOrPlayerPet then
                        local idx = DOTS[aura.spellId]
                        if not idx then
                            if aura.name == "Vampiric Touch" then idx = 11
                            elseif aura.name == "Shadow Word: Pain" then idx = 12
                            elseif aura.name == "Devouring Plague" then idx = 13 end
                        end
                        if idx then dVals[idx] = 255 end
                    end
                end
                AuraUtil.ForEachAura("target", "HARMFUL", nil, CheckAura, true)
            else
                -- Legacy API (Classic/Era)
                for i = 1, 40 do
                    local name, _, _, _, _, _, source, _, _, spellId = UnitAura("target", i, "HARMFUL|PLAYER")
                    if not name then break end
                    if source == "player" or source == "pet" then
                        local idx = DOTS[spellId]
                        if not idx then
                            if name == "Vampiric Touch" then idx = 11
                            elseif name == "Shadow Word: Pain" then idx = 12
                            elseif name == "Devouring Plague" then idx = 13 end
                        end
                        if idx then dVals[idx] = 255 end
                    end
                end
            end
        end
        SetPixel(11, dVals[11])
        SetPixel(12, dVals[12])
        SetPixel(13, dVals[13])

        -- 4. RESOURCES
        local pMax = UnitPowerMax("player")
        SetPixel(7, (pMax > 0 and UnitPower("player") / pMax or 0) * 255)
        
        if classID == 5 then 
            local pSec = UnitPower("player", 13) 
            if pSec then SetPixel(8, pSec * 2.55) end
        end

        -- 5. SENSORS
        SetPixel(17, IsKeyDown("2") and 255 or 0)
        local _, _, _, _, _, _, _, kick = UnitCastingInfo("target")
        SetPixel(18, (kick == false) and 255 or 0)
        SetPixel(19, IsStealthed() and 255 or 0)
        SetPixel(6, 40 * 4.25) -- Simplified Range (Always 40y to prevent range blocks)
    end)
    
    SetPixel(31, 255)
end)

print("|cff00ffccColorProfile|r: Restore Complete.")
