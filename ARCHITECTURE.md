# MYADDONS MONOREPO — SYSTEM ARCHITECTURE

## NOTE
Addon-level behavioral guarantees and parity rules are defined in:
[ADDON_CONTRACTS.md](./ADDON_CONTRACTS.md)

Detailed implementation checklists and status tracking are in:
[PARITY_SCORECARDS.md](./PARITY_SCORECARDS.md)

---

## 1. Repository Structure

The monorepo contains both World of Warcraft Addons (client-side Lua) and the Holocron Web Platform (backend + frontend).

```
Documents/MyAddons-Mono/
├── DeepPockets/       # [Addon] Modern Inventory Interface
├── PetWeaver/         # [Addon] Pet Battle Automation + Microservice
├── SkillWeaver/       # [Addon] Rotation Automation + Microservice
├── Holocron/          # [Service] API Gateway & Dashboard
│   ├── server.py      # Gateway + Holocron Service
│   └── frontend/      # React Dashboard (Vite)
└── Goblin/            # [Service] Economy Analytics
```

---

## 2. System Architecture

The system follows a **Hub & Spoke** architecture where `Holocron` acts as the central API Gateway and User Interface adjacent to specialized microservices.

### Service Map

| Service | Port | Description |
| :--- | :--- | :--- |
| **Holocron (Gateway)** | `8003` | Central entry point (`/api/v1/*`). Hosts the web dashboard. |
| **PetWeaver** | `5003` | Pet battle logic & strategy service. |
| **SkillWeaver** | `3000` | Rotation logic service (Collision with frontend dev port). |
| **Goblin** | `8001` | Economy intelligence service. |

### Gateway Routing Rules

All external access (from Frontend or CLI) MUST go through Holocron Gateway.

- **Frontend Prefix**: `/api/v1/`
- **Routing Logic**:
    - `/api/v1/petweaver/*` -> `http://localhost:5003/api/*`
    - `/api/v1/skillweaver/*` -> `http://localhost:3000/api/*`
    - `/api/v1/goblin/*` -> `http://localhost:8001/api/*`
    - `/api/v1/holocron/*` -> `localhost:8003/api/*` (Internal)

---

## 3. Data Flow

### A. Addon Sync (Offline)
World of Warcraft saves data to `SavedVariables/*.lua` on logout/reload.
The `Holocron/sync_addon_data.py` script:
1.  Target: `SavedVariables` folder.
2.  Action: Parses Lua tables.
3.  Output: SQLite (`holocron.db`) or JSON (`synced_data/`).
4.  Reporting: Posts `SANITY_RESULT` to Holocron API.

### B. Live Data (Online)
(Future Scope)
- Services may offer real-time endpoints.
- Gateway proxies these requests to the appropriate service.

---

## 4. Ownership Boundaries

### Addons (Lua)
- Owned by: Individual Addon Folders.
- Responsibility: In-game UI, Logic, Data Collection.
- **NO** direct dependency on backend services.

### Dashboard (React)
- Owned by: `Holocron/frontend`.
- Responsibility: Visualization, Aggregation.
- **MUST** fetch data via Gateway (`/api/v1/*`).

### Gateway (Python)
- Owned by: `Holocron/server.py`.
- Responsibility: Routing, Identity, Confidence Reporting.
