import random


# Default counts for pathfinding graph. Defining here so that both logic.py and node.py has access.
# Recursive division only works on certain row values. 22,23,46,47,94,95.
ROWS = 46
WIDTH_HEIGHT = 800
SQUARE_SIZE = WIDTH_HEIGHT / ROWS


def get_random_sample(population, k):
    """Returns a k length list of unique elements from population"""
    return random.sample(population, k)


def get_randrange(start, stop):
    """Return a random int within a range"""
    return random.randrange(start, stop)
