import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict

""" Docstrings explaining the file. Module way. https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings
"""

# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html for bar funcs
# plt.xticks(x_values, xticks) to change tick name under graph, update list and reset values.

# TODO UI Elements ----------------------------------------
# Use an online Jupyter Notebook, Repl.it for visualizations, move to tableau if possible
# Link to Jupyter in git readme to for visualizations and walkthrough as second header after explaining what it is
# Add note: Animation speed for each algorithm is chosen for clarity and not completely indicative of real world speed.
# Rename vis.py to main.py once finished. Point to *algos.py code implementation.
# search_algos.py, sort_algos.py, and pathfinding_algos.py are used for pure algorithms with no visualization
# Allow generating random graphs
# Add warning for slow algos
# For bogosort say how long it will take to find ans given array size. Say they are going to be here for a while.
# If bogosort happens to sort the list say that they are extremely special and should be proud
# Say to use smaller array sizes for individual operations, larger sizes for overall picture
# Explain what each color means for each algo
# Use fill to just have outline of bar
# Blurbs of fun tidbits about algos
# Animated graphs?
# Add stop button that doesn't require restart of code. Esp for bogosort
# Upside down graph?
# Allow to go step by step?
# Allow comparing multiple algorithms at the same time, subplots maybe

# TODO Bug fixes ------------------------------------------
# Check whether algos needs pause_long
# Run algos 10 times on random list on size 5, 10, 25, 50, and 100 to find any and all bugs.
# Change colors for each algo to be meaningful and consistent across all
# Don't sort array for linear, but sort of everything else
# Optimize how to sort for search functions that require sorting
# Visualize fib numbers in fib. Also red does not fill on dim 100 and sometimes 5
# Exponential search bug. Also red seems to be overflowing. Check on dim 100
# Look into set_facecolor, set_edgecolor. Maybe solves edge bug in search algos.
# Seems as though you can only call each search function once. Need to fix for actual deployment
# Putting plt.pause() in if statements are what causes the outline color and slows down visualizer. Only part of it
# Check on larger list. Make sure all edge cases are dealt with.
# Return non sorted value for algorithms that require sort
# Use dict of key=Values and value=index in reverse order to get original index for searches. Or use list values[0]
# Timsort seems to do too much insertion over binary


