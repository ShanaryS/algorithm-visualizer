"""Functions and constants needed by multiple modules"""


import random


# Default counts for pathfinding graph. Defining here so that both logic.py and node.py has access.
# Recursive division only works on certain row values. 22,23,46,47,94,95,...
ROWS: int = 46
WIDTH_HEIGHT: int = 800
OFFSET: int = 1


def calc_square_size(width, rows) -> float:
    """Calculates square size"""
    
    # Only use offset if size of square is larger than a pixel
    if WIDTH_HEIGHT / width > 1:
        final_width = width - OFFSET
    else:
        final_width = width
    
    return final_width / rows


SQUARE_SIZE: float = calc_square_size(WIDTH_HEIGHT, ROWS)


def get_random_sample(population: tuple, k: int) -> list:
    """Returns a k length list of unique elements from population"""
    return random.sample(population, k)


def get_randrange(start: int, stop: int) -> int:
    """Return a random int within a range"""
    return random.randrange(start, stop)
