local LSM = LibStub("LibSharedMedia-3.0")

-- Ensure Holocron global exists
Holocron = Holocron or {}

-- 1. Register Textures
-- Note: These files must exist in the Interface/AddOns/HolocronCore/Media folder
if LSM then
    LSM:Register("background", "Holocron Arcane Glass", "Interface\\AddOns\\HolocronCore\\Media\\Glass_Arcane.tga")
    LSM:Register("background", "Holocron Industrial Glass", "Interface\\AddOns\\HolocronCore\\Media\\Glass_Industrial.tga")
    LSM:Register("background", "Holocron Cyber Glass", "Interface\\AddOns\\HolocronCore\\Media\\Glass_Cyber.tga")
    LSM:Register("background", "Holocron Druid Glass", "Interface\\AddOns\\HolocronCore\\Media\\Glass_Druid.tga")
    LSM:Register("background", "Holocron Titan Glass", "Interface\\AddOns\\HolocronCore\\Media\\Glass_Titan.tga")
    
    LSM:Register("border", "Holocron Glow", "Interface\\AddOns\\HolocronCore\\Media\\Border_Glow.tga")
    LSM:Register("font", "Holocron Header", "Interface\\AddOns\\HolocronCore\\Media\\Beaufort.ttf")
end

-- 2. Define Theme Colors
Holocron.Colors = {
    Arcane = { r = 0.0, g = 0.82, b = 1.0, hex = "00d2ff" },     -- Cyan/Blue
    Industrial = { r = 1.0, g = 0.55, b = 0.0, hex = "ff8c00" }, -- Amber/Orange
    Cyber = { r = 0.0, g = 1.0, b = 0.25, hex = "00ff41" },      -- Neon Green
    Druid = { r = 0.31, g = 0.78, b = 0.47, hex = "50c878" },    -- Emerald Green
    Titan = { r = 0.83, g = 0.68, b = 0.21, hex = "d4af37" }     -- Gold
}

-- 3. Theme Helper
function Holocron:GetTheme(moduleName)
    if moduleName == "DeepPockets" then 
        return self.Colors.Industrial, "Holocron Industrial Glass" 
    elseif moduleName == "GoblinAI" then 
        return self.Colors.Cyber, "Holocron Cyber Glass" 
    elseif moduleName == "PetWeaver" then 
        return self.Colors.Druid, "Holocron Druid Glass" 
    elseif moduleName == "SkillWeaver" then 
        return self.Colors.Titan, "Holocron Titan Glass" 
    else
        return self.Colors.Arcane, "Holocron Arcane Glass"
    end
end
