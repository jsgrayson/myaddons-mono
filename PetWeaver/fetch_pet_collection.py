#!/usr/bin/env python3
"""
Fetch WoW Pet Collection from Blizzard API
Uses OAuth token to retrieve user's complete pet collection
"""

import json
import os
import sys
from blizzard_oauth import BlizzardOAuth
import requests


class PetCollectionFetcher:
    """Fetches and processes WoW pet collection data"""
    
    def __init__(self, access_token, region="us"):
        self.access_token = access_token
        self.region = region
        self.api_base = f"https://{region}.api.blizzard.com"
        
    def _make_request(self, endpoint):
        """Make authenticated API request"""
        url = f"{self.api_base}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Battlenet-Namespace': f'profile-{self.region}'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
        
        return response.json()
    
    def get_user_info(self):
        """Get basic WoW account info"""
        return self._make_request('/profile/user/wow')
    
    def get_pet_collection(self):
        """Get complete pet collection"""
        return self._make_request('/profile/user/wow/collections/pets')
    
    def analyze_collection(self, collection_data):
        """Analyze pet collection and generate statistics"""
        pets = collection_data.get('pets', [])
        
        if not pets:
            return {
                'total': 0,
                'error': 'No pets found in collection'
            }
        
        analysis = {
            'total': len(pets),
            'max_level': 0,
            'level_25': 0,
            'below_25': 0,
            'quality_distribution': {},
            'pets_by_level': {},
            'sample_pets': []
        }
        
        for pet in pets:
            level = pet.get('level', 0)
            quality = pet.get('quality', {}).get('type', 'UNKNOWN')
            
            # Level stats
            if level == 25:
                analysis['level_25'] += 1
            else:
                analysis['below_25'] += 1
            
            analysis['max_level'] = max(analysis['max_level'], level)
            
            # Level distribution
            analysis['pets_by_level'][level] = analysis['pets_by_level'].get(level, 0) + 1
            
            # Quality distribution
            analysis['quality_distribution'][quality] = analysis['quality_distribution'].get(quality, 0) + 1
            
            # Sample pets (first 10)
            if len(analysis['sample_pets']) < 10:
                species = pet.get('species', {})
                stats = pet.get('stats', {})
                name_dict = species.get('name', {})
                name = name_dict.get('en_US', 'Unknown') if isinstance(name_dict, dict) else str(name_dict)
                analysis['sample_pets'].append({
                    'name': name,
                    'species_id': species.get('id', 0),
                    'level': level,
                    'quality': quality,
                    'health': stats.get('health', 0),
                    'power': stats.get('power', 0),
                    'speed': stats.get('speed', 0)
                })
        
        return analysis
    
    def save_collection(self, data, filename='my_pets.json'):
        """Save raw collection data to file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✅ Raw collection data saved to {filename}")
    
    def print_analysis(self, analysis):
        """Pretty print collection analysis"""
        print("\n" + "="*60)
        print("🐾 PET COLLECTION ANALYSIS")
        print("="*60)
        
        if 'error' in analysis:
            print(f"\n❌ {analysis['error']}")
            return
        
        print(f"\n📊 Total Pets: {analysis['total']}")
        print(f"⭐ Level 25 Pets: {analysis['level_25']}")
        print(f"📈 Pets Below Level 25: {analysis['below_25']}")
        print(f"🏆 Highest Level: {analysis['max_level']}")
        
        print(f"\n🎨 Quality Distribution:")
        for quality, count in sorted(analysis['quality_distribution'].items()):
            print(f"   {quality}: {count}")
        
        print(f"\n📊 Level Distribution:")
        for level in sorted(analysis['pets_by_level'].keys(), reverse=True)[:10]:
            count = analysis['pets_by_level'][level]
            bar = "█" * min(count // 5, 50)
            print(f"   Level {level:2d}: {count:4d} {bar}")
        
        if analysis['sample_pets']:
            print(f"\n🐾 Sample Pets (first 10):")
            print(f"{'Name':<30} {'Level':<7} {'Quality':<10} {'H/P/S':<15}")
            print("-" * 70)
            for pet in analysis['sample_pets']:
                stats = f"{pet['health']}/{pet['power']}/{pet['speed']}"
                print(f"{pet['name']:<30} {pet['level']:<7} {str(pet['quality']):<10} {stats:<15}")


def main():
    """Main execution"""
    print("\n" + "="*60)
    print("🎮 WOW PET COLLECTION FETCHER")
    print("="*60)
    
    # Get credentials
    client_id = os.getenv('BLIZZARD_CLIENT_ID')
    client_secret = os.getenv('BLIZZARD_CLIENT_SECRET')
    region = os.getenv('REGION', 'us')
    
    if not client_id or not client_secret:
        print("\n⚠️  Missing API credentials!")
        print("Run blizzard_oauth.py first to set up authentication.")
        print("\nOr set environment variables:")
        print("  export BLIZZARD_CLIENT_ID='your_client_id'")
        print("  export BLIZZARD_CLIENT_SECRET='your_client_secret'")
        return
    
    try:
        # Authenticate
        print("\n🔐 Authenticating with Blizzard API...")
        oauth = BlizzardOAuth(client_id, client_secret, region)
        access_token = oauth.get_access_token()
        print("✅ Authentication successful!")
        
        # Create fetcher
        fetcher = PetCollectionFetcher(access_token, region)
        
        # Get user info
        print("\n📥 Fetching account information...")
        user_info = fetcher.get_user_info()
        print(f"✅ Account ID: {user_info.get('id', 'Unknown')}")
        
        # Get pet collection
        print("\n📥 Fetching pet collection...")
        collection = fetcher.get_pet_collection()
        print(f"✅ Retrieved {len(collection.get('pets', []))} pets")
        
        # Save raw data
        fetcher.save_collection(collection)
        
        # Analyze collection
        analysis = fetcher.analyze_collection(collection)
        fetcher.print_analysis(analysis)
        
        print("\n" + "="*60)
        print("✅ COLLECTION FETCH COMPLETE!")
        print("="*60)
        print(f"\n📁 Data saved to: my_pets.json")
        print("\n💡 Next steps:")
        print("  1. Review your pet collection in my_pets.json")
        print("  2. Run strategy scraper to get optimal teams")
        print("  3. Compare your collection vs required pets")
        
    except FileNotFoundError:
        print("\n❌ Error: token.json not found")
        print("Run blizzard_oauth.py first to authenticate")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
