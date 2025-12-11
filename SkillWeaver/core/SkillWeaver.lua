local HealerLoader = require("skillweaver.core.HealerLoader")
require("skillweaver.core.ContentDetector")
require("skillweaver.core.AutoTrinkets")

local SkillWeaver = {}

SkillWeaver.currentSpec = nil
SkillWeaver.role = nil
SkillWeaver.Sequences = {}

---------------------------------------------------------
-- Secure Buttons (ST & AoE)
---------------------------------------------------------
-- These buttons are clicked by the user's macro.
-- They use SecureHandler to cycle through steps.

local btnST = CreateFrame("Button", "SkillWeaverButton_ST", UIParent, "SecureActionButtonTemplate, SecureHandlerStateTemplate")
btnST:SetAttribute("type", "macro")
btnST:RegisterForClicks("AnyDown", "AnyUp")

local btnAoE = CreateFrame("Button", "SkillWeaverButton_AoE", UIParent, "SecureActionButtonTemplate, SecureHandlerStateTemplate")
btnAoE:SetAttribute("type", "macro")
btnAoE:RegisterForClicks("AnyDown", "AnyUp")

-- Secure Snippet: Cycles 'stepX' attributes into 'macrotext'
-- This runs in the restricted environment.
local secureSnippet = [[
    local step = self:GetAttribute("step_index") or 1
    local total = self:GetAttribute("step_total") or 1
    
    -- Get command for current step
    local cmd = self:GetAttribute("step" .. step)
    
    -- Set macrotext for execution
    self:SetAttribute("macrotext", cmd)
    
    -- Advance index
    step = step + 1
    if step > total then step = 1 end
    self:SetAttribute("step_index", step)
]]

-- Attach snippet to OnClick
btnST:SetAttribute("_onclick", secureSnippet)
btnAoE:SetAttribute("_onclick", secureSnippet)

