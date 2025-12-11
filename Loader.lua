-- SkillWeaver file loader wrapper
function SkillWeaver.Loader(path)
    local addonName = ...
    local env = setmetatable({}, { __index = _G })
    local file = addonName .. "/" .. path .. ".lua"
    return loadfile(file, "bt", env)()
end
