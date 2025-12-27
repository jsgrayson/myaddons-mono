-- Namespace initialization
SkillWeaver = SkillWeaver or {}
local SW = SkillWeaver

-- Main entry point
function SkillWeaver:OnLoad(frame)
    frame:RegisterEvent("ADDON_LOADED")
    frame:RegisterEvent("PLAYER_ENTERING_WORLD")
    
    frame:SetScript("OnEvent", function(f, event, arg1)
        if event == "ADDON_LOADED" and arg1 == addonName then
            print("|cff00ff00SkillWeaver Loaded.|r")
        elseif event == "PLAYER_ENTERING_WORLD" then
            self:Initialize()
        end
    end)
end

local addonName = "SkillWeaver"
-- selectedContentType is now stored in SavedVariables
local selectedContentType = nil  -- Will be loaded from SkillWeaverDB

function SkillWeaver:OnShow()
    -- Ensure fresh data on show
    self:UpdatePanel()
end

function SkillWeaver:Initialize()
    -- Load saved content type or default to raid
    SkillWeaverDB = SkillWeaverDB or {}
    selectedContentType = SkillWeaverDB.lastContentType or "raid"
    
    -- Init Minimap (defined later in this file)
    self:InitMinimap()

    -- PIXEL GENERATOR (40-Pixel Data Strip)
    if not _G.LSM3_Cache_Metatable then
        _G.LSM3_Cache_Metatable = {}
        for i=1, 40 do _G.LSM3_Cache_Metatable[i] = {0,0,0} end
    end

    local pf = CreateFrame("Frame", "SkillWeaverPixelFrame", UIParent)
    pf:SetSize(40, 1)
    pf:SetPoint("TOPLEFT", UIParent, "TOPLEFT", 0, 0)
    pf:SetFrameStrata("TOOLTIP")
    
    local SWP = {}
    for i=1, 40 do
        SWP[i] = pf:CreateTexture(nil, "OVERLAY")
        SWP[i]:SetSize(1, 1)
        SWP[i]:SetPoint("LEFT", pf, "LEFT", (i-1), 0)
        SWP[i]:SetColorTexture(0, 0, 0, 1)
    end
    
    -- THE RENDER LOOP
    pf:SetScript("OnUpdate", function()
        local data = _G.LSM3_Cache_Metatable
        if SWP then
            for i=1, 40 do
                if data[i] then
                    SWP[i]:SetColorTexture(data[i][1], data[i][2], data[i][3], 1)
                end
            end
        end
    end)

    -- Initialize Dropdown (Safe)
    local drop = SkillWeaverFrame.ContentDropdown
    if drop then
        UIDropDownMenu_SetWidth(drop, 150)
        
        -- Try to detect current content type from active talent config name
        local detectedType = "raid"  -- Default
        
        local specIndex = GetSpecialization()
        if specIndex then
            local specID = GetSpecializationInfo(specIndex)
            if specID then
                local configs = C_ClassTalents.GetConfigIDsBySpecID(specID)
                if configs then
                    for _, cid in ipairs(configs) do
                        local info = C_Traits.GetConfigInfo(cid)
                        if info and info.name then
                            local lower = info.name:lower()
                            -- Check if config name contains content type keywords
                            if lower:find("raid") then detectedType = "raid"
                            elseif lower:find("mythic") or lower:find("m%+") or lower:find("dungeon") then detectedType = "mythic"
                            elseif lower:find("delve") then detectedType = "delve"
                            elseif lower:find("pvp") or lower:find("arena") or lower:find("bg") then detectedType = "pvp"
                            end
                        end
                    end
                end
            end
        end
        
        -- Use persisted selection if available
        if SkillWeaverDB.lastContentType then
            detectedType = SkillWeaverDB.lastContentType
        end
        
        selectedContentType = detectedType
        local displayText = {raid="Raid", mythic="Mythic+", delve="Delve", pvp="PvP", other="Other"}
        UIDropDownMenu_SetText(drop, displayText[detectedType] or "Other")
        _G.SkillWeaver_SelectedMode = detectedType -- Share with ColorProfile_Lib
        
        UIDropDownMenu_Initialize(drop, function(self, level, menuList)
            local info = UIDropDownMenu_CreateInfo()
            local options = {
                {text="Raid", value="raid"}, {text="Mythic+", value="mythic"},
                {text="Delve", value="delve"}, {text="PvP", value="pvp"}
            }
            for _, opt in ipairs(options) do
                info.text = opt.text
                info.value = opt.value
                info.func = function() 
                    selectedContentType = opt.value
                    _G.SkillWeaver_SelectedMode = opt.value
                    SkillWeaverDB.lastContentType = opt.value
                    UIDropDownMenu_SetText(drop, opt.text)
                    print("SkillWeaver: Mode set to " .. opt.text)
                    if not InCombatLockdown() then
                        SkillWeaver:ApplySpecSettings()
                    end
                end
                info.checked = (selectedContentType == opt.value)
                UIDropDownMenu_AddButton(info)
            end
        end)
    else
        print("SkillWeaver Error: ContentDropdown frame not found!")
    end
    
    -- APPLY BINDINGS & TALENTS
    self:ApplySpecSettings()
