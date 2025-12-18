-- ui/Minimap.lua
local SW = SkillWeaver
SW.UI = SW.UI or {}

function SW.UI:InitMinimap()
  if self.minimapButton then return end

  local b = CreateFrame("Button", "SkillWeaver_MinimapButton", Minimap)
  b:SetSize(32, 32)
  b:SetFrameStrata("MEDIUM")
  b:SetFrameLevel(Minimap:GetFrameLevel() + 10)

  -- Use a built-in Blizzard texture so it's always visible
  b:SetNormalTexture("Interface\\Minimap\\Tracking\\Class")
  b:SetHighlightTexture("Interface\\Minimap\\UI-Minimap-ZoomButton-Highlight", "ADD")

  -- Position: top-left of minimap (simple, reliable)
  b:SetPoint("TOPLEFT", Minimap, "TOPLEFT", -6, 6)

  b:RegisterForClicks("LeftButtonUp", "RightButtonUp")
  b:SetScript("OnClick", function(_, button)
    if button == "LeftButton" then
      if SW.UI and SW.UI.TogglePanel then
        SW.UI:TogglePanel()
      end
    else
      if SW.UI and SW.UI.ToggleMenu then
        SW.UI:ToggleMenu(b)
      end
    end
  end)

  -- Tooltip support
  b:SetScript("OnEnter", function(self)
    GameTooltip:SetOwner(self, "ANCHOR_LEFT")
    GameTooltip:SetText("SkillWeaver")
    GameTooltip:AddLine("Left-Click: Toggle Panel", 1, 1, 1)
    GameTooltip:AddLine("Right-Click: Options Menu", 1, 1, 1)
    GameTooltip:Show()
  end)
  b:SetScript("OnLeave", function() GameTooltip:Hide() end)

  b:Show()
  self.minimapButton = b
end
