from vis import SearchVisualizer
from vis import SortVisualizer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

if __name__ == '__main__':
    test = [4, 89, 1, 9, 69, 49, 149, 84, 15, 15, 79, 41, 9, 62, 19]  # Original test array. Use as base. 48/49
    test1 = [4, 89, 1, 9, 69, 49, 149, 84, 15, 79, 41, 62, 19]  # No duplicates
    test2 = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]

    size = 100  # Range from 5 to 100
    test3 = np.random.randint(0, 150, size)

    values = test3
    # Sort = SortVisualizer(values)
    # Sort.set_graph()

    # Sort.merge()
    # Sort.radix()
    # Sort.quick()
    # Sort.heap()
    # Sort.tim()

    # Sort.insertion()
    # Sort.selection()
    # Sort.bubble()

    # Sort.bogo()

    # ---------------------------------------------------------
    Search = SearchVisualizer(values)
    Search.set_graph()
    key = 83

    # Search.binary(key)
    # Search.jump(key)
    # Search.exponential(key)
    # Search.fibonacci(key)
    # Search.linear(key)
    # Search.comparison(key)
