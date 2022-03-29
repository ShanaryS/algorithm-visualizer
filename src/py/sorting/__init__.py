"""Package for sorting visualizer"""


import sys
import os

# This allows less verbose importing for the sorting package
_path = os.path.abspath(os.path.join("src", "py"))
if _path not in sys.path:
    sys.path.append(_path)
