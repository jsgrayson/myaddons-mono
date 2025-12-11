# fabricator.py
# The Fabricator: Multi-Alt Crafting Dependency Graph

import psycopg2
import networkx as nx
from collections import defaultdict

class Fabricator:
    def __init__(self, db_connection_string):
        self.conn_str = db_connection_string
        
    def get_db(self):
        return psycopg2.connect(self.conn_str)
        
    def build_dependency_graph(self, target_item_id, quantity):
        """
        Builds a directed graph of dependencies to craft the target item.
        Returns the graph and a list of steps.
        """
        G = nx.DiGraph()
        steps = []
        
        # Queue: (item_id, quantity_needed)
        queue = [(target_item_id, quantity)]
        
        # Cache to avoid re-querying same item
        visited = set()
        
        with self.get_db() as conn:
            with conn.cursor() as cur:
                while queue:
                    item_id, qty = queue.pop(0)
                    
                    if item_id in visited:
                        continue
                    visited.add(item_id)
                    
                    G.add_node(item_id, quantity=qty)
                    
                    # 1. Check Inventory (Holocron)
                    # For now, assume 0 inventory to force crafting logic
                    # In real implementation, subtract inventory from needed qty
                    
                    # 2. Find Recipe
                    cur.execute("""
                        SELECT r.recipe_id, r.name, r.min_yield, r.max_yield
                        FROM fabricator.recipes r
                        WHERE r.crafted_item_id = %s
                    """, (item_id,))
                    recipe = cur.fetchone()
                    
                    if recipe:
                        recipe_id, recipe_name, min_yield, max_yield = recipe
                        avg_yield = (min_yield + max_yield) / 2
                        crafts_needed = (qty / avg_yield)
                        
                        # Find who can craft it
                        cur.execute("""
                            SELECT character_guid 
                            FROM fabricator.character_recipes 
                            WHERE recipe_id = %s
                            LIMIT 1
                        """, (recipe_id,))
                        crafter = cur.fetchone()
                        crafter_guid = crafter[0] if crafter else None
                        
                        G.nodes[item_id]['action'] = 'CRAFT'
                        G.nodes[item_id]['crafter'] = crafter_guid
                        G.nodes[item_id]['recipe_id'] = recipe_id
                        
                        # Get Reagents
                        cur.execute("""
                            SELECT item_id, count 
                            FROM fabricator.reagents 
                            WHERE recipe_id = %s
                        """, (recipe_id,))
                        reagents = cur.fetchall()
                        
                        for reagent_id, reagent_count in reagents:
                            total_reagent_qty = reagent_count * crafts_needed
                            G.add_edge(reagent_id, item_id, quantity=total_reagent_qty)
                            queue.append((reagent_id, total_reagent_qty))
                            
                    else:
                        # No recipe -> Base Material
                        G.nodes[item_id]['action'] = 'BUY/FARM'
                        
        return G

    def generate_plan(self, G):
        """
        Topological sort to determine order of operations.
        """
        try:
            order = list(nx.topological_sort(G))
        except nx.NetworkXUnfeasible:
            print("Error: Cycle detected in crafting graph!")
            return []
            
        plan = []
        for item_id in order:
            node = G.nodes[item_id]
            if 'action' in node:
                step = {
                    'item_id': item_id,
                    'action': node['action'],
                    'quantity': node.get('quantity', 0) # This might be wrong, need to sum incoming edges
                }
                if node['action'] == 'CRAFT':
                    step['crafter'] = node.get('crafter')
                    step['recipe'] = node.get('recipe_id')
                
                plan.append(step)
                
        return plan

# Mock usage
if __name__ == "__main__":
    # fab = Fabricator("dbname=holocron user=postgres")
    # G = fab.build_dependency_graph(12345, 1)
    # plan = fab.generate_plan(G)
    pass
