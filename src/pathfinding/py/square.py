"""Creates square objects that drives the visualizations"""


class Square:
    """Defines the properties needed for each square on graph"""

    __slots__ = (
        "row",
        "col",
        "pos",
        "rows",
        "x",
        "y",
        "square_dim",
        "neighbours",
        "color",
        "wall_color",
        "color_history",
        "highway"
    )
    
    # Possible colors for square
    _DEFAULT_COLOR = (255, 255, 255)
    _OPEN_COLOR = (64, 224, 208)
    _OPEN2_COLOR = (64, 223, 208)
    _OPEN3_COLOR = (64, 225, 208)
    _CLOSED_COLOR = (0, 0, 255)
    _CLOSED2_COLOR = (0, 0, 254)
    _CLOSED3_COLOR = (0, 0, 253)
    _START_COLOR = (0, 255, 0)
    _MID_COLOR = (255, 165, 0)
    _END_COLOR = (255, 0, 0)
    __WALL_COLOR = (0, 0, 0)  # To avoid using over self.wall_color
    __WALL_COLOR_MAP = (0, 0, 0)  # To avoid using over self.wall_color
    _PATH_COLOR = (255, 255, 0)
    _HISTORY_COLOR = (106, 13, 173)
    
    # Extend set class and remove ability to .copy() to
    # force use of copy module. This is for seamless compatibility
    # with the C++ square implementation of this class

    # Stores the instances of all the squares in a 1D graph for cache efficiency.
    # Row-major order
    graph: list['Square'] = []

    # Info about the squares
    num_rows = 46  # Default value.
    num_cols = 46  # Default value.
    square_length = 0  # Assigned in init() method

    # Keeps track of all the squares of each type for easy manipulation
    # These are copied when accessed from outside class to match C++
    # implementation behaviour as it can only return by value. 10us -> 350us
    all_empty_squares = set()
    all_open_squares = set()
    all_open2_squares = set()
    all_open3_squares = set()
    all_closed_squares = set()
    all_closed2_squares = set()
    all_closed3_squares = set()
    all_start_squares = set()
    all_mid_squares = set()
    all_end_squares = set()
    all_wall_squares = set()
    all_path_squares = set()
    all_history_squares = set()

    # All changed squares are queue for update each frame
    squares_to_update = set()

    # Used for checking if only changed squares are being updated
    future_history_squares = set()
    track_square_history = False

    # Null square for easy checks
    null_square = None

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

        self.pos = row, col
        self.x: float = self.row * Square.square_length
        self.y: float = self.col * Square.square_length
        self.square_dim = (self.x, self.y, int(Square.square_length), int(Square.square_length))
        self.neighbours: dict = {}
        self.color = Square._DEFAULT_COLOR
        self.wall_color = Square.__WALL_COLOR
        self.color_history = None
        self.highway = False

    def __bool__(self) -> bool:
        """Returns false for impossible squares"""
        return (self.row >= 0 and self.col >= 0)

    def get_pos(self) -> tuple[int, int]:
        """Returns the square location"""
        return self.pos

    def get_color(self) -> tuple:
        """Gets color of square"""
        return self.color
    
    def get_neighbours(self) -> list:
        """Gets list of neighbours"""
        neighbours = []
        for direction in self.neighbours:
            nei: Square = self.neighbours[direction]
            # Append walls to list if nei exists
            neighbours.append(nei)
        return neighbours

    def draw_square(self) -> tuple:
        """Updates the square with square type"""
        return self.square_dim

    def is_empty(self) -> bool:
        """Checks if blank square"""
        return self.color == Square._DEFAULT_COLOR

    def is_open(self) -> bool:
        """Checks if open square"""
        return self.color == Square._OPEN_COLOR

    def is_open2(self) -> bool:
        """Checks if open square for second swarm of bi_dijkstra"""
        return self.color == Square._OPEN2_COLOR

    def is_open3(self) -> bool:
        """Checks if open square for end square when mid is included"""
        return self.color == Square._OPEN3_COLOR

    def is_closed(self) -> bool:
        """Checks if closed square"""
        return self.color == Square._CLOSED_COLOR

    def is_closed2(self) -> bool:
        """Checks if closed square for second swarm of bi_dijkstra"""
        return self.color == Square._CLOSED2_COLOR

    def is_closed3(self) -> bool:
        """Checks if closed square for end square when mid is included"""
        return self.color == Square._CLOSED3_COLOR

    def is_start(self) -> bool:
        """Checks if start square"""
        return self.color == Square._START_COLOR

    def is_mid(self) -> bool:
        """Checks if mid square"""
        return self.color == Square._MID_COLOR

    def is_end(self) -> bool:
        """Checks if end square"""
        return self.color == Square._END_COLOR

    def is_wall(self) -> bool:
        """Checks if wall square"""
        return self.color == self.wall_color

    def is_path(self) -> bool:
        """Checks if path square"""
        return self.color == Square._PATH_COLOR

    def is_history(self) -> bool:
        """Checks if history square"""
        return self.color == Square._HISTORY_COLOR
    
    def is_highway(self) -> bool:
        """Checks if square is a highway"""
        return self.highway

    def reset(self) -> None:
        """Sets square to blank"""
        # Don't do anything if already set correctly
        if self.is_empty():
            return

        # Add to square history if user requests to track
        if Square.track_square_history:
            Square.future_history_squares.add(self)

        self._discard_square()
        self.color = Square._DEFAULT_COLOR
        self.highway = False
        Square.squares_to_update.add(self)
        Square.all_empty_squares.add(self)

    def set_open(self) -> None:
        """Sets square to open"""
        # Don't do anything if already set correctly
        if self.is_open():
            return

        # Add to square history if user requests to track
        if Square.track_square_history:
            Square.future_history_squares.add(self)

        self._discard_square()
        self.color = Square._OPEN_COLOR
        Square.squares_to_update.add(self)
        Square.all_open_squares.add(self)

    def set_open2(self) -> None:
        """Sets square to open for second swarm of bi_dijkstra"""
        # Don't do anything if already set correctly
        if self.is_open2():
            return

        # Add to square history if user requests to track
        if Square.track_square_history:
            Square.future_history_squares.add(self)

        self._discard_square()
        self.color = Square._OPEN2_COLOR
        Square.squares_to_update.add(self)
        Square.all_open2_squares.add(self)

    def set_open3(self) -> None:
        """Sets square to open for end square when mid is included.
        Each swarms needs to be different colors for best path algo to work.
        """
        # Don't do anything if already set correctly
        if self.is_open3():
            return

        # Add to square history if user requests to track
        if Square.track_square_history:
            Square.future_history_squares.add(self)

        self._discard_square()
        self.color = Square._OPEN3_COLOR
        Square.squares_to_update.add(self)
        Square.all_open3_squares.add(self)

    def set_closed(self) -> None:
        """Sets square to closed"""
        # Don't do anything if already set correctly
        if self.is_closed():
            return

        # Add to square history if user requests to track
        if Square.track_square_history:
            Square.future_history_squares.add(self)

        self._discard_square()
        self.color = Square._CLOSED_COLOR
        Square.squares_to_update.add(self)
        Square.all_closed_squares.add(self)

    def set_closed2(self) -> None:
        """Sets square to closed for second swarm of bi_dijkstra"""
        # Don't do anything if already set correctly
        if self.is_closed2():
            return

        # Add to square history if user requests to track
        if Square.track_square_history:
            Square.future_history_squares.add(self)

        self._discard_square()
        self.color = Square._CLOSED2_COLOR
        Square.squares_to_update.add(self)
        Square.all_closed2_squares.add(self)

    def set_closed3(self) -> None:
        """Sets square to closed for end now when mid is included"""
        # Don't do anything if already set correctly
        if self.is_closed3():
            return

        # Add to square history if user requests to track
        if Square.track_square_history:
            Square.future_history_squares.add(self)

        self._discard_square()
        self.color = Square._CLOSED3_COLOR
        Square.squares_to_update.add(self)
        Square.all_closed3_squares.add(self)

    def set_start(self) -> None:
        """Sets square to start"""
        # Don't do anything if already set correctly
        if self.is_start():
            return

        # Add to square history if user requests to track
        if Square.track_square_history:
            Square.future_history_squares.add(self)

        self._discard_square(remove_wall=False)
        self.color = Square._START_COLOR
        Square.squares_to_update.add(self)
        Square.all_start_squares.add(self)

    def set_mid(self) -> None:
        """Sets square to mid"""
        # Don't do anything if already set correctly
        if self.is_mid():
            return

        # Add to square history if user requests to track
        if Square.track_square_history:
            Square.future_history_squares.add(self)

        self._discard_square(remove_wall=False)
        self.color = Square._MID_COLOR
        Square.squares_to_update.add(self)
        Square.all_mid_squares.add(self)

    def set_end(self) -> None:
        """Sets square to end"""
        # Don't do anything if already set correctly
        if self.is_end():
            return

        # Add to square history if user requests to track
        if Square.track_square_history:
            Square.future_history_squares.add(self)

        self._discard_square(remove_wall=False)
        self.color = Square._END_COLOR
        Square.squares_to_update.add(self)
        Square.all_end_squares.add(self)

    def set_wall(self) -> None:
        """Sets square to wall"""
        # Don't do anything if already set correctly
        if self.is_wall():
            return

        # Add to square history if user requests to track
        if Square.track_square_history:
            Square.future_history_squares.add(self)

        self._discard_square()
        self.color = self.wall_color
        Square.squares_to_update.add(self)
        Square.all_wall_squares.add(self)

    def set_path(self) -> None:
        """Sets square to path"""
        # Don't do anything if already set correctly
        if self.is_path():
            return

        # Add to square history if user requests to track
        if Square.track_square_history:
            Square.future_history_squares.add(self)

        self._discard_square()
        self.color = Square._PATH_COLOR
        Square.squares_to_update.add(self)
        Square.all_path_squares.add(self)

    def set_history(self) -> None:
        """Sets square to history visualization"""
        # Don't do anything if already set correctly
        if self.is_history():
            return

        # Don't do anything if ordinal square or path square
        if self.is_path() or self.is_start() or self.is_mid() or self.is_end():
            return

        # Don't discard square from list as will be immediately revert color
        # Also don't add to squares_to_update as it is handled differently
        self.color_history = self.color
        self.color = Square._HISTORY_COLOR
        Square.all_history_squares.add(self)
    
    def set_history_rollback(self) -> None:
        """Set square to previous color before setting to history"""
        self.color = self.color_history

    def set_wall_color_map(self) -> None:
        """Resets wall color for map to default"""
        self.wall_color = Square.__WALL_COLOR_MAP
    
    def set_highway(self, x: bool) -> None:
        """Sets the square to highway"""
        self.highway = x
    
    def _update_neighbours(self) -> None:
        """Updates this square's neighbours in the four cardinal directions"""
        if self.col > 0:
            self.neighbours["Left"] = Square.get_square(self.row, self.col - 1)
        if self.row > 0:
            self.neighbours["Up"] = Square.get_square(self.row - 1, self.col)
        if self.col < Square.num_cols - 1:
            self.neighbours["Right"] = Square.get_square(self.row, self.col + 1)
        if self.row < Square.num_rows - 1:
            self.neighbours["Down"] = Square.get_square(self.row + 1, self.col)

    def _reset_wall_color(self) -> None:
        """Resets wall color to default"""
        self.wall_color = Square.__WALL_COLOR

    def _discard_square(self, remove_wall=True) -> None:
        """Discard the square from corresponding set when changed"""
        
        # Ordinal squares should not remove wall to reinstate after dragging
        if not remove_wall and self.is_wall():
            return
        
        if self.is_empty():
            Square.all_empty_squares.discard(self)
        elif self.is_open():
            Square.all_open_squares.discard(self)
        elif self.is_open2():
            Square.all_open2_squares.discard(self)
        elif self.is_open3():
            Square.all_open3_squares.discard(self)
        elif self.is_closed():
            Square.all_closed_squares.discard(self)
        elif self.is_closed2():
            Square.all_closed2_squares.discard(self)
        elif self.is_closed3():
            Square.all_closed3_squares.discard(self)
        elif self.is_start():
            Square.all_start_squares.discard(self)
        elif self.is_mid():
            Square.all_mid_squares.discard(self)
        elif self.is_end():
            Square.all_end_squares.discard(self)
        elif self.is_wall():
            Square.all_wall_squares.discard(self)
        elif self.is_path():
            Square.all_path_squares.discard(self)
        elif self.is_history():
            Square.all_history_squares.discard(self)

    @classmethod
    def init(cls, graph_width, pixel_offset=0) -> None:
        """Initializes the graph for the class"""
        # Reset class
        cls._clear_all_square_lists()
        cls.graph.clear()
        
        # Update values
        cls._update_square_length(graph_width, pixel_offset)
        
        # Emplace each square into graph in row-major order
        for row in range(cls.num_rows):
            for col in range(cls.num_cols):
                cls.graph.append(Square(row, col))
        
        # Update neighbours once graph is done
        for square in cls.graph:
            square._update_neighbours()

        cls.null_square = Square(-1, -1)
    
    @classmethod
    def get_square(cls, row, col) -> 'Square':
        """Get a square by row and col"""
        return cls.graph[cls.num_cols * row + col]

    @classmethod
    def get_num_rows(cls) -> int:
        """Get number of rows in graph"""
        return cls.num_rows

    @classmethod
    def get_num_cols(cls) -> int:
        """Get number of rows in graph"""
        return cls.num_cols

    @classmethod
    def get_square_length(cls) -> float:
        """Get square size of a single dimension"""
        return cls.square_length
    
    @classmethod
    def get_all_empty_squares(cls) -> list:
        """Gets all empty squares"""
        return list(cls.all_empty_squares)

    @classmethod
    def get_all_open_squares(cls) -> list:
        """Gets all open squares"""
        return list(cls.all_open_squares)

    @classmethod
    def get_all_open2_squares(cls) -> list:
        """Gets all open_2 squares"""
        return list(cls.all_open2_squares)

    @classmethod
    def get_all_open3_squares(cls) -> list:
        """Gets all open_3 squares"""
        return list(cls.all_open3_squares)

    @classmethod
    def get_all_closed_squares(cls) -> list:
        """Gets all closed squares"""
        return list(cls.all_closed_squares)

    @classmethod
    def get_all_closed2_squares(cls) -> list:
        """Gets all closed_2 squares"""
        return list(cls.all_closed2_squares)

    @classmethod
    def get_all_closed3_squares(cls) -> list:
        """Gets all closed_3 squares"""
        return list(cls.all_closed3_squares)

    @classmethod
    def get_all_start_squares(cls) -> list:
        """Gets all start squares"""
        return list(cls.all_start_squares)

    @classmethod
    def get_all_mid_squares(cls) -> list:
        """Gets all mid squares"""
        return list(cls.all_mid_squares)

    @classmethod
    def get_all_end_squares(cls) -> list:
        """Gets all end squares"""
        return list(cls.all_end_squares)

    @classmethod
    def get_all_wall_squares(cls) -> list:
        """Gets all wall squares"""
        return list(cls.all_wall_squares)

    @classmethod
    def get_all_path_squares(cls) -> list:
        """Gets all path squares"""
        return list(cls.all_path_squares)

    @classmethod
    def get_all_history_squares(cls) -> list:
        """Gets all history squares"""
        return list(cls.all_history_squares)

    @classmethod
    def get_squares_to_update(cls) -> list:
        """Gets squares to update"""
        return list(cls.squares_to_update)

    @classmethod
    def get_future_history_squares(cls) -> list:
        """Get square history"""
        return list(cls.future_history_squares)

    @classmethod
    def get_track_square_history(cls) -> bool:
        """Get track square history"""
        return cls.track_square_history

    @classmethod
    def get_null_square(cls) -> "Square":
        """Get the null square"""
        return cls.null_square

    @classmethod
    def reset_algo_squares(cls) -> None:
        """Reset algo squares"""
        squares_to_reset = [
            cls.get_all_open_squares(),
            cls.get_all_open2_squares(),
            cls.get_all_open3_squares(),
            cls.get_all_closed_squares(),
            cls.get_all_closed2_squares(),
            cls.get_all_closed3_squares(),
            cls.get_all_path_squares()
        ]
        square: Square
        for type_set in squares_to_reset:
            for square in type_set:
                square.reset()
    
    @classmethod
    def reset_all_squares(cls) -> None:
        """Reset all squares"""
        squares_to_reset = [
            cls.get_all_open_squares(),
            cls.get_all_open2_squares(),
            cls.get_all_open3_squares(),
            cls.get_all_closed_squares(),
            cls.get_all_closed2_squares(),
            cls.get_all_closed3_squares(),
            cls.get_all_start_squares(),
            cls.get_all_mid_squares(),
            cls.get_all_end_squares(),
            cls.get_all_wall_squares(),
            cls.get_all_path_squares(),
            cls.get_all_history_squares()
        ]
        square: Square
        for type_set in squares_to_reset:
            for square in type_set:
                square._reset_wall_color()
                square.reset()

    @classmethod
    def clear_squares_to_update(cls) -> None:
        """Clears squares to update"""
        cls.squares_to_update.clear()

    @classmethod
    def _clear_all_square_lists(cls) -> None:
        """Clears the list of all squares for recreating graph"""
        cls.all_empty_squares.clear()
        cls.all_open_squares.clear()
        cls.all_open2_squares.clear()
        cls.all_open3_squares.clear()
        cls.all_closed_squares.clear()
        cls.all_closed2_squares.clear()
        cls.all_closed3_squares.clear()
        cls.all_start_squares.clear()
        cls.all_mid_squares.clear()
        cls.all_end_squares.clear()
        cls.all_wall_squares.clear()
        cls.all_path_squares.clear()
        cls.all_history_squares.clear()

    @classmethod
    def clear_history_squares(cls) -> None:
        """Clears set that keeps track of history squares"""
        cls.all_history_squares.clear()

    @classmethod
    def clear_future_history_squares(cls) -> None:
        """Clears square history"""
        cls.future_history_squares.clear()
    
    @classmethod
    def set_track_square_history(cls, x: bool) -> None:
        """Sets track square history to true or false"""
        cls.track_square_history = x

    @classmethod
    def set_square_color_by_group(cls, squares, square_type: str) -> None:
        """Sets a group of squares to a color"""
        square: Square
        if square_type == "reset":
            for square in squares:
                square.reset()
        elif square_type == "open":
            for square in squares:
                square.set_open()
        elif square_type == "open2":
            for square in squares:
                square.set_open2()
        elif square_type == "open3":
            for square in squares:
                square.set_open3()
        elif square_type == "closed":
            for square in squares:
                square.set_closed()
        elif square_type == "closed2":
            for square in squares:
                square.set_closed2()
        elif square_type == "closed3":
            for square in squares:
                square.set_closed3()
        elif square_type == "start":
            for square in squares:
                square.set_start()
        elif square_type == "mid":
            for square in squares:
                square.set_mid()
        elif square_type == "end":
            for square in squares:
                square.set_end()
        elif square_type == "wall":
            for square in squares:
                square.set_wall()
        elif square_type == "path":
            for square in squares:
                square.set_path()
        elif square_type == "history":
            for square in squares:
                square.set_history()
        elif square_type == "history_rollback":
            for square in squares:
                square.set_history_rollback()
        else:
            raise NotImplementedError("Invalid square type provided")

    @classmethod
    def set_square_color_by_array(cls, pixels_r, pixels_g, pixels_b) -> None:
        """Set the square colors based on the 2D array of rgb values."""

        ROAD_CUTOFF = 1  # Any value above this is a road
        HIGHWAY_CUTOFF = 225  # Any value below this is a highway

        square_length = cls.get_square_length()
        square_length_squared = square_length * square_length
        length_int = int(square_length)

        square: Square
        for index, square in enumerate(cls.graph):
            square.set_wall_color_map()
            row, col = square.get_pos()

            rgb_sum = 0
            blue_sum = 0  # Used for highway
            for x in range(row * length_int, (row+1) * length_int):
                for y in range(col * length_int, (col+1) * length_int):
                    rgb_sum += pixels_r[x][y] + pixels_g[x][y] + pixels_b[x][y]
                    blue_sum += pixels_b[x][y]
            rgb_avg = rgb_sum / square_length_squared * 3
            blue_avg = blue_sum / square_length_squared

            # Set squares to roads, highways and non pathable space
            if rgb_avg < ROAD_CUTOFF:
                square.set_wall()
            else:
                square.reset()
                if blue_avg < HIGHWAY_CUTOFF:
                    square.set_highway(True)

    @classmethod
    def update_num_rows_cols(cls, new_num) -> None:
        """Updates the num of rows and cols"""
        cls.num_rows = cls.num_cols = new_num

    @classmethod
    def _update_square_length(cls, graph_width, pixel_offset) -> None:
        """Calculates square size with an optional offset"""
        cls.square_length = (graph_width - pixel_offset) / cls.num_rows
