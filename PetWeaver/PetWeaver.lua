
local addonName, addonTable = ...
local PetWeaver = LibStub("AceAddon-3.0"):NewAddon("PetWeaver", "AceConsole-3.0", "AceEvent-3.0")
local AceGUI = LibStub("AceGUI-3.0")

-- Data Defaults
local defaults = {
    profile = {
        teams = {},   -- [id] = { name="", pets={...} }
        scripts = {}, -- [id] = { name="New Script", text="" }
        bindings = {} -- [encounterId] = { teamId, scriptId }
    }
}

-- Safe UI Access
function PetWeaver:EnsureUI()
    self.frames = self.frames or {}
    if self.frames.journal then return end
    
    -- Try to find the XML frame
    local f = _G["PetweaverJournalFrame"]
    if not f then
        -- XML failed to load? Create placeholder to prevent nil crashes
        -- Ideally this shouldn't happen if TOC/XML are correct
        f = CreateFrame("Frame", "PetweaverJournalFrame", UIParent)
    end
    self.frames.journal = f
end

function PetWeaver:OnInitialize()
    self.db = LibStub("AceDB-3.0"):New("PetWeaverDB", defaults, true)
    
    self:RegisterChatCommand("pw", "ToggleUI")
    self:RegisterChatCommand("petweaver", "ToggleUI")
    
    self:Print("PetWeaver Loaded. Type /pw to open.")
end

function PetWeaver:OnEnable()
    self:RegisterEvent("PET_BATTLE_OPENING_START")
end

function PetWeaver:PET_BATTLE_OPENING_START()
    local npcID = C_PetBattles.GetInfo(Enum.BattlePetOwner.Enemy, 1) -- Basic NPC check?
    -- Better: C_PetBattles.GetForfeitPenalty() usually 0 for wild.
    -- Need accurate NPC ID. The best is usually from GUID of unit 'pet1' or similar?
    -- C_PetBattles.GetBattleState() ?
    
    -- MVP: Just bind to Zone or Name? 
    -- Let's try to get NPC ID from C_PetBattles.
    -- Actually, for PVE, Opponent ID 1 is the primary pet.
    local opponentID = C_PetBattles.GetActivePet(Enum.BattlePetOwner.Enemy)
    local speciesID = C_PetBattles.GetPetSpeciesID(Enum.BattlePetOwner.Enemy, opponentID)
    
    self:Print("Battle Started! Enemy Species: " .. (speciesID or "Unknown"))
    
    -- Checking Binding
    local binding = self.db.profile.bindings[speciesID] -- Simple binding by SpeciesID for now
    if binding then
         local team = self.db.profile.teams[binding.teamId]
         local script = self.db.profile.scripts[binding.scriptId]
         
         if team and script then
             self:Print("Auto-Loading Strategy: " .. team.name)
             -- Load Team Logic (If not already loaded? Too late to load inside battle start?)
             -- Actually, PET_BATTLE_OPENING_START is usually too late to Change Loadout?
             -- "Teams must be loaded BEFORE battle".
             -- If we are IN battle, we can only run the script.
             
             -- Construct runtime object for Engine
             local runtimeTeam = {
                 name = team.name,
                 script = script.text
             }
             
             if addonTable.BattleEngine then
                 addonTable.BattleEngine:StartBattle(runtimeTeam)
             else
                 self:Print("Error: BattleEngine not loaded.")
             end
         end
    end
end

-- ============================================================================
-- Utility: JSON Serialization (Simple)
-- ============================================================================

function PetWeaver:TableToJSON(tbl)
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

function PetWeaver:JSONToTable(str)
    -- Basic JSON parsing (Limited, but functional for simple structures)
    -- Use Lua's loadstring for safety? No, manual parse safer.
    -- For MVP, just use loadstring with safeguards.
    local fn, err = loadstring("return " .. str)
    if fn then return fn() else error("Invalid JSON: " .. err) end
end

-- ============================================================================
-- UI Construction (AceGUI)
-- ============================================================================

function PetWeaver:ToggleUI()
    if not self.frame then
        self:CreateMainFrame()
    end
    if self.frame:IsShown() then
        self.frame:Hide()
    else
        self.frame:Show()
    end
end

