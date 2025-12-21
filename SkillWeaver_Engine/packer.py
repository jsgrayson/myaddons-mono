import os

# Files to ignore
IGNORE_DIRS = {'.git', '.vscode', '.idea', 'libs', 'textures', 'media'}
# Extensions to include (adjust for your specific addon needs)
INCLUDE_EXTS = {'.lua', '.xml', '.toc', '.md', '.txt'}

output_file = "codebase_dump.txt"

def pack_repo():
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Walk the current directory
        for root, dirs, files in os.walk("."):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in INCLUDE_EXTS:
                    file_path = os.path.join(root, file)
                    
                    # Write file header
                    outfile.write(f"\n{'='*50}\n")
                    outfile.write(f"FILE: {file_path}\n")
                    outfile.write(f"{'='*50}\n")
                    
                    # Write file content
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                    except Exception as e:
                        outfile.write(f"Error reading file: {e}\n")

    print(f"Done! All code saved to {output_file}")

if __name__ == "__main__":
    pack_repo()
