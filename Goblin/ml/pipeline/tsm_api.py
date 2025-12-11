"""
TSM API Integration - Fetch historical pricing data from TradeSkillMaster
"""
import requests
import pandas as pd
from loguru import logger
from typing import Dict, List, Optional
import time

class TSMAPIClient:
    """Access TradeSkillMaster pricing database for historical data."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://pricing-api.tradeskillmaster.com"
        self.api_key = api_key
        self.session = requests.Session()
        
    def get_realm_data(self, region: str, realm_slug: str) -> Dict:
        """Get current pricing data for a realm."""
        url = f"{self.base_url}/ah/{region}/{realm_slug}"
        
        headers = {}
        if self.api_key:
            headers['X-API-Key'] = self.api_key
            
        try:
            response = self.session.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"TSM API error: {e}")
            return {}
    
    def get_item_history(self, item_id: int, region: str, realm_slug: str, 
                        days: int = 30) -> pd.DataFrame:
        """
        Get historical pricing for specific item.
        
        Returns DataFrame with columns: timestamp, price, quantity, seller_count
        """
        # TSM historical API endpoint (may require premium)
        url = f"{self.base_url}/item/{region}/{realm_slug}/{item_id}"
        
        headers = {}
        if self.api_key:
            headers['X-API-Key'] = self.api_key
        
        params = {'days': days}
        
        try:
            response = self.session.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Parse TSM response into DataFrame
            records = []
            for entry in data.get('history', []):
                records.append({
                    'timestamp': pd.to_datetime(entry['time']),
                    'item_id': item_id,
                    'price': entry.get('marketValue', 0),
                    'quantity': entry.get('quantity', 0),
                    'seller_count': entry.get('numAuctions', 0)
                })
            
            df = pd.DataFrame(records)
            logger.info(f"Fetched {len(df)} historical records for item {item_id}")
            return df
            
        except Exception as e:
            logger.warning(f"Could not fetch TSM history for {item_id}: {e}")
            return pd.DataFrame()
    
    def get_popular_items(self, region: str, realm_slug: str, limit: int = 100) -> List[int]:
        """Get most traded items on realm (for bulk historical fetch)."""
        url = f"{self.base_url}/popular/{region}/{realm_slug}"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            items = data.get('items', [])[:limit]
            item_ids = [item['id'] for item in items]
            
            logger.info(f"Fetched {len(item_ids)} popular items")
            return item_ids
            
        except Exception as e:
            logger.error(f"Error fetching popular items: {e}")
            return []
    
    def bulk_historical_fetch(self, region: str, realm_slug: str, 
                             item_ids: List[int], days: int = 30) -> pd.DataFrame:
        """
        Fetch historical data for multiple items (for ML training).
        Rate-limited to avoid API throttling.
        """
        logger.info(f"Bulk fetching TSM data for {len(item_ids)} items...")
        
        all_data = []
        for i, item_id in enumerate(item_ids):
            if i % 10 == 0:
                logger.info(f"Progress: {i}/{len(item_ids)}")
            
            df = self.get_item_history(item_id, region, realm_slug, days)
            if not df.empty:
                all_data.append(df)
            
            # Rate limiting: 10 requests per second
            time.sleep(0.1)
        
        if all_data:
            combined = pd.concat(all_data, ignore_index=True)
            logger.success(f"Fetched {len(combined)} total historical records")
            return combined
        else:
            logger.warning("No TSM data retrieved")
            return pd.DataFrame()


def enrich_training_data_with_tsm(blizzard_data: pd.DataFrame, 
                                  region: str, realm_slug: str,
                                  api_key: Optional[str] = None) -> pd.DataFrame:
    """
    Enrich Blizzard API data with TSM historical pricing.
    This gives us YEARS of data for better ML training.
    """
    logger.info("Enriching training data with TSM historical data...")
    
    tsm = TSMAPIClient(api_key)
    
    # Get unique items from our current data
    unique_items = blizzard_data['item_id'].unique()[:200]  # Limit for API rate
    
    # Fetch TSM historical data
    tsm_data = tsm.bulk_historical_fetch(region, realm_slug, unique_items.tolist(), days=90)
    
    if tsm_data.empty:
        logger.warning("No TSM data - using only Blizzard data")
        return blizzard_data
    
    # Combine datasets
    combined = pd.concat([blizzard_data, tsm_data], ignore_index=True)
    combined = combined.drop_duplicates(subset=['item_id', 'timestamp'])
    combined = combined.sort_values(['item_id', 'timestamp'])
    
    logger.success(f"Combined dataset: {len(combined)} records ({len(blizzard_data)} Blizzard + {len(tsm_data)} TSM)")
    return combined


if __name__ == "__main__":
    # Test
    tsm = TSMAPIClient()
    
    # Example: Get data for Dalaran-US
    data = tsm.get_realm_data("us", "dalaran")
    print(f"TSM API working: {len(data) > 0}")
