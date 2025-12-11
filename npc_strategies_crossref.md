# NPC / Gimmick Fight Strategies – Ability Cross‑Reference

This document maps each special NPC encounter (the "PC strategies" you already have in `gimmick_fights.md`) to the **specific pet abilities** that can be used to counter the mechanic.  It is intended for the AI decision‑tree and for manual team‑building.

| Encounter (Tamer / ID) | Core Mechanic | Counter‑Ability(s) | Example Pet(s) |
|---|---|---|---|
| **Rocko – Needs a Shave** (98572) | Damage Immunity for 10 rounds, then dies | **Dodge** (avoid attacks), **Burrow** (hide for a turn), **Heal** (keep HP), **Decoy** (block damage), **Cleansing Rain** (reduce DoT duration) | *Murloc Tidehunter* (Dodge), *Murloc Tidehunter* (Burrow), *Murloc Tidehunter* (Heal) |
| **Gorespine** (Pet Dungeon) | Gore Stacks – DoT damage increases each round | **Shell Shield** (‑50% damage), **Decoy** (block one instance), **Heal** (recover), **Cleansing Rain** (reduce DoT duration) | *Murloc Tidehunter* (Shell Shield), *Murloc Tidehunter* (Decoy) |
| **Dah'da (Wrathion)** – Life Exchange | Swaps health percentages with target each turn | **High‑HP pet** (e.g., *Murloc Tidehunter* with 100 % HP), **Heal** to keep HP high, **Burst Damage** to kill before swap completes | *Murloc Tidehunter* (Heal), *Murloc Tidehunter* (High HP) |
| **The Impossible Boss** (Pet Dungeon) | Massive Team Healing every few turns | **Plague Touch** (‑50% healing received), **Cleansing Rain** (reduces DoT, also helps healing), **Burst Damage** (overwhelm before heal) | *Murloc Tidehunter* (Plague Touch) |
| **Seeker Zusshi** (Pandaria) | Shell Shield – 3‑round damage reduction | **Burst Damage** during shield downtime, **Stun/Root** to interrupt, **DoT** abilities (e.g., *Flame Breath*) to chip through | *Murloc Tidehunter* (Flame Breath) |
| **Morulu the Elder** (Pandaria) | Feed – Large self‑heal on its turn | **Stun** (prevent heal), **Burst Damage** before heal, **Decoy** (block heal if it deals damage) | *Murloc Tidehunter* (Stun) |
| **Flowing Pandaren Spirit – Tidal Wave** | +25 % Aquatic damage & water‑based healing | **Aquatic pets** (benefit), **Magic pets** (ignore positive boost), **Call Darkness** (negate healing) | *Murloc Tidehunter* (Aquatic) |
| **Burning Pandaren Spirit – Scorched Earth** | +25 % Elemental damage + 35 % Dragonkin DoT each round | **Elemental pets** (damage boost), **Heal** or **Shell Shield** to survive DoT, **Cleansing Rain** to reduce DoT duration | *Murloc Tidehunter* (Elemental) |
| **Whispering Pandaren Spirit – Call Darkness** | -50 % healing received, +10 % hit chance (actually -10 % accuracy) | **High burst damage**, **Undead pets** (benefit from Darkness), **Plague Touch** (reduce healing) | *Murloc Tidehunter* (Undead) |
| **Thundering Pandaren Spirit – Call Lightning** | +25 % Mechanical/Flying damage + 30 % Elemental DoT each round | **Mechanical/Flying pets** (damage boost), **Decoy** (block DoT), **Heal** to survive DoT | *Murloc Tidehunter* (Mechanical) |
| **Shadowlands – Aura of Undeath** | All pets count as Undead | **Humanoid pets** (Undead is weak to Humanoid), **Plague Touch** (reduce healing) | *Murloc Tidehunter* (Humanoid) |

**How to use this table**
- The AI should look up the encounter’s mechanic and select a pet that possesses one of the listed counter abilities.
- When multiple abilities are viable, prioritize those with the **lowest cooldown** or **highest survivability**.
- For stalling encounters (Rocko, Gorespine), combine **Dodge/Burrow** with **Heal** to extend survivability.

*Note*: This cross‑reference assumes the standard WoW pet ability set. If you have custom abilities, add rows accordingly.
