local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):NewAddon("SkillWeaver", "AceConsole-3.0", "AceEvent-3.0")
local AceGUI = LibStub("AceGUI-3.0")

-- Data Defaults
local defaults = {
    profile = {
        profiles = {},  -- [id] = { name, specId, class, active=false }
        sequences = {}, -- [id] = { name, profileId, steps=[], notes }
        toggles = {},   -- [name] = { enabled=true/false }
        meta = { last_profileId = nil, last_seqId = nil }
    }
}

function SkillWeaver:OnInitialize()
    self.db = LibStub("AceDB-3.0"):New("SkillWeaverDB", defaults, true)
    
    self:RegisterChatCommand("sw", "HandleCommand")
    self:RegisterChatCommand("skillweaver", "HandleCommand")
    
    self:Print("SkillWeaver Loaded. Type /sw to open.")
end

function SkillWeaver:OnEnable()
    -- Future: Hook rotation tick for actual execution
end

function SkillWeaver:HandleCommand(input)
    local cmd = input:lower() :match("^(%S+)")
    
    if cmd == "dump" then
        local profileCount = 0
        local activeProfileName = "None"
        for _, prof in pairs(self.db.profile.profiles) do
            profileCount = profileCount + 1
            if prof.active then activeProfileName = prof.name end
        end
        
        local seqCount = 0
        for _ in pairs(self.db.profile.sequences) do seqCount = seqCount + 1 end
        
        self:Print("SW DUMP: Profiles=" .. profileCount .. ", Sequences=" .. seqCount .. ", Active=" .. activeProfileName)
        
    elseif cmd == "sanity" then
        local passed = true
        
        if not self.db.profile.profiles then
            self:Print("FAIL: Missing profiles table")
            passed = false
        end
        
        if not self.db.profile.sequences then
            self:Print("FAIL: Missing sequences table")
            passed = false
        end
        
        local activeCount = 0
        if self.db.profile.profiles then
            for _, prof in pairs(self.db.profile.profiles) do
                if prof.active then activeCount = activeCount + 1 end
            end
        end
        
        if activeCount > 1 then
            self:Print("FAIL: Multiple active profiles")
            passed = false
        end
        
        if passed then
            self:Print("|cff00FF00SW SANITY PASS|r")
            print(string.format('SANITY_RESULT {"addon":"SkillWeaver","status":"OK","checks":3,"failures":0}'))
        else
            self:Print("|cffFF0000SW SANITY FAIL|r")
            print(string.format('SANITY_RESULT {"addon":"SkillWeaver","status":"FAIL","checks":3,"failures":1}'))
        end
        
    elseif cmd == "rebuild" then
        for id, seq in pairs(self.db.profile.sequences) do
            seq.steps = self:ParseSteps(seq.stepsText or "")
        end
        self:Print("Sequences rebuilt.")
        
    elseif cmd == "resetdb" then
        SkillWeaverDB = nil
        ReloadUI()
        
    else
        self:ToggleUI()
    end
end

-- ============================================================================
-- Utility: JSON Serialization
-- ============================================================================

function SkillWeaver:TableToJSON(tbl)
    local function serializeValue(val)
        local vtype = type(val)
        if vtype == "string" then
            return '"' .. val:gsub('"', '\\"'):gsub('\n', '\\n') .. '"'
        elseif vtype == "number" then
            return tostring(val)
        elseif vtype == "boolean" then
            return tostring(val)
        elseif vtype == "table" then
            local isArray = true
            for k, _ in pairs(val) do
                if type(k) ~= "number" then isArray = false break end
            end
            if isArray then
                local items = {}
                for i, v in ipairs(val) do
                    table.insert(items, serializeValue(v))
                end
                return "[" .. table.concat(items, ",") .. "]"
            else
                local items = {}
                for k, v in pairs(val) do
                    table.insert(items, '"' .. k .. '":' .. serializeValue(v))
                end
                return "{" .. table.concat(items, ",") .. "}"
            end
        else
            return "null"
        end
    end
    return serializeValue(tbl)
end

function SkillWeaver:JSONToTable(str)
    local fn, err = loadstring("return " .. str)
    if fn then return fn() else error("Invalid JSON: " .. err) end
end

-- ============================================================================
-- Step Parser (MVP)
-- ============================================================================

