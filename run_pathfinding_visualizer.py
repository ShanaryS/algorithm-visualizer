"""Run pathfinding visualizer. Must be '__main__'."""

from pathfinding.logic import LogicState, run_pathfinding
from pathfinding.graph import GraphState
from pathfinding.algorithms import AlgoState


def main() -> None:
    """Main function"""

    gph = GraphState(graph=[], wall_nodes=set())

    algo = AlgoState(ordinal_node_clicked=[])

    lgc = LogicState()

    run_pathfinding(gph, algo, lgc)


if __name__ == '__main__':
    main()
