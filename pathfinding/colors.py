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

    DEFAULT_COLOR: tuple[int, int, int] = Colors.WHITE
    LEGEND_AREA_COLOR: tuple[int, int, int] = Colors.GREY
    LINE_COLOR: tuple[int, int, int] = Colors.GREY
    OPEN_COLOR: tuple[int, int, int] = Colors.TURQUOISE
    OPEN_ALT_COLOR: tuple[int, int, int] = Colors.TURQUOISE_ALT
    OPEN_ALT_COLOR_: tuple[int, int, int] = Colors.TURQUOISE_ALT_
    CLOSED_COLOR: tuple[int, int, int] = Colors.BLUE
    START_COLOR: tuple[int, int, int] = Colors.GREEN
    MID_COLOR: tuple[int, int, int] = Colors.ORANGE
    END_COLOR: tuple[int, int, int] = Colors.RED
    WALL_COLOR: tuple[int, int, int] = Colors.BLACK
    PATH_COLOR: tuple[int, int, int] = Colors.YELLOW
    LEGEND_COLOR: tuple[int, int, int] = Colors.BLACK
    VIS_COLOR: tuple[int, int, int] = Colors.RED
