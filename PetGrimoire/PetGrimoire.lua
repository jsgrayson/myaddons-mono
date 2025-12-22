PetGrimoire = {}

function PetGrimoire:OnLoad(self)
    -- Load DB or empty table if Python hasn't run yet
    if not PetGrimoireDB_Static then 
        PetGrimoireDB_Static = { Encounters={}, Strategies={} }
        print("PetGrimoire: No Data File Found. Run Python script.")
    else
        print("PetGrimoire: Loaded " .. #PetGrimoireDB_Static.Strategies .. " strategies.")
    end

    self:RegisterForDrag("LeftButton")
    
    if self.portrait then
        SetPortraitToTexture(self.portrait, "Interface\\Icons\\Inv_Pet_BattlePetTraining")
    end
    self.TitleText:SetText("Pet Grimoire")
    
    -- Init Scroll Frame
    self.List.ScrollFrame.update = function() self:UpdateList() end
    HybridScrollFrame_CreateButtons(self.List.ScrollFrame, "PetGrimoireListButtonTemplate", 0, 0)
    self:UpdateList()
end

SLASH_PETGRIMOIRE1 = "/pg"
SlashCmdList["PETGRIMOIRE"] = function()
    if PetGrimoireFrame:IsShown() then PetGrimoireFrame:Hide() else PetGrimoireFrame:Show() end
end

function PetGrimoire:UpdateList()
    local scroll = self.List.ScrollFrame
    local buttons = scroll.buttons
    local offset = HybridScrollFrame_GetOffset(scroll)
    local data = PetGrimoireDB_Static.Strategies -- Simple list for now
    
    for i = 1, #buttons do
        local idx = offset + i
        if idx <= #data then
            local strat = data[idx]
            local enc = PetGrimoireDB_Static.Encounters[strat.encounterId]
            local name = enc and enc.name or "Unknown Encounter"
            
            buttons[i].Name:SetText(name)
            buttons[i].Note:SetText(strat.notes or "")
            buttons[i]:Show()
        else
            buttons[i]:Hide()
        end
    end
    
    HybridScrollFrame_Update(scroll, #data * 50, scroll:GetHeight())
end