function PetWeaver:CreateMainFrame()
    local frame = AceGUI:Create("Frame")
    frame:SetTitle("PetWeaver")
    frame:SetStatusText("Offline-First Pet Battle Scripting")
    frame:SetCallback("OnClose", function(widget) widget:Hide() end)
    frame:SetLayout("Fill")
    frame:SetWidth(800)
    frame:SetHeight(600)
    
    -- Main Tabs
    local tabGroup = AceGUI:Create("TabGroup")
    tabGroup:SetLayout("Flow")
    tabGroup:SetTabs({
        {text="Teams", value="teams"},
        {text="Scripts", value="scripts"}
    })
    tabGroup:SetCallback("OnGroupSelected", function(container, event, group)
        container:ReleaseChildren()
        if group == "teams" then
            PetWeaver:DrawTeamsTab(container)
        elseif group == "scripts" then
            PetWeaver:DrawScriptsTab(container)
        end
    end)
    
    frame:AddChild(tabGroup)
    tabGroup:SelectTab("teams")
    
    self.frame = frame
end

-- ============================================================================
-- Teams Tab
-- ============================================================================

function PetWeaver:DrawTeamsTab(container)
    local btnNew = AceGUI:Create("Button")
    btnNew:SetText("New Team")
    btnNew:SetWidth(200)
    btnNew:SetCallback("OnClick", function()
        local id = tostring(math.random(1000000))
        self.db.profile.teams[id] = { name="New Team", pets={ {}, {}, {} } }
        -- Refresh handled below via redraw or tree refresh hook
        -- To keep it simple, we just re-select current tab
        container:ReleaseChildren()
        self:DrawTeamsTab(container) 
    end)
    container:AddChild(btnNew)

    local tree = AceGUI:Create("TreeGroup")
    tree:SetLayout("Flow")
    tree:SetFullWidth(true)
    tree:SetFullHeight(true)
    tree:SetTreeWidth(200, false)
    
    local function RefreshTree()
        local t = {}
        for id, team in pairs(self.db.profile.teams) do
            table.insert(t, {value=id, text=team.name})
        end
        table.sort(t, function(a,b) return a.text < b.text end)
        tree:SetTree(t)
    end
    
    local activeTeamId = nil
    
    local function DrawTeamEditor(group)
        group:ReleaseChildren()
        
        if not activeTeamId then 
            local l = AceGUI:Create("Label")
            l:SetText("Select a team to edit.")
            group:AddChild(l)
            return
        end
        
        local team = self.db.profile.teams[activeTeamId]
        if not team then return end
        
        -- Header Actions
        local grpHeader = AceGUI:Create("SimpleGroup")
        grpHeader:SetLayout("Flow")
        grpHeader:SetFullWidth(true)
        
        local btnLoad = AceGUI:Create("Button")
        btnLoad:SetText("Equip Team")
        btnLoad:SetWidth(120)
        btnLoad:SetCallback("OnClick", function()
            self:Print("Equipping " .. team.name)
            for i=1,3 do
                local p = team.pets[i]
                if p and p.speciesId then
                   -- Basic load logic (To be refined with proper PetID lookup)
                   -- MVP: Just print for now, hook up C_PetJournal logic later
                   self:Print("Slot "..i..": Species "..(p.speciesId or "None"))
                end
            end
        end)
        grpHeader:AddChild(btnLoad)
        
        local btnImport = AceGUI:Create("Button")
        btnImport:SetText("Import Equipped")
        btnImport:SetWidth(120)
        btnImport:SetCallback("OnClick", function()
             for i=1,3 do
                local pid, speciesID, _, _, _, _, _, name = C_PetJournal.GetPetLoadOutInfo(i)
                if pid then
                    local _, _, _, _, _, _, _, _, _, _, _, displayID, _, _, modID = C_PetJournal.GetPetInfoByPetID(pid)
                    local a1, a2, a3 = C_PetJournal.GetPetAbilityList(speciesID, true, false) 
                    -- MVP: Just grabbing species. Abilities require slot lookup. 
                    team.pets[i] = { speciesId = speciesID, name = name }
                else
                    team.pets[i] = {}
                end
             end
             group:ReleaseChildren()
             DrawTeamEditor(group) -- Redraw
             self:Print("Imported current team.")
        end)
        grpHeader:AddChild(btnImport)
        
        local btnDel = AceGUI:Create("Button")
        btnDel:SetText("Delete Team")
        btnDel:SetWidth(120)
        btnDel:SetCallback("OnClick", function()
             self.db.profile.teams[activeTeamId] = nil
             activeTeamId = nil
             RefreshTree()
             tree:SelectByValue(nil)
        end)
        grpHeader:AddChild(btnDel)
        
        -- Export Button
        local btnExport = AceGUI:Create("Button")
        btnExport:SetText("Export")
        btnExport:SetWidth(100)
        btnExport:SetCallback("OnClick", function()
            local exportData = {
                type = "PetWeaverTeam",
                version = 1,
                name = team.name,
                pets = team.pets
            }
            local jsonStr = self:TableToJSON(exportData)
            
            -- Show popup with export string
            local popup = AceGUI:Create("Frame")
            popup:SetTitle("Export Team: " .. team.name)
            popup:SetWidth(600)
            popup:SetHeight(300)
            popup:SetLayout("Fill")
            popup:SetCallback("OnClose", function(widget) AceGUI:Release(widget) end)
            
            local editBox = AceGUI:Create("MultiLineEditBox")
            editBox:SetLabel("Copy this string:")
            editBox:SetText(jsonStr)
            editBox:SetNumLines(10)
            editBox:SetFullWidth(true)
            editBox:DisableButton(true)
            popup:AddChild(editBox)
        end)
        grpHeader:AddChild(btnExport)
        
        -- Import Button (Team-level import to replace current)
        local btnImportStr = AceGUI:Create("Button")
        btnImportStr:SetText("Import String")
        btnImportStr:SetWidth(100)
        btnImportStr:SetCallback("OnClick", function()
            local popup = AceGUI:Create("Frame")
            popup:SetTitle("Import Team String")
            popup:SetWidth(600)
            popup:SetHeight(300)
            popup:SetLayout("Fill")
            popup:SetCallback("OnClose", function(widget) AceGUI:Release(widget) end)
            
            local editBox = AceGUI:Create("MultiLineEditBox")
            editBox:SetLabel("Paste team string:")
            editBox:SetNumLines(10)
            editBox:SetFullWidth(true)
            
            local btnConfirm = AceGUI:Create("Button")
            btnConfirm:SetText("Import")
            btnConfirm:SetWidth(150)
            btnConfirm:SetCallback("OnClick", function()
                local importStr = editBox:GetText()
                local success, data = pcall(self.JSONToTable, self, importStr)
                if success and data and data.type == "PetWeaverTeam" then
                    team.name = data.name
                    team.pets = data.pets
                    RefreshTree()
                    group:ReleaseChildren()
                    DrawTeamEditor(group)
                    self:Print("Team imported successfully!")
                    popup:Hide()
                else
                    self:Print("Error: Invalid team string.")
                end
            end)
            
            popup:AddChild(editBox)
            popup:AddChild(btnConfirm)
        end)
        grpHeader:AddChild(btnImportStr)
        
        group:AddChild(grpHeader)
        
        -- Name Edit
        local nameEdit = AceGUI:Create("EditBox")
        nameEdit:SetLabel("Team Name")
        nameEdit:SetText(team.name)
        nameEdit:SetWidth(300)
        nameEdit:SetCallback("OnEnterPressed", function(widget, event, text)
             team.name = text
             RefreshTree()
        end)
        group:AddChild(nameEdit)
        
        -- 3 Pet Slots
        for i=1,3 do
            local p = team.pets[i] or {}
            local box = AceGUI:Create("InlineGroup")
            box:SetTitle("Slot " .. i)
            box:SetLayout("Flow")
            box:SetFullWidth(true)
            
            local sEdit = AceGUI:Create("EditBox")
            sEdit:SetLabel("Species ID")
            sEdit:SetText(p.speciesId or "")
            sEdit:SetWidth(100)
            sEdit:SetCallback("OnEnterPressed", function(w,e,t) p.speciesId = tonumber(t) end)
            box:AddChild(sEdit)
            
            local nEdit = AceGUI:Create("EditBox")
            nEdit:SetLabel("Abilities (Comma sep)")
            nEdit:SetText(table.concat(p.abilities or {}, ","))
            nEdit:SetWidth(200)
            nEdit:SetCallback("OnEnterPressed", function(w,e,t) 
                -- parse "111,222,333"
                p.abilities = {}
                for num in string.gmatch(t, "([^,]+)") do
                    table.insert(p.abilities, tonumber(num))
                end
            end)
            box:AddChild(nEdit)
            
            group:AddChild(box)
        end
    end
    
    tree:SetCallback("OnGroupSelected", function(widget, event, uniquevalue)
        activeTeamId = uniquevalue
        DrawTeamEditor(tree)
    end)
    
    RefreshTree()
    container:AddChild(tree)
