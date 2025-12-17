local SW = SkillWeaver
SW.UI = SW.UI or {}

local menuFrame

local function toggleValue(path)
  local t = SkillWeaverDB.toggles
  t[path] = not t[path]
  SW.Engine:RefreshAll("toggle_changed")
end

function SW.UI:ToggleMenu(anchor)
  if not menuFrame then
    menuFrame = CreateFrame("Frame", "SkillWeaver_Dropdown", UIParent, "UIDropDownMenuTemplate")
  end

  local key = SW.State:GetClassSpecKey()
  local mode = SW.State:GetMode()
  local profile = SW.Profiles:GetActiveProfileName(key)

  local function init()
    local info = UIDropDownMenu_CreateInfo()

    info.isTitle = true
    info.text = "SkillWeaver"
    info.notCheckable = true
    UIDropDownMenu_AddButton(info)

    info = UIDropDownMenu_CreateInfo()
    info.text = "Mode: " .. mode
    info.notCheckable = true
    UIDropDownMenu_AddButton(info)

    local modes = { "Delves", "MythicPlus", "Raid", "PvP", "OpenWorld" }
    if SkillWeaverBackend and SkillWeaverBackend:SupportsMidnight() then
      table.insert(modes, "Midnight")
    end

    for _, m in ipairs(modes) do
      info = UIDropDownMenu_CreateInfo()
      info.text = "Set Mode: " .. m
      info.notCheckable = true
      info.func = function() SW.State:SetMode(m) end
      UIDropDownMenu_AddButton(info)
    end

    info = UIDropDownMenu_CreateInfo()
    info.text = "Profile: " .. profile
    info.notCheckable = true
    UIDropDownMenu_AddButton(info)

    local profiles = { "Balanced", "HighPerformance", "Safe" }
    for _, p in ipairs(profiles) do
      info = UIDropDownMenu_CreateInfo()
      info.text = "Set Profile: " .. p
      info.notCheckable = true
      info.func = function() SW.Profiles:SetActiveProfileName(key, p) end
      UIDropDownMenu_AddButton(info)
    end

    info = UIDropDownMenu_CreateInfo()
    info.isTitle = true
    info.text = "Toggles"
    info.notCheckable = true
    UIDropDownMenu_AddButton(info)

    local toggles = {
      { k="burst", text="Burst" },
      { k="defensives", text="Defensives" },
      { k="interrupts", text="Interrupts" },
      { k="trinkets", text="Use Trinkets" },
      { k="dpsEmergencyHeals", text="DPS Emergency Heals" },
    }

    for _, t in ipairs(toggles) do
      info = UIDropDownMenu_CreateInfo()
      info.text = t.text
      info.checked = SkillWeaverDB.toggles[t.k]
      info.func = function()
        SkillWeaverDB.toggles[t.k] = not SkillWeaverDB.toggles[t.k]
        SW.Engine:RefreshAll("toggle_" .. t.k)
      end
      UIDropDownMenu_AddButton(info)
    end

    -- Ground Target Mode Submenu
    info = UIDropDownMenu_CreateInfo()
    info.isTitle, info.notCheckable = true, true
    info.text = "Ground Target Mode"
    UIDropDownMenu_AddButton(info)

    for _, v in ipairs({ "cursor", "player" }) do
      info = UIDropDownMenu_CreateInfo()
      info.text = (v == "cursor") and "@cursor (fast)" or "@player (safe)"
      info.checked = (SkillWeaverDB.toggles.groundTargetMode == v)
      info.func = function()
        SkillWeaverDB.toggles.groundTargetMode = v
        SW.Engine:RefreshAll("ground_mode")
      end
      UIDropDownMenu_AddButton(info)
    end

    info = UIDropDownMenu_CreateInfo()
    info.text = "Reload UI"
    info.notCheckable = true
    info.func = ReloadUI
    UIDropDownMenu_AddButton(info)
  end

  EasyMenu(init, menuFrame, anchor, 0, 0, "MENU")
end
