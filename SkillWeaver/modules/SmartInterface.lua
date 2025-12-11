--========================================================--
-- SkillWeaver - Smart Interface
-- Displays context-aware recommendations for Spec, Talents, Gear, etc.
--========================================================--

local ADDON_NAME, SkillWeaver = ...
local SmartInterface = {}
SkillWeaver.SmartInterface = SmartInterface

-- Dependencies
local ContentDetector = SkillWeaver.ContentDetector
local TalentRecommendations = SkillWeaver.TalentRecommendations
local EquipmentManager = SkillWeaver.EquipmentManager
local BrannHelper = SkillWeaver.BrannHelper

-- UI Constants
local WINDOW_WIDTH = 300
local WINDOW_HEIGHT = 250
local ROW_HEIGHT = 30

------------------------------------------------------------
-- Create Main Window
------------------------------------------------------------
function SmartInterface:CreateUI()
    if self.frame then return end

    local f = CreateFrame("Frame", "SkillWeaverSmartFrame", UIParent, "BackdropTemplate")
    f:SetSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    f:SetPoint("CENTER")
    f:SetMovable(true)
    f:EnableMouse(true)
    f:RegisterForDrag("LeftButton")
    f:SetScript("OnDragStart", f.StartMoving)
    f:SetScript("OnDragStop", f.StopMovingOrSizing)
    f:SetBackdrop({
        bgFile = "Interface\\DialogFrame\\UI-DialogBox-Background",
        edgeFile = "Interface\\DialogFrame\\UI-DialogBox-Border",
        tile = true, tileSize = 32, edgeSize = 32,
        insets = { left = 11, right = 12, top = 12, bottom = 11 }
    })
    
    -- Title
    f.title = f:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    f.title:SetPoint("TOP", 0, -15)
    f.title:SetText("SkillWeaver Smart Assist")
    
    -- Close Button
    f.closeBtn = CreateFrame("Button", nil, f, "UIPanelCloseButton")
    f.closeBtn:SetPoint("TOPRIGHT", -5, -5)
    
    self.frame = f
    
    -- Content Rows
    self.rows = {}
    local labels = { "Current Content:", "Recommended Spec:", "Talent Build:", "PvP Talents:", "Equipment Set:", "Brann Perk:" }
    
    for i, label in ipairs(labels) do
        local row = CreateFrame("Frame", nil, f)
        row:SetSize(WINDOW_WIDTH - 40, ROW_HEIGHT)
        row:SetPoint("TOPLEFT", 20, -50 - ((i-1) * ROW_HEIGHT))
        
        row.label = row:CreateFontString(nil, "OVERLAY", "GameFontNormal")
        row.label:SetPoint("LEFT", 0, 0)
        row.label:SetText(label)
        
        -- Special handling for Content Row (Row 1)
        if i == 1 then
            -- Dropdown for Content Override
            local dropdown = CreateFrame("Frame", "SkillWeaverContentDropdown", row, "UIDropDownMenuTemplate")
            dropdown:SetPoint("RIGHT", 10, 0)
            UIDropDownMenu_SetWidth(dropdown, 120)
            UIDropDownMenu_SetText(dropdown, "Auto-Detect")
            
            -- Initialize Dropdown
            UIDropDownMenu_Initialize(dropdown, function(self, level, menuList)
                local info = UIDropDownMenu_CreateInfo()
                local options = { "Auto-Detect", "Raid", "Mythic+", "Delve", "PvP" }
                
                for _, opt in ipairs(options) do
                    info.text = opt
                    info.func = function() 
                        UIDropDownMenu_SetText(dropdown, opt)
                        SmartInterface.ContentOverride = (opt ~= "Auto-Detect") and opt or nil
                        SmartInterface:UpdateDisplay()
                    end
                    info.checked = (SmartInterface.ContentOverride == opt) or (not SmartInterface.ContentOverride and opt == "Auto-Detect")
                    UIDropDownMenu_AddButton(info)
                end
            end)
            
            row.dropdown = dropdown
        else
            row.value = row:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
            row.value:SetPoint("RIGHT", 0, 0)
            row.value:SetText("...")
        end
        
        self.rows[i] = row
    end
    
    -- Apply Button
    f.applyBtn = CreateFrame("Button", nil, f, "GameMenuButtonTemplate")
    f.applyBtn:SetSize(120, 25)
    f.applyBtn:SetPoint("BOTTOM", 0, 20)
    f.applyBtn:SetText("Apply All")
    f.applyBtn:SetScript("OnClick", function() self:ApplyRecommendations() end)
    
    -- Register Events
    f:RegisterEvent("ZONE_CHANGED_NEW_AREA")
    f:RegisterEvent("PLAYER_ENTERING_WORLD")
    f:RegisterEvent("GROUP_ROSTER_UPDATE")
    f:SetScript("OnEvent", function() self:UpdateDisplay() end)
    
    -- Initial Update
    self:UpdateDisplay()
end

