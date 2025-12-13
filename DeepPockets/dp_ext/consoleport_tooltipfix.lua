-- DP_TooltipConsolePortFix.lua
-- Backend-only, safe alongside BetterBags. Goal: recover when ConsolePort makes all tooltips vanish.

local DP = DP or {}
DP.TooltipFix = DP.TooltipFix or {}

local function IsCP()
  return IsAddOnLoaded("ConsolePort") or _G.ConsolePort ~= nil
end

local function ResetTooltip(reason)
  if not GameTooltip then return end

  -- Hard reset ownership/anchors without forcing a show.
  GameTooltip:Hide()
  GameTooltip:SetOwner(UIParent, "ANCHOR_NONE")
  GameTooltip:ClearAllPoints()
  GameTooltip:SetPoint("CENTER", UIParent, "CENTER", 0, 0)
  GameTooltip:SetOwner(nil)

  if DP.TooltipFix.debug then
    print("|cffDAA520DP|r Tooltip reset: " .. (reason or "unknown"))
  end
end

-- Optional: detect “tooltip is being force-hidden a lot”
local hideCount, hideWindowStart = 0, 0
hooksecurefunc(GameTooltip, "Hide", function()
  if not IsCP() then return end
  local t = GetTime()
  if hideWindowStart == 0 or (t - hideWindowStart) > 2.0 then
    hideWindowStart = t
    hideCount = 0
  end
  hideCount = hideCount + 1
end)

local f = CreateFrame("Frame")
f:RegisterEvent("PLAYER_ENTERING_WORLD")
f:RegisterEvent("PLAYER_REGEN_ENABLED") -- leaving combat is a common “stuck tooltip” moment
f:SetScript("OnEvent", function(_, event)
  if not IsCP() then return end
  ResetTooltip(event)
end)

-- Conservative watchdog:
-- Only intervenes if (a) CP is active, (b) tooltip is hidden, (c) you’re clearly over UI,
-- and (d) either tooltip has been hidden excessively recently OR it’s been dead for a while.
local deadFor = 0
f:SetScript("OnUpdate", function(_, dt)
  if not IsCP() then return end
  if InCombatLockdown() then return end

  local focus = GetMouseFocus()
  local overUI = focus and focus ~= WorldFrame and focus.IsVisible and focus:IsVisible()

  if GameTooltip and not GameTooltip:IsShown() and overUI then
    deadFor = deadFor + dt
  else
    deadFor = 0
  end

  -- Trigger conditions:
  -- 1) Tooltip has been “dead” while hovering UI for > 1.25s
  -- 2) OR ConsolePort/others are spamming Hide() (10+ hides in 2 seconds)
  if deadFor > 1.25 or (hideCount >= 10 and (GetTime() - hideWindowStart) <= 2.0) then
    hideCount = 0
    hideWindowStart = 0
    deadFor = 0
    ResetTooltip("watchdog")
  end
end)

-- Slash controls
SLASH_DPTOOLTIPFIX1 = "/dptipfix"
SlashCmdList["DPTOOLTIPFIX"] = function()
  ResetTooltip("manual")
  print("|cffDAA520DP|r Tooltip reset.")
end

SLASH_DPTOOLTIPDBG1 = "/dptipdbg"
SlashCmdList["DPTOOLTIPDBG"] = function(msg)
  msg = (msg or ""):lower()
  DP.TooltipFix.debug = (msg == "on") and true or (msg == "off") and false or not DP.TooltipFix.debug
  print("|cffDAA520DP|r Tooltip debug: " .. (DP.TooltipFix.debug and "ON" or "OFF"))
end