function SkillWeaver:ParseSteps(stepsText)
    local steps = {}
    if not stepsText or stepsText == "" then return steps end
    
    for line in stepsText:gmatch("[^\r\n]+") do
        line = line:match("^%s*(.-)%s*$") -- trim
        
        -- Skip blank lines and comments
        if line == "" or line:match("^#") then
            -- skip
        else
            -- Split on first "|"
            local action, cond = line:match("^(.-)%s*|%s*(.+)$")
            if not action then
                -- No "|" found, entire line is action
                action = line
                cond = "always"
            end
            
            table.insert(steps, {
                action = action,
                cond = cond,
                enabled = true
            })
        end
    end
    
    return steps
end

-- ============================================================================
-- Condition Evaluator (MVP Whitelist)
-- ============================================================================

function SkillWeaver:EvaluateCondition(cond)
    if not cond or cond == "always" then return true end
    
    -- target.health<0.2
    local targetHealth = cond:match("target%.health%s*([<>=]+)%s*([%d%.]+)")
    if targetHealth then
        local op, val = cond:match("target%.health%s*([<>=]+)%s*([%d%.]+)")
        val = tonumber(val)
        if UnitExists("target") then
            local healthPct = UnitHealth("target") / UnitHealthMax("target")
            if op == "<" then return healthPct < val
            elseif op == ">" then return healthPct > val
            elseif op == "<=" then return healthPct <= val
            elseif op == ">=" then return healthPct >= val
            elseif op == "==" then return healthPct == val
            end
        end
        return false
    end
    
    -- player.mana>0.5
    local playerMana = cond:match("player%.mana%s*([<>=]+)%s*([%d%.]+)")
    if playerMana then
        local op, val = cond:match("player%.mana%s*([<>=]+)%s*([%d%.]+)")
        val = tonumber(val)
        local manaPct = UnitPower("player", Enum.PowerType.Mana) / UnitPowerMax("player", Enum.PowerType.Mana)
        if op == "<" then return manaPct < val
        elseif op == ">" then return manaPct > val
        elseif op == "<=" then return manaPct <= val
        elseif op == ">=" then return manaPct >= val
        elseif op == "==" then return manaPct == val
        end
        return false
    end
    
    -- cooldown(12345).ready
    local cdSpell = cond:match("cooldown%((%d+)%)%.ready")
    if cdSpell then
        local spellId = tonumber(cdSpell)
        local start, duration = GetSpellCooldown(spellId)
        return (start == 0 or (start + duration - GetTime()) <= 0)
    end
    
    -- Unknown condition: warn and return false
    if self.db.profile.settings and self.db.profile.settings.debug then
        self:Print("Unknown condition: " .. cond)
    end
    return false
end

-- ============================================================================
-- Runtime Hook (MVP)
-- ============================================================================

function SkillWeaver:GetNextAction()
    local activeProfile = nil
    for id, prof in pairs(self.db.profile.profiles) do
        if prof.active then
            activeProfile = prof
            break
        end
    end
    
    if not activeProfile then return nil end
    
    local activeSeq = nil
    for id, seq in pairs(self.db.profile.sequences) do
        if seq.profileId == activeProfile.id then
            activeSeq = seq
            break
        end
    end
    
    if not activeSeq or not activeSeq.steps then return nil end
    
    for _, step in ipairs(activeSeq.steps) do
        if step.enabled and self:EvaluateCondition(step.cond) then
            return step.action
        end
    end
    
    return nil
end

-- ============================================================================
-- Slash Commands
-- ============================================================================

