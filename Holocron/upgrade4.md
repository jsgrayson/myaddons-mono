Based on \`SkillWeaver\_Project\_Spec.pdf\` and \`03\_Holocron\_Features.md\`, here are the "Killer Features" for the remaining two projects, designed for \*\*Single-Player Dominance\*\*.

\#\#\# \*\*Project: SkillWeaver (Combat Engine)\*\*  
\*Goal: Flawless, logic-driven rotation execution.\*

1\.  \*\*"The Shapeshifter" (Context-Aware Rotation)\*\*  
    \* \*\*Concept:\*\* Standard macros fail because they don't know \*what\* you are fighting.  
    \* \*\*Function:\*\* The addon scans nameplates in real-time.  
        \* \*1 Target:\* Executes the Single-Target priority list.  
        \* \*3+ Targets:\* Instantly hot-swaps the logic to the AoE / Cleave priority list without you changing keys.  
        \* \*Target \< 20% HP:\* Automatically prioritizes "Execute" abilities over resource builders.

2\.  \*\*"The Oracle" (Resource Lookahead)\*\*  
    \* \*\*Concept:\*\* Most rotation addons are reactive (e.g., "I have 5 Combo Points \-\> Spend"). This leads to waste.  
    \* \*\*Function:\*\* The engine calculates resource generation \*2 GCDs into the future\*.  
        \* \*Scenario:\* You are at 3 Combo Points. Your next move generates 2\.  
        \* \*Action:\* The Oracle forces a spender \*now\* (early) to prevent over-capping resources in the next second, mimicking top-tier human foresight.

3\.  \*\*"The Auditor" (Death Recap & Adjustment)\*\*  
    \* \*\*Concept:\*\* Learning from failure.  
    \* \*\*Function:\*\* If you die, the Desktop Engine parses the combat log. It identifies the exact timestamp you took lethal damage and checks if a defensive cooldown was available but unused.  
    \* \*Correction:\* It effectively "patches" the macro logic for that specific dungeon/boss, inserting a forced Defensive Cast at that specific timing trigger for the next attempt.

4\.  \*\*"The Sandbox" (Local SimC Integration)\*\*  
    \* \*\*Concept:\*\* Proving your rotation is mathematically perfect for \*your\* gear.  
    \* \*\*Function:\*\* The Desktop App runs a headless SimulationCraft instance locally. It generates thousands of permutations of your macro sequence (e.g., "Cast \*Bloodthirst\* before \*Rampage\* vs after") and finds the specific sequence that yields the highest theoretical DPS for your current item level.

\---

\#\#\# \*\*Project: Holocron (Logistics Core)\*\*  
\*Goal: Managing your "Army of Alts" as one giant inventory.\*

1\.  \*\*"The Quartermaster" (Predictive Restocking)\*\*  
    \* \*\*Concept:\*\* You should never realize you are out of potions \*during\* a raid.  
    \* \*\*Function:\*\* You define "Par" levels for every character (e.g., "Main needs 20 Flasks, Alt needs 5").  
    \* \*\*Trigger:\*\* When you log out of your Main, Holocron scans the inventory. If Flasks \< 20, it instantly generates a "Job" for your Bank Alt. Next time you log into the Bank Alt, the mailbox is pre-addressed to your Main with the exact number of Flasks needed to hit Par.

2\.  \*\*"The Fabricator" (Complex Supply Chains)\*\*  
    \* \*\*Concept:\*\* Automating multi-alt crafting (e.g., Mining on Alt A \-\> Smelting on Alt B \-\> Engineering on Main).  
    \* \*\*Function:\*\* You select the item you want to craft (e.g., "Mecha-Mogul Mk2"). Holocron calculates the raw materials needed across \*all\* alts.  
    \* \*\*Directives:\*\* It generates a "Step-by-Step" manifest.  
        \* \*Step 1:\* Log into Miner. (Arrow points to Ore nodes).  
        \* \*Step 2:\* Log into Alchemist. (Button appears: "Transmute Living Steel").  
        \* \*Step 3:\* Mail to Engineer.

3\.  \*\*"The Vacuum" (Inventory Defragmentation)\*\*  
    \* \*\*Concept:\*\* Your materials are scattered across 12 characters, making them unusable.  
    \* \*\*Function:\*\* One button press ("Defrag"). Holocron scans every bag and bank on every character. It identifies partial stacks (e.g., 50 Cloth on Alt A, 100 Cloth on Alt B).  
    \* \*\*Action:\*\* It creates "Mail Jobs" to send all partial stacks to a designated "Warehouse Alt," consolidating them into full stacks (200) automatically.

4\.  \*\*"The Museum" (Shadow Collection)\*\*  
    \* \*\*Concept:\*\* Knowing what you have without logging in.  
    \* \*\*Function:\*\* The Desktop App maintains a local SQL database of every item, pet, and currency on every character.  
    \* \*\*Search:\*\* You type "Thunderfury" into the Web Portal. It tells you: "Alt \#4 has the Right Binding in the Bank. Main has the Left Binding in Void Storage." No need to cycle logins to find lost items.  
