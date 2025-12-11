local ADDON_NAME, SkillWeaver = ...

-- Visual Cue Module
-- Purpose: Display a high-contrast icon for the Python CV Agent to detect.

local VisualCue = {}
SkillWeaver.VisualCue = VisualCue

local frame = CreateFrame("Frame", "SkillWeaverVisualCue", UIParent)
frame:SetSize(64, 64)
frame:SetPoint("CENTER", 0, -200) -- Default position, user can move
frame:SetMovable(true)
frame:EnableMouse(true)
frame:RegisterForDrag("LeftButton")
frame:SetScript("OnDragStart", frame.StartMoving)
frame:SetScript("OnDragStop", frame.StopMovingOrSizing)

-- Icon Texture
local texture = frame:CreateTexture(nil, "BACKGROUND")
texture:SetAllPoints()
texture:SetTexture("Interface\\Icons\\INV_Misc_QuestionMark")
frame.texture = texture

-- Data Pixel (1x1) for Python Communication
-- Encoding: Red = 0, Green = 0, Blue = SlotID / 255
local dataPixel = frame:CreateTexture(nil, "OVERLAY")
dataPixel:SetSize(16, 16)
dataPixel:SetPoint("TOPLEFT", frame, "TOPLEFT", 0, 0)
dataPixel:SetColorTexture(0, 0, 0, 1) -- Default Black (No Action)

-- Action Bar Cache: SpellName -> {slot=1..12, mod="NONE"|"SHIFT"|"CTRL"|"ALT"}
local spellSlots = {}

function VisualCue:ScanActionBars()
    table.wipe(spellSlots)
    
    -- Helper to scan a range and assign a modifier
    local function ScanRange(startSlot, endSlot, mod)
        for slot = startSlot, endSlot do
            local type, id = GetActionInfo(slot)
            local keySlot = (slot - startSlot) + 1 -- Normalize to 1-12
            
            if type == "spell" then
                local name = GetSpellInfo(id)
                if name then
                    spellSlots[name] = {slot = keySlot, mod = mod}
                end
            elseif type == "macro" then
                local name = GetMacroSpell(id)
                if name then
                    spellSlots[name] = {slot = keySlot, mod = mod}
                end
            end
        end
    end

    -- Bar 1: 1-12 (No Mod)
    ScanRange(1, 12, "NONE")
    -- Bar 2 (BottomLeft): 61-72 (Shift) - Standard ElvUI/Blizz mapping
    ScanRange(61, 72, "SHIFT")
    -- Bar 3 (BottomRight): 49-60 (Ctrl)
    ScanRange(49, 60, "CTRL")
    -- Bar 4 (Right): 25-36 (Alt)
    ScanRange(25, 36, "ALT")
end

-- ... Event Listener (unchanged) ...

function VisualCue:Update(iconST, spellST, iconAoE, spellAoE)
    -- ST CUE (Left)
    if not iconST then
        frame:Hide()
        dataPixel:SetColorTexture(0, 0, 0, 1)
    else
        frame:Show()
        texture:SetTexture(iconST)
        self:RenderPixel(dataPixel, texture, spellST)
    end

    -- AOE CUE (Right)
    if not frame.textureAoE then
        -- Create AoE Texture/Pixel if missing
        frame.textureAoE = frame:CreateTexture(nil, "BACKGROUND")
        frame.textureAoE:SetSize(64, 64)
        frame.textureAoE:SetPoint("LEFT", texture, "RIGHT", 10, 0)
        
        frame.dataPixelAoE = frame:CreateTexture(nil, "OVERLAY")
        frame.dataPixelAoE:SetSize(16, 16)
        frame.dataPixelAoE:SetPoint("TOPLEFT", frame.textureAoE, "TOPLEFT", 0, 0)
    end

    if iconAoE then
        frame.textureAoE:Show()
        frame.textureAoE:SetTexture(iconAoE)
        frame.dataPixelAoE:Show()
        self:RenderPixel(frame.dataPixelAoE, frame.textureAoE, spellAoE)
    else
        frame.textureAoE:Hide()
        frame.dataPixelAoE:Hide()
    end
    
    -- Data Pixel 2: Health & Resource Telemetry (Offset from ST Pixel)
    -- R = Player Health %
    -- G = Target Health %
    -- B = Resource % (Mana/Rage/Energy)
    local playerHealth = UnitHealth("player") / UnitHealthMax("player")
    local targetHealth = 0
    if UnitExists("target") then
        local maxHp = UnitHealthMax("target")
        if maxHp > 0 then
            targetHealth = UnitHealth("target") / maxHp
        end
    end
    
    -- Resource Normalization (0-1)
    local maxPower = UnitPowerMax("player")
    local resource = 0
    if maxPower > 0 then
        resource = UnitPower("player") / maxPower
    end
    
    -- Set Data Pixel 2 (Offset by 16px from ST pixel)
    if not frame.dataPixel2 then
        frame.dataPixel2 = frame:CreateTexture(nil, "OVERLAY")
        frame.dataPixel2:SetSize(16, 16)
        frame.dataPixel2:SetPoint("LEFT", dataPixel, "RIGHT", 0, 0)
    end
    frame.dataPixel2:SetColorTexture(playerHealth, targetHealth, resource, 1)
