import json
import os
from pathlib import Path

def get_move_orders():
    """Loads the pre-calculated NPC move orders from JSON."""
    # Path is relative to this file
    json_path = Path(__file__).resolve().parent.parent / "npc_move_orders.json"
    
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Convert string keys "1" back to int 1 for the simulator
        processed_data = {}
        for npc, pets in data.items():
            processed_data[npc] = {}
            for pet_idx, moves in pets.items():
                # Convert round keys "1" -> 1
                processed_data[npc][int(pet_idx)] = {int(r): m for r, m in moves.items()}
                
        return processed_data
    except FileNotFoundError:
        print(f"Warning: {json_path} not found. NPC AI will guess.")
        return {}
