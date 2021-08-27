import math
import matplotlib.pyplot as plt
from collections import OrderedDict

""" Docstrings explaining the file. Module way. https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings
"""

# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html for bar funcs
# plt.xticks(x_values, xticks) to change tick name under graph, update list and reset values. set_height for values.
# plt.gca().axes.xaxis.set_visible(False) to hide xaxis

# Use an online Jupyter Notebook, Repl.it for visualizations, move to tableau if possible
# Link to Jupyter in git readme to for visualizations and walkthrough as first header
# Rename vis.py to main.py once finished. Point to *algos.py code implementation.
# search_algos.py, sort_algos.py, and pathfinding_algos.py are used for pure algorithms with no visualization
# Relative speed depending on size. Maybe speed increase n^2 with n size? Or 2n. Or just use time complexity.
# Allow generating random graphs


# Putting plt.pause() in if statements are what causes the outline color and slows down visualizer. Only part of it
# Check on larger list. Make sure all edge cases are dealt with.
# Return non sorted value for algorithms that require sort
# Use dict of key=Values and value=index in reverse order to get original index for searches. Or use list values[0]

# Remove temp variable for swapping two values. Will have to change bar updating method
# Seems as though you can only call each search function once. Need to fix for actual deployment
# Create subplots to visualize multiple at once
# Currently this gets rid of duplicates nums. See test4
# Optimize so you don't need to clear graph each update
# Use an upside down bar graph
# Add note: Animation speed for each algorithm is chosen for clarity and not completely indicative of real world speed.
# Choose different pause_short and pause_long for each algorithm
# Animated graphs?
# Allow to go step by step?

