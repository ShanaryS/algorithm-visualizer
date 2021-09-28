"""Colors needed for visualizations"""

from enum import Enum, unique


@unique
class MatplotlibColors(Enum):
    """Colors for matplotlib"""

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


MPL_DEFAULT = MatplotlibColors.BLUE
MPL_GOLD = MatplotlibColors.GOLD          # Checking
MPL_MAGENTA = MatplotlibColors.MAGENTA    # Pivot
MPL_CYAN = MatplotlibColors.CYAN          # Special value unique to that algorithm
MPL_GREEN = MatplotlibColors.GREEN        # Result
MPL_BLACK = MatplotlibColors.BLACK        # To swap
MPL_RED = MatplotlibColors.RED            # Moving
MPL_ORANGE = MatplotlibColors.ORANGE      # Used for buttons
MPL_YELLOW = MatplotlibColors.YELLOW      # Used for buttons
MPL_TOMATO = MatplotlibColors.TOMATO      # Used for buttons