end


function PetWeaver:DrawScriptsTab(container)
    local label = AceGUI:Create("Label")
    label:SetText("Script Authoring Coming Soon")
    container:AddChild(label)
end
-- ============================================================================
local function GetPetDetails(petID)
    if not petID then return nil end
    local speciesID, customName, level, _, _, _, _, name, icon = C_PetJournal.GetPetInfoByPetID(petID)
    return {icon = icon, name = customName or name, level = level}
end

-- ============================================================================
-- Queue Management
-- ============================================================================

local function AddToQueue(petID)
    -- Check if already in queue
    for _, pid in ipairs(addonTable.levelingQueue) do
        if pid == petID then
            print("Pet is already in leveling queue.")
            return
        end
    end
    tinsert(addonTable.levelingQueue, petID)
    PlaySound(SOUNDKIT.IG_BACKPACK_OPEN)
    print("Added to Leveling Queue.")
end

local function RemoveFromQueue(index)
    tremove(addonTable.levelingQueue, index)
    PlaySound(SOUNDKIT.IG_BACKPACK_CLOSE)
    PetweaverList_Update() -- Refresh immediately if looking at queue
end

-- ============================================================================
-- Team Management
-- ============================================================================

local function UpdateTeamSlots()
    local p1 = C_PetJournal.GetPetLoadOutInfo(1)
    local p2 = C_PetJournal.GetPetLoadOutInfo(2)
    local p3 = C_PetJournal.GetPetLoadOutInfo(3)

    local loadoutFrame = PetWeaver.frames.journal.RightInset.TeamLoadout
    local function SetSlot(btn, pid)
        if pid then
            local d = GetPetDetails(pid)
            btn.Icon:SetTexture(d.icon)
            btn.Icon:Show()
        else
            btn.Icon:Hide()
        end
    end
    SetSlot(loadoutFrame.Slot1, p1)
    SetSlot(loadoutFrame.Slot2, p2)
    SetSlot(loadoutFrame.Slot3, p3)
