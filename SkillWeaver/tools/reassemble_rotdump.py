# tools/reassemble_rotdump.py
import re, sys, json

pat = re.compile(r"^SWROT_CHUNK\|(\d+)\/(\d+)\|(.*)$")

def main():
    if len(sys.argv) < 3:
        print("Usage: python reassemble_rotdump.py <dump.txt> <output.json>")
        return

    chunks = {}
    total = None
    
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading input: {e}")
        return

    count = 0
    for line in lines:
        m = pat.match(line.rstrip("\n"))
        if not m:
            continue
        i = int(m.group(1))
        t_in_line = int(m.group(2))
        
        if total is None: total = t_in_line
        elif total != t_in_line:
            print(f"Warning: Chunk total mismatch at chunk {i}")

        chunks[i] = m.group(3)
        count += 1
        
    if total is None:
        print("No SWROT_CHUNK lines found")
        return
        
    if count < total:
        print(f"Warning: Found {count}/{total} chunks")

    try:
        raw = "".join(chunks[i] for i in range(1, total + 1))
        obj = json.loads(raw)

        with open(sys.argv[2], "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2)

        print(f"Successfully wrote {sys.argv[2]}") 
        print(f"Specs exported: {len(obj)}")
    except Exception as e:
        print(f"Error reassembling JSON: {e}")

if __name__ == "__main__":
    main()
