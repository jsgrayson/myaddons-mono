-- BattleEngine.lua
-- Executes pet battle strategies automatically

local _, addon = ...
addon.BattleEngine = {}
local Engine = addon.BattleEngine
local Parser = addon.ScriptParser

-- State
Engine.active = false
Engine.currentTeam = nil
Engine.currentScript = nil
Engine.commands = {}
Engine.commandIndex = 1
Engine.round = 0
Engine.battleContext = {}

-- Initialize battle
function Engine:StartBattle(team)
    if not team or not team.script then
        print("|cffff0000PetWeaver:|r No valid team/script provided")
        return false
    end
    
    self.active = true
    self.currentTeam = team
    self.currentScript = team.script
    self.commands = Parser:ParseScript(team.script)
    self.commandIndex = 1
    self.round = 0
    
    print("|cff00ff00PetWeaver:|r Battle started with", #self.commands, "commands")
    print("|cff00ff00PetWeaver:|r Team:", team.name)
    
    return true
end

-- Stop battle
function Engine:StopBattle()
    self.active = false
    self.currentTeam = nil
    self.currentScript = nil
    self.commands = {}
    self.commandIndex = 1
    self.round = 0
    self.battleContext = {}
end

-- Update battle context with current state
function Engine:UpdateContext()
    if not C_PetBattles or not C_PetBattles.IsInBattle() then
        return
    end
    
    local ctx = {}
    
    -- Round info
    ctx.round = C_PetBattles.GetTurn() or 0
    
    -- Active pet
    local activePetSlot = C_PetBattles.GetActivePet(Enum.BattlePetOwner.Ally)
    if activePetSlot then
        ctx.activePet = {
            slot = activePetSlot,
            health = C_PetBattles.GetHealth(Enum.BattlePetOwner.Ally, activePetSlot),
            maxHealth = C_PetBattles.GetMaxHealth(Enum.BattlePetOwner.Ally, activePetSlot),
            level = C_PetBattles.GetLevel(Enum.BattlePetOwner.Ally, activePetSlot)
        }
    end
    
    -- Enemy active pet
    local enemySlot = C_PetBattles.GetActivePet(Enum.BattlePetOwner.Enemy)
    if enemySlot then
        ctx.enemy = {
            slot = enemySlot,
            health = C_PetBattles.GetHealth(Enum.BattlePetOwner.Enemy, enemySlot),
            maxHealth = C_PetBattles.GetMaxHealth(Enum.BattlePetOwner.Enemy, enemySlot),
            auras = {} -- TODO: Parse auras
        }
    end
    
    -- Team state
    ctx.team = {}
    for i = 1, C_PetBattles.GetNumPets(Enum.BattlePetOwner.Ally) do
        ctx.team[i] = {
            health = C_PetBattles.GetHealth(Enum.BattlePetOwner.Ally, i),
            maxHealth = C_PetBattles.GetMaxHealth(Enum.BattlePetOwner.Ally, i),
            level = C_PetBattles.GetLevel(Enum.BattlePetOwner.Ally, i)
        }
    end
    
    self.battleContext = ctx
    self.round = ctx.round
    
    return ctx
end

-- Execute next command
function Engine:ExecuteNextCommand()
    if not self.active or not C_PetBattles.IsInBattle() then
        return
    end
    
    -- Update context
    local ctx = self:UpdateContext()
    
    -- Find next executable command
    while self.commandIndex <= #self.commands do
        local cmd = self.commands[self.commandIndex]
        
        -- Check condition
        if not cmd.condition or Parser:EvaluateCondition(cmd.condition, ctx) then
            -- Execute command
            local success = self:ExecuteCommand(cmd, ctx)
            if success then
                self.commandIndex = self.commandIndex + 1
                return true
            end
        end
        
        self.commandIndex = self.commandIndex + 1
    end
    
    -- No more commands - use default ability
    self:UseDefaultAbility()
    self.commandIndex = 1 -- Reset for next round
    
    return false
end

-- Execute a single command
function Engine:ExecuteCommand(cmd, ctx)
    if cmd.type == "use" then
        return self:UseAbility(cmd.ability, ctx)
    elseif cmd.type == "change" then
        return self:ChangePet(cmd.target, ctx)
    elseif cmd.type == "standby" then
        return self:Standby()
    elseif cmd.type == "if" then
        -- Handle if blocks (simple version - just evaluate condition)
        return true
    elseif cmd.type == "endif" then
        return true
    end
    
    return false
end

-- Use an ability
function Engine:UseAbility(ability, ctx)
    if not ability or not ability.id then
        return false
    end
    
    -- Find ability slot by ID
    for slot = 1, C_PetBattles.GetNumAbilities(Enum.BattlePetOwner.Ally, ctx.activePet.slot) do
        local abilityID = C_PetBattles.GetAbilityInfo(Enum.BattlePetOwner.Ally, ctx.activePet.slot, slot)
        
        if abilityID == ability.id then
            -- Check if ability is usable
            local usable = C_PetBattles.GetAbilityState(Enum.BattlePetOwner.Ally, ctx.activePet.slot, slot)
            
            if usable then
                print("|cff00ff00PetWeaver:|r Using", ability.name)
                C_PetBattles.UseAbility(slot)
                return true
            else
                print("|cffff00 00PetWeaver:|r", ability.name, "on cooldown or locked")
                return false
            end
        end
    end
    
    print("|cffff0000PetWeaver:|r Ability not found:", ability.name, ability.id)
    return false
end

-- Change to a different pet
function Engine:ChangePet(target, ctx)
    local targetSlot = nil
    
    if target == "next" then
        -- Switch to next alive pet
        for i = 1, 3 do
            if i ~= ctx.activePet.slot and ctx.team[i] and ctx.team[i].health > 0 then
                targetSlot = i
                break
            end
        end
    elseif target:match("^#(%d)$") then
        -- Specific slot
        targetSlot = tonumber(target:match("^#(%d)$"))
    end
    
    if targetSlot and targetSlot ~= ctx.activePet.slot then
        print("|cff00ff00PetWeaver:|r Swapping to pet", targetSlot)
        C_PetBattles.ChangePet(targetSlot)
        return true
    end
    
    return false
end

-- Pass turn
function Engine:Standby()
    print("|cff00ff00PetWeaver:|r Passing turn")
    C_PetBattles.SkipTurn()
    return true
end

-- Use first available ability as fallback
function Engine:UseDefaultAbility()
    local ctx = self:UpdateContext()
    
    if not ctx.activePet then return end
    
    for slot = 1, C_PetBattles.GetNumAbilities(Enum.BattlePetOwner.Ally, ctx.activePet.slot) do
        local usable = C_PetBattles.GetAbilityState(Enum.BattlePetOwner.Ally, ctx.activePet.slot, slot)
        if usable then
            print("|cff888888PetWeaver:|r Using default ability (slot", slot, ")")
            C_PetBattles.UseAbility(slot)
            return
        end
    end
end

-- Check if auto-battle is enabled
function Engine:IsEnabled()
    return PetWeaverDB and PetWeaverDB.settings and PetWeaverDB.settings.autoBattle
end