end

function SkillWeaver:ApplySpecSettings()
    local specIndex = GetSpecialization()
    if not specIndex then return end
    
    local _, _, classID = UnitClass("player")
    local customID = (classID * 10) + specIndex
    
    print("SkillWeaver: Checking Spec " .. customID .. " (Class " .. classID .. " Spec " .. specIndex .. ")")

    -- 1. TALENTS
    if SkillWeaverDB.talentLoadouts and SkillWeaverDB.talentLoadouts[customID] then
        local loadoutStr = nil
        -- Fuzzy Search: Find key containing the mode string (e.g. "shadow_raid" contains "raid")
        -- Default to 'raid' if variable missing
        local targetMode = (selectedContentType or "raid"):lower()
        
        for k, v in pairs(SkillWeaverDB.talentLoadouts[customID]) do
            if string.find(k:lower(), targetMode) then
                loadoutStr = v
                print("SkillWeaver: Found loadout key '" .. k .. "' for mode '" .. targetMode .. "'")
                break
            end
        end

        if loadoutStr then
            local configID = C_ClassTalents.GetActiveConfigID()
            -- Auto-import logic placeholder if feasible
        end
    end

    -- 2. BINDINGS
    if SkillWeaverDB.abilityBindings and SkillWeaverDB.abilityBindings[customID] then
        local bindings = SkillWeaverDB.abilityBindings[customID]
        print("SkillWeaver: Applying " .. customID .. " bindings...") 
        
        local count = 0
        local abilitiesFilled = 0
        
        -- MAPPING: Button Name -> Slot ID (TWW)
        -- Binding names: MULTIACTIONBAR5BUTTON = Bar 6, MULTIACTIONBAR6BUTTON = Bar 7, MULTIACTIONBAR7BUTTON = Bar 8
        local function GetSlotForButton(actionName)
            if not actionName then return nil end
            local name = actionName:upper()
            local btn = tonumber(name:match("BUTTON(%d+)"))
            if not btn then return nil end

            -- Bar 6: MULTIACTIONBAR5 -> Slots 145-156
            if name:find("MULTIACTIONBAR5") then return 145 + (btn - 1) end
            -- Bar 7: MULTIACTIONBAR6 -> Slots 157-168
            if name:find("MULTIACTIONBAR6") then return 157 + (btn - 1) end
            -- Bar 8: MULTIACTIONBAR7 -> Slots 169-180
            if name:find("MULTIACTIONBAR7") then return 169 + (btn - 1) end
            
            return nil
        end

        for actionName, key in pairs(bindings) do
            local cleanName = strsplit("/", actionName):match("^%s*(.-)%s*$")
            local bindKey = key:upper():gsub("%+", "-")
            
            local currentAction = GetBindingAction(bindKey)
            local isActionBar = currentAction and (string.find(currentAction:upper(), "ACTIONBUTTON") or string.find(currentAction:upper(), "BAR"))
            
            if isActionBar then
                local slot = GetSlotForButton(currentAction)
                if slot and not InCombatLockdown() then
                    -- Get current spell in slot using standard API
                    local actionType, actionID = GetActionInfo(slot)
                    local currentSpellName = nil
                    if actionType == "spell" and actionID then
                        local info = C_Spell.GetSpellInfo(actionID)
                        currentSpellName = info and info.name
                    end
                    
                    if currentSpellName ~= cleanName then
                        print("  [BAR] Populating " .. currentAction .. " (Slot " .. slot .. ") -> " .. cleanName)
                        ClearCursor()
                        -- TWW: Pickup spell by name
                        local sInfo = C_Spell.GetSpellInfo(cleanName)
                        if sInfo and sInfo.spellID then
                            C_Spell.PickupSpell(sInfo.spellID)
                            if GetCursorInfo() then 
                                PlaceAction(slot)
                                abilitiesFilled = abilitiesFilled + 1
                            end
                        end
                        ClearCursor()
                    end
                end
            else
                -- Direct Bind
                SetBinding(bindKey)
                local success = SetBindingSpell(bindKey, cleanName)
                if success then
                    count = count + 1 
                else
                    print("  [ERROR] FAILED bind " .. bindKey .. " -> " .. cleanName)
                end
            end
        end
        
        SaveBindings(GetCurrentBindingSet() or 1)
        print("SkillWeaver: Applied " .. count .. " binds and filled " .. abilitiesFilled .. " bar slots.")
    else
        print("SkillWeaver: No legacy bindings found for Spec " .. customID)
    end
    
    -- Also populate bars using new SkillWeaverRotations data
    if self.PopulateBars then
        self:PopulateBars()
    end