end

local function LoadTeam(teamIndex)
    local team = addonTable.savedTeams[teamIndex]
    if not team then return end
    print("Loading Team: " .. team.name)
    if team.pets[1] then C_PetJournal.SetPetLoadOutInfo(1, team.pets[1]) end
    if team.pets[2] then C_PetJournal.SetPetLoadOutInfo(2, team.pets[2]) end
    if team.pets[3] then C_PetJournal.SetPetLoadOutInfo(3, team.pets[3]) end
    PlaySound(SOUNDKIT.IG_ABILITY_PAGE_TURN)
    C_Timer.After(0.2, UpdateTeamSlots)
end

local function SaveActiveTeam()
    local p1 = C_PetJournal.GetPetLoadOutInfo(1)
    local p2 = C_PetJournal.GetPetLoadOutInfo(2)
    local p3 = C_PetJournal.GetPetLoadOutInfo(3)
    if not p1 and not p2 and not p3 then print("Cannot save empty team.") return end

    local d = GetPetDetails(p1)
    local teamName = "Team: " .. (d and d.name or "Unnamed")
    local icon = d and d.icon or "Interface\\Icons\\inv_misc_questionmark"

    tinsert(addonTable.savedTeams, {
        name = teamName,
        pets = {p1, p2, p3},
        icon = icon
    })
    PlaySound(SOUNDKIT.IG_CHARACTER_INFO_TAB)
    print("Saved " .. teamName)
    if currentTab == 2 then PetweaverList_Update() end
end

