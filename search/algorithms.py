"""Contains searching algorithms"""


import matplotlib.pyplot as plt
import numpy as np
from search.colors import *
from search.values import get_sqrt


def linear(vis_: plt.bar,
           key: int,
           array: np.ndarray,
           array_size: int,
           pause_short: float,
           low: int = 0,
           high: int = None) \
        -> None:
    """Loops through array once and returns the first item of value key. Complexity: Time - O(n), Space - O(1)
    Only algorithm that does not require sorted array. Use to find unsorted index.
    """

    if not high:
        high = array_size

    for i in range(low, high):
        vis_[i].set_color(GOLD)
        plt.pause(pause_short)

        if array[i] != key:
            vis_[i].set_color(RED)
            plt.pause(pause_short)
        elif array[i] == key:
            vis_[i].set_color(GREEN)
            for bar in range(i+1, array_size):
                vis_[bar].set_color(RED)

            plt.draw()
            return


def binary(vis_: plt.bar,
           key: int,
           array: np.ndarray,
           array_size: int,
           pause_long: float,
           low: int = 0,
           high: int = None) \
           -> None:
    """Divides array into halves and checks if key is in that half.
    Continues until no longer possible. Requires sorted array. Complexity: Time - O(log(n)), Space - O(1)
    """

    if not high:  # Necessary as exponential calls binary with it's own high
        high = array_size
    lower: int = low
    upper: int = high

    while high >= low:
        mid = (high + low) // 2

        if mid >= array_size:
            mid = array_size - 1

            if mid == key:
                vis_[mid].set_color(GREEN)
                for bar in range(low - 1, mid):
                    vis_[bar].set_color(RED)

                plt.draw()
                return
            else:
                for bar in range(low - 1, array_size):
                    vis_[bar].set_color(RED)

                plt.draw()
                return

        vis_[mid].set_color(MAGENTA)
        plt.pause(pause_long)

        if array[mid] > key:
            if high < array_size-1:
                upper = high+1
            else:
                upper = high

            for i in range(mid, upper):
                vis_[i].set_color(RED)
            high = mid - 1
        elif array[mid] < key:
            if low > 1:
                lower = low-1
            else:
                lower = low

            for i in range(lower, mid):
                vis_[i].set_color(RED)
            low = mid + 1
        elif array[mid] == key:
            vis_[mid].set_color(GREEN)
            for i in range(lower, mid):
                vis_[i].set_color(RED)
            for i in range(mid+1, upper):
                vis_[i].set_color(RED)

            plt.draw()
            return

    for bar in range(lower, upper):
        vis_[bar].set_color(RED)

    plt.draw()


def jump(vis_: plt.bar,
         key: int,
         array: np.ndarray,
         array_size: int,
         pause_short: float,
         pause_long: float) \
         -> None:
    """Optimization for linear search. Similar to binary but steps by a sqrt(n) instead of halving current window.
    Requires sorted array. Complexity: Time - O(sqrt(n)), Space - O(1)
    """

    step: int = get_sqrt(array_size)
    left: int = 0

    if array[left] > key:
        for bar in range(array_size):
            vis_[bar].set_color(RED)

        plt.draw()
        return

    while left < array_size:
        right = min(array_size-1, left + step)

        vis_[left].set_color(CYAN)
        vis_[right].set_color(CYAN)
        plt.pause(pause_long)

        if array[left] <= key <= array[right]:
            for i in range(right+1, array_size):
                vis_[i].set_color(RED)
            plt.pause(pause_long)

            linear(vis_, key, array, array_size, pause_short, left, right + 1)
            return

        for i in range(left, right+1):
            if i < array_size:
                vis_[i].set_color(RED)

        left += step + 1

    plt.draw()


# Does weird stuff when searching for 48 with array. The height arg for binary search probably is the cause.
def exponential(vis_: plt.bar,
                key: int,
                array: np.ndarray,
                array_size: int,
                pause_long: float) \
                -> None:
    """Optimization for binary search. Faster finding of upper bound.
    Finds upper bound in 2^i operations where i is the desired index. Complexity: Time - O(log(i)), Space - O(1)
    Best when index is relatively close to the beginning of the array, such as with unbounded or infinite arrays
    """

    vis_[0].set_color(GOLD)
    plt.pause(pause_long)
    vis_[0].set_color(RED)

    if array[0] == key:
        for i in range(1, array_size):
            vis_[i].set_color(RED)
        vis_[0].set_color(GREEN)

    i: int = 1
    temp_low: int = 1
    temp: int = 1

    vis_[0].set_color(RED)
    vis_[i].set_color(GOLD)

    while i < array_size and array[i] <= key:
        i *= 2
        if i <= array_size:
            for j in range(temp_low, temp):
                vis_[j].set_color(RED)
            vis_[i].set_color(CYAN)
        plt.pause(pause_long)
        temp = i
        temp_low = int(temp / 2)

    if i <= array_size:
        for j in range(i+1, array_size):
            vis_[j].set_color(RED)

    if i < array_size:
        return binary(vis_, key, array, array_size, pause_long, high=i)
    else:
        return binary(vis_, key, array, array_size, pause_long)


def fibonacci(vis_: plt.bar,
              key: int,
              array: np.ndarray,
              array_size: int,
              pause_long: float) \
              -> None:
    """Creates fibonacci numbers up to the length of the list, then iterates downward until target value is in range
    Useful for very large numbers as it avoids division. Complexity: Time - O(log(n)), Space - O(1)
    """

    fib_minus_2: int = 0
    fib_minus_1: int = 1
    fib: int = fib_minus_1 + fib_minus_2

    vis_[fib_minus_2].set_color(CYAN)
    plt.pause(pause_long)

    while fib < array_size:
        fib_minus_2 = fib_minus_1
        fib_minus_1 = fib
        fib = fib_minus_1 + fib_minus_2

        if fib < array_size:
            vis_[fib].set_color(CYAN)
            plt.pause(pause_long)

    index: int = -1

    while fib > 1:
        i: int = min(index + fib_minus_2, (array_size - 1))

        vis_[i].set_color(MAGENTA)
        plt.pause(pause_long)

        if array[i] < key:
            for j in range(i+1):
                vis_[j].set_color(RED)

            fib = fib_minus_1
            fib_minus_1 = fib_minus_2
            fib_minus_2 = fib - fib_minus_1
            index = i
        elif array[i] > key:
            for j in range(i, array_size):
                vis_[j].set_color(RED)

            fib = fib_minus_2
            fib_minus_1 = fib_minus_1 - fib_minus_2
            fib_minus_2 = fib - fib_minus_1
        elif array[i] == key:
            vis_[i].set_color(GREEN)
            for bar in range(i):
                vis_[bar].set_color(RED)
            for bar in range(i+1, array_size):
                vis_[bar].set_color(RED)

            plt.draw()
            return

    plt.draw()