---------------------------------------------------------
-- Update Secure Button with Sequence Data
---------------------------------------------------------
function SkillWeaver:UpdateSecureButton(sequence)
    if not sequence then return end
    
    -- Store for Overlay
    self.ActiveSequence = sequence

    -- 1. Generate the macro body for the SecureHandler
    -- We want a snippet that iterates our steps.
    -- But SecureHandlers are tricky.
    -- Simplified approach for "One Button":
    -- We will use a snippet that runs on PreClick.
    if InCombatLockdown() then
        print("|cffFF0000SkillWeaver: Cannot update buttons in combat!|r")
        return
    end

    -- 1. Process Single Target (ST)
    -- If sequence has explicit 'st' table, use it. Otherwise use main 'steps'.
    local stSteps = sequence.st or sequence.steps
    if stSteps then
        btnST:SetAttribute("step_total", #stSteps)
        btnST:SetAttribute("step_index", 1)
        for i, step in ipairs(stSteps) do
            btnST:SetAttribute("step" .. i, step.command)
        end
    else
        btnST:SetAttribute("step_total", 1)
        btnST:SetAttribute("step1", "/cast [help] Flash Heal; Smite") -- Fallback
    end

    -- 2. Process AoE
    -- If sequence has explicit 'aoe' table, use it. Otherwise default to ST.
    local aoeSteps = sequence.aoe
    if aoeSteps then
        btnAoE:SetAttribute("step_total", #aoeSteps)
        btnAoE:SetAttribute("step_index", 1)
        for i, step in ipairs(aoeSteps) do
            btnAoE:SetAttribute("step" .. i, step.command)
        end
    else
        -- Fallback: Clone ST if no AoE specified
        btnAoE:SetAttribute("step_total", #stSteps)
        btnAoE:SetAttribute("step_index", 1)
        for i, step in ipairs(stSteps) do
            btnAoE:SetAttribute("step" .. i, step.command)
        end
    end

    print("|cff00ff00SkillWeaver: Secure Buttons Updated.|r")
end

---------------------------------------------------------
-- Called when player changes spec
---------------------------------------------------------
function SkillWeaver:OnSpecChanged(specID)
    self.currentSpec = specID

    if self:IsHealerSpec(specID) then
        self.role = "HEALER"
        HealerLoader:Activate(specID)
    else
        self.role = "DPS" -- future
    end
end

---------------------------------------------------------
-- Identify healer specs
---------------------------------------------------------
function SkillWeaver:IsHealerSpec(specID)
    return (
        specID == "PALADIN_65" or
        specID == "PRIEST_256" or
        specID == "PRIEST_257" or
        specID == "DRUID_105" or
        specID == "SHAMAN_264" or
        specID == "MONK_270" or
        specID == "EVOKER_1468"
    )
end

---------------------------------------------------------
-- Content-Aware Loadout Switching
---------------------------------------------------------
function SkillWeaver:OnContentChanged(newType)
    self:CheckLoadout(newType)
end

function SkillWeaver:CheckLoadout(contentType)
    if not SkillWeaverDB or not SkillWeaverDB.Loadouts then return end
    
    local specID = self.currentSpec or GetSpecializationInfo(GetSpecialization())
    if not specID then return end
    
    local loadouts = SkillWeaverDB.Loadouts[specID]
    if not loadouts then return end
    
    -- Map internal types to DB keys
    local dbKey = nil
    if contentType == "RAID" then dbKey = "Raid"
    elseif contentType == "MYTHIC_PLUS" then dbKey = "MythicPlus"
    elseif contentType == "PVP" or contentType == "ARENA" then dbKey = "PvP"
    end
    
    if dbKey and loadouts[dbKey] then
        local importString = loadouts[dbKey]
        print("|cff00ff00SkillWeaver: Detected " .. contentType .. ".|r")
        print("|cffFFFF00Suggested Loadout Found!|r Type |cff00ffff/sw load " .. dbKey .. "|r to apply.")
        
        -- Store for slash command
        self.pendingLoadout = importString
    end
end

SLASH_SKILLWEAVER1 = "/sw"
SlashCmdList["SKILLWEAVER"] = function(msg)
    local cmd, arg = msg:match("^(%S*)%s*(.-)$")
    
    if cmd == "load" and arg then
        -- Handle "/sw load Raid"
        local specID = GetSpecializationInfo(GetSpecialization())
        if SkillWeaverDB and SkillWeaverDB.Loadouts and SkillWeaverDB.Loadouts[specID] then
            local str = SkillWeaverDB.Loadouts[specID][arg]
            if str then
                C_ClassTalents.ImportLoadout(str, arg .. " (SW)")
                print("SkillWeaver: Importing loadout for " .. arg)
            else
                print("SkillWeaver: No loadout found for " .. arg)
            end
        end
    elseif cmd == "equip" then
        if arg == "Raid" or arg == "M+" or arg == "PvP" or arg == "Delve" or arg == "Fishing" or arg == "Speed" then
            SkillWeaver.EquipmentManager:EquipBestSet(arg)
        else
            print("Usage: /sw equip [Raid|M+|PvP|Delve|Fishing|Speed]")
        end
    elseif cmd == "battleres" then
        if arg == "on" then
            SkillWeaver.BattleRes:Toggle(true)
        elseif arg == "off" then
            SkillWeaver.BattleRes:Toggle(false)
        else
            SkillWeaver.BattleRes:Toggle() -- Toggle current state
        end
    elseif cmd == "stockcheck" or cmd == "stock" then
        if SkillWeaver.StockManager then
            SkillWeaver.StockManager:PerformCheck()
        end
    else
        print("SkillWeaver Commands:")
        print("  /sw load [Raid|MythicPlus|PvP] - Import talent loadout")
        print("  /sw equip [Raid|M+|PvP|Delve|Fishing|Speed] - Equip best gear for content")
        print("  /sw battleres [on|off] - Toggle auto battle res")
        print("  /sw stockcheck - Manual consumable stock check")
    end
end


---------------------------------------------------------
-- Visual Loop (AI Camera Support)
---------------------------------------------------------
local visualTimer = 0
local VISUAL_INTERVAL = 0.1

local visualFrame = CreateFrame("Frame")
visualFrame:SetScript("OnUpdate", function(self, elapsed)
    visualTimer = visualTimer + elapsed
    if visualTimer < VISUAL_INTERVAL then return end
    visualTimer = 0
    
    if not SkillWeaver.ActiveSequence then return end
    
    -- 1. Evaluate Single Target (ST)
    local cmdST = SkillWeaver.Engine.Sequence:EvaluateNext(SkillWeaver.ActiveSequence)
    local iconST, spellST = nil, nil
    
    if cmdST then
        if cmdST:match("^/cycle") or cmdST:match("^/targetenemy") then
            iconST = "Interface\\Icons\\INV_Misc_QuestionMark"
            spellST = "/cycle"
        else
            local spell = cmdST:match("/cast%s+(.+)")
            if spell then
                spell = spell:gsub("%[.-%]", ""):match("^%s*(.-)%s*$")
                local name, _, icon = GetSpellInfo(spell)
                iconST = icon
                spellST = name or spell
            end
        end
    end

    -- 2. Evaluate AoE (if available)
    local cmdAoE = nil
    local iconAoE, spellAoE = nil, nil
    
    if SkillWeaver.ActiveSequence.aoe and #SkillWeaver.ActiveSequence.aoe > 0 then
        -- Temporarily swap 'steps' or 'st' with 'aoe' for evaluation
        -- Actually, EvaluateNext checks 'st' or 'steps'. We need to trick it or pass a dummy sequence.
        -- Let's create a dummy sequence object for AoE evaluation
        local aoeSeq = {
            type = SkillWeaver.ActiveSequence.type,
            st = SkillWeaver.ActiveSequence.aoe, -- Put AoE steps in 'st' slot for EvaluateNext
            steps = SkillWeaver.ActiveSequence.aoe
        }
        cmdAoE = SkillWeaver.Engine.Sequence:EvaluateNext(aoeSeq)
        
        if cmdAoE then
            local spell = cmdAoE:match("/cast%s+(.+)")
            if spell then
                spell = spell:gsub("%[.-%]", ""):match("^%s*(.-)%s*$")
                local name, _, icon = GetSpellInfo(spell)
                iconAoE = icon
                spellAoE = name or spell
            end
        end
    end

    -- Update Visual Cue with BOTH
    SkillWeaver.VisualCue:Update(iconST, spellST, iconAoE, spellAoE)
end)

-- Event Frame for Data Export
local exportFrame = CreateFrame("Frame")
exportFrame:RegisterEvent("PLAYER_LOGOUT")
exportFrame:SetScript("OnEvent", function(self, event)
    if event == "PLAYER_LOGOUT" then
        SkillWeaverDB = SkillWeaverDB or {}
        SkillWeaverDB.Bags = {}
        
        -- Scan Bags
        for bag = 0, 4 do
            local numSlots = C_Container.GetContainerNumSlots(bag)
            for slot = 1, numSlots do
                local info = C_Container.GetContainerItemInfo(bag, slot)
                if info then
                    local link = info.hyperlink
                    local _, _, quality, iLvl, _, _, _, _, _, _, sellPrice, classID, subClassID = GetItemInfo(link)
                    local name = GetItemInfo(link) 
                    
                    table.insert(SkillWeaverDB.Bags, {
                        name = name or "Unknown",
                        link = link,
                        id = info.itemID,
                        quality = quality,
                        ilvl = iLvl,
                        sellPrice = sellPrice,
                        slot = slot,
                        bag = bag,
                        classID = classID,
                        subClassID = subClassID
                    })
                end
            end
        end
        
        -- Scan Equipped
        SkillWeaverDB.Equipped = {}
        for slotID = 1, 19 do -- Scan all slots
            local link = GetInventoryItemLink("player", slotID)
            if link then
                local _, _, quality, iLvl = GetItemInfo(link)
                local name = GetItemInfo(link)
                local id = GetItemInfoInstant(link)
                
                table.insert(SkillWeaverDB.Equipped, {
                    name = name or "Unknown",
                    link = link,
                    id = id,
                    quality = quality,
                    ilvl = iLvl,
                    slotID = slotID
                })
            end
        end
        
        print("SkillWeaver: Bag and Equipment data saved.")
    end
end)

return SkillWeaver
