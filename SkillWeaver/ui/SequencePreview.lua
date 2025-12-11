--========================================================--
-- SkillWeaver - Sequence Preview Panel (Dark Mode)
--========================================================--

local ADDON_NAME, SkillWeaver = ...
SkillWeaver.UI = SkillWeaver.UI or {}
local UI = {}
SkillWeaver.UI.SequencePreview = UI

local SAFE      = function() return SkillWeaver.SafeMode end
local RESTRICT  = function() return SkillWeaver.Restricted end
local FULL      = function() return SkillWeaver.FullEngine end


------------------------------------------------------------
-- Create Frame
------------------------------------------------------------

function UI:Create()
    if self.frame then return end

    local f = CreateFrame("Frame", "SkillWeaverSequencePreview", UIParent, "BackdropTemplate")
    self.frame = f
    f:SetSize(540, 500)
    f:SetPoint("CENTER")
    f:SetMovable(true)
    f:EnableMouse(true)
    f:RegisterForDrag("LeftButton")
    f:SetScript("OnDragStart", f.StartMoving)
    f:SetScript("OnDragStop", f.StopMovingOrSizing)

    -- Dark, glassy background
    f:SetBackdrop({
        bgFile = "Interface\\DialogFrame\\UI-DialogBox-Background-Dark",
        edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
        edgeSize = 16, 
        insets = { left = 4, right = 4, top = 4, bottom = 4 }
    })
    f:SetBackdropColor(0, 0, 0, 0.85)

    -- Title
    local title = f:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    title:SetPoint("TOP", 0, -12)
    title:SetText("|cff4af2f8SkillWeaver Sequence Preview|r")

    --------------------------------------------------------
    -- Header: Mode + Variant labels
    --------------------------------------------------------

    local header = f:CreateFontString(nil, "OVERLAY", "GameFontHighlightLarge")
    header:SetPoint("TOPLEFT", 20, -50)
    header:SetText("")

    self.header = header

    --------------------------------------------------------
    -- Scrollable Step Viewer
    --------------------------------------------------------

    local scroll = CreateFrame("ScrollFrame", "SW_SeqPreviewScroll", f, "UIPanelScrollFrameTemplate")
    scroll:SetPoint("TOPLEFT", 20, -90)
    scroll:SetPoint("BOTTOMRIGHT", -30, 60)

    local container = CreateFrame("Frame", nil, scroll)
    container:SetSize(480, 2000)  -- Big enough; auto-clamped by scroll
    scroll:SetScrollChild(container)

    self.container = container
    self.scroll = scroll

    --------------------------------------------------------
    -- Apply Button
    --------------------------------------------------------

    local apply = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
    apply:SetSize(140, 28)
    apply:SetPoint("BOTTOMLEFT", 20, 20)
    apply:SetText("Apply Rotation")

    apply:SetScript("OnClick", function()
        if UI.currentMode and UI.currentVariant then
            SkillWeaver.UI.ModeSelector.lastMode = UI.currentMode
            SkillWeaver.UI.ModeSelector.lastVariant = UI.currentVariant
            print("|cff4af2f8SkillWeaver|r: Applied " ..
                  UI.currentMode .. " - " .. UI.currentVariant)
        end
    end)

    --------------------------------------------------------
    -- Copy Button
    --------------------------------------------------------

    local copy = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
    copy:SetSize(140, 28)
    copy:SetPoint("LEFT", apply, "RIGHT", 20, 0)
    copy:SetText("Copy to Clipboard")

    copy:SetScript("OnClick", function()
        if not UI.currentSequence then
            print("|cffFF6666No sequence loaded.|r")
            return
        end

        local macroText = ""
        for i, step in ipairs(UI.currentSequence.steps) do
            macroText = macroText .. (step.command or "") .. "\n"
        end

        -- Classic WoW copy: place text into Chat EditBox
        ChatEdit_ActivateChat(ChatEdit_GetActiveWindow())
        ChatEdit_InsertLink(macroText)

        print("|cff4af2f8SkillWeaver|r: Sequence copied to chat box.")
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
-- Render Sequence Steps
------------------------------------------------------------

function UI:RenderSteps(seq)
    if not seq or not self.container then return end

    -- Clear old entries
    for _, child in ipairs({ self.container:GetChildren() }) do
        child:Hide()
        child:SetParent(nil)
    end

    local offsetY = -10

    for i, step in ipairs(seq.steps) do
        local box = CreateFrame("Frame", nil, self.container, "BackdropTemplate")
        box:SetSize(440, 50)
        box:SetPoint("TOPLEFT", 0, offsetY)

        box:SetBackdrop({
            bgFile = "Interface\\Buttons\\WHITE8x8",
            edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
            edgeSize = 10
        })
        box:SetBackdropColor(0.12, 0.12, 0.12, 0.85)

        -- Command Text
        local cmd = box:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
        cmd:SetPoint("TOPLEFT", 10, -6)
        cmd:SetText("|cff99FF99" .. (step.command or "") .. "|r")

        -- Conditions (hide advanced if SafeMode)
        local cond = box:CreateFontString(nil, "OVERLAY", "GameFontDisable")
        cond:SetPoint("TOPLEFT", 10, -28)

        if SAFE() then
            cond:SetText("(conditions hidden in Safe Mode)")
        else
            cond:SetText(step.conditions ~= "" and step.conditions or "(no conditions)")
        end

        offsetY = offsetY - 55
    end
end

------------------------------------------------------------
-- Public: Open Panel to Show a Sequence
------------------------------------------------------------

function UI:ShowSequence(mode, variant, sequenceTable)
    if not self.frame then self:Create() end

    self.currentMode    = mode
    self.currentVariant = variant
    self.currentSequence= sequenceTable

    self.header:SetText(
        "|cff4af2f8Mode:|r " .. mode ..
        "   |cff66CCFFVariant:|r " .. variant
    )

    self:RenderSteps(sequenceTable)

    self.frame:Show()
end

------------------------------------------------------------
-- Slash Command Integration
------------------------------------------------------------

SLASH_SWPREV1 = "/swpreview"
SlashCmdList["SWPREV"] = function()
    SkillWeaver.UI.SequencePreview:Toggle()
end

function UI:Toggle()
    if not self.frame then self:Create() end
    if self.frame:IsShown() then self.frame:Hide()
    else self.frame:Show() end
end
