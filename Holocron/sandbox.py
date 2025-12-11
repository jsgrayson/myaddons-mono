# sandbox.py
# The Sandbox: Local SimulationCraft Integration

import subprocess
import json
import os
import sys
import shutil
import shutil

# Configuration
def find_simc():
    # Check environment variable
    if os.getenv("SIMC_PATH"):
        return os.getenv("SIMC_PATH")
        
    # Check standard PATH
    if shutil.which("simc"):
        return "simc"
        
    # Check common macOS locations
    common_paths = [
        "/Applications/SimulationCraft.app/Contents/MacOS/simc",
        "/Applications/SimulationCraft-11.0.2.app/Contents/MacOS/simc", # Update version as needed
        os.path.expanduser("~/Applications/SimulationCraft.app/Contents/MacOS/simc")
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
            
    # Fallback (will likely fail if not in PATH)
    return "simc"

SIMC_PATH = find_simc()

class Sandbox:
    def __init__(self, simc_path=None):
        self.simc_path = simc_path or SIMC_PATH
        
    def run_sim(self, simc_input, iterations=1000, json_output=True):
        """
        Runs a simulation with the given input string.
        """
        # Create temporary input file
        input_file = "temp_sim.simc"
        with open(input_file, "w") as f:
            f.write(simc_input)
            f.write(f"\niterations={iterations}\n")
            if json_output:
                f.write("json2=temp_result.json\n")
                
        # Run SimC
        cmd = [self.simc_path, input_file]
        try:
            print(f"Running SimC: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"SimC Error: {result.stderr}")
                return None
                
            # Parse JSON output
            if json_output and os.path.exists("temp_result.json"):
                with open("temp_result.json", "r") as f:
                    data = json.load(f)
                
                # Cleanup
                os.remove(input_file)
                os.remove("temp_result.json")
                
                return self.parse_results(data)
                
            return result.stdout
            
        except FileNotFoundError:
            print(f"Error: SimC executable not found at {self.simc_path}")
            return None
            
    def parse_results(self, data):
        """
        Extracts key metrics from SimC JSON output.
        Returns a list of result objects if multiple players, or a single object if one.
        """
        try:
            sim = data['sim']
            players = sim['players']
            
            parsed_results = []
            
            for player in players:
                res = {
                    "name": player['name'],
                    "dps": player['collected_data']['dps']['mean'],
                    "dps_min": player['collected_data']['dps']['min'],
                    "dps_max": player['collected_data']['dps']['max'],
                    "talents": player.get('talents'),
                    "gear_ilvl": player.get('gear_ilvl_mean'),
                    "timestamp": sim['options']['timestamp']
                }
                
                # Stat weights if available
                if 'scale_factors' in player:
                    res['weights'] = player['scale_factors']
                    
                parsed_results.append(res)
                
            if len(parsed_results) == 1:
                return parsed_results[0]
            return parsed_results
            
        except KeyError as e:
            print(f"Error parsing JSON: {e}")
            return None

if __name__ == "__main__":
    # Example usage
    sandbox = Sandbox()
    
    # Check if input file provided
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            sim_input = f.read()
        
        result = sandbox.run_sim(sim_input)
        if result:
            print(json.dumps(result, indent=2))
    else:
        print("Usage: python sandbox.py <simc_input_file>")