local function EquipSelectedPet()
    if not selectedID or currentTab ~= 1 then return end
    local p1 = C_PetJournal.GetPetLoadOutInfo(1)
    local p2 = C_PetJournal.GetPetLoadOutInfo(2)
    local p3 = C_PetJournal.GetPetLoadOutInfo(3)
    local target = 1
    if not p1 then target = 1 elseif not p2 then target = 2 elseif not p3 then target = 3 end
    C_PetJournal.SetPetLoadOutInfo(target, selectedID)
    PlaySound(SOUNDKIT.IG_ABILITY_PAGE_TURN)
    C_Timer.After(0.2, UpdateTeamSlots)
end

-- ============================================================================
-- Display Logic
-- ============================================================================

local function UpdatePetCard(petID)
    local frame = PetWeaver.frames.journal.RightInset.SelectedPetDetails
    local speciesID, customName, level, _, _, _, _, name, icon, petType = C_PetJournal.GetPetInfoByPetID(petID)
    local _, _, _, _, rarity = C_PetJournal.GetPetStats(petID)
    local rarityColor = ITEM_QUALITY_COLORS[rarity-1]

    frame.PetName:SetText(customName or name)
    if rarityColor then frame.PetName:SetTextColor(rarityColor.r, rarityColor.g, rarityColor.b) end
    local _, _, _, _, _, _, _, _, _, _, _, displayID = C_PetJournal.GetPetInfoBySpeciesID(speciesID)
    if displayID then frame.ModelFrame:SetDisplayInfo(displayID) end
    frame.TypeIcon:SetTexture(GetPetTypeTexture(petType))
    local health, power, speed = C_PetJournal.GetPetStats(petID)
    frame.HealthText:SetText("Health: " .. health)
    frame.PowerText:SetText("Power: " .. power)
    frame.SpeedText:SetText("Speed: " .. speed)
end

-- ============================================================================
-- SCROLL LIST LOGIC
-- ============================================================================

local function UpdatePetData()
    addonTable.petList = addonTable.petList or {}
    wipe(addonTable.petList)
    local _, numOwned = C_PetJournal.GetNumPets()
    local searchLower = string.lower(currentSearch or "")

    for i = 1, numOwned do
        local petID, speciesID, owned, customName, level, _, _, speciesName, icon = C_PetJournal.GetPetInfoByIndex(i)
        
        if petID then
            local displayName = customName or speciesName
            local match = true
            if currentSearch ~= "" then
                if not string.find(string.lower(displayName), searchLower, 1, true) then match = false end
            end

            if match then
                local _, _, _, _, rarity = C_PetJournal.GetPetStats(petID)
                local rarityColor = ITEM_QUALITY_COLORS[rarity-1] 
                tinsert(addonTable.petList, {
                    petID = petID,
                    displayName = displayName,
                    level = level,
                    icon = icon,
                    rarityColor = rarityColor
                })
            end
        end
    end
    PetweaverList_Update()
end

function PetweaverList_Update()
    PetWeaver:EnsureUI()
    if not PetWeaver.frames.journal or not PetWeaver.frames.journal.LeftInset then return end
    local scrollFrame = PetWeaver.frames.journal.LeftInset.ListScrollFrame
    if not scrollFrame then return end
    local buttons = scrollFrame.buttons
    if not buttons then return end
    local offset = HybridScrollFrame_GetOffset(scrollFrame)

    -- DETERMINE DATA SOURCE
    local dataList = {}
    if currentTab == 1 then
        dataList = addonTable.petList
    elseif currentTab == 2 then
        dataList = addonTable.savedTeams
    elseif currentTab == 3 then
        -- Build queue display list on the fly
        for i, pid in ipairs(addonTable.levelingQueue) do
            local d = GetPetDetails(pid)
            if d then
                tinsert(dataList, {petID=pid, displayName=d.name, level=d.level, icon=d.icon})
            end
        end
    end

    local numItems = #dataList

    for i = 1, #buttons do
        local button = buttons[i]
        local index = offset + i 
        
        if index <= numItems then
            local item = dataList[index]
            button:Show()
            
            if currentTab == 2 then
                -- TEAMS
                button.name:SetText(item.name)
                button.name:SetTextColor(1, 0.82, 0)
                button.level:SetText("3 Pets")
                button.icon:SetTexture(item.icon)
                button.rarityBorder:Hide()
                button.dataID = index 
            else
                -- PETS OR QUEUE
                button.name:SetText(item.displayName)
                button.level:SetText("Level " .. item.level)
                button.icon:SetTexture(item.icon)
                if currentTab == 3 then
                    button.name:SetTextColor(0, 1, 0) -- Green text for Queue
                elseif item.rarityColor then
                    button.name:SetTextColor(item.rarityColor.r, item.rarityColor.g, item.rarityColor.b)
                    button.rarityBorder:SetVertexColor(item.rarityColor.r, item.rarityColor.g, item.rarityColor.b)
                    button.rarityBorder:Show()
                else
                    button.name:SetTextColor(1, 1, 1)
                    button.rarityBorder:Hide()
                end
                button.dataID = (currentTab == 3) and index or item.petID 
            end
            
            if button.dataID == selectedID then button:LockHighlight() else button:UnlockHighlight() end
        else
            button:Hide()
        end
    end
    HybridScrollFrame_Update(scrollFrame, numItems * 46, scrollFrame:GetHeight())
