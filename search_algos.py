import math


# Loops through array once and returns the first item of value key. Complexity: Time - O(n), Space - O(1)
def linear(values, key):
    for i in range(len(values)):
        if values[i] == key:
            return i

    return f"{key} not found"


# Divides values into halves and checks if key is in that half.
# Continues until no longer possible. Requires sorted values. Complexity: Time - O(log(n)), Space - O(1)
def binary(values, key, high=None):
    low = 0
    if not high:
        high = len(values)

    while high >= low:
        mid = (high + low) // 2

        if values[mid] > key:
            high = mid - 1
        elif values[mid] < key:
            low = mid + 1
        else:
            return mid

    return f"{key} not found"


# Optimization for linear search. Similar to binary but steps by a sqrt(n) instead of halving current window.
# Requires sorted values. Complexity: Time - O(sqrt(n)), Space - O(1)
def jump(values, key):
    length = len(values)
    step = int(math.sqrt(length))
    left, right = 0, 0

    while left < length and values[left] <= key:
        right = min(length - 1, left + step)
        if values[left] <= key <= values[right]:
            break
        left += step

    if left >= length or values[left] > key:
        return -1

    right = min(length - 1, right)
    i = left

    while i <= right and values[i] <= key:
        if values[i] == key:
            return i
        i += 1

    return f"{key} not found"


# Optimization for binary search. Faster finding of upper bound.
# Finds upper bound in 2^i operations where i is the desired index. Complexity: Time - O(log(i)), Space - O(1)
# Best when index is relatively close to the beginning of the array, such as with unbounded or infinite arrays
def exponential(values, key):
    if values[0] == key:
        return 0

    i = 1

    while i < len(values) and values[i] <= key:
        i *= 2

    if i < len(values):
        return binary(values, key, i)
    else:
        return binary(values, key)


# Creates fibonacci numbers up to the length of the list, then iterates downward until target value is in range
# Useful for very large numbers as it avoids division. Complexity: Time - O(log(n)), Space - O(1)
def fibonacci(values, key):
    fib_minus_2 = 0
    fib_minus_1 = 1
    fib = fib_minus_1 + fib_minus_2

    while fib < len(values):
        fib_minus_2 = fib_minus_1
        fib_minus_1 = fib
        fib = fib_minus_1 + fib_minus_2

    index = -1

    while fib > 1:
        i = min(index + fib_minus_2, (len(values) - 1))
        if values[i] < key:
            fib = fib_minus_1
            fib_minus_1 = fib_minus_2
            fib_minus_2 = fib - fib_minus_1
            index = i
        elif values[i] > key:
            fib = fib_minus_2
            fib_minus_1 = fib_minus_1 - fib_minus_2
            fib_minus_2 = fib - fib_minus_1
        else:
            return i

    if fib_minus_1 and index < (len(values) - 1) and values[index + 1] == key:
        return index + 1

    return f"{key} not found"
