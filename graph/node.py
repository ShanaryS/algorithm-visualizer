class Square():
    """Defines the properties needed for each node on graph"""
    def __init__(self, row, col):
        # Gains access to parent class methods and attributes
        super().__init__()

        # Defines attributes of nodes
        self.rows = self.rows
        self.square_size = self.square_size
        self.row = row
        self.col = col
        self.x = self.row * self.square_size
        self.y = self.col * self.square_size
        self.neighbours = []
        self.color = self.DEFAULT_COLOR

    def __lt__(self, other):
        """Allows comparison of squares"""
        return False

    def get_pos(self):
        """Returns the square location"""
        return self.row, self.col

    def update_neighbours(self, graph):
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

    def is_empty(self):
        """Checks if blank node"""
        return self.color == self.DEFAULT_COLOR

    def is_open(self):
        """Checks if open node"""
        return self.color == self.OPEN_COLOR

    def is_open_alt(self):
        """Checks if open node for second swarm of bi_dijkstra"""
        return self.color == self.OPEN_ALT_COLOR

    def is_open_alt_(self):
        """Checks if open node for end node when mid is included"""
        return self.color == self.OPEN_ALT_COLOR_

    def is_closed(self):
        """Checks if closed node"""
        return self.color == self.CLOSED_COLOR

    def is_start(self):
        """Checks if start node"""
        return self.color == self.START_COLOR

    def is_mid(self):
        """Checks if mid node"""
        return self.color == self.MID_COLOR

    def is_end(self):
        """Checks if end node"""
        return self.color == self.END_COLOR

    def is_wall(self):
        """Checks if wall node"""
        return self.color == self.WALL_COLOR

    def is_path(self):
        """Checks if path node"""
        return self.color == self.PATH_COLOR

    def reset(self):
        """Sets node to blank"""
        self.color = self.DEFAULT_COLOR

    def set_open(self):
        """Sets node to open"""
        self.color = self.OPEN_COLOR

    def set_open_alt(self):
        """Sets node to open for second swarm of bi_dijkstra"""
        self.color = self.OPEN_ALT_COLOR

    def set_open_alt_(self):
        """Sets node to open for end node when mid is included.
        Each swarms needs to be different colors for best path algo to work.
        """
        self.color = self.OPEN_ALT_COLOR_

    def set_closed(self):
        """Sets node to closed"""
        self.color = self.CLOSED_COLOR

    def set_start(self):
        """Sets node to start"""
        self.color = self.START_COLOR

    def set_mid(self):
        """Sets node to mid"""
        self.color = self.MID_COLOR

    def set_end(self):
        """Sets node to end"""
        self.color = self.END_COLOR

    def set_wall(self):
        """Sets node to wall"""
        self.color = self.WALL_COLOR

    def set_path(self):
        """Sets node to path"""
        self.color = self.PATH_COLOR

    def draw_square(self):
        """Updates the square with node type"""
        return self.color, (self.x, self.y, int(self.square_size), int(self.square_size))

    def update_values(self, rows, square_size):
        """Updates the attributes of node. Used when changing graph size"""
        self.rows = rows
        self.square_size = square_size
        self.x = self.row * self.square_size
        self.y = self.col * self.square_size
