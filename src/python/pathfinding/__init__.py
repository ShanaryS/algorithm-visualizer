"""Package for pathfinding visualizer"""


import sys
import os

# This allows less verbose importing for the pathfinding package
_path = os.path.abspath(os.path.join("src", "python"))
if _path not in sys.path:
    sys.path.append(_path)
