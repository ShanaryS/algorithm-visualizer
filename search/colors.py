"""Colors needed for visualizations"""

from enum import Enum, unique


@unique
class MatplotlibColors(Enum):
    """Colors for matplotlib"""

    BLUE: str = 'blue'
    GOLD: str = 'gold'
    MAGENTA: str = 'magenta'
    CYAN: str = 'cyan'
    GREEN: str = 'green'
    RED: str = 'red'
    BLACK: str = 'black'
    YELLOW: str = 'yellow'


MPL_DEFAULT = MatplotlibColors.BLUE
MPL_GOLD = MatplotlibColors.GOLD          # Checking
MPL_MAGENTA = MatplotlibColors.MAGENTA    # Pivot
MPL_CYAN = MatplotlibColors.CYAN          # Special value unique to that algorithm
MPL_GREEN = MatplotlibColors.GREEN        # Result
MPL_RED = MatplotlibColors.RED            # Checked but false
MPL_BLACK = MatplotlibColors.BLACK        # Misc
MPL_YELLOW = MatplotlibColors.YELLOW      # Used for buttons
