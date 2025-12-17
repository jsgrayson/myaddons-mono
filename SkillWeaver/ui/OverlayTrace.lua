-- ui/OverlayTrace.lua
local addonName, addonTable = ...
local SkillWeaver = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
local OverlayTrace = {}
SkillWeaver.OverlayTrace = OverlayTrace

-- We need to require Trace, or assume it's loaded. 
-- Since we are in the addon, let's grab it via file return if we can, or global if we set it.
-- We'll assume typically `local Trace = require(...)` semantics if we bad a loader, but WoW 
-- usually relies on globals or addonTable.
-- Let's assume we can access it via addonTable or we'll define a way to get it.
-- For now, let's grab it from addonTable which we set in DecisionTrace.
local Trace = addonTable.DecisionTrace

function OverlayTrace:Create()
  if self.frame then return end
  
  local f = CreateFrame("Frame", "SkillWeaverTraceOverlay", UIParent, "BackdropTemplate")
  f:SetSize(400, 140)
  f:SetPoint("CENTER", UIParent, "CENTER", 0, -220)
  f:SetMovable(true)
  f:EnableMouse(true)
  f:RegisterForDrag("LeftButton")
  f:SetScript("OnDragStart", f.StartMoving)
  f:SetScript("OnDragStop", f.StopMovingOrSizing)
  
  -- Backdrop
  f:SetBackdrop({
      bgFile = "Interface\\Tooltips\\UI-Tooltip-Background",
      edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
      tile = true, tileSize = 16, edgeSize = 16,
      insets = { left = 4, right = 4, top = 4, bottom = 4 }
  })
  f:SetBackdropColor(0, 0, 0, 0.7)

  f.text = f:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
  f.text:SetPoint("TOPLEFT", f, "TOPLEFT", 10, -10)
  f.text:SetPoint("BOTTOMRIGHT", f, "BOTTOMRIGHT", -10, 10)
  f.text:SetJustifyH("LEFT")
  f.text:SetJustifyV("TOP")
  f.text:SetText("SkillWeaver Trace Initialized")

  f:Hide()
  self.frame = f
end

function OverlayTrace:SetShown(shown)
  if not self.frame then self:Create() end
  if shown then 
      self.frame:Show() 
      Trace:SetLevel(1) -- Auto enable trace if overlay shown
  else 
      self.frame:Hide() 
  end
end

function OverlayTrace:Toggle()
    if not self.frame then self:Create() end
    if self.frame:IsShown() then
        self:SetShown(false)
    else
        self:SetShown(true)
    end
end

function OverlayTrace:Update()
  if not self.frame or not self.frame:IsShown() then return end
  if not Trace then Trace = addonTable.DecisionTrace end
  if not Trace then return end
  
  local items = Trace:Last(8)
  local lines = {}
  for _, it in ipairs(items) do
    local timeStr = string.format("%0.1f", it.t % 100)
    if it.kind == "chosen" then
      lines[#lines+1] = ("|cff00ff00[OK]|r %s: %s"):format(it.section or "?", it.command or "?")
    else
      -- Shorten reason
      local reason = it.reason or "?"
      local detail = it.detail or ""
      lines[#lines+1] = ("|cffff0000[NO]|r %s: %s |cffaaaaaa(%s)|r"):format(it.section or "?", it.command or "?", reason)
    end
  end
  
  -- Fill empty lines to keep size stable?
  while #lines < 8 do
      table.insert(lines, "")
  end
  
  self.frame.text:SetText(table.concat(lines, "\n"))
end

return OverlayTrace
