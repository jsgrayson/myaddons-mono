
import unittest
from unittest.mock import MagicMock
from genetic.fitness import FitnessEvaluator
from genetic.genome import TeamGenome, PetGene
from simulator.battle_state import PetStats

class TestFitnessStats(unittest.TestCase):
    def test_genome_to_team_uses_pt_stats(self):
        # Setup
        target_team = MagicMock()
        ability_db = {}
        species_db = {}
        
        evaluator = FitnessEvaluator(target_team, ability_db, species_db)
        
        # Mock PetTracker stats
        # Species 123: Base 8/8/8
        evaluator.pt_base_stats = {
            "123": {"health": 8, "power": 8, "speed": 8}
        }
        
        # Create genome with species 123
        genome = TeamGenome()
        genome.pets = [PetGene(123)]
        
        # Convert to team
        team = evaluator._genome_to_team(genome)
        pet = team.pets[0]
        
        # Check stats
        # Expected: HP=8*175=1400, Power=8*35=280, Speed=8*35=280
        self.assertEqual(pet.stats.max_hp, 1400)
        self.assertEqual(pet.stats.power, 280)
        self.assertEqual(pet.stats.speed, 280)
        
    def test_genome_to_team_fallback(self):
        # Setup
        target_team = MagicMock()
        ability_db = {}
        species_db = {}
        
        evaluator = FitnessEvaluator(target_team, ability_db, species_db)
        evaluator.pt_base_stats = {} # Empty
        
        # Create genome with unknown species 999
        genome = TeamGenome()
        genome.pets = [PetGene(999)]
        
        # Convert to team
        team = evaluator._genome_to_team(genome)
        pet = team.pets[0]
        
        # Check fallback stats (1400/280/280)
        self.assertEqual(pet.stats.max_hp, 1400)
        self.assertEqual(pet.stats.power, 280)
        self.assertEqual(pet.stats.speed, 280)

if __name__ == '__main__':
    unittest.main()
