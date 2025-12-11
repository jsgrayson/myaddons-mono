"""
PetTracker Data Decoder

This module decodes the encoded ability strings from PetTracker and cross-references
with the Blizzard Battle Pet API to get full ability details.

PetTracker Data Structure:
- Addon.Species[speciesID][abilitySlot] = encoded_string
- Addon.SpecieBreeds[speciesID] = array of breed IDs
- Addon.SpecieStats[speciesID] = {power, speed, health} stat multipliers
"""

import os
import json
import requests
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()

# Base-36 alphabet used by PetTracker (0-9, A-Z)
BASE36_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class PetTrackerDecoder:
    def __init__(self, blizzard_token: Optional[str] = None):
        """
        Initialize decoder with optional Blizzard API token
        
        Args:
            blizzard_token: OAuth token for Blizzard API access
        """
        self.blizzard_token = blizzard_token or os.getenv("BLIZZARD_ACCESS_TOKEN")
        self.ability_cache = {}
        self.species_cache = {}
        
    def decode_base36(self, encoded: str) -> List[int]:
        """
        Decode a PetTracker base-36 encoded string to ability IDs
        
        The encoding uses standard Base-36 (0-9, A-Z).
        It appears to encode ability IDs in chunks.
        
        Args:
            encoded: Base-36 encoded string from PetTracker
            
        Returns:
            List of decoded integer values (likely ability IDs)
        """
        values = []
        
        # Process in chunks
        # Based on typical ability IDs (3-4 digits), 2 chars in Base36 (36^2 = 1296) might be too small
        # 3 chars (36^3 = 46656) covers all ability IDs.
        # Let's try to determine chunk size dynamically or assume 3 based on data volume
        
        # Let's try 2 characters per ID based on analysis
        chunk_size = 2
        
        for i in range(0, len(encoded), chunk_size):
            chunk = encoded[i:i+chunk_size]
            value = 0
            
            for char in chunk:
                if char in BASE36_ALPHABET:
                    value = value * 36 + BASE36_ALPHABET.index(char)
            
            if value > 0:
                values.append(value)
            
        return values
    
    async def fetch_ability_details(self, ability_id: int) -> Optional[Dict]:
        """
        Fetch ability details from Blizzard API
        
        Args:
            ability_id: WoW Battle Pet ability ID
            
        Returns:
            Ability details dictionary or None if not found
        """
        if ability_id in self.ability_cache:
            return self.ability_cache[ability_id]
            
        if not self.blizzard_token:
            print(f"No Blizzard token available, cannot fetch ability {ability_id}")
            return None
            
        url = f"https://us.api.blizzard.com/data/wow/pet-ability/{ability_id}"
        params = {
            "namespace": "static-us",
            "locale": "en_US",
            "access_token": self.blizzard_token
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.ability_cache[ability_id] = data
                return data
            else:
                print(f"Failed to fetch ability {ability_id}: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching ability {ability_id}: {e}")
            return None
    
    async def fetch_species_details(self, species_id: int) -> Optional[Dict]:
        """
        Fetch pet species details from Blizzard API
        
        Args:
            species_id: WoW Battle Pet species ID
            
        Returns:
            Species details dictionary or None if not found
        """
        if species_id in self.species_cache:
            return self.species_cache[species_id]
            
        if not self.blizzard_token:
            print(f"No Blizzard token available, cannot fetch species {species_id}")
            return None
            
        url = f"https://us.api.blizzard.com/data/wow/pet/{species_id}"
        params = {
            "namespace": "static-us",
            "locale": "en_US",
            "access_token": self.blizzard_token
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.species_cache[species_id] = data
                return data
            else:
                print(f"Failed to fetch species {species_id}: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching species {species_id}: {e}")
            return None
    
    def parse_species_data(self, species_data: Dict) -> Dict:
        """
        Parse raw PetTracker species data
        
        Args:
            species_data: Dictionary of {abilitySlot: encoded_string}
            
        Returns:
            Dictionary of {abilitySlot: [ability_ids]}
        """
        parsed = {}
        
        for slot, encoded in species_data.items():
            try:
                ability_ids = self.decode_base32(encoded)
                parsed[int(slot)] = ability_ids
            except Exception as e:
                print(f"Error decoding slot {slot}: {e}")
                parsed[int(slot)] = []
                
        return parsed
    
    def calculate_stats(self, base_stats: Tuple[float, float, float], 
                       breed_id: int, level: int = 25) -> Dict[str, int]:
        """
        Calculate pet stats based on breed and level
        
        WoW Battle Pet stat formula:
        - Health = (base_health + breed_health) * level * quality + 100
        - Power = (base_power + breed_power) * level * quality / 20
        - Speed = (base_speed + breed_speed) * level * quality / 20
        
        Args:
            base_stats: Tuple of (power, speed, health) multipliers
            breed_id: Breed ID (3-12, affects stat distribution)
            level: Pet level (1-25)
            
        Returns:
            Dictionary with calculated power, speed, health
        """
        base_power, base_speed, base_health = base_stats
        quality = 1.0  # Rare quality multiplier
        
        # Breed modifiers (simplified - real values would come from game data)
        # These are approximations and would need to be refined
        breed_modifiers = {
            3: (0, 0, 0.9),      # B/B (Balanced)
            4: (0.5, 0, 0.4),    # P/P (Power)
            5: (0, 0.5, 0.4),    # S/S (Speed)
            6: (0.25, 0.25, 0.4),# H/H (Health)
            7: (0.4, 0, 0.9),    # H/P
            8: (0, 0.4, 0.9),    # H/S
            9: (0.4, 0.4, 0),    # P/S
            10: (0.25, 0, 0.65), # P/B
            11: (0, 0.25, 0.65), # S/B
            12: (0.125, 0.125, 0.65), # H/B
        }
        
        breed_mod = breed_modifiers.get(breed_id, (0, 0, 0))
        
        power = int((base_power + breed_mod[0]) * level * quality / 20)
        speed = int((base_speed + breed_mod[1]) * level * quality / 20)
        health = int((base_health + breed_mod[2]) * level * quality) + 100
        
        return {
            "power": power,
            "speed": speed,
            "health": health
        }


async def main():
    """Test the decoder with sample data"""
    decoder = PetTrackerDecoder()
    
    # Example: Decode a single species ability set
    # Species 862 (from the data)
    sample_encoded = "ESP2F2NIF6PMFCQ8FIO0G2O0G8KWG8LQG8QWGEMGGGN6GIKEGKP2GKQ8GUNMH2K4HGNSHMK6I6JYIMNAIQKOISLUISMMJ2L6"
    
    print("Decoding sample ability data...")
    ability_ids = decoder.decode_base36(sample_encoded)
    print(f"Decoded ability IDs: {ability_ids[:5]}...")
    
    # Verify with Blizzard API
    print("\nVerifying first 3 abilities with Blizzard API...")
    for ability_id in ability_ids[:3]:
        details = await decoder.fetch_ability_details(ability_id)
        if details:
            print(f"  ID {ability_id}: Found - {details.get('name', 'Unknown Name')}")
        else:
            print(f"  ID {ability_id}: Not found or API error")
    
    # Example stat calculation
    
    # Example stat calculation
    base_stats = (8.5, 7.5, 8)  # From SpecieStats data
    breed_id = 4  # P/P breed
    
    stats = decoder.calculate_stats(base_stats, breed_id, level=25)
    print(f"\nCalculated stats for L25 P/P breed:")
    print(f"  Power: {stats['power']}")
    print(f"  Speed: {stats['speed']}")
    print(f"  Health: {stats['health']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