# Add comments explaining each block of code after rewriting
class SearchVisualizer:
    def __init__(self, values):
        self.values = values
        self.LENGTH = len(self.values)
        self.names = [str(i) for i in values]
        plt.gca().axes.xaxis.set_visible(False)
        # plt.gca().axes.yaxis.set_visible(False)
        plt.axis('off')
        self.show_axis = False
        self.vis_unchecked = 'blue'

        self.vis = plt.bar(self.names, self.values, color=self.vis_unchecked)
        self.pause = 150/self.LENGTH * 0.01  # plt.pause(0.02) is the min it seems
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
        if not self.show_axis:
            # plt.axis('off')
            plt.gca().axes.xaxis.set_visible(False)

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
                if res[0] < self.LENGTH:
                    self.vis[res[0]].set_color(self.vis_right)
                    for i in range(res[0]+1, res[1]+1):
                        self.vis[i].set_color(self.vis_wrong)
            else:
                if -res[0] < self.LENGTH:
                    for i in range(-res[0], res[1]+1):
                        self.vis[i].set_color(self.vis_wrong)
        plt.show()
        plt.clf()   # Might break something. Idk yet. Maybe it will help to call multiple times per single run

    # Use *args to compare all at once. Or just open each in different windows
    # Turn visualize into function where you pass every color change. This allows you to not show plots individually
    # And can wait and combine them for this function.
    # Maybe paralleling threads? Idk if that would apply in this situation.
    # def comparison(self, key, func1=None, func2=None):  # Use strings to know which functions needs to be compared
    #     plt.close()
    #     self.vis = plt.figure()
    #     a = self.vis.add_subplot(211)
    #     b = self.vis.add_subplot(212)
    #
    #     a.bar(self.names, self.values)
    #     b.bar(self.names, self.values)
    #
    #     self.linear(key, a)
    #     self.linear(key, b)

    def linear(self, key, fig=None):  # Only algorithm that does not require sorted values.
        pause_short = self.pause

        if not fig:
            fig = self.vis

        for i in range(self.LENGTH):
            if self.values[i] != key:
                fig[i].set_color(self.vis_wrong)
                plt.pause(pause_short)
                if i == self.LENGTH-1:
                    return self.visualize(-i)
            else:
                return self.visualize(i)

    def binary(self, key, high=None, fig=None):
        pause_long = (self.pause * 3) + (self.LENGTH * 0.005)

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
            plt.pause(pause_long)

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
        pause_short = self.pause
        pause_long = (self.pause * 3) + (self.LENGTH * 0.005)

        step = int(np.sqrt(self.LENGTH))     # Using numpy for sqrt, one less thing to import.
        left, right = 0, 0

        while left < self.LENGTH and self.values[left] <= key:
            right = min(self.LENGTH - 1, left + step)

            self.vis[left].set_color(self.vis_checking)
            self.vis[right].set_color(self.vis_checking)
            plt.pause(pause_long)

            if self.values[left] <= key <= self.values[right]:
                for i in range(right+1, self.LENGTH):
                    self.vis[i].set_color(self.vis_wrong)
                plt.pause(pause_long)
                break
            left += step

            for i in range(left):
                if i < self.LENGTH:
                    self.vis[i].set_color(self.vis_wrong)

        if left >= self.LENGTH or self.values[left] > key:
            return self.visualize((left, right))

        right = min(self.LENGTH - 1, right)
        i = left

        while i <= right and self.values[i] <= key:
            if self.values[i] == key:
                return self.visualize((i, right))
            self.vis[i].set_color(self.vis_wrong)
            plt.pause(pause_short)
            i += 1

        return self.visualize((-i, right))

    # Does weird stuff when searching for 48 with values. The height arg for binary search probably is the cause.
    def exponential(self, key):
        pause_long = (self.pause * 3) + (self.LENGTH * 0.005)

        self.vis[0].set_color(self.vis_checking)
        plt.pause(pause_long)

        if self.values[0] == key:
            for i in range(1, self.LENGTH):
                self.vis[i].set_color(self.vis_wrong)
            return 0

        i = temp_low = temp = 1
        self.vis[0].set_color(self.vis_wrong)
        self.vis[i].set_color(self.vis_checking)

        while i < self.LENGTH and self.values[i] <= key:
            i *= 2
            if i <= self.LENGTH:
                for j in range(temp_low, temp+2):
                    self.vis[j].set_color(self.vis_wrong)
            plt.pause(pause_long)
            temp = i
            temp_low = int(temp / 2)

        if i <= self.LENGTH:
            for j in range(i+1, self.LENGTH):
                self.vis[j].set_color(self.vis_wrong)

        if i < self.LENGTH:
            return self.binary(key, i)
        else:
            return self.binary(key)

    def fibonacci(self, key):
        pause_long = (self.pause * 3) + (self.LENGTH * 0.005)

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
            plt.pause(pause_long)

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


