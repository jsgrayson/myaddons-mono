This list of features is designed to bridge the gap between a "database" addon (Rematch) and a "logic" addon (PetBattleScript), while adding modern quality-of-life improvements that the current ecosystem lacks.  
The goal is to move from **"Managing Lists"** to **"Managing Strategy."**

### **1\. The "Tactician" Module (Real-Time Logic)**

Current scripting addons require you to write code and then blindly mash a key. A modern replacement should feel like a tactical overlay.

* **Visual Block Scripting (Scratch-like):** Instead of writing Lua conditional text (if self.hp \< 50), use a drag-and-drop interface.  
  * *Example:* Drag a "When Enemy \< 25% HP" block \-\> Snap an "Explode" block inside it.  
* **"Coach Mode" Overlay:** Instead of auto-playing the move, highlight the *suggested* button on the UI. This teaches the player *why* a script works rather than just automating it.  
* **Dynamic "Ghost" Simulations:** During a battle, hovering over an enemy ability shows a "predicted state" for the next turn (e.g., "If you swap now, you will take 400 dmg from \[Minefield\]").

### **2\. "Smart" Team Management**

Rematch is great at static lists, but bad at dynamic contexts.

* **The "Swiss Army" Slot:** A dynamic team slot that auto-fills based on criteria rather than a specific pet.  
  * *Example:* Instead of saving "Anubisath Idol," you save "Target Dummy \+ \[Any Mechanical with Decoy\] \+ \[Leveling Pet\]." The addon picks the highest health mechanical you have available at that moment.  
* **Smart Leveling Queue:**  
  * **XP Optimization:** Auto-swaps the leveling pet based on the XP multiplier of the target. Don't waste a x3 XP trainer battle on a pet that only needs 50 XP to cap.  
  * **Safe-Swap Calculator:** Warns you if the leveling pet in the queue has too little HP to survive the enemy's first round AOE/Speed.

### **3\. Analytics & History (The "Recount" for Pets)**

Currently, there is no way to know *why* a team failed without watching closely.

* **Combat Log & Replay:** A text log of the last battle. "Turn 4: Your Starlette died to crit." allows for debugging scripts.  
* **RNG Audit:** After a loss, the addon calculates luck. "You lost, but the enemy crit rate was 40% (Expected: 5%). Unlucky try again."  
* **Success Rate Tracking:** Tracks win/loss % for specific teams against specific trainers. If a team drops below 80%, flag it as "Needs Revision."

### **4\. UX & Architecture**

* **"Mini-Mode" HUD:** A detachable combat-only window that replaces the default pet battle UI entirely, showing only cooldowns, weather, and the script button.  
* **Contextual Auto-Load:**  
  * **Zone-Based Loadouts:** When you enter "Nazjatar," the addon automatically swaps your "capture team" preference to pets with *Weakening Blow* and *Superbark*.  
* **AtlasLoot Integration:** Clicking a pet in the journal shows a map pin of exactly where to farm it (integrating data currently split between Rarity/PetTracker).

### **5\. Social & External Integration**

* **Xu-Fu / Wowhead Direct Feed:** A "Fetch Strategy" button that parses the clipboard for a URL. If you copy a Xu-Fu URL, it immediately attempts to build the team and script without needing an import string.  
* **Collection "Health" Score:** A dashboard showing gaps in your strategic roster. "You are missing a fast S/S rabbit" or "You have no Undead counters leveled."

### **Summary of the "Killer Feature"**

If you had to pick just one thing to differentiate this from Rematch: Visual Strategy Building.  
Merging the Team (the pets) and the Script (the instructions) into a single object. You don't load a team; you load a Strategy.  
Since you have previously mapped out an architecture for this, would you like to look at a schema for how to store a "Strategy" object that combines the Team ID, the Visual Script nodes, and the Analytics history into one JSON structure?