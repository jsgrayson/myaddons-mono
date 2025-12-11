local addonName, addonTable = ...

-- ============================================================================
-- Data & State
-- ============================================================================
addonTable.petScripts = {}
addonTable.savedTeams = {}
addonTable.levelingQueue = {} -- NEW: Stores the list of pets to level
addonTable.petList = {}

tinsert(addonTable.savedTeams, {name="Starter Team", pets={nil, nil, nil}, icon="Interface\\Icons\\inv_misc_questionmark"})

local selectedID = nil
local currentTab = 1 -- 1=Pets, 2=Teams, 3=Queue
local currentSearch = ""

-- ============================================================================
-- Helpers
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

    local loadoutFrame = PetweaverJournalFrame.RightInset.TeamLoadout
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
    local frame = PetweaverJournalFrame.RightInset.SelectedPetDetails
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
    wipe(addonTable.petList)
    local _, numOwned = C_PetJournal.GetNumPets()
    local searchLower = string.lower(currentSearch)

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
    local scrollFrame = PetweaverJournalFrame.LeftInset.ListScrollFrame
    local buttons = scrollFrame.buttons
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
    PanelTemplates_SetTab(PetweaverJournalFrame, id)
    selectedID = nil
    currentSearch = ""
    PetweaverJournalFrame.LeftInset.FilterHeader.SearchBox:SetText("")
    UpdatePetData()
end

-- ============================================================================
-- INIT
-- ============================================================================

local function OnEvent(self, event, ...)
    if event == "PLAYER_LOGIN" then
        if PetweaverJournalFrameTitleText then PetweaverJournalFrameTitleText:SetText("Petweaver Journal"); end

        PetweaverJournalFrame.PetsTab:SetScript("OnClick", function() SetTab(1) end)
        PetweaverJournalFrame.TeamsTab:SetScript("OnClick", function() SetTab(2) end)
        PetweaverJournalFrame.QueueTab:SetScript("OnClick", function() SetTab(3) end) -- NEW TAB
        
        PanelTemplates_SetNumTabs(PetweaverJournalFrame, 3); -- UPDATED COUNT
        SetTab(1)

        local searchBox = PetweaverJournalFrame.LeftInset.FilterHeader.SearchBox
        searchBox:SetScript("OnTextChanged", function(self)
            currentSearch = self:GetText()
            UpdatePetData()
        end)

        local scrollFrame = PetweaverJournalFrame.LeftInset.ListScrollFrame
        HybridScrollFrame_CreateButtons(scrollFrame, "PetweaverListButtonTemplate")
        scrollFrame.update = PetweaverList_Update
        
        if PetweaverJournalFrame.RightInset.TeamLoadout.SaveTeamButton then
             PetweaverJournalFrame.RightInset.TeamLoadout.SaveTeamButton:SetScript("OnClick", SaveActiveTeam)
        end

        UpdatePetData()
        UpdateTeamSlots()

    elseif event == "PET_JOURNAL_LIST_UPDATE" then
        UpdatePetData()
    end
end

local eventFrame = CreateFrame("Frame")
eventFrame:RegisterEvent("PLAYER_LOGIN")
eventFrame:RegisterEvent("PET_JOURNAL_LIST_UPDATE")
eventFrame:SetScript("OnEvent", OnEvent)

SLASH_PETWEAVER1 = "/petweaver"
SlashCmdList["PETWEAVER"] = function(msg)
    if PetweaverJournalFrame:IsShown() then PetweaverJournalFrame:Hide() else PetweaverJournalFrame:Show() end
end
