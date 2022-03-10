"""Creates square objects that drives the visualizations"""


from src.pathfinding.colors import *


class Square:
    """Defines the properties needed for each node on graph"""

    all_empty_nodes = set()
    all_open_nodes = set()
    all_open_nodes_alt = set()
    all_open_nodes_alt_ = set()
    all_closed_nodes = set()
    all_closed_nodes_alt = set()
    all_closed_nodes_alt_ = set()
    all_start_nodes = set()
    all_mid_nodes = set()
    all_end_nodes = set()
    all_wall_nodes = set()
    all_path_nodes = set()

    nodes_to_update = []

    def __init__(self, row: int, col: int, rows: int, square_size) -> None:
        self.row: int = row
        self.col: int = col
        self.rows: int = rows
        self.square_size: float = square_size

        self.x: float = self.row * self.square_size
        self.y: float = self.col * self.square_size
        self.neighbours: list = []
        self.color = DEFAULT_COLOR
        self.wall_color = WALL_COLOR
        self.is_highway = False

    def __lt__(self, other) -> bool:
        """Allows comparison of squares"""
        return False

    def get_pos(self) -> tuple[int, int]:
        """Returns the square location"""
        return self.row, self.col

    def update_neighbours(self, gph) -> None:
        """Updates the neighbours in the four cardinal directions"""

        self.neighbours = []
        if self.row < self.rows-1 and not gph.graph[self.row + 1][self.col].is_wall():  # Down
            self.neighbours.append(gph.graph[self.row+1][self.col])
        if self.row > 0 and not gph.graph[self.row-1][self.col].is_wall():  # UP
            self.neighbours.append(gph.graph[self.row-1][self.col])
        if self.col < self.rows-1 and not gph.graph[self.row][self.col + 1].is_wall():  # RIGHT
            self.neighbours.append(gph.graph[self.row][self.col+1])
        if self.col > 0 and not gph.graph[self.row][self.col-1].is_wall():  # LEFT
            self.neighbours.append(gph.graph[self.row][self.col-1])
    
    def _update_surrounding_neighbour_pool(self, gph) -> None:
        """Update's this square's neighbours' neighbours to remove this square.
        Wall nodes cannot be neighbours while every other node can be.
        """
        nei: Square
        for nei in self.neighbours:
            nei.update_neighbours(gph)

    def is_empty(self) -> bool:
        """Checks if blank node"""
        return self.color == DEFAULT_COLOR

    def is_open(self) -> bool:
        """Checks if open node"""
        return self.color == OPEN_COLOR

    def is_open_alt(self) -> bool:
        """Checks if open node for second swarm of bi_dijkstra"""
        return self.color == OPEN_ALT_COLOR

    def is_open_alt_(self) -> bool:
        """Checks if open node for end node when mid is included"""
        return self.color == OPEN_ALT_COLOR_

    def is_closed(self) -> bool:
        """Checks if closed node"""
        return self.color == CLOSED_COLOR
    
    def is_closed_alt(self) -> bool:
        """Checks if closed node for second swarm of bi_dijkstra"""
        return self.color == CLOSED_ALT_COLOR
    
    def is_closed_alt_(self) -> bool:
        """Checks if closed node for end node when mid is included"""
        return self.color == CLOSED_ALT_COLOR_

    def is_start(self) -> bool:
        """Checks if start node"""
        return self.color == START_COLOR

    def is_mid(self) -> bool:
        """Checks if mid node"""
        return self.color == MID_COLOR

    def is_end(self) -> bool:
        """Checks if end node"""
        return self.color == END_COLOR

    def is_wall(self) -> bool:
        """Checks if wall node"""
        return self.color == self.wall_color

    def is_path(self) -> bool:
        """Checks if path node"""
        return self.color == PATH_COLOR
    
    def get_color(self) -> tuple:
        """Gets color of square"""
        return self.color

    def reset(self, gph) -> None:
        """Sets node to blank"""
        self._discard_node()
        self.color, self.is_highway = DEFAULT_COLOR, False
        self._update_surrounding_neighbour_pool(gph)
        type(self).nodes_to_update.append(self)
        type(self).all_empty_nodes.add(self)

    def set_open(self, gph) -> None:
        """Sets node to open"""
        self._discard_node()
        self.color = OPEN_COLOR
        self._update_surrounding_neighbour_pool(gph)
        type(self).nodes_to_update.append(self)
        type(self).all_open_nodes.add(self)

    def set_open_alt(self, gph) -> None:
        """Sets node to open for second swarm of bi_dijkstra"""
        self._discard_node()
        self.color = OPEN_ALT_COLOR
        self._update_surrounding_neighbour_pool(gph)
        type(self).nodes_to_update.append(self)
        type(self).all_open_nodes_alt.add(self)

    def set_open_alt_(self, gph) -> None:
        """Sets node to open for end node when mid is included.
        Each swarms needs to be different colors for best path algo to work.
        """
        self._discard_node()
        self.color = OPEN_ALT_COLOR_
        self._update_surrounding_neighbour_pool(gph)
        type(self).nodes_to_update.append(self)
        type(self).all_open_nodes_alt_.add(self)

    def set_closed(self, gph) -> None:
        """Sets node to closed"""
        self._discard_node()
        self.color = CLOSED_COLOR
        self._update_surrounding_neighbour_pool(gph)
        type(self).nodes_to_update.append(self)
        type(self).all_closed_nodes.add(self)
    
    def set_closed_alt(self, gph) -> None:
        """Sets node to closed for second swarm of bi_dijkstra"""
        self._discard_node()
        self.color = CLOSED_ALT_COLOR
        self._update_surrounding_neighbour_pool(gph)
        type(self).nodes_to_update.append(self)
        type(self).all_closed_nodes_alt.add(self)
    
    def set_closed_alt_(self, gph) -> None:
        """Sets node to closed for end now when mid is included"""
        self._discard_node()
        self.color = CLOSED_ALT_COLOR_
        self._update_surrounding_neighbour_pool(gph)
        type(self).nodes_to_update.append(self)
        type(self).all_closed_nodes_alt_.add(self)

    def set_start(self, gph) -> None:
        """Sets node to start"""
        self._discard_node()
        self.color = START_COLOR
        self._update_surrounding_neighbour_pool(gph)
        type(self).nodes_to_update.append(self)
        type(self).all_start_nodes.add(self)

    def set_mid(self, gph) -> None:
        """Sets node to mid"""
        self._discard_node()
        self.color = MID_COLOR
        self._update_surrounding_neighbour_pool(gph)
        type(self).nodes_to_update.append(self)
        type(self).all_mid_nodes.add(self)

    def set_end(self, gph) -> None:
        """Sets node to end"""
        self._discard_node()
        self.color = END_COLOR
        self._update_surrounding_neighbour_pool(gph)
        type(self).nodes_to_update.append(self)
        type(self).all_end_nodes.add(self)

    def set_wall(self, gph) -> None:
        """Sets node to wall"""
        self._discard_node()
        self.color = self.wall_color
        self._update_surrounding_neighbour_pool(gph)
        type(self).nodes_to_update.append(self)
        type(self).all_wall_nodes.add(self)

    def set_path(self, gph) -> None:
        """Sets node to path"""
        self._discard_node()
        self.color = PATH_COLOR
        self._update_surrounding_neighbour_pool(gph)
        type(self).nodes_to_update.append(self)
        type(self).all_path_nodes.add(self)

    def draw_square(self) -> tuple:
        """Updates the square with node type"""
        return self.color, (self.x, self.y, int(self.square_size), int(self.square_size))
    
    def _discard_node(self) -> None:
        """Discard the node from corresponding set when changed"""
        
        if self.is_empty:
            type(self).all_empty_nodes.discard(self)
        elif self.is_open:
            type(self).all_open_nodes.discard(self)
        elif self.is_open_alt:
            type(self).all_open_nodes_alt.discard(self)
        elif self.is_open_alt_:
            type(self).all_open_nodes_alt_.discard(self)
        elif self.is_closed:
            type(self).all_closed_nodes.discard(self)
        elif self.is_closed_alt:
            type(self).all_closed_nodes_alt.discard(self)
        elif self.is_closed_alt_:
            type(self).all_closed_nodes_alt_.discard(self)
        elif self.is_start:
            type(self).all_start_nodes.discard(self)
        elif self.is_mid:
            type(self).all_mid_nodes.discard(self)
        elif self.is_end:
            type(self).all_end_nodes.discard(self)
        elif self.is_wall:
            type(self).all_wall_nodes.discard(self)
        elif self.is_path:
            type(self).all_path_nodes.discard(self)
    
    @classmethod
    def get_all_empty_nodes(cls) -> set:
        "Gets all empty nodes"
        return cls.all_empty_nodes

    @classmethod
    def get_all_open_nodes(cls) -> set:
        "Gets all open nodes"
        return cls.all_open_nodes

    @classmethod
    def get_all_open_nodes_alt(cls) -> set:
        "Gets all open_alt nodes"
        return cls.all_open_nodes_alt

    @classmethod
    def get_all_open_nodes_alt_(cls) -> set:
        "Gets all open_alt_ nodes"
        return cls.all_open_nodes_alt_

    @classmethod
    def get_all_closed_nodes(cls) -> set:
        "Gets all closed nodes"
        return cls.all_closed_nodes

    @classmethod
    def get_all_closed_nodes_alt(cls) -> set:
        "Gets all closed_alt nodes"
        return cls.all_closed_nodes_alt

    @classmethod
    def get_all_closed_nodes_alt_(cls) -> set:
        "Gets all closed_alt_ nodes"
        return cls.all_closed_nodes_alt_

    @classmethod
    def get_all_start_nodes(cls) -> set:
        "Gets all start nodes"
        return cls.all_start_nodes

    @classmethod
    def get_all_mid_nodes(cls) -> set:
        "Gets all mid nodes"
        return cls.all_mid_nodes

    @classmethod
    def get_all_end_nodes(cls) -> set:
        "Gets all end nodes"
        return cls.all_end_nodes

    @classmethod
    def get_all_wall_nodes(cls) -> set:
        "Gets all wall nodes"
        return cls.all_wall_nodes

    @classmethod
    def get_all_path_nodes(cls) -> set:
        "Gets all path nodes"
        return cls.all_path_nodes
    
    @classmethod
    def get_nodes_to_update(cls) -> list:
        """Gets nodes to update"""
        return cls.nodes_to_update
    
    @classmethod
    def clear_nodes_to_update(cls) -> None:
        """Clears nodes to update"""
        cls.nodes_to_update.clear()
