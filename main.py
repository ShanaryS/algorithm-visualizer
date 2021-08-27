from vis import SearchVisualizer
from vis import SortVisualizer
import numpy as np

if __name__ == '__main__':
    test = [4, 89, 1, 9, 69, 49, 149, 84, 15, 15, 79, 41, 9, 62, 19]  # Original test array. Use as base. 48/49
    test1 = [4, 89, 1, 9, 69, 49, 149, 84, 15, 79, 41, 62, 19]  # No duplicates
    test2 = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]

    dim = 100  # Range from 5 to 100
    test3 = np.random.randint(0, 150, dim)

    numbers = test3
    y = SortVisualizer(numbers)

    y.merge()
    # y.radix()
    # y.quick()
    # y.heap()
    # y.tim()

    # y.insertion()
    # y.selection()
    # y.bubble()

    # y.bogo()

    # ---------------------------------------------------------
    x = SearchVisualizer(numbers)
    x.values_sort()
    k = 121

    # x.binary(k)
    # x.jump(k)
    # x.exponential(k)
    # x.fibonacci(k)
    # x.linear(k)
    # x.comparison(k)