# Add comments explaining each block of code after rewriting
class SearchVisualizer:
    def __init__(self, values, pause_short=0.1, pause_long=1.0):   # Look into set_facecolor, set_edgecolor. Maybe solves edge bug
        self.values = values
        self.LENGTH = len(self.values)
        self.names = [str(i) for i in values]
        self.vis_unchecked = 'blue'

        self.vis = plt.bar(self.names, self.values, color=self.vis_unchecked)
        self.pause_short = pause_short
        self.pause_long = pause_long
        self.vis_checking = 'gold'
        self.vis_right = 'green'
        self.vis_wrong = 'red'
        plt.suptitle('Yellow is pivot - Red is not valid - Green is found value')
        # self._values_sorted = sorted(values)
        # self._names_sorted = [str(i) for i in values]
        # Alternative way to sort values for non linear searches. Currently using values_sort function instead.

    def values_sort(self):
        self.values.sort()
        self.names = [str(i) for i in self.values]
        plt.clf()   # Might be costly. Optimization could be to keep different set of sorted values rather than updating
        self.vis = plt.bar(self.names, self.values, color=self.vis_unchecked)

    def visualize(self, res):
        if isinstance(res, int):
            if res > -1:
                self.vis[res].set_color(self.vis_right)
            else:
                self.vis[res].set_color(self.vis_wrong)
                # for i in range(-res, self.length):
                #     test[i].set_color(self.vis_wrong)
                # This may be necessary for exponential to work properly. Leaving just in case.
        else:
            if res[0] > -1:
                self.vis[res[0]].set_color(self.vis_right)
                for i in range(res[0]+1, res[1]+1):
                    self.vis[i].set_color(self.vis_wrong)
            else:
                for i in range(-res[0], res[1]+1):
                    self.vis[i].set_color(self.vis_wrong)
        plt.show()
        plt.clf()   # Might break something. Idk yet. Maybe it will help to call multiple times per single run

    # TODO Use *args to compare all at once. Or just open each in different windows
    # Turn visualize into function where you pass every color change. This allows you to not show plots individually
    # And can wait and combine them for this function.
    # Maybe paralleling threads? Idk if that would apply in this situation.
    # Figure out how to change default color in line with self.vis_color
    def comparison(self, key, func1=None, func2=None):  # Use strings to know which functions needs to be compared
        plt.close()
        self.vis = plt.figure()
        a = self.vis.add_subplot(211)
        b = self.vis.add_subplot(212)

        a.bar(self.names, self.values)
        b.bar(self.names, self.values)

        self.linear(key, a)
        self.linear(key, b)

    def linear(self, key, fig=None):  # Only algorithm that does not require sorted values.
        if not fig:
            fig = self.vis

        for i in range(self.LENGTH):
            if self.values[i] != key:
                fig[i].set_color(self.vis_wrong)
                plt.pause(self.pause_short)
                if i == self.LENGTH-1:
                    return self.visualize(-i)
            else:
                return self.visualize(i)

    def binary(self, key, high=None, fig=None):
        if not fig:
            fig = self.vis

        if not high:
            high = self.LENGTH
        low = 0
        mid = (high + low) // 2
        upper = high

        while high >= low:
            mid = (high + low) // 2
            fig[mid].set_color(self.vis_checking)
            plt.pause(self.pause_long)

            if self.values[mid] > key:
                if high < self.LENGTH-2:
                    upper = high+1
                else:
                    upper = high
                for i in range(mid, upper):
                    fig[i].set_color(self.vis_wrong)
                high = mid - 1
            elif self.values[mid] < key:
                if low > 1:
                    lower = low-1
                else:
                    lower = low
                for i in range(lower, mid):
                    fig[i].set_color(self.vis_wrong)
                low = mid + 1
            else:
                for i in range(low-1, mid):
                    fig[i].set_color(self.vis_wrong)
                for i in range(mid+1, upper):
                    fig[i].set_color(self.vis_wrong)
                return self.visualize(mid)

        for i in range(self.LENGTH-1):
            fig[i].set_color(self.vis_wrong)
        return self.visualize(-mid)

    def jump(self, key):
        step = int(math.sqrt(self.LENGTH))
        left, right = 0, 0

        while left < self.LENGTH and self.values[left] <= key:
            right = min(self.LENGTH - 1, left + step)

            self.vis[left].set_color(self.vis_checking)
            self.vis[right].set_color(self.vis_checking)
            plt.pause(self.pause_long)

            if self.values[left] <= key <= self.values[right]:
                for i in range(right+1, self.LENGTH):
                    self.vis[i].set_color(self.vis_wrong)
                plt.pause(self.pause_long)
                break
            left += step

            for i in range(left):
                self.vis[i].set_color(self.vis_wrong)

        if left >= self.LENGTH or self.values[left] > key:
            return self.visualize((left, right))

        right = min(self.LENGTH - 1, right)
        i = left

        while i <= right and self.values[i] <= key:
            if self.values[i] == key:
                return self.visualize((i, right))
            self.vis[i].set_color(self.vis_wrong)
            plt.pause(self.pause_short)
            i += 1

        return self.visualize((-i, right))

    # TODO Does weird stuff when searching for 48 with values. The height arg for binary search probably is the cause.
    def exponential(self, k):
        self.vis[0].set_color(self.vis_checking)
        plt.pause(self.pause_long)

        if self.values[0] == k:
            for i in range(1, self.LENGTH):
                self.vis[i].set_color(self.vis_wrong)
            return 0

        i = temp_low = temp = 1
        self.vis[0].set_color(self.vis_wrong)
        self.vis[i].set_color(self.vis_checking)

        while i < self.LENGTH and self.values[i] <= k:
            i *= 2
            if i <= self.LENGTH:
                for j in range(temp_low, temp+2):
                    self.vis[j].set_color(self.vis_wrong)
            plt.pause(self.pause_long)
            temp = i
            temp_low = int(temp / 2)

        if i <= self.LENGTH:
            for j in range(i+1, self.LENGTH):
                self.vis[j].set_color(self.vis_wrong)

        if i < self.LENGTH:
            return self.binary(k, i)
        else:
            return self.binary(k)

    def fibonacci(self, key):
        fib_minus_2 = 0
        fib_minus_1 = 1
        fib = fib_minus_1 + fib_minus_2
        i = 1

        while fib < self.LENGTH:
            fib_minus_2 = fib_minus_1
            fib_minus_1 = fib
            fib = fib_minus_1 + fib_minus_2

        index = -1

        while fib > 1:
            i = min(index + fib_minus_2, (self.LENGTH - 1))

            self.vis[i].set_color(self.vis_checking)
            plt.pause(self.pause_long)

            if self.values[i] < key:
                for j in range(i+1):
                    self.vis[j].set_color(self.vis_wrong)

                fib = fib_minus_1
                fib_minus_1 = fib_minus_2
                fib_minus_2 = fib - fib_minus_1
                index = i
            elif self.values[i] > key:
                for j in range(i, self.LENGTH):
                    self.vis[j].set_color(self.vis_wrong)

                fib = fib_minus_2
                fib_minus_1 = fib_minus_1 - fib_minus_2
                fib_minus_2 = fib - fib_minus_1
            else:
                return self.visualize(i)

        if fib_minus_1 and index < (self.LENGTH - 1) and self.values[index + 1] == key:
            return self.visualize(index + 1)

        return self.visualize(-i)


