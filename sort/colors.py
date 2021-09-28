"""Colors needed for visualizations"""

from enum import Enum, unique


@unique
class Colors(Enum):
    """Name for certain colors"""

    BLUE = 'blue'
    GOLD = 'gold'
    MAGENTA = 'magenta'
    CYAN = 'cyan'
    GREEN = 'green'
    BLACK = 'black'
    RED = 'red'
    ORANGE = 'orange'
    YELLOW = 'yellow'
    TOMATO = 'tomato'


class MatplotlibColors(Enum):
    """Colors for matplotlib"""

    MPL_DEFAULT = Colors.BLUE
    MPL_GOLD = Colors.GOLD          # Checking
    MPL_MAGENTA = Colors.MAGENTA    # Pivot
    MPL_CYAN = Colors.CYAN          # Special value unique to that algorithm
    MPL_GREEN = Colors.GREEN        # Result
    MPL_BLACK = Colors.BLACK        # To swap
    MPL_RED = Colors.RED            # Moving
    MPL_ORANGE = Colors.ORANGE      # Used for buttons
    MPL_YELLOW = Colors.YELLOW      # Used for buttons
    MPL_TOMATO = Colors.TOMATO      # Used for buttons
