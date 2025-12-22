local addonName, addon = ...
PetWeaverMixin = {}

function PetWeaverMixin:OnLoad()
    PetWeaverDBManager:Init()

    -- UI Setup
    self:RegisterForDrag("LeftButton")
    SetPortraitToTexture(self.portrait, "Interface\\Icons\\Inv_Pet_BattlePetTraining")
    self.TitleText:SetText("PetWeaver Grimoire")
    
    -- Scroll List Init
    self.ListInset.ScrollFrame.update = function() self:UpdateScroll() end
    HybridScrollFrame_CreateButtons(self.ListInset.ScrollFrame, "PetWeaverListButtonTemplate", 0, 0)

    -- Events
    self:RegisterEvent("PET_JOURNAL_LIST_UPDATE")
    self:RegisterEvent("PLAYER_TARGET_CHANGED")
    self:RegisterEvent("PET_BATTLE_OPENING_START")
    self:RegisterEvent("PET_BATTLE_CLOSE")
    self:RegisterEvent("PET_BATTLE_TURN_STARTED")

    -- Init Sub-Systems
    self:InitScanner()
    self:SetTab(1) -- Default to Journal
    self:UpdateScroll()
end

function PetWeaverMixin:OnEvent(event, ...)
    if event == "PET_JOURNAL_LIST_UPDATE" then
        self:UpdateScroll()
    elseif event == "PLAYER_TARGET_CHANGED" then
        self:CheckTargetForStrategy()
    elseif event == "PET_BATTLE_OPENING_START" then
        PetWeaverCombatHUD:Show()
        -- Load script into engine automatically
        if self.currentTargetScript then
             self.currentActiveScript = self.currentTargetScript
             PetWeaverCombatHUD.PredictionText:SetText("Strategy Loaded.")
        else
             self.currentActiveScript = nil
             PetWeaverCombatHUD.PredictionText:SetText("No Auto-Script.")
        end
    elseif event == "PET_BATTLE_CLOSE" then
        PetWeaverCombatHUD:Hide()
    elseif event == "PET_BATTLE_TURN_STARTED" then
        local petOwner = ... -- 1 = Ally, 2 = Enemy
        PetWeaverCombatHUD.ExecuteBtn:SetEnabled(petOwner == 1)
    end
end

-- [TAB NAVIGATION]
function PetWeaverMixin:SetTab(id)
    self.ListInset:Hide()
    self.DetailInset:Hide()
    self.TeamFrame:Hide()
    self.ScriptFrame:Hide()
    
    if id == 1 then -- Journal
        self.ListInset:Show(); self.DetailInset:Show()
    elseif id == 2 then -- War Room (Teams)
        self.TeamFrame:Show(); self:UpdateTeamView()
    elseif id == 3 then -- Scribe (Scripts)
        self.ScriptFrame:Show()
    end
end

-- [JOURNAL SCROLL & SELECTION]
function PetWeaverMixin:UpdateScroll()
    local scrollFrame = self.ListInset.ScrollFrame
    local buttons = scrollFrame.buttons
    local offset = HybridScrollFrame_GetOffset(scrollFrame)
    local numPets = C_PetJournal.GetNumPets() 
    
    for i = 1, #buttons do
        local button = buttons[i]
        local index = offset + i
        if index <= numPets then
            self:UpdateListItem(button, index)
            button:Show()
        else
            button:Hide()
        end
    end
    HybridScrollFrame_Update(scrollFrame, numPets * 46, scrollFrame:GetHeight())
end

function PetWeaverMixin:UpdateListItem(button, index)
    local petID, speciesID, owned, customName, level, _, _, speciesName, icon = C_PetJournal.GetPetInfoByIndex(index)
    if not speciesID then return end
    button.Name:SetText(customName or speciesName)
    button.Icon:SetTexture(icon)
    button.petID = petID; button.speciesID = speciesID; button.index = index
    button.Level:SetText(owned and "Lvl " .. level or "Uncollected")
    button.Icon:SetDesaturated(not owned)
    
    -- Rarity Border
    local _, _, _, _, rarity = C_PetJournal.GetPetStats(petID)
    button.RarityBorder:SetShown(owned and rarity and rarity >= 3)
    if rarity == 3 then button.RarityBorder:SetVertexColor(0,0.44,0.87) -- Rare
    elseif rarity == 4 then button.RarityBorder:SetVertexColor(0.64,0.21,0.93) end -- Epic
end

function PetWeaverMixin:SelectPet(index)
    local petID, speciesID, owned, customName, _, _, _, speciesName = C_PetJournal.GetPetInfoByIndex(index)
    self.selectedPetID = petID
    local _, _, _, _, _, _, _, _, _, _, _, displayID = C_PetJournal.GetPetInfoBySpeciesID(speciesID)
    if displayID then self.DetailInset.Model:SetDisplayInfo(displayID) else self.DetailInset.Model:ClearModel() end
    self.DetailInset.SummonButton:SetEnabled(owned and petID)
end

-- [WAR ROOM: TEAMS & STRATEGIES]
function PetWeaverMixin:UpdateTeamView()
    local targetName = UnitName("target") or "No Target"
    self.TeamFrame.TargetName:SetText("Strategy Target: " .. targetName)
    
    -- Update 3D Models of current loadout
    for i=1,3 do
        local petID = C_PetJournal.GetPetLoadOutInfo(i)
        if petID then
            local speciesID, _, _, _, _, _, _, _, _, _, _, displayID = C_PetJournal.GetPetInfoByPetID(petID)
            self.TeamFrame["Pet"..i.."Model"]:SetDisplayInfo(displayID)
        else
            self.TeamFrame["Pet"..i.."Model"]:ClearModel()
        end
    end
