"""
AI Item Clustering - Automatically discover item behavior patterns
and create intelligent TSM-style groups.
"""
import os
import json
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from loguru import logger
from datetime import datetime
from typing import List, Dict, Any

class ItemClusterer:
    """Unsupervised learning to discover item market patterns."""
    
    def __init__(self, n_clusters: int = 8):
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.kmeans = None
        self.cluster_names = {}
        
    def load_historical_data(self) -> pd.DataFrame:
        """Load all historical price data."""
        raw_dir = os.path.join(os.path.dirname(__file__), "../data/raw")
        
        import glob
        all_files = glob.glob(os.path.join(raw_dir, "blizzard_*.csv"))
        
        if not all_files:
            logger.error("No historical data found for clustering")
            return pd.DataFrame()
        
        logger.info(f"Loading {len(all_files)} historical snapshots...")
        df_list = []
        for file in all_files:
            try:
                df = pd.read_csv(file)
                df_list.append(df)
            except Exception as e:
                logger.warning(f"Failed to load {file}: {e}")
        
        if not df_list:
            return pd.DataFrame()
            
        combined = pd.concat(df_list, ignore_index=True)
        logger.info(f"Loaded {len(combined)} total auction records")
        return combined
    
    def calculate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate clustering features for each item."""
        logger.info("Calculating item features...")
        
        # Group by item
        features = df.groupby('item_id').agg({
            'price': ['mean', 'std', 'min', 'max', 'count'],
            'quantity': ['mean', 'sum']
        }).reset_index()
        
        # Flatten column names
        features.columns = ['_'.join(col).strip('_') for col in features.columns.values]
        features.rename(columns={'item_id_': 'item_id'}, inplace=True)
        
        # Calculate additional features
        features['price_volatility'] = features['price_std'] / (features['price_mean'] + 1)
        features['price_range'] = (features['price_max'] - features['price_min']) / (features['price_mean'] + 1)
        features['volume_score'] = np.log1p(features['price_count'])  # Log of listing frequency
        features['supply_score'] = np.log1p(features['quantity_sum'])  # Total supply
        
        # Drop items with insufficient data
        features = features[features['price_count'] >= 3]  # At least 3 listings
        
        logger.info(f"Calculated features for {len(features)} items")
        return features
    
    def fit_clusters(self, features: pd.DataFrame) -> pd.DataFrame:
        """Fit K-means clustering on item features."""
        logger.info(f"Fitting {self.n_clusters} clusters...")
        
        # Select features for clustering
        cluster_features = [
            'price_mean', 'price_volatility', 'price_range',
            'volume_score', 'supply_score'
        ]
        
        X = features[cluster_features].fillna(0)
        
        # Standardize
        X_scaled = self.scaler.fit_transform(X)
        
        # Fit K-means
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        features['cluster'] = self.kmeans.fit_predict(X_scaled)
        
        logger.success(f"Clustering complete. {self.n_clusters} groups discovered.")
        return features
    
    def label_clusters(self, features: pd.DataFrame) -> Dict[int, Dict[str, Any]]:
        """Assign human-readable names to clusters based on characteristics."""
        logger.info("Labeling discovered groups...")
        
        cluster_profiles = {}
        
        for cluster_id in range(self.n_clusters):
            cluster_data = features[features['cluster'] == cluster_id]
            
            # Calculate cluster characteristics
            avg_price = cluster_data['price_mean'].mean()
            avg_volatility = cluster_data['price_volatility'].mean()
            avg_volume = cluster_data['volume_score'].mean()
            avg_supply = cluster_data['supply_score'].mean()
            item_count = len(cluster_data)
            
            # Determine cluster name based on characteristics
            name = self._generate_cluster_name(
                avg_price, avg_volatility, avg_volume, avg_supply
            )
            
            cluster_profiles[cluster_id] = {
                "name": name,
                "description": self._generate_description(
                    avg_price, avg_volatility, avg_volume, avg_supply
                ),
                "item_count": item_count,
                "avg_price": round(avg_price / 10000, 2),  # Convert copper to gold
                "avg_volatility": round(avg_volatility, 2),
                "strategy": self._generate_strategy(avg_volatility, avg_volume)
            }
            
            logger.info(f"Cluster {cluster_id}: {name} ({item_count} items)")
        
        return cluster_profiles
    
    def _generate_cluster_name(self, price: float, volatility: float, volume: float, supply: float) -> str:
        """Generate descriptive name for cluster."""
        # Price tier
        if price > 500000:  # > 50g
            price_tier = "High-Value"
        elif price > 50000:  # > 5g
            price_tier = "Mid-Tier"
        else:
            price_tier = "Budget"
        
        # Volatility
        if volatility > 0.5:
            behavior = "Volatile"
        elif volatility > 0.2:
            behavior = "Moderate"
        else:
            behavior = "Stable"
        
        # Volume
        if volume > 5:
            market = "High-Volume"
        elif volume > 3:
            market = "Active"
        else:
            market = "Niche"
        
        return f"{price_tier} {behavior} {market}"
    
    def _generate_description(self, price: float, volatility: float, volume: float, supply: float) -> str:
        """Generate human-readable description."""
        desc = []
        
        if volatility > 0.5:
            desc.append("Prices swing wildly - risky but high profit potential")
        elif volatility < 0.1:
            desc.append("Stable prices - predictable but lower margins")
        
        if volume > 5:
            desc.append("High trading volume - easy to buy/sell")
        elif volume < 2:
            desc.append("Low volume - may take time to sell")
        
        return ". ".join(desc) if desc else "Standard market behavior"
    
    def _generate_strategy(self, volatility: float, volume: float) -> str:
        """Suggest trading strategy for cluster."""
        if volatility > 0.5 and volume > 4:
            return "Day trading - Buy dips, sell peaks quickly"
        elif volatility < 0.2 and volume > 4:
            return "Volume flipping - Small margins, high turnover"
        elif volatility > 0.3:
            return "Patience flipping - Wait for good deals"
        else:
            return "Steady investment - Buy and hold"
    
    def export_tsm_groups(self, features: pd.DataFrame, cluster_profiles: Dict) -> str:
        """Generate TSM group import string."""
        logger.info("Generating TSM group export...")
        
        tsm_string = "group:GoblinAI\\n"
        
        for cluster_id, profile in cluster_profiles.items():
            group_name = profile['name'].replace(' ', '_')
            items = features[features['cluster'] == cluster_id]['item_id'].tolist()
            
            tsm_string += f"  group:{group_name}\\n"
            tsm_string += f"    items:{'i:'.join(map(str, items))}\\n"
        
        return tsm_string
    
    def run(self) -> Dict[str, Any]:
        """Execute full clustering pipeline."""
        logger.info("Starting AI item clustering...")
        
        #  Load data
        df = self.load_historical_data()
        if df.empty:
            logger.error("No data available for clustering")
            return {}
        
        # Calculate features
        features = self.calculate_features(df)
        if features.empty:
            logger.error("Feature calculation failed")
            return {}
        
        # Cluster
        features = self.fit_clusters(features)
        
        # Label
        cluster_profiles = self.label_clusters(features)
        
        # Export
        tsm_export = self.export_tsm_groups(features, cluster_profiles)
        
        # Save results
        output_dir = os.path.join(os.path.dirname(__file__), "../data/groups")
        os.makedirs(output_dir, exist_ok=True)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "num_items": len(features),
            "num_groups": self.n_clusters,
            "groups": cluster_profiles,
            "item_assignments": features[['item_id', 'cluster']].to_dict('records')
        }
        
        with open(os.path.join(output_dir, "ai_groups.json"), "w") as f:
            json.dump(result, f, indent=2)
        
        with open(os.path.join(output_dir, "tsm_export.txt"), "w") as f:
            f.write(tsm_export)
        
        logger.success(f"AI grouping complete! Discovered {self.n_clusters} intelligent groups.")
        logger.info(f"Results saved to {output_dir}")
        
        return result

if __name__ == "__main__":
    clusterer = ItemClusterer(n_clusters=8)
    result = clusterer.run()
    
    # Print summary
    if result:
        print("\n" + "="*60)
        print("AI-DISCOVERED ITEM GROUPS")
        print("="*60)
        for cluster_id, profile in result['groups'].items():
            print(f"\n{profile['name']} ({profile['item_count']} items)")
            print(f"  Avg Price: {profile['avg_price']}g")
            print(f"  Strategy: {profile['strategy']}")
            print(f"  {profile['description']}")
