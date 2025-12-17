-- tools/gen_policy_packs.lua
package.path = package.path .. ";./?.lua;./db/?.lua"

-- Mock global if running standalone
if not SkillWeaverDB then SkillWeaverDB = {} end

-- Simplified mock require for db/SpecRegistry
local SpecRegistry = require("db.SpecRegistry")

local function fileExists(path)
  local f = io.open(path, "r")
  if f then f:close(); return true end
  return false
end

local function readAll(path)
  local f = io.open(path, "r"); if not f then return nil end
  local s = f:read("*a"); f:close(); return s
end

local function writeFile(path, content)
  local f = assert(io.open(path, "w"))
  f:write(content)
  f:close()
end

local template = assert(readAll("policies/spec/_template.lua"), "Missing policies/spec/_template.lua")

local created = 0
for _, specs in pairs(SpecRegistry) do
  if type(specs) == "table" then
      for _, meta in pairs(specs) do
        local specKey = meta.key
        local outPathManual = "policies/spec/" .. specKey .. ".manual.lua"
        local outPathGen = "policies/spec/" .. specKey .. ".gen.lua"
        
        -- Create Manual if missing
        if not fileExists(outPathManual) then
          local header = ("-- policies/spec/%s.manual.lua\nlocal addonName, addonTable = ...\n"):format(specKey)
          local footer = ("\n\nif addonTable then\n  addonTable.PolicyPacksManual = addonTable.PolicyPacksManual or {}\n  addonTable.PolicyPacksManual[\"%s\"] = pack\nend\nreturn pack\n"):format(specKey)
          local body = template:gsub("local addonName, addonTable = ...%s+", ""):gsub("return pack", "")
          writeFile(outPathManual, header .. body .. footer)
          created = created + 1
          print("created: " .. outPathManual)
        end
        
        -- Create Gen if missing (normally compiler does this, but scaffold essentially acts as 'empty scrape')
        if not fileExists(outPathGen) then
          local header = ("-- policies/spec/%s.gen.lua\nlocal addonName, addonTable = ...\n"):format(specKey)
          local footer = ("\n\nif addonTable then\n  addonTable.PolicyPacksGen = addonTable.PolicyPacksGen or {}\n  addonTable.PolicyPacksGen[\"%s\"] = pack\nend\nreturn pack\n"):format(specKey)
          local body = "local pack = {}\n" -- Gen starts empty if scaffolding
          writeFile(outPathGen, header .. body .. footer)
           -- created = created + 1 -- count manual mainly
        end
      end
  end
end

print(("done. created %d policy packs."):format(created))
