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
    RED = 'red'
    BLACK = 'black'
    YELLOW = 'yellow'


class MatplotlibColors(Enum):
    """Matplotlib colors"""

    MPL_DEFAULT = Colors.BLUE
    MPL_GOLD = Colors.GOLD          # Checking
    MPL_MAGENTA = Colors.MAGENTA    # Pivot
    MPL_CYAN = Colors.CYAN          # Special value unique to that algorithm
    MPL_GREEN = Colors.GREEN        # Result
    MPL_RED = Colors.RED            # Checked but false
    MPL_BLACK = Colors.BLACK        # Misc
    MPL_YELLOW = Colors.YELLOW      # Used for buttons
