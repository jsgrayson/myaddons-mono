-- Namespace
local addonName, addon = ...
PetWeaver = {}

-- Main Init
function PetWeaver:OnLoad(self)
    -- Init DB
    if not PetWeaverDB then PetWeaverDB = {} end
    
    self:RegisterForDrag("LeftButton")
    
    -- Icon & Title
    if self.portrait then
        SetPortraitToTexture(self.portrait, "Interface\\Icons\\Inv_Pet_BattlePetTraining")
    end
    self.TitleText:SetText("PetWeaver")
    
    -- Setup Tabs (Standard Blizzard API)
    PanelTemplates_SetNumTabs(self, 3)
    PanelTemplates_SetTab(self, 1)
    
    print("|cff0070ddPetWeaver loaded.|r Type /pw to toggle.")
end

-- Slash Command
SLASH_PETWEAVER1 = "/pw"
SlashCmdList["PETWEAVER"] = function()
    if PetWeaverFrame:IsShown() then
        PetWeaverFrame:Hide()
    else
        PetWeaverFrame:Show()
    end
end

-- Tab Switching
function PetWeaver:SetTab(id)
    local f = PetWeaverFrame
    f.ListFrame:Hide()
    f.TeamFrame:Hide()
    f.ScriptFrame:Hide()
    
    if id == 1 then f.ListFrame:Show()
    elseif id == 2 then f.TeamFrame:Show()
    elseif id == 3 then f.ScriptFrame:Show()
    end
end
