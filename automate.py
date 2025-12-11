#!/usr/bin/env python3
"""
PetWeaver Automation Script
Orchestrates the entire flow:
1. Authenticate & Fetch Pet Collection
2. Scrape Strategies (if needed/requested)
3. Match Strategies
4. Update Addon Data
"""

import os
import sys
import argparse
from blizzard_oauth import BlizzardOAuth
from fetch_pet_collection import PetCollectionFetcher
from match_strategies import StrategyMatcher
from scrape_final_robust import RobustXuFuScraper

import platform

def get_default_addon_path():
    system = platform.system()
    if system == "Darwin":  # macOS
        return "/Applications/World of Warcraft/_retail_/Interface/AddOns/PetWeaver"
    elif system == "Windows":
        return r"C:\Program Files (x86)\World of Warcraft\_retail_\Interface\AddOns\PetWeaver"
    return "./PetWeaver"

def main():
    default_path = get_default_addon_path()
    
    parser = argparse.ArgumentParser(description='PetWeaver Automation')
    parser.add_argument('--scrape', action='store_true', help='Force scrape strategies from Xu-Fu')
    parser.add_argument('--skip-fetch', action='store_true', help='Skip fetching pet collection from Blizzard API')
    parser.add_argument('--addon-path', type=str, default=default_path, help=f'Path to PetWeaver addon folder (default: {default_path})')
    args = parser.parse_args()

    print("\n" + "="*60)
    print("🚀 PETWEAVER AUTOMATION")
    print("="*60)

    # 1. Authentication & Collection Fetch
    if not args.skip_fetch:
        print("\n[1/4] 🔐 Checking Blizzard Authentication...")
        client_id = os.getenv('BLIZZARD_CLIENT_ID')
        client_secret = os.getenv('BLIZZARD_CLIENT_SECRET')
        
        # If no env vars, try to use cached token with dummy credentials
        # The BlizzardOAuth class will check the token file first
        if not client_id or not client_secret:
            if os.path.exists('token.json'):
                print("⚠️  Env vars missing, attempting to use cached token...")
                client_id = "dummy_id"
                client_secret = "dummy_secret"
            else:
                print("❌ Error: Environment variables BLIZZARD_CLIENT_ID and BLIZZARD_CLIENT_SECRET must be set.")
                print("💡 Tip: Use --skip-fetch if you already have my_pets.json")
                return

        try:
            oauth = BlizzardOAuth(client_id, client_secret)
            access_token = oauth.get_access_token()
            
            # If we used dummy creds and get_access_token returned a token, we are good.
            # If it tried to authenticate (because token was invalid), it would fail with dummy creds.
            
            print("\n[2/4] 📥 Fetching Pet Collection...")
            fetcher = PetCollectionFetcher(access_token)
            collection = fetcher.get_pet_collection()
            fetcher.save_collection(collection)
            print(f"✅ Collection saved with {len(collection.get('pets', []))} pets")
            
        except Exception as e:
            print(f"❌ Error during auth/fetch: {e}")
            return
    else:
        print("\n[1/4] ⏭️  Skipping Authentication & Fetch (--skip-fetch used)")
        print("[2/4] ⏭️  Using existing my_pets.json")

    # 2. Scraping (Optional)
    if args.scrape or not os.path.exists('strategies.json'):
        print("\n[3/4] 🔄 Scraping Strategies (this may take a while)...")
        scraper = RobustXuFuScraper()
        # Note: scrape_all saves to strategies_final.json, we might need to rename or adjust
        # For now, let's assume the user might want to run the robust scraper manually if it's a huge job
        # But if they asked for it, we run it.
        try:
            scraper.scrape_all()
            # Rename for the matcher to find it easily if it expects 'strategies.json'
            if os.path.exists('strategies_final.json'):
                os.rename('strategies_final.json', 'strategies.json')
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
            return
    else:
        print("\n[3/4] ⏭️  Skipping Scrape (strategies.json exists)")

    # 3. Matching & Export
    print("\n[4/4] 🎯 Matching Strategies & Updating Addon...")
    try:
        matcher = StrategyMatcher()
        matches = matcher.match_strategies()
        matcher.save_matches(matches)
        
        # Export to Lua
        lua_path = os.path.join(args.addon_path, 'PetWeaverData.lua')
        matcher.export_to_lua(matches, output_path=lua_path)
        
    except Exception as e:
        print(f"❌ Error during matching: {e}")
        return

    print("\n" + "="*60)
    print("✅ AUTOMATION COMPLETE!")
    print("="*60)
    print(f"Addon data updated at: {os.path.abspath(lua_path)}")
    print("You can now reload your UI in WoW (/reload) to see the changes.")

if __name__ == "__main__":
    main()
