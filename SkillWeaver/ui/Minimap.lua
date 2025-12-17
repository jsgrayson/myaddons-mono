local SW = SkillWeaver
SW.UI = SW.UI or {}

function SW.UI:Init()
  SW.UI:InitPanel()
  SW.UI:InitMinimap()
end

function SW.UI:InitMinimap()
  local btn = CreateFrame("Button", "SkillWeaver_MinimapButton", Minimap)
  btn:SetSize(32, 32)
  btn:SetNormalTexture("Interface\\AddOns\\SkillWeaver\\UI\\icon") -- add an icon file later
  btn:SetPoint("TOPLEFT", Minimap, "TOPLEFT")

  btn:RegisterForClicks("LeftButtonUp", "RightButtonUp")
  btn:SetScript("OnClick", function(_, button)
    if button == "LeftButton" then
      SW.UI:TogglePanel()
    else
      SW.UI:ToggleMenu(btn)
    end
  end)

  self.minimapButton = btn
end
