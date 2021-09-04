import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, TextBox


class SearchVisualizer:
    def __init__(self, values=None):
        if not values:
            values = np.random.randint(0, 150, 30)
        self.values = values
        self.LENGTH = len(values)
        self.names = [i for i in range(self.LENGTH)]
        self.size = len(self.values)
        self.key = 44

        self.pause = 150 / self.LENGTH * 0.01  # 50 instead of 150 for replit. plt.pause(0.02) is the min it seems
        self.vis_default = 'blue'
        self.vis_gold = 'gold'          # Checking
        self.vis_magenta = 'magenta'    # Pivot
        self.vis_cyan = 'cyan'          # Special value unique to that algorithm
        self.vis_green = 'green'        # Result
        self.vis_red = 'red'            # Checked but false
        self.vis_black = 'black'        # Misc

        self.vis = None                 # Set plot by calling set_graph in driver code

    def set_graph(self, names=None, values=None, show_axis='None'):
        if not names:
            names = self.names
        if values is None:
            values = self.values

        plt.clf()
        self.vis = plt.bar(names, values, color=self.vis_default)
        plt.subplots_adjust(left=0.15, bottom=0.3)

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

        generate_loc = plt.axes([0.2, 0.2, 0.3, 0.05])  # left, bottom, width, height
        generate = Button(ax=generate_loc, label='Generate New Array', color='cyan')
        stop_loc = plt.axes([0.85, 0.01, 0.1, 0.05])  # left, bottom, width, height
        stop = Button(ax=stop_loc, label='Stop', color='red')
        size_loc = plt.axes([0.05, 0.235, 0.05, 0.5])
        size = Slider(ax=size_loc, label='Size & Speed', valmin=5, valmax=100,
                      valinit=self.size, valstep=1, orientation='vertical')
        text_loc = plt.axes([0.475, 0.01, 0.3, 0.05])
        text = TextBox(ax=text_loc, label='Enter search value (1-150): ', initial=str(self.key))
        sort_loc = plt.axes([0.60, 0.2, 0.3, 0.05])
        sort = Button(ax=sort_loc, label='Sort Array', color='cyan')
        linear_loc = plt.axes([0.825, 0.1, 0.15, 0.05])
        linear = Button(ax=linear_loc, label='Linear', color='yellow')
        binary_loc = plt.axes([0.025, 0.1, 0.15, 0.05])
        binary = Button(ax=binary_loc, label='Binary', color='green')
        jump_loc = plt.axes([0.225, 0.1, 0.15, 0.05])
        jump = Button(ax=jump_loc, label='Jump', color='green')
        exp_loc = plt.axes([0.425, 0.1, 0.15, 0.05])
        exp = Button(ax=exp_loc, label='Exponential', color='green')
        fib_loc = plt.axes([0.625, 0.1, 0.15, 0.05])
        fib = Button(ax=fib_loc, label='Fibonacci', color='green')

        def generate_new_array(_):      # Argument is typically called event but using _ to suppress errors
            self.values = np.random.randint(0, 150, self.LENGTH)
            self.set_graph()
            generate.disconnect(generate_cid)

        def stop_graph(_):
            plt.close()
            self.set_graph()
            stop.disconnect(stop_cid)

        def change_size(_):
            self.size = int(size.val)
            self.update_values()

        def change_key(_):
            try:
                if int(text.text) > 0:
                    self.key = int(text.text)
                else:
                    self.key = 44
            except ValueError:
                self.key = 44

        def sort_array(_):
            self.values.sort()
            self.set_graph()
            sort.disconnect(sort_cid)

        def linear_search(_):
            self.linear(self.key)
            linear.disconnect(linear_cid)

        def binary_search(_):
            self.binary(self.key)
            binary.disconnect(binary_cid)

        def jump_search(_):
            self.jump(self.key)
            jump.disconnect(jump_cid)

        def exp_search(_):
            self.exponential(self.key)
            exp.disconnect(exp_cid)

        def fib_search(_):
            self.fibonacci(self.key)
            fib.disconnect(fib_cid)

        generate_cid = generate.on_clicked(generate_new_array)
        stop_cid = stop.on_clicked(stop_graph)
        size.on_changed(change_size)
        text.on_submit(change_key)
        sort_cid = sort.on_clicked(sort_array)
        linear_cid = linear.on_clicked(linear_search)
        binary_cid = binary.on_clicked(binary_search)
        jump_cid = jump.on_clicked(jump_search)
        exp_cid = exp.on_clicked(exp_search)
        fib_cid = fib.on_clicked(fib_search)

        plt.show()

    def update_values(self):
        self.LENGTH = self.size
        self.values = np.random.randint(0, 150, self.LENGTH)
        self.names = [i for i in range(self.LENGTH)]
        self.pause = 150 / self.LENGTH * 0.01
        self.set_graph()

    def visualize(self, res):
        if isinstance(res, int):
            if res > -1:
                for i in range(self.LENGTH):
                    self.vis[i].set_color(self.vis_red)
                self.vis[res].set_color(self.vis_green)
            else:
                for i in range(self.LENGTH):
                    self.vis[i].set_color(self.vis_red)

        else:
            if res[0] > -1:
                if res[0] < self.LENGTH:
                    for i in range(self.LENGTH):
                        self.vis[i].set_color(self.vis_red)
                    self.vis[res[0]].set_color(self.vis_green)
            else:
                for i in range(self.LENGTH):
                    self.vis[i].set_color(self.vis_red)

        plt.draw()

    def linear(self, key):  # Only algorithm that does not require sorted values. Use to find unsorted index.
        """Loops through array once and returns the first item of value key. Complexity: Time - O(n), Space - O(1)"""
        self.set_graph()
        pause_short = self.pause

        for i in range(self.LENGTH):
            self.vis[i].set_color(self.vis_gold)
            plt.pause(pause_short)

            if self.values[i] != key:
                self.vis[i].set_color(self.vis_red)
                plt.pause(pause_short)
                if i == self.LENGTH-1:
                    return self.visualize(-i)
            else:
                for b in range(self.LENGTH):
                    self.vis[b].set_color(self.vis_red)
                return self.visualize(i)

    def binary(self, key, high=None, reset=True):
        """Divides values into halves and checks if key is in that half.
        Continues until no longer possible. Requires sorted values. Complexity: Time - O(log(n)), Space - O(1)
        """
        if reset is True:   # Exponential calls binary. This is to avoid resetting colors when it does.
            self.values.sort()
            self.set_graph()
            plt.pause(1)
        pause_long = (self.pause * 3) + (self.LENGTH * 0.005)

        if not high:
            high = self.LENGTH
        low = 0
        mid = (high + low) // 2
        upper = high

        while high >= low:
            mid = (high + low) // 2

            if mid >= self.LENGTH:
                mid = self.LENGTH-1
                if mid == key:
                    for i in range(low - 1, mid):
                        self.vis[i].set_color(self.vis_red)
                    for i in range(mid + 1, upper):
                        self.vis[i].set_color(self.vis_red)
                    return self.visualize(mid)
                else:
                    for i in range(self.LENGTH):
                        self.vis[i].set_color(self.vis_red)
                    plt.draw()
                    return

            self.vis[mid].set_color(self.vis_magenta)
            plt.pause(pause_long)

            if self.values[mid] > key:
                if high < self.LENGTH-2:
                    upper = high+1
                else:
                    upper = high
                for i in range(mid, upper):
                    self.vis[i].set_color(self.vis_red)
                high = mid - 1
            elif self.values[mid] < key:
                if low > 1:
                    lower = low-1
                else:
                    lower = low
                for i in range(lower, mid):
                    self.vis[i].set_color(self.vis_red)
                low = mid + 1
            else:
                for i in range(low-1, mid):
                    self.vis[i].set_color(self.vis_red)
                for i in range(mid+1, upper):
                    self.vis[i].set_color(self.vis_red)
                return self.visualize(mid)

        if mid != key:
            mid = -1

        for i in range(self.LENGTH):
            self.vis[i].set_color(self.vis_red)
        return self.visualize(mid)

    def jump(self, key):
        """Optimization for linear search. Similar to binary but steps by a sqrt(n) instead of halving current window.
        Requires sorted values. Complexity: Time - O(sqrt(n)), Space - O(1)
        """
        self.values.sort()
        self.set_graph()
        plt.pause(1)
        pause_short = self.pause
        pause_long = (self.pause * 3) + (self.LENGTH * 0.005)

        step = int(np.sqrt(self.LENGTH))     # Using numpy for sqrt, one less thing to import.
        left, right = 0, 0

        while left < self.LENGTH and self.values[left] <= key:
            right = min(self.LENGTH - 1, left + step)

            self.vis[left].set_color(self.vis_cyan)
            self.vis[right].set_color(self.vis_cyan)
            plt.pause(pause_long)

            if self.values[left] <= key <= self.values[right]:
                for i in range(right+1, self.LENGTH):
                    self.vis[i].set_color(self.vis_red)
                plt.pause(pause_long)
                break
            left += step

            for i in range(left):
                if i < self.LENGTH:
                    self.vis[i].set_color(self.vis_red)

        if left >= self.LENGTH or self.values[left] > key:
            if left != key:
                left = -1
            return self.visualize((left, right))

        right = min(self.LENGTH - 1, right)
        i = left

        while i <= right and self.values[i] <= key:
            self.vis[i].set_color(self.vis_gold)
            plt.pause(pause_short)

            if self.values[i] == key:
                return self.visualize((i, right))
            self.vis[i].set_color(self.vis_red)
            plt.pause(pause_short)
            i += 1

        return self.visualize((-i, right))

    # Does weird stuff when searching for 48 with values. The height arg for binary search probably is the cause.
    def exponential(self, key):
        """Optimization for binary search. Faster finding of upper bound.
        Finds upper bound in 2^i operations where i is the desired index. Complexity: Time - O(log(i)), Space - O(1)
        Best when index is relatively close to the beginning of the array, such as with unbounded or infinite arrays
        """
        self.values.sort()
        self.set_graph()
        plt.pause(1)
        pause_long = (self.pause * 3) + (self.LENGTH * 0.005)

        self.vis[0].set_color(self.vis_gold)
        plt.pause(pause_long)
        self.vis[0].set_color(self.vis_red)

        if self.values[0] == key:
            for i in range(1, self.LENGTH):
                self.vis[i].set_color(self.vis_red)
            return 0

        i = temp_low = temp = 1
        self.vis[0].set_color(self.vis_red)
        self.vis[i].set_color(self.vis_gold)

        while i < self.LENGTH and self.values[i] <= key:
            i *= 2
            if i <= self.LENGTH:
                for j in range(temp_low, temp):
                    self.vis[j].set_color(self.vis_red)
                self.vis[i].set_color(self.vis_cyan)
            plt.pause(pause_long)
            temp = i
            temp_low = int(temp / 2)

        if i <= self.LENGTH:
            for j in range(i+1, self.LENGTH):
                self.vis[j].set_color(self.vis_red)

        if i < self.LENGTH:
            return self.binary(key, i, reset=False)
        else:
            return self.binary(key, reset=False)

    def fibonacci(self, key):
        """Creates fibonacci numbers up to the length of the list, then iterates downward until target value is in range
        Useful for very large numbers as it avoids division. Complexity: Time - O(log(n)), Space - O(1)
        """
        self.values.sort()
        self.set_graph()
        plt.pause(1)
        pause_long = (self.pause * 3) + (self.LENGTH * 0.005)

        fib_minus_2 = 0
        fib_minus_1 = 1
        fib = fib_minus_1 + fib_minus_2
        i = 1

        self.vis[fib_minus_2].set_color(self.vis_cyan)
        plt.pause(pause_long)

        while fib < self.LENGTH:
            fib_minus_2 = fib_minus_1
            fib_minus_1 = fib
            fib = fib_minus_1 + fib_minus_2

            if fib < self.LENGTH:
                self.vis[fib].set_color(self.vis_cyan)
                plt.pause(pause_long)

        index = -1

        while fib > 1:
            i = min(index + fib_minus_2, (self.LENGTH - 1))

            self.vis[i].set_color(self.vis_magenta)
            plt.pause(pause_long)

            if self.values[i] < key:
                for j in range(i+1):
                    self.vis[j].set_color(self.vis_red)

                fib = fib_minus_1
                fib_minus_1 = fib_minus_2
                fib_minus_2 = fib - fib_minus_1
                index = i
            elif self.values[i] > key:
                for j in range(i, self.LENGTH):
                    self.vis[j].set_color(self.vis_red)

                fib = fib_minus_2
                fib_minus_1 = fib_minus_1 - fib_minus_2
                fib_minus_2 = fib - fib_minus_1
            else:
                return self.visualize(i)

        if fib_minus_1 and index < (self.LENGTH - 1) and self.values[index + 1] == key:
            return self.visualize(index + 1)

        if i != key:
            i = -1

        return self.visualize(i)
