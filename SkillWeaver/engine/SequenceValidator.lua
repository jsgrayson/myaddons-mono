-- SkillWeaver Sequence Validator (Robust)
-- Validates Structural Integrity and Condition Safety (Tier A + Tier B).

local Validator = {}

local allowedKeywords = {
  ["and"]=true, ["or"]=true, ["not"]=true, ["true"]=true, ["false"]=true,
}

local function parensBalanced(s)
  local n = 0
  for i=1,#s do
    local c = s:sub(i,i)
    if c == "(" then n = n + 1 end
    if c == ")" then n = n - 1; if n < 0 then return false end end
  end
  return n == 0
end

local function looksLikeCommand(cmd)
  return type(cmd) == "string" and (cmd:find("^/cast") or cmd:find("^/pet") or cmd:find("^/use") or cmd:find("^/click"))
end

-- minimal token check: flags weird characters early
local function conditionCharsOK(s)
  -- allow letters, numbers, spaces, underscores, colons, quotes, dots, commas, brackets, math ops
  return not s:find("[^%w%s_:%[%]%(%)'\"%.-,<>!=+*/]")
end

-- Validates a Normalized Sequence (Schema: meta + blocks.st/aoe)
function Validator:ValidateNormalized(seq)
  local errors, warnings = {}, {}

  if type(seq) ~= "table" or type(seq.meta) ~= "table" or type(seq.blocks) ~= "table" then
    table.insert(errors, "Sequence is not normalized (missing meta/blocks).")
    return errors, warnings
  end

  for _, blockName in ipairs({"st","aoe"}) do
    local steps = seq.blocks[blockName]
    if steps and type(steps) ~= "table" then
      table.insert(errors, ("Block '%s' is not a table."):format(blockName))
    else
      for i, step in ipairs(steps or {}) do
        if type(step) ~= "table" then
          table.insert(errors, ("%s[%d] is not a table."):format(blockName, i))
        else
          if not looksLikeCommand(step.command) then
             -- Warn rather than error for now, as custom actions might exist
            table.insert(warnings, ("%s[%d] unusual command: %s"):format(blockName, i, tostring(step.command)))
          end

          if step.conditions ~= nil then
            if type(step.conditions) ~= "string" or step.conditions == "" then
              -- Empty conditions are fine (treated as 'always'), but non-string is bad
              if step.conditions ~= nil and step.conditions ~= "" then
                 table.insert(errors, ("%s[%d] conditions must be string."):format(blockName, i))
              end
            else
              if not conditionCharsOK(step.conditions) then
                table.insert(errors, ("%s[%d] conditions contains unsupported characters."):format(blockName, i))
              end
              if not parensBalanced(step.conditions) then
                table.insert(errors, ("%s[%d] conditions parentheses not balanced."):format(blockName, i))
              end
              -- warn on mixed enemy keys (you use both enemies + active_enemies + enemies_nearby)
              if step.conditions:find("enemies") and step.conditions:find("active_enemies") then
                table.insert(warnings, ("%s[%d] mixes enemies and active_enemies; normalize one."):format(blockName, i))
              end
            end
          end
        end
      end
    end
  end

  return errors, warnings
end

return Validator