# TODO Prevent duplicates in input
class SortVisualizer:
    """Example docstring.

    Add these for every class and function. https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings
    """

    def __init__(self, values, pause_short=0.1, pause_long=0.2):
        """Single line doc string"""
        # self.values = list(OrderedDict.fromkeys(values))   # Removes duplicates. Breaks radix and merge??????????????
        self.values = values
        self.LENGTH = len(self.values)
        # self.names = [str(i) for i in self.values]    - Bar names need to be unique or they overlap. This fails
        self.names = [i for i in range(self.LENGTH)]    # Sets names to index of self.values.
        plt.gca().axes.xaxis.set_visible(False)         # Hides x axis values. Prevents needing to update them.
        self.vis_unsorted = 'blue'

        self.vis = plt.bar(self.names, self.values, color=self.vis_unsorted)
        self.pause_short = pause_short
        self.pause_long = pause_long
        self.vis_pivot = 'red'  # Change color names to vis_red, vis_green etc
        self.vis_min = 'magenta'
        self.vis_checking = 'gold'
        self.vis_sorted = 'green'
        self.vis_cyan = 'cyan'
        # Might need to check to see if all of these are needed in more than one func. If not place in individual func

    def visualize(self):
        """Multi line doc string
        Example example
        """
        pass

    def selection(self):
        for i in range(self.LENGTH - 1):
            self.vis[i].set_color(self.vis_pivot)
            plt.pause(self.pause_long)

            index = i
            for j in range(i + 1, self.LENGTH):
                self.vis[j].set_color(self.vis_checking)
                plt.pause(self.pause_short)

                if self.values[j] < self.values[index]:
                    self.vis[j].set_color(self.vis_min)
                    if index != i:
                        self.vis[index].set_color(self.vis_checking)

                    index = j

            # Swaps bars while maintaining color for each
            self.vis[i].set_height(self.values[index])
            self.vis[i].set_color(self.vis_min)
            self.values[i], self.values[index] = self.values[index], self.values[i]
            self.vis[index].set_height(self.values[index])
            self.vis[index].set_color(self.vis_pivot)
            plt.pause(self.pause_long)

            self.vis[i].set_color(self.vis_sorted)
            for b in range(i+1, self.LENGTH):
                self.vis[b].set_color(self.vis_unsorted)

            if i == self.LENGTH-2:
                for b in range(i, self.LENGTH):
                    self.vis[b].set_color(self.vis_sorted)

        plt.show()

    def insertion(self):
        for i in range(1, self.LENGTH):
            a = i

            self.vis[a].set_color(self.vis_pivot)

            while a > 0 and self.values[a] < self.values[a - 1]:
                # Swaps bars while maintaining color for each
                self.vis[a].set_color(self.vis_pivot)
                self.vis[a-1].set_color(self.vis_checking)
                plt.pause(self.pause_long)
                self.vis[a].set_color(self.vis_unsorted)
                self.vis[a-1].set_color(self.vis_unsorted)

                self.vis[a].set_height(self.values[a-1])
                self.values[a], self.values[a-1] = self.values[a-1], self.values[a]
                self.vis[a-1].set_height(self.values[a-1])

                a -= 1
            else:
                self.vis[a+1].set_color(self.vis_checking)
                self.vis[a].set_color(self.vis_pivot)
                plt.pause(self.pause_long)
                self.vis[a+1].set_color(self.vis_unsorted)
                self.vis[a].set_color(self.vis_unsorted)

        for b in range(self.LENGTH):
            self.vis[b].set_color(self.vis_sorted)
        plt.show()

    def bubble(self):
        for i in range(self.LENGTH-1):
            for j in range(0, self.LENGTH-i - 1):
                self.vis[j].set_color(self.vis_pivot)
                self.vis[j+1].set_color(self.vis_checking)
                plt.pause(self.pause_short)

                if self.values[j] > self.values[j+1]:
                    # Swaps bars while maintaining color for each
                    self.vis[j].set_height(self.values[j+1])
                    self.vis[j].set_color(self.vis_checking)
                    self.values[j], self.values[j+1] = self.values[j+1], self.values[j]
                    self.vis[j+1].set_height(self.values[j+1])
                    self.vis[j+1].set_color(self.vis_pivot)
                    plt.pause(self.pause_short)

                self.vis[j].set_color(self.vis_unsorted)
                self.vis[j+1].set_color(self.vis_unsorted)

                if j == self.LENGTH-i - 2:
                    self.vis[j+1].set_color(self.vis_sorted)

        self.vis[0].set_color(self.vis_sorted)
        plt.show()

    def heap(self):
        # Puts values in heap
        for i in range(self.LENGTH // 2 - 1, -1, -1):
            self._heap(self.LENGTH, i)

        # Show that values are now in heap
        for b in range(self.LENGTH):
            self.vis[b].set_color(self.vis_min)
        plt.pause(self.pause_long)

        # Sorts values from min to max, max first
        for i in range(self.LENGTH - 1, 0, -1):
            self.vis[i].set_color(self.vis_checking)
            self.vis[0].set_color(self.vis_checking)
            for b in range(i):
                self.vis[b].set_color(self.vis_min)
            plt.pause(self.pause_short)
            for b in range(i):
                self.vis[b].set_color(self.vis_unsorted)

            self.vis[i].set_height(self.values[0])
            self.values[i], self.values[0] = self.values[0], self.values[i]
            self.vis[0].set_height(self.values[0])
            self.vis[i].set_color(self.vis_sorted)
            plt.pause(self.pause_short)
            self.vis[0].set_color(self.vis_unsorted)

            self._heap(i, 0)

        self.vis[0].set_color(self.vis_sorted)
        plt.show()

    def _heap(self, length, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        self.vis[i].set_color(self.vis_checking)

        if left < length:
            self.vis[left].set_color(self.vis_checking)
            if self.values[largest] < self.values[left]:
                largest = left

        if right < length:
            self.vis[right].set_color(self.vis_checking)
            if self.values[largest] < self.values[right]:
                largest = right

        plt.pause(self.pause_short)

        if largest != i:
            self.vis[i].set_color(self.vis_pivot)
            self.vis[largest].set_color(self.vis_pivot)
            plt.pause(self.pause_short)

            self.vis[i].set_height(self.values[largest])
            self.values[i], self.values[largest] = self.values[largest], self.values[i]
            self.vis[largest].set_height(self.values[largest])
            plt.pause(self.pause_short)

            self._heap(length, largest)

        self.vis[i].set_color(self.vis_unsorted)
        if left < length:
            self.vis[left].set_color(self.vis_unsorted)
        if right < length:
            self.vis[right].set_color(self.vis_unsorted)

    def quick(self, start=0, end=-1):
        if end == -1:
            end = self.LENGTH - 1

        if end <= start:
            return

        high = self._quick(start, end)

        self.quick(start, high)

        self.quick(high + 1, end)

        if end == self.LENGTH-1:
            self.vis[end].set_color(self.vis_sorted)
            self.vis[end-1].set_color(self.vis_sorted)  # Sometimes this one is colored.

    def _quick(self, start, end):
        print(start, end)
        mid = start + (end - start) // 2
        pivot = self.values[mid]

        self.vis[mid].set_color(self.vis_pivot)
        plt.pause(self.pause_short)

        low = start
        high = end

        done = False
        while not done:
            while self.values[low] < pivot:
                if low != mid:
                    self.vis[low].set_color(self.vis_min)
                    plt.pause(self.pause_short)
                low += 1

            while pivot < self.values[high]:
                if high != mid:
                    self.vis[high].set_color(self.vis_checking)
                    plt.pause(self.pause_short)
                high -= 1

            if low >= high:
                done = True
            else:
                if low != mid:
                    self.vis[low].set_color(self.vis_checking)
                if high != mid:
                    self.vis[high].set_color(self.vis_min)
                plt.pause(self.pause_short)
                if low != mid and high != mid:
                    self.vis[low].set_color(self.vis_min)
                    self.vis[high].set_color(self.vis_checking)
                elif low == mid and high == mid:
                    self.vis[mid].set_color(self.vis_pivot)     # Does nothing. Avoiding using pass
                elif low == mid:
                    self.vis[low].set_color(self.vis_min)
                    self.vis[high].set_color(self.vis_pivot)
                elif high == mid:
                    self.vis[high].set_color(self.vis_checking)
                    self.vis[low].set_color(self.vis_pivot)

                self.vis[low].set_height(self.values[high])
                self.values[low], self.values[high] = self.values[high], self.values[low]
                self.vis[high].set_height(self.values[high])
                plt.pause(self.pause_short)

                low += 1
                high -= 1

        for b in range(start, end+1):
            self.vis[b].set_color(self.vis_unsorted)

        if end - start <= 1:
            for i in range(end+1):
                self.vis[i].set_color(self.vis_sorted)

        return high

    def merge(self, i=0, key=-1):
        if key == -1:
            key = len(self.values) - 1

        if i < key:
            j = (i + key) // 2

            self.merge(i, j)
            self.merge(j + 1, key)

            self._merge(self.values, i, j, key)

    # Set bars to green as doing the final merge. When j is half.
    def _merge(self, numbers, i, j, key):   # Is numbers necessary or can i replace with self.values
        merged_size = key - i + 1
        merged_numbers = [0] * merged_size
        merge_pos = 0
        left_pos = i
        right_pos = j + 1

        left_bar, right_bar = left_pos, right_pos
        temp = numbers.copy()

        # Compares left and right merge and places lowest of each first.
        while left_pos <= j and right_pos <= key:
            self.vis[left_bar].set_color(self.vis_checking)
            self.vis[right_bar].set_color(self.vis_checking)
            plt.pause(self.pause_short)

            # If left bar less, it's already in place.
            if numbers[left_pos] <= numbers[right_pos]:
                self.vis[left_bar].set_color(self.vis_unsorted)
                self.vis[right_bar].set_color(self.vis_unsorted)
                left_bar += 1

                merged_numbers[merge_pos] = numbers[left_pos]
                left_pos += 1

            # If right bar is less, shifts everything in between left and right bar to the right.
            # Moves right bar to the left spot, moves the left bar one spot ahead.
            else:
                t = temp.copy()
                temp[left_bar] = numbers[right_pos]
                for b in range(left_bar, right_bar):
                    temp[b + 1] = t[b]
                    self.vis[b].set_height(temp[b])
                left_bar += 1
                self.vis[left_bar].set_color(self.vis_checking)
                self.vis[right_bar].set_height(temp[right_bar])
                self.vis[right_bar].set_color(self.vis_unsorted)
                right_bar += 1
                plt.pause(self.pause_short)
                self.vis[left_bar-1].set_color(self.vis_unsorted)
                self.vis[left_bar].set_color(self.vis_unsorted)

                merged_numbers[merge_pos] = numbers[right_pos]
                right_pos += 1

            merge_pos += 1

        # Runs when right merge ends before left merge. Rest of left's values are just added as it's already sorted.
        while left_pos <= j:
            self.vis[left_bar].set_color(self.vis_min)
            plt.pause(self.pause_short)

            self.vis[left_bar].set_color(self.vis_unsorted)
            left_bar += 1

            merged_numbers[merge_pos] = numbers[left_pos]
            left_pos += 1
            merge_pos += 1

        # Runs when left merge ends before right merge. Rest of right's values are just added as it's already sorted.
        while right_pos <= key:
            self.vis[right_bar].set_color(self.vis_min)
            plt.pause(self.pause_short)

            for b in range(left_bar, right_bar):  # Shifts bars between left and right-1 over by 1
                self.vis[b + 1].set_height(numbers[b])
            left_bar += 1
            self.vis[left_bar-1].set_height(numbers[right_pos])  # Moves right bar to left bar's original position
            self.vis[right_bar].set_color(self.vis_unsorted)  # Removes right bar's original position's color
            self.vis[left_bar-1].set_color(self.vis_min)    # Adds color to current right bar
            plt.pause(self.pause_short)

            self.vis[left_bar - 1].set_color(self.vis_unsorted)  # Removes right bar's color
            right_bar += 1

            merged_numbers[merge_pos] = numbers[right_pos]
            right_pos += 1
            merge_pos += 1

        # Commits the current sorted values to self.values. Redundant for visualization but necessary for the sort.
        for merge_pos in range(merged_size):
            numbers[i + merge_pos] = merged_numbers[merge_pos]

    def timsort(self):  # Need to fix merge sort first
        pass

    # TODO More colors for numbers over 9999.
    # Does not work with duplicate numbers. Ignoring for now.
    def radix(self):
        buckets = []
        for i in range(10):
            buckets.append([])

        max_digits = self._radix_max()
        pow_10 = 1

        for digit_index in range(max_digits):
            for num in self.values:
                bucket_index = (abs(num) // pow_10) % 10
                buckets[bucket_index].append(num)

            color = ''  # Used so each digit gets it's own color.
            temp = self.values.copy()

            if pow_10 == 1:
                color = self.vis_checking
            elif pow_10 == 10:
                color = self.vis_pivot
            elif pow_10 == 100:
                color = self.vis_min
            elif pow_10 == 1000:
                color = self.vis_unsorted

            self.values.clear()
            for bucket in buckets:
                self.values.extend(bucket)
                bucket.clear()

            # Main tool for visualizing. Needs to be complicated to push values to the right rather than just replace.
            for b in range(self.LENGTH):
                index = temp.index(self.values[b])
                self.vis[b].set_color(color)
                self.vis[index].set_color(color)
                plt.pause(self.pause_short)

                t = temp.copy()
                temp[b] = self.values[b]
                for i in range(b, index):
                    temp[i + 1] = t[i]
                    self.vis[i].set_height(temp[i])
                self.vis[index].set_height(temp[index])
                self.vis[index].set_color(self.vis_unsorted)
                plt.pause(self.pause_short)
                if digit_index != max_digits-1:
                    self.vis[b].set_color(self.vis_unsorted)
                else:
                    self.vis[b].set_color(self.vis_sorted)

            plt.pause(self.pause_long)

            pow_10 = pow_10 * 10

        negatives = []
        non_negatives = []
        for num in self.values:
            if num < 0:
                negatives.append(num)
            else:
                non_negatives.append(num)
        negatives.reverse()
        self.values.clear()
        self.values.extend(negatives + non_negatives)

        plt.show()

    def _radix_max(self):
        max_digits = 0
        for num in self.values:
            digit_count = self._radix_length(num)
            if digit_count > max_digits:
                max_digits = digit_count

        return max_digits

    @staticmethod
    def _radix_length(value):
        if value == 0:
            return 1

        digits = 0
        while value != 0:
            digits += 1
            value = int(value / 10)
        return digits


if __name__ == '__main__':
    import random

    test = [4, 89, 1, 9, 69, 49, 149, 84, 15, 15, 79, 41, 9, 62, 19]    # Original test array. Use as base. 48/49
    test1 = [4, 89, 1, 9, 69, 49, 149, 84, 15, 79, 41, 62, 19]  # No duplicates
    test2 = random.sample(range(1000), 1000)
    test3 = [74, 83, 4, 62, 23, 71, 22, 13, 69, 6, 16, 9, 99, 97, 34, 18, 93, 61, 15, 64, 55, 72, 35, 50, 63, 25, 26, 54, 36, 47, 2, 66, 38, 81, 95, 46, 79, 77, 28, 49, 56, 76, 41, 27, 82, 24, 10, 7, 3, 75, 48, 90, 51, 98, 33, 21, 37, 52, 80, 17, 42, 29, 19, 11, 20, 96, 43, 59, 57, 88, 8, 5, 94, 84, 87, 68, 30, 60, 12, 0, 1, 40, 14, 31, 45, 92, 70, 32, 67, 73, 78, 89, 65, 44, 86, 53, 39, 58, 85, 91]
    test4 = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    k = 49

    y = SortVisualizer(test3, 0.01, 0.1)    # TODO Test on large values

    # y.selection()
    # y.insertion()
    # y.bubble()
    # y.heap()
    # y.quick()

    y.merge()
    # y.timsort() TODO

    # y.radix()

    plt.show()  # Put this in visualize for merge and quick sort
    print(y.values)
    # print(sorted(y.values))

# ---------------------------------------------------------

    # x = SearchVisualizer(test3)
    # x.values_sort()

    # x.comparison(k)
    # x.linear(k)
    # x.binary(k)
    # x.jump(k)
    # x.exponential(k)
    # x.fibonacci(k)
