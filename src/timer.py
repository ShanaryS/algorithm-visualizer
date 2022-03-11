"""Fuctions used to time different sections of code for debugging
Usage:
1. Place timer_start() and timer_end() around section of code to time
2. Place timer_print() to print the result
3. timer_print() should only be called once, timer_start() and timer_end()
    can be called as many times as needed. For example a section of a loop.
"""


import time


g_timer_start = 0
g_timer_count = 0
g_timer_min = float('inf')
g_timer_max = float('-inf')
g_timer_total_time = 0


def timer_start() -> None:
    """Start timer for a section of code"""
    global g_timer_start
    g_timer_start = time.time_ns()


def timer_end() -> None:
    """End timer for a section of code"""
    end = time.time_ns()
    
    global g_timer_start, g_timer_count, g_timer_min
    global g_timer_max, g_timer_total_time
    g_timer_count += 1
    total = end - g_timer_start
    g_timer_min = min(g_timer_min, total)
    g_timer_max = max(g_timer_max, total)
    g_timer_total_time += total


def timer_print() -> None:
    """Prints info about the timer"""
    global g_timer_start, g_timer_count, g_timer_min
    global g_timer_max, g_timer_total_time
    
    # Display total time with correct units
    if g_timer_total_time > (10**9 * 60):
        final_total = g_timer_total_time / (10**9 * 60)
        time_unit = "min"
    elif g_timer_total_time > 10**9:
        final_total = g_timer_total_time / 10**9
        time_unit = "s"
    elif g_timer_total_time > 10**6:
        final_total = g_timer_total_time / 10**6
        time_unit = "ms"
    elif g_timer_total_time > 10**3:
        final_total = g_timer_total_time / 10**3
        time_unit = "us"
    else:
        final_total = g_timer_total_time
        time_unit = "ns"
    
    # Display min time with correct units
    if g_timer_min > (10**9 * 60):
        final_min = g_timer_min / (10**9 * 60)
        time_unit = "min"
    elif g_timer_min > 10**9:
        final_min = g_timer_min / 10**9
        time_unit = "s"
    elif g_timer_min > 10**6:
        final_min = g_timer_min / 10**6
        time_unit = "ms"
    elif g_timer_min > 10**3:
        final_min = g_timer_min / 10**3
        time_unit = "us"
    else:
        final_min = g_timer_min
        time_unit = "ns"
    
    # Display max time with correct units
    if g_timer_max > (10**9 * 60):
        final_max = g_timer_max / (10**9 * 60)
        time_unit = "min"
    elif g_timer_max > 10**9:
        final_max = g_timer_max / 10**9
        time_unit = "s"
    elif g_timer_max > 10**6:
        final_max = g_timer_max / 10**6
        time_unit = "ms"
    elif g_timer_max > 10**3:
        final_max = g_timer_max / 10**3
        time_unit = "us"
    else:
        final_max = g_timer_max
        time_unit = "ns"
    
    print("-------------------------------------")
    print(f"Total Time: {final_total:.2f}{time_unit}")
    print(f"Min Time: {final_min:.2f}{time_unit}")
    print(f"Max Time: {final_max:.2f}{time_unit}")
    print(f"Count: {g_timer_count:,}")
    print("-------------------------------------")
    
    g_timer_start = 0
    g_timer_count = 0
    g_timer_min = 0
    g_timer_max = 0
    g_timer_total_time = 0
