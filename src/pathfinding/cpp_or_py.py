"""Use python or c++ implementation for certain parts of code.
For pure python, choose ".py". For maximum C++ usage, choose highest item.
Going up the import tree will override those python implementations with C++.
Items higher up the import tree requires those below.
Example: "algorithms.h" will also include "square.h" automatically.
C++ imports are optional but program will always depend on python.
"""

######################################################################
_include = ".py"  # <----- ONLY CHANGE THIS!!! #
######################################################################
""" --- Import Tree: Choose One ---
    "algorithms.h"
    "square.h"
    ".py"
"""

# Setup imports across program.
use_square_h = False
use_algorithms_h = False
if _include == ".py":
    pass
elif _include == "square.h":
    use_square_h = True
elif _include == "algorithms.h":
    use_square_h = True
    use_algorithms_h = True