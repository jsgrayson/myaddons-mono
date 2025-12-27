SkillWeaverDB = SkillWeaverDB or {}

-- 1. Default Data
SkillWeaverDefaults = {
  version = 7,
  enabled = true,
  toggles = {
    burst = true, defensives = true, interrupts = true, trinkets = false,
    groundTargetMode = "cursor", showHealButton = true, showSelfButton = true,
    hideEmptyButtons = false, 
  },
  ui = { minimap = { hide = false, angle = -0.785 }, panel = { show = true } },
  charSettings = {},
  bindingProfiles = {}, 
  currentBindingProfile = "None",
}

-- Standard Profiles (Using Real Commands)
local StandardProfiles = {
    ["Keyboard"] = {
        ["CLICK SkillWeaver_Button_ST:LeftButton"]   = "X",
        ["CLICK SkillWeaver_Button_AOE:LeftButton"]  = "C",
        ["CLICK SkillWeaver_Button_INT:LeftButton"]  = "R",
        ["CLICK SkillWeaver_Button_UTIL:LeftButton"] = "T",
        ["CLICK SkillWeaver_Button_HEAL:LeftButton"] = "CTRL-X",
        ["CLICK SkillWeaver_Button_SELF:LeftButton"] = "Z"
    },
    ["Controller"] = {
        ["CLICK SkillWeaver_Button_ST:LeftButton"]   = "PAD1",
        ["CLICK SkillWeaver_Button_AOE:LeftButton"]  = "PAD2",
        ["CLICK SkillWeaver_Button_INT:LeftButton"]  = "PADRTRIGGER",
        ["CLICK SkillWeaver_Button_UTIL:LeftButton"] = "PADLTRIGGER",
        ["CLICK SkillWeaver_Button_HEAL:LeftButton"] = "PAD3",
        ["CLICK SkillWeaver_Button_SELF:LeftButton"] = "PAD4"
    },
    ["MMO_Mouse"] = {
        ["CLICK SkillWeaver_Button_ST:LeftButton"]   = "NUMPAD1",
        ["CLICK SkillWeaver_Button_AOE:LeftButton"]  = "NUMPAD2",
        ["CLICK SkillWeaver_Button_INT:LeftButton"]  = "NUMPAD3",
        ["CLICK SkillWeaver_Button_UTIL:LeftButton"] = "NUMPAD4",
        ["CLICK SkillWeaver_Button_HEAL:LeftButton"] = "NUMPAD5",
        ["CLICK SkillWeaver_Button_SELF:LeftButton"] = "NUMPAD6"
    }
}

SkillWeaver = SkillWeaver or {}
local SW = SkillWeaver
SW.Defaults = SW.Defaults or {}
SW.Defaults.registry = SW.Defaults.registry or {}

function SW.Defaults:InitDB()
    -- FIXED: Deep Copy that handles non-table values safely
    local function deepCopy(src)
        if type(src) ~= "table" then return src end
        local t = {}
        for k,v in pairs(src) do
            t[k] = deepCopy(v)
        end
        return t
    end

    -- 1. Ensure DB Table and Version
    if not SkillWeaverDB.version then 
        SkillWeaverDB.version = SkillWeaverDefaults.version
    end

    -- Preserve existing data (synced via Python) while adding defaults
    for k,v in pairs(SkillWeaverDefaults) do
        if SkillWeaverDB[k] == nil then
            SkillWeaverDB[k] = deepCopy(v)
        end
    end

    -- 2. Force Enable
    if SkillWeaverDB.enabled == nil then SkillWeaverDB.enabled = true end
    
    -- 3. REPAIR PROFILES
    SkillWeaverDB.bindingProfiles = SkillWeaverDB.bindingProfiles or {}
    for name, data in pairs(StandardProfiles) do
        -- Inject if missing OR if outdated
        if not SkillWeaverDB.bindingProfiles[name] or (SkillWeaverDB.version < 7) then
            SkillWeaverDB.bindingProfiles[name] = deepCopy(data)
        end
    end
    
    SkillWeaverDB.version = SkillWeaverDefaults.version
end

-- === PUBLIC HELPERS ===

function SW.Defaults:GetCharKey()
    return UnitName("player").."-"..GetRealmName()
end

function SW.Defaults:GetCurrentBindingProfile() 
    if not SkillWeaverDB or not SkillWeaverDB.charSettings then return "Keyboard" end
    local s = SkillWeaverDB.charSettings[self:GetCharKey()]
    return s and s.bindingProfile or "Keyboard"
end

function SW.Defaults:SetBindingProfile(p)
    if not SkillWeaverDB then return end
    local k = self:GetCharKey()
    SkillWeaverDB.charSettings = SkillWeaverDB.charSettings or {}
    SkillWeaverDB.charSettings[k] = SkillWeaverDB.charSettings[k] or {}
    SkillWeaverDB.charSettings[k].bindingProfile = p
end

-- Utils
SW.Utils = SW.Utils or {}
function SW.Utils.DeepCopy(src)
    if type(src) ~= "table" then return src end
    local t = {}
    for k,v in pairs(src) do
        t[k] = SW.Utils.DeepCopy(v)
    end
    return t
end

-- Rotation Registry
function SW.Defaults:RegisterRotation(k, m, p, r) 
  self.registry[k] = self.registry[k] or {}; self.registry[k][m] = self.registry[k][m] or {}
  self.registry[k][m][p] = r
end

function SW.Defaults:GetFallbackRotation(k, m, p)
  local c = self.registry[k]; if not c then return nil end
  return c[m] and c[m][p] or nil
end
