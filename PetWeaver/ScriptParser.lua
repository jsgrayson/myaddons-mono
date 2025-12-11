-- ScriptParser.lua
-- Parses Xu-Fu strategy scripts into executable commands

local _, addon = ...
addon.ScriptParser = {}
local Parser = addon.ScriptParser

-- Parse a single command line
function Parser:ParseLine(line)
    if not line or line == "" then return nil end
    
    -- Remove whitespace
    line = strtrim(line)
    
    -- Skip comments
    if line:match("^%-%-") then return nil end
    
    -- Parse use() command
    local abilityName, abilityID, condition = line:match("use%(([^:]+):(%d+)%)%s*(.*)") 
    if abilityName then
        return {
            type = "use",
            ability = {
                name = abilityName,
                id = tonumber(abilityID)
            },
            condition = condition ~= "" and condition or nil
        }
    end
    
    -- Parse change() command
    local target, condition = line:match("change%(([^%)]+)%)%s*(.*)")
    if target then
        return {
            type = "change",
            target = target, -- "#1", "#2", "#3", "next", etc.
            condition = condition ~= "" and condition or nil
        }
    end
    
    -- Parse standby command
    local condition = line:match("standby%s*(.*)")
    if line:match("^standby") then
        return {
            type = "standby",
            condition = condition ~= "" and condition or nil
        }
    end
    
    -- Parse if/endif blocks
    if line:match("^if%s+") then
        local condition = line:match("^if%s+(.+)")
        return {
            type = "if",
            condition = condition
        }
    end
    
    if line == "endif" then
        return {
            type = "endif"
        }
    end
    
    -- Unknown command
    return nil
end

-- Parse full script into command list
function Parser:ParseScript(scriptText)
    if not scriptText or scriptText == "" then
        return {}
    end
    
    local commands = {}
    local lines = {strsplit("\n", scriptText)}
    
    for _, line in ipairs(lines) do
        local cmd = self:ParseLine(line)
        if cmd then
            table.insert(commands, cmd)
        end
    end
    
    return commands
end

-- Evaluate a condition string
function Parser:EvaluateCondition(conditionStr, context)
    if not conditionStr or conditionStr == "" then
        return true
    end
    
    -- Remove brackets if present
    conditionStr = conditionStr:gsub("^%[", ""):gsub("%]$", "")
    
    -- Parse round= conditions
    local roundNum = conditionStr:match("round=(%d+)")
    if roundNum then
        return context.round == tonumber(roundNum)
    end
    
    -- Parse round> conditions
    local roundGT = conditionStr:match("round>(%d+)")
    if roundGT then
        return context.round > tonumber(roundGT)
    end
    
    -- Parse round~ (modulo) conditions
    local roundMod = conditionStr:match("round~(%d+)")
    if roundMod then
        for num in roundMod:gmatch("%d+") do
            if context.round == tonumber(num) then
                return true
            end
        end
        return false
    end
    
    -- Parse enemy.hp conditions
    local enemyHP = conditionStr:match("enemy%.hp<(%d+)")
    if enemyHP and context.enemy then
        return context.enemy.health < tonumber(enemyHP)
    end
    
    -- Parse self.dead
    if conditionStr:match("self%.dead") then
        return context.activePet and context.activePet.health <= 0
    end
    
    -- Parse self(#N).dead
    local petSlot = conditionStr:match("self%(#(%d+)%)%.dead")
    if petSlot and context.team then
        local pet = context.team[tonumber(petSlot)]
        return pet and pet.health <= 0
    end
    
    -- Parse enemy.aura(...).exists
    local auraName = conditionStr:match("enemy%.aura%(([^%)]+)%)%.exists")
    if auraName and context.enemy and context.enemy.auras then
        for _, aura in ipairs(context.enemy.auras) do
            if aura.name == auraName then
                return true
            end
        end
        return false
    end
    
    -- Parse !enemy.aura(...).exists (negation)
    if conditionStr:match("^!") then
        local innerCondition = conditionStr:sub(2)
        return not self:EvaluateCondition(innerCondition, context)
    end
    
    -- Default: condition not recognized, return true to be safe
    return true
end
