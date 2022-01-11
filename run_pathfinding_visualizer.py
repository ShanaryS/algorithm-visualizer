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
