import os
import re
import sys

def check_lua_syntax(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    errors = []
    stack = []
    
    # Simple state machine for block balancing
    # We want to track: function, if, do (loops), and their corresponding 'end'
    # Also track parentheses () and braces {}
    
    # Regex patterns
    # Note: Lua "if" blocks end with "end". "elseif" does not start a new block nesting-wise in terms of "end" count if we treat it right, 
    # but "if ... then" starts one.
    # "function" starts one.
    # "do" starts one (while ... do, for ... do).
    # "repeat ... until" is a pair.
    
    # This is a heuristic checker, not a full parser.
    
    line_num = 0
    for line in lines:
        line_num += 1
        stripped = line.strip()
        
        # Skip comments
        if stripped.startswith('--'):
            continue
        
        # Remove inline comments for analysis
        code_part = re.sub(r'--.*$', '', stripped)
        
        # Check parentheses/braces balance on this line (simple check)
        # This doesn't account for strings, but good enough for a sanity check
        # Actually, let's strip strings first to avoid false positives
        code_no_strings = re.sub(r'(".*?"|\'.*?\')', '', code_part)
        
        open_parens = code_no_strings.count('(')
        close_parens = code_no_strings.count(')')
        if open_parens != close_parens:
            # Multi-line function calls are common, so this might be too strict.
            # Let's just track total balance?
            pass

        # Block balancing
        # Keywords that start blocks: function, if, do, repeat
        # Keywords that end blocks: end, until
        
        # We need to be careful with "end" appearing in strings or variables, but we stripped strings.
        # We need to match whole words.
        
        tokens = re.findall(r'\b(function|if|do|repeat|end|until)\b', code_no_strings)
        
        for token in tokens:
            if token in ['function', 'if', 'do', 'repeat']:
                stack.append((token, line_num))
            elif token == 'end':
                if not stack:
                    errors.append(f"Line {line_num}: Unexpected 'end'")
                else:
                    last_start, _ = stack[-1]
                    if last_start == 'repeat':
                        # 'end' does not close 'repeat', 'until' does
                        # But wait, 'repeat' is closed by 'until'. 'end' closes function, if, do.
                        # If we see 'end' and top is 'repeat', that's an error?
                        # Actually, you can have: repeat if ... end until ...
                        # So 'end' closes the inner 'if'.
                        # If top is 'repeat', we search down stack? No, stack is LIFO.
                        # If top is 'repeat', 'end' is invalid for it.
                        # But maybe we are inside a block inside repeat.
                        pass
                    
                    # Pop matching block
                    # 'end' closes: function, if, do
                    if stack[-1][0] in ['function', 'if', 'do']:
                        stack.pop()
                    else:
                        # Mismatch?
                        # Lua is simple: 'end' closes the most recent open block that isn't 'repeat'
                        # But wait, 'repeat' MUST be closed by 'until'.
                        # So if we hit 'end', the top of stack MUST be function/if/do.
                        errors.append(f"Line {line_num}: 'end' found but open block was '{stack[-1][0]}'")
            
            elif token == 'until':
                if not stack:
                    errors.append(f"Line {line_num}: Unexpected 'until'")
                else:
                    if stack[-1][0] == 'repeat':
                        stack.pop()
                    else:
                        errors.append(f"Line {line_num}: 'until' found but open block was '{stack[-1][0]}'")

    if stack:
        for item in stack:
            errors.append(f"Unclosed block '{item[0]}' starting at line {item[1]}")

    return errors

def scan_directory(root_dir):
    print(f"Scanning {root_dir} for Lua files...")
    has_errors = False
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".lua"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, root_dir)
                
                try:
                    errors = check_lua_syntax(full_path)
                    if errors:
                        print(f"❌ {rel_path}:")
                        for e in errors:
                            print(f"  - {e}")
                        has_errors = True
                    else:
                        print(f"✅ {rel_path}")
                except Exception as e:
                    print(f"⚠️ Could not check {rel_path}: {e}")
                    
    if not has_errors:
        print("\n🎉 All Lua files passed syntax check!")
    else:
        print("\n⚠️ Some files have syntax errors.")

if __name__ == "__main__":
    scan_directory(".")
