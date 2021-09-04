import pygame
from queue import PriorityQueue
import random


# noinspection PyUnresolvedReferences, PyTypeChecker
# PyCharm bug, doesn't realize that square is a Node class object. Above comment removes it.
class PathfindingVisualizer:
    def __init__(self):
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 800
        self.WIDTH = 800
        self.HEIGHT = 800
        self.WINDOW = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Pathfinding Visualizer - github.com/ShanaryS/algorithm-visualizer")

        # Recursive division only works on certain row values. 22,23,46,47,94,95.
        self.rows = 46
        # self.COLS = 50        # Use to make graph none square but requires a lot of reworking
        self.square_size = self.WIDTH / self.rows

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

        self.DEFAULT_COLOR = self.WHITE
        self.LINE_COLOR = self.GREY
        self.OPEN_COLOR = self.TURQUOISE
        self.CLOSED_COLOR = self.BLUE
        self.START_COLOR = self.GREEN
        self.MID_COLOR = self.ORANGE
        self.END_COLOR = self.RED
        self.WALL_COLOR = self.BLACK
        self.PATH_COLOR = self.YELLOW
        self.TEXT_COLOR = self.RED

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 12)
        self.legend_add_node = self.font.render("Add Node - Left Click (Start -> End -> Walls)", True, self.TEXT_COLOR)
        self.legend_remove_node = self.font.render("Remove Node - Right Click", True, self.TEXT_COLOR)
        self.legend_clear_graph = self.font.render("Clear Graph - Middle Click", True, self.TEXT_COLOR)
        self.legend_dijkstra = self.font.render("Dijkstra - Press 'D'", True, self.TEXT_COLOR)
        self.legend_a_star = self.font.render("A* - Press 'A'", True, self.TEXT_COLOR)
        self.legend_recursive_maze = self.font.render("Generate maze - Press 'G' or 'V'", True, self.TEXT_COLOR)
        self.legend_graph_size = self.font.render("Change graph size - Press 'S', 'M', 'L'", True, self.TEXT_COLOR)
        self.vis_text_dijkstra = self.font.render("Visualizing Dijkstra:", True, self.TEXT_COLOR)
        self.vis_text_a_star = self.font.render("Visualizing A*:", True, self.TEXT_COLOR)
        self.vis_text_recursive_maze = self.font.render("Creating recursive maze:", True, self.TEXT_COLOR)
        self.vis_text_graph_size = self.font.render("Changing graph size... May take up to 30 seconds",
                                                    True, self.TEXT_COLOR)

        self.dijkstra_finished = False
        self.a_star_finished = False
        self.maze = False   # Used to prevent drawing extra walls during maze
        self.start_or_end_clicked = []   # Used for dragging start and end once algos are finished
        self.wall_nodes = set()     # Used to reinstate walls after deletion for mazes and dragging

    def main(self):     # Put all game specific variables in here so it's easy to restart with main()
        graph = self.set_graph()

        start = None
        end = None

        run = True
        while run:
            self.draw(graph, legend=True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if not pygame.mouse.get_pressed(3)[0]:
                    self.start_or_end_clicked.clear()
                if pygame.mouse.get_pressed(3)[0]:       # LEFT
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    square = graph[row][col]
                    if (self.dijkstra_finished or self.a_star_finished) and start and end:
                        if self.start_or_end_clicked:
                            if square != start and square != end:
                                last_square = self.start_or_end_clicked[0]
                                if last_square == 'start':
                                    if start in self.wall_nodes:
                                        start.set_wall()
                                    else:
                                        start.reset()
                                    start = square
                                    start.set_start()
                                elif last_square == 'end':
                                    if end in self.wall_nodes:
                                        end.set_wall()
                                    else:
                                        end.reset()
                                    end = square
                                    end.set_end()
                                if self.dijkstra_finished:
                                    self.algo_no_vis(graph, start, end, dijkstra=True)
                                elif self.a_star_finished:
                                    self.algo_no_vis(graph, start, end, a_star=True)
                        elif square is start:
                            self.start_or_end_clicked.append('start')
                        elif square is end:
                            self.start_or_end_clicked.append('end')
                    elif not start and square != end:
                        start = square
                        square.set_start()

                        if self.dijkstra_finished and start and end:
                            self.algo_no_vis(graph, start, end, dijkstra=True)
                        if self.a_star_finished and start and end:
                            self.algo_no_vis(graph, start, end, a_star=True)
                    elif not end and square != start:
                        end = square
                        end.set_end()

                        if self.dijkstra_finished and start and end:
                            self.algo_no_vis(graph, start, end, dijkstra=True)
                        if self.a_star_finished and start and end:
                            self.algo_no_vis(graph, start, end, a_star=True)
                    elif square != start and square != end and self.maze is False:
                        square.set_wall()
                        self.wall_nodes.add(square)
                elif pygame.mouse.get_pressed(3)[2]:     # RIGHT
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    square = graph[row][col]

                    if square.is_wall:
                        self.wall_nodes.discard(square)

                    square.reset()
                    if square == start:
                        start = None
                    elif square == end:
                        end = None
                elif pygame.mouse.get_pressed(3)[1]:
                    self.reset_graph(graph)
                    if start:
                        start.reset()
                        start = None
                    if end:
                        end.reset()
                        end = None

                # Run Dijkstra with "D" key on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d and start and end:
                        self.reset_algo(graph)
                        for row in graph:
                            for square in row:
                                square.update_neighbours(graph)

                        self.dijkstra(graph, start, end)
                        self.dijkstra_finished = True

                # Run A* with "A" key on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a and start and end:
                        self.reset_algo(graph)
                        for row in graph:
                            for square in row:
                                square.update_neighbours(graph)

                        self.a_star(graph, start, end)
                        self.a_star_finished = True

                # Draw recursive maze with "G" key on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.reset_graph(graph)
                        self.draw_recursive_maze(graph)
                        self.maze = True
                        start = None
                        end = None

                # Draw recursive maze with NO VISUALIZATIONS with "V" key on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v:
                        self.reset_graph(graph)
                        self.draw_recursive_maze(graph, visualize=False)
                        self.maze = True
                        start = None
                        end = None

                # Redraw small maze with "S" key on keyboard if not currently small
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        if self.rows != 22:
                            graph = self.change_graph_size(22)
                            start = None
                            end = None

                # Redraw medium maze with "M" key on keyboard if not currently medium
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        if self.rows != 46:
                            graph = self.change_graph_size(46)
                            start = None
                            end = None

                # Redraw large maze with "L" key on keyboard if not currently large
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        if self.rows != 95:
                            graph = self.change_graph_size(95)
                            start = None
                            end = None

        pygame.quit()

    def set_graph(self):
        graph = []
        for i in range(self.rows):
            graph.append([])
            for j in range(self.rows):
                square = Square(i, j)
                square.update_values(self.rows, self.square_size)
                graph[i].append(square)

        return graph

    def draw(self, graph, legend=False, display_update=True):
        self.WINDOW.fill(self.DEFAULT_COLOR)
        for row in graph:
            for square in row:
                square.draw_square(self.WINDOW)

        self._draw_lines()
        if legend:
            self._draw_legend()
        if display_update:
            pygame.display.update()

    def _draw_lines(self):
        for i in range(self.rows):
            pygame.draw.line(self.WINDOW, self.LINE_COLOR,
                             (0, i * self.square_size), (self.WIDTH, i * self.square_size))
            pygame.draw.line(self.WINDOW, self.LINE_COLOR,
                             (i * self.square_size, 0), (i * self.square_size, self.WIDTH))

    def _draw_legend(self):
        self.WINDOW.blit(self.legend_add_node, (0, 15*46))
        self.WINDOW.blit(self.legend_remove_node, (0, 15*47))
        self.WINDOW.blit(self.legend_clear_graph, (0, 15*48))
        self.WINDOW.blit(self.legend_dijkstra, (0, 15*49))
        self.WINDOW.blit(self.legend_a_star, (0, 15*50))
        self.WINDOW.blit(self.legend_recursive_maze, (0, 15*51))
        self.WINDOW.blit(self.legend_graph_size, (0, 15*52))

    def draw_vis_text(self, dijkstra=False, a_star=False, recursive_maze=False, graph_size=False):
        if dijkstra:
            self.WINDOW.blit(self.vis_text_dijkstra, (0, 15*52))
        elif a_star:
            self.WINDOW.blit(self.vis_text_a_star, (0, 15*52))
        elif recursive_maze:
            self.WINDOW.blit(self.vis_text_recursive_maze, (0, 15*52))
        elif graph_size:
            self.WINDOW.blit(self.vis_text_graph_size,
                             (self.WIDTH//2 - self.vis_text_graph_size.get_width()//2,
                              self.HEIGHT//2 - self.vis_text_graph_size.get_height()//2))

        pygame.display.update()

    def reset_graph(self, graph):
        self.dijkstra_finished = False
        self.a_star_finished = False
        self.maze = False
        for i in range(self.rows):
            for j in range(self.rows):
                square = graph[i][j]
                square.reset()

    def reset_algo(self, graph):    # Resets algo colors while keeping board obstacles
        self.dijkstra_finished = False
        self.a_star_finished = False
        for i in range(self.rows):
            for j in range(self.rows):
                square = graph[i][j]
                if square.color == self.TURQUOISE or square.color == self.BLUE or square.color == self.YELLOW:
                    square.reset()

    def change_graph_size(self, new_row_size):
        self.draw_vis_text(graph_size=True)

        self.rows = new_row_size
        self.square_size = self.WIDTH / self.rows

        graph = self.set_graph()
        self.draw(graph)

        return graph

    def get_clicked_pos(self, pos):
        y, x = pos
        row = int(y / self.square_size)
        col = int(x / self.square_size)
        return row, col

    def dijkstra(self, graph, start, end, visualize=True):
        queue_pos = 0
        open_set = PriorityQueue()
        open_set.put((0, queue_pos, start))
        open_set_hash = {start}

        g_score = {square: float('inf') for row in graph for square in row}
        g_score[start] = 0
        came_from = {}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            curr_square = open_set.get()[2]
            open_set_hash.remove(curr_square)

            if curr_square == end:
                self.best_path(came_from, end, graph, visualize=visualize)
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

            if visualize:
                self.draw(graph, display_update=False)
                self.draw_vis_text(dijkstra=True)

            if curr_square != start:
                curr_square.set_closed()

        return False

    def a_star(self, graph, start, end, visualize=True):
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
                self.best_path(came_from, end, graph, visualize=visualize)
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

            if visualize:
                self.draw(graph, display_update=False)
                self.draw_vis_text(a_star=True)

            if curr_square != start:
                curr_square.set_closed()

        return False

    @staticmethod
    def heuristic(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)

    def best_path(self, came_from, curr_square, graph, visualize=True):
        while curr_square in came_from:
            curr_square = came_from[curr_square]
            curr_square.set_path()
            if visualize:
                self.draw(graph)

    def algo_no_vis(self, graph, start, end, dijkstra=False, a_star=False):
        if dijkstra:
            self.reset_algo(graph)
            self.dijkstra(graph, start, end, visualize=False)
            self.dijkstra_finished = True
        if a_star:
            self.reset_algo(graph)
            self.a_star(graph, start, end, visualize=False)
            self.a_star_finished = True

    def draw_recursive_maze(self, graph, chamber=None, visualize=True):
        """Implemented following wikipedia guidelines.
        https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_division_method
        Inspired by https://github.com/ChrisKneller/pygame-pathfinder
        """
        division_limit = 3

        if chamber is None:
            chamber_width = len(graph)
            chamber_height = len(graph[1])
            chamber_left = 0
            chamber_top = 0
        else:
            chamber_width = chamber[2]
            chamber_height = chamber[3]
            chamber_left = chamber[0]
            chamber_top = chamber[1]

        x_divide = int(chamber_width/2)
        y_divide = int(chamber_height/2)

        if chamber_width >= division_limit:
            for y in range(chamber_height):
                graph[chamber_left + x_divide][chamber_top + y].set_wall()
                self.wall_nodes.add(graph[chamber_left + x_divide][chamber_top + y])
                if visualize:
                    self.draw(graph, display_update=False)
                    self.draw_vis_text(recursive_maze=True)

        if chamber_height >= division_limit:
            for x in range(chamber_width):
                graph[chamber_left + x][chamber_top + y_divide].set_wall()
                self.wall_nodes.add(graph[chamber_left + x][chamber_top + y_divide])
                if visualize:
                    self.draw(graph, display_update=False)
                    self.draw_vis_text(recursive_maze=True)

        if chamber_width < division_limit and chamber_height < division_limit:
            return

        top_left = (chamber_left, chamber_top, x_divide, y_divide)
        top_right = (chamber_left + x_divide+1, chamber_top, chamber_width - x_divide-1, y_divide)
        bottom_left = (chamber_left, chamber_top + y_divide+1, x_divide, chamber_height - y_divide-1)
        bottom_right = (chamber_left + x_divide+1, chamber_top + y_divide+1,
                        chamber_width - x_divide-1, chamber_height - y_divide-1)

        chambers = (top_left, top_right, bottom_left, bottom_right)

        left = (chamber_left, chamber_top + y_divide, x_divide, 1)
        right = (chamber_left + x_divide+1, chamber_top + y_divide, chamber_width - x_divide-1, 1)
        top = (chamber_left + x_divide, chamber_top, 1, y_divide)
        bottom = (chamber_left + x_divide, chamber_top + y_divide+1, 1, chamber_height - y_divide-1)

        walls = (left, right, top, bottom)

        # Number of gaps to leave after each division into four sub quadrants. See docstring for deeper explanation.
        num_gaps = 3
        gaps_to_offset = [x for x in range(num_gaps - 1, self.rows, num_gaps)]

        for wall in random.sample(walls, num_gaps):
            if wall[3] == 1:
                x = random.randrange(wall[0], wall[0] + wall[2])
                y = wall[1]
                if x in gaps_to_offset and y in gaps_to_offset:
                    if wall[2] == x_divide:
                        x -= 1
                    else:
                        x += 1
                if x >= self.rows:
                    x = self.rows - 1
            else:
                x = wall[0]
                y = random.randrange(wall[1], wall[1] + wall[3])
                if y in gaps_to_offset and x in gaps_to_offset:
                    if wall[3] == y_divide:
                        y -= 1
                    else:
                        y += 1
                if y >= self.rows:
                    y = self.rows - 1
            graph[x][y].reset()
            self.wall_nodes.discard(graph[x][y])
            if visualize:
                self.draw(graph, display_update=False)
                self.draw_vis_text(recursive_maze=True)

        for chamber in chambers:
            if visualize:
                self.draw_recursive_maze(graph, chamber)
            else:
                self.draw_recursive_maze(graph, chamber, visualize=False)

    def get_rows(self):
        return self.rows

    def get_square_size(self):
        return self.square_size


class Square(PathfindingVisualizer):
    def __init__(self, row, col):
        super().__init__()
        self.rows = self.rows
        self.square_size = self.square_size
        self.row = row
        self.col = col
        self.x = self.row * self.square_size
        self.y = self.col * self.square_size
        self.neighbours = []
        self.color = self.DEFAULT_COLOR

    def __lt__(self, other):    # Allows comparison of length of squares
        return False

    def get_pos(self):
        return self.row, self.col

    def update_neighbours(self, graph):
        self.neighbours = []
        if self.row < self.rows-1 and not graph[self.row + 1][self.col].is_wall():  # Down
            self.neighbours.append(graph[self.row+1][self.col])
        if self.row > 0 and not graph[self.row-1][self.col].is_wall():  # UP
            self.neighbours.append(graph[self.row-1][self.col])
        if self.col < self.rows-1 and not graph[self.row][self.col + 1].is_wall():  # RIGHT
            self.neighbours.append(graph[self.row][self.col+1])
        if self.col > 0 and not graph[self.row][self.col-1].is_wall():  # LEFT
            self.neighbours.append(graph[self.row][self.col-1])

    def is_open(self):
        return self.color == self.OPEN_COLOR

    def is_closed(self):
        return self.color == self.CLOSED_COLOR

    def is_start(self):
        return self.color == self.START_COLOR

    def is_mid(self):
        return self.color == self.MID_COLOR

    def is_end(self):
        return self.color == self.END_COLOR

    def is_wall(self):
        return self.color == self.WALL_COLOR

    def is_path(self):
        return self.color == self.PATH_COLOR

    def reset(self):
        self.color = self.DEFAULT_COLOR

    def set_open(self):
        self.color = self.OPEN_COLOR

    def set_closed(self):
        self.color = self.CLOSED_COLOR

    def set_start(self):
        self.color = self.START_COLOR

    def set_mid(self):
        self.color = self.MID_COLOR

    def set_end(self):
        self.color = self.END_COLOR

    def set_wall(self):
        self.color = self.WALL_COLOR

    def set_path(self):
        self.color = self.PATH_COLOR

    def draw_square(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, int(self.square_size), int(self.square_size)))

    def update_values(self, rows, square_size):
        self.rows = rows
        self.square_size = square_size
        self.x = self.row * self.square_size
        self.y = self.col * self.square_size
