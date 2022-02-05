"""Run pathfinding visualizer. Must be '__main__'."""

from src.pathfinding.logic import LogicState, run_pathfinding
from src.pathfinding.graph import GraphState, VisText
from src.pathfinding.algorithms import AlgoState
import sys
import os


def overide_where():
    """Fixes error when compiling program to exe."""

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


def _override_where():
    """Helper function"""
    # change this to match the location of cacert.pem
    return os.path.abspath(
        os.path.join("venv", "Lib", "site-packages", "certifi", "cacert.pem")
    )


def main() -> None:
    """Main function"""

    gph = GraphState(graph=[], wall_nodes=set())

    algo = AlgoState(ordinal_node_clicked=[])

    lgc = LogicState()

    txt = VisText()

    run_pathfinding(gph, algo, lgc, txt)

    overide_where()


if __name__ == "__main__":
    main()
    # --- Known Bugs ---
    # IMG files does not work when built as .exe
    # On algo completion with mid node, changing them does not update correctly
    # Bi dijk only draws best_path when edges of swarms are touching, mid node
    # (Potential) Maze changes size if window loses focus
    #   pygame.event.set_grab and pygame.mouse.get_focused potential solutions
    # Updating entire screen every frame instead of changed items

    # --- Features to add ---
    # Add second location (Seems pointless as can't zoom too far)
    #   Use markers from maps api, disable clicking, becomes like google maps
    # Sticky mud for patches where algo goes slowly
    # Oil slick where algo goes faster
    # Take in consideration speed limit of roads
    # Instantly update algo when changing walls after completion
    # Add prim maze
    # Multithreading (Concurrency, Parallelism)
    # Async for getting clean img while displaying img_base
    # Write tests
