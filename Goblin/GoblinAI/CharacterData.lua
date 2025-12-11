-- CharacterData.lua - Track character information automatically

GoblinAI.CharacterData = {}
local CharData = GoblinAI.CharacterData

function CharData:Update()
    local playerName = UnitName("player")
    local realmName = GetRealmName()
    local charKey = playerName .. "-" .. realmName
    
    -- Initialize character data
    if not GoblinAIDB.characters[charKey] then
        GoblinAIDB.characters[charKey] = {}
    end
    
    local char = GoblinAIDB.characters[charKey]
    
    -- Basic info
    char.name = playerName
    char.realm = realmName
    char.faction = UnitFactionGroup("player")
    char.level = UnitLevel("player")
    char.class = UnitClass("player")
    char.gold = GetMoney()
    char.lastUpdate = time()
    
    -- Professions
    char.professions = self:GetProfessions()
    
    -- Bank access
    char.hasBankAccess = IsPlayerInBankingRange()
    
    print("|cFF00FF00Goblin AI|r: Character data updated")
end

function CharData:GetProfessions()
    local profs = {}
    
    for i = 1, 2 do
        local name, _, rank, maxRank, _, _, skillLine = GetProfessionInfo(i)
        if name then
            profs[skillLine] = {
                name = name,
                rank = rank,
                maxRank = maxRank,
                skillLine = skillLine
            }
        end
    end
    
    return profs
end

function CharData:GetCurrentCharacter()
    local playerName = UnitName("player")
    local realmName = GetRealmName()
    local charKey = playerName .. "-" .. realmName
    return GoblinAIDB.characters[charKey]
end

function CharData:GetGoldFormatted()
    local gold = GetMoney()
    return GoblinAI:FormatGold(gold)
end
