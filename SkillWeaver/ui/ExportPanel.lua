-- ui/ExportPanel.lua
local addonName, addonTable = ...
local ExportPanel = {}
addonTable.ExportPanel = ExportPanel
local RotDump = addonTable.RotationDump
local SpellDump = addonTable.SpellbookDumpV2

ExportPanel.frame = nil

local function currentTimeLabel()
  if date then return date("%Y-%m-%d %H:%M:%S") end
  return tostring(GetTime and GetTime() or 0)
end

local function appendText(box, s)
  local cur = box:GetText() or ""
  if cur ~= "" and not cur:match("\n$") then cur = cur .. "\n" end
  box:SetText(cur .. s)
  -- Scroll to bottom? Maybe.
end

local function setText(box, s)
  box:SetText(s or "")
  box:HighlightText()
  box:SetFocus()
end

-- Capture print output into the box (temporarily hook print)
local function captureToBox(box, fn)
  local oldPrint = print
  print = function(...)
    local parts = {}
    for i=1, select("#", ...) do
      parts[#parts+1] = tostring(select(i, ...))
    end
    appendText(box, table.concat(parts, " "))
  end

  local ok, err = pcall(fn)

  print = oldPrint

  if not ok then
    appendText(box, "ERROR: " .. tostring(err))
  end
end

function ExportPanel:Create()
  if self.frame then return end

  local f = CreateFrame("Frame", "SkillWeaverExportPanel", UIParent, "BackdropTemplate")
  f:SetSize(780, 520)
  f:SetPoint("CENTER")
  f:SetMovable(true); f:EnableMouse(true)
  f:RegisterForDrag("LeftButton")
  f:SetScript("OnDragStart", f.StartMoving)
  f:SetScript("OnDragStop", f.StopMovingOrSizing)
  f:SetBackdrop({
    bgFile="Interface/Tooltips/UI-Tooltip-Background",
    edgeFile="Interface/Tooltips/UI-Tooltip-Border",
    tile=true, tileSize=16, edgeSize=16,
    insets={left=4,right=4,top=4,bottom=4}
  })
  f:SetBackdropColor(0,0,0,0.92)

  f.title = f:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
  f.title:SetPoint("TOPLEFT", 12, -10)
  f.title:SetText("SkillWeaver Exporter")
  
  -- Ensure localized close button works or manual close
  local close = CreateFrame("Button", nil, f, "UIPanelCloseButton")
  close:SetPoint("TOPRIGHT", -4, -4)

  -- Controls row
  local y = -36

  f.btnRot = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
  f.btnRot:SetSize(160, 22)
  f.btnRot:SetPoint("TOPLEFT", 12, y)
  f.btnRot:SetText("Export Rotations")
  f.btnRot.tooltipText = "Collect SWROT_CHUNK lines from loaded sequences"

  f.btnSpell = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
  f.btnSpell:SetSize(190, 22)
  f.btnSpell:SetPoint("LEFT", f.btnRot, "RIGHT", 8, 0)
  f.btnSpell:SetText("Dump+Export Spells")
  f.btnSpell.tooltipText = "Runs /swspelldump2 then exports SWSPELL2_CHUNK lines"

  f.chkTooltip = CreateFrame("CheckButton", nil, f, "UICheckButtonTemplate")
  f.chkTooltip:SetPoint("LEFT", f.btnSpell, "RIGHT", 10, 0)
  f.chkTooltip.text = f.chkTooltip:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
  f.chkTooltip.text:SetPoint("LEFT", f.chkTooltip, "RIGHT", 2, 0)
  f.chkTooltip.text:SetText("Tooltip hints")
  f.chkTooltip:SetChecked(false)

  f.btnAll = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
  f.btnAll:SetSize(180, 22)
  f.btnAll:SetPoint("TOPLEFT", 12, y-28)
  f.btnAll:SetText("Export ALL (Both)")
  f.btnAll.tooltipText = "Exports rotations + spelldump to the box"

  f.btnClear = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
  f.btnClear:SetSize(90, 22)
  f.btnClear:SetPoint("LEFT", f.btnAll, "RIGHT", 8, 0)
  f.btnClear:SetText("Clear")

  f.btnSelect = CreateFrame("Button", nil, f, "UIPanelButtonTemplate")
  f.btnSelect:SetSize(120, 22)
  f.btnSelect:SetPoint("LEFT", f.btnClear, "RIGHT", 8, 0)
  f.btnSelect:SetText("Select All")

  -- Multi-line scroll box
  local sf = CreateFrame("ScrollFrame", nil, f, "UIPanelScrollFrameTemplate")
  sf:SetPoint("TOPLEFT", 12, -96)
  sf:SetPoint("BOTTOMRIGHT", -32, 12)

  local eb = CreateFrame("EditBox", nil, sf)
  eb:SetMultiLine(true)
  eb:SetAutoFocus(false)
  eb:SetFontObject(ChatFontNormal)
  eb:SetWidth(720)
  eb:SetScript("OnEscapePressed", function() eb:ClearFocus() end)

  sf:SetScrollChild(eb)

  f.scroll = sf
  f.box = eb

  -- Button wiring
  f.btnClear:SetScript("OnClick", function()
    setText(f.box, "")
  end)

  f.btnSelect:SetScript("OnClick", function()
    f.box:HighlightText()
    f.box:SetFocus()
  end)

  f.btnRot:SetScript("OnClick", function()
    if not RotDump then RotDump = addonTable.RotationDump end
    if RotDump then
        appendText(f.box, ("--- SkillWeaver Rotations Export @ %s ---"):format(currentTimeLabel()))
        captureToBox(f.box, function()
          RotDump:ExportChunks(220)
        end)
        appendText(f.box, "--- END ROTATIONS ---\n")
        f.box:HighlightText()
        f.box:SetFocus()
    else
        appendText(f.box, "Error: RotationDump module not loaded.\n")
    end
  end)

  f.btnSpell:SetScript("OnClick", function()
    if not SpellDump then SpellDump = addonTable.SpellbookDumpV2 end
    if SpellDump then
        appendText(f.box, ("--- SkillWeaver Spellbook Export @ %s ---"):format(currentTimeLabel()))
        local wantTooltip = f.chkTooltip:GetChecked() == true
        captureToBox(f.box, function()
          SpellDump:ScanSpellbook({ tooltip = wantTooltip })
          SpellDump:ExportChunks(220)
        end)
        appendText(f.box, "--- END SPELLBOOK ---\n")
        f.box:HighlightText()
        f.box:SetFocus()
    else
        appendText(f.box, "Error: SpellbookDumpV2 module not loaded.\n")
    end
  end)

  f.btnAll:SetScript("OnClick", function()
    if not RotDump then RotDump = addonTable.RotationDump end
    if not SpellDump then SpellDump = addonTable.SpellbookDumpV2 end

    appendText(f.box, ("=== SkillWeaver FULL EXPORT @ %s ==="):format(currentTimeLabel()))
    captureToBox(f.box, function()
      if RotDump then RotDump:ExportChunks(220) end
      local wantTooltip = f.chkTooltip:GetChecked() == true
      if SpellDump then
        SpellDump:ScanSpellbook({ tooltip = wantTooltip })
        SpellDump:ExportChunks(220)
      end
    end)
    appendText(f.box, "=== END FULL EXPORT ===\n")
    f.box:HighlightText()
    f.box:SetFocus()
  end)

  self.frame = f
  f:Hide()
end

function ExportPanel:Toggle()
  self:Create()
  if self.frame:IsShown() then
    self.frame:Hide()
  else
    self.frame:Show()
    self.frame.box:SetFocus()
    self.frame.box:HighlightText()
  end
end

return ExportPanel
