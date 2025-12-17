SkillWeaverDB = SkillWeaverDB or {}

local function deepCopy(src)
  local t = {}
  for k,v in pairs(src) do
    if type(v) == "table" then t[k] = deepCopy(v) else t[k] = v end
  end
  return t
end

SkillWeaverDefaults = {
  version = 1,
  enabled = true,

  -- Global “Mode” selection (can be overridden per spec)
  mode = "Delves", -- "Delves" | "MythicPlus" | "Raid" | "PvP" | "OpenWorld"

  -- Safety toggles (used by your backend logic; addon just exposes & persists)
  toggles = {
    burst = true,
    defensives = true,
    interrupts = true,
    trinkets = false,
    emergencyGroupHeals = true,

    dpsEmergencyHeals = true,
    groundTargetMode = "cursor",
  }, -- for hybrid DPS specs (your backend decides)

  -- UI
  ui = {
    minimap = { hide = false },
    panel = { show = true },
  },

  -- Profile selection
  profiles = {
    -- keyed by "CLASS_SPECID"
    -- example: ["DEATHKNIGHT_250"] = { name="Balanced", mode="Delves" }
  },

  -- Secure button macro templates (set by engine)
  bindings = {
    ST = "X",
    AOE = "C",
    INT = "R",
    UTIL = "T",
    HEAL = "CTRL-X",
    SELF = "Z",
  },
}

if not SkillWeaverDB.version then
  SkillWeaverDB = deepCopy(SkillWeaverDefaults)
end
