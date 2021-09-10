"""Functions for generating arrays, random values, and misc operations"""
import numpy as np
from collections import OrderedDict


def generate_array(low, high, size=None):
    """Returns generated numbers to be used for search and sort visualizations"""
    return np.random.randint(low, high, size)


def remove_duplicates(array):
    """Return list of array with no duplicates. Preserves order. Used by radix sort."""
    return list(OrderedDict.fromkeys(array))


def get_factorial(num):
    """Returns factorial of a number. Used by bogosort"""
    return np.math.factorial(num)
