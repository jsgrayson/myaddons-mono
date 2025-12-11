"""
Unit tests for damage calculator

Tests the core damage formulas, family effectiveness, quality modifiers,
and special combat mechanics (crits, dodges, etc.)
"""

import pytest
from simulator.damage_calculator import DamageCalculator, FAMILY_EFFECTIVENESS
from simulator.battle_state import (
    Pet, Ability, PetStats, PetFamily, PetQuality, Buff, BuffType
)


@pytest.fixture
def basic_pets():
    """Create basic test pets"""
    # Create a rare Beast pet
    beast_stats = PetStats(max_hp=1500, current_hp=1500, power=300, speed=280)
    beast = Pet(
        species_id=1,
        name="Test Beast",
        family=PetFamily.BEAST,
        quality=PetQuality.RARE,
        stats=beast_stats,
        abilities=[]
    )
    
    # Create a rare Critter pet (weak to Beast)
    critter_stats = PetStats(max_hp=1400, current_hp=1400, power=280, speed=300)
    critter = Pet(
        species_id=2,
        name="Test Critter",
        family=PetFamily.CRITTER,
        quality=PetQuality.RARE,
        stats=critter_stats,
        abilities=[]
    )
    
    return beast, critter


@pytest.fixture
def basic_ability():
    """Create a basic damage ability"""
    return Ability(
        id=1,
        name="Bite",
        power=20,
        accuracy=100,
        speed=0,
        cooldown=0,
        family=PetFamily.BEAST
    )


class TestDamageCalculator:
    
    def test_basic_damage(self, basic_pets, basic_ability):
        """Test basic damage formula without special modifiers"""
        beast, critter = basic_pets
        calc = DamageCalculator(rng_seed=42)
        
        damage, details = calc.calculate_damage(basic_ability, beast, critter)
        
        # Base damage = 20 * (300 / 20) = 300
        assert details['base_damage'] == 300
        assert details['hit'] is True
        assert damage > 0
    
    def test_family_effectiveness(self, basic_pets, basic_ability):
        """Test family effectiveness multipliers"""
        beast, critter = basic_pets
        calc = DamageCalculator(rng_seed=42)
        
        damage, details = calc.calculate_damage(basic_ability, beast, critter)
        
        # Beast vs Critter should be strong (+50%)
        assert details['family_multiplier'] == 1.5
    
    def test_quality_modifier(self, basic_pets, basic_ability):
        """Test quality damage modifiers"""
        beast, critter = basic_pets
        
        # Test with Poor quality attacker
        beast_poor = Pet(
            species_id=1,
            name="Poor Beast",
            family=PetFamily.BEAST,
            quality=PetQuality.POOR,
            stats=PetStats(max_hp=1500, current_hp=1500, power=300, speed=280),
            abilities=[]
        )
        
        calc = DamageCalculator(rng_seed=42)
        damage, details = calc.calculate_damage(basic_ability, beast_poor, critter)
        
        # Quality is applied in power stat, not in damage calculation
        assert details['quality_multiplier'] == 1.0
    
    def test_miss(self):
        """Test ability missing"""
        # 50% accuracy ability
        low_accuracy_ability = Ability(
            id=2,
            name="Low Accuracy",
            power=50,
            accuracy=50,
            speed=0,
            cooldown=0,
            family=PetFamily.BEAST
        )
        
        beast_stats = PetStats(max_hp=1500, current_hp=1500, power=300, speed=280)
        beast = Pet(
            species_id=1,
            name="Beast",
            family=PetFamily.BEAST,
            quality=PetQuality.RARE,
            stats=beast_stats,
            abilities=[]
        )
        
        critter_stats = PetStats(max_hp=1400, current_hp=1400, power=280, speed=300)
        critter = Pet(
            species_id=2,
            name="Critter",
            family=PetFamily.CRITTER,
            quality=PetQuality.RARE,
            stats=critter_stats,
            abilities=[]
        )
        
        calc = DamageCalculator(rng_seed=100)  # Seed that causes miss
        
        # Run multiple times to check for misses
        hits = 0
        misses = 0
        for i in range(100):
            calc = DamageCalculator(rng_seed=i)
            damage, details = calc.calculate_damage(low_accuracy_ability, beast, critter)
            if details['hit']:
                hits += 1
            else:
                misses += 1
                assert damage == 0
        
        # With 50% accuracy, we should see roughly 50% hits
        assert 30 < hits < 70  # Allow some variance
    
    def test_crit_damage(self, basic_pets, basic_ability):
        """Test critical hit damage"""
        beast, critter = basic_pets
        
        # Force a crit by testing multiple seeds
        found_crit = False
        for seed in range(100):
            calc = DamageCalculator(rng_seed=seed)
            damage, details = calc.calculate_damage(basic_ability, beast, critter)
            
            if details['crit']:
                found_crit = True
                # Crit should do +50% damage
                break
        
        assert found_crit, "Should find at least one crit in 100 attempts"
    
    def test_buff_power_modifier(self, basic_pets, basic_ability):
        """Test power buff affecting damage"""
        beast, critter = basic_pets
        
        # Add +25% power buff to beast
        power_buff = Buff(
            type=BuffType.STAT_MOD,
            duration=2,
            magnitude=1.25,
            stat_affected='power'
        )
        beast.active_buffs.append(power_buff)
        
        calc = DamageCalculator(rng_seed=42)
        damage, details = calc.calculate_damage(basic_ability, beast, critter)
        
        # With +25% power, base damage should be higher
        # Base: 20 * (300 * 1.25 / 20) = 375
        assert details['base_damage'] == 375
    
    def test_healing_calculation(self, basic_pets):
        """Test healing ability calculation"""
        beast, _ = basic_pets
        
        heal_ability = Ability(
            id=10,
            name="Heal",
            power=15,
            accuracy=100,
            speed=0,
            cooldown=0,
            family=PetFamily.BEAST,
            is_heal=True
        )
        
        calc = DamageCalculator(rng_seed=42)
        heal_amount = calc.calculate_healing(heal_ability, beast)
        
        # Heal = 15 * (300 / 20) = 225
        assert heal_amount == 225


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
