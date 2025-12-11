#!/usr/bin/env python3
"""
Project Pathfinder - Intelligent Travel Route Optimizer
Uses graph algorithms to find shortest paths between WoW locations
"""

import networkx as nx
import psycopg2
from typing import List, Dict, Optional, Tuple
import os

class PathfinderEngine:
    """
    Routing engine that calculates optimal travel paths using:
    - Portals
    - Hearthstones (with cooldown awareness)
    - Flight paths
    - Character-specific abilities (Mage teleports, etc.)
    """
    
    def __init__(self, db_url: str, deeppockets_engine=None):
        self.db_url = db_url
        self.deeppockets = deeppockets_engine
        self.graph = nx.DiGraph()  # Directed graph for one-way connections
        self.zones = {}  # zone_id -> {name, expansion}
        
    def build_graph(self):
        """Load zones and travel nodes from database into graph"""
        conn = psycopg2.connect(self.db_url)
        cur = conn.cursor()
        
        # Load zones
        cur.execute("SELECT zone_id, name, expansion FROM pathfinder.zones")
        for zone_id, name, expansion in cur.fetchall():
            self.zones[zone_id] = {"name": name, "expansion": expansion}
            self.graph.add_node(zone_id, name=name, expansion=expansion)
        
        # Load travel connections
        cur.execute("""
            SELECT source_zone_id, dest_zone_id, method, travel_time_seconds, requirements
            FROM pathfinder.travel_nodes
        """)
        
        for source, dest, method, time, requirements in cur.fetchall():
            self.graph.add_edge(
                source, dest,
                method=method,
                time=time,
                requirements=requirements or ""
            )
        
        cur.close()
        conn.close()
        
        print(f"✓ Graph built: {self.graph.number_of_nodes()} zones, {self.graph.number_of_edges()} connections")
        
    def load_mock_data(self):
        """Load mock data for testing without DB"""
        # Add some zones
        self.zones[84] = {"name": "Stormwind", "expansion": "Classic"}
        self.zones[1670] = {"name": "Oribos", "expansion": "Shadowlands"}
        self.zones[1978] = {"name": "Dragon Isles", "expansion": "Dragonflight"}
        self.zones[2022] = {"name": "The Waking Shores", "expansion": "Dragonflight"}
        self.zones[2023] = {"name": "Ohn'ahran Plains", "expansion": "Dragonflight"}
        self.zones[2024] = {"name": "The Azure Span", "expansion": "Dragonflight"}
        self.zones[2025] = {"name": "Thaldraszus", "expansion": "Dragonflight"}
        self.zones[-1] = {"name": "Bank (Stormwind)", "expansion": "Classic"} # Mock Bank Zone
        
        # Add nodes to graph
        for zid, data in self.zones.items():
            self.graph.add_node(zid, **data)
            
        # Add some edges (Mocking a connected world)
        # Hubs
        self.graph.add_edge(84, 1670, method="PORTAL", time=15, requirements="")
        self.graph.add_edge(1670, 84, method="PORTAL", time=15, requirements="")
        self.graph.add_edge(84, 1978, method="BOAT", time=120, requirements="")
        self.graph.add_edge(1978, 84, method="BOAT", time=120, requirements="")
        
        # Dragon Isles connections
        di_zones = [1978, 2022, 2023, 2024, 2025]
        for i in range(len(di_zones)):
            for j in range(len(di_zones)):
                if i != j:
                    self.graph.add_edge(di_zones[i], di_zones[j], method="DRAGONRIDING", time=45, requirements="")
                    
        # Bank connection
        self.graph.add_edge(84, -1, method="WALK", time=30, requirements="")
        self.graph.add_edge(-1, 84, method="WALK", time=30, requirements="")
        
        print(f"✓ Mock Graph built: {self.graph.number_of_nodes()} zones")

    def optimize_route(self, start_zone: int, destinations: List[int]) -> Dict:
        """
        Solve TSP for the given destinations using Nearest Neighbor algorithm.
        """
        if start_zone not in self.graph:
            return {"success": False, "error": f"Start zone {start_zone} not found"}
            
        # Validate destinations
        valid_dests = [d for d in destinations if d in self.graph]
        if len(valid_dests) != len(destinations):
            print(f"Warning: Some destinations were invalid and ignored.")
            
        route = [start_zone]
        current_node = start_zone
        unvisited = set(valid_dests)
        if start_zone in unvisited:
            unvisited.remove(start_zone)
            
        total_time = 0
        steps_details = []
        
        while unvisited:
            nearest_node = None
            min_dist = float('inf')
            best_path_segment = None
            
            for node in unvisited:
                # Find shortest path to this node
                try:
                    path_result = self.find_shortest_path(current_node, node)
                    if path_result["success"]:
                        dist = path_result["total_time"]
                        if dist < min_dist:
                            min_dist = dist
                            nearest_node = node
                            best_path_segment = path_result
                except Exception:
                    continue
            
            if nearest_node is None:
                # Cannot reach remaining nodes
                break
                
            # Add segment to route
            route.append(nearest_node)
            unvisited.remove(nearest_node)
            total_time += min_dist
            current_node = nearest_node
            
            steps_details.append({
                "from": best_path_segment["source"],
                "to": best_path_segment["destination"],
                "time": best_path_segment["total_time"],
                "method": best_path_segment["steps"][0]["method"] if best_path_segment["steps"] else "Walk"
            })
            
        return {
            "success": True,
            "route_order": route,
            "total_time": total_time,
            "segments": steps_details
        }

    def check_quest_items(self, quest_ids: List[int]) -> List[int]:
        """
        Check if items required for these quests are in the bank.
        Returns a list of zone_ids to add to the route (e.g., Bank).
        """
        if not self.deeppockets:
            return []
            
        # Mock Quest DB (Quest ID -> Item ID)
        quest_items = {
            123: 194820, # Quest 123 needs Hochenblume
            456: 200111  # Quest 456 needs Resonant Crystal
        }
        
        extra_stops = set()
        
        for qid in quest_ids:
            item_id = quest_items.get(qid)
            if item_id:
                # Check DeepPockets
                locations = self.deeppockets.search_inventory(str(item_id))
                for loc in locations:
                    if loc['container'] == 'Bank' or loc['container'] == 'Reagent Bank':
                        # Item is in bank! Add Bank Stop.
                        # Assuming Bank is Zone -1 for now (or nearest city)
                        extra_stops.add(-1) 
                        
        return list(extra_stops)

    def load_real_data(self):
        """Load real player data from SavedInstances.json"""
        import json
        json_path = "SavedInstances.json"
        
        if not os.path.exists(json_path):
            print("SavedInstances.json not found. Using mock player data.")
            return

        try:
            with open(json_path, "r") as f:
                data = json.load(f)
            
            # SavedInstances structure: DB.Toons["Realm - Name"]
            db = data.get("DB", {})
            toons = db.get("Toons", {})
            
            # Find most recently active toon
            latest_toon = None
            latest_time = 0
            
            for name, info in toons.items():
                last_seen = info.get("LastSeen", 0)
                if last_seen > latest_time:
                    latest_time = last_seen
                    latest_toon = info
                    
            if latest_toon:
                zone = latest_toon.get("Zone", "Unknown")
                print(f"✓ Loaded real data: Player is in {zone}")
                # Store this for dashboard use
                self.current_player_zone = zone
                
        except Exception as e:
            print(f"Error loading SavedInstances: {e}")
    
    def find_shortest_path(
        self,
        source_zone_id: int,
        dest_zone_id: int,
        character_class: Optional[str] = None,
        hearthstone_available: bool = True
    ) -> Dict:
        """
        Find shortest path between two zones
        
        Args:
            source_zone_id: Starting zone
            dest_zone_id: Destination zone
            character_class: e.g., "Mage" (enables class-specific portals)
            hearthstone_available: Whether hearthstone is off cooldown
        
        Returns:
            {
                "path": [zone_ids],
                "steps": [{zone, method, time}],
                "total_time": seconds,
                "success": bool
            }
        """
        if source_zone_id not in self.graph:
            return {"success": False, "error": f"Source zone {source_zone_id} not found"}
        
        if dest_zone_id not in self.graph:
            return {"success": False, "error": f"Destination zone {dest_zone_id} not found"}
        
        # Create filtered graph based on character abilities
        filtered_graph = self._filter_graph(character_class, hearthstone_available)
        
        try:
            # Use Dijkstra's algorithm with time as weight
            path = nx.shortest_path(
                filtered_graph,
                source=source_zone_id,
                target=dest_zone_id,
                weight='time'
            )
            
            # Calculate steps and total time
            steps = []
            total_time = 0
            
            for i in range(len(path) - 1):
                source = path[i]
                dest = path[i + 1]
                edge_data = filtered_graph[source][dest]
                
                steps.append({
                    "from_zone": self.zones[source]["name"],
                    "to_zone": self.zones[dest]["name"],
                    "method": edge_data["method"],
                    "time": edge_data["time"]
                })
                total_time += edge_data["time"]
            
            return {
                "success": True,
                "path": path,
                "steps": steps,
                "total_time": total_time,
                "source": self.zones[source_zone_id]["name"],
                "destination": self.zones[dest_zone_id]["name"]
            }
            
        except nx.NetworkXNoPath:
            return {
                "success": False,
                "error": f"No path found from {self.zones[source_zone_id]['name']} to {self.zones[dest_zone_id]['name']}"
            }
    
    def _filter_graph(self, character_class: Optional[str], hearthstone_available: bool) -> nx.DiGraph:
        """
        Create filtered graph based on character abilities
        """
        filtered = self.graph.copy()
        
        # Remove edges with unmet requirements
        edges_to_remove = []
        for source, dest, data in filtered.edges(data=True):
            requirements = data.get('requirements', '')
            
            # Filter class-specific abilities
            if requirements:
                if 'Mage' in requirements and character_class != 'Mage':
                    edges_to_remove.append((source, dest))
                elif 'Engineer' in requirements and character_class != 'Engineer':
                    edges_to_remove.append((source, dest))
                elif 'Druid' in requirements and character_class != 'Druid':
                    edges_to_remove.append((source, dest))
            
            # Remove hearthstone connections if on cooldown
            if data.get('method') in ['HEARTHSTONE', 'DALARAN_HEARTHSTONE', 'GARRISON_HEARTHSTONE']:
                if not hearthstone_available:
                    edges_to_remove.append((source, dest))
        
        filtered.remove_edges_from(edges_to_remove)
        return filtered
    
    def get_reachable_zones(self, source_zone_id: int, max_time: int = 120) -> List[Dict]:
        """
        Get all zones reachable within max_time seconds from source
        Useful for "where can I get to quickly?" queries
        """
        reachable = []
        
        for zone_id in self.graph.nodes():
            if zone_id == source_zone_id:
                continue
                
            result = self.find_shortest_path(source_zone_id, zone_id)
            if result["success"] and result["total_time"] <= max_time:
                reachable.append({
                    "zone_id": zone_id,
                    "zone_name": self.zones[zone_id]["name"],
                    "time": result["total_time"],
                    "steps": len(result["steps"])
                })
        
        return sorted(reachable, key=lambda x: x["time"])


if __name__ == "__main__":
    # Test the engine
    from dotenv import load_dotenv
    load_dotenv('/Users/jgrayson/Documents/holocron/.env')
    
    db_url = os.getenv('DATABASE_URL')
    engine = PathfinderEngine(db_url)
    engine.build_graph()
    
    # Test route: Stormwind (84) to Oribos (1670)
    print("\n" + "="*60)
    print("Test Route: Stormwind → Oribos")
    print("="*60)
    
    result = engine.find_shortest_path(84, 1670)
    
    if result["success"]:
        print(f"\n✓ Route found! Total time: {result['total_time']} seconds\n")
        for i, step in enumerate(result["steps"], 1):
            print(f"{i}. {step['from_zone']} → {step['to_zone']}")
            print(f"   Method: {step['method']} ({step['time']}s)\n")
    else:
        print(f"\n✗ Error: {result['error']}")
