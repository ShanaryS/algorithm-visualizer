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

    gph = GraphState(graph=[], wall_nodes=set(), rects_to_update=[])

    algo = AlgoState(ordinal_node_clicked=[])

    lgc = LogicState()

    txt = VisText()

    run_pathfinding(gph, algo, lgc, txt)


if __name__ == "__main__":
    main()

    # --- Partial Display Update Bugs/Features ---
    # Instant maze does not draw barriers
    # Text over legend
    # Bidijk slower that other algos
    # Algos too fast
    # Delay in starting algos with converted map
    # Map is not being converted to squares, only moving to background
    # 40ms when reseting large graph, maybe save nodes that aren't reset?
    #   Also optimizes dragging nodes. Futher optimization is to only reset
    #   nodes that will be different under new conditions. Most won't change.
    # Default to large grid? Speed of algos now allow it.
    # Add a key that queues up all squares that change until the button is pressed again
    #   Flip all those square colors to purple. This is to verify that only specific nodes are updating

    # --- Update github page ---
    # In first gif, show adding walls after competion as well
    # In features note that only changed pixels update each fresh
    #   Mention that it took a lot of effort!

    # --- Known Bugs ---
    # Bi dijk only draws best_path when edges of swarms are touching, mid node
    # Updating entire screen every frame instead of changed items
    #   Update the entire text box whenever the update_text func is called
    #   Otherwise only update that square's area when used by anything

    # --- Features to add ---
    # Sticky mud for patches where algo goes slowly
    # Take in consideration speed limit of roads
    #   Use length of open_set to assign queue_pos
    # Add prim maze
    # Multithreading (Concurrency, Parallelism)
    # Write tests
