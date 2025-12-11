--========================================================--
-- SkillWeaver - Sequence Browser UI (Dark Mode)
--========================================================--

local ADDON_NAME, SkillWeaver = ...
SkillWeaver.UI = SkillWeaver.UI or {}
local UI = {}
SkillWeaver.UI.SequenceBrowser = UI

local SAFE      = function() return SkillWeaver.SafeMode end
local RESTRICT  = function() return SkillWeaver.Restricted end
local FULL      = function() return SkillWeaver.FullEngine end

------------------------------------------------------------
-- Create Main Browser Frame
------------------------------------------------------------
function UI:Create()
    if self.frame then return end

    local f = CreateFrame("Frame", "SkillWeaverSequenceBrowser", UIParent, "BackdropTemplate")
    self.frame = f
    f:SetSize(420, 500)
    f:SetPoint("CENTER")
    f:SetMovable(true)
    f:EnableMouse(true)
    f:RegisterForDrag("LeftButton")
    f:SetScript("OnDragStart", f.StartMoving)
    f:SetScript("OnDragStop", f.StopMovingOrSizing)

    -- Dark Theme Background
    f:SetBackdrop({
        bgFile = "Interface\\DialogFrame\\UI-DialogBox-Background-Dark",
        edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
        edgeSize = 16, insets = { left = 4, right = 4, top = 4, bottom = 4 }
    })
    f:SetBackdropColor(0, 0, 0, 0.85)

    -- Title
    local title = f:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    title:SetPoint("TOP", 0, -12)
    title:SetText("|cff4af2f8SkillWeaver Sequence Browser|r")

    --------------------------------------------------------
    -- Search Box
    --------------------------------------------------------
    local search = CreateFrame("EditBox", nil, f, "InputBoxTemplate")
    search:SetSize(260, 28)
    search:SetPoint("TOPLEFT", 20, -45)
    search:SetAutoFocus(false)
    search:SetText("")
    search:SetScript("OnEscapePressed", search.ClearFocus)
    search:SetScript("OnEnterPressed", function() search:ClearFocus() end)

    local searchLabel = f:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    searchLabel:SetPoint("LEFT", search, "RIGHT", 10, 0)
    searchLabel:SetText("Search")

    --------------------------------------------------------
    -- Scroll Panel
    --------------------------------------------------------
    local scroll = CreateFrame("ScrollFrame", "SW_SeqBrowserScroll", f, "UIPanelScrollFrameTemplate")
    scroll:SetPoint("TOPLEFT", 20, -90)
    scroll:SetPoint("BOTTOMRIGHT", -30, 20)

    local container = CreateFrame("Frame", nil, scroll)
    container:SetSize(350, 1000)
    scroll:SetScrollChild(container)
    self.container = container

    --------------------------------------------------------
    -- Close Button
    --------------------------------------------------------
    local close = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
    close:SetSize(60, 24)
    close:SetPoint("TOPRIGHT", -12, -12)
    close:SetText("X")
    close:SetScript("OnClick", function() f:Hide() end)

    --------------------------------------------------------
    -- Store Reference
    --------------------------------------------------------
    self.searchBox = search
    self.scrollFrame = scroll

    -- Initial population
    self:RefreshList()
end

------------------------------------------------------------
-- Populate List of Sequences
------------------------------------------------------------
function UI:RefreshList()
    if not self.container then return end

    -- Clear old buttons
    for _, child in ipairs({ self.container:GetChildren() }) do
        child:Hide()
        child:SetParent(nil)
    end

    local class = select(2, UnitClass("player"))
    if not class then return end
    class = class:upper()

    local spec = GetSpecialization()
    if not spec then return end
    local specID = GetSpecializationInfo(spec)
    if not specID then return end

    local key = class .. "_" .. specID
    local seqData = SkillWeaver.Sequences[key]
    if not seqData then return end

    local searchText = (self.searchBox:GetText() or ""):lower()

    local offsetY = -10
    for modeName, variants in pairs(seqData) do
        for variant, sequence in pairs(variants) do

            -- Safe Mode hides HighPerformance
            if SAFE() and variant == "HighPerformance" then
                -- skip
            else
                -- Apply search filter
                if searchText == "" or 
                   modeName:lower():find(searchText) or
                   variant:lower():find(searchText) then

                    local btn = CreateFrame("Button", nil, self.container, "BackdropTemplate")
                    btn:SetSize(300, 40)
                    btn:SetPoint("TOPLEFT", 5, offsetY)

                    btn:SetBackdrop({
                        bgFile = "Interface\\Buttons\\WHITE8x8",
                        edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
                        edgeSize = 12
                    })
                    btn:SetBackdropColor(0.1, 0.1, 0.1, 0.8)

                    btn:SetScript("OnEnter", function()
                        btn:SetBackdropColor(0.2, 0.2, 0.2, 0.9)
                    end)
                    btn:SetScript("OnLeave", function()
                        btn:SetBackdropColor(0.1, 0.1, 0.1, 0.8)
                    end)

                    btn:SetScript("OnClick", function()
                        print("|cff4af2f8SkillWeaver|r: Selected " ..
                            modeName .. " - " .. variant)
                        SkillWeaver.UI.ModeSelector.lastMode = modeName
                        SkillWeaver.UI.ModeSelector.lastVariant = variant
                    end)

                    local text = btn:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
                    text:SetPoint("LEFT", 10, 0)
                    text:SetText(modeName .. "  |  " .. variant)

                    offsetY = offsetY - 45
                end
            end
        end
    end
end

------------------------------------------------------------
-- Toggle Window
------------------------------------------------------------
function UI:Toggle()
    if not self.frame then self:Create() end
    if self.frame:IsShown() then
        self.frame:Hide()
    else
        self.frame:Show()
        self:RefreshList()
    end
end

------------------------------------------------------------
-- Hook Slash Commands
------------------------------------------------------------
SlashCmdList["SWSEQ"] = function()
    SkillWeaver.UI.SequenceBrowser:Toggle()
end
SLASH_SWSEQ1 = "/swseq"
