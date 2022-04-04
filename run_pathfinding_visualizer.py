"""Run pathfinding visualizer. Must be '__main__'."""


# Handles how much C++ the the program should use
from src.pathfinding.cpp_or_py import use_algorithms_h
if use_algorithms_h:
    from pathfinding_cpp_algorithms import AlgoState
else:
    from src.pathfinding.py.algorithms import AlgoState

from src.pathfinding.py.graph import GraphState, VisText
from src.pathfinding.py.logic import LogicState, run_pathfinding

import sys
import os


def overide_where():
    """Fixes error when compiling program to exe."""

    def _override_where():
        """Helper function"""
        # change this to match the location of cacert.pem
        return os.path.abspath(os.path.join("lib", "cacert.pem"))

    if hasattr(sys, "frozen"):
        import certifi.core

        os.environ["REQUESTS_CA_BUNDLE"] = _override_where()
        certifi.core.where = _override_where

        # delay importing until after where() has been replaced
        import requests.utils
        import requests.adapters

        # replace these variables in case these modules were
        # imported before we replaced certifi.core.where
        requests.utils.DEFAULT_CA_BUNDLE_PATH = _override_where()
        requests.adapters.DEFAULT_CA_BUNDLE_PATH = _override_where()


def main() -> None:
    """Main function"""

    overide_where()

    gph = GraphState(rects_to_update=[])

    algo = AlgoState(ordinal_square_clicked=[])

    lgc = LogicState()

    txt = VisText()

    run_pathfinding(gph, algo, lgc, txt)


if __name__ == "__main__":
    main()

# Have all unordered set funcs return pointers
# Have get neighbours return pointer (set that as opaque as well, move nei)
# Move into vectors
# Update neighbours once in cpp class
# Initalize variables
# Multiple maze generation does look right
# Offload any reasonable functionality into square class

# C++ algo drawing over walls. Colors not being set.
# In general it doesn't seem like instance varaibles are being saved into class.
# Check if get_square for C++ returns a copy. More generally if copies are only forced for containers.
# Walls don't get reset with Space

# --- C++ Performance Rewrite ---
# Change title of pygame to show what is in c++
# Rewrite square.py (Test with python for speed up? Both debug and release.)
# Can potentially use bind_map for unordered_map, use unordered_map instead of unordered_set
# Use Opaque where possible for speed improvements
# Optimise return types. Use correct return value policy for each function.
# Add algo timer to c++ functions?
# algorithms.py into C++
# Create new project and use submodules to separate square and algorithm
# Allow importing square.py into algorithms.h, base it off cpp_or_py.py as well.
# Rewrite algos to not call draw, take in gph.graph directly, use loop to check new rects
#   Adding _update_surrounding_neighbour_pool() to other set_ methods 0.1x performance in python
#   Changing to large graph takes 40ms
# Use -p tag in pyinstaller?
# - https://github.com/pyinstaller/pyinstaller/issues/4073
# - https://stackoverflow.com/a/51992944
# Try to remove external cacert.pem dependency (also lib folder)
# Put json in lib folder
# Add conditional cpp include from json file in readme
# Test debug and release

# (Optimization Station: Things to test to see if faster)
# Store graph in std::array and not nested for a signle block of memory
# Rewrite update_neighbours to only passed need squares to instance
# Use unordered_set for square lists, add hash to class
# Reserve m_neighbours
# Square::get_neighbours replace vector with array by first looping and counting number of neighbours then create an array with that amount. [May no longer need to include vector]
# In set methods either remove guard statement or use something faster than a set (array, vector)
# In set_history impletement switch statement
# In algorithms check if not closed first when setting open
# Define the size of containers using number of rows^2
# Use struct for colors with two attributes, int id and array color, inititalize each into the static variable for the class. Rewrite discard_square using switch statement and color ids.
# Write gph.graph as a single list to optimize cache hits
# Passing square containers by pointers rather than copy
# Test debug and release

# --- Build Systems ---
# https://pybind11.readthedocs.io/en/stable/compiling.html#building-with-cppimport
# https://pybind11.readthedocs.io/en/stable/compiling.html#generating-binding-code-automatically
# https://pybind11.readthedocs.io/en/stable/compiling.html#building-with-cmake

# Update requirements.txt to latest versions

# --- Mutltithreading/Multiprocessing ---
# Maybe just put pygame and logic on two distinct processes at leave it at that
#   - Else probably would need to mantually set processes then manually assign it to everything
#   - Need to already have processes started else there won't be any performance increase
# psutil.cpu_count(logical=True/False), add to requirements.txt
# May need multiprocessing.freeze_support()
# 2ms to 54us for thread startup, linear scaling for func calls
# 1.35s to 600us for process startup, non linear scaling for increased func calls
# https://stackoverflow.com/questions/66018977/using-multiprocessing-with-pygame
# Update performance section of github with Multiprocessing/Multithreading
# All performance intensive code
#   - Cannot update two neighbouring squares if becoming a wall is possible
#   - Keep pygame on its own processor at all times?
#       - Whenever calling funcs that update pygame: draw, draw_vis_text, reset_graph, reset_algo
#       - E.g algo button reset and draw calls are 80ms vs 700ms for entire algo after
#       - No point if draw call is right before run_pathfinding or other non time critical event
#   - run_pathfinding_visualizer.py
#   - square.py (Not invidiually)
#       - _discard_square
#       - clear_all_square_lists
#       - update_nieghbours
#       - _update_surrounding_neighbour_pool
#   - graph.py
#       - set_graph
#       - set_squares_to_roads*
#       - reset_graph
#       - reset_algo
#   - algorithms.py
#       - dijkstra*
#       - a_star*
#       - bi_dijkstra*
#       - best_path*
#       - draw_recursive_maze*
# Write tests for both threading and multiprocessing

# --- Known Bugs ---
# Can place walls during maze, causes crash when dragging over it
# Bi dijk redraws open squares
# Bi dijk only draws best_path when edges of swarms are touching, mid square

# --- Features to add ---
# Sticky mud for patches where algo goes slowly
# Take in consideration speed limit of roads
#   Use length of open_set to assign queue_pos
# Add prim maze
# Write tests