end

-- ============================================================================
-- INTERACTION
-- ============================================================================

function Petweaver_OnListButtonClicked(self, button)
    if not self.dataID then return end
    selectedID = self.dataID

    if currentTab == 1 then
        -- TAB 1: Main List
        if button == "RightButton" then
            -- Right Click: Add to Queue
            AddToQueue(selectedID)
        else
            -- Left Click: Select
            UpdatePetCard(selectedID)
            if IsShiftKeyDown() then EquipSelectedPet() end
        end

    elseif currentTab == 2 then
        -- TAB 2: Teams
        LoadTeam(selectedID)

    elseif currentTab == 3 then
        -- TAB 3: Queue
        if button == "RightButton" then
            -- Right Click: Remove from Queue (self.dataID is the index here)
            RemoveFromQueue(selectedID)
        else
            -- Left Click: Preview the pet
            -- (We need to get the real petID from the queue table)
            local realPetID = addonTable.levelingQueue[selectedID]
            if realPetID then UpdatePetCard(realPetID) end
        end
    end
    PetweaverList_Update()
end

local function SetTab(id)
    currentTab = id
    PanelTemplates_SetTab(PetWeaver.frames.journal, id)
    selectedID = nil
    currentSearch = ""
    PetWeaver.frames.journal.LeftInset.FilterHeader.SearchBox:SetText("")
    UpdatePetData()
end

-- ============================================================================
-- INIT
-- ============================================================================

local function EnsureState()
    PetWeaverDB = PetWeaverDB or {}
    PetWeaverDB.teams = PetWeaverDB.teams or {}
    PetWeaverDB.queue = PetWeaverDB.queue or {}
    PetWeaverDB.settings = PetWeaverDB.settings or { debug = false }
    
    addonTable.savedTeams = PetWeaverDB.teams
    addonTable.levelingQueue = PetWeaverDB.queue
    addonTable.petList = addonTable.petList or {}
    
    PetWeaver.frames = PetWeaver.frames or {}
end

