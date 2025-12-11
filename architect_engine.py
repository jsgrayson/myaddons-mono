#!/usr/bin/env python3
"""
The Architect - Graph-Based Synergy Engine for PetWeaver
Transforms team building from random search to mathematical graph analysis.
"""

import networkx as nx
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class SynergyEdge:
    """Represents a synergy between two pets"""
    pet_a: str
    pet_b: str
    weight: float  # 0.0 to 1.0, higher = stronger synergy
    edge_type: str  # 'damage_multiplier', 'weather', 'speed_control', 'utility'
    setup_ability: str
    payoff_ability: str
    description: str

class ArchitectEngine:
    """
    Graph-based synergy engine.
    Nodes = Pets, Edges = Combos
    """
    
    def __init__(self):
        self.graph = nx.DiGraph()  # Directed graph (A->B is not B->A)
        self.synergies: List[SynergyEdge] = []
        
    def build_hardcoded_graph(self):
        """
        Phase 1: Manually define known powerful combos
        Based on meta strategies and Xu-Fu data
        """
        # Define known synergies
        known_combos = [
            # Ikky + Mechanical Pandaren Dragonling (The Classic)
            SynergyEdge(
                pet_a="Ikky",
                pet_b="Mechanical Pandaren Dragonling",
                weight=0.95,
                edge_type="damage_multiplier",
                setup_ability="Flock",
                payoff_ability="Decoy + Thunderbolt",
                description="Flock applies 100% damage taken debuff. MPD survives with Decoy and nukes."
            ),
            
            # Black Claw + Multi-Hit (Universal Combo)
            SynergyEdge(
                pet_a="Zandalari Anklerender",
                pet_b="Chrominius",
                weight=0.90,
                edge_type="damage_multiplier",
                setup_ability="Black Claw",
                payoff_ability="Howl + Surge of Power",
                description="Black Claw adds flat damage. Surge hits 4 times = massive burst."
            ),
            
            # Curse of Doom + Flock (Val'kyr Combo)
            SynergyEdge(
                pet_a="Unborn Val'kyr",
                pet_b="Ikky",
                weight=0.88,
                edge_type="damage_multiplier",
                setup_ability="Curse of Doom",
                payoff_ability="Flock",
                description="Curse explodes during Flock debuff window for execute damage."
            ),
            
            # Call Blizzard + Deep Freeze (Weather Control)
            SynergyEdge(
                pet_a="Tiny Snowman",
                pet_b="Kun-Lai Runt",
                weight=0.85,
                edge_type="weather",
                setup_ability="Call Blizzard",
                payoff_ability="Deep Freeze",
                description="Blizzard chills enemies. Deep Freeze has 100% stun chance on chilled targets."
            ),
            
            # Sandstorm + Sandstorm Benefits
            SynergyEdge(
                pet_a="Anubisath Idol",
                pet_b="Xu-Fu, Cub of Xuen",
                weight=0.82,
                edge_type="weather",
                setup_ability="Sandstorm",
                payoff_ability="Prowl + Feed",
                description="Sandstorm reduces hit chance. Xu-Fu doesn't care (always hits) and sustains."
            ),
            
            # Speed Swap + Slower Heavy Hitter
            SynergyEdge(
                pet_a="Nether Faerie Dragon",
                pet_b="Emerald Proto-Whelp",
                weight=0.75,
                edge_type="speed_control",
                setup_ability="Arcane Storm",
                payoff_ability="Emerald Dream",
                description="Speed buff lets slow pet move first and heal before enemy attacks."
            ),
            
            # Swarm + Multi-Hit
            SynergyEdge(
                pet_a="Crow",
                pet_b="Hatchling",
                weight=0.80,
                edge_type="damage_multiplier",
                setup_ability="Moth Dust + Call Lightning",
                payoff_ability="Flock",
                description="Elemental damage boost + Flock spam."
            ),
            
            # Nocturnal Strike + Blind Setup
            SynergyEdge(
                pet_a="Teroclaw Hatchling",
                pet_b="Any Pet with Nocturnal Strike",
                weight=0.70,
                edge_type="utility",
                setup_ability="Nature's Ward (Heal)",
                payoff_ability="Nocturnal Strike",
                description="Dodge + heal stalling, then execute with Nocturnal Strike."
            ),
        ]
        
        # Build graph
        for synergy in known_combos:
            self.add_synergy(synergy)
            
        print(f"✓ Architect: Built hardcoded graph with {len(self.synergies)} synergies")
        
    def add_synergy(self, synergy: SynergyEdge):
        """Add a synergy edge to the graph"""
        self.graph.add_edge(
            synergy.pet_a,
            synergy.pet_b,
            weight=synergy.weight,
            edge_type=synergy.edge_type,
            setup=synergy.setup_ability,
            payoff=synergy.payoff_ability,
            description=synergy.description
        )
        self.synergies.append(synergy)
        
    def find_best_core(self, enemy_team=None, my_collection: Optional[List[str]] = None) -> List[Tuple[str, str]]:
        """
        Find the top 5 strongest 2-pet cores
        
        Args:
            enemy_team: Optional enemy team context (future feature)
            my_collection: Optional filter to only suggest pets the user owns
            
        Returns:
            List of (pet_a, pet_b) tuples, sorted by synergy weight
        """
        # Get all edges sorted by weight
        edges = sorted(
            self.graph.edges(data=True),
            key=lambda x: x[2]['weight'],
            reverse=True
        )
        
        # Filter by collection if provided
        if my_collection:
            edges = [
                (a, b, data) for a, b, data in edges
                if a in my_collection and b in my_collection
            ]
        
        # Return top 5 cores
        cores = [(edge[0], edge[1]) for edge in edges[:5]]
        return cores
    
    def get_synergy_score(self, pet_a: str, pet_b: str) -> float:
        """Get the synergy weight between two pets"""
        if self.graph.has_edge(pet_a, pet_b):
            return self.graph[pet_a][pet_b]['weight']
        return 0.0
    
    def explain_synergy(self, pet_a: str, pet_b: str) -> str:
        """Get human-readable explanation of synergy"""
        if self.graph.has_edge(pet_a, pet_b):
            data = self.graph[pet_a][pet_b]
            return f"{pet_a} → {pet_b}: {data['description']} (Weight: {data['weight']})"
        return f"No synergy found between {pet_a} and {pet_b}"
    
    def get_statistics(self) -> Dict:
        """Get graph statistics"""
        return {
            "total_pets": self.graph.number_of_nodes(),
            "total_synergies": self.graph.number_of_edges(),
            "avg_synergies_per_pet": self.graph.number_of_edges() / max(self.graph.number_of_nodes(), 1),
            "strongest_synergy": max(
                ((u, v, d['weight']) for u, v, d in self.graph.edges(data=True)),
                key=lambda x: x[2],
                default=("None", "None", 0.0)
            )
        }
    
    def get_most_connected_pets(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Find pets with the most synergies (out-degree)
        These are "flex picks" that work in many teams
        """
        degrees = dict(self.graph.out_degree())
        sorted_pets = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
        return sorted_pets[:top_n]
    
    def suggest_third_pet(self, core: Tuple[str, str], my_collection: Optional[List[str]] = None) -> List[str]:
        """
        Given a 2-pet core, suggest a third pet
        Looks for pets that synergize with either pet in the core
        """
        pet_a, pet_b = core
        
        # Find all pets that synergize with either core pet
        candidates = set()
        
        # Check successors (pets that benefit from core)
        candidates.update(self.graph.successors(pet_a))
        candidates.update(self.graph.successors(pet_b))
        
        # Check predecessors (pets that set up for core)
        candidates.update(self.graph.predecessors(pet_a))
        candidates.update(self.graph.predecessors(pet_b))
        
        # Remove core pets themselves
        candidates.discard(pet_a)
        candidates.discard(pet_b)
        
        # Filter by collection
        if my_collection:
            candidates = {pet for pet in candidates if pet in my_collection}
        
        # Sort by average synergy weight with both core pets
        def avg_synergy(pet):
            score_a = self.get_synergy_score(pet, pet_a) + self.get_synergy_score(pet_a, pet)
            score_b = self.get_synergy_score(pet, pet_b) + self.get_synergy_score(pet_b, pet)
            return (score_a + score_b) / 2
        
        sorted_candidates = sorted(candidates, key=avg_synergy, reverse=True)
        return sorted_candidates[:5]
    
    def suggest_with_alternatives(self, my_collection: List[str], pet_factory=None, limit: int = 5) -> List[Dict]:
        """
        Suggest teams with alternatives for pets the player doesn't own.
        
        Args:
            my_collection: List of pet names the player owns
            pet_factory: Optional PetFactory for finding alternatives
            limit: Max teams to suggest
            
        Returns:
            List of dicts with {'core': (pet_a, pet_b), 'alternatives': {...}}
        """
        suggestions = []
        cores = self.find_best_core()
        
        for pet_a, pet_b in cores[:limit]:
            suggestion = {
                'core': (pet_a, pet_b),
                'weight': self.get_synergy_score(pet_a, pet_b),
                'alternatives': {}
            }
            
            # Check if player owns these pets
            if pet_a not in my_collection:
                # Find alternatives for pet_a
                if pet_factory:
                    alts = pet_factory.find_alternatives(pet_a, self, my_collection, limit=3)
                    suggestion['alternatives'][pet_a] = alts
                else:
                    suggestion['alternatives'][pet_a] = []
            
            if pet_b not in my_collection:
                # Find alternatives for pet_b
                if pet_factory:
                    alts = pet_factory.find_alternatives(pet_b, self, my_collection, limit=3)
                    suggestion['alternatives'][pet_b] = alts
                else:
                    suggestion['alternatives'][pet_b] = []
            
            suggestions.append(suggestion)
        
        return suggestions
    
    def load_from_xufu(self, xufu_path: str = "deprecated/variations_with_scripts.json", 
                       species_path: str = "species_data.json", 
                       min_weight: float = 0.6):
        """
        Phase 2: Auto-discover synergies from Xu-Fu strategy data
        
        Args:
            xufu_path: Path to variations_with_scripts.json
            species_path: Path to species_data.json (ID -> name mapping)
            min_weight: Minimum weight threshold for adding edges (0.0-1.0)
        """
        import json
        from itertools import combinations
        from collections import Counter
        
        print(f"\n🔍 Mining Xu-Fu strategies for synergies...")
        
        # Load species mapping
        with open(species_path, 'r') as f:
            species_data = json.load(f)
        
        def get_pet_name(species_id):
            """Convert species ID to pet name"""
            sid = str(species_id)
            if sid in species_data:
                return species_data[sid]['name']
            # For unknown IDs (NPC IDs), use placeholder
            return f"Pet_{species_id}"
        
        # Load Xu-Fu strategies
        with open(xufu_path, 'r') as f:
            strategies = json.load(f)
        
        # Track pet pair frequencies
        pair_counter = Counter()
        synergies_found = 0
        total_teams = 0
        
        # Process all encounters
        for encounter_name, variations in strategies.items():
            for variation in variations:
                team = variation['team']
                
                # Filter out 0 (empty slots)
                valid_pets = []
                for species_id in team:
                    if species_id != 0:
                        name = get_pet_name(species_id)
                        valid_pets.append(name)
                
                if len(valid_pets) >= 2:
                    total_teams += 1
                    # Count all pairs in this team
                    for pet_a, pet_b in combinations(valid_pets, 2):
                        # Directional edge (order matters)
                        pair_counter[(pet_a, pet_b)] += 1
        
        # Convert frequency to synergy weights
        max_frequency = max(pair_counter.values()) if pair_counter else 1
        
        for (pet_a, pet_b), count in pair_counter.most_common():
            # Normalize to 0.6-0.95 range
            # Popular combos (high frequency) get higher weight
            weight = 0.6 + (count / max_frequency) * 0.35
            
            if weight >= min_weight:
                # Check if edge already exists (don't overwrite hardcoded ones)
                if not self.graph.has_edge(pet_a, pet_b):
                    synergy = SynergyEdge(
                        pet_a=pet_a,
                        pet_b=pet_b,
                        weight=round(weight, 2),
                        edge_type="xu-fu_proven",
                        setup_ability="Unknown",
                        payoff_ability="Unknown",
                        description=f"Proven combo from Xu-Fu (used in {count} strategies)"
                    )
                    self.add_synergy(synergy)
                    synergies_found += 1
        
        print(f"✓ Discovered {synergies_found} new synergies from Xu-Fu data")
        print(f"  Teams analyzed: {total_teams}")
        print(f"  Unique pairs found: {len(pair_counter)}")
        print(f"  Graph now has {self.graph.number_of_edges()} total synergies")

# ============================================================================
# FUTURE: Phase 2 - Heuristic Edge Detection
# ============================================================================
def auto_detect_edges(pet_data):
    """
    Auto-detect synergies by parsing ability metadata
    TODO: Implement in Phase 2
    """
    pass

# ============================================================================
# Phase 3 - ML-Based Learning
# ============================================================================
class ArchitectLearner:
    """
    Learns new synergies from Dojo Engine victories.
    Creates a feedback loop: Dojo discovers → Architect learns → Better seeds.
    """
    
    def __init__(self, architect: ArchitectEngine):
        self.architect = architect
        self.victory_history = []  # Track all winning teams
        self.learning_threshold = 0.7  # Min win rate to add edge
        
    def learn_from_generation(self, teams_with_scores: List[tuple]):
        """
        Learn from one Dojo generation.
        
        Args:
            teams_with_scores: List of (Team, win_rate) tuples
        """
        from itertools import combinations
        from collections import Counter
        
        # Filter high-performing teams
        winners = [
            team for team, score in teams_with_scores 
            if score >= self.learning_threshold
        ]
        
        if not winners:
            return
        
        # Extract pet pairs from winning teams
        pair_wins = Counter()
        
        for team in winners:
            # Get all pet pairs in this team
            pet_names = [pet.name for pet in team.pets]
            
            for pet_a, pet_b in combinations(pet_names, 2):
                pair_wins[(pet_a, pet_b)] += 1
        
        # Add/strengthen edges for frequent pairs
        synergies_learned = 0
        synergies_strengthened = 0
        
        for (pet_a, pet_b), count in pair_wins.items():
            if count >= 2:  # Appeared in at least 2 winning teams
                if self.architect.graph.has_edge(pet_a, pet_b):
                    # Strengthen existing edge
                    current_weight = self.architect.graph[pet_a][pet_b]['weight']
                    new_weight = min(0.95, current_weight + 0.05)  # Cap at 0.95
                    self.architect.graph[pet_a][pet_b]['weight'] = new_weight
                    synergies_strengthened += 1
                else:
                    # Add new learned edge
                    synergy = SynergyEdge(
                        pet_a=pet_a,
                        pet_b=pet_b,
                        weight=0.65,  # Start with moderate weight
                        edge_type="learned",
                        setup_ability="Discovered",
                        payoff_ability="Discovered",
                        description=f"Learned from victories (appeared in {count} winning teams)"
                    )
                    self.architect.add_synergy(synergy)
                    synergies_learned += 1
        
        if synergies_learned > 0 or synergies_strengthened > 0:
            print(f"🧠 Architect learned: +{synergies_learned} new, ↑{synergies_strengthened} strengthened")
        
        # Track history
        self.victory_history.extend(winners)
        
    def prune_weak_edges(self, min_weight: float = 0.4):
        """
        Remove weak synergies that haven't proven themselves.
        Only affects "learned" edges, not hardcoded or Xu-Fu ones.
        """
        edges_to_remove = []
        
        for u, v, data in self.architect.graph.edges(data=True):
            if data.get('edge_type') == 'learned' and data['weight'] < min_weight:
                edges_to_remove.append((u, v))
        
        for u, v in edges_to_remove:
            self.architect.graph.remove_edge(u, v)
        
        if edges_to_remove:
            print(f"✂️  Pruned {len(edges_to_remove)} weak synergies")
        
        return len(edges_to_remove)
    
    def get_statistics(self) -> Dict:
        """Get learning statistics"""
        learned_edges = sum(
            1 for u, v, d in self.architect.graph.edges(data=True) 
            if d.get('edge_type') == 'learned'
        )
        
        return {
            "total_victories_analyzed": len(self.victory_history),
            "learned_synergies": learned_edges,
            "graph_size": self.architect.graph.number_of_edges()
        }


if __name__ == "__main__":
    # Test the Architect
    print("\n" + "="*70)
    print("THE ARCHITECT - Synergy Graph Engine")
    print("="*70)
    
    engine = ArchitectEngine()
    engine.build_hardcoded_graph()
    
    # Get statistics (Phase 1)
    stats = engine.get_statistics()
    print(f"\n📊 Graph Statistics (Phase 1 - Hardcoded):")
    print(f"  Total Pets: {stats['total_pets']}")
    print(f"  Total Synergies: {stats['total_synergies']}")
    print(f"  Strongest Synergy: {stats['strongest_synergy'][0]} → {stats['strongest_synergy'][1]} ({stats['strongest_synergy'][2]})")
    
    # Phase 2: Load from Xu-Fu
    print(f"\n" + "="*70)
    print("PHASE 2: XU-FU MINING")
    print("="*70)
    try:
        engine.load_from_xufu()
        
        # Stats after Xu-Fu mining
        stats2 = engine.get_statistics()
        print(f"\n📊 Graph Statistics (After Xu-Fu Mining):")
        print(f"  Total Pets: {stats2['total_pets']}")
        print(f"  Total Synergies: {stats2['total_synergies']}")
        print(f"  New synergies discovered: {stats2['total_synergies'] - stats['total_synergies']}")
        
    except FileNotFoundError as e:
        print(f"\n⚠️  Xu-Fu data not found: {e}")
        print(f"   Skipping Phase 2 mining demo")
    
    # Find best cores
    print(f"\n🔥 Top 5 Strongest Cores:")
    cores = engine.find_best_core()
    for i, (a, b) in enumerate(cores, 1):
        weight = engine.get_synergy_score(a, b)
        print(f"  {i}. {a} + {b} (Weight: {weight})")
    
    # Most connected pets
    print(f"\n🌟 Most Versatile Pets (Flex Picks):")
    flex_picks = engine.get_most_connected_pets(5)
    for pet, count in flex_picks:
        print(f"  {pet}: {count} synergies")
    
    print("\n" + "="*70)
    print("✓ Architect Engine Test Complete!")
    print("="*70)
