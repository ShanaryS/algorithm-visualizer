# Goes through list left to right comparing values of the current number to all values after, swapping as need
# Complexity: Time - O(n^2), Space - O(1), Unstable
def selection(values):
    for i in range(len(values)-1):
        index = i
        for j in range(i+1, len(values)):
            if values[j] < values[index]:
                index = j

        temp = values[i]
        values[i] = values[index]
        values[index] = temp


# Splits input into the sorted and unsorted parts from left to right. Places unsorted elements to the correct position.
# Complexity: Time - O(n^2), Space - O(1), Stable
def insertion(values):
    for i in range(1, len(values)):
        a = i

        while a > 0 and values[a] < values[a - 1]:
            values[a], values[a-1] = values[a-1], values[a]
            a -= 1


# Recursively splits input in halves. Sorts each element at each level bottom up.
# Complexity: Time - O(nlog(n)), Space - O(n), Stable
def merge(values, i=0, k=-1):
    if k == -1:
        k = len(values)-1

    if i < k:
        j = (i + k) // 2

        merge(values, i, j)
        merge(values, j + 1, k)

        _merge(values, i, j, k)


def _merge(numbers, i, j, k):
    merged_size = k - i + 1
    merged_numbers = [0] * merged_size
    merge_pos = 0
    left_pos = i
    right_pos = j + 1

    while left_pos <= j and right_pos <= k:
        if numbers[left_pos] <= numbers[right_pos]:
            merged_numbers[merge_pos] = numbers[left_pos]
            left_pos += 1
        else:
            merged_numbers[merge_pos] = numbers[right_pos]
            right_pos += 1
        merge_pos += 1

    while left_pos <= j:
        merged_numbers[merge_pos] = numbers[left_pos]
        left_pos += 1
        merge_pos += 1

    while right_pos <= k:
        merged_numbers[merge_pos] = numbers[right_pos]
        right_pos += 1
        merge_pos += 1

    for merge_pos in range(merged_size):
        numbers[i + merge_pos] = merged_numbers[merge_pos]


# Only for integers. Places values into buckets from the least to most significant digit. Sorts with buckets
# Complexity: Time - O(n*k), Space - O(n+k), Stable
def radix(numbers):
    buckets = []
    for i in range(10):
        buckets.append([])

    max_digits = _radix_max(numbers)
    pow_10 = 1

    for digit_index in range(max_digits):
        for num in numbers:
            bucket_index = (abs(num) // pow_10) % 10
            buckets[bucket_index].append(num)

        numbers.clear()
        for bucket in buckets:
            numbers.extend(bucket)
            bucket.clear()

        pow_10 = pow_10 * 10

    negatives = []
    non_negatives = []
    for num in numbers:
        if num < 0:
            negatives.append(num)
        else:
            non_negatives.append(num)
    negatives.reverse()
    numbers.clear()
    numbers.extend(negatives + non_negatives)


def _radix_max(numbers):
    max_digits = 0
    for num in numbers:
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


# Counts the number of objects with unique key values. Uses arithmetic to calculate the position of each object.
# Complexity: Time - O(n+k), Space - O(n+k), Stable
def counting(values):
    max_element = int(max(values))
    min_element = int(min(values))
    range_of_elements = max_element - min_element + 1

    count = [0 for _ in range(range_of_elements)]
    res = [0 for _ in range(len(values))]

    for i in range(0, len(values)):
        count[values[i] - min_element] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for i in range(len(values) - 1, -1, -1):
        res[count[values[i] - min_element] - 1] = values[i]
        count[values[i] - min_element] -= 1

    for i in range(0, len(values)):
        values[i] = res[i]

    # return values


# Sets a pivot value and places every value below the pivot before the pivot and all values greater than pivot after.
# Repeats recursively until only single element partitions remains.
# Complexity: Time - O(nlog(n)), Space - O(log(n)), Unstable
def quicksort(values, start=0, end=-1):
    if end == -1:
        end = len(values)-1

    if end <= start:
        return

    high = _quicksort(values, start, end)

    quicksort(values, start, high)

    quicksort(values, high + 1, end)


def _quicksort(values, start, end):
    mid = start + (end - start) // 2
    pivot = values[mid]

    low = start
    high = end

    done = False
    while not done:
        while values[low] < pivot:
            low += 1

        while pivot < values[high]:
            high -= 1

        if low >= high:
            done = True
        else:
            temp = values[low]
            values[low] = values[high]
            values[high] = temp
            low += 1
            high -= 1

    return high


# Swaps adjacent elements if they are in the wrong order. Repeats n-1 times with max index to check decreasing by 1.
# Complexity: Time - O(n^2), Space - O(1), Stable
def bubble(values):
    length = len(values)

    for i in range(length - 1):
        for j in range(0, length - i - 1):
            if values[j] > values[j + 1]:
                values[j], values[j + 1] = values[j + 1], values[j]


# Converts input into a min heap data structure and pops values.
# Complexity: Time - O(nlog(n)), Space - O(1), Unstable
def heap(values):
    length = len(values)

    for i in range(length // 2 - 1, -1, -1):
        _heap(values, length, i)

    for i in range(length - 1, 0, -1):
        values[i], values[0] = values[0], values[i]
        _heap(values, i, 0)


def _heap(values, length, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < length and values[i] < values[left]:
        largest = left

    if right < length and values[largest] < values[right]:
        largest = right

    if largest != i:
        values[i], values[largest] = values[largest], values[i]

        _heap(values, length, largest)


# Combination of merge sort and insertion sort. Divides input into blocks, sorts using insertion, combines using merge.
# Complexity: Time - O(nlog(n)), Space - O(1), Stable
def timsort(values):
    length = len(values)
    min_run = _min_run(length)

    for start in range(0, length, min_run):
        insertion(values)

    size = min_run
    while size < length:

        for left in range(0, length, 2 * size):

            mid = min(length - 1, left + size - 1)
            right = min((left + 2 * size - 1), (length - 1))

            if mid < right:
                _merge(values, left, mid, right)

        size = 2 * size


def _min_run(n):
    MIN_MERGE = 32

    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r
