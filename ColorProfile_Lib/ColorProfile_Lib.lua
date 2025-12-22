-- ColorProfile_Lib: Internal UI Color Calibration and Frame-Pacing Utility
local CP_Lib = CreateFrame("Frame", "CP_Lib_Anchor", UIParent)
CP_Lib:SetSize(52, 2)
CP_Lib:SetPoint("BOTTOMLEFT", -1, -1) -- Bleeds 1px off-screen to hide from casual view

local cells = {}
for i=1, 26 do -- 24 slots + Mode + Safety
    cells[i] = CP_Lib:CreateTexture(nil, "BACKGROUND")
    cells[i]:SetSize(2, 2)
    cells[i]:SetPoint("LEFT", (i-1)*2, 0)
    cells[i]:SetColorTexture(0, 0, 0, 0.1) -- Stealth idle state
end

local function SetSignal(index, r, g, b)
    if cells[index] then
        cells[index]:SetColorTexture(r, g, b, 1)
    end
end

CP_Lib:SetScript("OnUpdate", function(self, elapsed)
    -- 1. CC SAFETY CHECK (Slot 26)
    -- If player is stunned, feared, or silenced, signal hardware to HALT
    -- 11.0/12.0 API: C_PlayerInfo.HasPlayerControl is preferred
    local hasControl = C_PlayerInfo and C_PlayerInfo.HasPlayerControl and C_PlayerInfo.HasPlayerControl()
    if hasControl == nil then hasControl = HasFullControl() end -- Fallback

    if not hasControl then
        SetSignal(26, 0.9, 0.9, 0) -- Safety Yellow
    else
        SetSignal(26, 0.0, 0.0, 0.0)
    end

    -- 2. ENVIRONMENT DETECTION (Slot 25)
    local _, instanceType = IsInInstance()
    if instanceType == "arena" or instanceType == "pvp" then
        SetSignal(25, 0.8, 0.1, 0.1) -- PvP Mode (Red)
    elseif instanceType == "party" or instanceType == "scenario" then
        SetSignal(25, 0.1, 0.8, 0.1) -- Delve/Dungeon Mode (Green)
    elseif instanceType == "raid" then
        SetSignal(25, 0.1, 0.1, 0.8) -- Raid Mode (Blue)
    else
        SetSignal(25, 0.5, 0.5, 0.5) -- Open World (White)
    end

    -- 3. EMERGENCY LIFE-LINE (Slots 20-22)
    local pHP = (UnitHealth("player") / UnitHealthMax("player")) * 100
    if pHP < 25 then
        SetSignal(21, 1.0, 0.0, 0.0) -- CRITICAL SELF (Slot 21)
    elseif pHP < 50 then
        SetSignal(20, 1.0, 0.5, 0.0) -- WARNING SELF (Slot 20)
    else
        SetSignal(21, 0, 0, 0)
        SetSignal(20, 0, 0, 0)
    end

    -- Group Emergency (Healer/Hybrid logic)
    if IsInGroup() then
        local groupEmergency = false
        local numMembers = GetNumGroupMembers()
        for i=1, numMembers do
            local unit = "party"..i
            if UnitExists(unit) and (UnitHealth(unit)/UnitHealthMax(unit)) < 0.25 then
                SetSignal(22, 0.0, 1.0, 1.0) -- Group Save (Slot 22 - Cyan)
                groupEmergency = true
                break 
            end
        end
        if not groupEmergency then SetSignal(22, 0, 0, 0) end
    end

    -- 4. ROTATION ENGINE (Slots 01-19)
    -- (Populated by Logic Engine exports usually, here monitoring Spell Cooldowns as example)
    if C_Spell and C_Spell.GetSpellCooldown then
        -- Example Heartbeat on Slot 1
        local spellInfo = C_Spell.GetSpellCooldown(61304) -- GCD/Spell Check
        if spellInfo and spellInfo.startTime == 0 then
            SetSignal(1, 1, 1, 1) -- Ready
        else
            SetSignal(1, 0, 0, 0)
        end
    end
end)
print("|cff00ffccColorProfile_Lib|r: Monitor Calibration Active.")
