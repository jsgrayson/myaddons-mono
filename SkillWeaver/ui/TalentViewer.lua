--========================================================--
-- SkillWeaver - Talent Import / Build Viewer UI (Dark Mode)
--========================================================--

local ADDON_NAME, SkillWeaver = ...
SkillWeaver.UI = SkillWeaver.UI or {}
local UI = {}
SkillWeaver.UI.TalentViewer = UI

local SAFE      = function() return SkillWeaver.SafeMode end
local RESTRICT  = function() return SkillWeaver.Restricted end
local FULL      = function() return SkillWeaver.FullEngine end


------------------------------------------------------------
-- Data Storage for Saved Builds
------------------------------------------------------------
SkillWeaver.DB.Talents = SkillWeaver.DB.Talents or {}


------------------------------------------------------------
-- Create UI Frame
------------------------------------------------------------
function UI:Create()
    if self.frame then return end

    local f = CreateFrame("Frame", "SkillWeaverTalentViewer", UIParent, "BackdropTemplate")
    self.frame = f
    f:SetSize(600, 520)
    f:SetPoint("CENTER")
    f:SetMovable(true)
    f:EnableMouse(true)
    f:RegisterForDrag("LeftButton")
    f:SetScript("OnDragStart", f.StartMoving)
    f:SetScript("OnDragStop", f.StopMovingOrSizing)

    -- Dark theme
    f:SetBackdrop({
        bgFile = "Interface\\DialogFrame\\UI-DialogBox-Background-Dark",
        edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
        edgeSize = 16,
        insets = { left = 4, right = 4, top = 4, bottom = 4 }
    })
    f:SetBackdropColor(0,0,0,0.90)

    -- Title
    local title = f:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    title:SetPoint("TOP", 0, -10)
    title:SetText("|cff4af2f8SkillWeaver Talent Viewer|r")

    --------------------------------------------------------
    -- Wowhead Import Box
    --------------------------------------------------------

    local importLabel = f:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    importLabel:SetPoint("TOPLEFT", 20, -50)
    importLabel:SetText("Import Wowhead Talent String")

    local importBox = CreateFrame("EditBox", nil, f, "InputBoxTemplate")
    importBox:SetSize(400, 28)
    importBox:SetPoint("TOPLEFT", importLabel, "BOTTOMLEFT", 0, -4)
    importBox:SetAutoFocus(false)

    self.importBox = importBox

    --------------------------------------------------------
    -- Import Button
    --------------------------------------------------------

    local importBtn = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
    importBtn:SetSize(100, 26)
    importBtn:SetPoint("LEFT", importBox, "RIGHT", 10, 0)
    importBtn:SetText("Import")

    importBtn:SetScript("OnClick", function()
        local str = importBox:GetText()
        if not str or str == "" then
            print("|cffFF6666No import string provided.|r")
            return
        end

        UI:LoadTalentString(str)
    end)

    --------------------------------------------------------
    -- Load Scraped Button
    --------------------------------------------------------
    local loadScraped = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
    loadScraped:SetSize(120, 26)
    loadScraped:SetPoint("LEFT", importBtn, "RIGHT", 10, 0)
    loadScraped:SetText("Load Scraped")
    
    loadScraped:SetScript("OnClick", function()
        local spec = SkillWeaver.currentSpec
        local class = select(2, UnitClass("player"))
        local key = class .. "_" .. spec
        
        -- Try to find scraped talents for current mode, or fallback to Raid
        local mode = SkillWeaver.UI.ModeSelector and SkillWeaver.UI.ModeSelector.lastMode or "Raid"
        
        local tData = SkillWeaver.Talents[key]
        if tData and tData[mode] and tData[mode]["Scraped"] then
            UI:LoadTalentString(tData[mode]["Scraped"])
        else
            print("|cffFF6666No scraped talents found for " .. mode .. ".|r")
        end
    end)

    --------------------------------------------------------
    -- Scrollable Talent Display
    --------------------------------------------------------

    local scroll = CreateFrame("ScrollFrame", "SW_TalentScrollFrame", f, "UIPanelScrollFrameTemplate")
    scroll:SetPoint("TOPLEFT", 20, -140)
    scroll:SetPoint("BOTTOMRIGHT", -30, 80)

    local container = CreateFrame("Frame", nil, scroll)
    container:SetSize(520, 2000)
    scroll:SetScrollChild(container)

    self.container = container
    self.scroll = scroll

    --------------------------------------------------------
    -- Save Button
    --------------------------------------------------------

    local save = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
    save:SetSize(120, 26)
    save:SetPoint("BOTTOMLEFT", 20, 20)
    save:SetText("Save Build")

    save:SetScript("OnClick", function()
        UI:SaveBuild()
    end)

    --------------------------------------------------------
    -- Apply Button
    --------------------------------------------------------

    local apply = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
    apply:SetSize(120, 26)
    apply:SetPoint("LEFT", save, "RIGHT", 20, 0)
    apply:SetText("Apply Build")

    apply:SetScript("OnClick", function()
        UI:ApplyBuild()
    end)

    --------------------------------------------------------
    -- Close Button
    --------------------------------------------------------

    local close = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
    close:SetSize(60, 24)
    close:SetPoint("BOTTOMRIGHT", -20, 22)
    close:SetText("X")

    close:SetScript("OnClick", function() f:Hide() end)
