import matplotlib.pyplot as plt
from colors import *
from values import generate_array, get_factorial


def selection(vis_, array, array_size, pause_short, pause_mid):
    """Goes through list comparing values of the current number to all values after, swapping as needed.
    Complexity: Time - O(n^2), Space - O(1), Unstable
    """

    for i in range(array_size - 1):
        vis_[i].set_color(MPL_BLACK)
        plt.pause(pause_mid)

        index = i
        for j in range(i + 1, array_size):
            vis_[j].set_color(MPL_GOLD)
            plt.pause(pause_short)

            if array[j] < array[index]:
                vis_[j].set_color(MPL_CYAN)
                if index != i:
                    vis_[index].set_color(MPL_GOLD)

                index = j

        # Swaps bars while maintaining color for each
        vis_[i].set_height(array[index])
        vis_[i].set_color(MPL_CYAN)
        array[i], array[index] = array[index], array[i]
        vis_[index].set_height(array[index])
        vis_[index].set_color(MPL_BLACK)
        plt.pause(pause_mid)

        vis_[i].set_color(MPL_GREEN)
        for b in range(i+1, array_size):
            vis_[b].set_color(MPL_DEFAULT)

        if i == array_size-2:
            for b in range(i, array_size):
                vis_[b].set_color(MPL_GREEN)

    plt.draw()


def insertion(vis_, array, array_size, pause_short):
    """Splits input into the sorted and unsorted parts. Places unsorted elements to the correct position.
    Complexity: Time - O(n^2), Space - O(1), Stable
    """

    for i in range(1, array_size):
        a = i

        vis_[a].set_color(MPL_RED)

        while a > 0 and array[a] < array[a - 1]:
            # Swaps bars while maintaining color for each
            vis_[a].set_color(MPL_RED)
            vis_[a-1].set_color(MPL_GOLD)
            plt.pause(pause_short)
            vis_[a].set_color(MPL_DEFAULT)
            vis_[a-1].set_color(MPL_DEFAULT)

            vis_[a].set_height(array[a-1])
            array[a], array[a-1] = array[a-1], array[a]
            vis_[a-1].set_height(array[a-1])

            a -= 1
        else:
            if a < array_size-1:
                vis_[a+1].set_color(MPL_GOLD)
            vis_[a].set_color(MPL_RED)
            plt.pause(pause_short)
            if a < array_size-1:
                vis_[a+1].set_color(MPL_DEFAULT)
            vis_[a].set_color(MPL_DEFAULT)

    for b in range(array_size):
        vis_[b].set_color(MPL_GREEN)
    plt.draw()


def bubble(vis_, array, array_size, pause_short):
    """Swaps adjacent elements if they are in the wrong order.
    Repeats n-1 times with max index to check decreasing by 1.
    Complexity: Time - O(n^2), Space - O(1), Stable
    """

    for i in range(array_size - 1):
        for j in range(0, array_size-i - 1):
            vis_[j].set_color(MPL_RED)
            vis_[j+1].set_color(MPL_GOLD)
            plt.pause(pause_short)

            if array[j] > array[j+1]:
                # Swaps bars while maintaining color for each
                vis_[j].set_height(array[j+1])
                vis_[j].set_color(MPL_GOLD)
                array[j], array[j+1] = array[j+1], array[j]
                vis_[j+1].set_height(array[j+1])
                vis_[j+1].set_color(MPL_RED)
                plt.pause(pause_short)

            vis_[j].set_color(MPL_DEFAULT)
            vis_[j+1].set_color(MPL_DEFAULT)

            if j == array_size-i - 2:
                vis_[j+1].set_color(MPL_GREEN)

    vis_[0].set_color(MPL_GREEN)
    plt.draw()


