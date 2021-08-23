import random
import search_algos
import sort_algos
import pathfinder_algos
import time

if __name__ == '__main__':
    test = [4, 89, 1, 9, 6489, 49, 149, 84, 15, 15, 949, 41, 9, 489, 19]
    test2 = random.sample(range(2**12), 2**11)
    test3 = ['e', 'fajfu', 'ew', 'ao', 'pmn', 'o', 'ig', 'uowajfoep', 'wa', 'hf', 'po', 'ie', ['a', 'b']]

    values = test
    key = 4
    # print(len(test2))

    # start = time.time_ns()
    # end = time.time_ns()
    # print((end-start) / 1000)

    # print("Linear Search: Index =", search_algos.linear(values, key), "\n")
    #
    # values.sort()    # Replace with own sort function
    # print("Jump Search: Index =", search_algos.jump(values, key), "\nInvalid if values not sorted\n")
    # print("Binary Search: Index =", search_algos.binary(values, key), "\nInvalid if values not sorted\n")
    # print("Exponential Search: Index =", search_algos.exponential(values, key), "\nInvalid if values not sorted\n")
    # print("Fibonacci Search: Index =", search_algos.fibonacci(values, key), "\nInvalid if values not sorted")
    #
    # print(test)

    # print(f"Unsorted: {values}\n")
    a, b, c, d, e = values.copy(), values.copy(), values.copy(), values.copy(), values.copy()
    f, g, h, i, j = values.copy(), values.copy(), values.copy(), values.copy(), values.copy()

    start = time.time_ns()
    sort_algos.selection(a)
    end = time.time_ns()
    # print(f"Selection Sort: {a}")
    print(f"Selection Sort: {(end - start) / 1000}")

    start = time.time_ns()
    sort_algos.insertion(b)
    end = time.time_ns()
    # print(f"Insertion sort: {b}")
    print(f"Insertion sort: {(end - start) / 1000}")

    start = time.time_ns()
    sort_algos.merge(c)
    end = time.time_ns()
    # print(f"Merge sort: {c}")
    print(f"Merge sort: {(end - start) / 1000}")

    start = time.time_ns()
    sort_algos.radix(d)
    end = time.time_ns()
    # print(f"Radix sort: {d}")
    print(f"Radix sort: {(end - start) / 1000}")

    start = time.time_ns()
    sort_algos.counting(e)
    end = time.time_ns()
    # print(f"Counting sort: {e}")
    print(f"Counting sort: {(end - start) / 1000}")

    start = time.time_ns()
    sort_algos.quicksort(f)
    end = time.time_ns()
    # print(f"Quicksort: {f}")
    print(f"Quicksort: {(end - start) / 1000}")

    start = time.time_ns()
    sort_algos.bubble(g)
    end = time.time_ns()
    # print(f"Bubble sort: {g}")
    print(f"Bubble sort: {(end - start) / 1000}")

    start = time.time_ns()
    sort_algos.heapsort(h)
    end = time.time_ns()
    # print(f"Heap sort: {h}")
    print(f"Heap sort: {(end - start) / 1000000}")

    start = time.time_ns()
    sort_algos.timsort(i)
    end = time.time_ns()
    # print(f"Timsort: {i}")
    print(f"Timsort: {(end - start) / 1000}")

    start = time.time_ns()
    j.sort()
    end - time.time_ns()
    print(f"Python sort: {(end - start) / 1000}")
