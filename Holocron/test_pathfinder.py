#!/usr/bin/env python3
"""
Test Pathfinder with mock data (no database needed)
"""

import networkx as nx
from pathfinder_engine import PathfinderEngine

# Create mock pathfinder with in-memory graph
class MockPathfinder(PathfinderEngine):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.zones = {}
        
    def build_mock_graph(self):
        """Build graph with mock TWW/DF/SL data"""
        
        # Add zones
        zones_data = [
            (84, "Stormwind City", "Vanilla"),
            (85, "Orgrimmar", "Vanilla"),
            (1670, "Oribos", "Shadowlands"),
            (2112, "Valdrakken", "Dragonflight"),
            (2339, "Dornogal", "TWW"),
            (1220, "Legion Dalaran", "Legion"),
            (125, "Dalaran (Northrend)", "WotLK"),
        ]
        
        for zone_id, name, expansion in zones_data:
            self.zones[zone_id] = {"name": name, "expansion": expansion}
            self.graph.add_node(zone_id, name=name, expansion=expansion)
        
        # Add travel connections
        connections = [
            # Stormwind portals
            (84, 1670, "PORTAL", 10, None),  # SW → Oribos
            (84, 2112, "PORTAL", 10, None),  # SW → Valdrakken
            (84, 2339, "PORTAL", 10, None),  # SW → Dornogal
            (84, 1220, "PORTAL", 10, None),  # SW → Legion Dalaran
            
            # Orgrimmar portals
            (85, 1670, "PORTAL", 10, None),  # Org → Oribos
            (85, 2112, "PORTAL", 10, None),  # Org → Valdrakken
            (85, 2339, "PORTAL", 10, None),  # Org → Dornogal
            
            # Return portals
            (1670, 84, "PORTAL", 10, None),  # Oribos → SW
            (1670, 85, "PORTAL", 10, None),  # Oribos → Org
            (2112, 84, "PORTAL", 10, None),  # Valdrakken → SW
            (2112, 85, "PORTAL", 10, None),  # Valdrakken → Org
            (2339, 84, "PORTAL", 10, None),  # Dornogal → SW
            (2339, 85, "PORTAL", 10, None),  # Dornogal → Org
            
            # Mage teleports (class-specific)
            (84, 85, "MAGE_PORTAL", 5, "Mage"),  # SW ↔ Org
            (85, 84, "MAGE_PORTAL", 5, "Mage"),
            (84, 125, "MAGE_PORTAL", 5, "Mage"),  # Any → Dalaran
            (85, 125, "MAGE_PORTAL", 5, "Mage"),
            (2339, 125, "MAGE_PORTAL", 5, "Mage"),
        ]
        
        for source, dest, method, time, requirements in connections:
            self.graph.add_edge(
                source, dest,
                method=method,
                time=time,
                requirements=requirements or ""
            )
        
        print(f"✓ Mock graph built: {self.graph.number_of_nodes()} zones, {self.graph.number_of_edges()} connections")

if __name__ == "__main__":
    engine = MockPathfinder()
    engine.build_mock_graph()
    
    # Test 1: Simple route
    print("\n" + "="*70)
    print("TEST 1: Stormwind → Oribos (Direct Portal)")
    print("="*70)
    
    result = engine.find_shortest_path(84, 1670)
    if result["success"]:
        print(f"\n✓ Route found! Total time: {result['total_time']} seconds\n")
        for i, step in enumerate(result["steps"], 1):
            print(f"  {i}. {step['from_zone']} → {step['to_zone']}")
            print(f"     Method: {step['method']} ({step['time']}s)")
    else:
        print(f"\n✗ {result['error']}")
    
    # Test 2: Multi-hop route
    print("\n" + "="*70)
    print("TEST 2: Dornogal → Orgrimmar (via Stormwind)")
    print("="*70)
    
    result = engine.find_shortest_path(2339, 85)
    if result["success"]:
        print(f"\n✓ Route found! Total time: {result['total_time']} seconds\n")
        for i, step in enumerate(result["steps"], 1):
            print(f"  {i}. {step['from_zone']} → {step['to_zone']}")
            print(f"     Method: {step['method']} ({step['time']}s)")
    else:
        print(f"\n✗ {result['error']}")
    
    # Test 3: Mage-only shortcut
    print("\n" + "="*70)
    print("TEST 3: Stormwind → Orgrimmar (Mage vs Non-Mage)")
    print("="*70)
    
    # Non-Mage route
    result_warrior = engine.find_shortest_path(84, 85, character_class="Warrior")
    # Mage route
    result_mage = engine.find_shortest_path(84, 85, character_class="Mage")
    
    print(f"\n  Warrior: {result_warrior['total_time']}s ({len(result_warrior['steps'])} steps)")
    if result_warrior["success"]:
        for step in result_warrior["steps"]:
            print(f"    - {step['from_zone']} → {step['to_zone']} ({step['method']})")
    
    print(f"\n  Mage: {result_mage['total_time']}s ({len(result_mage['steps'])} steps)")
    if result_mage["success"]:
        for step in result_mage["steps"]:
            print(f"    - {step['from_zone']} → {step['to_zone']} ({step['method']})")
    
    # Test 4: Reachable zones
    print("\n" + "="*70)
    print("TEST 4: Zones reachable from Dornogal within 20 seconds")
    print("="*70)
    
    reachable = engine.get_reachable_zones(2339, max_time=20)
    print(f"\n  Found {len(reachable)} zones:\n")
    for zone in reachable:
        print(f"  - {zone['zone_name']}: {zone['time']}s ({zone['steps']} steps)")
    
    print("\n" + "="*70)
    print("✓ All tests complete!")
    print("="*70)
