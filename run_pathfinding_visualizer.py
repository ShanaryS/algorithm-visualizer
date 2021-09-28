"""Run pathfinding visualizer. Must be '__main__'."""

from pathfinding.logic import run_pathfinding as run_pathfinding
from pathfinding.algorithms import AlgoState


def main() -> None:
    """Main function"""

    algo = AlgoState(
        dijkstra_finished=False,
        a_star_finished=False,
        bi_dijkstra_finished=False,
        maze=False,
        ordinal_node_clicked=[]
    )

    run_pathfinding(algo)


if __name__ == '__main__':
    main()
