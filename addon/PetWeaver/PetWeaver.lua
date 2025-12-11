local ADDON_NAME, PetWeaver = ...

-- SavedVariables
PetWeaverSaved = PetWeaverSaved or {
    battles = {}
}

local frame = CreateFrame("Frame")
frame:RegisterEvent("PET_BATTLE_OPENING_START")
frame:RegisterEvent("PET_BATTLE_CLOSE")
frame:RegisterEvent("PET_BATTLE_ACTION_LOG")

local currentBattle = nil

function PetWeaver:StartBattle()
    currentBattle = {
        timestamp = time(),
        enemyID = C_PetBattles.GetDisplayID(2, 1), -- Enemy Pet 1 Display ID (NPC ID?)
        enemyName = C_PetBattles.GetName(2, 1),
        rounds = {}
    }
    print("PetWeaver: Battle Recording Started for " .. (currentBattle.enemyName or "Unknown"))
end

function PetWeaver:EndBattle()
    if currentBattle then
        table.insert(PetWeaverSaved.battles, currentBattle)
        print("PetWeaver: Battle Recorded. Total Rounds: " .. #currentBattle.rounds)
        currentBattle = nil
    end
end

function PetWeaver:LogAction(...)
    if not currentBattle then return end
    
    -- Parse Combat Log
    -- This is complex, simplified for now:
    -- We want to know what ability the ENEMY used.
    
    -- C_PetBattles.GetAbilityInfo(petOwner, petIndex, abilityIndex)
    -- But we need the EVENT log to know what happened *this turn*.
    
    -- Actually, simpler approach:
    -- On "PET_BATTLE_PET_ROUND_PLAYBACK_COMPLETE" or similar, check history?
    -- Or just listen to CHAT_MSG_PET_BATTLE_COMBAT_LOG?
end

-- Hooking Chat Log might be easier for "Basic" recording
frame:RegisterEvent("CHAT_MSG_PET_BATTLE_COMBAT_LOG")

frame:SetScript("OnEvent", function(self, event, ...)
    if event == "PET_BATTLE_OPENING_START" then
        PetWeaver:StartBattle()
    elseif event == "PET_BATTLE_CLOSE" then
        PetWeaver:EndBattle()
    elseif event == "CHAT_MSG_PET_BATTLE_COMBAT_LOG" then
        local msg = ...
        if currentBattle then
            -- Store raw log for Python to parse? 
            -- Or try to parse here. Python is better at parsing strings.
            -- Let's store raw log lines for now.
            table.insert(currentBattle.rounds, msg)
        end
    end
end)
