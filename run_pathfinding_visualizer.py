"""Run pathfinding visualizer. Must be '__main__'."""


# Handles how much C++ the the program should use
from src.pathfinding.cpp_or_py import use_algorithms_h
if use_algorithms_h:
    from src.pathfinding.cpp.modules import AlgoState
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

    algo = AlgoState()

    lgc = LogicState(ordinal_square_clicked_last_tick=[])

    txt = VisText()

    run_pathfinding(gph, algo, lgc, txt)


if __name__ == "__main__":
    main()

# --- C++ Performance Rewrite ---
# Add to readme, conditional cpp include from json file and title of pygame window
#   Note that #include square.h only paradoxically slows down code from pure python
#   This is due to there then being a lot of passing data back and forth between C++ and Python (thousands of times per second!)
#   through pybind11 which creates overhead.
#   Fun fact: a no-op method call in C++ through pybind11 is 60% slower (1.79us vs 2.87us) than a no-op method call in pure python.
#   Of course this 1us difference is quickly irrelevant if the function does intense work.
#   #include algorithms.h means python never calls C++ directly, but insteads set the task for C++ to run through methods
#   These are one time func calls and thus there is 0 overhead under this mode with the exepction of
#   reading the queue of items that needs to be updated every frame. This locks the thread and blocks the C++ code during that time.
#   With pygame fps at 60 or below, limiting factor is C++. Above 60fps, python accesses the data so frequently
#   that the mutex lock starts delaying the C++ execution. 60fps gives a 16.6ms window, on a large graph
#   the C++ algo can finish in less than 10ms and thus isn't affected.
#   #include algorithms.h has a 50x perf improvement over pure python.
#   Mention CMake to compile C++ code
#   Squares 2d squares laid out as 1d vector for cache efficiency

# (Optimization Station: Things to test to see if faster)
# Square on it's on thread?
#   Implement threading in square access methods. Separate locks for square and algo?
#   Place set_squares to road on that thread to visualize changes
# Multiprocessing for algo, may need to share memory
#   Can safely parrallise set_ square methods? Except for algos?
# Multiple threads for algorithm?
# Simplify code. Remove functions. Use cleaver args like passing in a function

# --- C++ Mutltithreading ---
# Write threading pool class in its own .h and .cpp file. Include in square.cpp and algorithms.cpp.
# Force python version if not enough cores avaiable. Possibly makes it easier to make it multithreaded.
#   If possible try to use a pool that can be reduced to single threaded C++
# psutil.cpu_count(logical=True/False), add to requirements.txt
# Update performance section of github with C++ Multithreading
# All performance intensive code
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

# --- Known Bugs ---
# Bi_Dijkstra mid seems to have wrong best path
#   (maybe if closed check fails, let it through if it's not in either visited)

# --- Features to add ---
# Try to remove external cacert.pem dependency (also lib folder)
# Sticky mud for patches where algo goes slowly
# Take in consideration speed limit of roads
#   Use length of open_set to assign queue_pos
# Add prim maze
# Write tests
# Rewrite messy complicated functions. Split into smaller parts (e.g. draw()?)

# --- Possible API for multiprocessing ---
# Goal is to use multiprocessing.Pipe and pass info using enums for any possibe interaction.
# May need multiprocessing.freeze_support()
#
# def config(self, config_type, options: list) -> None:
#     """Sets the state=self.STATE_* to value. Usually you want to call
#     this function before every start_action() call.
#     """
#     if config_type == self.CONFIG_RUN:
#         self.run_config(*options)
#     elif config_type == self.CONFIG_BEST_PATH_DELAY:
#         self._set_best_path_delay(*options)
#     elif conifg_type == self.CONFIG_RECURSIVE_MAZE_DELAY:
#         self._set_recursive_maze_delay(*options)
#     else:
#         raise NotImplementedError("Invalid config_type provided!")

# def start_action(self, action) -> None:
#     """Starts the action specified by action. Use self.START_* for action.
#     Usually self.config() is called before self.start_action() is called.
#     """
#     if action == self.START_DIJKSTRA:
#         self._run(self.PHASE_ALGO, self.ALGO_DIJKSTRA)
#     elif action == self.START_A_STAR:
#         self._run(self.PHASE_ALGO, self.ALGO_A_STAR)
#     elif action == self.START_BI_DIJKSTRA:
#         self._run(self.PHASE_ALGO, self.ALGO_BI_DIJKSTRA)
#     elif action == self.START_RECURSIVE_MAZE:
#         self._run(self.PHASE_MAZE, self.ALGO_RECURSIVE_MAZE)
#     else:
#         raise NotImplementedError("Invalid action provided!")

# def check(self, state) -> int:
#     """Checks the state provided. Bools are returned as 0 or 1."""
#     if state == self.CHECK_PHASE:
#         res = self._check_phase()
#     elif state == self.CHECK_ALGO:
#         res = self._check_algo()
#     elif state == self.CHECK_FINISHED:
#         res = int(self._check_finished())
#     else:
#         raise NotImplementedError("Invalid state provided!")
#     return res