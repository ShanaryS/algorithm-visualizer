"""Package for searching visualizer"""


import sys
import os

# This allows less verbose importing for the searching package
_path = os.path.abspath(os.path.join("src", "python"))
if _path not in sys.path:
    sys.path.append(_path)
