# **Holocron Ecosystem Integration Architecture**

## **1\. System Topology ("The Quad")**

The system runs on a single hardware node (Dell R720) hosting four distinct services that share a unified data layer.

### **Hardware Layer**

* **Host:** Dell R720  
* **OS:** Linux (Ubuntu Server / Debian)  
* **Containerization:** Docker Compose (4 containers \+ Database \+ Redis)  
* **Network:** LAN Exposure (accessible by Gaming PC via IP)

### **Service Layout**

1. **Goblin (Finance):** Python/Pandas service. Polls Blizzard AH API. Calculates MV (Market Value) and Crafting Costs.  
2. **Skillweaver (Performance):** Python/SimC service. parses Combat Logs, manages SimulationCraft profiles, tracks Great Vault.  
3. **Petweaver (Strategy):** Python service. Manages Pet Battle algorithms, species database, and team compositions.  
4. **Holocron (Logistics):** Python/Flask service. The central "Router" that moves assets based on decisions made by the other three.

## **2\. The Unified Data Layer**

To minimize latency and complexity, all four services connect to a **Single PostgreSQL Instance**. Integration is achieved primarily through **SQL Views** and **Shared Schemas**, ensuring real-time data consistency without needing complex API calls between containers.

### **Database Schema Separation**

* schema\_goblin: Pricing tables, Ledger, Transaction History.  
* schema\_skillweaver: Char Specs, Gear Sets, Logs, Vault Status.  
* schema\_petweaver: Species DB, Breeds, Saved Teams.  
* schema\_holocron: Inventory Snapshot, Storage Locations, Logistics Queue.

### **Cross-Schema Integration Views**

These SQL Views act as the "API" between modules.

#### **A. Goblin $\\rightarrow$ Holocron (Valuation)**

* **View:** view\_inventory\_valuation  
* **Function:** Joins holocron.items with goblin.market\_prices.  
* **Usage:** Holocron queries this to determine if an item in a bag is "Trash" (Vendor) or "Asset" (Auction).

#### **B. Petweaver $\\rightarrow$ Holocron (Protection)**

* **View:** view\_protected\_pets  
* **Function:** Returns a list of pet\_guids currently used in active Petweaver Teams.  
* **Usage:** Holocron excludes these GUIDs from "Liquidation" logic to prevent selling key battle pets.

#### **C. Skillweaver $\\rightarrow$ Holocron (Re-supply)**

* **View:** view\_consumable\_needs  
* **Function:** Calculates the delta between "Required Consumables" (defined in Skillweaver configs) and "Current Inventory" (Holocron).  
* **Usage:** Holocron generates "Mail Jobs" to send Potions/Flasks from the Bank to the Raiding Character.

## **3\. Event-Driven Workflows**

When a specific event happens in one module, it triggers a cascade across the ecosystem.

### **Workflow 1: The "Liquidation" Loop**

*Trigger: User uploads a Bag Snapshot (via Bridge).*

1. **Holocron** ingests raw inventory data.  
2. **Holocron** queries goblin.view\_liquidatable\_assets:  
   * *Logic:* Finds items where quantity \> keep\_threshold AND market\_value \> min\_post\_price.  
3. **Holocron** checks petweaver.view\_protected\_pets:  
   * *Logic:* Removes any Pet Item IDs that are flagged as "Strategic Assets."  
4. **Holocron** checks skillweaver.view\_reserved\_gear:  
   * *Logic:* Removes any BoE gear that is an upgrade for an Alt.  
5. **Result:** Holocron generates a **Logistics Job**: "Mail \[Item X\] to Auction-Alt."  
6. **Feedback:** In-game addon highlights \[Item X\] in Gold.

### **Workflow 2: The "Weekly Reset" Protocol**

*Trigger: Tuesday Reset (Time Event).*

1. **Skillweaver** resets vault\_status table to "Locked."  
2. **Holocron** resets raid\_lockouts table.  
3. **Goblin** triggers api\_fetch\_prices to capture "Reset Day" inflation.  
4. **Holocron** updates the **Dashboard Hitlist**:  
   * Prioritizes Alts that need "1 more run" for Vault.  
   * Prioritizes Mount Farms that are now unlocked.  
5. **Goblin** checks holocron.view\_missing\_utility:  
   * If "Knowledge Point Treatise" is missing for the week, Goblin adds it to the "Shopping List."

## **4\. Infrastructure Services**

### **A. The "Bridge" (Ingress)**

* **Role:** Single entry point for data from the Gaming PC.  
* **Protocol:** HTTP POST (JSON payload).  
* **Routing:**  
  * DataStore\_Containers $\\rightarrow$ holocron.inventory\_processor  
  * DataStore\_Auctions $\\rightarrow$ goblin.market\_processor  
  * WoWCombatLog.txt $\\rightarrow$ skillweaver.log\_processor

### **B. The "Courier" (Egress)**

* **Role:** Generates the static files the WoW Client reads.  
* **Output:**  
  * Holocron\_Index.lua: Inventory search & Logistics Jobs.  
  * Holocron\_PetNeeds.lua: Which pets to learn/upgrade.  
  * Goblin\_Pricing.lua: Tooltip price data (Optional replacement for TSM App).

## **5\. Dashboard Integration (The "Command Center")**

A unified Web UI running on Port 80/443 of the R720.

* **Home (Status):**  
  * *Alerts:* "3 Mail Jobs Pending", "Vault Unlocked on Main", "Auction Value: 500k."  
* **Tab: Market (Goblin):**  
  * Graphs: Gold Velocity, Asset Liquidity.  
* **Tab: Operations (Holocron):**  
  * Search Bar: "Where is my \[Sulfuron Hammer\]?"  
  * Buttons: "Generate Restock Manifest."  
* **Tab: Roster (Skillweaver):**  
  * Grid: Char Name | ilvl | Vault Status | KP Status.  
* **Tab: Collection (Petweaver):**  
  * List: "Missing Breeds", "Duplicates to Sell."

## **6\. Development Priority**

1. **Database:** Establish the shared PostgreSQL container and schemas.  
2. **Holocron Core:** Build the Inventory Ingest and simple Search.  
3. **Goblin Link:** Connect Inventory to Pricing for "Total Account Value."  
4. **Petweaver Link:** Implement the "Safe Liquidation" logic.  
5. **Skillweaver Link:** Implement the "Vault/Lockout" tracking.