"""Run pathfinding visualizer. Must be '__main__'."""

from src.pathfinding.logic import LogicState, run_pathfinding
from src.pathfinding.graph import GraphState, VisText
from src.pathfinding.algorithms import AlgoState
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

    gph = GraphState(graph=[], rects_to_update=[])

    algo = AlgoState(ordinal_node_clicked=[])

    lgc = LogicState()

    txt = VisText()

    run_pathfinding(gph, algo, lgc, txt)


if __name__ == "__main__":
    main()

    # --- Partial Display Update Bugs/Features ---
    # Compare performance with changes
    
    # --- Mutltithreading/Multiprocessing ---
    # May need multiprocessing.freeze_support()
    # 90us for thread startup, linear scaling for func calls
    # 2s for process startup, non linear scaling for increased func calls
    # Update performance section of github with Multiprocessing/Multithreading
    # All performance intensive code
    #   - Cannot update two neighbouring squares if becoming a wall is possible
    #   - Keep pygame on its own processor at all times?
    #       - Whenever calling funcs that update pygame: draw, draw_vis_text, reset_graph, reset_algo
    #       - E.g algo button reset and draw calls are 80ms vs 700ms for entire algo after
    #       - No point if draw call is right before run_pathfinding or other non time critical event
    #   - Key functions speed to check: update_neighbours, change_graph_size,
    #   set_squares_to_roads, 
    #   - node.py
    #       - update_nieghbours
    #       - _update_surrounding_neighbour_pool
    #   - graph.py
    #       - set_graph
    #       - set_squares_to_roads
    #       - reset_graph
    #       - reset_algo
    #   - algorithms.py
    #       - dijkstra
    #       - a_star
    #       - bi_dijkstra
    #       - best_path
    #       - draw_recursive_maze
    # Write tests for both threading and multiprocessing

    # --- Update github page ---
    # Remake gifs
    # In first gif, show adding walls after competion as well
    # Written with a performance first mindset
    #   Only changed pixels update each frame (Took a lot of effort!)
    #   Show 'V' button to prove it actually does this (maze, map a_star then dijk)
    #   Link to archive/V2.0/feature-complete for speed comparisons

    # --- Known Bugs ---
    # Bi dijk redraws open nodes
    # Bi dijk only draws best_path when edges of swarms are touching, mid node
    # Add multithreading to code that iterates through gph.graph

    # --- Features to add ---
    # Sticky mud for patches where algo goes slowly
    # Take in consideration speed limit of roads
    #   Use length of open_set to assign queue_pos
    # Add prim maze
    # Write tests

    # --- C++ Performance Rewrite ---
    # Rewrite node.py, algorithms.py into C++
    # Rewrite all code that iterates through gph.graph, slow when max graph size (Using maps)
    #   Adding _update_surrounding_neighbour_pool() to other set_ methods 0.1x performance in python
    #   Changing to large graph takes 40ms
    # Create new branch 'archive/python_only'
