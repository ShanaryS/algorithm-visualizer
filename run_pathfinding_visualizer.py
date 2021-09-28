"""Run pathfinding visualizer. Must be '__main__'."""

from pathfinding.logic import run_pathfinding as run_pathfinding
from pathfinding.graph import GraphState
from pathfinding.algorithms import AlgoState
from pathfinding.values import ROWS, SQUARE_SIZE


def main() -> None:
    """Main function"""

    gph = GraphState(
        rows=ROWS,
        square_size=SQUARE_SIZE,
        wall_nodes=set(),
        has_img=False,
        img=None
    )

    algo = AlgoState(
        dijkstra_finished=False,
        a_star_finished=False,
        bi_dijkstra_finished=False,
        maze=False,
        ordinal_node_clicked=[],
        best_path_sleep=3
    )

    run_pathfinding(gph, algo)


if __name__ == '__main__':
    main()
