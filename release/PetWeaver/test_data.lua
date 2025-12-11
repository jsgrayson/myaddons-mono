#!/usr/bin/env lua

-- Simple test to verify PetWeaver data files are syntactically correct
print("Testing PetWeaver data files...")

-- Load teams_data.lua
dofile("teams_data.lua")
if PetWeaver_DefaultTeams then
    print("✓ teams_data.lua loaded successfully")
    print("  Found " .. #PetWeaver_DefaultTeams .. " default teams")
    for i, team in ipairs(PetWeaver_DefaultTeams) do
        print("    - " .. (team.name or "Unnamed") .. " (" .. #team.pets .. " pets, " .. (#team.script or 0) .. " script steps)")
    end
else
    print("✗ teams_data.lua failed - PetWeaver_DefaultTeams is nil")
end

print()

-- Load encounters_data.lua
dofile("encounters_data.lua")
if PetWeaver_Encounters then
    print("✓ encounters_data.lua loaded successfully")
    local count = 0
    for name, _ in pairs(PetWeaver_Encounters) do
        count = count + 1
    end
    print("  Found " .. count .. " encounters")
    for name, encounter in pairs(PetWeaver_Encounters) do
        print("    - " .. (encounter.displayName or name) .. " (" .. #encounter.pets .. " pets)")
    end
else
    print("✗ encounters_data.lua failed - PetWeaver_Encounters is nil")
end

print()
print("Data file validation complete!")
