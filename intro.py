import sys

print("Missionaries and Cannibals - search project")
print("Python version:", sys.version.split()[0])

try:
    import networkx
    import matplotlib
    print("networkx and matplotlib are installed. Setup is ready!")
except ImportError:
    print("A library is missing. Run: pip install -r requirements.txt")