class SortVisualizer:
    """Example docstring.

    Add these for every class and function. https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings
    """

    def __init__(self, values):
        """Single line doc string"""
        self.values = values
        self.LENGTH = len(self.values)
        self.names = [i for i in range(self.LENGTH)]
        # plt.gca().axes.xaxis.set_visible(False)         # Hides x axis values. Prevents needing to update them.
        # plt.gca().axes.yaxis.set_visible(False)
        plt.axis('off')
        self.vis_unsorted = 'blue'

        self.vis = plt.bar(self.names, self.values, color=self.vis_unsorted)
        self.pause = 150/self.LENGTH * 0.01  # plt.pause(0.02) is the min it seems
        self.vis_red = 'red'
        self.vis_magenta = 'magenta'
        self.vis_gold = 'gold'
        self.vis_green = 'green'
        self.vis_cyan = 'cyan'

    def visualize(self):
        """Multi line doc string
        Example example
        """
        pass

    def selection(self):
        pause_short = self.pause
        pause_long = (self.pause * 3) + (self.LENGTH * 0.005)

        for i in range(self.LENGTH - 1):
            self.vis[i].set_color(self.vis_red)
            plt.pause(pause_long)

            index = i
            for j in range(i + 1, self.LENGTH):
                self.vis[j].set_color(self.vis_gold)
                plt.pause(pause_short)

                if self.values[j] < self.values[index]:
                    self.vis[j].set_color(self.vis_magenta)
                    if index != i:
                        self.vis[index].set_color(self.vis_gold)

                    index = j

            # Swaps bars while maintaining color for each
            self.vis[i].set_height(self.values[index])
            self.vis[i].set_color(self.vis_magenta)
            self.values[i], self.values[index] = self.values[index], self.values[i]
            self.vis[index].set_height(self.values[index])
            self.vis[index].set_color(self.vis_red)
            plt.pause(pause_long)

            self.vis[i].set_color(self.vis_green)
            for b in range(i+1, self.LENGTH):
                self.vis[b].set_color(self.vis_unsorted)

            if i == self.LENGTH-2:
                for b in range(i, self.LENGTH):
                    self.vis[b].set_color(self.vis_green)

        plt.show()

    def insertion(self):
        pause_short = self.pause

        for i in range(1, self.LENGTH):
            a = i

            self.vis[a].set_color(self.vis_red)

            while a > 0 and self.values[a] < self.values[a - 1]:
                # Swaps bars while maintaining color for each
                self.vis[a].set_color(self.vis_red)
                self.vis[a-1].set_color(self.vis_gold)
                plt.pause(pause_short)
                self.vis[a].set_color(self.vis_unsorted)
                self.vis[a-1].set_color(self.vis_unsorted)

                self.vis[a].set_height(self.values[a-1])
                self.values[a], self.values[a-1] = self.values[a-1], self.values[a]
                self.vis[a-1].set_height(self.values[a-1])

                a -= 1
            else:
                self.vis[a+1].set_color(self.vis_gold)
                self.vis[a].set_color(self.vis_red)
                plt.pause(pause_short)
                self.vis[a+1].set_color(self.vis_unsorted)
                self.vis[a].set_color(self.vis_unsorted)

        for b in range(self.LENGTH):
            self.vis[b].set_color(self.vis_green)
        plt.show()

    def bubble(self):
        pause_short = self.pause

        for i in range(self.LENGTH-1):
            for j in range(0, self.LENGTH-i - 1):
                self.vis[j].set_color(self.vis_red)
                self.vis[j+1].set_color(self.vis_gold)
                plt.pause(pause_short)

                if self.values[j] > self.values[j+1]:
                    # Swaps bars while maintaining color for each
                    self.vis[j].set_height(self.values[j+1])
                    self.vis[j].set_color(self.vis_gold)
                    self.values[j], self.values[j+1] = self.values[j+1], self.values[j]
                    self.vis[j+1].set_height(self.values[j+1])
                    self.vis[j+1].set_color(self.vis_red)
                    plt.pause(pause_short)

                self.vis[j].set_color(self.vis_unsorted)
                self.vis[j+1].set_color(self.vis_unsorted)

                if j == self.LENGTH-i - 2:
                    self.vis[j+1].set_color(self.vis_green)

        self.vis[0].set_color(self.vis_green)
        plt.show()

    def heap(self):
        pause_short = self.pause
        pause_long = (self.pause * 3) + (self.LENGTH * 0.005)

        # Puts values in heap
        for i in range(self.LENGTH // 2 - 1, -1, -1):
            self._heap(self.LENGTH, i, pause_short)

        # Show that values are now in heap
        for b in range(self.LENGTH):
            self.vis[b].set_color(self.vis_magenta)
        plt.pause(pause_long)

        # Sorts values from min to max, max first
        for i in range(self.LENGTH - 1, 0, -1):
            self.vis[i].set_color(self.vis_gold)
            self.vis[0].set_color(self.vis_gold)
            for b in range(i):
                self.vis[b].set_color(self.vis_magenta)
            plt.pause(pause_short)
            for b in range(i):
                self.vis[b].set_color(self.vis_unsorted)

            self.vis[i].set_height(self.values[0])
            self.values[i], self.values[0] = self.values[0], self.values[i]
            self.vis[0].set_height(self.values[0])
            self.vis[i].set_color(self.vis_green)
            plt.pause(pause_short)
            self.vis[0].set_color(self.vis_unsorted)

            self._heap(i, 0, pause_short)

        self.vis[0].set_color(self.vis_green)
        plt.show()

    def _heap(self, length, i, pause_short):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        self.vis[i].set_color(self.vis_gold)

        if left < length:
            self.vis[left].set_color(self.vis_gold)
            if self.values[largest] < self.values[left]:
                largest = left

        if right < length:
            self.vis[right].set_color(self.vis_gold)
            if self.values[largest] < self.values[right]:
                largest = right

        plt.pause(pause_short)

        if largest != i:
            self.vis[i].set_color(self.vis_red)
            self.vis[largest].set_color(self.vis_red)
            plt.pause(pause_short)

            self.vis[i].set_height(self.values[largest])
            self.values[i], self.values[largest] = self.values[largest], self.values[i]
            self.vis[largest].set_height(self.values[largest])
            plt.pause(pause_short)

            self._heap(length, largest, pause_short)

        self.vis[i].set_color(self.vis_unsorted)
        if left < length:
            self.vis[left].set_color(self.vis_unsorted)
        if right < length:
            self.vis[right].set_color(self.vis_unsorted)

    def quick(self, start=0, end=-1):   # Weird bug where bar is misplaced only once. Can't trace it.
        if end == -1:
            end = self.LENGTH - 1

        if end <= start:
            return

        high = self._quick(start, end)

        self.quick(start, high)

        self.quick(high + 1, end)

        if end == self.LENGTH-1:
            self.vis[end].set_color(self.vis_green)
            self.vis[end-1].set_color(self.vis_green)  # Sometimes this one is colored.
            plt.show()

    def _quick(self, start, end):
        pause_short = self.pause

        mid = start + (end - start) // 2
        pivot = self.values[mid]

        self.vis[mid].set_color(self.vis_red)
        plt.pause(pause_short)

        low = start
        high = end

        done = False
        while not done:
            while self.values[low] < pivot:
                if low != mid:
                    self.vis[low].set_color(self.vis_magenta)
                    plt.pause(pause_short)
                low += 1

            while pivot < self.values[high]:
                if high != mid:
                    self.vis[high].set_color(self.vis_gold)
                    plt.pause(pause_short)
                high -= 1

            if low >= high:
                done = True
            else:
                if low != mid:
                    self.vis[low].set_color(self.vis_gold)
                if high != mid:
                    self.vis[high].set_color(self.vis_magenta)
                plt.pause(pause_short)
                if low != mid and high != mid:
                    self.vis[low].set_color(self.vis_magenta)
                    self.vis[high].set_color(self.vis_gold)
                elif low == mid and high == mid:
                    self.vis[mid].set_color(self.vis_red)     # Does nothing. Avoiding using pass
                elif low == mid:
                    self.vis[low].set_color(self.vis_magenta)
                    self.vis[high].set_color(self.vis_red)
                elif high == mid:
                    self.vis[high].set_color(self.vis_gold)
                    self.vis[low].set_color(self.vis_red)

                self.vis[low].set_height(self.values[high])
                self.values[low], self.values[high] = self.values[high], self.values[low]
                self.vis[high].set_height(self.values[high])
                plt.pause(pause_short)

                low += 1
                high -= 1

        for b in range(start, end+1):
            self.vis[b].set_color(self.vis_unsorted)

        if end - start <= 1:
            for i in range(end+1):
                self.vis[i].set_color(self.vis_green)

        return high

    def merge(self, i=0, key=-1):
        if key == -1:
            key = self.LENGTH - 1

        if i < key:
            j = (i + key) // 2

            self.merge(i, j)
            self.merge(j + 1, key)

            self._merge(i, j, key)

        if i == 0 and key == self.LENGTH - 1:
            plt.show()

    def _merge(self, i, j, key):
        pause_short = self.pause

        merged_size = key - i + 1
        merged_numbers = [0] * merged_size
        merge_pos = 0
        left_pos = i
        right_pos = j + 1

        left_bar, right_bar = left_pos, right_pos
        temp = self.values.copy()

        # Compares left and right merge and places lowest of each first.
        while left_pos <= j and right_pos <= key:
            self.vis[left_bar].set_color(self.vis_gold)
            self.vis[right_bar].set_color(self.vis_gold)
            plt.pause(pause_short)

            # If left bar less, it's already in place.
            if self.values[left_pos] <= self.values[right_pos]:
                if i != 0 or key != self.LENGTH-1:
                    self.vis[left_bar].set_color(self.vis_unsorted)
                else:
                    self.vis[left_bar].set_color(self.vis_green)
                self.vis[right_bar].set_color(self.vis_unsorted)
                left_bar += 1

                merged_numbers[merge_pos] = self.values[left_pos]
                left_pos += 1

            # If right bar is less, shifts everything in between left and right bar to the right.
            # Moves right bar to the left spot, moves the left bar one spot ahead.
            else:
                t = temp.copy()
                temp[left_bar] = self.values[right_pos]
                for b in range(left_bar, right_bar):
                    temp[b + 1] = t[b]
                    self.vis[b].set_height(temp[b])
                left_bar += 1
                self.vis[left_bar].set_color(self.vis_gold)
                self.vis[right_bar].set_height(temp[right_bar])
                self.vis[right_bar].set_color(self.vis_unsorted)
                right_bar += 1
                plt.pause(pause_short)
                if i != 0 or key != self.LENGTH-1:
                    self.vis[left_bar-1].set_color(self.vis_unsorted)
                else:
                    self.vis[left_bar-1].set_color(self.vis_green)
                self.vis[left_bar].set_color(self.vis_unsorted)

                merged_numbers[merge_pos] = self.values[right_pos]
                right_pos += 1

            merge_pos += 1

        # Runs when right merge ends before left merge. Rest of left's values are just added as it's already sorted.
        while left_pos <= j:
            self.vis[left_bar].set_color(self.vis_magenta)
            plt.pause(pause_short)
            if i != 0 or key != self.LENGTH-1:
                self.vis[left_bar].set_color(self.vis_unsorted)
            else:
                self.vis[left_bar].set_color(self.vis_green)
            left_bar += 1

            merged_numbers[merge_pos] = self.values[left_pos]
            left_pos += 1
            merge_pos += 1

        # Runs when left merge ends before right merge. Rest of right's values are just added as it's already sorted.
        while right_pos <= key:
            self.vis[right_bar].set_color(self.vis_magenta)
            plt.pause(pause_short)

            for b in range(left_bar, right_bar):  # Shifts bars between left and right-1 over by 1
                self.vis[b + 1].set_height(self.values[b])
            left_bar += 1
            self.vis[left_bar-1].set_height(self.values[right_pos])  # Moves right bar to left bar's original position
            self.vis[right_bar].set_color(self.vis_unsorted)  # Removes right bar's original position's color
            self.vis[left_bar-1].set_color(self.vis_magenta)    # Adds color to current right bar
            plt.pause(pause_short)
            if i != 0 or key != self.LENGTH - 1:
                self.vis[left_bar-1].set_color(self.vis_unsorted)  # Removes right bar's color
            else:
                self.vis[left_bar-1].set_color(self.vis_green)
            right_bar += 1

            merged_numbers[merge_pos] = self.values[right_pos]
            right_pos += 1
            merge_pos += 1

        # Commits the current sorted values to self.values. Redundant for visualization but necessary for the sort.
        for merge_pos in range(merged_size):
            self.values[i + merge_pos] = merged_numbers[merge_pos]

    def tim(self):
        min_run = self._min_run(self.LENGTH)

        for start in range(0, self.LENGTH, min_run):
            self.insertion()

        size = min_run
        while size < self.LENGTH:

            for left in range(0, self.LENGTH, 2 * size):

                mid = min(self.LENGTH - 1, left + size - 1)
                right = min((left + 2 * size - 1), (self.LENGTH - 1))

                if mid < right:
                    self._merge(left, mid, right)

            size = 2 * size

    @staticmethod
    def _min_run(n):
        MIN_MERGE = 32

        r = 0
        while n >= MIN_MERGE:
            r |= n & 1
            n >>= 1
        return n + r

    def radix(self):
        pause_short = self.pause
        pause_long = (self.pause * 3) + (self.LENGTH * 0.005)

        values = list(OrderedDict.fromkeys(self.values))   # Doesn't work with duplicate numbers so this ignores them.
        length = len(values)
        names = [i for i in range(length)]
        plt.clf()   # Might be problematic when showing multiple algos at once.
        self.vis = plt.bar(names, values, color=self.vis_unsorted)

        buckets = []
        for i in range(10):
            buckets.append([])

        max_digits = self._radix_max(values)
        pow_10 = 1

        for digit_index in range(max_digits):
            for num in values:
                bucket_index = (abs(num) // pow_10) % 10
                buckets[bucket_index].append(num)

            color = ''  # Used so each digit gets it's own color.
            temp = values.copy()

            if pow_10 == 1:
                color = self.vis_gold
            elif pow_10 == 10:
                color = self.vis_red
            elif pow_10 == 100:
                color = self.vis_magenta
            elif pow_10 == 1000:
                color = self.vis_cyan

            values.clear()
            for bucket in buckets:
                values.extend(bucket)
                bucket.clear()

            # Main tool for visualizing. Needs to be complicated to push values to the right rather than just replace.
            for b in range(length):
                index = temp.index(values[b])
                self.vis[b].set_color(color)
                self.vis[index].set_color(color)
                plt.pause(pause_short)

                t = temp.copy()
                temp[b] = values[b]
                for i in range(b, index):
                    temp[i + 1] = t[i]
                    self.vis[i].set_height(temp[i])
                self.vis[index].set_height(temp[index])
                self.vis[index].set_color(self.vis_unsorted)
                plt.pause(pause_short)
                if digit_index != max_digits-1:
                    self.vis[b].set_color(self.vis_unsorted)
                else:
                    self.vis[b].set_color(self.vis_green)

            plt.pause(pause_long)

            pow_10 = pow_10 * 10

        negatives = []
        non_negatives = []
        for num in values:
            if num < 0:
                negatives.append(num)
            else:
                non_negatives.append(num)
        negatives.reverse()
        values.clear()
        values.extend(negatives + non_negatives)

        plt.show()
        plt.clf()
        self.vis = plt.bar(self.names, self.values, color=self.vis_unsorted)    # To reset so other funcs can use

    def _radix_max(self, values):
        max_digits = 0
        for num in values:
            digit_count = self._radix_length(num)
            if digit_count > max_digits:
                max_digits = digit_count

        return max_digits

    @staticmethod
    def _radix_length(num):
        if num == 0:
            return 1

        digits = 0
        while num != 0:
            digits += 1
            num = int(num / 10)
        return digits

    # Equivalent of throwing a deck of cards in the air, picking them up randomly hoping it's sorted
    def bogo(self):
        pause_short = self.pause
        EXPECTED_RUN_TIME = self.LENGTH * ((np.math.factorial(self.LENGTH)) / 3.2)

        if EXPECTED_RUN_TIME < 60:
            title = f"This should be solved in about {np.round(EXPECTED_RUN_TIME, 2)} SECONDS"
        elif EXPECTED_RUN_TIME < 3600:
            title = f"""Expected solve time is {np.round((EXPECTED_RUN_TIME / 60), 2)} MINUTES."
Dare to increase array size?"""
        elif EXPECTED_RUN_TIME < 86400:
            title = f""""Only {np.round((EXPECTED_RUN_TIME / 3600), 2)} HOURS?
C'mon, that's over in the blink of an eye"""
        elif EXPECTED_RUN_TIME < 604800:
            title = f""""This is now your day job?
You'll be payed in {np.round((EXPECTED_RUN_TIME / 86400), 2)} DAYS"""
        elif EXPECTED_RUN_TIME < 2.628**6:
            title = f"""Family? Friends? The outside world?
Bah! You're gonna be here for {np.round((EXPECTED_RUN_TIME / 604800), 2)} WEEKS"""
        elif EXPECTED_RUN_TIME < 3.154**7:
            title = f"""This is some serious dedication you have, waiting for {np.round((EXPECTED_RUN_TIME / 2.628**6), 2)} MONTHS"
But since you're, here might as well go all the way right?"""
        elif EXPECTED_RUN_TIME < 3.154**107:
            title = f"""Here you discover the meaning of life. Get comfortable.
This may take some time. Only {np.round((EXPECTED_RUN_TIME / 3.154**7), 2)} YEARS"""
        else:
            title = f"""Congratulations! You won! What did you win? Well you'll just have to wait a measly
{np.round((EXPECTED_RUN_TIME / 3.154 ** 7), 2)} YEARS to find out. (The universe dies at 10e+100 YEARS btw.)"""

        plt.title(title)

        while not self._is_sorted():
            self._shuffle()
            for b in range(self.LENGTH):
                self.vis[b].set_height(self.values[b])
            plt.pause(pause_short)

        for i in range(self.LENGTH):
            self.vis[i].set_color(self.vis_green)
        plt.show()

    def _is_sorted(self):
        for b in range(0, self.LENGTH - 1):
            if self.values[b] > self.values[b + 1]:
                return False
        return True

    def _shuffle(self):
        for i in range(0, self.LENGTH):
            r = np.random.randint(0, self.LENGTH-1)
            self.values[i], self.values[r] = self.values[r], self.values[i]


if __name__ == '__main__':
    test = [4, 89, 1, 9, 69, 49, 149, 84, 15, 15, 79, 41, 9, 62, 19]    # Original test array. Use as base. 48/49
    test1 = [4, 89, 1, 9, 69, 49, 149, 84, 15, 79, 41, 62, 19]  # No duplicates
    test2 = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]

    dim = 100    # Range from 5 to 100
    test3 = np.random.randint(0, 150, dim)

    numbers = test3
    y = SortVisualizer(numbers)

    # y.merge()
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
