-- PetWeaverEnemyRecorder.lua
-- Records enemy pet abilities during battles for AI script generation

local addonName, addon = ...

PetWeaverEnemyRecorder = {}
local recorder = PetWeaverEnemyRecorder

-- Saved variables
PetWeaverEnemyRecordings = PetWeaverEnemyRecordings or {}

-- Current battle state
local currentBattle = nil
local currentTurn = 0
local isRecording = false

function recorder:Initialize()
    print("|cFF00FF00PetWeaver Enemy Recorder loaded!|r Type /pwrecord to toggle recording")
    
    -- Slash command
    SLASH_PWRECORD1 = "/pwrecord"
    SlashCmdList["PWRECORD"] = function(msg)
        self:ToggleRecording()
    end
    
    -- Hook battle events
    self:RegisterEvents()
end

function recorder:RegisterEvents()
    local frame = CreateFrame("Frame")
    frame:RegisterEvent("PET_BATTLE_OPENING_START")
    frame:RegisterEvent("PET_BATTLE_TURN_STARTED")
    frame:RegisterEvent("PET_BATTLE_ACTION_SELECTED")
    frame:RegisterEvent("PET_BATTLE_CLOSE")
    frame:RegisterEvent("CHAT_MSG_PET_BATTLE_COMBAT_LOG")
    
    frame:SetScript("OnEvent", function(_, event, ...)
        if event == "PET_BATTLE_OPENING_START" then
            self:OnBattleStart()
        elseif event == "PET_BATTLE_TURN_STARTED" then
            self:OnTurnStart()
        elseif event == "PET_BATTLE_ACTION_SELECTED" then
            self:OnActionSelected()
        elseif event == "PET_BATTLE_CLOSE" then
            self:OnBattleEnd()
        elseif event == "CHAT_MSG_PET_BATTLE_COMBAT_LOG" then
            self:OnCombatLog(..., event)
        end
    end)
end

-- ... (ToggleRecording and OnBattleStart remain same) ...

function recorder:OnCombatLog(msg)
    if not isRecording or not currentBattle then return end
    
    -- Ensure current turn exists (sometimes logs come before turn start event)
    if currentTurn == 0 then return end
    
    if not currentBattle.turns[currentTurn] then
        currentBattle.turns[currentTurn] = {
            turnNumber = currentTurn,
            enemyActions = {},
            logs = {}
        }
    end
    
    local turn = currentBattle.turns[currentTurn]
    if not turn.logs then turn.logs = {} end
    
    table.insert(turn.logs, msg)
end

function recorder:OnTurnStart()
    if not currentBattle then return end
    
    currentTurn = currentTurn + 1
    currentBattle.turns[currentTurn] = {
        turnNumber = currentTurn,
        enemyActions = {},
        logs = {}
    }
end

function recorder:OnActionSelected()
    if not currentBattle then return end
    -- We rely on chat logs now, but keeping this for timing if needed
end

function recorder:RecordEnemyAction()
    -- Deprecated in favor of chat logs, but keeping structure for now
end

function recorder:OnBattleEnd()
    if not currentBattle then return end
    
    -- Save recording
    local enemyName = currentBattle.enemyName
    
    if not PetWeaverEnemyRecordings[enemyName] then
        PetWeaverEnemyRecordings[enemyName] = {battles = {}}
    end
    
    table.insert(PetWeaverEnemyRecordings[enemyName].battles, currentBattle)
    
    print("|cFF00FF00Recorded battle vs " .. enemyName .. "|r (" .. currentTurn .. " turns)")
    print("Total recordings for this enemy: " .. #PetWeaverEnemyRecordings[enemyName].battles)
    
    currentBattle = nil
end

-- Export function
function recorder:ExportRecordings()
    if not PetWeaverEnemyRecordings or not next(PetWeaverEnemyRecordings) then
        print("|cFFFF0000No recordings to export|r")
        return
    end
    
    print("|cFFFFFF00Recorded Encounters:|r")
    for enemyName, data in pairs(PetWeaverEnemyRecordings) do
        print("  " .. enemyName .. ": " .. #data.battles .. " battles")
    end
    print("Data saved to SavedVariables/PetWeaver.lua")
end

-- Initialize on load
recorder:Initialize()
