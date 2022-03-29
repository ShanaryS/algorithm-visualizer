"""Run search visualizer. Must be '__main__'."""

from src.searching.py.graph import Graph, set_graph
from src.searching.py.utils.values import generate_array, KEY, HESITATE


def main() -> None:
    """Set default values to initialize graph with"""

    array = generate_array(0, 150, 30)
    array_size = len(array)
    labels = [label for label in range(array_size)]

    vis = None
    pause_short = 150 / array_size * 0.01
    pause_long = (pause_short * 3) + (array_size * 0.005)

    g = Graph(
        array=array,
        array_size=array_size,
        labels=labels,
        key=KEY,
        vis=vis,
        pause_short=pause_short,
        pause_long=pause_long,
        hesitate=HESITATE
    )

    set_graph(g, initialize=True)


if __name__ == '__main__':
    main()
    
    # Keeps running in background if closed while algo running.
