import math
import matplotlib.pyplot as plt


# Putting plt.pause() in if statements are what causes the outline color and slows down visualizer. Only part of it
# Check on larger list. Make sure all edge cases are dealt with.
# Return non sorted value for algorithms that require sort
# Seems as though you can only call each search function once. Need to fix for actual deployment
# Create subplots to visualize multiple at once

class SearchVisualizer:
    def __init__(self, values, pause_linear=0.1, pause_leap=1.0):
        self.values = values
        self.names = [str(i) for i in values]
        self.pause_linear = pause_linear
        self.pause_leap = pause_leap
        self.vis = plt.bar(self.names, self.values)
        plt.suptitle('Yellow is pivot - Red is not valid - Green is found value')
        # self._values_sorted = sorted(values)
        # self._names_sorted = [str(i) for i in values]
        # Alternative way to sort values for non linear searches. Currently using values_sort function instead.

    def values_sort(self):
        self.values.sort()
        self.names = [str(i) for i in self.values]
        plt.clf()   # Might be costly. Optimization could be to keep different set of sorted values rather than updating
        self.vis = plt.bar(self.names, self.values)

    def visualize(self, res):
        if isinstance(res, int):
            if res > -1:
                self.vis[res].set_color('g')
            else:
                self.vis[res].set_color('r')
                # for i in range(-res, len(values)):
                #     test[i].set_color('r')
                # This may be necessary for exponential to work properly. Leaving just in case.
        else:
            if res[0] > -1:
                self.vis[res[0]].set_color('g')
                for i in range(res[0]+1, res[1]+1):
                    self.vis[i].set_color('r')
            else:
                for i in range(-res[0], res[1]+1):
                    self.vis[i].set_color('r')
        plt.show()

    def comparison(self, *args):
        pass    # TODO take func name as arg and create subplots comparing multiple

    def linear(self, key):  # Only algorithm that does not require sorted values.
        length = len(self.values)
        for i in range(length):
            if self.values[i] != key:
                self.vis[i].set_color('r')
                plt.pause(self.pause_linear)
                if i == length-1:
                    return self.visualize(-i)
            else:
                return self.visualize(i)

    def binary(self, key, high=None):
        length = len(self.values)
        if not high:
            high = length
        low = 0
        mid = (high + low) // 2
        upper = high

        while high >= low:
            mid = (high + low) // 2
            self.vis[mid].set_color('y')
            plt.pause(self.pause_leap)

            if self.values[mid] > key:
                if high < length-2:
                    upper = high+1
                else:
                    upper = high
                for i in range(mid, upper):
                    self.vis[i].set_color('r')
                high = mid - 1
            elif self.values[mid] < key:
                if low > 1:
                    lower = low-1
                else:
                    lower = low
                for i in range(lower, mid):
                    self.vis[i].set_color('r')
                low = mid + 1
            else:
                for i in range(low-1, mid):
                    self.vis[i].set_color('r')
                for i in range(mid+1, upper):
                    self.vis[i].set_color('r')
                return self.visualize(mid)

        for i in range(length-1):
            self.vis[i].set_color('r')
        return self.visualize(-mid)

    def jump(self, key):
        length = len(self.values)
        step = int(math.sqrt(length))
        left, right = 0, 0

        while left < length and self.values[left] <= key:
            right = min(length - 1, left + step)

            self.vis[left].set_color('y')
            self.vis[right].set_color('y')
            plt.pause(self.pause_leap)

            if self.values[left] <= key <= self.values[right]:
                for i in range(right+1, length):
                    self.vis[i].set_color('r')
                plt.pause(self.pause_leap)
                break
            left += step

            for i in range(left):
                self.vis[i].set_color('r')

        if left >= length or self.values[left] > key:
            return self.visualize((left, right))

        right = min(length - 1, right)
        i = left

        while i <= right and self.values[i] <= key:
            if self.values[i] == key:
                return self.visualize((i, right))
            self.vis[i].set_color('r')
            plt.pause(self.pause_linear)
            i += 1

        return self.visualize((-i, right))

    # TODO Does weird stuff when searching for 48 with values. The height arg for binary search probably is the cause.
    def exponential(self, k):
        length = len(self.values)
        self.vis[0].set_color('y')
        plt.pause(self.pause_leap)

        if self.values[0] == k:
            for i in range(1, length):
                self.vis[i].set_color('r')
            return 0

        i = temp_low = temp = 1
        self.vis[0].set_color('r')
        self.vis[i].set_color('y')

        while i < length and self.values[i] <= k:
            i *= 2
            if i <= length:
                for j in range(temp_low, temp+2):
                    self.vis[j].set_color('r')
            plt.pause(self.pause_leap)
            temp = i
            temp_low = int(temp / 2)

        if i <= length:
            for j in range(i+1, length):
                self.vis[j].set_color('r')

        if i < length:
            return self.binary(k, i)
        else:
            return self.binary(k)

    def fibonacci(self, key):
        length = len(self.values)
        fib_minus_2 = 0
        fib_minus_1 = 1
        fib = fib_minus_1 + fib_minus_2
        i = 1

        while fib < length:
            fib_minus_2 = fib_minus_1
            fib_minus_1 = fib
            fib = fib_minus_1 + fib_minus_2

        index = -1

        while fib > 1:
            i = min(index + fib_minus_2, (length - 1))

            self.vis[i].set_color('y')
            plt.pause(self.pause_leap)

            if self.values[i] < key:
                for j in range(i+1):
                    self.vis[j].set_color('r')

                fib = fib_minus_1
                fib_minus_1 = fib_minus_2
                fib_minus_2 = fib - fib_minus_1
                index = i
            elif self.values[i] > key:
                for j in range(i, length):
                    self.vis[j].set_color('r')

                fib = fib_minus_2
                fib_minus_1 = fib_minus_1 - fib_minus_2
                fib_minus_2 = fib - fib_minus_1
            else:
                return self.visualize(i)

        if fib_minus_1 and index < (length - 1) and self.values[index + 1] == key:
            return self.visualize(index + 1)

        return self.visualize(-i)


if __name__ == '__main__':
    import random

    test = [4, 89, 1, 9, 69, 49, 149, 84, 15, 15, 79, 41, 9, 62, 19]    # Original test array. Use as base. 48/49
    test2 = random.sample(range(100), 100)

    x = SearchVisualizer(test2, 0.01, 0.1)
    x.linear(148)
    # x.values_sort()
    # x.binary(49)
    # x.jump(50)
    # x.exponential(48)
    # x.fibonacci(49)
