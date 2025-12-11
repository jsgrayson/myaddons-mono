Here is the final **Design Document** for "The Silent Assassin."  
I have updated the **Navigation** section to include your **"Smart Evac" (Auto-Fly to Flightpoint)** logic, which automatically calculates the fastest way to leave a zone (Whistle vs. Hearth vs. Flight) so you never get stuck.  
You can copy/paste this directly into your drive.  
---

# **Project Design Document: "The Silent Assassin"**

Concept: A hybrid "Addon \+ Desktop Engine" system designed to solve World of Warcraft Pet Battles with 100% efficiency.  
Goal: To navigate the world, manage teams, and execute battles using a single physical keypress (Spacebar) with zero on-screen HUD.  
Philosophy: "The User provides the muscle (Keypress); The Machine provides the brain."  
---

## **1\. System Architecture**

The system is split into three layers to bypass Lua limitations and avoid TOS violations.

### **Layer 1: The Executioner (WoW Addon)**

* **Role:** The dumb client. It displays nothing and thinks little. It only executes orders pushed to it.  
* **Tech:** Lua, SecureStateDriver, TomTom API, Rematch API.  
* **Function:** Handles the "Master Key" logic, renders the navigation arrow, and executes battle commands.

### **Layer 2: The Brain (Desktop Agent)**

* **Role:** The heavy lifter. Runs in the background on the PC.  
* **Tech:** Rust/C++ (for simulation speed), File Watcher (to sync with Lua).  
* **Function:** Runs Genetic Algorithms to build teams, Minimax to solve battles, and manages the "Smart GPS" routing.

### **Layer 3: The War Room (Web Portal)**

* **Role:** The command center (Second Monitor).  
* **Tech:** Localhost Web Server.  
* **Function:** Displays the Playlist, Market Data, and Simulation Results.

---

## **2\. Navigation: "The Smart GPS"**

*The logic that moves you between battles.*

### **A. The Playlist (Circuit System)**

You do not target trainers manually. The Desktop Engine pushes a "Route" to the addon.

* **Step 1:** Target Farmer Nishi.  
* **Step 2:** Battle Nishi.  
* **Step 3:** **Smart Evac** (Get to next zone).  
* **Step 4:** Target Mo'ruk.

### **B. The "Smart Evac" Protocol (Auto-Fly)**

When a battle ends and the next trainer is far away, the Desktop Engine calculates the fastest method to move:

1. **Check Whistle:** If inside a Legion/BfA zone, the Playlist inserts: **Use Item: Flight Master's Whistle**. (Instant Teleport).  
2. **Check Hearth:** If the destination is another continent, the Playlist inserts: **Use Item: Dalaran Hearthstone**.  
3. **Fallback (Nearest Flightpoint):**  
   * If no teleport is available, the Engine calculates the distance to the **Nearest Flight Master**.  
   * It sets the TomTom arrow to that Flight Master.  
   * It triggers **"Flight Mode"** (See below).

### **C. Flight Mode (Point & Shoot)**

Since we cannot automate 3D flying (TOS violation), we use a "Semi-Auto" method:

* **The Heading:** The screen displays a massive Arrow. You align your camera with it.  
* **The Engine:** You hold **Spacebar**. The addon triggers /cast \[mount\] \+ AutoMoveForward.  
* **The Arrival:** When you reach the Flight Master, the addon detects arrival, stops you, interacts, and **Automatically selects the Taxi Node** to the next zone.

---

## **3\. The Addon: "The Master Key"**

One physical key (Spacebar) dynamically changes function based on the game state.

| Game State | Spacebar Function | Action |
| :---- | :---- | :---- |
| **Idle** | /tar \[NextTarget\] | Selects the next Trainer or Flight Master. |
| **Moving** | /click InteractWithTarget | Character auto-runs (CTM) to the target. |
| **Flying** | /cast \[mount\]; /run MoveForwardStart() | Engines ON. You just steer the camera. |
| **Gossip** | SelectGossipOption(1) | Skips dialog and starts the fight. |
| **Combat** | /click AutoBattleButton | Executes the perfect script move. |
| **Win** | /cast Revive Battle Pets | Heals team and loads next target. |
| **Loss** | /run C\_PetBattles.ForfeitGame() | Instant forfeit to save time. |

---

## **4\. The Desktop Engine: "The Logic"**

### **A. Genetic Team Builder**

* **Problem:** You don't have the specific pets a guide asks for.  
* **Solution:** The Engine scans *your* specific collection. It runs a Genetic Algorithm (evolution) to find a combination of pets you *do* own that has a 100% win rate against the specific trainer.

### **B. The Strategist (Minimax)**

* **Problem:** RNG (Crits/Misses) can lose fights.  
* **Solution:** The Engine simulates the battle 1,000 times before you start. If there is even a 1% chance of losing (due to bad RNG), it **flags the team as unsafe** and refuses to let you start until you swap gear/breeds.

---

## **5\. The Tactician Syntax (TTS)**

*The "Easy-to-Read" language required for your custom scripts.*  
**Format:** \[TRIGGER\] :: \[ACTION\]

### **The Keywords**

* **BLOCK:** Only fires if the enemy is about to deal massive damage.  
* **MAINTAIN:** Only fires if a specific buff/weather is missing.  
* **EXECUTE:** Only fires if the enemy is in kill range.  
* **SPAM:** The default filler move.

### **Example Script (Generated by Desktop App)**

**Scenario:** Anubisath Idol vs. Dragonkin

Plaintext

BLOCK     :: BIG HIT (Deep Breath) \-\> Use Deflection  
MAINTAIN  :: Sandstorm             \-\> Use Sandstorm  
EXECUTE   :: HP \< 250              \-\> Use Crush  
SPAM      :: Filler                \-\> Use Crush

*Note: The Desktop App compiles this simple text into complex Lua code automatically.*  
---

## **6\. Data Sources**

* **Species Data:** **Blizzard Game Data API** (Stats/Abilities).  
* **Trainer Locations:** **Data Mining** (Parsed from PetTracker).  
* **Strategies:** **Xu-Fu’s Pet Guides** (Community Scripts).  
* **Prices:** **TradeSkillMaster (TSM) API** (Auction Values).

---

## **7\. "Silent Assassin" Workflow**

1. **Setup:** On your **Second Monitor**, you drag the "Pandaria Circuit" into your Queue.  
2. **Sync:** The Desktop Engine calculates the route and pushes the first team to the game.  
3. **The Loop:**  
   * **Tap Spacebar:** Target Nishi.  
   * **Tap Spacebar:** Auto-Run to Nishi.  
   * **Tap Spacebar:** Win Battle (Perfect Script).  
   * **Tap Spacebar:** Auto-Heal.  
   * **Tap Spacebar:** Target Flight Master.  
   * **Hold Spacebar:** Fly to Flight Master (Point & Shoot).  
   * **Tap Spacebar:** Auto-Take Taxi to next zone.  
4. **You:** Never touch the mouse. Never look at the main screen. Just watch Netflix and tap Spacebar.