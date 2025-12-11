"""
Monte Carlo Validator for Genetic Algorithm Team Testing

This module provides comprehensive team validation through large-scale simulations
to ensure team stability across varying RNG conditions.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import Counter
import statistics

from .genome import TeamGenome
from .fitness import FitnessEvaluator


@dataclass
class ValidationReport:
    """Results from Monte Carlo validation"""
    team_genome: TeamGenome
    num_simulations: int
    win_count: int
    loss_count: int
    win_rate: float
    confidence_interval: Tuple[float, float]  # (lower, upper) 95% CI
    avg_turns_when_won: float
    avg_turns_when_lost: float
    failure_modes: List[str] = field(default_factory=list)
    rng_sensitivity: str = "Unknown"  # Low, Medium, High
    
    def is_stable(self, threshold: float = 0.95) -> bool:
        """Check if team has stable win rate above threshold"""
        return self.win_rate >= threshold
    
    def summary(self) -> str:
        """Generate human-readable summary"""
        return f"""
Monte Carlo Validation Report
==============================
Simulations: {self.num_simulations}
Win Rate: {self.win_rate:.1%} ({self.win_count}W - {self.loss_count}L)
95% CI: [{self.confidence_interval[0]:.1%}, {self.confidence_interval[1]:.1%}]
Avg Turns (Win): {self.avg_turns_when_won:.1f}
Avg Turns (Loss): {self.avg_turns_when_lost:.1f}
RNG Sensitivity: {self.rng_sensitivity}
Stable: {'✓ YES' if self.is_stable() else '✗ NO'}

Failure Modes:
{chr(10).join(f'  - {mode}' for mode in self.failure_modes) if self.failure_modes else '  None detected'}
"""


class MonteCarloValidator:
    """Validates team stability through large-scale simulations"""
    
    def __init__(self, evaluator: FitnessEvaluator):
        self.evaluator = evaluator
    
    def validate_team(
        self, 
        genome: TeamGenome, 
        num_simulations: int = 1000,
        rng_seed_start: int = 0
    ) -> ValidationReport:
        """
        Run Monte Carlo validation on a team.
        
        Args:
            genome: Team to validate
            num_simulations: Number of battles to simulate
            rng_seed_start: Starting RNG seed
            
        Returns:
            ValidationReport with detailed results
        """
        wins = 0
        losses = 0
        win_turns = []
        loss_turns = []
        loss_reasons = []
        
        # Track which pet dies first in losses
        first_deaths = Counter()
        
        for sim_num in range(num_simulations):
            # Run a single battle with unique seed
            # Note: We need to temporarily set the simulator's seed
            original_seed = self.evaluator.simulator.rng_seed
            self.evaluator.simulator.rng_seed = rng_seed_start + sim_num
            
            result = self.evaluator.play_battle(genome)
            
            # Restore original seed
            self.evaluator.simulator.rng_seed = original_seed
            
            if result['winner'] == 'player':
                wins += 1
                win_turns.append(result['turns'])
            else:
                losses += 1
                loss_turns.append(result['turns'])
                
                # Analyze failure mode
                if result.get('final_state'):
                    # Find which player pet died first
                    for i, pet in enumerate(result['final_state'].player_team.pets):
                        if not pet.stats.is_alive():
                            first_deaths[i] += 1
                            break
                
                # Track loss reason
                if result['turns'] >= 40:
                    loss_reasons.append("Timeout/Stalemate")
                elif result.get('final_state'):
                    alive_enemy = sum(1 for p in result['final_state'].enemy_team.pets if p.stats.is_alive())
                    loss_reasons.append(f"Wiped with {alive_enemy} enemies alive")
        
        # Calculate statistics
        win_rate = wins / num_simulations
        
        # Calculate 95% confidence interval using normal approximation
        # CI = p ± 1.96 * sqrt(p(1-p)/n)
        ci_margin = 1.96 * (win_rate * (1 - win_rate) / num_simulations) ** 0.5
        ci_lower = max(0, win_rate - ci_margin)
        ci_upper = min(1, win_rate + ci_margin)
        
        avg_win_turns = statistics.mean(win_turns) if win_turns else 0
        avg_loss_turns = statistics.mean(loss_turns) if loss_turns else 0
        
        # Identify failure modes
        failure_modes = self._identify_failure_modes(
            loss_reasons, 
            first_deaths, 
            losses,
            num_simulations
        )
        
        # Determine RNG sensitivity
        rng_sensitivity = self._calculate_rng_sensitivity(win_rate, ci_margin)
        
        return ValidationReport(
            team_genome=genome,
            num_simulations=num_simulations,
            win_count=wins,
            loss_count=losses,
            win_rate=win_rate,
            confidence_interval=(ci_lower, ci_upper),
            avg_turns_when_won=avg_win_turns,
            avg_turns_when_lost=avg_loss_turns,
            failure_modes=failure_modes,
            rng_sensitivity=rng_sensitivity
        )
    
    def _identify_failure_modes(
        self, 
        loss_reasons: List[str], 
        first_deaths: Counter, 
        total_losses: int,
        total_sims: int
    ) -> List[str]:
        """Identify common failure patterns"""
        modes = []
        
        if total_losses == 0:
            return ["No losses detected - perfect team!"]
        
        # Check for stalemates
        stalemate_count = sum(1 for r in loss_reasons if "Timeout" in r)
        if stalemate_count > total_sims * 0.05:  # More than 5% stalemates
            modes.append(f"Stalemate in {stalemate_count} battles ({stalemate_count/total_sims:.1%})")
        
        # Check for first pet dying often
        if first_deaths:
            most_fragile_slot, death_count = first_deaths.most_common(1)[0]
            if death_count > total_losses * 0.5:  # Dies first in >50% of losses
                modes.append(f"Slot {most_fragile_slot + 1} dies first in {death_count/total_losses:.1%} of losses")
        
        # Check for RNG-dependent losses
        if 0.80 <= (total_sims - total_losses) / total_sims < 0.98:
            modes.append("RNG-dependent: Team can lose to bad luck (crits/misses)")
        
        return modes if modes else ["Unknown failure pattern"]
    
    def _calculate_rng_sensitivity(self, win_rate: float, ci_margin: float) -> str:
        """Determine how sensitive team is to RNG"""
        if win_rate >= 0.98:
            return "Low - Nearly guaranteed wins"
        elif win_rate >= 0.90:
            if ci_margin < 0.03:
                return "Low - Consistent performance"
            else:
                return "Medium - Some RNG variance"
        elif win_rate >= 0.75:
            return "Medium - RNG matters"
        else:
            return "High - Very RNG dependent"
    
    def quick_validate(self, genome: TeamGenome, threshold: float = 0.95) -> bool:
        """Quick validation with fewer simulations (100)"""
        report = self.validate_team(genome, num_simulations=100)
        return report.is_stable(threshold)
    
    def compare_teams(
        self, 
        teams: List[TeamGenome], 
        num_simulations: int = 500
    ) -> List[ValidationReport]:
        """Compare multiple teams and return sorted by win rate"""
        reports = []
        for team in teams:
            report = self.validate_team(team, num_simulations)
            reports.append(report)
        
        # Sort by win rate (descending)
        reports.sort(key=lambda r: r.win_rate, reverse=True)
        return reports
