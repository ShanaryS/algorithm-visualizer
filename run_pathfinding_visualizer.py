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
    # Dragging updates slowly
    # Add a key that queues up all squares that change until the button is pressed again
    #   Flip all those square colors to purple. This is to verify that only specific nodes are updating
    # Rewrite draw function
    # Compare performance with changes
    # Create a new branch 'archive/pre_partial_display_update' for current main branch

    # --- Update github page ---
    # In first gif, show adding walls after competion as well
    # In features note that only changed pixels update each fresh
    #   Mention that it took a lot of effort!
    # Create git branch 'archive/MVP_of_visualizers' for old folder

    # --- Known Bugs ---
    # Bi dijk redraws open nodes
    # Bi dijk only draws best_path when edges of swarms are touching, mid node
    # Add multithreading to code that iterates through gph.graph

    # --- C++ Performance Rewrite ---
    # Rewrite algorithms.py into C++
    # Rewrite all code that iterates through gph.graph, slow when max graph size (Using maps)
    #   Changing to large graph takes 40ms
    # Create new branch 'archive/python_only'

    # --- Features to add ---
    # Sticky mud for patches where algo goes slowly
    # Take in consideration speed limit of roads
    #   Use length of open_set to assign queue_pos
    # Add prim maze
    # Multithreading (Concurrency, Parallelism)
    # Write tests