SLASH_SKILLWEAVER1 = "/sw"
SLASH_SKILLWEAVER2 = "/skillweaver"
SlashCmdList["SKILLWEAVER"] = function(msg)
    local cmd = msg:lower():match("^(%S+)")
    
    if cmd == "dump" then
        local profileCount = 0
        local activeProfileName = "None"
        for _, prof in pairs(SkillWeaver.db.profile.profiles) do
            profileCount = profileCount + 1
            if prof.active then activeProfileName = prof.name end
        end
        
        local seqCount = 0
        for _ in pairs(SkillWeaver.db.profile.sequences) do seqCount = seqCount + 1 end
        
        SkillWeaver:Print("SW DUMP: Profiles=" .. profileCount .. ", Sequences=" .. seqCount .. ", Active=" .. activeProfileName)
        
    elseif cmd == "sanity" then
        local passed = true
        
        -- Check 1: Profile integrity
        if not SkillWeaver.db.profile.profiles then
            SkillWeaver:Print("FAIL: Missing profiles table")
            passed = false
        end
        
       -- Check 2: Sequence integrity
        if not SkillWeaver.db.profile.sequences then
            SkillWeaver:Print("FAIL: Missing sequences table")
            passed = false
        end
        
        -- Check 3: Active check
        local activeCount = 0
        if SkillWeaver.db.profile.profiles then
            for _, prof in pairs(SkillWeaver.db.profile.profiles) do
                if prof.active then activeCount = activeCount + 1 end
            end
        end
        
        if activeCount > 1 then
            SkillWeaver:Print("FAIL: Multiple active profiles")
            passed = false
        end
        
        if passed then
            SkillWeaver:Print("|cff00FF00SW SANITY PASS|r")
            print(string.format('SANITY_RESULT {"addon":"SkillWeaver","status":"OK","checks":3,"failures":0}'))
        else
            SkillWeaver:Print("|cffFF0000SW SANITY FAIL|r")
            print(string.format('SANITY_RESULT {"addon":"SkillWeaver","status":"FAIL","checks":3,"failures":1}'))
        end
        
    elseif cmd == "rebuild" then
        for id, seq in pairs(SkillWeaver.db.profile.sequences) do
            seq.steps = SkillWeaver:ParseSteps(seq.stepsText or "")
        end
        SkillWeaver:Print("Sequences rebuilt.")
        
    elseif cmd == "resetdb" then
        SkillWeaverDB = nil
        ReloadUI()
        
    else
        SkillWeaver:ToggleUI()
    end
end


-- ============================================================================
-- UI Construction
-- ============================================================================

function SkillWeaver:ToggleUI()
    if not self.frame then
        self:CreateMainFrame()
    end
    if self.frame:IsShown() then
        self.frame:Hide()
    else
        self.frame:Show()
    end
end

function SkillWeaver:CreateMainFrame()
    local frame = AceGUI:Create("Frame")
    frame:SetTitle("SkillWeaver")
    frame:SetStatusText("Offline-First Rotation Authoring")
    frame:SetCallback("OnClose", function(widget) widget:Hide() end)
    frame:SetLayout("Fill")
    frame:SetWidth(900)
    frame:SetHeight(650)
    
    local tabGroup = AceGUI:Create("TabGroup")
    tabGroup:SetLayout("Flow")
    tabGroup:SetTabs({
        {text="Profiles", value="profiles"},
        {text="Sequences", value="sequences"}
    })
    tabGroup:SetCallback("OnGroupSelected", function(container, event, group)
        container:ReleaseChildren()
        if group == "profiles" then
            SkillWeaver:DrawProfilesTab(container)
        elseif group == "sequences" then
            SkillWeaver:DrawSequencesTab(container)
        end
    end)
    
    frame:AddChild(tabGroup)
    tabGroup:SelectTab("profiles")
    
    self.frame = frame
end

-- ============================================================================
-- Profiles Tab
-- ============================================================================

