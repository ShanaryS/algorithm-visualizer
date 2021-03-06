"""Contains sorting algorithms"""


from src.sorting.py.utils.colors import *
import matplotlib.pyplot as plt
import numpy as np
from src.sorting.py.utils.values import generate_array, get_factorial


def selection(vis: plt.bar,
              array: np.ndarray,
              array_size: int,
              pause_short: float,
              pause_mid: float) \
              -> None:

    """Goes through list comparing values of the current number to all values after, swapping as needed.
    Complexity: Time - O(n^2), Space - O(1), Unstable
    """

    for i in range(array_size - 1):
        vis[i].set_color(BLACK)
        plt.pause(pause_mid)

        index: int = i
        for j in range(i + 1, array_size):
            vis[j].set_color(GOLD)
            plt.pause(pause_short)

            if array[j] < array[index]:
                vis[j].set_color(CYAN)
                if index != i:
                    vis[index].set_color(GOLD)

                index = j

        # Swaps bars while maintaining color for each
        vis[i].set_height(array[index])
        vis[i].set_color(CYAN)
        array[i], array[index] = array[index], array[i]
        vis[index].set_height(array[index])
        vis[index].set_color(BLACK)
        plt.pause(pause_mid)

        vis[i].set_color(GREEN)
        for b in range(i+1, array_size):
            vis[b].set_color(DEFAULT)

        if i == array_size-2:
            for b in range(i, array_size):
                vis[b].set_color(GREEN)

    plt.draw()


def insertion(vis: plt.bar,
              array: np.ndarray,
              array_size: int,
              pause_short: float) \
              -> None:

    """Splits input into the sorted and unsorted parts. Places unsorted elements to the correct position.
    Complexity: Time - O(n^2), Space - O(1), Stable
    """

    for i in range(1, array_size):
        a: int = i

        vis[a].set_color(RED)

        while a > 0 and array[a] < array[a - 1]:
            # Swaps bars while maintaining color for each
            vis[a].set_color(RED)
            vis[a-1].set_color(GOLD)
            plt.pause(pause_short)
            vis[a].set_color(DEFAULT)
            vis[a-1].set_color(DEFAULT)

            vis[a].set_height(array[a-1])
            array[a], array[a-1] = array[a-1], array[a]
            vis[a-1].set_height(array[a-1])

            a -= 1
        else:
            if a < array_size-1:
                vis[a+1].set_color(GOLD)
            vis[a].set_color(RED)
            plt.pause(pause_short)
            if a < array_size-1:
                vis[a+1].set_color(DEFAULT)
            vis[a].set_color(DEFAULT)

    for b in range(array_size):
        vis[b].set_color(GREEN)
    plt.draw()


def bubble(vis: plt.bar,
           array: np.ndarray,
           array_size: int,
           pause_short: float) \
           -> None:

    """Swaps adjacent elements if they are in the wrong order.
    Repeats n-1 times with max index to check decreasing by 1.
    Complexity: Time - O(n^2), Space - O(1), Stable
    """

    for i in range(array_size - 1):
        for j in range(0, array_size-i - 1):
            vis[j].set_color(RED)
            vis[j+1].set_color(GOLD)
            plt.pause(pause_short)

            if array[j] > array[j+1]:
                # Swaps bars while maintaining color for each
                vis[j].set_height(array[j+1])
                vis[j].set_color(GOLD)
                array[j], array[j+1] = array[j+1], array[j]
                vis[j+1].set_height(array[j+1])
                vis[j+1].set_color(RED)
                plt.pause(pause_short)

            vis[j].set_color(DEFAULT)
            vis[j+1].set_color(DEFAULT)

            if j == array_size-i - 2:
                vis[j+1].set_color(GREEN)

    vis[0].set_color(GREEN)
    plt.draw()


