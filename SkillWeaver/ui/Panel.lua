local SW = SkillWeaver
SW.UI = SW.UI or {}

function SW.UI:InitPanel()
  local f = CreateFrame("Frame", "SkillWeaver_Panel", UIParent, "BackdropTemplate")
  f:SetSize(360, 260)
  f:SetPoint("CENTER")
  f:SetBackdrop({
    bgFile = "Interface\\DialogFrame\\UI-DialogBox-Background",
    edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
    tile = true, tileSize = 16, edgeSize = 12,
    insets = { left=3, right=3, top=3, bottom=3 }
  })
  f:Hide()

  local title = f:CreateFontString(nil, "OVERLAY", "GameFontNormalLarge")
  title:SetPoint("TOPLEFT", 12, -10)
  title:SetText("SkillWeaver")

  local txt = f:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
  txt:SetPoint("TOPLEFT", 12, -40)
  txt:SetWidth(336)
  txt:SetJustifyH("LEFT")
  txt:SetJustifyV("TOP")
  txt:SetText("Loading...")

  self.panel = f
  self.panelText = txt
end

function SW.UI:TogglePanel()
  if not self.panel then return end
  if self.panel:IsShown() then self.panel:Hide() else self.panel:Show() end
end

function SW.UI:Toggle()
  self:TogglePanel()
end

function SW.UI:UpdatePanel()
  if not self.panelText then return end
  local key = SW.State:GetClassSpecKey()
  local mode = SW.State:GetMode()

  local sug = SW.TalentSuggestions and SW.TalentSuggestions[key]
  local p = sug and sug.PvE and sug.PvE[mode]
  self.panelText:SetText(p and (p.notes .. "\n\nTalents:\n" .. (p.talents or "N/A")) or "No build suggestions available for this mode.")
end
