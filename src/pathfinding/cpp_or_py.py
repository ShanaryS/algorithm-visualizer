"""Use python or C++ implementation for certain parts of code.
For pure python, choose ".py". For maximum C++ usage, choose highest item.
Going up the import tree will override those python implementations with C++.
Items higher up the import tree requires those below.
Example: "algorithms.h" will also include "square.h" automatically.
C++ imports are optional but program will always depend on python.
"""


import os
import json


json_name = "include_cpp.json"
json_path = ["lib",]  # Don't use os specific spepartors

try:
    with open(os.path.join(*json_path, json_name), encoding='utf-8') as json_file:
        _use_cpp = json.load(json_file)
except (FileNotFoundError, json.JSONDecodeError):
    with open(os.path.join(*json_path, json_name), 'w', encoding='utf-8') as json_file:
        _use_cpp = {
            "#include": "algorithms.h",
            "How to Use": [
                "Use python or C++ implementation for certain parts of code",
                "For pure python, choose '.py'. For maximum C++ usage, choose highest item.",
                "Going up the import tree will override those python implementations with C++.",
                "Items higher up the import tree requires those below.",
                "Example: 'algorithms.h' will also include 'square.h' automatically.",
                "C++ imports are optional but the program will always depend on python.",
                "######################################################################",
                "--- Import Tree: #include only one ---",
                "algorithms.h",
                "square.h",
                ".py"
            ]
        }
        json.dump(_use_cpp, json_file, indent=4)

# Setup imports across program.
use_square_h = False
use_algorithms_h = False
if _use_cpp["#include"] == ".py":
    pass
elif _use_cpp["#include"] == "square.h":
    use_square_h = True
elif _use_cpp["#include"] == "algorithms.h":
    use_algorithms_h = True