"""Use python or c++ implementation for certain parts of code.
Only change remove(...).
"""


# For pure python, choose ".py". For maximum C++ usage, choose highest item.
# Going up the chain will override those python implementations with C++.
# Items higher up the chain requires those below.
# Example: "algorithms.h" will also include "square.h" automatically.
# C++ imports are optional but program will always depend on python.
_implementations = {
    "algorithms.h",
    "square.h",
    ".py",
}



######################################################################
_include = _implementations.remove(".py")  # <----- ONLY CHANGE THIS!!! #
######################################################################




# Use these variables to setup import across program. Do not change.
use_square_h = False
use_algorithms_h = False
if _include == ".py":
    pass
elif _include == "square.h":
    use_square_h = True
elif _include == "algorithms.h":
    use_square_h = True
    use_algorithms_h = True