import matplotlib.pyplot as plt
from values import get_sqrt
from colors import *


def visualize(vis, res, array_size):
    """Visualizes the final result of search"""

    # res can either be int or list depending on which algorithm called it. Requires different handling
    if isinstance(res, int):
        if res > -1:
            for i in range(array_size):
                vis[i].set_color(MPL_RED)
            vis[res].set_color(MPL_GREEN)
        else:
            for i in range(array_size):
                vis[i].set_color(MPL_RED)

    else:
        if res[0] > -1:
            if res[0] < array_size:
                for i in range(array_size):
                    vis[i].set_color(MPL_RED)
                vis[res[0]].set_color(MPL_GREEN)
        else:
            for i in range(array_size):
                vis[i].set_color(MPL_RED)

    plt.draw()


def linear(vis_, key, array, array_size, pause_short):
    """Loops through array once and returns the first item of value key. Complexity: Time - O(n), Space - O(1)
    Only algorithm that does not require sorted array. Use to find unsorted index.
    """

    for i in range(array_size):
        vis_[i].set_color(MPL_GOLD)
        plt.pause(pause_short)

        if array[i] != key:
            vis_[i].set_color(MPL_RED)
            plt.pause(pause_short)
            if i == array_size-1:
                return visualize(vis_, -i, array_size)
        else:
            for b in range(array_size):
                vis_[b].set_color(MPL_RED)
            return visualize(vis_, i, array_size)


def binary(vis_, key, array, array_size, pause_long, high=None):
    """Divides array into halves and checks if key is in that half.
    Continues until no longer possible. Requires sorted array. Complexity: Time - O(log(n)), Space - O(1)
    """

    if not high:
        high = array_size
    low = 0
    mid = (high + low) // 2
    upper = high

    while high >= low:
        mid = (high + low) // 2

        if mid >= array_size:
            mid = array_size - 1
            if mid == key:
                for i in range(low - 1, mid):
                    vis_[i].set_color(MPL_RED)
                for i in range(mid + 1, upper):
                    vis_[i].set_color(MPL_RED)
                return visualize(vis_, mid, array_size)
            else:
                for i in range(array_size):
                    vis_[i].set_color(MPL_RED)
                plt.draw()
                return

        vis_[mid].set_color(MPL_MAGENTA)
        plt.pause(pause_long)

        if array[mid] > key:
            if high < array_size-2:
                upper = high+1
            else:
                upper = high
            for i in range(mid, upper):
                vis_[i].set_color(MPL_RED)
            high = mid - 1
        elif array[mid] < key:
            if low > 1:
                lower = low-1
            else:
                lower = low
            for i in range(lower, mid):
                vis_[i].set_color(MPL_RED)
            low = mid + 1
        else:
            for i in range(low-1, mid):
                vis_[i].set_color(MPL_RED)
            for i in range(mid+1, upper):
                vis_[i].set_color(MPL_RED)
            return visualize(vis_, mid, array_size)

    if mid != key:
        mid = -1

    for i in range(array_size):
        vis_[i].set_color(MPL_RED)
    return visualize(vis_, mid, array_size)


def jump(vis_, key, array, array_size, pause_short, pause_long):
    """Optimization for linear search. Similar to binary but steps by a sqrt(n) instead of halving current window.
    Requires sorted array. Complexity: Time - O(sqrt(n)), Space - O(1)
    """

    step = int(get_sqrt(array_size))
    left, right = 0, 0

    while left < array_size and array[left] <= key:
        right = min(array_size-1, left + step)

        vis_[left].set_color(MPL_CYAN)
        vis_[right].set_color(MPL_CYAN)
        plt.pause(pause_long)

        if array[left] <= key <= array[right]:
            for i in range(right+1, array_size):
                vis_[i].set_color(MPL_RED)
            plt.pause(pause_long)
            break
        left += step

        for i in range(left):
            if i < array_size:
                vis_[i].set_color(MPL_RED)

    if left >= array_size or array[left] > key:
        if left != key:
            left = -1
        return visualize(vis_, (left, right), array_size)

    right = min(array_size-1, right)
    i = left

    while i <= right and array[i] <= key:
        vis_[i].set_color(MPL_GOLD)
        plt.pause(pause_short)

        if array[i] == key:
            return visualize(vis_, (i, right), array_size)
        vis_[i].set_color(MPL_RED)
        plt.pause(pause_short)
        i += 1

    return visualize(vis_, (-i, right), array_size)


# Does weird stuff when searching for 48 with array. The height arg for binary search probably is the cause.
def exponential(vis_, key, array, array_size, pause_long):
    """Optimization for binary search. Faster finding of upper bound.
    Finds upper bound in 2^i operations where i is the desired index. Complexity: Time - O(log(i)), Space - O(1)
    Best when index is relatively close to the beginning of the array, such as with unbounded or infinite arrays
    """

    vis_[0].set_color(MPL_GOLD)
    plt.pause(pause_long)
    vis_[0].set_color(MPL_RED)

    if array[0] == key:
        for i in range(1, array_size):
            vis_[i].set_color(MPL_RED)
        return 0

    i = temp_low = temp = 1
    vis_[0].set_color(MPL_RED)
    vis_[i].set_color(MPL_GOLD)

    while i < array_size and array[i] <= key:
        i *= 2
        if i <= array_size:
            for j in range(temp_low, temp):
                vis_[j].set_color(MPL_RED)
            vis_[i].set_color(MPL_CYAN)
        plt.pause(pause_long)
        temp = i
        temp_low = int(temp / 2)

    if i <= array_size:
        for j in range(i+1, array_size):
            vis_[j].set_color(MPL_RED)

    if i < array_size:
        return binary(vis_, key, array, array_size, pause_long, high=i)
    else:
        return binary(vis_, key, array, array_size, pause_long)


def fibonacci(vis_, key, array, array_size, pause_long):
    """Creates fibonacci numbers up to the length of the list, then iterates downward until target value is in range
    Useful for very large numbers as it avoids division. Complexity: Time - O(log(n)), Space - O(1)
    """

    fib_minus_2 = 0
    fib_minus_1 = 1
    fib = fib_minus_1 + fib_minus_2
    i = 1

    vis_[fib_minus_2].set_color(MPL_CYAN)
    plt.pause(pause_long)

    while fib < array_size:
        fib_minus_2 = fib_minus_1
        fib_minus_1 = fib
        fib = fib_minus_1 + fib_minus_2

        if fib < array_size:
            vis_[fib].set_color(MPL_CYAN)
            plt.pause(pause_long)

    index = -1

    while fib > 1:
        i = min(index + fib_minus_2, (array_size - 1))

        vis_[i].set_color(MPL_MAGENTA)
        plt.pause(pause_long)

        if array[i] < key:
            for j in range(i+1):
                vis_[j].set_color(MPL_RED)

            fib = fib_minus_1
            fib_minus_1 = fib_minus_2
            fib_minus_2 = fib - fib_minus_1
            index = i
        elif array[i] > key:
            for j in range(i, array_size):
                vis_[j].set_color(MPL_RED)

            fib = fib_minus_2
            fib_minus_1 = fib_minus_1 - fib_minus_2
            fib_minus_2 = fib - fib_minus_1
        else:
            return visualize(vis_, i, array_size)

    if fib_minus_1 and index < (array_size - 1) and array[index + 1] == key:
        return visualize(vis_, index + 1, array_size)

    if i != key:
        i = -1

    return visualize(vis_, i, array_size)
