"""Class used to time different sections of code for debugging
Usually would would import the class Timer and instance it per it's usage.
If you want to share the same timer across your program, 
import the variable timer instead.
"""


from time import perf_counter_ns as _get_time_ns
from typing import Callable


class Timer:
    """Timer for a code section.
    
    Usage:
    1. Instance Timer and call wrap a section of code between 
        start() and end() methods
    2. Use print() method to print the result
    3. print() should only be called once, start() and end()
        can be called as many times as needed. For example a section of a loop.
    4. print() takes an optional string arg to name the section code in print
    5. Min Time result ignores zero time values as they are usually trivial
    """
    
    def __init__(self, name="Code Section") -> None:
        self.timer_name = name
        self.timer_start = None
        self.timer_count = 0
        self.timer_min = float('inf')
        self.timer_max = float('-inf')
        self.timer_total_time = 0
    
    def _reset(self) -> None:
        """Resets the timer. Calls __init__ per DRY principle."""
        self.__init__(self.timer_name)

    def start(self) -> None:
        """Start timer for a section of code"""
        self.timer_start = _get_time_ns()

    def end(self) -> None:
        """End timer for a section of code"""
        end = _get_time_ns()

        self.timer_count += 1
        total = end - self.timer_start
        self.timer_min = min(self.timer_min, total) if total > 0 else self.timer_min
        self.timer_max = max(self.timer_max, total)
        self.timer_total_time += total
    
    def loop(self, num_loops: int, func: Callable[..., None], args: list = None):
        """Loops a function a number of times"""
        for _ in range(num_loops):
            self.start()
            func(*args)
            self.end()

    def print(self) -> None:
        """Prints info about the timer"""
        
        # Display total time with correct units
        if self.timer_total_time >= (10**9 * 60):
            final_total = self.timer_total_time / (10**9 * 60)
            final_total_time_unit = "min"
        elif self.timer_total_time >= 10**9:
            final_total = self.timer_total_time / 10**9
            final_total_time_unit = "s"
        elif self.timer_total_time >= 10**6:
            final_total = self.timer_total_time / 10**6
            final_total_time_unit = "ms"
        elif self.timer_total_time >= 10**3:
            final_total = self.timer_total_time / 10**3
            final_total_time_unit = "us"
        else:
            final_total = self.timer_total_time
            final_total_time_unit = "ns"
        
        # Display average time with correct units
        # Divide by zero fix
        self.timer_count = self.timer_count if self.timer_count != 0 else 1
        average_time = self.timer_total_time / self.timer_count
        if average_time >= (10**9 * 60):
            final_average = average_time / (10**9 * 60)
            final_average_time_unit = "min"
        elif average_time >= 10**9:
            final_average = average_time / 10**9
            final_average_time_unit = "s"
        elif average_time >= 10**6:
            final_average = average_time / 10**6
            final_average_time_unit = "ms"
        elif average_time >= 10**3:
            final_average = average_time / 10**3
            final_average_time_unit = "us"
        else:
            final_average = average_time
            final_average_time_unit = "ns"
        
        # Display min time with correct units
        if self.timer_min >= (10**9 * 60):
            final_min = self.timer_min / (10**9 * 60)
            final_min_time_unit = "min"
        elif self.timer_min >= 10**9:
            final_min = self.timer_min / 10**9
            final_min_time_unit = "s"
        elif self.timer_min >= 10**6:
            final_min = self.timer_min / 10**6
            final_min_time_unit = "ms"
        elif self.timer_min >= 10**3:
            final_min = self.timer_min / 10**3
            final_min_time_unit = "us"
        else:
            final_min = self.timer_min
            final_min_time_unit = "ns"
        if final_min == float('inf'):
            final_min = 0
            final_min_time_unit = 'ns'
        
        # Display max time with correct units
        if self.timer_max >= (10**9 * 60):
            final_max = self.timer_max / (10**9 * 60)
            final_max_time_unit = "min"
        elif self.timer_max >= 10**9:
            final_max = self.timer_max / 10**9
            final_max_time_unit = "s"
        elif self.timer_max >= 10**6:
            final_max = self.timer_max / 10**6
            final_max_time_unit = "ms"
        elif self.timer_max >= 10**3:
            final_max = self.timer_max / 10**3
            final_max_time_unit = "us"
        else:
            final_max = self.timer_max
            final_max_time_unit = "ns"
        if final_max == float('-inf'):
            final_max = 0
            final_max_time_unit = 'ns'
        
        # Print results
        print("-------------------------------------")
        print(f"--- {self.timer_name} ---")
        print(f"Total Time: {final_total:.2f}{final_total_time_unit}")
        print(f"Avg Time: {final_average:.2f}{final_average_time_unit}")
        print(f"Max Time: {final_max:.2f}{final_max_time_unit}")
        print(f"Min Time: {final_min:.2f}{final_min_time_unit}")
        print(f"Count: {self.timer_count:,}")
        
        # Reset timer after printing
        self._reset()


# Import this var instead of class to share timer across modules
timer = Timer()


# Highest accuracy sleep
def sleep(delay: int, unit: str ="s") -> None:
        """Sleeps for specified unit of time."""
        if unit == "ns":
            ns = delay
        elif unit == "us":
            ns = delay * 10**3
        elif unit == "ms":
            ns = delay * 10**6
        elif unit == "s":
            ns = delay * 10**9
        elif unit == "min":
            ns = delay * (10**9 * 60)
        elif unit == "h":
            ns = delay * (10**9 * 60 * 60)
        else:
            raise NotImplementedError("Invalid time unit for sleep.")
        
        end = _get_time_ns() + ns
        while _get_time_ns() < end:
            pass