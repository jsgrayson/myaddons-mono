# Goblin Integration Specification

PetWeaver integrates with the Goblin economy system by watching for a specific JSON file containing Auction House data.

## 1. File Location
PetWeaver watches the root directory for a file named:
`price_list.json`

## 2. Data Format
The file must contain a JSON array of objects. Each object represents a pet listing.

### Required Fields
- `speciesId` (number): The Blizzard species ID.
- `price` (number): The current buyout price.
- `marketValue` (number): The calculated market value (provided by Goblin).
- `discount` (number): The discount percentage.
- `isDeal` (boolean): Whether Goblin considers this a "deal".
- `level` (number): The level of the pet listed (Required for arbitrage).
- `name` (string): Pet name.

### Example JSON
```json
[
  {
    "speciesId": 123,
    "price": 5000,
    "marketValue": 10000,
    "discount": 50,
    "isDeal": true,
    "level": 1,
    "name": "Mechanical Squirrel"
  }
]
```

## 3. Behavior
- **Display Only**: PetWeaver acts as a **display layer** for Goblin's intelligence.
- **Sync**: PetWeaver watches `price_list.json` and updates the UI immediately.
- **Alerts**: PetWeaver triggers UI alerts for:
    1.  **Hot Deals**: Any item marked `isDeal: true`.
    2.  **Missing Collection**: Deals for pets the user does *not* own.
    3.  **Level 1 Flips**: Cheap Level 1 pets that sell for high prices at Level 25.

## 4. PetWeaver Processing Logic
PetWeaver trusts Goblin's analysis but adds context from the user's profile:
1.  **Ingest**: Reads `price_list.json`.
2.  **Cross-Reference**: Checks `speciesId` against the user's `collection.json` to flag "Missing" pets.
3.  **Arbitrage Calc**: Identifies "Level 1 Flips" where `Lvl 1 Price + Leveling Effort < Lvl 25 Market Value`.
4.  **Display**: Populates the "Hot Deals", "Missing", and "Arbitrage" dashboards.

## 5. Implementation Notes for Goblin
- Ensure the file write is atomic if possible (write to temp file, then rename) to prevent PetWeaver from reading a partial file.
- Updates can be pushed as frequently as needed, but a batch update every few minutes is recommended to avoid excessive I/O.
