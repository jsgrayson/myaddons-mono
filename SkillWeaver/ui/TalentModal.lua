-- SkillWeaver/ui/TalentModal.lua
local SW = SkillWeaver
SW.UI = SW.UI or {}

-- 1. THE TOAST (Notification)
-- Uses standard RAID INFO colors and fonts
function SW.UI:ShowToast(title, subtitle, type)
    local f = SW_ToastFrame or CreateFrame("Frame", "SW_ToastFrame", UIParent, "BackdropTemplate")
    f:SetSize(280, 60)
    f:SetPoint("TOP", 0, -180)
    f:SetFrameStrata("DIALOG")
    
    -- Standard Tooltip Look
    f:SetBackdrop({
        bgFile = "Interface\\Tooltips\\UI-Tooltip-Background",
        edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
        tile = true, tileSize = 16, edgeSize = 16,
        insets = { left=4, right=4, top=4, bottom=4 }
    })
    
    -- Dark background, Gold border
    f:SetBackdropColor(0.05, 0.05, 0.05, 0.9)
    if type == "SUCCESS" then
        f:SetBackdropBorderColor(0, 1, 0, 1) -- Green border for success
    else
        f:SetBackdropBorderColor(1, 0.82, 0, 1) -- Gold/Yellow for alerts
    end

    if not f.title then
        f.title = f:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
        f.title:SetPoint("TOP", 0, -10)
        f.sub = f:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
        f.sub:SetPoint("TOP", 0, -32)
    end
    
    f.title:SetText(title)
    f.sub:SetText(subtitle)
    
    f:Show()
    f:SetAlpha(0)
    
    -- Simple Fade Animation
    UIFrameFadeIn(f, 0.2, 0, 1)
    C_Timer.After(3, function() UIFrameFadeOut(f, 0.5, 1, 0) end)
end

-- 2. THE IMPORT POPUP (Manual Fallback)
-- Looks like a standard WoW dialog box
function SW.UI:ShowImportModal(mode, importString)
    local f = SW_ImportModal or CreateFrame("Frame", "SW_ImportModal", UIParent, "BackdropTemplate")
    f:SetSize(450, 220)
    f:SetPoint("CENTER")
    f:SetFrameStrata("DIALOG")
    f:EnableMouse(true)
    f:SetMovable(true)
    f:RegisterForDrag("LeftButton")
    f:SetScript("OnDragStart", f.StartMoving)
    f:SetScript("OnDragStop", f.StopMovingOrSizing)
    
    -- Standard Dialog Background
    f:SetBackdrop({
        bgFile = "Interface\\DialogFrame\\UI-DialogBox-Background",
        edgeFile = "Interface\\DialogFrame\\UI-DialogBox-Border",
        tile = true, tileSize = 32, edgeSize = 32,
        insets = { left=11, right=12, top=12, bottom=11 }
    })

    -- Header
    local title = f:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
    title:SetPoint("TOP", 0, -16)
    title:SetText("SkillWeaver: Import Talents")

    -- Description
    local desc = f:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    desc:SetPoint("TOP", 0, -45)
    desc:SetWidth(400)
    desc:SetText("Auto-switch failed. Please create a loadout named:\n|cFFFFD100SW " .. mode .. "|r\n\nOr copy the string below to import manually:")

    -- EditBox (The Copy Field)
    -- Using ScrollFrame for long strings
    local scroll = CreateFrame("ScrollFrame", nil, f, "UIPanelScrollFrameTemplate")
    scroll:SetSize(360, 60)
    scroll:SetPoint("CENTER", 0, -10)

    local eb = CreateFrame("EditBox", nil, scroll)
    eb:SetMultiLine(true)
    eb:SetSize(360, 60)
    eb:SetFontObject(ChatFontNormal)
    eb:SetText(importString)
    eb:SetFocus()
    eb:HighlightText()
    eb:SetScript("OnEscapePressed", function() f:Hide() end)
    
    scroll:SetScrollChild(eb)

    -- Close Button
    local btn = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
    btn:SetSize(120, 25)
    btn:SetPoint("BOTTOM", 0, 20)
    btn:SetText("Done")
    btn:SetScript("OnClick", function() f:Hide() end)

    f:Show()
    SW_ImportModal = f
end
