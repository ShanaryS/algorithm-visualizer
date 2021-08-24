import math
import matplotlib.pyplot as plt


# Putting plt.pause() in if statements are what causes the outline color and slows down visualizer. Only part of it
# Put everything in a class so you don't need to repeat driver code
# Clean up code. Use a single length variable instead of constantly using len(v). Make as readable as possible.
# Check on larger list. Make sure all edge cases are dealt with.

values = [4, 89, 1, 9, 69, 49, 149, 84, 15, 15, 79, 41, 9, 62, 19]
values.sort()
names = [str(i) for i in values]


def linear(v, k):
    for i in range(len(v)):
        if v[i] != k:
            test[i].set_color('r')
            plt.pause(0.1)
            if i == len(v)-1:
                return -i
        else:
            return i


# key = 49
# test = plt.bar(names, values)
# res = linear(values, key)
# if res > -1:
#     test[res].set_color('g')
# else:
#     test[res].set_color('r')
# plt.show()


def binary(v, k, high=None):
    if not high:
        high = len(v)
    low = 0
    mid = (high + low) // 2
    upper = high

    while high >= low:
        mid = (high + low) // 2
        test[mid].set_color('y')
        plt.pause(1)

        if v[mid] > k:
            if high < len(v)-2:
                upper = high+1
            else:
                upper = high
            for i in range(mid, upper):
                test[i].set_color('r')
            high = mid - 1
        elif v[mid] < k:
            if low > 1:
                lower = low-1
            else:
                lower = low
            for i in range(lower, mid):
                test[i].set_color('r')
            low = mid + 1
        else:
            for i in range(low-1, mid):
                test[i].set_color('r')
            for i in range(mid+1, upper):
                test[i].set_color('r')
            return mid

    for i in range(len(v)-1):
        test[i].set_color('r')
    return -mid


# key = 48
# test = plt.bar(names, values)
# plt.suptitle('Yellow is pivot - Red is not valid - Green is found value')
# res = binary(values, key)
# if res > -1:
#     test[res].set_color('g')
# else:
#     test[res].set_color('r')
# plt.show()


def jump(v, k):
    length = len(v)
    step = int(math.sqrt(length))
    left, right = 0, 0

    while left < length and v[left] <= k:
        right = min(length - 1, left + step)

        test[left].set_color('y')
        test[right].set_color('y')
        plt.pause(1)

        if v[left] <= k <= v[right]:
            for i in range(right+1, length):
                test[i].set_color('r')
            plt.pause(1)
            break
        left += step

        for i in range(left):
            test[i].set_color('r')

    if left >= length or v[left] > k:
        return -left, right

    right = min(length - 1, right)
    i = left

    while i <= right and v[i] <= k:
        if v[i] == k:
            return i, right
        test[i].set_color('r')
        plt.pause(.4)
        i += 1

    print(i)
    return -i, right


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


def exponential(v, k):  # TODO Does weird stuff when searching for 48 with test. The height arg for binary search prob.
    test[0].set_color('y')
    plt.pause(1)

    if v[0] == k:
        for i in range(1, len(v)):
            test[i].set_color('r')
        return 0

    i = temp_low = temp = 1
    test[0].set_color('r')
    test[i].set_color('y')

    while i < len(v) and v[i] <= k:
        i *= 2
        if i <= len(v):
            for j in range(temp_low, temp+2):
                test[j].set_color('r')
        plt.pause(1)
        temp = i
        temp_low = int(temp / 2)

    if i <= len(v):
        for j in range(i+1, len(v)):
            test[j].set_color('r')

    if i < len(v):
        return binary(v, k, i)
    else:
        return binary(v, k)


# key = 48
# test = plt.bar(names, values)
# plt.suptitle('Yellow is pivot - Red is not valid - Green is found value')
# res = exponential(values, key)
# if res > -1:
#     test[res].set_color('g')
# else:
#     for i in range(-res, len(values)):
#         test[i].set_color('r')
# plt.show()


def fibonacci(v, k):
    fib_minus_2 = 0
    fib_minus_1 = 1
    fib = fib_minus_1 + fib_minus_2
    i = 1

    while fib < len(v):
        fib_minus_2 = fib_minus_1
        fib_minus_1 = fib
        fib = fib_minus_1 + fib_minus_2

    index = -1

    while fib > 1:
        i = min(index + fib_minus_2, (len(v) - 1))

        test[i].set_color('y')
        plt.pause(1)

        if v[i] < k:
            for j in range(i+1):
                test[j].set_color('r')

            fib = fib_minus_1
            fib_minus_1 = fib_minus_2
            fib_minus_2 = fib - fib_minus_1
            index = i
        elif v[i] > k:
            for j in range(i, len(v)):
                test[j].set_color('r')

            fib = fib_minus_2
            fib_minus_1 = fib_minus_1 - fib_minus_2
            fib_minus_2 = fib - fib_minus_1
        else:
            return i

    if fib_minus_1 and index < (len(v) - 1) and v[index + 1] == k:
        return index + 1

    return -i


key = 63
test = plt.bar(names, values)
plt.suptitle('Yellow is pivot - Red is not valid - Green is found value')
res = fibonacci(values, key)
if res > -1:
    test[res].set_color('g')
else:
    test[res].set_color('r')
plt.show()