end

function PetWeaverMixin:SaveCurrentTeam()
    local targetName = UnitName("target")
    if not targetName then print("Select a target first."); return end
    
    local team = {}
    for i=1, 3 do team[i] = C_PetJournal.GetPetLoadOutInfo(i) end
    local script = self.ScriptFrame.Editor.EditBox:GetText()
    
    PetWeaverDBManager:SaveStrategy(targetName, team, script)
end

function PetWeaverMixin:CheckTargetForStrategy()
    local targetName = UnitName("target")
    if not targetName then return end
    
    -- 1. Check User Local DB (SavedVariables)
    local userStrategy = PetWeaverDBManager:GetStrategy(targetName)
    if userStrategy then
        print("|cff00ff00PetWeaver:|r User Strategy found for " .. targetName .. ". Auto-loading...")
        self:LoadStrategy(userStrategy)
    else
        -- 2. Check STATIC OFFLINE DB (World Data)
        -- Need to find the NPC ID from the GUID
        local guid = UnitGUID("target")
        if guid then
             local type, _, _, _, _, npcID = strsplit("-", guid)
             if type == "Creature" or type == "Pet" then
                 npcID = tonumber(npcID)
                 local staticStrats = addon.Data.Strategies[npcID]
                 if staticStrats then
                     print("|cff0070ddPetWeaver:|r Official Strategy found for " .. targetName .. " ("..npcID..").")
                     self:LoadStrategy(staticStrats[1]) -- Load primary generic strategy
                     userStrategy = staticStrats[1] -- Flag as found
                 end
             end
        end
        
        if not userStrategy then
            self.currentTargetScript = nil
        end
    end

    if self.TeamFrame:IsShown() then self:UpdateTeamView() end
end

function PetWeaverMixin:LoadStrategy(strategy)
    for i, petGUID in ipairs(strategy.pets) do
        -- Check if it's a leveling slot placeholder (using a fake GUID convention for now)
        if petGUID == "LEVELING_SLOT" then
             local levelingPet = PetWeaverDBManager:GetTopLevelingPet()
             if levelingPet then C_PetJournal.SetPetLoadOutInfo(i, levelingPet) end
        else
             C_PetJournal.SetPetLoadOutInfo(i, petGUID)
        end
    end
    -- Load script into editor and buffer for combat
    self.ScriptFrame.Editor.EditBox:SetText(strategy.script)
    self.currentTargetScript = strategy.script
end

-- [COMBAT SCRIPT ENGINE (The "11")]
function PetWeaverMixin:ExecuteNextMove()
    if not C_PetBattles.IsInBattle() or not self.currentActiveScript then return end

    -- The Sandbox Environment
    local env = {
        print = print, tonumber = tonumber, math = math,
        ally = { hp = C_PetBattles.GetHealth(1, C_PetBattles.GetActivePet(1)), speed = C_PetBattles.GetSpeed(1, C_PetBattles.GetActivePet(1)) },
        enemy = { hp = C_PetBattles.GetHealth(2, C_PetBattles.GetActivePet(2)) },
        use = function(slot) C_PetBattles.UseAbility(slot) end,
        swap = function(slot) C_PetBattles.ChangePet(slot) end,
        pass = function() C_PetBattles.SkipTurn() end
    }
    
    local func, err = loadstring(self.currentActiveScript)
    if func then
        setfenv(func, env)
        local success, runtimeErr = pcall(func)
        if not success then print("|cffff0000Script Error:|r " .. runtimeErr) end
    else
        print("|cffff0000Compile Error:|r " .. err)
    end
end

-- [WISHLIST SCANNER]
function PetWeaverMixin:InitScanner()
    -- Only load if TooltipDataProcessor exists (10.0+ API)
    if TooltipDataProcessor and TooltipDataProcessor.AddTooltipPostCall then
        TooltipDataProcessor.AddTooltipPostCall(Enum.TooltipDataType.Unit, function(tooltip)
            local _, unit = tooltip:GetUnit()
            if unit and UnitIsWildBattlePet(unit) then
                local speciesID = C_PetJournal.GetPetInfoByUnit(unit)
                if speciesID and PetWeaverDBManager:IsOnWishlist(speciesID) then
                     -- Using standard icon fallback since gen failed
                     tooltip:AddLine("|TInterface\\Icons\\Ability_Hunter_SniperShot:16|t |cffff0000WISHLIST PET DETECTED!|r")
                     tooltip:Show()
                end
            end
        end)
    end
end

-- [CONTEXT MENU]
function PetWeaverMixin:OpenPetMenu(button, petID, speciesID)
    local menu = {
        { text = "Pet Options", isTitle = true, notCheckable = true },
        { text = "Add to Leveling Queue", func = function() PetWeaverDBManager:EnqueuePet(petID) end, notCheckable = true },
        { text = PetWeaverDBManager:IsOnWishlist(speciesID) and "Remove from Wishlist" or "Add to Wishlist", func = function() PetWeaverDBManager:ToggleWishlist(speciesID) end, notCheckable = true },
        { text = "Summon", func = function() C_PetJournal.SummonPetByGUID(petID) end, notCheckable = true },
        { text = "Cancel", notCheckable = true, func = function() end }
    }
    if not PetWeaver_ContextMenu then PetWeaver_ContextMenu = CreateFrame("Frame", "PetWeaver_ContextMenu", UIParent, "UIDropDownMenuTemplate") end
    EasyMenu(menu, PetWeaver_ContextMenu, "cursor", 0, 0, "MENU")
end
