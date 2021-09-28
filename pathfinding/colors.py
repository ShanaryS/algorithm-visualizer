"""Colors needed for visualization"""

from enum import Enum, unique


@unique
class Colors(Enum):
    """RGB values of colors"""

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (128, 128, 128)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    TURQUOISE = (64, 224, 208)
    TURQUOISE_ALT = (64, 223, 208)
    TURQUOISE_ALT_ = (64, 225, 208)


class PygameColors(Enum):
    """Pygame colors"""

    DEFAULT_COLOR = Colors.WHITE
    LEGEND_AREA_COLOR = Colors.GREY
    LINE_COLOR = Colors.GREY
    OPEN_COLOR = Colors.TURQUOISE
    OPEN_ALT_COLOR = Colors.TURQUOISE_ALT
    OPEN_ALT_COLOR_ = Colors.TURQUOISE_ALT_
    CLOSED_COLOR = Colors.BLUE
    START_COLOR = Colors.GREEN
    MID_COLOR = Colors.ORANGE
    END_COLOR = Colors.RED
    WALL_COLOR = Colors.BLACK
    PATH_COLOR = Colors.YELLOW
    LEGEND_COLOR = Colors.BLACK
    VIS_COLOR = Colors.RED
