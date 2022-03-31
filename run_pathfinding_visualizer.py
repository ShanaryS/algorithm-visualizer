"""Run pathfinding visualizer. Must be '__main__'."""


import sys
import os

from src.pathfinding.py.logic import LogicState, run_pathfinding
from src.pathfinding.py.graph import GraphState, VisText
from src.pathfinding.py.algorithms import AlgoState


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

    gph = GraphState(graph=[], rects_to_update=[])

    algo = AlgoState(ordinal_node_clicked=[])

    lgc = LogicState()

    txt = VisText()

    run_pathfinding(gph, algo, lgc, txt)


if __name__ == "__main__":
    main()

# Passing gph into update_neighbours or just stay with vector

# --- C++ Performance Rewrite ---
# Rewrite node.py (Test with python for speed up?)
# Add algo timer to c++ functions?
# algorithms.py into C++
# May need to write hash for unordered_set
# Rewrite algos to not call draw, take in gph.graph directly, use loop to check new rects
#   Adding _update_surrounding_neighbour_pool() to other set_ methods 0.1x performance in python
#   Changing to large graph takes 40ms
# Use -p tag in pyinstaller?
# - https://github.com/pyinstaller/pyinstaller/issues/4073
# - https://stackoverflow.com/a/51992944
# Try to remove external cacert.pem dependency (also lib folder)

# (Optimization Station: Things to test to see if faster)
# Reserve m_neighbours
# Square::get_neighbours replace vector with array by first looping and counting number of neighbours then create an array with that amount. [May no longer need to include vector]
# In set methods either remove guard statement or use something faster than a set (array, vector)
# In set_history impletement switch statement
# In algorithms check if not closed first when setting open
# Define the size of containers using number of rows^2
# Use struct for colors with two attributes, int id and array color, inititalize each into the static variable for the class. Rewrite discard_node using switch statement and color ids.
# Write gph.graph as a single list to optimize cache hits
# Passing node containers by pointers rather than copy



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
#   - node.py (Not invidiually)
#       - _discard_node
#       - clear_all_node_lists
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
# Bi dijk redraws open nodes
# Bi dijk only draws best_path when edges of swarms are touching, mid node

# --- Features to add ---
# Sticky mud for patches where algo goes slowly
# Take in consideration speed limit of roads
#   Use length of open_set to assign queue_pos
# Add prim maze
# Write tests
