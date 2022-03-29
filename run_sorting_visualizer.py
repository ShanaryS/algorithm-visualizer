"""Run sort visualizer. Must be '__main__'."""

from src.py.sorting.graph import Graph, set_graph
from src.py.sorting.utils.values import generate_array


def main() -> None:
    """Set default values to initialize graph with"""

    array = generate_array(0, 150, 30)
    array_size = len(array)
    labels = [label for label in range(array_size)]
    is_sorted = False

    vis = None  # Created in set_graph. Defining here would be redundant
    pause_short = 150 / array_size * 0.01
    pause_mid = (pause_short * 3) + (array_size * 0.001)
    pause_long = (pause_short * 3) + (array_size * 0.005)

    g = Graph(
        array=array,
        array_size=array_size,
        labels=labels,
        is_sorted=is_sorted,
        vis=vis,
        pause_short=pause_short,
        pause_mid=pause_mid,
        pause_long=pause_long
    )

    set_graph(g)


if __name__ == '__main__':
    main()
