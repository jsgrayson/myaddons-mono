
import re

def check_lua_balance(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    balance = 0
    stack = []
    
    # Simple regex for keywords that start a block
    # function, if, for, while, repeat
    # Note: 'function' can be 'local function' or 'function foo()' or 'foo = function()'
    # 'if' ... 'then'
    # 'repeat' ... 'until' (repeat doesn't use end, it uses until)
    
    # We'll just count 'function', 'if', 'for', 'while' vs 'end'
    # This is a heuristic.
    
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith('--'): continue # Skip comments
        
        # Remove comments at end of line
        line = line.split('--')[0]
        
        # Count keywords
        # We need to be careful about "end" appearing in strings, but for now let's assume simple code.
        
        # Check for 'function'
        # define function: function foo() ... end
        # anonymous function: foo = function() ... end
        if re.search(r'\bfunction\b', line):
            balance += 1
            stack.append(('function', i+1))
            
        if re.search(r'\bif\b', line) and re.search(r'\bthen\b', line):
            # Handle single line if: if x then y end? No, Lua doesn't support single line if without end unless it's not an if block?
            # Actually Lua: if x then y end is valid.
            balance += 1
            stack.append(('if', i+1))
            
        if re.search(r'\bfor\b', line) and re.search(r'\bdo\b', line):
            balance += 1
            stack.append(('for', i+1))
            
        if re.search(r'\bwhile\b', line) and re.search(r'\bdo\b', line):
            balance += 1
            stack.append(('while', i+1))
            
        if re.search(r'\bend\b', line):
            balance -= 1
            if stack:
                stack.pop()
            else:
                print(f"Excess 'end' at line {i+1}")
                
    if balance != 0:
        print(f"Balance is {balance}. Unclosed blocks:")
        for item in stack:
            print(f"{item[0]} at line {item[1]}")
    else:
        print("Balance seems OK.")

check_lua_balance('/Users/jgrayson/Documents/holocron/PetWeaver/PetWeaver.lua')
