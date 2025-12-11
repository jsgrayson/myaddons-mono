"""
Simplified PetTracker Data Parser

Parses PetTracker data.lua line by line since the tables are on separate lines.
"""

import json
import re
import sys


def parse_lua_array(array_str: str):
    """Parse a simple Lua array like {3,5,8} or {8.5,7.5,8}"""
    # Find all numbers (integers or floats)
    numbers = re.findall(r'[\d.]+', array_str)
    
    # Try to parse as integers first
    try:
        return [int(x) for x in numbers]
    except:
        # If that fails, parse as floats
        return [float(x) for x in numbers]


def parse_lua_nested_dict(dict_str: str) -> dict:
    """
    Parse nested Lua dictionary like:
    {[862]={[2385]="ABC",[2387]="DEF"}, [2248]={...}}
    """
    result = {}
    
    # Match outer level: [key]={...}
    # Use a more sophisticated pattern that handles nested braces
    pos = 0
    while pos < len(dict_str):
        # Find next [key]=
        match = re.search(r'\[(\d+)\]\s*=\s*\{', dict_str[pos:])
        if not match:
            break
            
        outer_key = int(match.group(1))
        brace_start = pos + match.end() - 1  # Position of opening {
        
        # Find matching closing brace
        brace_count = 1
        brace_end = brace_start + 1
        while brace_count > 0 and brace_end < len(dict_str):
            if dict_str[brace_end] == '{':
                brace_count += 1
            elif dict_str[brace_end] == '}':
                brace_count -= 1
            brace_end += 1
        
        inner_content = dict_str[brace_start+1:brace_end-1]
        
        # Check if this is a string dictionary or array
        if '="' in inner_content:
            # String dictionary: [slot]="encoded"
            inner_dict = {}
            for inner_match in re.finditer(r'\[(\d+)\]\s*=\s*"([^"]+)"', inner_content):
                slot = int(inner_match.group(1))
                value = inner_match.group(2)
                inner_dict[slot] = value
            result[outer_key] = inner_dict
        else:
            # Array: {3,5,8} or {8.5,7.5,8}
            result[outer_key] = parse_lua_array(inner_content)
        
        pos = brace_end
    
    return result

def parse_lua_sparse_array(array_str: str) -> dict:
    """
    Parse a sparse Lua array like {_,_,{11},{8},_,{3,5}}
    Returns a dict keyed by index (1-based)
    """
    result = {}
    index = 1
    
    # Simple state machine to parse comma-separated values
    # Values can be '_' (skip) or '{...}' (parse as array)
    
    pos = 0
    # Skip opening brace if present (though passed string usually is inside braces)
    if array_str.startswith('{'):
        array_str = array_str[1:-1]
        
    while pos < len(array_str):
        # Skip whitespace/commas
        while pos < len(array_str) and array_str[pos] in ' ,':
            pos += 1
            
        if pos >= len(array_str):
            break
            
        # Check for placeholder
        if array_str[pos] == '_':
            index += 1
            pos += 1
            continue
            
        # Check for nested table
        if array_str[pos] == '{':
            brace_count = 1
            end = pos + 1
            while brace_count > 0 and end < len(array_str):
                if array_str[end] == '{':
                    brace_count += 1
                elif array_str[end] == '}':
                    brace_count -= 1
                end += 1
            
            content = array_str[pos:end]
            # Parse the inner array (e.g. {3,5})
            result[index] = parse_lua_array(content)
            index += 1
            pos = end
            continue
            
        # Fallback (shouldn't happen in this specific file based on inspection)
        # Just skip to next comma
        while pos < len(array_str) and array_str[pos] != ',':
            pos += 1
        index += 1

    return result


def main():
    """Parse the PetTracker data and save as JSON"""
    
    # Read the raw Lua data from the source file
    with open('/Users/jgrayson/Documents/petweaver/pettracker_data_source.lua', 'r') as f:
        lines = f.readlines()
    
    print("Parsing PetTracker data...")
    print(f"Total lines: {len(lines)}")
    
    species_data = {}
    breeds_data = {}
    stats_data = {}
    
    # Parse line by line
    for i, line in enumerate(lines, 1):
        line = line.strip()
        
        if line.startswith('Addon.Species='):
            print(f"Found Species on line {i}")
            table_str = line[len('Addon.Species='):]
            species_data = parse_lua_nested_dict(table_str)
            
        elif line.startswith('Addon.SpecieBreeds='):
            print(f"Found SpecieBreeds on line {i}")
            table_str = line[len('Addon.SpecieBreeds='):]
            # Remove outer braces for the sparse array parser
            if table_str.startswith('{') and table_str.endswith('}'):
                table_str = table_str[1:-1]
            breeds_data = parse_lua_sparse_array(table_str)
            
        elif line.startswith('Addon.SpecieStats='):
            print(f"Found SpecieStats on line {i}")
            table_str = line[len('Addon.SpecieStats='):]
            # Remove outer braces for the sparse array parser
            if table_str.startswith('{') and table_str.endswith('}'):
                table_str = table_str[1:-1]
            stats_data = parse_lua_sparse_array(table_str)
    
    print(f"\nFound {len(species_data)} species with ability data")
    print(f"Found {len(breeds_data)} species with breed data")
    print(f"Found {len(stats_data)} species with stat data")
    
    # Convert stats to proper format
    formatted_stats = {}
    for species_id, stats in stats_data.items():
        if len(stats) == 3:
            formatted_stats[species_id] = {
                "power": stats[0],
                "speed": stats[1],
                "health": stats[2]
            }
    
    # Combine into a single structure
    combined_data = {
        "species_abilities": species_data,
        "species_breeds": breeds_data,
        "species_stats": formatted_stats,
        "metadata": {
            "source": "PetTracker addon",
            "species_count": len(species_data),
            "breeds_count": len(breeds_data),
            "stats_count": len(formatted_stats),
            "version": "extracted_2025-11-23"
        }
    }
    
    # Save as JSON
    output_path = '/Users/jgrayson/Documents/petweaver/pettracker_data.json'
    with open(output_path, 'w') as f:
        json.dump(combined_data, f, indent=2)
    
    print(f"\nSaved parsed data to: {output_path}")
    
    # Show samples
    if species_data:
        sample_species = list(species_data.keys())[0]
        print(f"\nSample data for species {sample_species}:")
        print(f"  Abilities: {len(species_data[sample_species])} slots")
        if sample_species in breeds_data:
            print(f"  Breeds: {breeds_data[sample_species]}")
        if sample_species in formatted_stats:
            print(f"  Base Stats: {formatted_stats[sample_species]}")
    
    # Show overall statistics
    total_abilities = sum(len(v) for v in species_data.values())
    print(f"\nTotal ability mappings: {total_abilities}")


if __name__ == "__main__":
    main()
