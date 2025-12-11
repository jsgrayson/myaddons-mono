import re
import os
from typing import Any, Dict, Optional

class LuaParser:
    """
    Parses World of Warcraft SavedVariables (.lua) files into Python dictionaries.
    These files typically contain a single global table assignment.
    """

    def parse_file(self, file_path: str, variable_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse a Lua SavedVariables file.
        
        Args:
            file_path: Absolute path to the .lua file.
            variable_name: Optional name of the global variable to extract. 
                           If None, tries to infer from the file content.
                           
        Returns:
            A dictionary representing the Lua table.
        """
        if not os.path.exists(file_path):
            print(f"LuaParser: File not found: {file_path}")
            return {}

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # If variable_name is provided, look for "Variable = { ... }"
            # Otherwise, just look for the first assignment "Something = { ... }"
            
            # Simple regex to find the start of the table assignment
            # Pattern: VariableName = {
            pattern = r'(\w+)\s*=\s*\{'
            match = re.search(pattern, content)
            
            if not match:
                print(f"LuaParser: No table assignment found in {file_path}")
                return {}
                
            found_var_name = match.group(1)
            if variable_name and found_var_name != variable_name:
                # If specifically looking for X but found Y first, might need to search specifically
                # For now, assume the file contains the main SV table
                pass

            # Extract the content inside the outer braces
            # This is a naive parser that assumes balanced braces
            start_index = match.end() - 1 # Point to the opening '{'
            
            parsed_data, _ = self._parse_table(content, start_index)
            return parsed_data

        except Exception as e:
            print(f"LuaParser: Error parsing {file_path}: {e}")
            return {}

    def _parse_table(self, text: str, start_index: int) -> tuple[Dict[str, Any] | list, int]:
        """
        Recursive function to parse a Lua table.
        Returns (parsed_object, end_index)
        """
        current_obj = {}
        is_list = True # Assume list until we see a key assignment
        list_items = []
        
        i = start_index + 1 # Skip opening '{'
        length = len(text)
        
        key = None
        
        while i < length:
            char = text[i]
            
            if char == '}':
                # End of table
                if is_list:
                    return list_items, i + 1
                return current_obj, i + 1
            
            elif char == '{':
                # Nested table
                nested_val, new_i = self._parse_table(text, i)
                if key is not None:
                    current_obj[key] = nested_val
                    key = None
                    is_list = False
                else:
                    list_items.append(nested_val)
                i = new_i
                continue
                
            elif char == '[':
                # Key definition ["Key"] = ... or [123] = ...
                # Find closing ']'
                close_bracket = text.find(']', i)
                if close_bracket != -1:
                    key_str = text[i+1:close_bracket]
                    
                    # Check if key is quoted string or number
                    if key_str.startswith('"') and key_str.endswith('"'):
                        key = key_str[1:-1]
                    elif key_str.isdigit():
                        key = int(key_str)
                    else:
                        key = key_str # Fallback
                        
                    # Skip to '='
                    eq_index = text.find('=', close_bracket)
                    if eq_index != -1:
                        i = eq_index + 1
                        is_list = False
                        continue
            
            elif char == '"':
                # String value or key
                # Find closing quote (handling escapes is tricky, doing simple version)
                # Assuming no escaped quotes for MVP
                close_quote = text.find('"', i + 1)
                if close_quote != -1:
                    val = text[i+1:close_quote]
                    
                    # Check if this is a key (followed by =) or a value
                    # Look ahead for '=' ignoring whitespace
                    next_char_idx = close_quote + 1
                    while next_char_idx < length and text[next_char_idx].isspace():
                        next_char_idx += 1
                        
                    if next_char_idx < length and text[next_char_idx] == '=':
                        # It's a key: "Key" = ...
                        key = val
                        i = next_char_idx + 1
                        is_list = False
                        continue
                    else:
                        # It's a value
                        if key is not None:
                            current_obj[key] = val
                            key = None
                        else:
                            list_items.append(val)
                        i = close_quote + 1
                        continue

            elif char == ',':
                # Separator, reset key
                key = None
                i += 1
                continue
                
            elif char.isspace():
                i += 1
                continue
                
            else:
                # Number, boolean, or unquoted string (nil, true, false)
                # Read until comma or closing brace
                j = i
                while j < length and text[j] not in ',}':
                    j += 1
                
                val_str = text[i:j].strip()
                
                # Parse value
                val = val_str
                if val_str == 'true': val = True
                elif val_str == 'false': val = False
                elif val_str == 'nil': val = None
                elif val_str.isdigit(): val = int(val_str)
                else:
                    try:
                        val = float(val_str)
                    except ValueError:
                        pass # Keep as string
                
                if val_str: # Ignore empty
                    if key is not None:
                        current_obj[key] = val
                        key = None
                    else:
                        list_items.append(val)
                
                i = j
                continue
                
            i += 1
            
        return current_obj, i
