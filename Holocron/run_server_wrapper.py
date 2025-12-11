
import sys
print("Wrapper starting...")
try:
    import server
    print("Server imported successfully")
except Exception as e:
    print(f"Error importing server: {e}")
except SystemExit as e:
    print(f"Server exited with: {e}")
