"""Functions and constants needed by multiple modules"""


import numpy as np


KEY = 44  # Value to search for. Defaults to 44.
HESITATE = 0.5  # Delay between starting new algo after sorting


def generate_array(low: int, high: int, size: int = None) -> np.ndarray:
    """Returns generated numbers to be used for search and sort visualizations"""
    return np.random.randint(low, high, size)


def get_sqrt(num: int) -> int:
    """Returns the sqrt (float) of a number. Used by jump search."""
    return int(np.sqrt(num))
