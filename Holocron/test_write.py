
import sys
with open("test_output.txt", "w") as f:
    f.write("Hello from python\n")
print("Printed to stdout")
print("Printed to stderr", file=sys.stderr)