end


------------------------------------------------------------
-- Load & Display a Wowhead Talent String
------------------------------------------------------------
function UI:LoadTalentString(str)
    -- In Midnight, talent API changes — we store string only.
    self.currentTalentString = str

    print("|cff4af2f8SkillWeaver|r: Talent string loaded.")

    self:RenderTalents(str)
end


------------------------------------------------------------
-- Display talent lines (pretty text version)
------------------------------------------------------------
function UI:RenderTalents(str)
    if not self.container then return end

    -- Clear container
    for _, child in ipairs({ self.container:GetChildren() }) do
        child:Hide()
        child:SetParent(nil)
    end

    -- Very clean display: break string into chunks
    local offsetY = -10
    local rawLines = {}

    for chunk in str:gmatch("[^:]+") do
        table.insert(rawLines, chunk)
    end

    for i, line in ipairs(rawLines) do
        local box = CreateFrame("Frame", nil, self.container, "BackdropTemplate")
        box:SetSize(480, 40)
        box:SetPoint("TOPLEFT", 0, offsetY)
        box:SetBackdrop({
            bgFile = "Interface\\Buttons\\WHITE8x8",
            edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
            edgeSize = 10
        })
        box:SetBackdropColor(0.12, 0.12, 0.12, 0.80)

        local text = box:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
        text:SetPoint("LEFT", 10, 0)
        text:SetText("|cff99CCFFLine " .. i .. ":|r  " .. line)

        offsetY = offsetY - 45
    end
end


------------------------------------------------------------
-- Save Build (per class+spec)
------------------------------------------------------------
function UI:SaveBuild()
    if not self.currentTalentString then
        print("|cffFF6666No talent string to save.|r")
        return
    end

    local class = select(2, UnitClass("player"))
    local specIndex = GetSpecialization()
    if not specIndex then
        print("|cffFF6666Cannot determine spec.|r")
        return
    end

    local specID = GetSpecializationInfo(specIndex)

    SkillWeaver.DB.Talents[class] = SkillWeaver.DB.Talents[class] or {}
    SkillWeaver.DB.Talents[class][specID] = self.currentTalentString

    print("|cff4af2f8SkillWeaver|r: Build saved for " .. class .. " (" .. specID .. ")")
end


------------------------------------------------------------
-- Apply Saved Build (links to ModeSelector)
------------------------------------------------------------
function UI:ApplyBuild()
    if not self.currentTalentString then
        print("|cffFF6666No build loaded.|r")
        return
    end

    print("|cff4af2f8SkillWeaver|r: Applying talents...")
    
    if C_ClassTalents and C_ClassTalents.ImportLoadout then
        local success, err = pcall(function()
            C_ClassTalents.ImportLoadout(self.currentTalentString)
        end)
        if success then
             print("|cff00ff00Talents imported successfully!|r")
        else
             print("|cffFF0000Error importing talents: " .. (err or "Unknown") .. "|r")
        end
    else
        print("|cffFF0000Talent Import API not available.|r")
    end

    SkillWeaver.UI.ModeSelector.lastVariant = SAFE() and "Safe" or "Balanced"
end


------------------------------------------------------------
-- Toggle
------------------------------------------------------------
function UI:Toggle()
    if not self.frame then self:Create() end
    if self.frame:IsShown() then
        self.frame:Hide()
    else
        self.frame:Show()
    end
end


------------------------------------------------------------
-- Slash Command
------------------------------------------------------------
SLASH_SWTALENTS1 = "/swtalents"
SlashCmdList["SWTALENTS"] = function()
    SkillWeaver.UI.TalentViewer:Toggle()
end
