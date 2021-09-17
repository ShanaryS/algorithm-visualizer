"""Functions and constants needed by multiple modules"""


import numpy as np


# Value to search for. Defaults to 44.
KEY: int = 44


def generate_array(low: int, high: int, size: int = None) -> np.ndarray:
    """Returns generated numbers to be used for search and sort visualizations"""
    return np.random.randint(low, high, size)


def get_sqrt(num: int) -> int:
    """Returns the sqrt (float) of a number. Used by jump search."""
    return int(np.sqrt(num))
