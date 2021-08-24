import math
import matplotlib.pyplot as plt


# Putting plt.pause() in if statements are what causes the outline color and slows down visualizer. Only part of it
# Clean up code. Use a single length variable instead of constantly using len(v). Make as readable as possible.
# Check on larger list. Make sure all edge cases are dealt with.
# Return non sorted value for algos that require sort

class SearchVisualizer:
    def __init__(self, values):
        self.values = values
        self.names = [str(i) for i in values]
        self.vis = plt.bar(self.names, self.values)
        plt.suptitle('Yellow is pivot - Red is not valid - Green is found value')
        self.pause_linear = 0.1
        # self._values_sorted = sorted(values)
        # self._names_sorted = [str(i) for i in values]
        # Alternative way to sort values for non linear searches. Currently using values_sort function instead.

    def values_sort(self):
        self.values.sort()
        self.names = [str(i) for i in self.values]
        plt.clf()   # Might be costly. Optimization could be to keep different set of sorted values rather than updating
        self.vis = plt.bar(self.names, self.values)

    # TODO Handle all edge cases for each algorithm
    def visualize(self, res):   # Going to use this for polymorphism. All searches should currently output from this.
        if isinstance(res, int):
            if res > -1:
                self.vis[res].set_color('g')
            else:
                self.vis[res].set_color('r')
        else:
            if res[0] > -1:
                self.vis[res[0]].set_color('g')
                for i in range(res[0]+1, res[1]+1):
                    self.vis[i].set_color('r')
            else:
                for i in range(-res[0], res[1]+1):
                    self.vis[i].set_color('r')
        plt.show()

    def linear(self, key):  # Only algorithm that does not require sorted values.
        for i in range(len(self.values)):
            if self.values[i] != key:
                self.vis[i].set_color('r')
                plt.pause(self.pause_linear)
                if i == len(self.values)-1:
                    return self.visualize(-i)
            else:
                return self.visualize(i)

    def binary(self, key, high=None):
        if not high:
            high = len(self.values)
        low = 0
        mid = (high + low) // 2
        upper = high

        while high >= low:
            mid = (high + low) // 2
            self.vis[mid].set_color('y')
            plt.pause(1)

            if self.values[mid] > key:
                if high < len(self.values)-2:
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

        for i in range(len(self.values) - 1):
            self.vis[i].set_color('r')
        return self.visualize(-mid)

    # key = 48
    # test = plt.bar(names, values)
    # plt.suptitle('Yellow is pivot - Red is not valid - Green is found value')
    # res = binary(values, key)
    # if res > -1:
    #     test[res].set_color('g')
    # else:
    #     test[res].set_color('r')
    # plt.show()

    def jump(self, key):
        length = len(self.values)
        step = int(math.sqrt(length))
        left, right = 0, 0

        while left < length and self.values[left] <= key:
            right = min(length - 1, left + step)

            self.vis[left].set_color('y')
            self.vis[right].set_color('y')
            plt.pause(1)

            if self.values[left] <= key <= self.values[right]:
                for i in range(right+1, length):
                    self.vis[i].set_color('r')
                plt.pause(1)
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
            plt.pause(.4)
            i += 1

        return self.visualize((-i, right))

    # key = 48
    # test = plt.bar(names, values)
    # res = jump(values, key)
    # if res[0] > -1:
    #     test[res[0]].set_color('g')
    #     for i in range(res[0]+1, res[1]+1):
    #         test[i].set_color('r')
    # else:
    #     for i in range(-res[0], res[1]+1):
    #         test[i].set_color('r')
    # plt.show()

    # TODO Does weird stuff when searching for 48 with values. The height arg for binary search probably is the cause.
    def exponential(self, k):
        self.vis[0].set_color('y')
        plt.pause(1)

        if self.values[0] == k:
            for i in range(1, len(self.values)):
                self.vis[i].set_color('r')
            return 0

        i = temp_low = temp = 1
        self.vis[0].set_color('r')
        self.vis[i].set_color('y')

        while i < len(self.values) and self.values[i] <= k:
            i *= 2
            if i <= len(self.values):
                for j in range(temp_low, temp+2):
                    self.vis[j].set_color('r')
            plt.pause(1)
            temp = i
            temp_low = int(temp / 2)

        if i <= len(self.values):
            for j in range(i+1, len(self.values)):
                self.vis[j].set_color('r')

        if i < len(self.values):
            return self.binary(k, i)
        else:
            return self.binary(k)

    # key = 49
    # test = plt.bar(names, values)
    # plt.suptitle('Yellow is pivot - Red is not valid - Green is found value')
    # res = exponential(values, key)
    # if res > -1:
    #     test[res].set_color('g')
    # else:
    #     for i in range(-res, len(values)):
    #         test[i].set_color('r')
    # plt.show()

    def fibonacci(self, key):
        fib_minus_2 = 0
        fib_minus_1 = 1
        fib = fib_minus_1 + fib_minus_2
        i = 1

        while fib < len(self.values):
            fib_minus_2 = fib_minus_1
            fib_minus_1 = fib
            fib = fib_minus_1 + fib_minus_2

        index = -1

        while fib > 1:
            i = min(index + fib_minus_2, (len(self.values) - 1))

            self.vis[i].set_color('y')
            plt.pause(1)

            if self.values[i] < key:
                for j in range(i+1):
                    self.vis[j].set_color('r')

                fib = fib_minus_1
                fib_minus_1 = fib_minus_2
                fib_minus_2 = fib - fib_minus_1
                index = i
            elif self.values[i] > key:
                for j in range(i, len(self.values)):
                    self.vis[j].set_color('r')

                fib = fib_minus_2
                fib_minus_1 = fib_minus_1 - fib_minus_2
                fib_minus_2 = fib - fib_minus_1
            else:
                return self.visualize(i)

        if fib_minus_1 and index < (len(self.values) - 1) and self.values[index + 1] == key:
            return self.visualize(index + 1)

        return self.visualize(-i)

    # key = 49
    # test = plt.bar(names, values)
    # plt.suptitle('Yellow is pivot - Red is not valid - Green is found value')
    # res = fibonacci(values, key)
    # if res > -1:
    #     test[res].set_color('g')
    # else:
    #     test[res].set_color('r')
    # plt.show()


if __name__ == '__main__':
    numbers = [4, 89, 1, 9, 69, 49, 149, 84, 15, 15, 79, 41, 9, 62, 19]

    x = SearchVisualizer(numbers)
    # x.linear(148)
    # x.values_sort()
    # x.binary(49)
    # x.jump(50)
    # x.exponential(48)
    # x.fibonacci(49)
