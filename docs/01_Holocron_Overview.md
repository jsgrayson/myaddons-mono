# **Holocron: World of Warcraft Enterprise Resource Planning (ERP)**

## **1\. Executive Summary**

**Holocron** is a server-based inventory and logistics management system for World of Warcraft. Unlike traditional addons that run entirely within the game client (causing memory bloat and lag), Holocron offloads data storage, processing, and logic to an external server (Dell R720).  
It acts as the **Chief Operating Officer (COO)** of the account, managing the physical movement of assets based on intelligence provided by three sister systems: **Goblin** (Finance), **Skillweaver** (Performance), and **Petweaver** (Strategy).

## **2\. Core Architecture**

The system utilizes a "Headless" architecture to bypass addon limitations and enable complex data analysis.

### **A. The Client (Gaming PC)**

* **DataStore (Addon):** Standard, lightweight data collection addon. No processing.  
* **Bridge Script (Python):** A background service that watches for changes in SavedVariables and uploads raw data to the server. It also downloads processed "instruction files" from the server to the addon folder.  
* **Holocron Viewer (Addon):** A minimal in-game UI that displays data processed by the server and executes "Logistics Jobs" (e.g., auto-filling mail).

### **B. The Server (Dell R720)**

* **Database (PostgreSQL):** Stores millions of items, price histories, and collection data without impacting game performance.  
* **The Brain (Python/Flask):** Processes raw data, calculates logistics routes, determines liquidation strategies, and generates static Lua files for the game client.  
* **The Dashboard (Web UI):** A browser-based "Command Center" accessible via second monitor or mobile device.

## **3\. Ecosystem Integration ("The Triad")**

Holocron serves as the logistics engine for existing modules:

| Module | Role | Holocron's Responsibility |
| :---- | :---- | :---- |
| **Goblin** | **CFO (Finance)** | Identifies valuable assets in storage. Executed "Liquidation" orders (moving items to the Auction Alt). |
| **Skillweaver** | **Coach (Gear)** | Ensures required gear sets and consumables are physically present on the character. |
| **Petweaver** | **General (Pets)** | Manages the "Caging Pipeline" (selling duplicates) while protecting pets used in active strategies. |

## **4\. Key Differentiators**

1. **Zero-Lag Search:** Search 50 characters' inventories instantly via web UI.  
2. **Warband Native:** Specifically designed for *The War Within* logistics (Warband Bank vs. Guild Bank vs. Mail).  
3. **Context Aware:** Won't tell you to sell a pet you need for a strat, or vendor a transmog you haven't learned.  
4. **Boredom Mode:** Generates personalized "To-Do" lists based on lockouts and collection gaps.