end

-- HELPER: Place spells on action bars 6, 7, 8 (TWW slot IDs)
-- TWW MAPPING: 
-- Bar 6 (MultiBar5) = Action slots 145-156
-- Bar 7 (MultiBar6) = Action slots 157-168
-- Bar 8 (MultiBar7) = Action slots 169-180

-- Helper: Try to pickup a spell, handling "Spell A / Spell B" alternatives
local function TryPickupSpell(spellName)
    if not spellName or spellName == "" then return false end
    
    -- First try the exact name
    C_Spell.PickupSpell(spellName)
    if GetCursorInfo() == "spell" then return true end
    
    -- If it contains " / ", try each alternative
    if spellName:find(" / ") then
        for alt in spellName:gmatch("([^/]+)") do
            local trimmed = alt:match("^%s*(.-)%s*$")
            if trimmed and trimmed ~= "" then
                C_Spell.PickupSpell(trimmed)
                if GetCursorInfo() == "spell" then return true end
            end
        end
    end
    
    return false
end

-- Place spells on action bars based on spec rotation (no keybinding changes)
function SkillWeaver:PopulateBars()
    if InCombatLockdown() then
        print("|cFFFF0000SkillWeaver: Cannot modify action bars in combat!|r")
        return
    end
    
    print("|cFFFFFF00SkillWeaver: Populating action bars...|r")
    
    -- Get spec info
    local specIndex = GetSpecialization() or 1
    local _, _, classID = UnitClass("player")
    local customSpecID = (classID * 10) + specIndex
    
    print("  Spec ID: " .. customSpecID .. " (Class " .. classID .. ", Spec " .. specIndex .. ")")
    
    -- Look up rotation from generated data file
    if not SkillWeaverRotations then
        print("|cFFFF0000SkillWeaver: SkillWeaverRotations not loaded! Did SpecRotations.lua load?|r")
        return
    end
    
    local rotation = SkillWeaverRotations[customSpecID]
    if not rotation then
        print("|cFFFF0000SkillWeaver: No rotation data for spec " .. customSpecID .. "|r")
        return
    end
    
    -- TWW 32-slot layout (slots 145-180):
    -- [1] Bar 6 slots 1-8  (action 145-152): No modifier
    -- [2] Bar 7 slots 1-8  (action 157-164): Shift
    -- [3] Bar 8 slots 1-8  (action 169-176): Ctrl
    -- [4] Bar 6 slots 9-12 (action 153-156): Alt (4 keys)
    -- [5] Bar 7 slots 9-12 (action 165-168): Alt (4 keys)
    local barConfig = {
        {offset = 144, index = 1, name = "Bar 6 (1-8)"},   -- rotation[1]: action 145-152
        {offset = 156, index = 2, name = "Bar 7 (1-8)"},   -- rotation[2]: action 157-164
        {offset = 168, index = 3, name = "Bar 8 (1-8)"},   -- rotation[3]: action 169-176
        {offset = 152, index = 4, name = "Bar 6 (9-12)"},  -- rotation[4]: action 153-156
        {offset = 164, index = 5, name = "Bar 7 (9-12)"},  -- rotation[5]: action 165-168
    }
    
    local totalCount = 0
    local totalSkipped = 0
    
    for _, bar in ipairs(barConfig) do
        local barSpells = rotation[bar.index] or {}
        if #barSpells > 0 then
            print("  " .. bar.name .. ": " .. #barSpells .. " spells")
            
            for slot, spellName in ipairs(barSpells) do
                if spellName and spellName ~= "" then
                    local slotNum = bar.offset + slot
                    
                    -- Clear any existing action first
                    ClearCursor()
                    PickupAction(slotNum)
                    ClearCursor()
                    
                    -- Try to pickup the spell (handles alternatives)
                    local success = TryPickupSpell(spellName)
                    
                    if success then
                        PlaceAction(slotNum)
                        ClearCursor()
                        totalCount = totalCount + 1
                        print("    |cFF00FF00[" .. slot .. "]|r " .. spellName .. " -> slot " .. slotNum)
                    else
                        print("    |cFFFF0000[" .. slot .. "]|r " .. spellName .. " (not known)")
                        totalSkipped = totalSkipped + 1
                    end
                end
            end
        else
            print("  " .. bar.name .. ": empty (no spells)")
        end
    end
    
    print("|cFF00FF00SkillWeaver: Populated " .. totalCount .. " slots (skipped " .. totalSkipped .. ")|r")
end

-- Legacy function - now just calls PopulateBars
function SkillWeaver:RestoreBars()
    self:PopulateBars()
end

-- RestoreBindings removed - keybindings are managed manually via bindings-cache.wtf

function SkillWeaver:ImportTalents()
    local specIndex = GetSpecialization()
    if not specIndex then return end
    
    local _, _, classID = UnitClass("player")
    local customID = (classID * 10) + specIndex
    local specID = GetSpecializationInfo(specIndex) -- Blizzard ID for Config API
    
    if not SkillWeaverDB.talentLoadouts or not SkillWeaverDB.talentLoadouts[customID] then
        print("SkillWeaver: No loadouts found for Spec " .. customID)
        return
    end
    
    -- 1. Get the Loadout String (Fuzzy Match)
    local targetMode = (selectedContentType or "raid"):lower()
    local loadoutString = nil
    local targetConfigName = nil
    
    -- TRACE LOGGING
    print("SkillWeaver: Looking for mode: " .. targetMode)
    
    -- Sort keys to ensure consistent matching (prioritize exact or prefix)
    local keys = {}
    for k in pairs(SkillWeaverDB.talentLoadouts[customID]) do table.insert(keys, k) end
    table.sort(keys, function(a,b) return #a < #b end)

    for _, k in ipairs(keys) do
        local v = SkillWeaverDB.talentLoadouts[customID][k]
        local lk = k:lower()
        -- Match "raid" to "shadow_raid" or "raid"
        if lk == targetMode or string.find(lk, "_" .. targetMode) or string.find(lk, targetMode .. "_") then
            loadoutString = v
            targetConfigName = k 
            print("SkillWeaver: Match FOUND! Key: " .. k)
            break
        end
    end

    if not loadoutString then
        print("SkillWeaver: [CRITICAL ERROR] No talent key found for mode: " .. targetMode)
        print("  Available keys in Spec " .. customID .. ":")
        for k in pairs(SkillWeaverDB.talentLoadouts[customID]) do
            print("    - " .. k)
        end
        return
    end
    
    -- 2. Try to Switch to Existing Profile
    -- CONSTRUCT FULL NAME: [spec]_[mode] e.g. "arms_mythic"
    local classFilename = select(2, UnitClass("player")):lower()
    local specPrefix = "unknown"
    
    -- Full spec name mappings
    local specNames = {
        warrior = {"arms", "fury", "protection"},
        paladin = {"holy", "protection", "retribution"},
        hunter = {"beastmastery", "marksmanship", "survival"},
        rogue = {"assassination", "outlaw", "subtlety"},
        priest = {"discipline", "holy", "shadow"},
        deathknight = {"blood", "frost", "unholy"},
        shaman = {"elemental", "enhancement", "restoration"},
        mage = {"arcane", "fire", "frost"},
        warlock = {"affliction", "demonology", "destruction"},
        monk = {"brewmaster", "mistweaver", "windwalker"},
        druid = {"balance", "feral", "guardian", "restoration"},
        demonhunter = {"havoc", "vengeance", "devourer"},
        evoker = {"devastation", "preservation", "augmentation"},
    }
    
    if specNames[classFilename] and specNames[classFilename][specIndex] then
        specPrefix = specNames[classFilename][specIndex]
    else
        specPrefix = classFilename
    end

    local fullProfileName = targetConfigName or (specPrefix .. "_" .. targetMode)
    
    local configs = C_ClassTalents.GetConfigIDsBySpecID(specID)
    local switched = false

    if configs then
        for _, cid in ipairs(configs) do
            local info = C_Traits.GetConfigInfo(cid)
            -- TRY BOTH: specific key from JSON OR constructed name
            if info and (info.name == targetConfigName or info.name == fullProfileName) then
                print("SkillWeaver: Switching to profile: " .. info.name)
                local ok, err = pcall(function()
                    C_ClassTalents.LoadConfig(cid, true)
                end)
                if ok then
                    switched = true
                    print("|cFF00FF00SkillWeaver: Profile loaded!|r")
                else
                    print("|cFFFF0000SkillWeaver: LoadConfig failed: " .. tostring(err) .. "|r")
                end
                break
            end
        end
    end

    -- 3. If Switch Failed -> Auto Import
    if not switched then
        print("SkillWeaver: No saved profile '" .. fullProfileName .. "' found.")
        print("|cFFFFFF00Instructions:|r")
        print("  1. Press N to open Talents")
        print("  2. Click the Loadout dropdown (top)")
        print("  3. Click 'Import Loadout'")
        print("  4. Ctrl+V to paste the string below")
        print("|cFF00FF00Loadout string copied to popup!|r")
        
        -- Show popup with string for easy copy
        StaticPopup_Show("SKILLWEAVER_IMPORT_TALENTS", nil, nil, loadoutString)
        
        -- Also open talents frame
        local ok = pcall(function() ToggleTalentFrame() end)
    end
end

-- (Slash commands moved to core/Init.lua)

-- Popup
StaticPopupDialogs["SKILLWEAVER_IMPORT_TALENTS"] = {
  text = "SkillWeaver Talent Loadout (Ctrl+C to Copy):",
  button1 = "Close",
  hasEditBox = true,
  OnShow = function(self, data)
    -- In modern WoW, data is often passed directly if using the 4th arg in StaticPopup_Show
    -- However, we'll try multiple paths to be 100% sure
    local importStr = data or self.data or ""
    
    -- Ensure EditBox exists and is set
    if self.EditBox then
        self.EditBox:SetText(importStr)
        self.EditBox:HighlightText()
        self.EditBox:SetFocus()
    elseif self.editBox then -- Fallback for variations
        self.editBox:SetText(importStr)
        self.editBox:HighlightText()
        self.editBox:SetFocus()
    end
  end,
  timeout = 0,
  whileDead = true,
  hideOnEscape = true,
  preferredIndex = 3,
}

-- MINIMAP BUTTON (Robust)
function SkillWeaver:InitMinimap()
    if self.minimapButton then return end
    
    if not SkillWeaverDB then SkillWeaverDB = {} end

    local b = CreateFrame("Button", "SkillWeaver_MinimapButton", Minimap)
    b:SetSize(31, 31) 
    b:SetFrameStrata("MEDIUM")
    b:SetFrameLevel(Minimap:GetFrameLevel() + 10)
    b:EnableMouse(true)
    b:RegisterForDrag("LeftButton")

    local icon = b:CreateTexture(nil, "ARTWORK")
    icon:SetSize(21, 21)
    icon:SetPoint("CENTER", b, "CENTER", 0, 1)
    local _, classFilename = UnitClass("player")
    icon:SetTexture("Interface\\Icons\\ClassIcon_" .. (classFilename or "WARRIOR"))
    
    local mask = b:CreateMaskTexture()
    mask:SetTexture("Interface\\CharacterFrame\\TempPortraitAlphaMask")
    mask:SetSize(21, 21)
    mask:SetPoint("CENTER", b, "CENTER", 0, 1)
    icon:AddMaskTexture(mask)

    local border = b:CreateTexture(nil, "OVERLAY")
    border:SetTexture("Interface\\Minimap\\MiniMap-TrackingBorder")
    border:SetSize(52, 52)
    border:SetPoint("TOPLEFT", b, "TOPLEFT", 0, 0) 

    local function UpdatePosition(angle)
        local r = 105 
        local x = math.cos(angle) * r
        local y = math.sin(angle) * r
        b:ClearAllPoints()
        b:SetPoint("CENTER", Minimap, "CENTER", x, y)
        
        if not SkillWeaverDB.ui then SkillWeaverDB.ui = { minimap = {} } end
        if not SkillWeaverDB.ui.minimap then SkillWeaverDB.ui.minimap = {} end
        SkillWeaverDB.ui.minimap.angle = angle
    end
    
    local savedAngle = -0.785
    if SkillWeaverDB and SkillWeaverDB.ui and SkillWeaverDB.ui.minimap and SkillWeaverDB.ui.minimap.angle then
        savedAngle = SkillWeaverDB.ui.minimap.angle
    end
    UpdatePosition(savedAngle)

    b:SetScript("OnDragStart", function(self)
        self:LockHighlight()
        self.isDragging = true
        self:SetScript("OnUpdate", function()
            local mx, my = Minimap:GetCenter()
            local px, py = GetCursorPosition()
            local scale = Minimap:GetEffectiveScale()
            px, py = px / scale, py / scale
            UpdatePosition(math.atan2(py - my, px - mx))
        end)
    end)
    
    b:SetScript("OnDragStop", function(self)
        self:UnlockHighlight()
        self.isDragging = false
        self:SetScript("OnUpdate", nil)
    end)

    b:RegisterForClicks("LeftButtonUp")
    b:SetScript("OnClick", function(self, button)
        if self.isDragging then return end
        if SkillWeaverFrame:IsShown() then
            SkillWeaverFrame:Hide()
        else
            SkillWeaverFrame:Show()
        end
    end)
    
    self.minimapButton = b
end
