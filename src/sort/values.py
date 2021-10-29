"""Functions needed by multiple modules"""


import numpy as np
from collections import OrderedDict


def generate_array(low: int, high: int, size: int = None) -> np.ndarray:
    """Returns generated numbers to be used for search and sort visualizations"""
    return np.random.randint(low, high, size)


def remove_duplicates(array: list) -> list:
    """Return list of array with no duplicates. Preserves order. Used by radix sort."""
    return list(OrderedDict.fromkeys(array))


def get_factorial(num: int) -> int:
    """Returns factorial of a number. Used by bogosort"""
    return np.math.factorial(num)
