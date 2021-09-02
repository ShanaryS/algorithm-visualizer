import pygame
from queue import PriorityQueue


# Stuff I will prob need
# rect = pygame.Rect(x_loc, y_loc, x_len, y_len)
# self.WINDOW.blit(source, (x_loc, y_loc or Rect))
# pygame.draw.rect(self.WINDOW, color, rect, width>0 for line)
# pygame.draw.line(self.WINDOW, color, start_pos, end+pos, width)
# pygame.draw.lines()
# pygame.font.init()
# pygame.font.SysFont()
# pygame.time.delay()
# rect.colliderect(rect2) # to check if two rect collided
# pygame.USEREVENT + n /// pygame.event.post(pygame.event.Event(pygame.USEREVENT)) # Where n is a unique event
# Set so can't change edge border of game
# Allow rectangle graph instead of just square
# Allow diag transitions or maybe not
# Pygame slow startup, check in separate python file
# Replicate colors of clement
# Add UI elements to select different algos
# Maybe algo args in constructor, might be cleaner

# Inspired by Tech With Tim
class PathfindingVisualizer:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 800
        self.WINDOW = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pathfinding Visualizer")

        self.FPS = 1000
        self.ROWS = 50
        # self.COLS = 50        # Use to make graph none square but requires a lot of reworking
        self.SQUARE_SIZE = 16   # num squares = (self.WIDTH/self.SQUARE_SIZE) * (self.HEIGHT/self.SQUARE_SIZE)

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.ORANGE = (255, 165, 0)
        self.PURPLE = (128, 0, 128)
        self.TURQUOISE = (64, 224, 208)
        self.GREY = (128, 128, 128)

    def main(self):     # Put all game specific variables in here so it's easy to restart with main()
        clock = pygame.time.Clock()
        graph = self.set_graph()

        start = None
        end = None

        run = True
        while run:
            clock.tick(self.FPS)
            self.draw(graph)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if pygame.mouse.get_pressed(3)[0]:       # LEFT
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    square = graph[row][col]
                    if not start and square != end:
                        start = square
                        # noinspection PyUnresolvedReferences
                        # PyCharm bug, doesn't realize that square is a Node class object. Above comment removes it.
                        square.set_start()
                    elif not end and square != start:
                        end = square
                        # noinspection PyUnresolvedReferences
                        # PyCharm bug, doesn't realize that square is a Node class object. Above comment removes it.
                        end.set_end()
                    elif square != start and square != end:
                        # noinspection PyUnresolvedReferences
                        # PyCharm bug, doesn't realize that square is a Node class object. Above comment removes it.
                        square.set_barrier()
                elif pygame.mouse.get_pressed(3)[2]:     # RIGHT
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    square = graph[row][col]
                    # noinspection PyUnresolvedReferences
                    # PyCharm bug, doesn't realize that square is a Node class object. Above comment removes it.
                    square.reset()
                    if square == start:
                        start = None
                    elif square == end:
                        end = None
                elif pygame.mouse.get_pressed(3)[1]:
                    for i in range(self.ROWS):
                        for j in range(self.ROWS):
                            square = graph[i][j]
                            square.reset()
                            if square == start:
                                start = None
                            elif square == end:
                                end = None

                # Run A* with "A" key on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a and start and end:
                        for row in graph:
                            for square in row:
                                square.update_neighbours(graph)

                        # noinspection PyTypeChecker
                        # PyCharm bug, doesn't realize that square is a Square class object. This removes it.
                        self.a_star(graph, start, end)

                # Run Dijkstra with "D" key on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d and start and end:
                        for row in graph:
                            for square in row:
                                square.update_neighbours(graph)

                        # noinspection PyTypeChecker
                        # PyCharm bug, doesn't realize that square is a Square class object. This removes it.
                        self.dijkstra(graph, start, end)

        pygame.quit()

    def set_graph(self):
        graph = []
        for i in range(self.ROWS):
            graph.append([])
            for j in range(self.ROWS):
                square = Square(i, j)
                graph[i].append(square)

        return graph

    def draw_graph(self):
        for i in range(self.ROWS):
            pygame.draw.line(self.WINDOW, self.GREY, (0, i * self.SQUARE_SIZE), (self.WIDTH, i * self.SQUARE_SIZE))
            pygame.draw.line(self.WINDOW, self.GREY, (i * self.SQUARE_SIZE, 0), (i * self.SQUARE_SIZE, self.WIDTH))

    def draw(self, graph):
        self.WINDOW.fill(self.WHITE)
        for row in graph:
            for square in row:
                square.draw_square(self.WINDOW)

        self.draw_graph()
        pygame.display.update()

    def get_clicked_pos(self, pos):
        y, x = pos

        row = y // self.SQUARE_SIZE
        col = x // self.SQUARE_SIZE

        return row, col

    # Reorganize dict comp for g score and open_set. Match with a*
    def dijkstra(self, graph, start, end):  # Maybe change to only use source at start per wiki
        queue_pos = 0
        open_set = PriorityQueue()
        open_set.put((0, queue_pos, start))
        open_set_hash = {start}

        g_score = {square: float('inf') for row in graph for square in row}
        g_score[start] = 0
        came_from = {}

        for row in graph:
            for square in row:
                if square != start:
                    g_score[square] = float('inf')
                    open_set.put((g_score[square], queue_pos, square))

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            curr_square = open_set.get()[2]
            open_set_hash.remove(curr_square)

            if curr_square == end:
                self.best_path(came_from, end, graph)
                start.set_start()
                end.set_end()
                return True

            for nei in curr_square.neighbours:
                temp_g_score = g_score[curr_square] + 1

                if temp_g_score < g_score[nei]:
                    came_from[nei] = curr_square
                    g_score[nei] = temp_g_score
                    if nei not in open_set_hash:
                        queue_pos += 1
                        open_set.put((g_score[nei], queue_pos, nei))
                        open_set_hash.add(nei)
                        nei.set_open()

            self.draw(graph)

            if curr_square != start:
                curr_square.set_closed()

        return False

    def a_star(self, graph, start, end):
        queue_pos = 0
        open_set = PriorityQueue()
        open_set.put((0, queue_pos, start))
        open_set_hash = {start}

        came_from = {}
        g_score = {square: float('inf') for row in graph for square in row}
        g_score[start] = 0
        f_score = {square: float('inf') for row in graph for square in row}
        f_score[start] = self.heuristic(start.get_pos(), end.get_pos())

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            curr_square = open_set.get()[2]
            open_set_hash.remove(curr_square)

            if curr_square == end:
                self.best_path(came_from, end, graph)
                start.set_start()
                end.set_end()
                return True

            for nei in curr_square.neighbours:
                temp_g_score = g_score[curr_square] + 1

                if temp_g_score < g_score[nei]:
                    came_from[nei] = curr_square
                    g_score[nei] = temp_g_score
                    f_score[nei] = temp_g_score + self.heuristic(nei.get_pos(), end.get_pos())
                    if nei not in open_set_hash:
                        queue_pos += 1
                        open_set.put((f_score[nei], queue_pos, nei))
                        open_set_hash.add(nei)
                        nei.set_open()

            self.draw(graph)

            if curr_square != start:
                curr_square.set_closed()

        return False

    @staticmethod
    def heuristic(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)

    def best_path(self, came_from, curr_square, graph):
        while curr_square in came_from:
            curr_square = came_from[curr_square]
            curr_square.set_path()
            self.draw(graph)


