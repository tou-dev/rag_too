import os
import sys

# Get the absolute path to the 'src' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "..", "src"))

# Insert 'src' at the very beginning of sys.path
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from main import app