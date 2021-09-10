"""Functions for generating arrays, random values, and calc operations"""

import numpy as np
from collections import OrderedDict
import random

# Default counts for pathfinding grpah. Defining here so that both graph_pathfinding.py and node.py has access.
# Recursive division only works on certain row values. 22,23,46,47,94,95.
ROWS = 46
WIDTH_HEIGHT = 800
SQUARE_SIZE = WIDTH_HEIGHT / ROWS


def generate_array(low, high, size=None):
    """Returns generated numbers to be used for search and sort visualizations"""
    return np.random.randint(low, high, size)


def remove_duplicates(array):
    """Return list of array with no duplicates. Preserves order. Used by radix sort."""
    return list(OrderedDict.fromkeys(array))


def get_sqrt(num):
    """Returns the sqrt (float) of a number. Used by jump search."""
    return np.sqrt(num)


def get_factorial(num):
    """Returns factorial of a number. Used by bogosort"""
    return np.math.factorial(num)


def get_random_sample(population, k):
    """Returns a k length list of unique elements from population"""
    return random.sample(population, k)


def get_randrange(start, stop):
    """Return a random int within a range"""
    return random.randrange(start, stop)
