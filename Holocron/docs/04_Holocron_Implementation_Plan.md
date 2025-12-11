# **Holocron Implementation Plan**

## **Phase 1: Data Pipeline Foundation**

**Goal:** Establish the flow of data from the WoW Client to the Dell R720 Server.

* **1.1 Client Setup:**  
  * Install DataStore and sub-modules (Containers, Auctions, Mails, Pets, Crafts, Quests).  
  * Install SavedInstances (for Lockout tracking).  
* **1.2 Database Initialization:**  
  * Set up PostgreSQL on Dell R720.  
  * Execute schema.sql to create tables for Characters, Storage, Items, and Pets.  
* **1.3 The Bridge Script (Python):**  
  * Develop bridge.py for the Gaming PC.  
  * Implement slpp Lua parsing.  
  * Implement watchdog file monitoring for SavedVariables.  
  * Implement HTTP POST logic to send JSON payloads to the server.  
* **1.4 The Server Receiver (Flask):**  
  * Develop server.py on the Dell R720.  
  * Create /upload endpoint.  
  * Write logic to parse incoming JSON and UPSERT data into Postgres.

## **Phase 2: The Viewer & Core Logistics**

**Goal:** Visualize the data and implement basic search.

* **2.1 Web Dashboard (MVP):**  
  * Create a basic HTML/Bootstrap frontend hosted on Flask.  
  * Implement "Global Search" (Query the items table).  
  * Implement "Gold Graph" (Query characters table history).  
* **2.2 In-Game Indexer:**  
  * Write Server logic to flatten the SQL database into a lightweight Lua table (Holocron\_Index.lua).  
  * Update bridge.py to download this file on startup.  
* **2.3 In-Game Tooltip Addon:**  
  * Write HolocronViewer Lua addon.  
  * Hook OnTooltipSetItem to display counts from the Index.

## **Phase 3: Pet & Transmog Logic**

**Goal:** Implement the "Brain" that makes decisions.

* **3.1 Pet Weaver Integration:**  
  * Import Petweaver team data into Postgres.  
  * Develop SQL Views for safe\_to\_sell\_pets (Logic: Count \> 3 AND Not in Team AND Breed Check).  
* **3.2 Transmog Logic:**  
  * Import "Can I Mog It?" data or build an internal appearance database.  
  * Implement valuation\_logic (Compare Appearance Value vs. Vendor Price).  
* **3.3 The "Liquidation" Dashboard:**  
  * Create a web view showing "Assets to Liquidate."  
  * Implement a button to "Generate Mail Job."

## **Phase 4: Logistics & Automation**

**Goal:** Close the loop with the "Mailing Shortcut."

* **4.1 Job Queue System:**  
  * Create logistics\_jobs table.  
  * Write Server logic to generate jobs based on Liquidation or Crafting needs.  
* **4.2 The Mailbox Addon:**  
  * Update HolocronViewer to include a "Process Mail" button.  
  * Implement Lua logic to read the Job table and auto-attach items.  
* **4.3 Warband Logic:**  
  * Implement "Tab Detection" in the Python Bridge (to know which tabs are unlocked).  
  * Update Logistics logic to prioritize Warband Bank over Mailbox.

## **Phase 5: "Boredom Mode" & Polish**

**Goal:** Quality of Life features.

* **5.1 Instance Database:**  
  * Populate instance\_locations table (Coords, Wiki URLs).  
  * Build the "Hitlist" Algorithm (Lockout vs. Collection Needs).  
* **5.2 The Navigator UI:**  
  * Add "Boredom Mode" page to the Web Dashboard.  
  * Implement Toggles (Mounts/Pets/Mog).  
* **5.3 Final Integration:**  
  * Ensure Goblin (Pricing) and Skillweaver (Gear) data is syncing correctly into the master database.