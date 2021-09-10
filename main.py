# Need to copy from test.py
from vis_search import SearchVisualizer
from vis_sort import SortVisualizer
from vis_path import PathfindingVisualizer

if __name__ == '__main__':
    Search = SearchVisualizer()
    Sort = SortVisualizer()

    # Search.set_graph()
    # Sort.set_graph()

    Path = PathfindingVisualizer()
    Path.main()
