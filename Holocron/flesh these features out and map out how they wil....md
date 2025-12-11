Here is the detailed technical breakdown of the **SkillWeaver** and **Holocron** "Killer Features," followed by the **Ecosystem Map** showing how all four projects (including PetWeaver and Goblin) integrate into a single "Lazy God" suite.

### **I. SkillWeaver: Feature Deep Dive**

*The Combat Engine. Goal: Perfect execution via context awareness.*

#### **1\. "The Shapeshifter" (Context-Aware Logic)**

**Concept:** Your rotation changes instantly based on the environment, not just your target.

* **How it Works (Lua Layer):** The addon registers events for ZONE\_CHANGED\_NEW\_AREA, PLAYER\_REGEN\_DISABLED, and NAME\_PLATE\_UNIT\_ADDED.  
* **Logic Flow:**  
  1. **Zone Check:** Entering a Raid ID triggers the "Boss" profile. Entering an Arena ID triggers the "PvP" profile.  
  2. **Combat Trigger:** When combat starts, the addon counts active enemy nameplates within 40yds.  
  3. **Dynamic Toggle:**  
     * If Nameplates \> 3 AND Profile \== Raid: Auto-toggle **AoE Mode** (Prioritize *Whirlwind* / *Chain Lightning*).  
     * If Nameplates \== 1: Auto-toggle **ST Mode** (Prioritize *Mortal Strike* / *Lightning Bolt*).  
* **Desktop Integration:** You don't write this logic. You use the **Visual Tactician** (drag-and-drop) to set thresholds (e.g., "Switch to AoE at 4 targets, not 3") which compiles into Lua.

#### **2\. "The Auditor" (Death & Failure Analysis)**

**Concept:** A post-mortem tool that tells you *why* you died, not just *that* you died.

* **How it Works (Desktop Layer):** The Desktop Engine monitors the WoWCombatLog.txt file in real-time.  
* **Logic Flow:**  
  1. **Trigger:** Detects UNIT\_DIED event for the player.  
  2. **Rewind:** Scans the last 10 seconds of log data.  
  3. **Analysis:** It compares "Incoming Damage" vs "Available Cooldowns."  
  4. **Verdict:**  
     * *Scenario A:* You died to a massive spike (100k dmg) while *Icebound Fortitude* was off cooldown. \-\> **Advice:** "You missed a defensive."  
     * *Scenario B:* You died to slow rot damage while your Healer was CC'd. \-\> **Advice:** "Not your fault."  
* **Feedback:** A toast notification on your desktop (overlay) immediately after death: *"Missed Kick on Hydrolance (0.5s window)."*

---

### **II. Holocron: Feature Deep Dive**

*The Logistics Core. Goal: Treating 50 characters as one inventory.*

#### **1\. "The Quartermaster" (Predictive Restocking)**

**Concept:** Automatically moving consumables to the characters that need them.

* **How it Works (Hybrid Layer):**  
  1. **Snapshot:** Upon logout, the addon dumps the character's inventory state to the Desktop Database.  
  2. **Analysis:** The Desktop Engine compares the inventory against your "Par" settings (e.g., "Raid Main needs 40 Potions").  
  3. **Sourcing:** It scans the DB to find which alt has the surplus supply (e.g., "Bank Alt has 2,000 Potions").  
  4. **Job Creation:** It creates a pending "Job."  
  5. **Execution:** When you log into "Bank Alt," Holocron flashes: *"Job Pending: Send 35 Potions to Main."* You click one button ("Process Job"), and it auto-fills the mail recipient and attaches the items.

#### **2\. "The Fabricator" (Chain Crafting)**

**Concept:** Automating the supply chain for complex items (e.g., Mounts, Legendaries) across professions.

* **How it Works:**  
  1. **Request:** You select "Craft \[Mechano-Hog\]" in the Web Portal.  
  2. **Deconstruction:** The Desktop Engine breaks it down: *Need 12 Titansteel, 40 Cobalt Bolts.*  
  3. **Inventory Check:** It sees *Alt A* has the Mining skill and *Alt B* has Engineering.  
  4. **Directives:**  
     * *Login A:* Waypoint arrow points to the specific bank slot containing the Ore. "Smelt this."  
     * *Mail:* "Send Bars to Alt B."  
     * *Login B:* "Craft Bolts."

---

### **III. The "Grand Unification" (Synergy Map)**

How these two new projects integrate with **PetWeaver** and **Goblin** to form the ultimate suite.

#### **1\. Holocron \+ Goblin (The Economy of Scale)**

* **The Interaction:** **Goblin** decides *what* to sell; **Holocron** finds it.  
* **Scenario:** You want to reset the market on *Peacebloom*.  
  * *Goblin:* Scans AH, identifies the buy-out price.  
  * *Holocron:* Scans your alt army. "Alt C has 500 Peacebloom in their guild bank."  
  * *Result:* You don't buy from the AH; you liquidate your own hidden stock first, maximizing profit margin.

#### **2\. SkillWeaver \+ Goblin (Cost-Per-Cast)**

* **The Interaction:** **SkillWeaver** tracks consumption; **Goblin** tracks cost.  
* **Scenario:** You are running a raid.  
  * *SkillWeaver:* Reports you used 15 "Rank 3" Potions in the last hour.  
  * *Goblin:* Calculates the real-time cost (15 x 80g \= 1,200g). It alerts you: *"Warning: You are spending more on consumables than the boss drops in gold. Switch to Rank 2 Potions?"*

#### **3\. Holocron \+ PetWeaver (The Zookeeper)**

* **The Interaction:** **PetWeaver** catches/levels; **Holocron** manages the "cages."  
* **Scenario:** You are out capturing pets.  
  * *PetWeaver:* "Bag Full. Cannot capture."  
  * *Holocron:* Triggers a "Vacuum" job. It detects you have a *MOLL-E* (mailbox toy). It prompts: "Deploy Mailbox."  
  * *Action:* You click one button. Holocron auto-mails all "Tradeable" pets to your "Auction Alt" to clear bag space instantly, keeping you in the field.

#### **4\. SkillWeaver \+ PetWeaver (Shared Brain)**

* **The Interaction:** Shared "Desktop Engine" resources.  
* **Scenario:** CPU priority.  
  * *Logic:* When you are in a **Pet Battle**, PetWeaver's AI Solver needs 100% CPU for Monte Carlo sims. SkillWeaver (Combat Rotation) is paused.  
  * *Logic:* When you exit the battle and pull a mob, the Desktop Engine instantly kills the Pet Solver thread and wakes up the SkillWeaver "Oracle" thread to ensure 0ms latency for your rotation.

### **Summary Dashboard (The Web Portal)**

Your "War Room" now displays the health of your entire WoW life:

1. **Combat:** 95% Parse Average (SkillWeaver).  
2. **Logistics:** 3 Pending Mail Jobs (Holocron).  
3. **Economy:** 400k Gold Profit today (Goblin).  
4. **Collection:** 12 new Rares captured (PetWeaver).