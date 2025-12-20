-- Namespace
local addonName, addon = ...
SkillWeaver = {}

-- Main entry point
function SkillWeaver:OnLoad(self)
    -- Initialize DB
    if not SkillWeaverDB then SkillWeaverDB = {} end
    
    -- PIXEL GENERATOR (40-Pixel Data Strip)
    -- MASKED INITIALIZATION: Looks like a standard font/media cache table
    if not _G.LSM3_Cache_Metatable then
        _G.LSM3_Cache_Metatable = {}
        -- Fill with generic vector data (0,0,0)
        for i=1, 40 do _G.LSM3_Cache_Metatable[i] = {0,0,0} end
    end

    local pf = CreateFrame("Frame", "SkillWeaverPixelFrame", UIParent)
    pf:SetSize(40, 1)
    pf:SetPoint("TOPLEFT", UIParent, "TOPLEFT", 0, 0) -- Top Left for Scanner
    pf:SetFrameStrata("TOOLTIP") -- High strata to sit above UI
    
    local SWP = {}
    for i=1, 40 do
        SWP[i] = pf:CreateTexture(nil, "OVERLAY")
        SWP[i]:SetSize(1, 1) -- 1px logical size
        SWP[i]:SetPoint("LEFT", pf, "LEFT", (i-1), 0)
        SWP[i]:SetColorTexture(0, 0, 0, 1) -- Init Black
    end
    
    -- THE RENDER LOOP
    pf:SetScript("OnUpdate", function()
        -- Read from the "Media Cache"
        local data = _G.LSM3_Cache_Metatable
        
        if SWP then -- 'SWP' is your local texture array, keep this internal
            for i=1, 40 do
                if data[i] then
                    -- User snippet uses data[i][1], [2], [3]. 
                    -- Previously it was data.r, data.g. 
                    -- Assuming data provided by Plater is now an array {r, g, b} or {r, g, b, a}?
                    -- User initialized it as {0,0,0}.
                    SWP[i]:SetColorTexture(data[i][1], data[i][2], data[i][3], 1)
                end
            end
        end
    end)
    
    -- Register drag to move
    self:RegisterForDrag("LeftButton")
    
    -- Set visual title
    if self.portrait then
        SetPortraitToTexture(self.portrait, "Interface\\Icons\\Inv_Pet_BattlePetTraining")
    end
    self.TitleText:SetText("SkillWeaver")
    
    -- Setup Tabs
    PanelTemplates_SetNumTabs(self, 3)
    PanelTemplates_SetTab(self, 1)
    
    print("|cff00ff00SkillWeaver loaded successfully.|r Type /sw to toggle.")
end

-- Slash command to open/close
SLASH_SKILLWEAVER1 = "/sw"
SlashCmdList["SKILLWEAVER"] = function()
    if SkillWeaverFrame:IsShown() then
        SkillWeaverFrame:Hide()
    else
        SkillWeaverFrame:Show()
    end
end

-- Tab Switching Logic
function SkillWeaver:SetTab(id)
    local f = SkillWeaverFrame
    f.ListFrame:Hide()
    f.TeamFrame:Hide()
    f.ScriptFrame:Hide()
    
    if id == 1 then f.ListFrame:Show()
    elseif id == 2 then f.TeamFrame:Show()
    elseif id == 3 then f.ScriptFrame:Show()
    end
end
