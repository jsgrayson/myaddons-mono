import re
import csv
from typing import Dict

class TSMDecoder:
    """
    Decodes the cryptic TSM AuctionDB strings found in SavedVariables.
    Format is often: "i:194823:2341:239,9482,283..." (ItemString:MarketValue:MinBuyout...)
    """
    
    def __init__(self, raw_lua_content: str):
        self.raw_data = raw_lua_content
        # Regex to find the 'CSV' blobs inside the Lua table
        self.blob_pattern = re.compile(r'\["(\w+)"\] = "([^"]+)"')

    def parse_auction_db(self) -> Dict[int, dict]:
        """
        Returns a dict of {ItemID: {MarketValue, MinBuyout, RegionSaleAvg}}
        """
        prices = {}
        
        # 1. Extract the compressed strings (Realms/Region data)
        matches = self.blob_pattern.findall(self.raw_data)
        
        for realm_key, csv_blob in matches:
            # TSM stores data in a pseudo-CSV format inside the string
            # We split by comma to get the fields
            records = csv_blob.split(',')
            
            # The structure changes based on TSM version, but generally:
            # itemString, marketValue, minBuyout, numAuctions, quantity
            
            # Iterate in chunks if it's a flat list
            # Note: This requires reverse-engineering your specific TSM export format
            # For this example, we assume a standard ItemID:Price mapping
            
            for record in records:
                if ":" in record:
                    parts = record.split(":")
                    if len(parts) >= 2:
                        try:
                            # Attempt to parse "i:12345:9000"
                            if parts[0].startswith("i"):
                                item_id = int(parts[1])
                                market_val = int(parts[2]) if parts[2].isdigit() else 0
                                
                                prices[item_id] = {
                                    "mv": market_val,
                                    "source": realm_key
                                }
                        except ValueError:
                            continue
                            
        return prices

# Usable Utility Function
def ingest_pricing_snapshot(file_path: str):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        # Read huge files safely? For now, load into memory (assuming 32GB RAM server)
        content = f.read()
        
    decoder = TSMDecoder(content)
    price_db = decoder.parse_auction_db()
    
    print(f"[GOBLIN] Ingested pricing for {len(price_db)} items.")
    return price_db