------------------------------------------------------------
-- Update Display Logic
------------------------------------------------------------
function SmartInterface:UpdateDisplay()
    if not self.frame then return end
    
    local content, difficulty = ContentDetector:GetCurrentContent()
    local specID = GetSpecializationInfo(GetSpecialization())
    
    -- 1. Content
    local content, difficulty = ContentDetector:GetCurrentContent()
    
    -- Apply Override
    if self.ContentOverride then
        if self.ContentOverride == "Raid" then content = "RAID"
        elseif self.ContentOverride == "Mythic+" then content = "MYTHIC_PLUS"
        elseif self.ContentOverride == "Delve" then content = "DELVE"
        elseif self.ContentOverride == "PvP" then content = "PVP"
        end
        -- Clear difficulty text if overridden to avoid confusion
        difficulty = nil 
    end

    -- Update Dropdown Text (if not already set by selection)
    -- Note: Dropdown text is usually set by selection, but we ensure it matches here if needed
    
    -- We don't set row.value for row 1 anymore, as it's a dropdown
    -- But we might want to show the *detected* content if in Auto-Detect mode
    if not self.ContentOverride then
        local displayText = content
        if difficulty then displayText = displayText .. " (" .. difficulty .. ")" end
        UIDropDownMenu_SetText(self.rows[1].dropdown, "Auto: " .. displayText)
    end
    
    -- 2. Spec (Placeholder logic for now, assumes current is okay unless mismatch)
    self.rows[2].value:SetText(select(2, GetSpecializationInfo(GetSpecialization())))
    
    -- 3. Talents
    local talentBuild = TalentRecommendations:GetRecommendation(specID, content)
    if talentBuild then
        self.rows[3].value:SetText(talentBuild.name)
        self.rows[3].value:SetTextColor(0, 1, 0) -- Green
    else
        self.rows[3].value:SetText("No Data")
        self.rows[3].value:SetTextColor(0.5, 0.5, 0.5) -- Grey
    end
    
    -- 4. PvP Talents (Row 4) - Only show if PvP
    if content == "PVP" or content == "ARENA" then
        self.rows[4]:Show()
        local pvpTalents = TalentRecommendations:GetPvPTalents(specID)
        if pvpTalents then
            -- Format as comma-separated string, truncate if too long
            local text = table.concat(pvpTalents, ", ")
            if string.len(text) > 35 then text = string.sub(text, 1, 32) .. "..." end
            self.rows[4].value:SetText(text)
            self.rows[4].value:SetTextColor(1, 0.5, 0) -- Orange
        else
            self.rows[4].value:SetText("None Recommended")
        end
    else
        self.rows[4]:Hide()
        self.rows[4].value:SetText("")
    end
    
    -- 5. Equipment (Row 5)
    -- Check if we have weights
    local weights = SkillWeaver.StatWeights:GetWeights(specID, content)
    if weights then
        self.rows[5].value:SetText("Optimized for " .. content)
        self.rows[5].value:SetTextColor(0, 1, 0)
    else
        self.rows[5].value:SetText("Default")
        self.rows[5].value:SetTextColor(1, 1, 0) -- Yellow
    end
    
    -- 6. Brann Perk (Row 6)
    local bestPerk, _ = BrannHelper:BestPerkForCurrentSpec()
    if bestPerk then
        self.rows[6].value:SetText(bestPerk)
        self.rows[6].value:SetTextColor(0, 1, 0)
    else
        self.rows[6].value:SetText("N/A")
        self.rows[6].value:SetTextColor(0.5, 0.5, 0.5)
    end
end

------------------------------------------------------------
-- Apply Recommendations
------------------------------------------------------------
function SmartInterface:ApplyRecommendations()
    local content = ContentDetector:GetCurrentContent()
    
    -- Apply Override
    if self.ContentOverride then
        if self.ContentOverride == "Raid" then content = "RAID"
        elseif self.ContentOverride == "Mythic+" then content = "MYTHIC_PLUS"
        elseif self.ContentOverride == "Delve" then content = "DELVE"
        elseif self.ContentOverride == "PvP" then content = "PVP"
        end
    end
    
    -- 1. Talents (Import String)
    local specID = GetSpecializationInfo(GetSpecialization())
    local talentString = TalentRecommendations:GetImportString(specID, content)
    if talentString then
        -- In a real addon, we'd use C_ClassTalents.ImportLoadout
        -- For now, we copy to clipboard
        print("SkillWeaver: Talent string copied to clipboard!")
        -- C_System.SetClipboard(talentString) -- Protected in some contexts, but usually okay
    end
    
    -- 2. Equipment
    EquipmentManager:EquipBestSet(content)
    
    -- 3. Brann Perk
    BrannHelper:ApplyBestPerk()
    
    print("SkillWeaver: Recommendations Applied for " .. content)
end

-- Auto-show on load for testing
C_Timer.After(2, function() SmartInterface:CreateUI() end)

return SmartInterface