class Square(PathfindingVisualizer):
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.x = self.row * self.SQUARE_SIZE
        self.y = self.col * self.SQUARE_SIZE
        self.neighbours = []
        self.total_rows = self.ROWS
        self.color = self.WHITE

    def __lt__(self, other):    # Allows comparison of length of squares
        return False

    def get_pos(self):
        return self.row, self.col

    def update_neighbours(self, graph):
        self.neighbours = []
        if self.row < self.ROWS-1 and not graph[self.row+1][self.col].is_barrier():  # Down
            self.neighbours.append(graph[self.row+1][self.col])
        if self.row > 0 and not graph[self.row-1][self.col].is_barrier():  # UP
            self.neighbours.append(graph[self.row-1][self.col])
        if self.col < self.ROWS-1 and not graph[self.row][self.col+1].is_barrier():  # RIGHT
            self.neighbours.append(graph[self.row][self.col+1])
        if self.col > 0 and not graph[self.row][self.col-1].is_barrier():  # LEFT
            self.neighbours.append(graph[self.row][self.col-1])

    def is_open(self):
        return self.color == self.TURQUOISE

    def is_closed(self):
        return self.color == self.BLUE

    def is_start(self):
        return self.color == self.GREEN

    def is_mid(self):
        return self.color == self.ORANGE

    def is_end(self):
        return self.color == self.RED

    def is_barrier(self):
        return self.color == self.BLACK

    def reset(self):
        self.color = self.WHITE

    def set_open(self):
        self.color = self.TURQUOISE

    def set_closed(self):
        self.color = self.BLUE

    def set_start(self):
        self.color = self.GREEN

    def set_mid(self):
        self.color = self.ORANGE

    def set_end(self):
        self.color = self.RED

    def set_barrier(self):
        self.color = self.BLACK

    def set_path(self):
        self.color = self.YELLOW

    def draw_square(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.SQUARE_SIZE, self.SQUARE_SIZE))
