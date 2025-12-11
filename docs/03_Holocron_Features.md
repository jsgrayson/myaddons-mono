# **Holocron Features Specification**

## **1\. Module: Logistics ("The Warehouse")**

The core engine responsible for knowing where items are and moving them where they need to be.

### **1.1 Unified Inventory Search**

* **Web Search:** Google-like search bar on the dashboard. Returns results across Bags, Banks, Reagent Banks, Warband Bank, Guild Banks, and Mailboxes.  
* **In-Game Tooltip:** Minimal Lua addon showing "Total Owned" and "Locations" in item tooltips, read from a server-generated static index.

### **1.2 Smart Logistics Engine**

* **Move Orders:** The server generates "Jobs" based on triggers (e.g., "Main is low on Potions").  
* **Route Optimization:** Logic determines the fastest transfer method:  
  * *Warband Bank:* Instant transfer (High Priority).  
  * *Guild Bank:* Requires physical travel (Medium Priority).  
  * *Mail:* 1-hour delay (Low Priority).

### **1.3 The Mailing Shortcut**

* **In-Game UI:** A "Process Holocron" button on the Mailbox frame.  
* **Function:** Reads the server-generated "Logistics Manifest." Automatically fills recipient and attaches items for pending jobs. User only clicks "Send."

## **2\. Module: Asset Management ("The Liquidation Pipeline")**

Automated decision-making for selling vs. keeping items.

### **2.1 Pet Logistics**

* **Collection Safety:** Prevents selling pets if the user owns \< 3 of that species.  
* **Breed Upgrader:** Identifies if a new drop (e.g., S/S breed) is superior to a leveled pet (B/B). Queues a job to swap them before selling the inferior one.  
* **Petweaver Lock:** Queries the Petweaver database to "Protect" any specific pet GUID used in a saved battle team.  
* **Puppy Mill:** Automatically identifies "Safe to Sell" duplicates and queues them for transfer to the Auction Alt.

### **2.2 Transmog Logistics ("The Wardrobe")**

* **BoE Filter:**  
  * If Appearance Known: **Mark for Sale**.  
  * If Appearance Unknown & Value \> Threshold: **Mark for Sale** (Profit \> Collection).  
  * If Appearance Unknown & Value \< Threshold: **Mark for Learn/Equip**.  
* **Warbound Logic:** Recognizes that Warbound items can be learned by any character, removing the need to mail Plate to Warriors.

## **3\. Module: Player Utility ("The Infrastructure")**

Ensures the player has the necessary tools to perform logistics in the field.

### **3.1 Utility Tracker**

* **Dashboard Widget:** Tracks ownership of critical utility items:  
  * *Mounts:* Yak (Reforging), Brutosaur (AH).  
  * *Toys:* Katy's Stampwhistle, MOLL-E, Ohuna Perch (Mail).  
  * *Spells:* Warband Bank Distance Inhibitor.  
* **Gap Analysis:** Highlights missing utilities and calculates the gold cost to acquire them (linked to Goblin).

### **3.2 Knowledge Point Tracker**

* **Weekly Checklist:** Tracks profession "Knowledge Points" (KP) acquisition per character.  
* **Treatise Procurement:** If a weekly Treatise is missing, queues a job for Goblin to buy it and Holocron to mail it to the alt.

## **4\. Module: Boredom Mode ("The Navigator")**

A dynamic activity generator for downtime.

### **4.1 The Hitlist**

* **Logic:** Queries the database for "Missing Collections" (Mounts/Pets) available in instances where the character is NOT locked out.  
* **Toggles:** Users can filter by \[Mounts\], \[Pets\], \[Transmog\], or \[Short Dungeons Only\].  
* **Output:** A prioritized list of activities:  
  * *Target:* "Invincible's Reins"  
  * *Location:* "Icecrown Citadel (25H)"  
  * *Status:* "Available on 8 Alts."

### **4.2 The Vault Visualizer**

* **Grid View:** A dashboard showing weekly Great Vault progress for all max-level characters.  
* **Highlight:** Identifies characters that are "One run away" from unlocking a reward tier.