local function OnEvent(self, event, ...)
    if event == "ADDON_LOADED" then
        local name = ...
        if name == addonName then
            PetWeaverDB = PetWeaverDB or {}
            
            -- SAFE MIGRATION (v1)
            if not PetWeaverDB.version or PetWeaverDB.version < 1 then
                PetWeaverDB.version = 1
                PetWeaverDB.settings = PetWeaverDB.settings or { debug = false }
                PetWeaverDB.teams = PetWeaverDB.teams or {}
                PetWeaverDB.queue = PetWeaverDB.queue or {}
                
                -- Default Starter Team if empty
                if #PetWeaverDB.teams == 0 then
                    tinsert(PetWeaverDB.teams, {name="Starter Team", pets={nil, nil, nil}, icon="Interface\\Icons\\inv_misc_questionmark"})
                end
                print("|cff00FF00PetWeaver|r: Database Migrated to v1.")
            else
                -- Integrity Assurance
                PetWeaverDB.teams = PetWeaverDB.teams or {}
                PetWeaverDB.queue = PetWeaverDB.queue or {}
            end
            
            -- Bind to Addon Table (Runtime)
            addonTable.savedTeams = PetWeaverDB.teams
            addonTable.levelingQueue = PetWeaverDB.queue
            
            print("|cff00FF00PetWeaver|r: Loaded.")
        end

    elseif event == "PLAYER_LOGIN" then
        EnsureState() -- Critical: Ensure data tables exist
        PetWeaver:EnsureUI() -- Critical: Ensure UI frames exist
        
        if PetweaverJournalFrameTitleText then PetweaverJournalFrameTitleText:SetText("Petweaver Journal"); end

        local f = PetWeaver.frames.journal
        if not f or not f.LeftInset then
             print("|cffDAA520PetWeaver|r: UI XML minimal or missing LeftInset; skipping UI init.")
             return
        end

        if PetWeaver.frames and PetWeaver.frames.journal and PetWeaver.frames.journal.PetsTab then
            PetWeaver.frames.journal.PetsTab:SetScript("OnClick", function() SetTab(1) end)
            PetWeaver.frames.journal.TeamsTab:SetScript("OnClick", function() SetTab(2) end)
            PetWeaver.frames.journal.QueueTab:SetScript("OnClick", function() SetTab(3) end) 
            
            PanelTemplates_SetNumTabs(PetWeaver.frames.journal, 3);
            SetTab(1)
        end

        local searchBox = PetWeaver.frames.journal.LeftInset.FilterHeader.SearchBox
        searchBox:SetScript("OnTextChanged", function(self)
            currentSearch = self:GetText()
            UpdatePetData()
        end)

        local scrollFrame = PetWeaver.frames.journal.LeftInset.ListScrollFrame
        HybridScrollFrame_CreateButtons(scrollFrame, "PetweaverListButtonTemplate", 0, 0)
        scrollFrame.update = PetweaverList_Update
        
        if PetWeaver.frames.journal.RightInset.TeamLoadout.SaveTeamButton then
             PetWeaver.frames.journal.RightInset.TeamLoadout.SaveTeamButton:SetScript("OnClick", SaveActiveTeam)
        end

        UpdatePetData()
        UpdateTeamSlots()

    elseif event == "PET_JOURNAL_LIST_UPDATE" then
        UpdatePetData()
    end
end

local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("ADDON_LOADED")
eventFrame:RegisterEvent("PLAYER_LOGIN")
eventFrame:RegisterEvent("PET_JOURNAL_LIST_UPDATE")
eventFrame:SetScript("OnEvent", OnEvent)

SLASH_PETWEAVER1 = "/petweaver"
SLASH_PETWEAVER2 = "/pw"
SlashCmdList["PETWEAVER"] = function(msg)
    msg = tostring(msg or "")
    local cmd, arg = msg:lower():match("^(%S+)%s*(.*)")
    
    if cmd == "dump" then
        if not PetWeaverDB then return end
        local t = #PetWeaverDB.teams
        local q = #PetWeaverDB.queue
        print("PW DUMP: Teams="..t..", Queue="..q)
        
    elseif cmd == "sanity" then
        if not PetWeaverDB then return end
        local passed = true
        if not PetWeaverDB.teams then passed = false; print("FAIL: Missing Teams table") end
        if not PetWeaverDB.queue then passed = false; print("FAIL: Missing Queue table") end
        
        if passed then
             print("|cff00FF00PW SANITY PASS|r")
             print(string.format('SANITY_RESULT {"addon":"PetWeaver","status":"OK","checks":2,"failures":0}'))
        else
             print("|cffrr0000PW SANITY FAIL|r")
             print(string.format('SANITY_RESULT {"addon":"PetWeaver","status":"FAIL","checks":2,"failures":1}'))
        end
        
    elseif cmd == "resetdb" then
        PetWeaverDB = {
            version = 1,
            settings = { debug = false },
            teams = {},
            queue = {}
        }
        -- Restore default
        tinsert(PetWeaverDB.teams, {name="Starter Team", pets={nil, nil, nil}, icon="Interface\\Icons\\inv_misc_questionmark"})
        ReloadUI()
        
    else
        if PetWeaver.frames.journal:IsShown() then PetWeaver.frames.journal:Hide() else PetWeaver.frames.journal:Show() end
    end
end