function SkillWeaver:DrawProfilesTab(container)
    local btnNew = AceGUI:Create("Button")
    btnNew:SetText("New Profile")
    btnNew:SetWidth(150)
    btnNew:SetCallback("OnClick", function()
        local id = tostring(math.random(1000000))
        self.db.profile.profiles[id] = { 
            name = "New Profile", 
            specId = 0, 
            class = select(2, UnitClass("player")),
            active = false
        }
        container:ReleaseChildren()
        self:DrawProfilesTab(container)
    end)
    container:AddChild(btnNew)
    
    local tree = AceGUI:Create("TreeGroup")
    tree:SetLayout("Flow")
    tree:SetFullWidth(true)
    tree:SetFullHeight(true)
    tree:SetTreeWidth(200, false)
    
    local function RefreshTree()
        local t = {}
        for id, prof in pairs(self.db.profile.profiles) do
            local text = prof.name
            if prof.active then text = "|cff00ff00" .. text .. "|r" end
            table.insert(t, {value=id, text=text})
        end
        table.sort(t, function(a,b) return a.text < b.text end)
        tree:SetTree(t)
    end
    
    local activeProfileId = nil
    
    local function DrawProfileEditor(group)
        group:ReleaseChildren()
        
        if not activeProfileId then
            local l = AceGUI:Create("Label")
            l:SetText("Select a profile to edit.")
            group:AddChild(l)
            return
        end
        
        local prof = self.db.profile.profiles[activeProfileId]
        if not prof then return end
        
        -- Name
        local nameEdit = AceGUI:Create("EditBox")
        nameEdit:SetLabel("Profile Name")
        nameEdit:SetText(prof.name)
        nameEdit:SetWidth(300)
        nameEdit:SetCallback("OnEnterPressed", function(widget, event, text)
            prof.name = text
            RefreshTree()
        end)
        group:AddChild(nameEdit)
        
        -- Spec ID
        local specEdit = AceGUI:Create("EditBox")
        specEdit:SetLabel("Spec ID (e.g., 62 for Arcane Mage)")
        specEdit:SetText(tostring(prof.specId or 0))
        specEdit:SetWidth(200)
        specEdit:SetCallback("OnEnterPressed", function(w,e,t)
            prof.specId = tonumber(t) or 0
        end)
        group:AddChild(specEdit)
        
        -- Set Active
        local btnActive = AceGUI:Create("Button")
        btnActive:SetText(prof.active and "Active" or "Set Active")
        btnActive:SetWidth(150)
        btnActive:SetDisabled(prof.active)
        btnActive:SetCallback("OnClick", function()
            -- Deactivate all others
            for _, p in pairs(self.db.profile.profiles) do p.active = false end
            prof.active = true
            self.db.profile.meta.last_profileId = activeProfileId
            RefreshTree()
            group:ReleaseChildren()
            DrawProfileEditor(group)
            self:Print("Set active profile: " .. prof.name)
        end)
        group:AddChild(btnActive)
        
        -- Delete
        local btnDel = AceGUI:Create("Button")
        btnDel:SetText("Delete Profile")
        btnDel:SetWidth(150)
        btnDel:SetCallback("OnClick", function()
            self.db.profile.profiles[activeProfileId] = nil
            activeProfileId = nil
            RefreshTree()
            tree:SelectByValue(nil)
        end)
        group:AddChild(btnDel)
    end
    
    tree:SetCallback("OnGroupSelected", function(widget, event, uniquevalue)
        activeProfileId = uniquevalue
        DrawProfileEditor(tree)
    end)
    
    RefreshTree()
    container:AddChild(tree)
end

-- ============================================================================
-- Sequences Tab
-- ============================================================================

