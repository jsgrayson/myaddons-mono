-- SkillWeaver/content_detect.lua
-- Small, safe “what content am I in?” detector.
-- Returns one of: "raid", "mythicplus", "delve", "pvp", "openworld"

local addonName, addonTable = ...
local SW = addonTable.SkillWeaver or _G.SkillWeaver

if not SW then
  -- Fallback if loaded too early (though TOC should prevent this if ordered correctly)
  SW = LibStub("AceAddon-3.0"):GetAddon("SkillWeaver")
end

function SW:DetectContentMode()
  -- Manual override wins
  local override = self.db and self.db.profile and self.db.profile.settings and self.db.profile.settings.modeOverride
  if override and override ~= "auto" then
    return override
  end

  -- Instance detection
  local inInstance, instanceType = IsInInstance()
  if inInstance then
    if instanceType == "raid" then
      return "raid"
    end

    -- Mythic+ (Retail): active challenge map implies M+
    if instanceType == "party" then
      if C_ChallengeMode and C_ChallengeMode.GetActiveChallengeMapID then
        local mapID = C_ChallengeMode.GetActiveChallengeMapID()
        if mapID and mapID ~= 0 then
          return "mythicplus"
        end
      end
      -- regular dungeon / party instance (treat as openworld for now)
      return "openworld"
    end

    if instanceType == "pvp" or instanceType == "arena" then
      return "pvp"
    end

    -- Delves are “scenario-like” in many builds; API is in flux.
    -- Best-effort: if Blizzard exposes a Delves UI API, use it.
    if instanceType == "scenario" then
      if C_DelvesUI and C_DelvesUI.IsInDelve and C_DelvesUI.IsInDelve() then
        return "delve"
      end
      -- otherwise assume openworld unless user overrides
      return "openworld"
    end
  end

  -- World PVP check (optional; conservative)
  if C_PvP and C_PvP.IsWarModeDesired and C_PvP.IsWarModeDesired() then
    -- war mode is still "openworld" context, not "pvp instance"
    return "openworld"
  end

  return "openworld"
end
