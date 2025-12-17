# tools/reassemble_spelldump.py
import re, sys, json

chunks = {}
total = None
pat = re.compile(r"^SWSPELL_CHUNK\|(\d+)\/(\d+)\|(.*)$")

def main():
    if len(sys.argv) < 3:
        print("Usage: python reassemble_spelldump.py <dump.txt> <output.json>")
        return

    try:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading dump file: {e}")
        return

    global total
    count = 0 
    for line in lines:
        line = line.rstrip("\n")
        m = pat.match(line)
        if not m:
            continue
        i = int(m.group(1))
        t_in_line = int(m.group(2))
        
        if total is None: 
            total = t_in_line
        elif total != t_in_line:
            print(f"Warning: total chunk count mismatch in line: {line}")
            
        chunks[i] = m.group(3)
        count += 1

    if total is None:
        print("No valid chunks found in input file.")
        return

    if count < total:
        print(f"Warning: Missing chunks. Found {count}/{total}")

    # Reassemble
    try:
        raw = "".join(chunks[i] for i in range(1, total+1))
        obj = json.loads(raw)
        
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2)
        print(f"Successfully wrote {sys.argv[2]} with {len(obj)} spells.")
        
    except Exception as e:
        print(f"Error processing JSON: {e}")

if __name__ == "__main__":
    main()
