#!/usr/bin/env python3
"""
Pet Factory - Converts pet names/IDs to Pet objects
Loads data from species_data.json and creates usable Pet instances
"""

import json
from typing import Optional, Dict, List
from simulator import Pet, Ability, PetStats, PetFamily, PetQuality

class PetFactory:
    """
    Creates Pet objects from species data.
    Handles name lookup and alternative suggestions.
    """
    
    def __init__(self, species_path: str = "species_data.json"):
        self.species_data = {}
        self.name_to_id = {}  # Fast name → species_id lookup
        
        # Load species data
        try:
            with open(species_path, 'r') as f:
                self.species_data = json.load(f)
            
            # Build reverse index
            for species_id, data in self.species_data.items():
                name = data.get('name')
                if name:
                    self.name_to_id[name] = int(species_id)
            
            print(f"✓ PetFactory loaded {len(self.species_data)} species")
        except FileNotFoundError:
            print(f"⚠️  Warning: {species_path} not found. Using empty database.")
    
    def create_pet(self, name_or_id, level: int = 25, quality: PetQuality = PetQuality.RARE) -> Optional[Pet]:
        """
        Create a Pet object from name or species ID.
        
        Args:
            name_or_id: Pet name (str) or species_id (int)
            level: Pet level (default 25)
            quality: Pet quality (default RARE)
            
        Returns:
            Pet object or None if not found
        """
        # Convert name to ID if needed
        if isinstance(name_or_id, str):
            species_id = self.name_to_id.get(name_or_id)
            if not species_id:
                # Try placeholder names like "Pet_12345"
                if name_or_id.startswith("Pet_"):
                    try:
                        species_id = int(name_or_id.split("_")[1])
                    except (IndexError, ValueError):
                        return None
                else:
                    return None
        else:
            species_id = name_or_id
        
        # Get species data
        species_key = str(species_id)
        if species_key not in self.species_data:
            # Create placeholder pet for unknown IDs
            return self._create_placeholder_pet(species_id, name_or_id if isinstance(name_or_id, str) else f"Pet_{species_id}")
        
        data = self.species_data[species_key]
        name = data.get('name', f"Pet_{species_id}")
        family_name = data.get('family_name', 'Beast')
        
        # Map family name to enum
        family = self._get_family_enum(family_name)
        
        # Calculate stats (simplified - real stats depend on level/quality/breed)
        stats = self._calculate_stats(level, quality)
        
        # Create abilities (TODO: Load from ability database)
        abilities = self._create_default_abilities(family)
        
        return Pet(
            species_id=species_id,
            name=name,
            family=family,
            quality=quality,
            stats=stats,
            abilities=abilities
        )
    
    def _create_placeholder_pet(self, species_id: int, name: str) -> Pet:
        """Create a placeholder pet for unknown species"""
        return Pet(
            species_id=species_id,
            name=name,
            family=PetFamily.BEAST,
            quality=PetQuality.RARE,
            stats=PetStats(max_hp=1500, current_hp=1500, power=300, speed=280),
            abilities=self._create_default_abilities(PetFamily.BEAST)
        )
    
    def _calculate_stats(self, level: int, quality: PetQuality) -> PetStats:
        """
        Calculate pet stats based on level and quality.
        Simplified formula - real WoW uses complex breed calculations.
        """
        # Base stats at level 25 (Rare quality, balanced breed)
        base_hp = 1400
        base_power = 280
        base_speed = 280
        
        # Quality multiplier
        quality_mult = {
            PetQuality.POOR: 0.8,
            PetQuality.COMMON: 0.9,
            PetQuality.UNCOMMON: 0.95,
            PetQuality.RARE: 1.0,
            PetQuality.EPIC: 1.05
        }.get(quality, 1.0)
        
        # Level scaling (25 is max)
        level_mult = level / 25.0
        
        max_hp = int(base_hp * quality_mult * level_mult)
        power = int(base_power * quality_mult * level_mult)
        speed = int(base_speed * quality_mult * level_mult)
        
        return PetStats(max_hp=max_hp, current_hp=max_hp, power=power, speed=speed)
    
    def _get_family_enum(self, family_name: str) -> PetFamily:
        """Convert family name string to PetFamily enum"""
        family_map = {
            'Humanoid': PetFamily.HUMANOID,
            'Dragonkin': PetFamily.DRAGONKIN,
            'Flying': PetFamily.FLYING,
            'Undead': PetFamily.UNDEAD,
            'Critter': PetFamily.CRITTER,
            'Magic': PetFamily.MAGIC,
            'Elemental': PetFamily.ELEMENTAL,
            'Beast': PetFamily.BEAST,
            'Aquatic': PetFamily.AQUATIC,
            'Mechanical': PetFamily.MECHANICAL
        }
        return family_map.get(family_name, PetFamily.BEAST)
    
    def _create_default_abilities(self, family: PetFamily) -> List[Ability]:
        """
        Create default abilities for a pet.
        TODO: Load from ability database instead.
        """
        # For now, create a simple attack ability
        return [
            Ability(
                id=1,
                name=f"{family.name.title()} Attack",
                power=20,
                accuracy=100,
                speed=0,
                cooldown=0,
                family=family
            )
        ]
    
    def find_alternatives(self, pet_name: str, architect, my_collection: List[str], limit: int = 5) -> List[str]:
        """
        Find alternative pets similar to the target pet.
        
        Uses the Architect graph to find pets with similar synergies.
        
        Args:
            pet_name: Target pet name
            architect: ArchitectEngine instance
            my_collection: List of pet names the player owns
            limit: Max alternatives to return
            
        Returns:
            List of alternative pet names
        """
        if not architect:
            return []
        
        # Find pets that have synergies with the same partners as target pet
        target_synergies = set()
        
        # Get all pets this pet synergizes with
        if pet_name in architect.graph:
            target_synergies = set(architect.graph.successors(pet_name))
            target_synergies.update(architect.graph.predecessors(pet_name))
        
        if not target_synergies:
            # Fallback: Return random pets from collection
            return my_collection[:limit] if my_collection else []
        
        # Score alternatives by overlap with target's synergies
        alternatives = {}
        
        for candidate in my_collection:
            if candidate == pet_name:
                continue
            
            candidate_synergies = set()
            if candidate in architect.graph:
                candidate_synergies = set(architect.graph.successors(candidate))
                candidate_synergies.update(architect.graph.predecessors(candidate))
            
            # Score = number of shared synergy partners
            overlap = len(target_synergies & candidate_synergies)
            if overlap > 0:
                alternatives[candidate] = overlap
        
        # Sort by overlap score
        sorted_alternatives = sorted(alternatives.items(), key=lambda x: x[1], reverse=True)
        return [name for name, score in sorted_alternatives[:limit]]

if __name__ == "__main__":
    # Test the factory
    print("\n" + "="*70)
    print("PET FACTORY TEST")
    print("="*70)
    
    factory = PetFactory()
    
    # Test name lookup
    print("\n📝 Test 1: Create pet from name")
    ikky = factory.create_pet("Ikky")
    if ikky:
        print(f"  ✓ Created: {ikky.name} (ID: {ikky.species_id})")
        print(f"    Family: {ikky.family}, HP: {ikky.stats.max_hp}, Power: {ikky.stats.power}")
    else:
        print(f"  ⚠️  'Ikky' not found in database")
    
    # Test ID lookup
    print("\n📝 Test 2: Create pet from ID")
    pet = factory.create_pet(117)  # Tiny Snowman
    if pet:
        print(f"  ✓ Created: {pet.name} (ID: {pet.species_id})")
    
    # Test placeholder
    print("\n📝 Test 3: Unknown pet (placeholder)")
    unknown = factory.create_pet("Pet_99999")
    if unknown:
        print(f"  ✓ Created placeholder: {unknown.name}")
    
    print("\n" + "="*70)
    print("✓ Factory Test Complete!")
    print("="*70)
