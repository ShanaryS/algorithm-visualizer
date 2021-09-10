"""Functions for generating arrays, random values, and misc operations"""
import numpy as np


def generate_array(low, high, size=None):
    """Returns generated numbers to be used for search and sort visualizations"""
    return np.random.randint(low, high, size)


def get_sqrt(num):
    """Returns the sqrt (float) of a number. Used by jump search."""
    return np.sqrt(num)