end

function VisualCue:RenderPixel(pixel, tex, spellName)
    -- Priority 1: Smart Interrupt (Red Light)
    local shouldKick = false
    if UnitExists("target") and UnitCanAttack("player", "target") then
        local name, _, _, startTime, endTime, _, _, notInterruptible = UnitCastingInfo("target")
        if not name then
            name, _, _, startTime, endTime, _, _, notInterruptible = UnitChannelInfo("target")
        end

        if name and not notInterruptible then
            local currentTime = GetTime() * 1000
            local remaining = endTime - currentTime
            local totalDuration = endTime - startTime
            
            local _, _, _, latencyWorld = GetNetStats()
            local lagSafety = latencyWorld or 50
            local threshold = 400 + 300 + lagSafety
            
            if (remaining < threshold) or (totalDuration < 1500) then
                shouldKick = true
            end
        end
    end

    if shouldKick then
        -- RED LIGHT: Interrupt Immediately!
        pixel:SetColorTexture(1, 0, 0, 1)
        tex:SetVertexColor(1, 0.5, 0.5)
        return
    end

    -- Priority 2: Auto-Trinkets (Magenta Light)
    if SkillWeaver.AutoTrinkets and SkillWeaver.AutoTrinkets:ShouldUse() then
        -- MAGENTA LIGHT: Use Trinkets!
        pixel:SetColorTexture(1, 0, 1, 1)
        tex:SetVertexColor(1, 0.5, 1)
        return
    end

    -- Priority 3: Rotation
    if spellName == "/cycle" or spellName == "/targetenemy" then
        -- CYCLE SIGNAL: Cyan Light (0, 1, 1)
        pixel:SetColorTexture(0, 1, 1, 1)
        tex:SetVertexColor(0.5, 1, 1)
        
    elseif spellName and spellSlots[spellName] then
        local info = spellSlots[spellName]
        local slot = info.slot
        local mod = info.mod
        
        -- Encode Key (Blue)
        local blueVal = (slot * 20) / 255
        
        -- Encode Mod (Green)
        local greenVal = 0
        if mod == "SHIFT" then greenVal = 0.25      -- ~64
        elseif mod == "CTRL" then greenVal = 0.5    -- ~128
        elseif mod == "ALT" then greenVal = 0.75    -- ~192
        end
        
        pixel:SetColorTexture(0, greenVal, blueVal, 1)
        tex:SetVertexColor(0.8, 0.8, 1) 
    else
        -- Unknown spell
        pixel:SetColorTexture(0, 0, 0, 1)
        tex:SetVertexColor(1, 1, 1)
    end
end

function VisualCue:Toggle(enable)
    if enable then
        frame:Show()
        print("SkillWeaver: Visual Cue Enabled")
    else
        frame:Hide()
        print("SkillWeaver: Visual Cue Disabled")
    end
end

-- Hook into the main engine update to get the current icon
-- This assumes SkillWeaver.Engine.CurrentStep contains the info
-- We'll need to ensure the main engine calls VisualCue:Update()