def heap(vis_, array, array_size, pause_short, pause_long):
    """Converts input into a max heap data structure and pops values.
    Complexity: Time - O(nlog(n)), Space - O(1), Unstable
    """

    # Puts values in heap
    for i in range(array_size // 2 - 1, -1, -1):
        _heap(vis_, array, pause_short, array_size, i)

    # Show that values are now in heap
    for b in range(array_size):
        vis_[b].set_color(MPL_BLACK)
    plt.pause(pause_long)

    # Sorts values from min to max, max first
    for i in range(array_size - 1, 0, -1):
        vis_[i].set_color(MPL_GOLD)
        vis_[0].set_color(MPL_GOLD)
        for b in range(i):
            vis_[b].set_color(MPL_BLACK)
        plt.pause(pause_short)
        for b in range(i):
            vis_[b].set_color(MPL_DEFAULT)

        vis_[i].set_height(array[0])
        array[i], array[0] = array[0], array[i]
        vis_[0].set_height(array[0])
        vis_[i].set_color(MPL_GREEN)
        plt.pause(pause_short)
        vis_[0].set_color(MPL_DEFAULT)

        _heap(vis_, array, pause_short, i, 0)

    vis_[0].set_color(MPL_GREEN)
    plt.draw()


def _heap(vis_, array, pause_short, length, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    vis_[i].set_color(MPL_GOLD)

    if left < length:
        vis_[left].set_color(MPL_GOLD)
        if array[largest] < array[left]:
            largest = left

    if right < length:
        vis_[right].set_color(MPL_GOLD)
        if array[largest] < array[right]:
            largest = right

    plt.pause(pause_short)

    if largest != i:
        vis_[i].set_color(MPL_RED)
        vis_[largest].set_color(MPL_RED)
        plt.pause(pause_short)

        vis_[i].set_height(array[largest])
        array[i], array[largest] = array[largest], array[i]
        vis_[largest].set_height(array[largest])
        plt.pause(pause_short)

        _heap(vis_, array, pause_short, length, largest)

    vis_[i].set_color(MPL_DEFAULT)
    if left < length:
        vis_[left].set_color(MPL_DEFAULT)
    if right < length:
        vis_[right].set_color(MPL_DEFAULT)


def quick(vis_, array, array_size, pause_short, start=0, end=-1):
    """Sets a pivot value and places every value below the pivot before and all values greater after.
    Repeats recursively until only single element partitions remains.
    Complexity: Time - O(nlog(n)), Space - O(log(n)), Unstable
    """

    if end == -1:
        end = array_size - 1

    if end <= start:
        return

    high = _quick(vis_, array, pause_short, start, end)

    quick(vis_, array, array_size, pause_short, start, high)

    quick(vis_, array, array_size, pause_short, high + 1, end)

    if end == array_size-1:
        vis_[end].set_color(MPL_GREEN)
        vis_[end-1].set_color(MPL_GREEN)  # Sometimes this one is colored.
        plt.draw()


def _quick(vis_, array, pause_short, start, end):
    mid = start + (end - start) // 2
    pivot = array[mid]

    vis_[mid].set_color(MPL_MAGENTA)
    plt.pause(pause_short)

    low = start
    high = end

    done = False
    while not done:
        while array[low] < pivot:
            if low != mid:
                vis_[low].set_color(MPL_RED)
                plt.pause(pause_short)
            low += 1

        while pivot < array[high]:
            if high != mid:
                vis_[high].set_color(MPL_CYAN)
                plt.pause(pause_short)
            high -= 1

        if low >= high:
            done = True
        else:
            if low != mid:
                vis_[low].set_color(MPL_CYAN)
            if high != mid:
                vis_[high].set_color(MPL_RED)
            plt.pause(pause_short)
            if low != mid and high != mid:
                vis_[low].set_color(MPL_RED)
                vis_[high].set_color(MPL_CYAN)
            elif low == mid and high == mid:
                vis_[mid].set_color(MPL_MAGENTA)     # Does nothing. Avoiding using pass
            elif low == mid:
                vis_[low].set_color(MPL_RED)
                vis_[high].set_color(MPL_MAGENTA)
            elif high == mid:
                vis_[high].set_color(MPL_CYAN)
                vis_[low].set_color(MPL_MAGENTA)

            vis_[low].set_height(array[high])
            array[low], array[high] = array[high], array[low]
            vis_[high].set_height(array[high])
            plt.pause(pause_short)

            low += 1
            high -= 1

    for b in range(start, end+1):
        vis_[b].set_color(MPL_DEFAULT)

    if end - start <= 1:
        for i in range(end+1):
            vis_[i].set_color(MPL_GREEN)

    return high


def merge(vis_, array, array_size, pause_short, i=0, key=-1):
    """Recursively splits input in halves. Sorts each element at each level bottom up.
    Complexity: Time - O(nlog(n)), Space - O(n), Stable
    """

    if key == -1:
        key = array_size - 1

    if i < key:
        j = (i + key) // 2

        merge(vis_, array, array_size, pause_short, i, j)
        merge(vis_, array, array_size, pause_short, j + 1, key)

        _merge(vis_, array, array_size, pause_short, i, j, key)

    if i == 0 and key == array_size - 1:
        plt.draw()


def _merge(vis_, array, array_size, pause_short, i, j, key):
    merged_size = key - i + 1
    merged_numbers = [0] * merged_size
    merge_pos = 0
    left_pos = i
    right_pos = j + 1

    left_bar, right_bar = left_pos, right_pos
    temp = array.copy()

    # Compares left and right merge and places lowest of each first.
    while left_pos <= j and right_pos <= key:
        vis_[left_bar].set_color(MPL_RED)
        vis_[right_bar].set_color(MPL_GOLD)
        plt.pause(pause_short)

        # If left bar less, it's already in place.
        if array[left_pos] <= array[right_pos]:
            if i != 0 or key != array_size-1:
                vis_[left_bar].set_color(MPL_DEFAULT)
            else:
                vis_[left_bar].set_color(MPL_GREEN)
            vis_[right_bar].set_color(MPL_DEFAULT)
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
                vis_[b].set_height(temp[b])
            left_bar += 1
            vis_[left_bar].set_color(MPL_RED)
            vis_[right_bar].set_height(temp[right_bar])
            vis_[right_bar].set_color(MPL_DEFAULT)
            right_bar += 1
            plt.pause(pause_short)
            if i != 0 or key != array_size-1:
                vis_[left_bar-1].set_color(MPL_DEFAULT)
            else:
                vis_[left_bar-1].set_color(MPL_GREEN)
            vis_[left_bar].set_color(MPL_DEFAULT)

            merged_numbers[merge_pos] = array[right_pos]
            right_pos += 1

        merge_pos += 1

    # Runs when right merge ends before left merge. Rest of left's values are just added as it's already sorted.
    while left_pos <= j:
        vis_[left_bar].set_color(MPL_MAGENTA)
        plt.pause(pause_short)
        if i != 0 or key != array_size-1:
            vis_[left_bar].set_color(MPL_DEFAULT)
        else:
            vis_[left_bar].set_color(MPL_GREEN)
        left_bar += 1

        merged_numbers[merge_pos] = array[left_pos]
        left_pos += 1
        merge_pos += 1

    # Runs when left merge ends before right merge. Rest of right's values are just added as it's already sorted.
    while right_pos <= key:
        vis_[right_bar].set_color(MPL_MAGENTA)
        plt.pause(pause_short)

        for b in range(left_bar, right_bar):  # Shifts bars between left and right-1 over by 1
            vis_[b + 1].set_height(array[b])
        left_bar += 1
        vis_[left_bar-1].set_height(array[right_pos])  # Moves right bar to left bar's original position
        vis_[right_bar].set_color(MPL_DEFAULT)  # Removes right bar's original position's color
        vis_[left_bar-1].set_color(MPL_MAGENTA)    # Adds color to current right bar
        plt.pause(pause_short)
        if i != 0 or key != array_size - 1:
            vis_[left_bar-1].set_color(MPL_DEFAULT)  # Removes right bar's color
        else:
            vis_[left_bar-1].set_color(MPL_GREEN)
        right_bar += 1

        merged_numbers[merge_pos] = array[right_pos]
        right_pos += 1
        merge_pos += 1

    # Commits the current sorted values to array. Redundant for visualization but necessary for the sort.
    for merge_pos in range(merged_size):
        array[i + merge_pos] = merged_numbers[merge_pos]


def tim(vis_, array, array_size, pause_short):      # Seems to use insertion too much. Possibly a bug.
    """Combination of merge sort and insertion sort.
    Divides input into blocks, sorts using insertion, combines using merge.
    Complexity: Time - O(nlog(n)), Space - O(1), Stable
    """

    min_run = _min_run(array_size)

    for start in range(0, array_size, min_run):
        insertion(vis_, array, array_size, pause_short)

    size = min_run
    while size < array_size:

        for left in range(0, array_size, 2 * size):

            mid = min(array_size - 1, left + size - 1)
            right = min((left + 2 * size - 1), (array_size - 1))

            if mid < right:
                _merge(vis_, array, array_size, pause_short, left, mid, right)

        size = 2 * size


def _min_run(n):
    MIN_MERGE = 51

    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r


def radix(vis_, array, array_size, pause_short, pause_long):
    """Only for integers. Places values into buckets from the least to most significant digit. Sorts with buckets
    Complexity: Time - O(n*k), Space - O(n+k), Stable
    """

    buckets = []
    for i in range(10):
        buckets.append([])

    max_digits = _radix_max(array)
    pow_10 = 1

    for digit_index in range(max_digits):
        for num in array:
            bucket_index = (abs(num) // pow_10) % 10
            buckets[bucket_index].append(num)

        color = ''  # Used so each digit gets it's own color.
        temp = array.copy()

        if pow_10 == 1:
            color = MPL_CYAN
        elif pow_10 == 10:
            color = MPL_MAGENTA
        elif pow_10 == 100:
            color = MPL_RED
        elif pow_10 == 1000:
            color = MPL_BLACK

        array.clear()
        for bucket in buckets:
            array.extend(bucket)
            bucket.clear()

        # Main tool for visualizing. Needs to be complicated to push values to the right rather than just replace.
        for b in range(array_size):
            index = temp.index(array[b])
            vis_[b].set_color(color)
            vis_[index].set_color(MPL_GOLD)
            plt.pause(pause_short)

            t = temp.copy()
            temp[b] = array[b]
            for i in range(b, index):
                temp[i + 1] = t[i]
                vis_[i].set_height(temp[i])
            vis_[index].set_height(temp[index])
            vis_[index].set_color(MPL_DEFAULT)
            plt.pause(pause_short)
            if digit_index != max_digits-1:
                vis_[b].set_color(MPL_DEFAULT)
            else:
                vis_[b].set_color(MPL_GREEN)

        plt.pause(pause_long)

        pow_10 = pow_10 * 10

    negatives = []
    non_negatives = []
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


def _radix_max(array):
    max_digits = 0
    for num in array:
        digit_count = _radix_length(num)
        if digit_count > max_digits:
            max_digits = digit_count

    return max_digits


def _radix_length(num):
    if num == 0:
        return 1

    digits = 0
    while num != 0:
        digits += 1
        num = int(num / 10)
    return digits


def bogo(vis_, array, array_size, pause_short):
    """Equivalent of throwing a deck of cards in the air, picking them up randomly hoping it's sorted
    Complexity: Time - O(n*n!), Space - O(1), Unstable
    """

    EXPECTED_RUN_TIME = ((get_factorial(array_size)) / 4)

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
            vis_[b].set_height(array[b])
        plt.pause(pause_short)

    for i in range(array_size):
        vis_[i].set_color(MPL_GREEN)
    plt.draw()


def _is_sorted(array, array_size):
    for b in range(0, array_size - 1):
        if array[b] > array[b + 1]:
            return False
    return True


def _shuffle(array, array_size):
    for i in range(0, array_size):
        r = generate_array(0, array_size-1)
        array[i], array[r] = array[r], array[i]
