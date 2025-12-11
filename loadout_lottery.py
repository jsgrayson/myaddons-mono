# loadout_lottery.py
# The Loadout Lottery: Talent Optimization

import sys
import os
from sandbox import Sandbox

class LoadoutLottery:
    def __init__(self):
        self.sandbox = Sandbox()
        
    def run_comparison(self, base_simc, talent_strings):
        """
        Runs a batch simulation comparing multiple talent strings.
        """
        batch_input = ""
        
        # Base profile
        batch_input += base_simc + "\n\n"
        
        # Variations
        for i, talent_str in enumerate(talent_strings):
            batch_input += f"copy=Loadout_{i+1}\n"
            batch_input += f"talents={talent_str}\n\n"
            
        print(f"Running comparison for {len(talent_strings)} loadouts...")
        
        # Run SimC (using sandbox)
        # Note: Sandbox currently runs single sim. We might need to adjust for batch.
        # But SimC JSON output for batch contains multiple players.
        
        # Run SimC (using sandbox)
        results = self.sandbox.run_sim(batch_input, iterations=1000)
        
        if not results:
            print("Simulation failed.")
            return
            
        # Ensure results is a list
        if not isinstance(results, list):
            results = [results]
            
        # Find winner
        winner = max(results, key=lambda x: x['dps'])
        
        print("-" * 40)
        print(f"Simulation Complete: {len(results)} profiles simulated.")
        print("-" * 40)
        
        for res in results:
            is_winner = "*" if res == winner else " "
            print(f"{is_winner} {res['name']}: {res['dps']:.0f} DPS")
            
        print("-" * 40)
        print(f"Winner: {winner['name']} with {winner['dps']:.0f} DPS")
        print(f"Talents: {winner['talents']}")
        
        return winner

if __name__ == "__main__":
    # Example usage
    lottery = LoadoutLottery()
    
    # Mock data
    base = "druid=\"Base\"\nlevel=80\nrace=night_elf\nrole=spell\nspec=balance"
    talents = [
        "CwGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgZmxMmZmZmZmxMzMjZYzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzA",
        "CwGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgZmxMmZmZmZmxMzMjZYzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzB"
    ]
    
    lottery.run_comparison(base, talents)
