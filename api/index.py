import os
import sys

# Append the absolute path of 'src' to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from main import app