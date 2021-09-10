import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
from collections import OrderedDict

"""Visualizer for major sorting algorithms such as Mergesort, Heapsort, and Timsort.
Implemented with matplotlib and numpy.
"""


class SortVisualizer:
    """Where all the algorithms and operations reside."""

    def __init__(self, values=None):
        if not values:
            values = np.random.randint(0, 150, 30)
        self.values = values
        self.LENGTH = len(self.values)
        self.names = [i for i in range(self.LENGTH)]
        self.size = len(self.values)  # This is controlled by the slider in the interactive plot.
        self.is_sorted = False

        self.pause = 150 / self.LENGTH * 0.01  # 50 instead of 150 for replit. plt.pause(0.02) is the min it seems.
        self.vis_default = 'blue'
        self.vis_gold = 'gold'        # Checking
        self.vis_magenta = 'magenta'  # Pivot
        self.vis_cyan = 'cyan'        # Special value unique to that algorithm
        self.vis_green = 'green'      # Result
        self.vis_black = 'black'      # To swap
        self.vis_red = 'red'          # Moving

        self.vis = None               # Set plot by calling set_graph in driver code

    def set_graph(self, names=None, values=None, show_axis='None'):
        """Creates graph. Gets called each time it updates"""

        if not names:
            names = self.names
        if values is None:
            values = self.values

        # Clears previous graph for update
        plt.clf()
        self.vis = plt.bar(names, values, color=self.vis_default)
        plt.subplots_adjust(left=0.15, bottom=0.3)

        # Shows axis if called
        if show_axis == 'None':
            plt.axis('off')
        elif show_axis == 'x':
            plt.axis('on')
            plt.gca().axes.xaxis.set_visible(True)
            plt.gca().axes.yaxis.set_visible(False)
        elif show_axis == 'y':
            plt.axis('on')
            plt.gca().axes.xaxis.set_visible(True)
            plt.gca().axes.xaxis.set_visible(False)

        # Buttons ---------------------------------------------------------------------------

        generate_loc = plt.axes([0.35, 0.235, 0.3, 0.05])  # left, bottom, width, height
        generate = Button(ax=generate_loc, label='Generate New Array', color='cyan')
        stop_loc = plt.axes([0.85, 0.03, 0.1, 0.05])  # left, bottom, width, height
        stop = Button(ax=stop_loc, label='Stop', color='red')
        size_loc = plt.axes([0.05, 0.235, 0.05, 0.5])
        size = Slider(ax=size_loc, label='Size & Speed', valmin=5, valmax=100,
                      valinit=self.size, valstep=1, orientation='vertical')
        sel_loc = plt.axes([0.225, 0.03, 0.15, 0.05])
        sel = Button(ax=sel_loc, label='Selection', color='orange')
        ins_loc = plt.axes([0.625, 0.1, 0.15, 0.05])
        ins = Button(ax=ins_loc, label='Insertion', color='orange')
        bub_loc = plt.axes([0.425, 0.03, 0.15, 0.05])
        bub = Button(ax=bub_loc, label='Bubble', color='orange')
        heap_loc = plt.axes([0.225, 0.1, 0.15, 0.05])
        heap = Button(ax=heap_loc, label='Heapsort', color='yellow')
        quick_loc = plt.axes([0.625, 0.17, 0.15, 0.05])
        quick = Button(ax=quick_loc, label='Quicksort', color='green')
        merge_loc = plt.axes([0.225, 0.17, 0.15, 0.05])
        merge = Button(ax=merge_loc, label='Mergesort', color='green')
        tim_loc = plt.axes([0.425, 0.1, 0.15, 0.05])
        tim = Button(ax=tim_loc, label='Timsort', color='yellow')
        radix_loc = plt.axes([0.425, 0.17, 0.15, 0.05])
        radix = Button(ax=radix_loc, label='Radix', color='green')
        bogo_loc = plt.axes([0.625, 0.03, 0.15, 0.05])
        bogo = Button(ax=bogo_loc, label='Bogosort', color='tomato')

        def generate_new_array(_):      # Argument is typically called event but using _ to suppress errors
            self.values = np.random.randint(0, 150, self.LENGTH)
            self.set_graph()
            self.is_sorted = False
            generate.disconnect(generate_cid)

        def stop_graph(_):
            plt.close()
            self.set_graph()
            self.is_sorted = True
            stop.disconnect(stop_cid)

        def change_size(_):
            self.size = int(size.val)
            self.update_values()
            self.is_sorted = False

        def sel_sort(_):
            if self.is_sorted:
                self.values = np.random.randint(0, 150, self.LENGTH)
                self.set_graph()
            self.is_sorted = True
            self.selection()
            sel.disconnect(sel_cid)

        def ins_sort(_):
            if self.is_sorted:
                self.values = np.random.randint(0, 150, self.LENGTH)
                self.set_graph()
            self.is_sorted = True
            self.insertion()
            ins.disconnect(ins_cid)

        def bub_sort(_):
            if self.is_sorted:
                self.values = np.random.randint(0, 150, self.LENGTH)
                self.set_graph()
            self.is_sorted = True
            self.bubble()
            bub.disconnect(bub_cid)

        def heap_sort(_):
            if self.is_sorted:
                self.values = np.random.randint(0, 150, self.LENGTH)
                self.set_graph()
            self.is_sorted = True
            self.heap()
            heap.disconnect(heap_cid)

        def quick_sort(_):
            if self.is_sorted:
                self.values = np.random.randint(0, 150, self.LENGTH)
                self.set_graph()
            self.is_sorted = True
            self.quick()
            quick.disconnect(quick_cid)

        def merge_sort(_):
            if self.is_sorted:
                self.values = np.random.randint(0, 150, self.LENGTH)
                self.set_graph()
            self.is_sorted = True
            self.merge()
            merge.disconnect(merge_cid)

        def tim_sort(_):
            if self.is_sorted:
                self.values = np.random.randint(0, 150, self.LENGTH)
                self.set_graph()
            self.is_sorted = True
            self.tim()
            tim.disconnect(tim_cid)

        def radix_sort(_):
            if self.is_sorted:
                self.values = np.random.randint(0, 150, self.LENGTH)
                self.set_graph()
            self.is_sorted = True
            self.radix()
            radix.disconnect(radix_cid)

        def bogo_sort(_):
            if self.is_sorted:
                self.values = np.random.randint(0, 150, self.LENGTH)
                self.set_graph()
            self.is_sorted = True
            self.bogo()
            bogo.disconnect(bogo_cid)

        generate_cid = generate.on_clicked(generate_new_array)
        stop_cid = stop.on_clicked(stop_graph)
        size.on_changed(change_size)
        sel_cid = sel.on_clicked(sel_sort)
        ins_cid = ins.on_clicked(ins_sort)
        bub_cid = bub.on_clicked(bub_sort)
        heap_cid = heap.on_clicked(heap_sort)
        quick_cid = quick.on_clicked(quick_sort)
        merge_cid = merge.on_clicked(merge_sort)
        tim_cid = tim.on_clicked(tim_sort)
        radix_cid = radix.on_clicked(radix_sort)
        bogo_cid = bogo.on_clicked(bogo_sort)

        plt.show()

    def update_values(self):
        """Used for updating slider of array size"""

        self.LENGTH = self.size
        self.values = np.random.randint(0, 150, self.LENGTH)
        self.names = [i for i in range(self.LENGTH)]
        self.pause = 150 / self.LENGTH * 0.01
        self.set_graph()

    def selection(self):
        """Goes through list comparing values of the current number to all values after, swapping as needed.
        Complexity: Time - O(n^2), Space - O(1), Unstable
        """

        pause_short = self.pause
        pause_long = (self.pause * 3) + (self.LENGTH * 0.001)

        for i in range(self.LENGTH - 1):
            self.vis[i].set_color(self.vis_black)
            plt.pause(pause_long)

            index = i
            for j in range(i + 1, self.LENGTH):
                self.vis[j].set_color(self.vis_gold)
                plt.pause(pause_short)

                if self.values[j] < self.values[index]:
                    self.vis[j].set_color(self.vis_cyan)
                    if index != i:
                        self.vis[index].set_color(self.vis_gold)

                    index = j

            # Swaps bars while maintaining color for each
            self.vis[i].set_height(self.values[index])
            self.vis[i].set_color(self.vis_cyan)
            self.values[i], self.values[index] = self.values[index], self.values[i]
            self.vis[index].set_height(self.values[index])
            self.vis[index].set_color(self.vis_black)
            plt.pause(pause_long)

            self.vis[i].set_color(self.vis_green)
            for b in range(i+1, self.LENGTH):
                self.vis[b].set_color(self.vis_default)

            if i == self.LENGTH-2:
                for b in range(i, self.LENGTH):
                    self.vis[b].set_color(self.vis_green)

        plt.draw()

    def insertion(self):
        """Splits input into the sorted and unsorted parts. Places unsorted elements to the correct position.
        Complexity: Time - O(n^2), Space - O(1), Stable
        """

        pause_short = self.pause

        for i in range(1, self.LENGTH):
            a = i

            self.vis[a].set_color(self.vis_red)

            while a > 0 and self.values[a] < self.values[a - 1]:
                # Swaps bars while maintaining color for each
                self.vis[a].set_color(self.vis_red)
                self.vis[a-1].set_color(self.vis_gold)
                plt.pause(pause_short)
                self.vis[a].set_color(self.vis_default)
                self.vis[a-1].set_color(self.vis_default)

                self.vis[a].set_height(self.values[a-1])
                self.values[a], self.values[a-1] = self.values[a-1], self.values[a]
                self.vis[a-1].set_height(self.values[a-1])

                a -= 1
            else:
                if a < self.LENGTH-1:
                    self.vis[a+1].set_color(self.vis_gold)
                self.vis[a].set_color(self.vis_red)
                plt.pause(pause_short)
                if a < self.LENGTH - 1:
                    self.vis[a+1].set_color(self.vis_default)
                self.vis[a].set_color(self.vis_default)

        for b in range(self.LENGTH):
            self.vis[b].set_color(self.vis_green)
        plt.draw()

    def bubble(self):
        """Swaps adjacent elements if they are in the wrong order.
        Repeats n-1 times with max index to check decreasing by 1.
        Complexity: Time - O(n^2), Space - O(1), Stable
        """

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

                self.vis[j].set_color(self.vis_default)
                self.vis[j+1].set_color(self.vis_default)

                if j == self.LENGTH-i - 2:
                    self.vis[j+1].set_color(self.vis_green)

        self.vis[0].set_color(self.vis_green)
        plt.draw()

    def heap(self):
        """Converts input into a max heap data structure and pops values.
        Complexity: Time - O(nlog(n)), Space - O(1), Unstable
        """

        pause_short = self.pause
        pause_long = (self.pause * 3) + (self.LENGTH * 0.005)

        # Puts values in heap
        for i in range(self.LENGTH // 2 - 1, -1, -1):
            self._heap(self.LENGTH, i, pause_short)

        # Show that values are now in heap
        for b in range(self.LENGTH):
            self.vis[b].set_color(self.vis_black)
        plt.pause(pause_long)

        # Sorts values from min to max, max first
        for i in range(self.LENGTH - 1, 0, -1):
            self.vis[i].set_color(self.vis_gold)
            self.vis[0].set_color(self.vis_gold)
            for b in range(i):
                self.vis[b].set_color(self.vis_black)
            plt.pause(pause_short)
            for b in range(i):
                self.vis[b].set_color(self.vis_default)

            self.vis[i].set_height(self.values[0])
            self.values[i], self.values[0] = self.values[0], self.values[i]
            self.vis[0].set_height(self.values[0])
            self.vis[i].set_color(self.vis_green)
            plt.pause(pause_short)
            self.vis[0].set_color(self.vis_default)

            self._heap(i, 0, pause_short)

        self.vis[0].set_color(self.vis_green)
        plt.draw()

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

        self.vis[i].set_color(self.vis_default)
        if left < length:
            self.vis[left].set_color(self.vis_default)
        if right < length:
            self.vis[right].set_color(self.vis_default)

    def quick(self, start=0, end=-1):   # Weird bug where bar is misplaced only once. Can't trace it.
        """Sets a pivot value and places every value below the pivot before and all values greater after.
        Repeats recursively until only single element partitions remains.
        Complexity: Time - O(nlog(n)), Space - O(log(n)), Unstable
        """

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
            plt.draw()

    def _quick(self, start, end):
        pause_short = self.pause

        mid = start + (end - start) // 2
        pivot = self.values[mid]

        self.vis[mid].set_color(self.vis_magenta)
        plt.pause(pause_short)

        low = start
        high = end

        done = False
        while not done:
            while self.values[low] < pivot:
                if low != mid:
                    self.vis[low].set_color(self.vis_red)
                    plt.pause(pause_short)
                low += 1

            while pivot < self.values[high]:
                if high != mid:
                    self.vis[high].set_color(self.vis_cyan)
                    plt.pause(pause_short)
                high -= 1

            if low >= high:
                done = True
            else:
                if low != mid:
                    self.vis[low].set_color(self.vis_cyan)
                if high != mid:
                    self.vis[high].set_color(self.vis_red)
                plt.pause(pause_short)
                if low != mid and high != mid:
                    self.vis[low].set_color(self.vis_red)
                    self.vis[high].set_color(self.vis_cyan)
                elif low == mid and high == mid:
                    self.vis[mid].set_color(self.vis_magenta)     # Does nothing. Avoiding using pass
                elif low == mid:
                    self.vis[low].set_color(self.vis_red)
                    self.vis[high].set_color(self.vis_magenta)
                elif high == mid:
                    self.vis[high].set_color(self.vis_cyan)
                    self.vis[low].set_color(self.vis_magenta)

                self.vis[low].set_height(self.values[high])
                self.values[low], self.values[high] = self.values[high], self.values[low]
                self.vis[high].set_height(self.values[high])
                plt.pause(pause_short)

                low += 1
                high -= 1

        for b in range(start, end+1):
            self.vis[b].set_color(self.vis_default)

        if end - start <= 1:
            for i in range(end+1):
                self.vis[i].set_color(self.vis_green)

        return high

    def merge(self, i=0, key=-1):
        """Recursively splits input in halves. Sorts each element at each level bottom up.
        Complexity: Time - O(nlog(n)), Space - O(n), Stable
        """

        if key == -1:
            key = self.LENGTH - 1

        if i < key:
            j = (i + key) // 2

            self.merge(i, j)
            self.merge(j + 1, key)

            self._merge(i, j, key)

        if i == 0 and key == self.LENGTH - 1:
            plt.draw()

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
            self.vis[left_bar].set_color(self.vis_red)
            self.vis[right_bar].set_color(self.vis_gold)
            plt.pause(pause_short)

            # If left bar less, it's already in place.
            if self.values[left_pos] <= self.values[right_pos]:
                if i != 0 or key != self.LENGTH-1:
                    self.vis[left_bar].set_color(self.vis_default)
                else:
                    self.vis[left_bar].set_color(self.vis_green)
                self.vis[right_bar].set_color(self.vis_default)
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
                self.vis[left_bar].set_color(self.vis_red)
                self.vis[right_bar].set_height(temp[right_bar])
                self.vis[right_bar].set_color(self.vis_default)
                right_bar += 1
                plt.pause(pause_short)
                if i != 0 or key != self.LENGTH-1:
                    self.vis[left_bar-1].set_color(self.vis_default)
                else:
                    self.vis[left_bar-1].set_color(self.vis_green)
                self.vis[left_bar].set_color(self.vis_default)

                merged_numbers[merge_pos] = self.values[right_pos]
                right_pos += 1

            merge_pos += 1

        # Runs when right merge ends before left merge. Rest of left's values are just added as it's already sorted.
        while left_pos <= j:
            self.vis[left_bar].set_color(self.vis_magenta)
            plt.pause(pause_short)
            if i != 0 or key != self.LENGTH-1:
                self.vis[left_bar].set_color(self.vis_default)
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
            self.vis[right_bar].set_color(self.vis_default)  # Removes right bar's original position's color
            self.vis[left_bar-1].set_color(self.vis_magenta)    # Adds color to current right bar
            plt.pause(pause_short)
            if i != 0 or key != self.LENGTH - 1:
                self.vis[left_bar-1].set_color(self.vis_default)  # Removes right bar's color
            else:
                self.vis[left_bar-1].set_color(self.vis_green)
            right_bar += 1

            merged_numbers[merge_pos] = self.values[right_pos]
            right_pos += 1
            merge_pos += 1

        # Commits the current sorted values to self.values. Redundant for visualization but necessary for the sort.
        for merge_pos in range(merged_size):
            self.values[i + merge_pos] = merged_numbers[merge_pos]

    def tim(self):      # Seems to use insertion too much. Possibly a bug.
        """Combination of merge sort and insertion sort.
        Divides input into blocks, sorts using insertion, combines using merge.
        Complexity: Time - O(nlog(n)), Space - O(1), Stable
        """

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
        MIN_MERGE = 51

        r = 0
        while n >= MIN_MERGE:
            r |= n & 1
            n >>= 1
        return n + r

    def radix(self):
        """Only for integers. Places values into buckets from the least to most significant digit. Sorts with buckets
        Complexity: Time - O(n*k), Space - O(n+k), Stable
        """

        values = list(OrderedDict.fromkeys(self.values))   # Doesn't work with duplicate numbers so this ignores them.
        length = len(values)
        names = [i for i in range(length)]
        self.set_graph(names, values, show_axis='None')
        pause_short = self.pause
        pause_long = (self.pause * 3) + (self.LENGTH * 0.005)

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
                color = self.vis_cyan
            elif pow_10 == 10:
                color = self.vis_magenta
            elif pow_10 == 100:
                color = self.vis_red
            elif pow_10 == 1000:
                color = self.vis_black

            values.clear()
            for bucket in buckets:
                values.extend(bucket)
                bucket.clear()

            # Main tool for visualizing. Needs to be complicated to push values to the right rather than just replace.
            for b in range(length):
                index = temp.index(values[b])
                self.vis[b].set_color(color)
                self.vis[index].set_color(self.vis_gold)
                plt.pause(pause_short)

                t = temp.copy()
                temp[b] = values[b]
                for i in range(b, index):
                    temp[i + 1] = t[i]
                    self.vis[i].set_height(temp[i])
                self.vis[index].set_height(temp[index])
                self.vis[index].set_color(self.vis_default)
                plt.pause(pause_short)
                if digit_index != max_digits-1:
                    self.vis[b].set_color(self.vis_default)
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

        plt.draw()
        # self.set_graph()    # To reset so other funcs can use. Causes reset after it's finished.

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
        """Equivalent of throwing a deck of cards in the air, picking them up randomly hoping it's sorted
        Complexity: Time - O(n*n!), Space - O(1), Unstable
        """

        pause_short = self.pause
        EXPECTED_RUN_TIME = ((np.math.factorial(self.LENGTH)) / 4)

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
            text = f"""This is some serious dedication you have, waiting for {round((EXPECTED_RUN_TIME / 2.628**6), 2)} MONTHS"
But since you're, here might as well go all the way right?"""
        elif EXPECTED_RUN_TIME < 3.154**107:
            text = f"""Here you discover the meaning of life. Get comfortable. This make take 
time. Only {round((EXPECTED_RUN_TIME / 3.154**7), 2)} YEARS"""
        else:
            text = f"""Congratulations! You won! What did you win? Well you'll just have to wait a 
measly {round((EXPECTED_RUN_TIME / 3.154 ** 7), 2)} YEARS to find out.
(The universe dies at 10e+100 YEARS btw.)"""

        plt.suptitle(text)

        while not self._is_sorted():
            self._shuffle()
            for b in range(self.LENGTH):
                self.vis[b].set_height(self.values[b])
            plt.pause(pause_short)

        for i in range(self.LENGTH):
            self.vis[i].set_color(self.vis_green)
        plt.draw()

    def _is_sorted(self):
        for b in range(0, self.LENGTH - 1):
            if self.values[b] > self.values[b + 1]:
                return False
        return True

    def _shuffle(self):
        for i in range(0, self.LENGTH):
            r = np.random.randint(0, self.LENGTH-1)
            self.values[i], self.values[r] = self.values[r], self.values[i]