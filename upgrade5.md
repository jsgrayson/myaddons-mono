To round out the ecosystem, here are the \*\*"Quality of Life"\*\* and \*\*"Infrastructure"\*\* features found in your design documents. These aren't about raw power, but about making the system feel alive and seamless.

\#\#\# \*\*1. "Boredom Mode" (The Navigator)\*\*  
\*Found in Holocron\*  
When you don't know what to do, the system tells you.  
\* \*\*The Hitlist:\*\* It queries your database for "Missing Collections" (Mounts, Pets, Transmog) that are available in instances where you are \*not\* currently locked out.  
\* \*\*Smart Filters:\*\* You toggle \`\[Short Dungeons Only\]\` or \`\[High Drop Rate\]\`.  
\* \*\*Output:\*\* It generates a prioritized itinerary:  
    \* \*Target:\* "Invincible's Reins"  
    \* \*Location:\* "Icecrown Citadel (25H)"  
    \* \*Status:\* "Available on 8 Alts."

\#\#\# \*\*2. "The Vault Visualizer" (Weekly Progress)\*\*  
\*Found in Holocron\*  
Managing the Great Vault across an army of alts is a headache.  
\* \*\*The Grid:\*\* A dashboard overlay showing a matrix of your characters vs. their Vault Slots (Raid, Mythic+, PvP).  
\* \*\*Optimization Logic:\*\* It highlights "Low Hanging Fruit."  
    \* \*Example:\* "Alt \#4 only needs \*\*one more\*\* M+ dungeon to unlock a second loot choice."  
    \* \*Action:\* It queues a job for SkillWeaver to load the "Mythic+" rotation profile for that alt.

\#\#\# \*\*3. "Visual Tactician" (Drag-and-Drop Logic)\*\*  
\*Found in PetWeaver/Rematch Ideas\*  
Moving away from writing code to building logic blocks.  
\* \*\*Scratch-like Interface:\*\* Instead of writing Lua code like \`if self.hp \< 50\`, you use a visual editor.  
    \* \*Action:\* Drag a \*\*"Condition"\*\* block (\`Health \< 50%\`) \-\> Snap an \*\*"Action"\*\* block (\`Cast Explode\`) inside it.  
\* \*\*Coach Mode:\*\* In-game, instead of just auto-playing, the addon highlights the \*suggested\* button and displays a tooltip explaining \*why\* the logic chose that move (e.g., "Blocking incoming Nuke").

\#\#\# \*\*4. "The Black Box" (Optical Communication)\*\*  
\*Found in PetWeaver Design\*  
A clever way to bypass Lua limitations for "Headless" operation.  
\* \*\*The Pixel:\*\* The addon renders a single 1x1 pixel in the corner of your screen that changes color to communicate status to the Desktop Engine without reading memory.  
    \* \*\*Black:\*\* Idle / Safe to press Spacebar.  
    \* \*\*Red:\*\* Critical Error (Bag Full, Out of Bandages, Stuck).  
    \* \*\*Green:\*\* Success / Sequence Complete.  
    \* \*\*Blue:\*\* Waiting for User Input (Captcha/Trade Window).

\#\#\# \*\*5. "Contextual Identity" (Mode Switching)\*\*  
\*Found in SkillWeaver\*  
Your rotation shouldn't be static; it should adapt to the content.  
\* \*\*Auto-Profile Loading:\*\* The system detects your zone or instance ID.  
    \* \*Raid Boss:\* Loads the \*\*"Single Target / Cleave"\*\* priority list.  
    \* \*Mythic+:\* Loads the \*\*"AoE / Interrupt-Heavy"\*\* priority list.  
    \* \*Open World:\* Loads the \*\*"Burst / Speed"\*\* priority list (for killing low-hp mobs quickly).  
    \* \*PvP:\* Loads the \*\*"Arena"\*\* profile (defensive focus).

\#\#\# \*\*6. "Utility Tracker" (Infrastructure)\*\*  
\*Found in Holocron\*  
Ensuring you never have to hearthstone back to town.  
\* \*\*Tool Check:\*\* A dashboard widget that tracks ownership of critical logistics items across all characters:  
    \* \*Mounts:\* Yak (Reforging), Brutosaur (Auction House).  
    \* \*Toys:\* Katy's Stampwhistle (Mail), MOLL-E (Mail), Ohuna Perch.  
    \* \*Spells:\* Warband Bank Distance Inhibitor.  
\* \*\*Gap Analysis:\*\* It calculates the gold cost to buy missing utility items for specific alts and sends a "Purchase Order" to the Goblin module.  