function SkillWeaver:DrawSequencesTab(container)
    local btnNew = AceGUI:Create("Button")
    btnNew:SetText("New Sequence")
    btnNew:SetWidth(150)
    btnNew:SetCallback("OnClick", function()
        local id = tostring(math.random(1000000))
        self.db.profile.sequences[id] = {
            name = "New Sequence",
            profileId = self.db.profile.meta.last_profileId,
            steps = {},
            notes = ""
        }
        container:ReleaseChildren()
        self:DrawSequencesTab(container)
    end)
    container:AddChild(btnNew)
    
    local tree = AceGUI:Create("TreeGroup")
    tree:SetLayout("Flow")
    tree:SetFullWidth(true)
    tree:SetFullHeight(true)
    tree:SetTreeWidth(200, false)
    
    local function RefreshTree()
        local t = {}
        for id, seq in pairs(self.db.profile.sequences) do
            table.insert(t, {value=id, text=seq.name})
        end
        table.sort(t, function(a,b) return a.text < b.text end)
        tree:SetTree(t)
    end
    
    local activeSeqId = nil
    
    local function DrawSeqEditor(group)
        group:ReleaseChildren()
        
        if not activeSeqId then
            local l = AceGUI:Create("Label")
            l:SetText("Select a sequence to edit.")
            group:AddChild(l)
            return
        end
        
        local seq = self.db.profile.sequences[activeSeqId]
        if not seq then return end
        
        -- Name
        local nameEdit = AceGUI:Create("EditBox")
        nameEdit:SetLabel("Sequence Name")
        nameEdit:SetText(seq.name)
        nameEdit:SetWidth(300)
        nameEdit:SetCallback("OnEnterPressed", function(widget, event, text)
            seq.name = text
            RefreshTree()
        end)
        group:AddChild(nameEdit)
        
        -- Steps (Multiline)
        local stepsBox = AceGUI:Create("MultiLineEditBox")
        stepsBox:SetLabel("Steps (Format: spellId | condition)")
        stepsBox:SetText(table.concat(seq.steps or {}, "\n"))
        stepsBox:SetNumLines(15)
        stepsBox:SetFullWidth(true)
        stepsBox:SetCallback("OnEnterPressed", function(widget, event, text)
            seq.steps = {}
            for line in text:gmatch("[^\r\n]+") do
                table.insert(seq.steps, line)
            end
            self:Print("Sequence steps saved.")
        end)
        group:AddChild(stepsBox)
        
        -- Notes
        local notesBox = AceGUI:Create("MultiLineEditBox")
        notesBox:SetLabel("Notes")
        notesBox:SetText(seq.notes or "")
        notesBox:SetNumLines(5)
        notesBox:SetFullWidth(true)
        notesBox:SetCallback("OnEnterPressed", function(w,e,text)
            seq.notes = text
        end)
        group:AddChild(notesBox)
        
        -- Delete
        local btnDel = AceGUI:Create("Button")
        btnDel:SetText("Delete Sequence")
        btnDel:SetWidth(150)
        btnDel:SetCallback("OnClick", function()
            self.db.profile.sequences[activeSeqId] = nil
            activeSeqId = nil
            RefreshTree()
            tree:SelectByValue(nil)
        end)
        group:AddChild(btnDel)
        
        -- Export
        local btnExport = AceGUI:Create("Button")
        btnExport:SetText("Export")
        btnExport:SetWidth(100)
        btnExport:SetCallback("OnClick", function()
            local exportData = {
                type = "SkillWeaverSequence",
                version = 1,
                name = seq.name,
                steps = seq.steps,
                notes = seq.notes
            }
            local jsonStr = self:TableToJSON(exportData)
            
            local popup = AceGUI:Create("Frame")
            popup:SetTitle("Export Sequence: " .. seq.name)
            popup:SetWidth(600)
            popup:SetHeight(300)
            popup:SetLayout("Fill")
            popup:SetCallback("OnClose", function(widget) AceGUI:Release(widget) end)
            
            local editBox = AceGUI:Create("MultiLineEditBox")
            editBox:SetLabel("Copy this string:")
            editBox:SetText(jsonStr)
            editBox:SetNumLines(10)
            editBox:SetFullWidth(True)
            editBox:DisableButton(true)
            popup:AddChild(editBox)
        end)
        group:AddChild(btnExport)
        
        -- Import
        local btnImport = AceGUI:Create("Button")
        btnImport:SetText("Import String")
        btnImport:SetWidth(100)
        btnImport:SetCallback("OnClick", function()
            local popup = AceGUI:Create("Frame")
            popup:SetTitle("Import Sequence")
            popup:SetWidth(600)
            popup:SetHeight(300)
            popup:SetLayout("Fill")
            popup:SetCallback("OnClose", function(widget) AceGUI:Release(widget) end)
            
            local editBox = AceGUI:Create("MultiLineEditBox")
            editBox:SetLabel("Paste sequence string:")
            editBox:SetNumLines(10)
            editBox:SetFullWidth(true)
            
            local btnConfirm = AceGUI:Create("Button")
            btnConfirm:SetText("Import")
            btnConfirm:SetWidth(150)
            btnConfirm:SetCallback("OnClick", function()
                local importStr = editBox:GetText()
                local success, data = pcall(self.JSONToTable, self, importStr)
                if success and data and data.type == "SkillWeaverSequence" then
                    seq.name = data.name
                    seq.steps = data.steps
                    seq.notes = data.notes
                    RefreshTree()
                    group:ReleaseChildren()
                    DrawSeqEditor(group)
                    self:Print("Sequence imported successfully!")
                    popup:Hide()
                else
                    self:Print("Error: Invalid sequence string.")
                end
            end)
            
            popup:AddChild(editBox)
            popup:AddChild(btnConfirm)
        end)
        group:AddChild(btnImport)
    end
    
    tree:SetCallback("OnGroupSelected", function(widget, event, uniquevalue)
        activeSeqId = uniquevalue
        DrawSeqEditor(tree)
    end)
    
    RefreshTree()
    container:AddChild(tree)
end
