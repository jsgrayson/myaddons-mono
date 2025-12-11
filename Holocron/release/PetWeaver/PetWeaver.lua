-- PetWeaver.lua (Native WoW API Version)
local addonName, addon = ...
print("|cff00ff00PetWeaver:|r Native Core Loaded.")

-- 1. SavedVariables Setup
PetWeaverDB = PetWeaverDB or {
    settings = { 
        uiScale = 1.0,
        autoBattle = false,
        autoLoadTeams = true,
        showCoachMode = true
    },
    teams = {},
    encounterDatabase = {},
    battleHistory = {},
    version = "1.0"
}

-- Load default teams on first launch
local function LoadDefaultTeams()
    print("|cff00ff00PetWeaver:|r LoadDefaultTeams() called")
    print("|cff00ff00PetWeaver:|r Current teams count:", #PetWeaverDB.teams)
    print("|cff00ff00PetWeaver:|r PetWeaver_DefaultTeams available:", PetWeaver_DefaultTeams ~= nil)
    
    if #PetWeaverDB.teams == 0 and PetWeaver_DefaultTeams then
        print("|cff00ff00PetWeaver:|r Loading default teams...")
        for _, teamData in ipairs(PetWeaver_DefaultTeams) do
            -- Deep copy the team
            local team = {
                name = teamData.name,
                enemyName = teamData.encounterName, -- Map encounterName to enemyName for internal consistency
                isLeveling = teamData.isLeveling,
                pets = {},
                script = teamData.script or {}
            }
            
            for i, speciesID in ipairs(teamData.pets) do
                table.insert(team.pets, {
                    speciesID = speciesID,
                    name = "", -- Name will be fetched later or is not needed for ID-based loading
                    abilities = {}, -- Abilities will be loaded from saved sets or defaults
                    slot = i,
                    isLeveling = (speciesID == 0),
                    level = 25
                })
            end
            
            table.insert(PetWeaverDB.teams, team)
        end
        print("|cff00ff00PetWeaver:|r Loaded " .. #PetWeaverDB.teams .. " default teams")
    else
        print("|cff00ff00PetWeaver:|r Skipping load - teams already exist or data not available")
    end
    
    -- Load encounter database
    if PetWeaver_Encounters then
        print("|cff00ff00PetWeaver:|r Loading encounter database...")
        local count = 0
        for encounterName, encounterData in pairs(PetWeaver_Encounters) do
            PetWeaverDB.encounterDatabase[encounterName] = encounterData
            count = count + 1
        end
        print("|cff00ff00PetWeaver:|r Loaded " .. count .. " encounters")
    else
        print("|cff00ff00PetWeaver:|r No encounters data found")
    end
end


-- 2. Event Handling
local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("PLAYER_LOGIN")
eventFrame:RegisterEvent("ADDON_LOADED")
eventFrame:RegisterEvent("PET_BATTLE_OPENING_START")
eventFrame:RegisterEvent("PET_BATTLE_TURN_STARTED")
eventFrame:RegisterEvent("PET_BATTLE_OVER")


eventFrame:SetScript("OnEvent", function(self, event, ...)
    if event == "ADDON_LOADED" and ... == addonName then
        -- Initialize SavedVariables first
        PetWeaverDB = PetWeaverDB or { settings = {}, teams = {}, encounterDatabase = {}, battleHistory = {} }
        
        -- Debug: Check if data files loaded
        print("|cff00ff00PetWeaver:|r Addon loaded, checking data files...")
        print("|cff00ff00PetWeaver:|r PetWeaver_DefaultTeams exists:", PetWeaver_DefaultTeams ~= nil)
        print("|cff00ff00PetWeaver:|r PetWeaver_Encounters exists:", PetWeaver_Encounters ~= nil)
        
        if PetWeaver_DefaultTeams then
            print("|cff00ff00PetWeaver:|r Found", #PetWeaver_DefaultTeams, "default teams in data file")
        end
        
        -- Load default teams and encounters
        LoadDefaultTeams()
        print("|cff00ff00PetWeaver:|r Ready. Current teams:", #PetWeaverDB.teams)
        
    elseif event == "PLAYER_LOGIN" then
        -- Initialize Battle UI after player logs in
        addon:InitBattleUI()
        print("|cff00ff00PetWeaver:|r Battle UI initialized")
        
    elseif event == "ADDON_LOADED" and ... == "Blizzard_Collections" then
        print("|cff00ff00PetWeaver:|r Hooking Pet Journal...")
        addon:HookPetJournal()
        
    elseif event == "PET_BATTLE_OPENING_START" then
        print("|cff00ff00PetWeaver:|r Battle Started!")
        
        -- Auto-load matching team if enabled
        if PetWeaverDB.settings.autoLoadTeams then
            addon:AutoLoadTeam()
        end
        
        if addon.BattleFrame then
            addon.BattleFrame:Show()
            addon:UpdateBattleUI()
        end
    elseif event == "PET_BATTLE_TURN_STARTED" then
        -- Auto-execute move if auto-battle is enabled
        if PetWeaverDB.settings.autoBattle and addon.BattleEngine and addon.BattleEngine.active then
            C_Timer.After(0.3, function()
                if C_PetBattles.IsInBattle() then
                    addon.BattleEngine:ExecuteNextCommand()
                end
            end)
        end
    elseif event == "PET_BATTLE_OVER" then
        -- Stop battle engine
        if addon.BattleEngine then
            addon.BattleEngine:StopBattle()
        end
        
        -- Log battle outcome
        addon:LogBattleOutcome()
        
        if addon.BattleFrame then
            addon.BattleFrame:Hide()
        end
    end
end)

-- 3. Battle UI
function addon:InitBattleUI()
    if addon.BattleFrame then return end
    
    local f = CreateFrame("Frame", "PetWeaverBattleFrame", UIParent, "BackdropTemplate")
    f:SetSize(350, 120)
    f:SetPoint("TOP", UIParent, "TOP", 0, -50)
    f:SetBackdrop({
        bgFile = "Interface\\Buttons\\WHITE8X8",
        edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
        tile = false, edgeSize = 16,
        insets = { left = 4, right = 4, top = 4, bottom = 4 }
    })
    f:SetBackdropColor(0, 0, 0, 0.9)
    f:SetBackdropBorderColor(0.4, 0.35, 0.2, 1)
    f:SetFrameStrata("HIGH")
    f:Hide()
    
    -- Title
    local title = f:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    title:SetPoint("TOP", 0, -10)
    title:SetText("PetWeaver Battle Assistant")
    title:SetTextColor(1, 0.82, 0)
    
    -- Enemy Name
    f.enemyName = f:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    f.enemyName:SetPoint("TOPLEFT", 10, -35)
    f.enemyName:SetText("Enemy: Unknown")
    
    -- Leveling Pet Info
    f.levelingPet = f:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    f.levelingPet:SetPoint("TOPLEFT", 10, -55)
    f.levelingPet:SetText("Leveling: None")
    f.levelingPet:SetTextColor(0.5, 1, 0.5)
    
    -- Auto Battle Toggle
    local autoBtn = CreateFrame("CheckButton", nil, f, "UICheckButtonTemplate")
    autoBtn:SetSize(20, 20)
    autoBtn:SetPoint("BOTTOMLEFT", 10, 10)
    autoBtn.text = autoBtn:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    autoBtn.text:SetPoint("LEFT", autoBtn, "RIGHT", 5, 0)
    autoBtn.text:SetText("Auto Battle")
    autoBtn:SetScript("OnClick", function(self)
        PetWeaverDB.settings.autoBattle = self:GetChecked()
        if self:GetChecked() then
            print("|cff00ff00PetWeaver:|r Auto Battle enabled")
        else
            print("|cff00ff00PetWeaver:|r Auto Battle disabled")
        end
    end)
    f.autoBtn = autoBtn
    
    -- Auto Battle Action Button (Press to execute next move)
    local actionBtn = CreateFrame("Button", "PetWeaverAutoBattleBtn", f, "UIPanelButtonTemplate")
    actionBtn:SetSize(90, 25)
    actionBtn:SetPoint("BOTTOM", f, "BOTTOM", 0, 10)
    actionBtn:SetText("Auto Move")
    actionBtn:SetScript("OnClick", function()
        addon:ExecuteAutoBattleMove()
    end)
    f.actionBtn = actionBtn
    
    -- Suggestion Text
    f.suggestion = f:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    f.suggestion:SetPoint("BOTTOMRIGHT", -10, 10)
    f.suggestion:SetText("No saved team")
    f.suggestion:SetTextColor(0.7, 0.7, 0.7)
    
    -- Close Button (X)
    local closeBtn = CreateFrame("Button", nil, f, "UIPanelCloseButton")
    closeBtn:SetSize(20, 20)
    closeBtn:SetPoint("TOPRIGHT", -2, -2)
    
    addon.BattleFrame = f
    print("|cff00ff00PetWeaver:|r Battle UI initialized.")
end

function addon:UpdateBattleUI()
    if not addon.BattleFrame then return end
    
    -- Get enemy info
    local enemyName = C_PetBattles.GetName(Enum.BattlePetOwner.Enemy)
    if enemyName then
        addon.BattleFrame.enemyName:SetText("Enemy: " .. enemyName)
        
        -- Check if we have a saved team
        local foundTeam = nil
        for _, team in ipairs(PetWeaverDB.teams) do
            if team.enemyName == enemyName then
                foundTeam = team
                break
            end
        end
        
        if foundTeam then
            addon.BattleFrame.suggestion:SetText("Using: " .. (foundTeam.name or "Unnamed"))
            addon.BattleFrame.suggestion:SetTextColor(0, 1, 0)
        else
            addon.BattleFrame.suggestion:SetText("No saved team")
            addon.BattleFrame.suggestion:SetTextColor(0.7, 0.7, 0.7)
        end
    end
    
    -- Show leveling pet
    local levelingQueue = PetWeaverDB.levelingQueue or {}
    if #levelingQueue > 0 then
        local petID = levelingQueue[1]
        local _, customName, level, _, _, _, _, petName = C_PetJournal.GetPetInfoByPetID(petID)
        local name = customName or petName or "Unknown"
        addon.BattleFrame.levelingPet:SetText("Leveling: " .. name .. " (Lvl " .. level .. ")")
    else
        addon.BattleFrame.levelingPet:SetText("Leveling: None (Add pets to queue)")
    end
    
    -- Auto battle checkbox
    if addon.BattleFrame.autoBtn then
        addon.BattleFrame.autoBtn:SetChecked(PetWeaverDB.settings.autoBattle or false)
    end
end

-- Auto Battle Logic with Script Execution
addon.currentScript = nil
addon.currentRound = 0
addon.scriptStep = 1

function addon:ExecuteAutoBattleMove()
    if not C_PetBattles.IsInBattle() then
        print("|cff00ff00PetWeaver:|r Not in a battle")
        return
    end
    
    if C_PetBattles.IsPlayerNPC(Enum.BattlePetOwner.Ally) then
        print("|cff00ff00PetWeaver:|r Cannot control NPC battles")
        return
    end
    
    -- Track round number
    addon.currentRound = (addon.currentRound or 0) + 1
    
    -- Use new Battle Engine if available
    if addon.BattleEngine and addon.BattleEngine:IsEnabled() then
        addon.BattleEngine:ExecuteNextCommand()
        return
    end
    
    -- Legacy: If we have a loaded script, execute it
    if addon.currentScript and addon.currentScript.script then
        local success = addon:ExecuteScriptStep()
        if success then
            return
        end
    end
    
    -- Fallback: intelligent ability selection
    addon:ExecuteIntelligentMove()
end

function addon:ExecuteScriptStep()
    local script = addon.currentScript.script
    
    -- Find the current step based on round
    local step = nil
    for _, s in ipairs(script) do
        if s.round == addon.currentRound then
            step = s
            break
        end
    end
    
    if not step then
        -- No scripted move for this round, use intelligent fallback
        return false
    end
    
    if step.action == "ability" then
        local activePet = C_PetBattles.GetActivePet(Enum.BattlePetOwner.Ally)
        local _, _, _, canUse = C_PetBattles.GetAbilityInfo(Enum.BattlePetOwner.Ally, activePet, step.abilitySlot)
        
        if canUse then
            C_PetBattles.UseAbility(step.abilitySlot)
            if PetWeaverDB.settings.showCoachMode then
                print("|cff00ff00PetWeaver:|r Round " .. addon.currentRound .. ": Using ability slot " .. step.abilitySlot)
            end
            return true
        else
            print("|cff00ff00PetWeaver:|r Ability " .. step.abilitySlot .. " not available, using fallback")
            return false
        end
        
    elseif step.action == "swap" then
        local targetSlot = step.targetSlot
        if targetSlot and targetSlot >= 1 and targetSlot <= 3 then
            C_PetBattles.ChangePet(targetSlot)
            if PetWeaverDB.settings.showCoachMode then
                print("|cff00ff00PetWeaver:|r Round " .. addon.currentRound .. ": Swapping to pet slot " .. targetSlot)
            end
            return true
        end
    end
    
    return false
end

function addon:ExecuteIntelligentMove()
    -- Intelligent move selection when no script is available
    local activePet = C_PetBattles.GetActivePet(Enum.BattlePetOwner.Ally)
    local health = C_PetBattles.GetHealth(Enum.BattlePetOwner.Ally, activePet)
    local maxHealth = C_PetBattles.GetMaxHealth(Enum.BattlePetOwner.Ally, activePet)
    local healthPercent = (health / maxHealth) * 100
    
    local enemyActivePet = C_PetBattles.GetActivePet(Enum.BattlePetOwner.Enemy)
    local enemyHealth = C_PetBattles.GetHealth(Enum.BattlePetOwner.Enemy, enemyActivePet)
    local enemyMaxHealth = C_PetBattles.GetMaxHealth(Enum.BattlePetOwner.Enemy, enemyActivePet)
    local enemyHealthPercent = (enemyHealth / enemyMaxHealth) * 100
    
    -- Priority 1: If very low health (<25%) and have other pets, try to swap
    if healthPercent < 25 then
        for i = 1, 3 do
            if i ~= activePet then
                local petHealth = C_PetBattles.GetHealth(Enum.BattlePetOwner.Ally, i)
                if petHealth > 0 then
                    C_PetBattles.ChangePet(i)
                    print("|cff00ff00PetWeaver:|r Low health, swapping out")
                    return
                end
            end
        end
    end
    
    -- Priority 2: Use first available ability
    for i = 1, 3 do
        local _, _, _, canUse = C_PetBattles.GetAbilityInfo(Enum.BattlePetOwner.Ally, activePet, i)
        if canUse then
            C_PetBattles.UseAbility(i)
            if PetWeaverDB.settings.showCoachMode then
                print("|cff00ff00PetWeaver:|r Using ability " .. i)
            end
            return
        end
    end
    
    print("|cff00ff00PetWeaver:|r No moves available")
end

-- Auto-load matching team for current encounter
function addon:AutoLoadTeam()
    local enemyName = C_PetBattles.GetName(Enum.BattlePetOwner.Enemy)
    if not enemyName then return end
    
    -- Find best matching team
    local foundTeam = nil
    for _, team in ipairs(PetWeaverDB.teams) do
        if team.enemyName == enemyName then
            foundTeam = team
            break
        end
    end
    
    if foundTeam then
        -- Load into new Battle Engine
        if addon.BattleEngine then
            addon.BattleEngine:StartBattle(foundTeam)
        end
        
        -- Keep legacy support
        addon.currentScript = foundTeam
        addon.currentRound = 0
        addon.scriptStep = 1
        print("|cff00ff00PetWeaver:|r Auto-loaded team: " .. (foundTeam.name or "Unnamed"))
        
        -- Auto-execute first move if enabled
        if PetWeaverDB.settings.autoBattle and addon.BattleEngine then
            C_Timer.After(0.5, function()
                addon.BattleEngine:ExecuteNextCommand()
            end)
        end
    else
        -- Check for generic teams
        for _, team in ipairs(PetWeaverDB.teams) do
            if not team.enemyName then -- Generic team
                if addon.BattleEngine then
                    addon.BattleEngine:StartBattle(team)
                end
                addon.currentScript = team
                addon.currentRound = 0
                addon.scriptStep = 1
                print("|cff00ff00PetWeaver:|r Using generic team: " .. (team.name or "Unnamed"))
                
                if PetWeaverDB.settings.autoBattle and addon.BattleEngine then
                    C_Timer.After(0.5, function()
                        addon.BattleEngine:ExecuteNextCommand()
                    end)
                end
                break
            end
        end
    end
end

-- Log battle outcome for statistics
function addon:LogBattleOutcome()
    local winner = C_PetBattles.GetBattleState()
    local enemyName = C_PetBattles.GetName(Enum.BattlePetOwner.Enemy)
    
    if not enemyName then return end
    
    local outcome = {
        enemyName = enemyName,
        won = (winner == Enum.BattlePetOwner.Ally),
        timestamp = time(),
        teamUsed = addon.currentScript and addon.currentScript.name or "None",
        rounds = addon.currentRound or 0
    }
    
    table.insert(PetWeaverDB.battleHistory, outcome)
    
    -- Keep only last 100 battles
    if #PetWeaverDB.battleHistory > 100 then
        table.remove(PetWeaverDB.battleHistory, 1)
    end
    
    if outcome.won then
        print("|cff00ff00PetWeaver:|r Victory! Logged to battle history")
    else
        print("|cff00ff00PetWeaver:|r Defeat. Logged to battle history")
    end
    
    -- Reset script tracking
    addon.currentScript = nil
    addon.currentRound = 0
    addon.scriptStep = 1
end

-- 4. Journal Replacement
function addon:HookPetJournal()
    if not PetJournal then return end
    
    -- Create our replacement UI parented to PetJournal
    local f = CreateFrame("Frame", "PetWeaverFrame", PetJournal)
    f:SetAllPoints(PetJournal)
    f:SetFrameLevel(PetJournal:GetFrameLevel() + 10)
    addon.Frame = f
    
    -- Background
    f.bg = f:CreateTexture(nil, "BACKGROUND")
    f.bg:SetAllPoints()
    f.bg:SetColorTexture(0.05, 0.05, 0.05, 0.95)
    
    -- Top Bar
    local topBar = CreateFrame("Frame", nil, f)
    topBar:SetSize(f:GetWidth(), 40)
    topBar:SetPoint("TOP", 0, -20)
    
    local title = topBar:CreateFontString(nil, "OVERLAY", "GameFontNormalHuge")
    title:SetPoint("LEFT", 20, 0)
    title:SetText("PetWeaver")
    title:SetTextColor(1, 0.82, 0)
    
    -- Tab Buttons
    local tabs = {"Teams", "Leveling", "Battles", "Collections"}
    local tabButtons = {}
    
    for i, tabName in ipairs(tabs) do
        local btn = CreateFrame("Button", nil, topBar, "UIPanelButtonTemplate")
        btn:SetSize(90, 30)
        btn:SetPoint("TOPLEFT", 120 + (i-1)*95, -5)
        btn:SetText(tabName)
        btn.tabName = tabName
        
        btn:SetScript("OnClick", function(self)
            addon:ShowTab(self.tabName)
            for _, b in pairs(tabButtons) do
                b:UnlockHighlight()
            end
            self:LockHighlight()
        end)
        
        tabButtons[tabName] = btn
    end
    
    -- Content Frame (ScrollFrame)
    local scrollFrame = CreateFrame("ScrollFrame", nil, f, "UIPanelScrollFrameTemplate")
    scrollFrame:SetPoint("TOPLEFT", 10, -70)
    scrollFrame:SetPoint("BOTTOMRIGHT", -30, 40)
    
    local scrollChild = CreateFrame("Frame", nil, scrollFrame)
    scrollChild:SetSize(600, 800)
    scrollFrame:SetScrollChild(scrollChild)
    
    addon.ScrollChild = scrollChild
    addon.TabButtons = tabButtons
    
    -- Toggle Button (Top-Right Corner)
    local toggleBtn = CreateFrame("CheckButton", nil, f, "UICheckButtonTemplate")
    toggleBtn:SetSize(24, 24)
    toggleBtn:SetPoint("TOPRIGHT", -40, -25)
    toggleBtn:SetChecked(true)
    toggleBtn:SetFrameLevel(f:GetFrameLevel() + 20) -- Above everything
    
    toggleBtn.text = toggleBtn:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    toggleBtn.text:SetPoint("RIGHT", toggleBtn, "LEFT", -5, 0)
    toggleBtn.text:SetText("PetWeaver")
    
    toggleBtn:SetScript("OnClick", function(self)
        if self:GetChecked() then
            f:Show()
        else
            f:Hide()
        end
    end)
    
    -- Show Teams tab by default
    addon:ShowTab("Teams")
    tabButtons["Teams"]:LockHighlight()
    
    print("|cff00ff00PetWeaver:|r Journal Replaced.")
end

-- 4. Tab Rendering
function addon:ShowTab(tabName)
    if not addon.ScrollChild then return end
    
    -- Clear current content
    for _, child in pairs({addon.ScrollChild:GetChildren()}) do
        child:Hide()
    end
    
    if tabName == "Teams" then
        addon:RenderTeams()
    elseif tabName == "Leveling" then
        addon:RenderLeveling()
    elseif tabName == "Battles" then
        addon:RenderBattles()
    elseif tabName == "Collections" then
        addon:RenderCollections()
    end
end

function addon:RenderTeams()
    local y = -10
    
    -- New Team Button
    local newTeamBtn = CreateFrame("Button", nil, addon.ScrollChild, "UIPanelButtonTemplate")
    newTeamBtn:SetSize(200, 30)
    newTeamBtn:SetPoint("TOPLEFT", 10, y)
    newTeamBtn:SetText("+ New Team")
    newTeamBtn:SetScript("OnClick", function()
        -- Create empty team for now
        table.insert(PetWeaverDB.teams, {
            name = "Team " .. (#PetWeaverDB.teams + 1),
            pets = {},
            enemyName = nil
        })
        print("|cff00ff00PetWeaver:|r Created new team")
        addon:RenderTeams()
    end)
    y = y - 50
    
    -- Teams List Header
    local header = addon.ScrollChild:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    header:SetPoint("TOPLEFT", 10, y)
    header:SetText("Saved Teams (" .. #PetWeaverDB.teams .. ")")
    y = y - 35
    
    if #PetWeaverDB.teams == 0 then
        local noTeams = addon.ScrollChild:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
        noTeams:SetPoint("TOPLEFT", 20, y)
        noTeams:SetText("No teams saved yet.\nClick '+ New Team' to create one.")
    else
        for i, team in ipairs(PetWeaverDB.teams) do
            local teamFrame = CreateFrame("Frame", nil, addon.ScrollChild, "BackdropTemplate")
            teamFrame:SetSize(550, 85)
            teamFrame:SetPoint("TOPLEFT", 10, y)
            teamFrame:SetBackdrop({
                bgFile = "Interface\\Buttons\\WHITE8X8",
                edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
                tile = false, edgeSize = 12,
                insets = { left = 2, right = 2, top = 2, bottom = 2 }
            })
            teamFrame:SetBackdropColor(0.1, 0.1, 0.1, 0.9)
            teamFrame:SetBackdropBorderColor(0.4, 0.35, 0.2, 1)
            
            -- Team Name
            local teamName = teamFrame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
            teamName:SetPoint("TOPLEFT", 10, -8)
            teamName:SetText(team.name or "Unnamed Team")
            teamName:SetTextColor(1, 0.82, 0)
            
            -- Delete Button
            local deleteBtn = CreateFrame("Button", nil, teamFrame, "UIPanelButtonTemplate")
            deleteBtn:SetSize(60, 20)
            deleteBtn:SetPoint("TOPRIGHT", -10, -8)
            deleteBtn:SetText("Delete")
            deleteBtn:SetScript("OnClick", function()
                table.remove(PetWeaverDB.teams, i)
                addon:RenderTeams()
            end)
            
            -- Pet Portraits (Rematch Style)
            local petY = -35
            if team.pets and #team.pets > 0 then
                for p = 1, math.min(3, #team.pets) do
                    local pet = team.pets[p]
                    if pet and pet.speciesID then
                        -- Pet Portrait Frame
                        local petFrame = CreateFrame("Frame", nil, teamFrame, "BackdropTemplate")
                        petFrame:SetSize(55, 55)
                        petFrame:SetPoint("TOPLEFT", 10 + (p-1)*60, petY)
                        petFrame:SetBackdrop({
                            bgFile = "Interface\\Buttons\\WHITE8X8",
                            edgeFile = "Interface\\Buttons\\WHITE8X8",
                            tile = false, edgeSize = 1,
                            insets = { left = 1, right = 1, top = 1, bottom = 1 }
                        })
                        petFrame:SetBackdropColor(0, 0, 0, 1)
                        petFrame:SetBackdropBorderColor(0.5, 0.5, 0.5, 1)
                        
                        -- Pet Icon
                        local icon = petFrame:CreateTexture(nil, "ARTWORK")
                        icon:SetPoint("TOPLEFT", 2, -2)
                        icon:SetPoint("BOTTOMRIGHT", -2, 2)
                        
                        local _, petIcon = C_PetJournal.GetPetInfoBySpeciesID(pet.speciesID)
                        if petIcon then
                            icon:SetTexture(petIcon)
                        else
                            icon:SetColorTexture(0.2, 0.2, 0.2, 1)
                        end
                        
                        -- Level Badge
                        if pet.level then
                            local levelText = petFrame:CreateFontString(nil, "OVERLAY", "NumberFontNormalSmall")
                            levelText:SetPoint("BOTTOMRIGHT", -2, 2)
                            levelText:SetText(pet.level)
                            levelText:SetTextColor(1, 1, 1)
                        end
                    end
                end
            else
                -- Empty slots
                for p = 1, 3 do
                    local emptyFrame = CreateFrame("Frame", nil, teamFrame, "BackdropTemplate")
                    emptyFrame:SetSize(55, 55)
                    emptyFrame:SetPoint("TOPLEFT", 10 + (p-1)*60, petY)
                    emptyFrame:SetBackdrop({
                        bgFile = "Interface\\Buttons\\WHITE8X8",
                        edgeFile = "Interface\\Buttons\\WHITE8X8",
                        tile = false, edgeSize = 1,
                        insets = { left = 1, right = 1, top = 1, bottom = 1 }
                    })
                    emptyFrame:SetBackdropColor(0.05, 0.05, 0.05, 0.8)
                    emptyFrame:SetBackdropBorderColor(0.3, 0.3, 0.3, 1)
                    
                    local plusText = emptyFrame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
                    plusText:SetPoint("CENTER")
                    plusText:SetText("+")
                    plusText:SetTextColor(0.5, 0.5, 0.5)
                end
            end
            
            y = y - 95
        end
    end
    
    addon.ScrollChild:SetHeight(math.abs(y) + 100)
end

function addon:RenderLeveling()
    local y = -10
    
    -- Initialize leveling queue if needed
    PetWeaverDB.levelingQueue = PetWeaverDB.levelingQueue or {}
    
    local header = addon.ScrollChild:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    header:SetPoint("TOPLEFT", 10, y)
    header:SetText("Leveling Queue (" .. #PetWeaverDB.levelingQueue .. " pets)")
    y = y - 35
    
    -- Add Pet Button
    local addBtn = CreateFrame("Button", nil, addon.ScrollChild, "UIPanelButtonTemplate")
    addBtn:SetSize(180, 30)
    addBtn:SetPoint("TOPLEFT", 10, y)
    addBtn:SetText("+ Add Pet to Queue")
    addBtn:SetScript("OnClick", function()
        -- Get first pet under level 25
        local numPets = C_PetJournal.GetNumPets()
        for i = 1, numPets do
            local petID, speciesID, owned, customName, level = C_PetJournal.GetPetInfoByIndex(i)
            if petID and level < 25 then
                -- Check if not already in queue
                local found = false
                for _, queuedID in ipairs(PetWeaverDB.levelingQueue) do
                    if queuedID == petID then
                        found = true
                        break
                    end
                end
                
                if not found then
                    table.insert(PetWeaverDB.levelingQueue, petID)
                    addon:RenderLeveling()
                    return
                end
            end
        end
        print("|cff00ff00PetWeaver:|r No eligible pets found (all max level or already queued)")
    end)
    y = y - 50
    
    -- Clear Queue Button
    local clearBtn = CreateFrame("Button", nil, addon.ScrollChild, "UIPanelButtonTemplate")
    clearBtn:SetSize(120, 25)
    clearBtn:SetPoint("TOPLEFT", 200, y + 25)
    clearBtn:SetText("Clear Queue")
    clearBtn:SetScript("OnClick", function()
        wipe(PetWeaverDB.levelingQueue)
        addon:RenderLeveling()
    end)
    
    if #PetWeaverDB.levelingQueue == 0 then
        local empty = addon.ScrollChild:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
        empty:SetPoint("TOPLEFT", 20, y)
        empty:SetText("Queue is empty.\nAdd pets under level 25 to level them up in battles.")
    else
        -- Display queued pets
        for i, petID in ipairs(PetWeaverDB.levelingQueue) do
            local _, customName, level, _, _, _, _, petName, petIcon = C_PetJournal.GetPetInfoByPetID(petID)
            
            if petID then
                local petFrame = CreateFrame("Frame", nil, addon.ScrollChild, "BackdropTemplate")
                petFrame:SetSize(550, 50)
                petFrame:SetPoint("TOPLEFT", 10, y)
                petFrame:SetBackdrop({
                    bgFile = "Interface\\Buttons\\WHITE8X8",
                    edgeFile = "Interface\\Buttons\\WHITE8X8",
                    tile = false, edgeSize = 1,
                    insets = { left = 1, right = 1, top = 1, bottom = 1 }
                })
                petFrame:SetBackdropColor(0.1, 0.1, 0.1, 0.8)
                petFrame:SetBackdropBorderColor(0.3, 0.3, 0.3, 1)
                
                -- Pet Icon
                local icon = petFrame:CreateTexture(nil, "ARTWORK")
                icon:SetSize(40, 40)
                icon:SetPoint("LEFT", 5, 0)
                if petIcon then
                    icon:SetTexture(petIcon)
                else
                    icon:SetColorTexture(0.2, 0.2, 0.2, 1)
                end
                
                -- Pet Name
                local name = petFrame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
                name:SetPoint("LEFT", icon, "RIGHT", 10, 5)
                name:SetText((customName or petName or "Unknown Pet"))
                
                -- Level
                local lvl = petFrame:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
                lvl:SetPoint("LEFT", icon, "RIGHT", 10, -10)
                lvl:SetText("Level " .. (level or 1))
                lvl:SetTextColor(0.5, 1, 0.5)
                
                -- Queue Position
                local pos = petFrame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
                pos:SetPoint("LEFT", 300, 0)
                pos:SetText("#" .. i)
                pos:SetTextColor(1, 0.82, 0)
                
                -- Remove Button
                local removeBtn = CreateFrame("Button", nil, petFrame, "UIPanelButtonTemplate")
                removeBtn:SetSize(70, 25)
                removeBtn:SetPoint("RIGHT", -10, 0)
                removeBtn:SetText("Remove")
                removeBtn:SetScript("OnClick", function()
                    table.remove(PetWeaverDB.levelingQueue, i)
                    addon:RenderLeveling()
                end)
                
                y = y - 55
            end
        end
    end
    
    addon.ScrollChild:SetHeight(math.abs(y) + 100)
end

function addon:RenderBattles()
    local y = -10
    
    local header = addon.ScrollChild:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    header:SetPoint("TOPLEFT", 10, y)
    header:SetText("Battle History (" .. #PetWeaverDB.battleHistory .. " battles)")
    y = y - 35
    
    -- Stats Summary
    local wins = 0
    local losses = 0
    for _, battle in ipairs(PetWeaverDB.battleHistory) do
        if battle.won then
            wins = wins + 1
        else
            losses = losses + 1
        end
    end
    
    if #PetWeaverDB.battleHistory > 0 then
        local winRate = string.format("%.1f", (wins / #PetWeaverDB.battleHistory) * 100)
        
        local statsBox = CreateFrame("Frame", nil, addon.ScrollChild, "BackdropTemplate")
        statsBox:SetSize(550, 60)
        statsBox:SetPoint("TOPLEFT", 10, y)
        statsBox:SetBackdrop({
            bgFile = "Interface\\Buttons\\WHITE8X8",
            edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
            tile = false, edgeSize = 12,
            insets = { left = 2, right = 2, top = 2, bottom = 2 }
        })
        statsBox:SetBackdropColor(0.1, 0.1, 0.1, 0.9)
        statsBox:SetBackdropBorderColor(0.4, 0.35, 0.2, 1)
        
        local statsText = statsBox:CreateFontString(nil, "OVERLAY", "GameFontNormal")
        statsText:SetPoint("LEFT", 15, 0)
        statsText:SetText(string.format("Wins: |cff00ff00%d|r  |  Losses: |cffff0000%d|r  |  Win Rate: |cffffd700%s%%|r", wins, losses, winRate))
        
        y = y - 75
    end
    
    -- Clear History Button
    local clearBtn = CreateFrame("Button", nil, addon.ScrollChild, "UIPanelButtonTemplate")
    clearBtn:SetSize(120, 25)
    clearBtn:SetPoint("TOPRIGHT", addon.ScrollChild, "TOPRIGHT", -10, -10)
    clearBtn:SetText("Clear History")
    clearBtn:SetScript("OnClick", function()
        wipe(PetWeaverDB.battleHistory)
        addon:RenderBattles()
    end)
    
    if #PetWeaverDB.battleHistory == 0 then
        local empty = addon.ScrollChild:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
        empty:SetPoint("TOPLEFT", 20, y)
        empty:SetText("No battles recorded yet.\nComplete pet battles to see your history here.")
    else
        -- Show recent battles (last 20)
        local recentBattles = {}
        for i = math.max(1, #PetWeaverDB.battleHistory - 19), #PetWeaverDB.battleHistory do
            table.insert(recentBattles, 1, PetWeaverDB.battleHistory[i])
        end
        
        for i, battle in ipairs(recentBattles) do
            local battleFrame = CreateFrame("Frame", nil, addon.ScrollChild, "BackdropTemplate")
            battleFrame:SetSize(550, 45)
            battleFrame:SetPoint("TOPLEFT", 10, y)
            battleFrame:SetBackdrop({
                bgFile = "Interface\\Buttons\\WHITE8X8",
                edgeFile = "Interface\\Buttons\\WHITE8X8",
                tile = false, edgeSize = 1,
                insets = { left = 1, right = 1, top = 1, bottom = 1 }
            })
            
            if battle.won then
                battleFrame:SetBackdropColor(0, 0.15, 0, 0.8)
                battleFrame:SetBackdropBorderColor(0, 0.5, 0, 1)
            else
                battleFrame:SetBackdropColor(0.15, 0, 0, 0.8)
                battleFrame:SetBackdropBorderColor(0.5, 0, 0, 1)
            end
            
            -- Enemy Name
            local enemyText = battleFrame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
            enemyText:SetPoint("LEFT", 10, 8)
            enemyText:SetText((battle.won and "|cff00ff00Victory|r" or "|cffff0000Defeat|r") .. " vs " .. battle.enemyName)
            
            -- Team Used
            local teamText = battleFrame:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
            teamText:SetPoint("LEFT", 10, -8)
            teamText:SetText("Team: " .. (battle.teamUsed or "None"))
            teamText:SetTextColor(0.7, 0.7, 0.7)
            
            -- Rounds
            local rounds = battleFrame:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
            rounds:SetPoint("RIGHT", -10, 0)
            rounds:SetText(battle.rounds .. " rounds")
            rounds:SetTextColor(0.5, 0.5, 0.5)
            
            y = y - 50
        end
    end
    
    addon.ScrollChild:SetHeight(math.abs(y) + 100)
end

function addon:RenderCollections()
    local y = -10
    
    local header = addon.ScrollChild:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    header:SetPoint("TOPLEFT", 10, y)
    header:SetText("Encounter Database")
    y = y - 35
    
    local encounterCount = 0
    for _ in pairs(PetWeaverDB.encounterDatabase) do
        encounterCount = encounterCount + 1
    end
    
    local subheader = addon.ScrollChild:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    subheader:SetPoint("TOPLEFT", 10, y)
    subheader:SetText(encounterCount .. " encounters available")
    subheader:SetTextColor(0.7, 0.7, 0.7)
    y = y - 35
    
    -- Category filter buttons (could expand later)
    local categories = {"all", "daily", "family_familiar", "world_quest"}
    local selectedCategory = "all"
    
    if encounterCount == 0 then
        local empty = addon.ScrollChild:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
        empty:SetPoint("TOPLEFT", 20, y)
        empty:SetText("No encounters in database.\\nEncounters will be loaded from data files.")
    else
        -- Display encounters
        for encounterName, encounter in pairs(PetWeaverDB.encounterDatabase) do
            local encounterFrame = CreateFrame("Frame", nil, addon.ScrollChild, "BackdropTemplate")
            encounterFrame:SetSize(550, 80)
            encounterFrame:SetPoint("TOPLEFT", 10, y)
            encounterFrame:SetBackdrop({
                bgFile = "Interface\\Buttons\\WHITE8X8",
                edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
                tile = false, edgeSize = 12,
                insets = { left = 2, right = 2, top = 2, bottom = 2 }
            })
            encounterFrame:SetBackdropColor(0.1, 0.1, 0.1, 0.9)
            encounterFrame:SetBackdropBorderColor(0.4, 0.35, 0.2, 1)
            
            -- Encounter Name
            local nameText = encounterFrame:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
            nameText:SetPoint("TOPLEFT", 10, -8)
            nameText:SetText(encounter.displayName or encounterName)
            nameText:SetTextColor(1, 0.82, 0)
            
            -- Zone and Category
            local infoText = encounterFrame:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
            infoText:SetPoint("TOPLEFT", 10, -28)
            infoText:SetText(string.format("%s  |  %s  |  Level %d", 
                encounter.zone or "Unknown", 
                encounter.category or "unknown",
                encounter.recommendedLevel or 25))
            infoText:SetTextColor(0.7, 0.7, 0.7)
            
            -- Pet count
            local petCount = encounterFrame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
            petCount:SetPoint("TOPLEFT", 10, -48)
            petCount:SetText((encounter.pets and #encounter.pets or 0) .. " enemy pets")
            
            -- Difficulty indicator
            local difficultyColors = {
                easy = {0, 1, 0},
                medium = {1, 0.82, 0},
                hard = {1, 0, 0}
            }
            local diffColor = difficultyColors[encounter.difficulty] or {0.5, 0.5, 0.5}
            
            local difficulty = encounterFrame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
            difficulty:SetPoint("TOPRIGHT", -10, -28)
            difficulty:SetText(string.upper(encounter.difficulty or "Unknown"))
            difficulty:SetTextColor(diffColor[1], diffColor[2], diffColor[3])
            
            y = y - 90
        end
    end
    
    addon.ScrollChild:SetHeight(math.abs(y) + 100)
end

-- 5. Slash Commands
SLASH_PETWEAVER1 = "/pw"
SlashCmdList["PETWEAVER"] = function(msg)
    if addon.Frame then
        if addon.Frame:IsShown() then
            addon.Frame:Hide()
        else
            addon.Frame:Show()
        end
    end
end

-- Auto Battle command (for keybinding)
SLASH_PWAUTOBATTLE1 = "/pwab"
SlashCmdList["PWAUTOBATTLE"] = function(msg)
    addon:ExecuteAutoBattleMove()
end

print("|cff00ff00PetWeaver:|r Loaded. Use /pw to toggle, /pwab for auto battle.")
