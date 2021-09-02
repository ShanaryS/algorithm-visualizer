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

    """ Docstrings explaining the file. Module way. https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings
    search_algos, sort_algos, and pathfinder_algos for pure implementation without visuals."""

    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html for bar funcs
    # plt.xticks(x_values, xticks) to change tick name under graph, update list and reset values.

    # TODO UI Elements ------------------------------------------------------------------
    # Use Repl.it for visualizations, different work spaces for each func?
    # Link to github, link to different repl.it for search, sort, and path with buttons similar to blinder
    # -----------------------------------------------------------------------------------
    # Add note: Tidbits about algos
    # Add note: Explain what each color means for each algo
    # -----------------------------------------------------------------------------------
    # Add comments to everything that needs it
    # Allow to go step by step?
    # Animated matplotlib module?
    # Allow comparing multiple algorithms at the same time, subplots maybe
    # Upside down graph?
    # Use fill and overlapping bars for coordinate plane?

    # ---------------------------------------------------------------------------------------------

    # Below was to test without GUI. No longer need doesn't harm to keep
    # test = [4, 89, 1, 9, 69, 49, 149, 84, 15, 15, 79, 41, 9, 62, 19]  # Original test array. Use as base. 48/49
    # test1 = [4, 89, 1, 9, 69, 49, 149, 84, 15, 79, 41, 62, 19]  # No duplicates
    # test2 = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    #
    # size = 100  # Range from 5 to 100
    # test3 = np.random.randint(0, 150, size)
    #
    # values = test3
    # # Sort = SortVisualizer(values)
    # # Sort.set_graph()
    #
    # # Sort.merge()
    # # Sort.radix()
    # # Sort.quick()
    # # Sort.heap()
    # # Sort.tim()
    #
    # # Sort.insertion()
    # # Sort.selection()
    # # Sort.bubble()
    #
    # # Sort.bogo()
    #
    # # ---------------------------------------------------------
    # Search = SearchVisualizer(values)
    # Search.set_graph()
    # key = 83
    #
    # # Search.binary(key)
    # # Search.jump(key)
    # # Search.exponential(key)
    # # Search.fibonacci(key)
    # # Search.linear(key)
    # # Search.comparison(key)
