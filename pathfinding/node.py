"""Creates square objects that drives the visualizations"""


from pathfinding.colors import PygameColors as PygC
from pathfinding.values import ROWS, SQUARE_SIZE


class Square:
    """Defines the properties needed for each node on graph"""

    def __init__(self, row: int, col: int) -> None:
        self.rows: int = ROWS
        self.square_size: float = SQUARE_SIZE
        self.row: int = row
        self.col: int = col
        self.x: float = self.row * self.square_size
        self.y: float = self.col * self.square_size
        self.neighbours: list = []
        self.color = PygC.DEFAULT_COLOR

    def __lt__(self, other) -> bool:
        """Allows comparison of squares"""
        return False

    def get_pos(self) -> tuple[int, int]:
        """Returns the square location"""
        return self.row, self.col

    def update_neighbours(self, graph: list) -> None:
        """Updates the neighbours in the four cardinal directions"""

        self.neighbours = []
        if self.row < self.rows-1 and not graph[self.row + 1][self.col].is_wall():  # Down
            self.neighbours.append(graph[self.row+1][self.col])
        if self.row > 0 and not graph[self.row-1][self.col].is_wall():  # UP
            self.neighbours.append(graph[self.row-1][self.col])
        if self.col < self.rows-1 and not graph[self.row][self.col + 1].is_wall():  # RIGHT
            self.neighbours.append(graph[self.row][self.col+1])
        if self.col > 0 and not graph[self.row][self.col-1].is_wall():  # LEFT
            self.neighbours.append(graph[self.row][self.col-1])

    def is_empty(self) -> bool:
        """Checks if blank node"""
        return self.color == PygC.DEFAULT_COLOR

    def is_open(self) -> bool:
        """Checks if open node"""
        return self.color == PygC.OPEN_COLOR

    def is_open_alt(self) -> bool:
        """Checks if open node for second swarm of bi_dijkstra"""
        return self.color == PygC.OPEN_ALT_COLOR

    def is_open_alt_(self) -> bool:
        """Checks if open node for end node when mid is included"""
        return self.color == PygC.OPEN_ALT_COLOR_

    def is_closed(self) -> bool:
        """Checks if closed node"""
        return self.color == PygC.CLOSED_COLOR

    def is_start(self) -> bool:
        """Checks if start node"""
        return self.color == PygC.START_COLOR

    def is_mid(self) -> bool:
        """Checks if mid node"""
        return self.color == PygC.MID_COLOR

    def is_end(self) -> bool:
        """Checks if end node"""
        return self.color == PygC.END_COLOR

    def is_wall(self) -> bool:
        """Checks if wall node"""
        return self.color == PygC.WALL_COLOR

    def is_path(self) -> bool:
        """Checks if path node"""
        return self.color == PygC.PATH_COLOR

    def reset(self) -> None:
        """Sets node to blank"""
        self.color = PygC.DEFAULT_COLOR

    def set_open(self) -> None:
        """Sets node to open"""
        self.color = PygC.OPEN_COLOR

    def set_open_alt(self) -> None:
        """Sets node to open for second swarm of bi_dijkstra"""
        self.color = PygC.OPEN_ALT_COLOR

    def set_open_alt_(self) -> None:
        """Sets node to open for end node when mid is included.
        Each swarms needs to be different colors for best path algo to work.
        """
        self.color = PygC.OPEN_ALT_COLOR_

    def set_closed(self) -> None:
        """Sets node to closed"""
        self.color = PygC.CLOSED_COLOR

    def set_start(self) -> None:
        """Sets node to start"""
        self.color = PygC.START_COLOR

    def set_mid(self) -> None:
        """Sets node to mid"""
        self.color = PygC.MID_COLOR

    def set_end(self) -> None:
        """Sets node to end"""
        self.color = PygC.END_COLOR

    def set_wall(self) -> None:
        """Sets node to wall"""
        self.color = PygC.WALL_COLOR

    def set_path(self) -> None:
        """Sets node to path"""
        self.color = PygC.PATH_COLOR

    def draw_square(self) -> tuple:
        """Updates the square with node type"""
        return self.color, (self.x, self.y, int(self.square_size), int(self.square_size))

    def update_values(self, rows: int, square_size: float) -> None:
        """Updates the attributes of node. Used when changing graph size"""

        self.rows = rows
        self.square_size = square_size
        self.x = self.row * self.square_size
        self.y = self.col * self.square_size
