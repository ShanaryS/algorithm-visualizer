"""Functions and constants needed by multiple modules"""


import random


# Default counts for pathfinding graph. Defining here so that both logic.py and node.py has access.
# Recursive division only works on certain row values. 22,23,46,47,94,95,...
ROWS: int = 46
WIDTH_HEIGHT: int = 800
SQUARE_SIZE: float = WIDTH_HEIGHT / ROWS


def get_random_sample(population: tuple, k: int) -> list:
    """Returns a k length list of unique elements from population"""
    return random.sample(population, k)


def get_randrange(start: int, stop: int) -> int:
    """Return a random int within a range"""
    return random.randrange(start, stop)
