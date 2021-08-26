import math
from heapq import heappush, heappop
import matplotlib.pyplot as plt

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


# Putting plt.pause() in if statements are what causes the outline color and slows down visualizer. Only part of it
# Check on larger list. Make sure all edge cases are dealt with.
# Return non sorted value for algorithms that require sort
# Use dict of key=Values and value=index in reverse order to get original index for searches. Or use list values[0]

# Remove temp variable for swaping two values. Will have to change bar updating method
# Seems as though you can only call each search function once. Need to fix for actual deployment
# Create subplots to visualize multiple at once
# Currently this gets rid of duplicates nums. See test4
# Optimize so you don't need to clear graph each update
# Use an upside down bar graph
# Add note: Animation speed for each algorithm is chosen for clarity and not completely indicative of real world speed.
# Choose different pause_short and pause_long for each algorithm
# Animated graphs?

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


class SortVisualizer:
    """Example docstring.

    Add these for every class and function. https://www.python.org/dev/peps/pep-0257/#multi-line-docstrings
    """

    def __init__(self, values, pause_short=0.1, pause_long=0.2):
        """Single line doc string"""
        self.values = values
        self.LENGTH = len(self.values)
        # self.names = [str(i) for i in self.values]    - Bar names need to be unique or they overlap. This fails
        self.names = [i for i in range(self.LENGTH)]
        plt.gca().axes.xaxis.set_visible(False)
        self.vis_unsorted = 'blue'

        self.vis = plt.bar(self.names, self.values, color=self.vis_unsorted)
        self.pause_short = pause_short
        self.pause_long = pause_long
        self.vis_pivot = 'red'
        self.vis_min = 'magenta'
        self.vis_checking = 'gold'
        self.vis_sorted = 'green'
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
                plt.pause(self.pause_long)

                if self.values[j] > self.values[j+1]:
                    # Swaps bars while maintaining color for each
                    self.vis[j].set_height(self.values[j+1])
                    self.vis[j].set_color(self.vis_checking)
                    self.values[j], self.values[j+1] = self.values[j+1], self.values[j]
                    self.vis[j+1].set_height(self.values[j+1])
                    self.vis[j+1].set_color(self.vis_pivot)
                    plt.pause(self.pause_long)

                self.vis[j].set_color(self.vis_unsorted)
                self.vis[j+1].set_color(self.vis_unsorted)

                if j == self.LENGTH-i - 2:
                    self.vis[j+1].set_color(self.vis_sorted)

        self.vis[0].set_color(self.vis_sorted)
        plt.show()

    def merge(self, i=0, key=-1):
        if key == -1:
            key = len(self.values) - 1

        if i < key:
            j = (i + key) // 2

            self.merge(i, j)
            self.merge(j + 1, key)

            self._merge(self.values, i, j, key)

    # Or just move everything over by 1
    # Set bars to green as doing the final merge. When j is half.
    def _merge(self, numbers, i, j, key):   # Is numbers necessary or can i replace with self.values
        merged_size = key - i + 1
        merged_numbers = [0] * merged_size
        merge_pos = 0
        left_pos = i
        right_pos = j + 1

        # Compares left and right merge and places lowest of each first.
        while left_pos <= j and right_pos <= key:
            self.vis[left_pos].set_color(self.vis_checking)
            self.vis[right_pos].set_color(self.vis_checking)
            plt.pause(self.pause_long)

            if numbers[left_pos] <= numbers[right_pos]:
                self.vis[i + merge_pos].set_height(numbers[left_pos])
                self.vis[left_pos].set_color(self.vis_unsorted)

                merged_numbers[merge_pos] = numbers[left_pos]
                left_pos += 1
            else:
                self.vis[i + merge_pos].set_height(numbers[right_pos])
                self.vis[right_pos].set_color(self.vis_unsorted)

                merged_numbers[merge_pos] = numbers[right_pos]
                right_pos += 1

            merge_pos = merge_pos + 1
        else:
            if left_pos > j:
                self.vis[right_pos].set_color(self.vis_unsorted)
            else:
                self.vis[left_pos].set_color(self.vis_unsorted)

        # Runs when right merge ends before left merge. Rest of left's values are just added as it's already sorted.
        while left_pos <= j:
            self.vis[i + merge_pos].set_color(self.vis_checking)
            plt.pause(self.pause_long)
            self.vis[i + merge_pos].set_height(numbers[left_pos])
            self.vis[i + merge_pos].set_color(self.vis_unsorted)

            merged_numbers[merge_pos] = numbers[left_pos]
            left_pos += 1
            merge_pos += 1

        # Runs when left merge ends before right merge. Rest of right's values are just added as it's already sorted.
        while right_pos <= key:
            self.vis[i + merge_pos].set_color(self.vis_checking)
            plt.pause(self.pause_long)
            self.vis[i + merge_pos].set_height(numbers[right_pos])
            self.vis[i + merge_pos].set_color(self.vis_unsorted)

            merged_numbers[merge_pos] = numbers[right_pos]
            right_pos = right_pos + 1
            merge_pos = merge_pos + 1

        # Commits the current sorted values to self.values. Redundant for visualization but necessary for the sort.
        for merge_pos in range(merged_size):
            numbers[i + merge_pos] = merged_numbers[merge_pos]

    def timsort(self):
        pass

    def quicksort(self):
        pass

    def heap(self):
        pass

    def counting(self):
        pass

    def radix(self):
        pass

# Search for len( and replace with self.LENGTH


if __name__ == '__main__':
    import random

    test = [4, 89, 1, 9, 69, 49, 149, 84, 15, 15, 79, 41, 9, 62, 19]    # Original test array. Use as base. 48/49
    test2 = random.sample(range(1000), 1000)
    test3 = [74, 83, 4, 62, 23, 71, 22, 13, 69, 6, 16, 9, 99, 97, 34, 18, 93, 61, 15, 64, 55, 72, 35, 50, 63, 25, 26, 54, 36, 47, 2, 66, 38, 81, 95, 46, 79, 77, 28, 49, 56, 76, 41, 27, 82, 24, 10, 7, 3, 75, 48, 90, 51, 98, 33, 21, 37, 52, 80, 17, 42, 29, 19, 11, 20, 96, 43, 59, 57, 88, 8, 5, 94, 84, 87, 68, 30, 60, 12, 0, 1, 40, 14, 31, 45, 92, 70, 32, 67, 73, 78, 89, 65, 44, 86, 53, 39, 58, 85, 91]
    test4 = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    k = 49

    y = SortVisualizer(test, 0.1, .25)

    # y.selection()
    # y.insertion()
    # y.bubble()
    y.merge()
    # y.timsort()
    # y.quicksort()
    # y.heap()
    # y.counting()
    # y.radix()

    plt.show()  # Put this in visualize for merge
    print(y.values)

# ---------------------------------------------------------

    # x = SearchVisualizer(test3)
    # x.values_sort()

    # x.comparison(k)
    # x.linear(k)
    # x.binary(k)
    # x.jump(k)
    # x.exponential(k)
    # x.fibonacci(k)
