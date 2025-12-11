Based on the architecture defined in \`Petweaver ideas.md\`, here are "Killer Features" for each of the four key pillars of your project: \*\*The Addon (Executioner)\*\*, \*\*The Desktop App (Brain)\*\*, \*\*The Web Portal (War Room)\*\*, and \*\*The AI Core (Solver)\*\*.

\#\#\# \*\*1. The Executioner (WoW Addon)\*\*  
\*Focused on invisible, context-aware input.\*

\* \*\*"The Co-Pilot" (Audio feedback):\*\* Since you are "watching Netflix on Monitor 2", you shouldn't have to look at the screen at all. The addon uses \`PlaySoundFile\` to give specific auditory cues:  
    \* \*Positive Chime:\* "Battle Won" or "Target Reached."  
    \* \*Negative Buzz:\* "Bag Full," "Out of Bandages," or "Rare Breed Spawned."  
    \* \*Voice:\* "Swap Now" (if manual intervention is required).  
\* \*\*"Panic Branches":\*\* Standard scripts fail if a 5% crit kills your pet early. The Executioner pre-loads a "Backup Script" into memory. If \`self.pet(1).dead\` triggers unexpectedly, it instantly swaps to the backup logic flow without you pressing a different key.

\#\#\# \*\*2. The Brain (Desktop Engine)\*\*  
\*Focused on heavy computation and logistics.\*

\* \*\*"The Time Machine" (Battle Replay):\*\* When a "100% Win Rate" team loses, you need to know why. The Engine records every combat log line from the failed battle. You can scrub through the fight turn-by-turn in the Desktop App to see exactly where the RNG deviated or where the logic broke, allowing for pixel-perfect debugging.  
\* \*\*"The Simulacrum" (Headless Client):\*\* Instead of just simulating math, the Engine runs a lightweight, text-only instance of the battle logic locally. It allows you to "Play" a battle manually in the Desktop App to test a strategy 1,000 times in one second before you ever log into WoW.

\#\#\# \*\*3. The War Room (Web Portal)\*\*  
\*Focused on visualization and planning.\*

\* \*\*"The Liquidity Heatmap" (Goblin Feature):\*\* A visual grid of your pet collection colored by \*\*Sale Rate\*\* (from TSM).  
    \* \*Red:\* High Value, but sells once a year (Long-term hold).  
    \* \*Green:\* Low Value, sells hourly (Quick cash).  
    \* \*Action:\* Drag a box around the "Green" pets to auto-generate a "Leveling Playlist" for fast liquid gold.  
\* \*\*"The Gene Pool" (Visualizer):\*\* A real-time graph showing the Genetic Algorithm at work. You watch dots (teams) moving towards a "Victory" line. You can manually click a "promising" team to save it from being mutated, acting as the "Intelligent Designer" guiding the evolution.

\#\#\# \*\*4. The AI Core (Data & Solver)\*\*  
\*Focused on mathematical perfection.\*

\* \*\*"RNG Proofing" (Monte Carlo Stress Test):\*\* A team isn't "Solved" until it survives the \*\*Worst Case Scenario\*\*. The AI runs 10,000 simulations where the enemy crits \*every single turn\* and your pets miss \*every 90% hit\*. If a team can still win (or draw) in that mathematical nightmare, it gets the "God Tier" tag.  
\* \*\*"The Bounty Hunter" (Collection Optimization):\*\* The AI scans every uncollected pet in the game and calculates a "Utility Score."  
    \* \*Example:\* "If you capture a \*\*Flayer Youngling (S/S)\*\*, your win rate against \*Pandaria Tamers\* increases by 14%."  
    \* It builds a prioritized "Hunting List" based on strategic value, not just completionism.  
