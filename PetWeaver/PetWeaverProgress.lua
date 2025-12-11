local addonName, addon = ...
local UI = PetWeaverUI

-- Favorites & Progress Tracker Module
UI.progressTracker = UI.progressTracker or {}
local Tracker = UI.progressTracker

-- Saved data (persisted across sessions)
PetWeaverProgressDB = PetWeaverProgressDB or {
    favorites = {},      -- {encounterName = true}
    completed = {},      -- {encounterName = {count, lastCompleted}}
    notes = {},          -- {encounterName = "user notes"}
    statistics = {
        totalBattles = 0,
        totalWins = 0,
        totalLosses = 0,
        timeSpent = 0,
        encounterStats = {}  -- {encounterName = {wins, losses, avgTime}}
    }
}

---
--- FAVORITES SYSTEM
---

function Tracker:ToggleFavorite(encounterName)
    if PetWeaverProgressDB.favorites[encounterName] then
        PetWeaverProgressDB.favorites[encounterName] = nil
        print("|cff00ff00PetWeaver:|r Removed " .. encounterName .. " from favorites")
        return false
    else
        PetWeaverProgressDB.favorites[encounterName] = true
        print("|cff00ff00PetWeaver:|r Added " .. encounterName .. " to favorites")
        return true
    end
end

function Tracker:IsFavorite(encounterName)
    return PetWeaverProgressDB.favorites[encounterName] or false
end

function Tracker:GetFavorites()
    local favorites = {}
    for encounterName, _ in pairs(PetWeaverProgressDB.favorites) do
        table.insert(favorites, encounterName)
    end
    return favorites
end

---
--- PROGRESS TRACKING
---

function Tracker:MarkCompleted(encounterName)
    if not PetWeaverProgressDB.completed[encounterName] then
        PetWeaverProgressDB.completed[encounterName] = {count = 0, lastCompleted = 0}
    end
    
    PetWeaverProgressDB.completed[encounterName].count = PetWeaverProgressDB.completed[encounterName].count + 1
    PetWeaverProgressDB.completed[encounterName].lastCompleted = time()
    
    print(string.format("|cff00ff00PetWeaver:|r %s marked complete (%dx)", 
        encounterName, PetWeaverProgressDB.completed[encounterName].count))
end

function Tracker:IsCompleted(encounterName)
    return PetWeaverProgressDB.completed[encounterName] ~= nil
end

function Tracker:GetCompletionCount(encounterName)
    if PetWeaverProgressDB.completed[encounterName] then
        return PetWeaverProgressDB.completed[encounterName].count
    end
    return 0
end

function Tracker:ClearCompletion(encounterName)
    PetWeaverProgressDB.completed[encounterName] = nil
    print("|cff00ff00PetWeaver:|r Cleared completion for " .. encounterName)
end

---
--- PERSONAL NOTES
---

function Tracker:SetNote(encounterName, note)
    if note and note ~= "" then
        PetWeaverProgressDB.notes[encounterName] = note
        print("|cff00ff00PetWeaver:|r Note saved for " .. encounterName)
    else
        PetWeaverProgressDB.notes[encounterName] = nil
        print("|cff00ff00PetWeaver:|r Note cleared for " .. encounterName)
    end
end

function Tracker:GetNote(encounterName)
    return PetWeaverProgressDB.notes[encounterName] or ""
end

---
--- BATTLE STATISTICS
---

function Tracker:RecordBattle(encounterName, won, duration)
    local stats = PetWeaverProgressDB.statistics
    
    -- Global stats
    stats.totalBattles = stats.totalBattles + 1
    if won then
        stats.totalWins = stats.totalWins + 1
    else
        stats.totalLosses = stats.totalLosses + 1
    end
    stats.timeSpent = stats.timeSpent + (duration or 0)
    
    -- Per-encounter stats
    if not stats.encounterStats[encounterName] then
        stats.encounterStats[encounterName] = {
            wins = 0,
            losses = 0,
            totalTime = 0,
            battles = 0
        }
    end
    
    local encounterStats = stats.encounterStats[encounterName]
    encounterStats.battles = encounterStats.battles + 1
    if won then
        encounterStats.wins = encounterStats.wins + 1
    else
        encounterStats.losses = encounterStats.losses + 1
    end
    encounterStats.totalTime = encounterStats.totalTime + (duration or 0)
end

function Tracker:GetGlobalStats()
    local stats = PetWeaverProgressDB.statistics
    local winRate = stats.totalBattles > 0 and (stats.totalWins / stats.totalBattles * 100) or 0
    local avgTime = stats.totalBattles > 0 and (stats.timeSpent / stats.totalBattles) or 0
    
    return {
        totalBattles = stats.totalBattles,
        totalWins = stats.totalWins,
        totalLosses = stats.totalLosses,
        winRate = winRate,
        timeSpent = stats.timeSpent,
        avgTime = avgTime
    }
end

function Tracker:GetEncounterStats(encounterName)
    local encounterStats = PetWeaverProgressDB.statistics.encounterStats[encounterName]
    if not encounterStats then
        return {wins = 0, losses = 0, battles = 0, winRate = 0, avgTime = 0}
    end
    
    local winRate = encounterStats.battles > 0 and (encounterStats.wins / encounterStats.battles * 100) or 0
    local avgTime = encounterStats.battles > 0 and (encounterStats.totalTime / encounterStats.battles) or 0
    
    return {
        wins = encounterStats.wins,
        losses = encounterStats.losses,
        battles = encounterStats.battles,
        winRate = winRate,
        avgTime = avgTime
    }
end

---
--- UTILITY
---

function Tracker:ExportProgress()
    print("|cff00ff00PetWeaver - Progress Report:|r")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    local globalStats = self:GetGlobalStats()
    print(string.format("Total Battles: %d (W:%d L:%d)", 
        globalStats.totalBattles, globalStats.totalWins, globalStats.totalLosses))
    print(string.format("Win Rate: %.1f%%", globalStats.winRate))
    print(string.format("Total Time: %.1f min", globalStats.timeSpent / 60))
    
    print("\nFavorites: " .. #self:GetFavorites())
    
    local completedCount = 0
    for _ in pairs(PetWeaverProgressDB.completed) do
        completedCount = completedCount + 1
    end
    print("Completed Encounters: " .. completedCount)
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
end

function Tracker:ResetAllProgress()
    PetWeaverProgressDB = {
        favorites = {},
        completed = {},
        notes = {},
        statistics = {
            totalBattles = 0,
            totalWins = 0,
            totalLosses = 0,
            timeSpent = 0,
            encounterStats = {}
        }
    }
    print("|cff00ff00PetWeaver:|r All progress reset")
end
