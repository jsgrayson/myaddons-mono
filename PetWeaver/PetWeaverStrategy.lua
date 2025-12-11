local addonName, addon = ...
local UI = PetWeaverUI

-- Strategy Manager Module
UI.strategyManager = UI.strategyManager or {}
local StrategyManager = UI.strategyManager

-- Current strategy selection per encounter
StrategyManager.selectedStrategies = {}

---
--- Get all strategies for an encounter
---
function StrategyManager:GetStrategies(encounterName)
    -- Check enhanced DB first
    if PetWeaverEnhancedDB and PetWeaverEnhancedDB[encounterName] then
        local encounter = PetWeaverEnhancedDB[encounterName]
        if encounter.strategies then
            return encounter.strategies
        end
    end
    
    -- Fallback to standard DB (single strategy)
    if PetWeaverDB and PetWeaverDB[encounterName] then
        return {
            {
                name = "Default Strategy",
                tags = {},
                rating = "Unknown",
                pet1 = PetWeaverDB[encounterName].pet1,
                pet2 = PetWeaverDB[encounterName].pet2,
                pet3 = PetWeaverDB[encounterName].pet3,
                script = PetWeaverDB[encounterName].script
            }
        }
    end
    
    return {}
end

---
--- Get the currently selected strategy for an encounter
---
function StrategyManager:GetCurrentStrategy(encounterName)
    local strategies = self:GetStrategies(encounterName)
    if #strategies == 0 then return nil end
    
    -- Get selected index or default to 1
    local index = self.selectedStrategies[encounterName] or 1
    return strategies[index]
end

---
--- Select a specific strategy by index
---
function StrategyManager:SelectStrategy(encounterName, index)
    local strategies = self:GetStrategies(encounterName)
    if index >= 1 and index <= #strategies then
        self.selectedStrategies[encounterName] = index
        return true
    end
    return false
end

---
--- Get next strategy (cycle through alternatives)
---
function StrategyManager:NextStrategy(encounterName)
    local strategies = self:GetStrategies(encounterName)
    if #strategies <= 1 then return false end
    
    local current = self.selectedStrategies[encounterName] or 1
    local next = (current % #strategies) + 1
    self.selectedStrategies[encounterName] = next
    
    print(string.format("|cff00ff00PetWeaver:|r Switched to strategy %d/%d: %s", 
        next, #strategies, strategies[next].name))
    
    return true
end

---
--- Get previous strategy
---
function StrategyManager:PreviousStrategy(encounterName)
    local strategies = self:GetStrategies(encounterName)
    if #strategies <= 1 then return false end
    
    local current = self.selectedStrategies[encounterName] or 1
    local prev = current - 1
    if prev < 1 then prev = #strategies end
    self.selectedStrategies[encounterName] = prev
    
    print(string.format("|cff00ff00PetWeaver:|r Switched to strategy %d/%d: %s", 
        prev, #strategies, strategies[prev].name))
    
    return true
end

---
--- Get encounter metadata
---
function StrategyManager:GetEncounterMetadata(encounterName)
    if PetWeaverEnhancedDB and PetWeaverEnhancedDB[encounterName] then
        local encounter = PetWeaverEnhancedDB[encounterName]
        return {
            expansion = encounter.expansion,
            zone = encounter.zone,
            category = encounter.category,
            difficulty = encounter.difficulty
        }
    end
    
    -- Default values if no metadata
    return {
        expansion = "Unknown",
        zone = "Unknown",
        category = "Unknown",
        difficulty = "Unknown"
    }
end

---
--- Filter encounters by category
---
function StrategyManager:FilterByCategory(category)
    if not PetWeaverEnhancedDB then return {} end
    
    local results = {}
    for encounterName, data in pairs(PetWeaverEnhancedDB) do
        if data.category == category then
            table.insert(results, encounterName)
        end
    end
    return results
end

---
--- Filter encounters by expansion
---
function StrategyManager:FilterByExpansion(expansion)
    if not PetWeaverEnhancedDB then return {} end
    
    local results = {}
    for encounterName, data in pairs(PetWeaverEnhancedDB) do
        if data.expansion == expansion then
            table.insert(results, encounterName)
        end
    end
    return results
end

---
--- Filter encounters by difficulty
---
function StrategyManager:FilterByDifficulty(difficulty)
    if not PetWeaverEnhancedDB then return {} end
    
    local results = {}
    for encounterName, data in pairs(PetWeaverEnhancedDB) do
        if data.difficulty == difficulty then
            table.insert(results, encounterName)
        end
    end
    return results
end

---
--- Get strategy tags
---
function StrategyManager:GetStrategyTags(encounterName, strategyIndex)
    local strategies = self:GetStrategies(encounterName)
    if strategies[strategyIndex] then
        return strategies[strategyIndex].tags or {}
    end
    return {}
end

---
--- Check if strategy has specific tag
---
function StrategyManager:HasTag(encounterName, tag, strategyIndex)
    local tags = self:GetStrategyTags(encounterName, strategyIndex)
    for _, t in ipairs(tags) do
        if t == tag then return true end
    end
    return false
end
