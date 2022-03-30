"""Creates square objects that drives the visualizations"""


DEFAULT_COLOR = (255, 255, 255)
OPEN_COLOR = (64, 224, 208)
OPEN_2_COLOR = (64, 223, 208)
OPEN_3_COLOR = (64, 225, 208)
CLOSED_COLOR = (0, 0, 255)
CLOSED_2_COLOR = (0, 0, 254)
CLOSED_3_COLOR = (0, 0, 253)
START_COLOR = (0, 255, 0)
MID_COLOR = (255, 165, 0)
END_COLOR = (255, 0, 0)
WALL_COLOR = (0, 0, 0)
WALL_COLOR_MAP = (0, 0, 0)
PATH_COLOR = (255, 255, 0)
HISTORY_COLOR = (106, 13, 173)


class Square:
    """Defines the properties needed for each node on graph"""

    __slots__ = (
        "row",
        "col",
        "rows",
        "square_size",
        "x",
        "y",
        "neighbours",
        "color",
        "wall_color",
        "color_history",
        "is_highway"
    )

    # Keeps track of all the nodes of each type for easy manipulation
    all_empty_nodes = set()
    all_open_nodes = set()
    all_open2_nodes = set()
    all_open3_nodes = set()
    all_closed_nodes = set()
    all_closed2_nodes = set()
    all_closed3_nodes = set()
    all_start_nodes = set()
    all_mid_nodes = set()
    all_end_nodes = set()
    all_wall_nodes = set()
    all_path_nodes = set()
    all_history_nodes = set()

    # All changed nodes are queue for update each frame
    nodes_to_update = set()

    # Used for checking if only changed nodes are being updated
    node_history = set()
    track_node_history = False

    def __init__(self, row: int, col: int, rows: int, square_size: float) -> None:
        self.row = row
        self.col = col
        self.rows = rows
        self.square_size = square_size

        self.x: float = self.row * self.square_size
        self.y: float = self.col * self.square_size
        self.neighbours: dict = {}
        self.color = DEFAULT_COLOR
        self.wall_color = WALL_COLOR
        self.color_history = None
        self.is_highway = False

    def __lt__(self, _) -> bool:
        """Allows comparison of squares"""
        return False

    def get_pos(self) -> tuple[int, int]:
        """Returns the square location"""
        return self.row, self.col

    def get_color(self) -> tuple:
        """Gets color of square"""
        return self.color
    
    def get_neighbours(self, include_walls=False) -> list:
        """Gets list of neighbours"""
        neighbours = []
        for direction in self.neighbours:
            nei: Square = self.neighbours[direction]
            # Append walls to list if include_walls and nei exists
            if nei:
                if not nei.is_wall():
                    neighbours.append(nei)
                elif include_walls:
                    neighbours.append(nei)
        return neighbours

    def draw_square(self) -> tuple:
        """Updates the square with node type"""
        return self.color, (
            self.x,
            self.y,
            int(self.square_size),
            int(self.square_size),
        )

    def is_empty(self) -> bool:
        """Checks if blank node"""
        return self.color == DEFAULT_COLOR

    def is_open(self) -> bool:
        """Checks if open node"""
        return self.color == OPEN_COLOR

    def is_open2(self) -> bool:
        """Checks if open node for second swarm of bi_dijkstra"""
        return self.color == OPEN_2_COLOR

    def is_open3(self) -> bool:
        """Checks if open node for end node when mid is included"""
        return self.color == OPEN_3_COLOR

    def is_closed(self) -> bool:
        """Checks if closed node"""
        return self.color == CLOSED_COLOR

    def is_closed2(self) -> bool:
        """Checks if closed node for second swarm of bi_dijkstra"""
        return self.color == CLOSED_2_COLOR

    def is_closed3(self) -> bool:
        """Checks if closed node for end node when mid is included"""
        return self.color == CLOSED_3_COLOR

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

    def is_history(self) -> bool:
        """Checks if history node"""
        return self.color == HISTORY_COLOR

    def reset(self) -> None:
        """Sets node to blank"""
        # Don't do anything if already set correctly
        if self.is_empty():
            return

        # Add to node history if user requests to track
        if type(self).track_node_history:
            type(self).node_history.add(self)

        self._discard_node()
        self.color, self.is_highway = DEFAULT_COLOR, False
        type(self).nodes_to_update.add(self)
        type(self).all_empty_nodes.add(self)

    def set_open(self) -> None:
        """Sets node to open"""
        # Don't do anything if already set correctly
        if self.is_open():
            return

        # Add to node history if user requests to track
        if type(self).track_node_history:
            type(self).node_history.add(self)

        self._discard_node()
        self.color = OPEN_COLOR
        type(self).nodes_to_update.add(self)
        type(self).all_open_nodes.add(self)

    def set_open2(self) -> None:
        """Sets node to open for second swarm of bi_dijkstra"""
        # Don't do anything if already set correctly
        if self.is_open2():
            return

        # Add to node history if user requests to track
        if type(self).track_node_history:
            type(self).node_history.add(self)

        self._discard_node()
        self.color = OPEN_2_COLOR
        type(self).nodes_to_update.add(self)
        type(self).all_open2_nodes.add(self)

    def set_open3(self) -> None:
        """Sets node to open for end node when mid is included.
        Each swarms needs to be different colors for best path algo to work.
        """
        # Don't do anything if already set correctly
        if self.is_open3():
            return

        # Add to node history if user requests to track
        if type(self).track_node_history:
            type(self).node_history.add(self)

        self._discard_node()
        self.color = OPEN_3_COLOR
        type(self).nodes_to_update.add(self)
        type(self).all_open3_nodes.add(self)

    def set_closed(self) -> None:
        """Sets node to closed"""
        # Don't do anything if already set correctly
        if self.is_closed():
            return

        # Add to node history if user requests to track
        if type(self).track_node_history:
            type(self).node_history.add(self)

        self._discard_node()
        self.color = CLOSED_COLOR
        type(self).nodes_to_update.add(self)
        type(self).all_closed_nodes.add(self)

    def set_closed2(self) -> None:
        """Sets node to closed for second swarm of bi_dijkstra"""
        # Don't do anything if already set correctly
        if self.is_closed2():
            return

        # Add to node history if user requests to track
        if type(self).track_node_history:
            type(self).node_history.add(self)

        self._discard_node()
        self.color = CLOSED_2_COLOR
        type(self).nodes_to_update.add(self)
        type(self).all_closed2_nodes.add(self)

    def set_closed3(self) -> None:
        """Sets node to closed for end now when mid is included"""
        # Don't do anything if already set correctly
        if self.is_closed3():
            return

        # Add to node history if user requests to track
        if type(self).track_node_history:
            type(self).node_history.add(self)

        self._discard_node()
        self.color = CLOSED_3_COLOR
        type(self).nodes_to_update.add(self)
        type(self).all_closed3_nodes.add(self)

    def set_start(self) -> None:
        """Sets node to start"""
        # Don't do anything if already set correctly
        if self.is_start():
            return

        # Add to node history if user requests to track
        if type(self).track_node_history:
            type(self).node_history.add(self)

        self._discard_node(remove_wall=False)
        self.color = START_COLOR
        type(self).nodes_to_update.add(self)
        type(self).all_start_nodes.add(self)

    def set_mid(self) -> None:
        """Sets node to mid"""
        # Don't do anything if already set correctly
        if self.is_mid():
            return

        # Add to node history if user requests to track
        if type(self).track_node_history:
            type(self).node_history.add(self)

        self._discard_node(remove_wall=False)
        self.color = MID_COLOR
        type(self).nodes_to_update.add(self)
        type(self).all_mid_nodes.add(self)

    def set_end(self) -> None:
        """Sets node to end"""
        # Don't do anything if already set correctly
        if self.is_end():
            return

        # Add to node history if user requests to track
        if type(self).track_node_history:
            type(self).node_history.add(self)

        self._discard_node(remove_wall=False)
        self.color = END_COLOR
        type(self).nodes_to_update.add(self)
        type(self).all_end_nodes.add(self)

    def set_wall(self) -> None:
        """Sets node to wall"""
        # Don't do anything if already set correctly
        if self.is_wall():
            return

        # Add to node history if user requests to track
        if type(self).track_node_history:
            type(self).node_history.add(self)

        self._discard_node()
        self.color = self.wall_color
        type(self).nodes_to_update.add(self)
        type(self).all_wall_nodes.add(self)

    def set_path(self) -> None:
        """Sets node to path"""
        # Don't do anything if already set correctly
        if self.is_path():
            return

        # Add to node history if user requests to track
        if type(self).track_node_history:
            type(self).node_history.add(self)

        self._discard_node()
        self.color = PATH_COLOR
        type(self).nodes_to_update.add(self)
        type(self).all_path_nodes.add(self)

    def set_history(self) -> None:
        """Sets node to history visualization"""
        # Don't do anything if already set correctly
        if self.is_history():
            return

        # Don't do anything if ordinal node or path node
        if self.is_start() or self.is_mid() or self.is_end() or self.is_path():
            return

        self.color_history = self.color
        self.color = HISTORY_COLOR
        type(self).all_history_nodes.add(self)
    
    def update_neighbours(self, gph) -> None:
        """Updates this square's neighbours in the four cardinal directions"""

        self.neighbours["Left"] = None
        self.neighbours["Up"] = None
        self.neighbours["Right"] = None
        self.neighbours["Down"] = None

        if self.col > 0:
            self.neighbours["Left"] = gph.graph[self.row][self.col - 1]
        if self.row > 0:
            self.neighbours["Up"] = gph.graph[self.row - 1][self.col]
        if self.col < self.rows - 1:
            self.neighbours["Right"] = gph.graph[self.row][self.col + 1]
        if self.row < self.rows - 1:
            self.neighbours["Down"] = gph.graph[self.row + 1][self.col]

    def reset_wall_color(self) -> None:
        """Resets wall color to default"""
        self.wall_color = WALL_COLOR

    def set_wall_color_map(self) -> None:
        """Resets wall color for map to default"""
        self.wall_color = WALL_COLOR_MAP

    def _discard_node(self, remove_wall=True) -> None:
        """Discard the node from corresponding set when changed"""

        # Ordinal nodes should not remove wall to reinstate after dragging
        if remove_wall:
            type(self).all_wall_nodes.discard(self)

        type(self).all_empty_nodes.discard(self)
        type(self).all_open_nodes.discard(self)
        type(self).all_open2_nodes.discard(self)
        type(self).all_open3_nodes.discard(self)
        type(self).all_closed_nodes.discard(self)
        type(self).all_closed2_nodes.discard(self)
        type(self).all_closed3_nodes.discard(self)
        type(self).all_start_nodes.discard(self)
        type(self).all_mid_nodes.discard(self)
        type(self).all_end_nodes.discard(self)
        type(self).all_path_nodes.discard(self)

    @classmethod
    def get_all_empty_nodes(cls, copy=False) -> set:
        """Gets all empty nodes"""
        if copy:
            return cls.all_empty_nodes.copy()
        return cls.all_empty_nodes

    @classmethod
    def get_all_open_nodes(cls, copy=False) -> set:
        """Gets all open nodes"""
        if copy:
            return cls.all_open_nodes.copy()
        return cls.all_open_nodes

    @classmethod
    def get_all_open2_nodes(cls, copy=False) -> set:
        """Gets all open_2 nodes"""
        if copy:
            return cls.all_open2_nodes.copy()
        return cls.all_open2_nodes

    @classmethod
    def get_all_open3_nodes(cls, copy=False) -> set:
        """Gets all open_3 nodes"""
        if copy:
            return cls.all_open3_nodes.copy()
        return cls.all_open3_nodes

    @classmethod
    def get_all_closed_nodes(cls, copy=False) -> set:
        """Gets all closed nodes"""
        if copy:
            return cls.all_closed_nodes.copy()
        return cls.all_closed_nodes

    @classmethod
    def get_all_closed2_nodes(cls, copy=False) -> set:
        """Gets all closed_2 nodes"""
        if copy:
            return cls.all_closed2_nodes.copy()
        return cls.all_closed2_nodes

    @classmethod
    def get_all_closed3_nodes(cls, copy=False) -> set:
        """Gets all closed_3 nodes"""
        if copy:
            return cls.all_closed3_nodes.copy()
        return cls.all_closed3_nodes

    @classmethod
    def get_all_start_nodes(cls, copy=False) -> set:
        """Gets all start nodes"""
        if copy:
            return cls.all_start_nodes.copy()
        return cls.all_start_nodes

    @classmethod
    def get_all_mid_nodes(cls, copy=False) -> set:
        """Gets all mid nodes"""
        if copy:
            return cls.all_mid_nodes.copy()
        return cls.all_mid_nodes

    @classmethod
    def get_all_end_nodes(cls, copy=False) -> set:
        """Gets all end nodes"""
        if copy:
            return cls.all_end_nodes.copy()
        return cls.all_end_nodes

    @classmethod
    def get_all_wall_nodes(cls, copy=False) -> set:
        """Gets all wall nodes"""
        if copy:
            return cls.all_wall_nodes.copy()
        return cls.all_wall_nodes

    @classmethod
    def get_all_path_nodes(cls, copy=False) -> set:
        """Gets all path nodes"""
        if copy:
            return cls.all_path_nodes.copy()
        return cls.all_path_nodes

    @classmethod
    def get_all_history_nodes(cls, copy=False) -> set:
        """Gets all history nodes"""
        if copy:
            return cls.all_history_nodes.copy()
        return cls.all_history_nodes

    @classmethod
    def get_nodes_to_update(cls, copy=False) -> set:
        """Gets nodes to update"""
        if copy:
            return cls.nodes_to_update.copy()
        return cls.nodes_to_update

    @classmethod
    def get_node_history(cls, copy=False) -> set:
        """Get node history"""
        if copy:
            return cls.node_history.copy()
        return cls.node_history

    @classmethod
    def clear_nodes_to_update(cls) -> None:
        """Clears nodes to update"""
        cls.nodes_to_update.clear()

    @classmethod
    def clear_all_node_lists(cls, clear_empty=True) -> None:
        """Clears the list of all nodes for recreating graph"""
        
        # May not want to clear empty since will likely be reseting
        if clear_empty:
            cls.all_empty_nodes.clear()
        
        cls.all_open_nodes.clear()
        cls.all_open2_nodes.clear()
        cls.all_open3_nodes.clear()
        cls.all_closed_nodes.clear()
        cls.all_closed2_nodes.clear()
        cls.all_closed3_nodes.clear()
        cls.all_start_nodes.clear()
        cls.all_mid_nodes.clear()
        cls.all_end_nodes.clear()
        cls.all_wall_nodes.clear()
        cls.all_path_nodes.clear()
        cls.all_history_nodes.clear()

    @classmethod
    def clear_history_nodes(cls) -> None:
        """Clears set that keeps track of history nodes"""
        cls.all_history_nodes.clear()

    @classmethod
    def clear_node_history(cls) -> None:
        """Clears node history"""
        cls.node_history.clear()