def heap(vis: plt.bar,
         array: np.ndarray,
         array_size: int,
         pause_short: float,
         pause_long: float) \
         -> None:

    """Converts input into a max heap data structure and pops values.
    Complexity: Time - O(nlog(n)), Space - O(1), Unstable
    """

    # Puts values in heap
    for i in range(array_size // 2 - 1, -1, -1):
        _heap(vis, array, pause_short, array_size, i)

    # Show that values are now in heap
    for b in range(array_size):
        vis[b].set_color(BLACK)
    plt.pause(pause_long)

    # Sorts values from min to max, max first
    for i in range(array_size - 1, 0, -1):
        vis[i].set_color(GOLD)
        vis[0].set_color(GOLD)
        for b in range(i):
            vis[b].set_color(BLACK)
        plt.pause(pause_short)
        for b in range(i):
            vis[b].set_color(DEFAULT)

        vis[i].set_height(array[0])
        array[i], array[0] = array[0], array[i]
        vis[0].set_height(array[0])
        vis[i].set_color(GREEN)
        plt.pause(pause_short)
        vis[0].set_color(DEFAULT)

        _heap(vis, array, pause_short, i, 0)

    vis[0].set_color(GREEN)
    plt.draw()


def _heap(vis: plt.bar,
          array: np.ndarray,
          pause_short: float,
          length: int,
          i: int) \
          -> None:

    """Helper function for heap"""

    largest: int = i
    left: int = 2 * i + 1
    right: int = 2 * i + 2

    vis[i].set_color(GOLD)

    if left < length:
        vis[left].set_color(GOLD)
        if array[largest] < array[left]:
            largest = left

    if right < length:
        vis[right].set_color(GOLD)
        if array[largest] < array[right]:
            largest = right

    plt.pause(pause_short)

    if largest != i:
        vis[i].set_color(RED)
        vis[largest].set_color(RED)
        plt.pause(pause_short)

        vis[i].set_height(array[largest])
        array[i], array[largest] = array[largest], array[i]
        vis[largest].set_height(array[largest])
        plt.pause(pause_short)

        _heap(vis, array, pause_short, length, largest)

    vis[i].set_color(DEFAULT)
    if left < length:
        vis[left].set_color(DEFAULT)
    if right < length:
        vis[right].set_color(DEFAULT)


def quick(vis: plt.bar,
          array: np.ndarray,
          array_size: int,
          pause_short: float,
          start: int = 0,
          end: int = -1) \
          -> None:

    """Sets a pivot value and places every value below the pivot before and all values greater after.
    Repeats recursively until only single element partitions remains.
    Complexity: Time - O(nlog(n)), Space - O(log(n)), Unstable
    """

    if end == -1:
        end = array_size - 1

    if end <= start:
        return

    high = _quick(vis, array, pause_short, start, end)

    quick(vis, array, array_size, pause_short, start, high)

    quick(vis, array, array_size, pause_short, high + 1, end)

    if end == array_size-1:
        vis[end].set_color(GREEN)
        vis[end-1].set_color(GREEN)  # Sometimes this one is colored.
        plt.draw()


def _quick(vis: plt.bar,
           array: np.ndarray,
           pause_short: float,
           start: int,
           end: int) \
           -> int:

    """Helper function for quick"""

    mid: int = start + (end - start) // 2
    pivot: int = array[mid]

    vis[mid].set_color(MAGENTA)
    plt.pause(pause_short)

    low: int = start
    high: int = end

    done: bool = False
    while not done:
        while array[low] < pivot:
            if low != mid:
                vis[low].set_color(RED)
                plt.pause(pause_short)
            low += 1

        while pivot < array[high]:
            if high != mid:
                vis[high].set_color(CYAN)
                plt.pause(pause_short)
            high -= 1

        if low >= high:
            done = True
        else:
            if low != mid:
                vis[low].set_color(CYAN)
            if high != mid:
                vis[high].set_color(RED)
            plt.pause(pause_short)
            if low != mid and high != mid:
                vis[low].set_color(RED)
                vis[high].set_color(CYAN)
            elif low == mid and high == mid:
                vis[mid].set_color(MAGENTA)     # Does nothing. Avoiding using pass
            elif low == mid:
                vis[low].set_color(RED)
                vis[high].set_color(MAGENTA)
            elif high == mid:
                vis[high].set_color(CYAN)
                vis[low].set_color(MAGENTA)

            vis[low].set_height(array[high])
            array[low], array[high] = array[high], array[low]
            vis[high].set_height(array[high])
            plt.pause(pause_short)

            low += 1
            high -= 1

    for b in range(start, end+1):
        vis[b].set_color(DEFAULT)

    if end - start <= 1:
        for i in range(end+1):
            vis[i].set_color(GREEN)

    return high


def merge(vis: plt.bar,
          array: np.ndarray,
          array_size: int,
          pause_short: float,
          i: int = 0,
          key: int = -1) \
          -> None:

    """Recursively splits input in halves. Sorts each element at each level bottom up.
    Complexity: Time - O(nlog(n)), Space - O(n), Stable
    """

    if key == -1:
        key = array_size - 1

    if i < key:
        j: int = (i + key) // 2

        merge(vis, array, array_size, pause_short, i, j)
        merge(vis, array, array_size, pause_short, j + 1, key)

        _merge(vis, array, array_size, pause_short, i, j, key)

    if i == 0 and key == array_size - 1:
        plt.draw()


def _merge(vis: plt.bar,
           array: np.ndarray,
           array_size: int,
           pause_short: float,
           i: int,
           j: int,
           key: int) \
           -> None:

    """Helper function for merge"""

    merged_size: int = key - i + 1
    merged_numbers: list = [0] * merged_size
    merge_pos: int = 0
    left_pos: int = i
    right_pos: int = j + 1

    left_bar, right_bar = left_pos, right_pos
    temp: np.ndarray = array.copy()

    # Compares left and right merge and places lowest of each first.
    while left_pos <= j and right_pos <= key:
        vis[left_bar].set_color(RED)
        vis[right_bar].set_color(GOLD)
        plt.pause(pause_short)

        # If left bar less, it's already in place.
        if array[left_pos] <= array[right_pos]:
            if i != 0 or key != array_size-1:
                vis[left_bar].set_color(DEFAULT)
            else:
                vis[left_bar].set_color(GREEN)
            vis[right_bar].set_color(DEFAULT)
            left_bar += 1

            merged_numbers[merge_pos] = array[left_pos]
            left_pos += 1

        # If right bar is less, shifts everything in between left and right bar to the right.
        # Moves right bar to the left spot, moves the left bar one spot ahead.
        else:
            t = temp.copy()
            temp[left_bar] = array[right_pos]
            for b in range(left_bar, right_bar):
                temp[b + 1] = t[b]
                vis[b].set_height(temp[b])
            left_bar += 1
            vis[left_bar].set_color(RED)
            vis[right_bar].set_height(temp[right_bar])
            vis[right_bar].set_color(DEFAULT)
            right_bar += 1
            plt.pause(pause_short)
            if i != 0 or key != array_size-1:
                vis[left_bar-1].set_color(DEFAULT)
            else:
                vis[left_bar-1].set_color(GREEN)
            vis[left_bar].set_color(DEFAULT)

            merged_numbers[merge_pos] = array[right_pos]
            right_pos += 1

        merge_pos += 1

    # Runs when right merge ends before left merge. Rest of left's values are just added as it's already sorted.
    while left_pos <= j:
        vis[left_bar].set_color(MAGENTA)
        plt.pause(pause_short)
        if i != 0 or key != array_size-1:
            vis[left_bar].set_color(DEFAULT)
        else:
            vis[left_bar].set_color(GREEN)
        left_bar += 1

        merged_numbers[merge_pos] = array[left_pos]
        left_pos += 1
        merge_pos += 1

    # Runs when left merge ends before right merge. Rest of right's values are just added as it's already sorted.
    while right_pos <= key:
        vis[right_bar].set_color(MAGENTA)
        plt.pause(pause_short)

        for b in range(left_bar, right_bar):  # Shifts bars between left and right-1 over by 1
            vis[b + 1].set_height(array[b])
        left_bar += 1
        vis[left_bar-1].set_height(array[right_pos])  # Moves right bar to left bar's original position
        vis[right_bar].set_color(DEFAULT)  # Removes right bar's original position's color
        vis[left_bar-1].set_color(MAGENTA)    # Adds color to current right bar
        plt.pause(pause_short)
        if i != 0 or key != array_size - 1:
            vis[left_bar-1].set_color(DEFAULT)  # Removes right bar's color
        else:
            vis[left_bar-1].set_color(GREEN)
        right_bar += 1

        merged_numbers[merge_pos] = array[right_pos]
        right_pos += 1
        merge_pos += 1

    # Commits the current sorted values to array. Redundant for visualization but necessary for the sort.
    for merge_pos in range(merged_size):
        array[i + merge_pos] = merged_numbers[merge_pos]


# Seems to use insertion too much. Possibly a bug.
def tim(vis: plt.bar,
        array: np.ndarray,
        array_size: int,
        pause_short: float) \
        -> None:

    """Combination of merge sort and insertion sort.
    Divides input into blocks, sorts using insertion, combines using merge.
    Complexity: Time - O(nlog(n)), Space - O(1), Stable
    """

    min_run = _min_run(array_size)

    for start in range(0, array_size, min_run):
        insertion(vis, array, array_size, pause_short)

    size: int = min_run
    while size < array_size:

        for left in range(0, array_size, 2 * size):

            mid: int = min(array_size - 1, left + size - 1)
            right: int = min((left + 2 * size - 1), (array_size - 1))

            if mid < right:
                _merge(vis, array, array_size, pause_short, left, mid, right)

        size *= 2


def _min_run(n: int) -> int:
    """Minimum size needed for merge sort, else insertion sort"""

    MIN_MERGE: int = 51

    r: int = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r


def radix(vis: plt.bar,
          array: np.ndarray,
          array_size: int,
          pause_short: float,
          pause_long: float) \
          -> None:

    """Only for integers. Places values into buckets from the least to most significant digit. Sorts with buckets
    Complexity: Time - O(n*k), Space - O(n+k), Stable
    """

    buckets: list = []
    for i in range(10):
        buckets.append([])

    max_digits: int = _radix_max(array)
    array = list(array)
    pow_10: int = 1

    for digit_index in range(max_digits):
        for num in array:
            bucket_index: int = (abs(num) // pow_10) % 10
            buckets[bucket_index].append(num)

        color: str = ''  # Used so each digit gets it's own color.
        temp: list[np.ndarray] = array.copy()

        if pow_10 == 1:
            color = CYAN
        elif pow_10 == 10:
            color = MAGENTA
        elif pow_10 == 100:
            color = RED
        elif pow_10 == 1000:
            color = BLACK

        array.clear()
        for bucket in buckets:
            array.extend(bucket)
            bucket.clear()

        # Main tool for visualizing. Needs to be complicated to push values to the right rather than just replace.
        for b in range(array_size):
            index: int = temp.index(array[b])
            vis[b].set_color(color)
            vis[index].set_color(GOLD)
            plt.pause(pause_short)

            t: list[np.ndarray] = temp.copy()
            temp[b] = array[b]
            for i in range(b, index):
                temp[i + 1] = t[i]
                vis[i].set_height(temp[i])
            vis[index].set_height(temp[index])
            vis[index].set_color(DEFAULT)
            plt.pause(pause_short)
            if digit_index != max_digits-1:
                vis[b].set_color(DEFAULT)
            else:
                vis[b].set_color(GREEN)

        plt.pause(pause_long)

        pow_10 *= 10

    negatives: list = []
    non_negatives: list = []
    for num in array:
        if num < 0:
            negatives.append(num)
        else:
            non_negatives.append(num)
    negatives.reverse()
    array.clear()
    array.extend(negatives + non_negatives)

    plt.draw()
    # set_graph()    # To reset so other funcs can use. Causes reset after it's finished.


def _radix_max(array: np.ndarray) -> int:
    """Finds the number with the maximum amount of digits"""

    max_digits: int = 0
    for num in array:
        digit_count = _radix_length(num)
        if digit_count > max_digits:
            max_digits = digit_count

    return max_digits


def _radix_length(num: int) -> int:
    """Finds the number of digits for a number"""

    if num == 0:
        return 1

    digits: int = 0
    while num != 0:
        digits += 1
        num = int(num / 10)
    return digits


def bogo(vis: plt.bar,
         array: np.ndarray,
         array_size: int,
         pause_short: float) \
         -> None:

    """Equivalent of throwing a deck of cards in the air, picking them up randomly hoping it's sorted
    Complexity: Time - O(n*n!), Space - O(1), Unstable
    """

    EXPECTED_RUN_TIME: float = ((get_factorial(array_size)) / 4)
    text: str

    if EXPECTED_RUN_TIME < 60:
        text = f"This should be solved in about {round(EXPECTED_RUN_TIME, 2)} SECONDS"
    elif EXPECTED_RUN_TIME < 3600:
        text = f"""Expected solve time is {round((EXPECTED_RUN_TIME / 60), 2)} MINUTES."
Dare to increase array size?"""
    elif EXPECTED_RUN_TIME < 86400:
        text = f""""Only {round((EXPECTED_RUN_TIME / 3600), 2)} HOURS?
C'mon, that's over in the blink of an eye"""
    elif EXPECTED_RUN_TIME < 604800:
        text = f""""This is now your day job?
You'll be payed in {round((EXPECTED_RUN_TIME / 86400), 2)} DAYS"""
    elif EXPECTED_RUN_TIME < 2.628**6:
        text = f"""Family? Friends? The outside world?
Bah! You're gonna be here for {round((EXPECTED_RUN_TIME / 604800), 2)} WEEKS"""
    elif EXPECTED_RUN_TIME < 3.154**7:
        text = f"""This is some serious dedication you have, waiting for {round((EXPECTED_RUN_TIME / 2.628**6), 2)}"
MONTHS. But since you're, here might as well go all the way right?"""
    elif EXPECTED_RUN_TIME < 3.154**107:
        text = f"""Here you discover the meaning of life. Get comfortable. This make take 
time. Only {round((EXPECTED_RUN_TIME / 3.154**7), 2)} YEARS"""
    else:
        text = f"""Congratulations! You won! What did you win? Well you'll just have to wait a 
measly {round((EXPECTED_RUN_TIME / 3.154 ** 7), 2)} YEARS to find out.
(The universe dies at 10e+100 YEARS btw.)"""

    plt.suptitle(text)

    while not _is_sorted(array, array_size):
        _shuffle(array, array_size)
        for b in range(array_size):
            vis[b].set_height(array[b])
        plt.pause(pause_short)

    for i in range(array_size):
        vis[i].set_color(GREEN)
    plt.draw()


def _is_sorted(array: np.ndarray, array_size: int) -> bool:
    """Checks if array is sorted"""

    for b in range(0, array_size - 1):
        if array[b] > array[b + 1]:
            return False
    return True


def _shuffle(array: np.ndarray, array_size: int) -> None:
    """Shuffles array"""

    for i in range(0, array_size):
        r = generate_array(0, array_size-1)
        array[i], array[r] = array[r], array[i]
