import pygame
from queue import PriorityQueue
import random
import time


# noinspection PyUnresolvedReferences, PyTypeChecker
# PyCharm bug, doesn't realize that square is a Node class object. Above comment removes it.
class PathfindingVisualizer:
    def __init__(self):
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 879
        self.WIDTH = 800
        self.HEIGHT = 800
        self.WINDOW = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.LEGEND_AREA = pygame.Rect(0, self.HEIGHT, self.WINDOW_WIDTH, self.WINDOW_HEIGHT - self.HEIGHT)
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
        self.LEGEND_AREA_COLOR = self.GREY
        self.LINE_COLOR = self.GREY
        self.OPEN_COLOR = self.TURQUOISE
        self.CLOSED_COLOR = self.BLUE
        self.START_COLOR = self.GREEN
        self.MID_COLOR = self.ORANGE
        self.END_COLOR = self.RED
        self.WALL_COLOR = self.BLACK
        self.PATH_COLOR = self.YELLOW
        self.LEGEND_COLOR = self.BLACK
        self.VIS_COLOR = self.RED

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 12)

        self.legend_add_node = self.font.render("Left Click - Add Node (Start -> End -> Walls)",
                                                True, self.LEGEND_COLOR)
        self.legend_add_mid_node = self.font.render("Middle Click - Add mid node", True, self.LEGEND_COLOR)
        self.legend_remove_node = self.font.render("Right Click - Remove Node",
                                                   True, self.LEGEND_COLOR)
        self.legend_clear_graph = self.font.render("Press 'SPACE' - Clear graph", True, self.LEGEND_COLOR)
        self.legend_graph_size = self.font.render("Press 'S', 'M', 'L' - Change graph size", True, self.LEGEND_COLOR)
        self.legend_dijkstra = self.font.render("Dijkstra - Press 'D'", True, self.LEGEND_COLOR)
        self.legend_a_star = self.font.render("A* - Press 'A'", True, self.LEGEND_COLOR)
        self.legend_bi_dijkstra = self.font.render("Bi-directional Dijkstra - Press 'B'", True, self.LEGEND_COLOR)
        self.legend_recursive_maze = self.font.render("Generate maze - Press 'G'", True, self.LEGEND_COLOR)
        self.legend_instant_recursive_maze = self.font.render("Generate maze (Instantly) - Press 'I'",
                                                              True, self.LEGEND_COLOR)

        self.vis_text_dijkstra = self.font.render("Visualizing Dijkstra...", True, self.VIS_COLOR)
        self.vis_text_a_star = self.font.render("Visualizing A*...", True, self.VIS_COLOR)
        self.vis_text_bi_dijkstra = self.font.render("Visualizing Bi-directional Dijkstra...", True, self.VIS_COLOR)
        self.vis_text_best_path = self.font.render("Laying best path...", True, self.VIS_COLOR)
        self.vis_text_recursive_maze = self.font.render("Generating recursive maze...", True, self.VIS_COLOR)
        self.vis_text_graph_size = self.font.render("Changing graph size... May take up to 30 seconds",
                                                    True, self.VIS_COLOR)

        self.dijkstra_finished = False
        self.a_star_finished = False
        self.bi_dijkstra_finished = False
        self.maze = False   # Used to prevent drawing extra walls during maze
        self.ordinal_node_clicked = []   # Used for dragging start and end once algos are finished. Length is 0 or 1.
        self.wall_nodes = set()     # Used to reinstate walls after deletion for mazes and dragging

    def main(self):     # Put all game specific variables in here so it's easy to restart with main()
        graph = self.set_graph()

        start = None
        mid = None
        end = None

        run = True
        while run:
            self.draw(graph, legend=True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                # Used to know if no longer dragging ordinal node after algo completion
                if not pygame.mouse.get_pressed(3)[0]:
                    self.ordinal_node_clicked.clear()

                # LEFT CLICK within graph
                if pygame.mouse.get_pressed(3)[0] and pygame.mouse.get_pos()[1] < self.HEIGHT:
                    # Get square clicked
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    square = graph[row][col]

                    if (self.dijkstra_finished or self.a_star_finished) and start and end:
                        if self.ordinal_node_clicked:
                            if square != start and square != mid and square != end:
                                last_square = self.ordinal_node_clicked[0]

                                if last_square == 'start':
                                    if start in self.wall_nodes:
                                        start.set_wall()
                                    else:
                                        start.reset()
                                    start = square
                                    square.set_start()
                                elif last_square == 'mid':
                                    if mid in self.wall_nodes:
                                        mid.set_wall()
                                    else:
                                        mid.reset()
                                    mid = square
                                    square.set_mid()
                                elif last_square == 'end':
                                    if end in self.wall_nodes:
                                        end.set_wall()
                                    else:
                                        end.reset()
                                    end = square
                                    square.set_end()

                                if self.dijkstra_finished:
                                    if mid:
                                        self.start_mid_end(graph, start, mid, end, dijkstra=True, visualize=False)
                                    else:
                                        self.algo_no_vis(graph, start, end, dijkstra=True)
                                elif self.a_star_finished:
                                    if mid:
                                        self.start_mid_end(graph, start, mid, end, a_star=True, visualize=False)
                                    else:
                                        self.algo_no_vis(graph, start, end, a_star=True)

                        elif square is start:
                            self.ordinal_node_clicked.append('start')
                        elif square is mid:
                            self.ordinal_node_clicked.append('mid')
                        elif square is end:
                            self.ordinal_node_clicked.append('end')

                    elif not start and square != mid and square != end:
                        start = square
                        square.set_start()

                        if self.dijkstra_finished and start and end:
                            self.algo_no_vis(graph, start, end, dijkstra=True)
                        if self.a_star_finished and start and end:
                            self.algo_no_vis(graph, start, end, a_star=True)
                    elif not end and square != start and square != mid:
                        end = square
                        square.set_end()

                        if self.dijkstra_finished and start and end:
                            self.algo_no_vis(graph, start, end, dijkstra=True)
                        if self.a_star_finished and start and end:
                            self.algo_no_vis(graph, start, end, a_star=True)
                    elif square != start and square != mid and square != end and self.maze is False:
                        square.set_wall()
                        self.wall_nodes.add(square)

                # RIGHT CLICK within graph
                elif pygame.mouse.get_pressed(3)[2] and pygame.mouse.get_pos()[1] < self.HEIGHT:
                    # Get square clicked
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    square = graph[row][col]

                    # If square to remove is wall, need to remove it from wall_node to retain accuracy
                    if square.is_wall():
                        self.wall_nodes.discard(square)

                    # Reset square and ordinal node if it was any
                    square.reset()
                    if square == start:
                        start = None
                    elif square == mid:
                        mid = None
                    elif square == end:
                        end = None

                # MIDDLE CLICK within graph
                elif pygame.mouse.get_pressed(3)[1] and pygame.mouse.get_pos()[1] < self.HEIGHT:
                    # Get square clicked
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    square = graph[row][col]

                    # Set square to mid if no square is already mid
                    if not mid:
                        if square != start and square != end:
                            mid = square
                            square.set_mid()

                # Reset graph with "SPACE" on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_graph(graph)
                        if start:
                            start = None
                        if mid:
                            mid = None
                        if end:
                            end = None

                # Run Dijkstra with "D" key on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d and start and end:
                        self.reset_algo(graph)
                        for row in graph:
                            for square in row:
                                square.update_neighbours(graph)

                        self.dijkstra_finished = True

                        if mid:
                            self.start_mid_end(graph, start, mid, end, dijkstra=True)
                        else:
                            self.dijkstra(graph, start, end)

                # Run A* with "A" key on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a and start and end:
                        self.reset_algo(graph)
                        for row in graph:
                            for square in row:
                                square.update_neighbours(graph)

                        self.a_star_finished = True

                        if mid:
                            self.start_mid_end(graph, start, mid, end, a_star=True)
                        else:
                            self.a_star(graph, start, end)

                # Draw recursive maze with "G" key on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.reset_graph(graph)
                        self.draw_recursive_maze(graph)
                        self.maze = True
                        start = None
                        mid = None
                        end = None

                # Draw recursive maze with NO VISUALIZATIONS with "I" key on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        self.reset_graph(graph)
                        self.draw_recursive_maze(graph, visualize=False)
                        self.maze = True
                        start = None
                        mid = None
                        end = None

                # Redraw small maze with "S" key on keyboard if not currently small
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        if self.rows != 22:
                            graph = self.change_graph_size(22)
                            start = None
                            mid = None
                            end = None

                # Redraw medium maze with "M" key on keyboard if not currently medium
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        if self.rows != 46:
                            graph = self.change_graph_size(46)
                            start = None
                            mid = None
                            end = None

                # Redraw large maze with "L" key on keyboard if not currently large
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        if self.rows != 95:
                            graph = self.change_graph_size(95)
                            start = None
                            mid = None
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
        self.WINDOW.fill(self.LEGEND_AREA_COLOR, self.LEGEND_AREA)
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
        # Left legend
        self.WINDOW.blit(self.legend_add_node, (2, 15*53.1 + 3))
        self.WINDOW.blit(self.legend_add_mid_node, (2, 15*54.1 + 3))
        self.WINDOW.blit(self.legend_remove_node, (2, 15*55.1 + 3))
        self.WINDOW.blit(self.legend_clear_graph, (2, 15*56.1 + 3))
        self.WINDOW.blit(self.legend_graph_size, (2, 15*57.1 + 3))

        # Right legend
        self.WINDOW.blit(self.legend_dijkstra, (self.WIDTH - self.legend_dijkstra.get_width()-2, 15*53.1 + 3))
        self.WINDOW.blit(self.legend_a_star, (self.WIDTH - self.legend_a_star.get_width()-2, 15*54.1 + 3))
        self.WINDOW.blit(self.legend_bi_dijkstra, (self.WIDTH - self.legend_bi_dijkstra.get_width()-2, 15*55.1 + 3))
        self.WINDOW.blit(self.legend_recursive_maze,
                         (self.WIDTH - self.legend_recursive_maze.get_width()-2, 15*56.1 + 3))
        self.WINDOW.blit(self.legend_instant_recursive_maze,
                         (self.WIDTH - self.legend_instant_recursive_maze.get_width()-2, 15*57.1 + 3))

    def draw_vis_text(self, dijkstra=False, a_star=False, bi_dijkstra=False,
                      best_path=False, recursive_maze=False, graph_size=False):

        center_graph = self.HEIGHT//2
        center_legend_area = self.HEIGHT + (self.WINDOW_HEIGHT - self.HEIGHT)//2
        if dijkstra:
            self.WINDOW.blit(self.vis_text_dijkstra,
                             (self.WIDTH//2 - self.vis_text_dijkstra.get_width()//2,
                              center_legend_area - self.vis_text_dijkstra.get_height()//2))
        elif a_star:
            self.WINDOW.blit(self.vis_text_a_star,
                             (self.WIDTH//2 - self.vis_text_a_star.get_width()//2,
                              center_legend_area - self.vis_text_a_star.get_height()//2))
        elif bi_dijkstra:
            self.WINDOW.blit(self.vis_text_bi_dijkstra,
                             (self.WIDTH//2 - self.vis_text_bi_dijkstra.get_width()//2,
                              center_legend_area - self.vis_text_bi_dijkstra.get_height()//2))
        elif best_path:
            self.WINDOW.blit(self.vis_text_best_path,
                             (self.WIDTH // 2 - self.vis_text_best_path.get_width() // 2,
                              center_legend_area - self.vis_text_best_path.get_height() // 2))
        elif recursive_maze:
            self.WINDOW.blit(self.vis_text_recursive_maze,
                             (self.WIDTH//2 - self.vis_text_recursive_maze.get_width()//2,
                              center_legend_area - self.vis_text_recursive_maze.get_height()//2))
        elif graph_size:
            self.WINDOW.blit(self.vis_text_graph_size,
                             (self.WIDTH//2 - self.vis_text_graph_size.get_width()//2,
                              center_graph - self.vis_text_graph_size.get_height()//2))

        pygame.display.update()

    def reset_graph(self, graph):
        self.dijkstra_finished = False
        self.a_star_finished = False
        self.maze = False
        for i in range(self.rows):
            for j in range(self.rows):
                square = graph[i][j]
                square.reset()

    # Resets algo colors while keeping board obstacles
    def reset_algo(self, graph):
        self.dijkstra_finished = False
        self.a_star_finished = False
        for i in range(self.rows):
            for j in range(self.rows):
                square = graph[i][j]
                if square.is_open() or square.is_closed() or square.is_path():
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

    def dijkstra(self, graph, start, end, ignore_node=None, draw_best_path=True, visualize=True):
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
                if draw_best_path:
                    self.best_path(graph, came_from, end, visualize=visualize)
                    return True

                return came_from

            for nei in curr_square.neighbours:
                temp_g_score = g_score[curr_square] + 1

                if temp_g_score < g_score[nei]:
                    came_from[nei] = curr_square
                    g_score[nei] = temp_g_score
                    if nei not in open_set_hash:
                        queue_pos += 1
                        open_set.put((g_score[nei], queue_pos, nei))
                        open_set_hash.add(nei)
                        if nei != end and nei.color != self.CLOSED_COLOR and nei != ignore_node:
                            nei.set_open()

            if visualize and not curr_square.is_closed():
                self.draw(graph, display_update=False)
                self.draw_vis_text(dijkstra=True)

            if curr_square != start and curr_square != ignore_node:
                curr_square.set_closed()

        return False

    def a_star(self, graph, start, end, ignore_node=None, draw_best_path=True, visualize=True):
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
                if draw_best_path:
                    self.best_path(graph, came_from, end, visualize=visualize)
                    return True

                return came_from

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
                        if nei != end and nei.color != self.CLOSED_COLOR and nei != ignore_node:
                            nei.set_open()

            if visualize and not curr_square.is_closed():
                self.draw(graph, display_update=False)
                self.draw_vis_text(a_star=True)

            if curr_square != start and curr_square != ignore_node:
                curr_square.set_closed()

        return False

    @staticmethod
    def heuristic(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)

    def start_mid_end(self, graph, start, mid, end, dijkstra=False, a_star=False, visualize=True):
        """Used if algos need to reach mid node first"""
        if dijkstra:
            if visualize:
                start_to_mid = self.dijkstra(graph, start, mid, ignore_node=end, draw_best_path=False)
                mid_to_end = self.dijkstra(graph, mid, end, ignore_node=start, draw_best_path=False)
            else:
                start_to_mid = self.algo_no_vis(graph, start, mid, dijkstra=True, ignore_node=end, draw_best_path=False)
                mid_to_end = self.algo_no_vis(graph, mid, end, dijkstra=True, ignore_node=start,
                                              draw_best_path=False, reset=False)
                start.set_start(), mid.set_mid(), end.set_end()  # Fixes nodes disappearing when dragging

            self.best_path(graph, start_to_mid, mid, visualize=visualize)
            self.best_path(graph, mid_to_end, end, visualize=visualize)
        if a_star:
            if visualize:
                start_to_mid = self.a_star(graph, start, mid, ignore_node=end, draw_best_path=False)
                mid_to_end = self.a_star(graph, mid, end, ignore_node=start, draw_best_path=False)
            else:
                start_to_mid = self.algo_no_vis(graph, start, mid, a_star=True, ignore_node=end, draw_best_path=False)
                mid_to_end = self.algo_no_vis(graph, mid, end, a_star=True, ignore_node=start,
                                              draw_best_path=False, reset=False)
                start.set_start(), mid.set_mid(), end.set_end()  # Fixes nodes disappearing when dragging

            self.best_path(graph, start_to_mid, mid, visualize=visualize)
            self.best_path(graph, mid_to_end, end, visualize=visualize)

    # Skip steps to end when visualizing algo. Used when dragging ordinal node once finished
    def algo_no_vis(self, graph, start, end, dijkstra=False, a_star=False,
                    ignore_node=None, draw_best_path=True, reset=True):
        if dijkstra:
            if reset:   # Used to not reset start -> mid visualizations if going from mid -> end
                self.reset_algo(graph)
            self.dijkstra_finished = True

            # Separates calling algo_no_vis with mid node or not
            if draw_best_path:
                self.dijkstra(graph, start, end, visualize=False)
                start.set_start()  # Fixes start disappearing when dragging
            else:
                return self.dijkstra(graph, start, end, ignore_node=ignore_node, draw_best_path=False, visualize=False)

        if a_star:
            if reset:   # Used to not reset start -> mid visualizations if going from mid -> end
                self.reset_algo(graph)
            self.a_star_finished = True

            # Separates calling algo_no_vis with mid node or not
            if draw_best_path:
                self.a_star(graph, start, end, visualize=False)
                start.set_start()  # Fixes start disappearing when dragging
            else:
                return self.a_star(graph, start, end, ignore_node=ignore_node, draw_best_path=False, visualize=False)

    def best_path(self, graph, came_from, curr_square, meet_node=None, visualize=True):
        if isinstance(came_from, bool):
            return

        # Path reconstruction if bidirectional
        if meet_node:
            if visualize:
                time.sleep(0.001)
                self.draw(graph, display_update=False)
                self.draw_vis_text(best_path=True)

        # Path reconstruction if no mid node or not bidirectional
        else:
            path = []

            while curr_square in came_from:
                curr_square = came_from[curr_square]
                path.append(curr_square)

            for square in path[len(path)-2::-1]:
                square.set_path()
                if visualize:
                    time.sleep(0.0025)
                    self.draw(graph, display_update=False)
                    self.draw_vis_text(best_path=True)

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

    def is_empty(self):
        return self.color == self.DEFAULT_COLOR

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
