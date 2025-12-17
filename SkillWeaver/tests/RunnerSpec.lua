-- tests/RunnerSpec.lua
return {
  {
    name = "Frost KM prefers Obliterate over Frost Strike",
    seq = {
      meta = { exec="Priority" },
      blocks = {
        st = {
          { command="/cast Frost Strike", conditions="true" },
          { command="/cast Obliterate",   conditions="true" },
        },
        aoe = {}
      }
    },
    context = {
      activeEnemies = 1,
      aoeThreshold = 3,
      procs = { ["Killing Machine"]=true },
      __sectionName = "core"
    },
    expect = "Obliterate"
  },

  {
    name = "Blood Boil charge urgency bubbles up",
    seq = {
      meta = { exec="Priority" },
      blocks = {
        st = {
          { command="/cast Heart Strike", conditions="true" },
          { command="/cast Blood Boil",   conditions="true" },
        },
        aoe = {}
      }
    },
    context = { 
        activeEnemies=3, aoeThreshold=3, __sectionName="core",
        -- We need to mock ChargeBudget inside Sim/run.lua if we want this to really work
        -- or reliance on Engine's charge logic
    },
    expect = "Blood Boil" 
    -- Note: This test implies Blood Boil is at 2 charges. 
    -- We need to mock GetSpellCharges in Sim for "Blood Boil" to allow this.
    -- For now, this is a placeholder spec.
  },
  
  {
    name = "Simple Sequential Step",
    seq = {
        meta = { exec="Sequential" },
        blocks = {
            st = {
                { command="/cast Icy Touch" },
                { command="/cast Plague Strike" }
            }
        }
    },
    context = { activeEnemies=1, spec={currentStep=1}, __sectionName="core" },
    expect = "Icy Touch"
  }
}
