import pygame
from queue import PriorityQueue
import random
import time

"""Visualizer for major pathfinding algorithms such as Dijkstra, A*, and my own creation Bi-directional Dijkstra.
Node and square used interchangeably.
"""


# noinspection PyUnresolvedReferences, PyTypeChecker
# PyCharm bug, doesn't realize that square is a Node class object. Above comment removes it.
class PathfindingVisualizer:
    """Where all the algorithms and operations reside. Call main() to run."""
    def __init__(self):
        """Creates the window size, graph size, colors, text, and many more variables"""

        # Defining window properties as well as graph size
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 879
        self.WIDTH = 800
        self.HEIGHT = 800
        self.WINDOW = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.LEGEND_AREA = pygame.Rect(0, self.HEIGHT, self.WINDOW_WIDTH, self.WINDOW_HEIGHT - self.HEIGHT)
        pygame.display.set_caption("Pathfinding Visualizer - github.com/ShanaryS/algorithm-visualizer")

        # Recursive division only works on certain row values. 22,23,46,47,94,95.
        self.rows = 46  # Number of rows get changed to change the size of graph, viable values for maze above.
        # self.COLS = 50        # Use to make graph none square but requires a lot of reworking
        self.square_size = self.WIDTH / self.rows   # The square size on the graph

        # Defining all colors that the program may use. Everything from node color to text color
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.ORANGE = (255, 165, 0)
        self.PURPLE = (128, 0, 128)
        self.TURQUOISE = (64, 224, 208)
        self.TURQUOISE_ALT = (64, 223, 208)
        self.GREY = (128, 128, 128)

        # Assigning colors to different conditions to allow easy updating and readability.
        self.DEFAULT_COLOR = self.WHITE
        self.LEGEND_AREA_COLOR = self.GREY
        self.LINE_COLOR = self.GREY
        self.OPEN_COLOR = self.TURQUOISE
        self.OPEN_ALT_COLOR = self.TURQUOISE_ALT
        self.CLOSED_COLOR = self.BLUE
        self.START_COLOR = self.GREEN
        self.MID_COLOR = self.ORANGE
        self.END_COLOR = self.RED
        self.WALL_COLOR = self.BLACK
        self.PATH_COLOR = self.YELLOW
        self.LEGEND_COLOR = self.BLACK
        self.VIS_COLOR = self.RED

        # Creates the text needed for legend and when visualizing
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

        # Extra variables needed in scope of entire class for different functions.
        self.dijkstra_finished = False
        self.a_star_finished = False
        self.bi_dijkstra_finished = False
        self.maze = False   # Used to prevent drawing extra walls during maze
        self.ordinal_node_clicked = []   # Used for dragging start and end once algos are finished. Length is 0 or 1.
        self.wall_nodes = set()     # Used to reinstate walls after deletion for mazes and dragging
        self.best_path_sleep = 0.0025

    def main(self):     # Put all game specific variables in here so it's easy to restart with main()
        """The pygame logic loop. This runs forever until exited. This is what should be called to run program."""
        graph = self.set_graph()

        # Defining ordinal nodes to be used within the loop in various places
        start = None
        mid = None
        end = None

        run = True
        while run:
            self.draw(graph, legend=True)

            # Allow clicking the "X" on the pygame window to end the program
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                # Used to know if no longer dragging ordinal node after algo completion
                if not pygame.mouse.get_pressed(3)[0]:
                    self.ordinal_node_clicked.clear()

                # LEFT MOUSE CLICK. self.HEIGHT condition prevents out of bound when clicking on legend.
                if pygame.mouse.get_pressed(3)[0] and pygame.mouse.get_pos()[1] < self.HEIGHT:

                    # Get square clicked
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    square = graph[row][col]

                    # Checks if algo is completed, used for dragging algo
                    if (self.dijkstra_finished or self.a_star_finished or self.bi_dijkstra_finished) and start and end:

                        # Checks if ordinal node is being dragged
                        if self.ordinal_node_clicked:

                            # Checks if the mouse is currently on an ordinal node, no need to update anything
                            if square != start and square != mid and square != end:
                                last_square = self.ordinal_node_clicked[0]  # Used to move ordinal node to new pos

                                # Checks if ordinal node was previously a wall to reinstate it after moving, else reset
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

                                # Runs the algo again instantly with no visualizations, handles whether mid exists
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
                                elif self.bi_dijkstra_finished:
                                    if mid:
                                        self.start_mid_end(graph, start, mid, end, bi_dijkstra=True, visualize=False)
                                    else:
                                        self.algo_no_vis(graph, start, end, bi_dijkstra=True)

                        # If ordinal node is not being dragged, prepare it to
                        elif square is start:
                            self.ordinal_node_clicked.append('start')
                        elif square is mid:
                            self.ordinal_node_clicked.append('mid')
                        elif square is end:
                            self.ordinal_node_clicked.append('end')

                    # If start node does not exist, create it. If not currently ordinal node.
                    elif not start and square != mid and square != end:
                        start = square
                        square.set_start()

                        # Handles removing and adding start manually instead of dragging on algo completion.
                        if self.dijkstra_finished and start and end:
                            self.algo_no_vis(graph, start, end, dijkstra=True)
                        elif self.a_star_finished and start and end:
                            self.algo_no_vis(graph, start, end, a_star=True)
                        elif self.bi_dijkstra_finished and start and end:
                            self.algo_no_vis(graph, start, end, bi_dijkstra=True)

                    # If end node does not exist, and start node does exist, create end node.
                    # If not currently ordinal node.
                    elif not end and square != start and square != mid:
                        end = square
                        square.set_end()

                        # Handles removing and adding end manually instead of dragging on algo completion.
                        if self.dijkstra_finished and start and end:
                            self.algo_no_vis(graph, start, end, dijkstra=True)
                        elif self.a_star_finished and start and end:
                            self.algo_no_vis(graph, start, end, a_star=True)
                        elif self.bi_dijkstra_finished and start and end:
                            self.algo_no_vis(graph, start, end, bi_dijkstra=True)

                    # If start and end node exists, create wall. If not currently ordinal node.
                    # Saves pos of wall to be able to reinstate it after dragging ordinal node past it.
                    elif square != start and square != mid and square != end and self.maze is False:
                        square.set_wall()
                        self.wall_nodes.add(square)

                # RIGHT MOUSE CLICK. self.HEIGHT condition prevents out of bound when clicking on legend.
                elif pygame.mouse.get_pressed(3)[2] and pygame.mouse.get_pos()[1] < self.HEIGHT:

                    # Get square clicked
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    square = graph[row][col]

                    # If square to remove is wall, need to remove it from wall_node as well to retain accuracy
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

                # MIDDLE MOUSE CLICK. self.HEIGHT condition prevents out of bound when clicking on legend.
                elif pygame.mouse.get_pressed(3)[1] and pygame.mouse.get_pos()[1] < self.HEIGHT:

                    # Get square clicked
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    square = graph[row][col]

                    # Set square to mid if no square is already mid, and not currently ordinal node.
                    if not mid:
                        if square != start and square != end:
                            mid = square
                            square.set_mid()

                            # Handles removing and adding mid manually instead of dragging on algo completion.
                            if self.dijkstra_finished and start and mid and end:
                                self.start_mid_end(graph, start, mid, end, dijkstra=True, visualize=False)
                            elif self.a_star_finished and start and mid and end:
                                self.start_mid_end(graph, start, mid, end, a_star=True, visualize=False)
                            elif self.bi_dijkstra_finished and start and mid and end:
                                self.start_mid_end(graph, start, mid, end, bi_dijkstra=True, visualize=False)

                # Reset graph with "SPACE" on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_graph(graph)

                        # Reset ordinal nodes as it cannot be in reset_graph due to scope
                        if start:
                            start = None
                        if mid:
                            mid = None
                        if end:
                            end = None

                # Run Dijkstra with "D" key on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d and start and end:

                        # Resets algo visualizations without removing ordinal nodes or walls
                        self.reset_algo(graph)

                        # Updates neighbours in case anything has changed
                        for row in graph:
                            for square in row:
                                square.update_neighbours(graph)

                        # Necessary to for dragging nodes on completion
                        self.dijkstra_finished = True

                        # Handles whether or not mid exists
                        if mid:
                            self.start_mid_end(graph, start, mid, end, dijkstra=True)
                        else:
                            self.dijkstra(graph, start, end)

                # Run A* with "A" key on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a and start and end:

                        # Resets algo visualizations without removing ordinal nodes or walls
                        self.reset_algo(graph)

                        # Updates neighbours in case anything has changed
                        for row in graph:
                            for square in row:
                                square.update_neighbours(graph)

                        # Necessary to for dragging nodes on completion
                        self.a_star_finished = True

                        # Handles whether or not mid exists
                        if mid:
                            self.start_mid_end(graph, start, mid, end, a_star=True)
                        else:
                            self.a_star(graph, start, end)

                # Run Bi-directional Dijkstra with "B" key on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b and start and end:

                        # Resets algo visualizations without removing ordinal nodes or walls
                        self.reset_algo(graph)

                        # Updates neighbours in case anything has changed
                        for row in graph:
                            for square in row:
                                square.update_neighbours(graph)

                        # Necessary to for dragging nodes on completion
                        self.bi_dijkstra_finished = True

                        # Handles whether or not mid exists
                        if mid:
                            self.start_mid_end(graph, start, mid, end, bi_dijkstra=True)
                        else:
                            self.bi_dijkstra(graph, start, end)

                # Draw recursive maze with "G" key on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:

                        # Resets entire graph to prevent any unintended behaviour
                        self.reset_graph(graph)

                        # Draw maze
                        self.draw_recursive_maze(graph)

                        # Necessary for handling dragging over barriers if in maze
                        self.maze = True

                        # Reset ordinal nodes as it cannot be in reset_graph due to scope
                        start = None
                        mid = None
                        end = None

                # Draw recursive maze with NO VISUALIZATIONS with "I" key on keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:

                        # Resets entire graph to prevent any unintended behaviour
                        self.reset_graph(graph)

                        # Draw maze instantly with no visualizations
                        self.draw_recursive_maze(graph, visualize=False)

                        # Necessary for handling dragging over barriers if in maze
                        self.maze = True

                        # Reset ordinal nodes as it cannot be in reset_graph due to scope
                        start = None
                        mid = None
                        end = None

                # Redraw small maze with "S" key on keyboard if not currently small
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:

                        # If maze is currently small, no need to redraw
                        if self.rows != 22:

                            # Changes graph size to small
                            graph = self.change_graph_size(22)

                            # Reset ordinal nodes as it cannot be in reset_graph due to scope
                            start = None
                            mid = None
                            end = None

                # Redraw medium maze with "M" key on keyboard if not currently medium
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:

                        # If maze is already medium, no need to redraw
                        if self.rows != 46:

                            # Changes graph size to medium
                            graph = self.change_graph_size(46)

                            # Reset ordinal nodes as it cannot be in reset_graph due to scope
                            start = None
                            mid = None
                            end = None

                # Redraw large maze with "L" key on keyboard if not currently large
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:

                        # If maze is already large, no need to redraw
                        if self.rows != 95:

                            # Changes graph size to large
                            graph = self.change_graph_size(95)

                            # Reset ordinal nodes as it cannot be in reset_graph due to scope
                            start = None
                            mid = None
                            end = None

        # Only reached if while loop ends, which happens if window is closed. Program terminates.
        pygame.quit()

    def set_graph(self):
        """Creates the graph object that stores the location of all the squares"""
        graph = []
        for i in range(self.rows):
            graph.append([])
            for j in range(self.rows):
                # Uses Square class to create square object with necessary attributes
                square = Square(i, j)

                # Necessary for when changing graph size
                square.update_values(self.rows, self.square_size)

                graph[i].append(square)

        return graph

    def draw(self, graph, legend=False, display_update=True):
        """Main function to update the window. Called by all operations that updates the window."""

        # Sets background of graph to white and legend to grey
        self.WINDOW.fill(self.DEFAULT_COLOR)
        self.WINDOW.fill(self.LEGEND_AREA_COLOR, self.LEGEND_AREA)

        # If colors of square were updated, reflected here
        for row in graph:
            for square in row:
                square.draw_square(self.WINDOW)

        # Draws the horizontal and vertical lines on the graph
        self._draw_lines()

        # Legend is only shown if graph can be interacted with
        if legend:
            self._draw_legend()

        # Display may not want to update display immediately before doing other operations
        if display_update:
            pygame.display.update()

    def _draw_lines(self):
        """Helper function to define the properties of the horizontal and vertical graph lines"""
        for i in range(self.rows):
            pygame.draw.line(self.WINDOW, self.LINE_COLOR,
                             (0, i * self.square_size), (self.WIDTH, i * self.square_size))
            pygame.draw.line(self.WINDOW, self.LINE_COLOR,
                             (i * self.square_size, 0), (i * self.square_size, self.WIDTH))

    def _draw_legend(self):
        """Helper function to define the location of the legend"""
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
        """Special text indicating some operation is being performed. No inputs are registered."""

        # Defines the center of the graph and legend for text placement
        center_graph = self.HEIGHT//2
        center_legend_area = self.HEIGHT + (self.WINDOW_HEIGHT - self.HEIGHT)//2

        # Text to be shown depending on operation
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

        # Always called after draw. In that scenario draw won't update display so this will
        pygame.display.update()

    def reset_graph(self, graph):
        """Resets entire graph removing every square"""

        # Need to update these values
        self.dijkstra_finished = False
        self.a_star_finished = False
        self.bi_dijkstra_finished = False
        self.maze = False

        # Resets each square
        for i in range(self.rows):
            for j in range(self.rows):
                square = graph[i][j]
                square.reset()

    def reset_algo(self, graph):
        """Resets algo colors while keeping ordinal nodes and walls"""

        # Need to update these values
        self.dijkstra_finished = False
        self.a_star_finished = False
        self.bi_dijkstra_finished = False

        # Resets only certain colors
        for i in range(self.rows):
            for j in range(self.rows):
                square = graph[i][j]
                if square.is_open() or square.is_open_alt() or square.is_closed() or square.is_path():
                    square.reset()

    def change_graph_size(self, new_row_size):
        """Changes graph size and updates squares and their locations as well.
        Restricted to certain sizes as recursive maze breaks otherwise
        """

        # Displays text that size is changing
        self.draw_vis_text(graph_size=True)

        # Updates rows and square size with new values
        self.rows = new_row_size
        self.square_size = self.WIDTH / self.rows

        # Recreates graph with new values
        graph = self.set_graph()
        self.draw(graph)

        return graph

    def get_clicked_pos(self, pos):
        """Turns the location data of the mouse into location of squares"""
        y, x = pos
        row = int(y / self.square_size)
        col = int(x / self.square_size)
        return row, col

    def dijkstra(self, graph, start, end, ignore_node=None, draw_best_path=True, visualize=True):
        """Code for the dijkstra algorithm"""

        # Used to determine the order of squares to check. Order of args helper decide the priority.
        queue_pos = 0
        open_set = PriorityQueue()
        open_set.put((0, queue_pos, start))
        open_set_hash = {start}

        # Determine what is the best square to check
        g_score = {square: float('inf') for row in graph for square in row}
        g_score[start] = 0

        # Keeps track of next node for every node in graph. A linked list basically.
        came_from = {}

        # Continues until every node has been checked or best path found
        while not open_set.empty():

            # If uses closes window the program terminates
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Gets the square currently being checked
            curr_square = open_set.get()[2]
            open_set_hash.remove(curr_square)

            # Terminates if found the best path
            if curr_square == end:
                if draw_best_path:
                    self.best_path(graph, came_from, end, visualize=visualize)
                    return True

                return came_from

            # Decides the order of neighbours to check
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

            # Only visualize if called. Checks if square is closed to not repeat when mid node included.
            if visualize and not curr_square.is_closed():
                self.draw(graph, display_update=False)
                self.draw_vis_text(dijkstra=True)

            # Sets square to closed after finished checking
            if curr_square != start and curr_square != ignore_node:
                curr_square.set_closed()

        return False

    def a_star(self, graph, start, end, ignore_node=None, draw_best_path=True, visualize=True):
        """Code for the A* algorithm"""

        # Used to determine the order of squares to check. Order of args helper decide the priority.
        queue_pos = 0
        open_set = PriorityQueue()
        open_set.put((0, queue_pos, start))
        open_set_hash = {start}

        # Determine what is the best square to check
        g_score = {square: float('inf') for row in graph for square in row}
        g_score[start] = 0
        f_score = {square: float('inf') for row in graph for square in row}
        f_score[start] = self.heuristic(start.get_pos(), end.get_pos())

        # Keeps track of next node for every node in graph. A linked list basically.
        came_from = {}

        # Continues until every node has been checked or best path found
        while not open_set.empty():

            # If uses closes window the program terminates
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Gets the square currently being checked
            curr_square = open_set.get()[2]
            open_set_hash.remove(curr_square)

            # Terminates if found the best path
            if curr_square == end:
                if draw_best_path:
                    self.best_path(graph, came_from, end, visualize=visualize)
                    return True

                return came_from

            # Decides the order of neighbours to check
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

            # Only visualize if called. Checks if square is closed to not repeat when mid node included.
            if visualize and not curr_square.is_closed():
                self.draw(graph, display_update=False)
                self.draw_vis_text(a_star=True)

            # Sets square to closed after finished checking
            if curr_square != start and curr_square != ignore_node:
                curr_square.set_closed()

        return False

    @staticmethod
    def heuristic(pos1, pos2):
        """Used by A* to prioritize traveling towards next node"""
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)

    def bi_dijkstra(self, graph, start, end, ignore_node=None, draw_best_path=True, visualize=True):
        """Code for Bi-directional Dijkstra algorithm. Custom algorithm made by me."""

        # Used to determine the order of squares to check. Order of args helper decide the priority.
        queue_pos = 0
        open_set = PriorityQueue()
        open_set_hash = {start, end}
        open_set.put((0, queue_pos, start, 'start'))
        queue_pos += 1
        open_set.put((0, queue_pos, end, 'end'))

        # Determine what is the best square to check
        g_score = {square: float('inf') for row in graph for square in row}
        g_score[start] = 0
        g_score[end] = 0

        # Keeps track of next node for every node in graph. A linked list basically.
        came_from_start = {}
        came_from_end = {}

        # Continues until every node has been checked or best path found
        while not open_set.empty():

            # If uses closes window the program terminates
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Gets the square currently being checked
            temp = open_set.get()
            curr_square = temp[2]
            open_set_hash.remove(curr_square)

            # Terminates if found the best path
            for nei in curr_square.neighbours:
                if curr_square.is_open() and nei.is_open_alt():
                    if draw_best_path:
                        self.best_path_bi_dijkstra(graph, came_from_start, came_from_end,
                                                   curr_square, nei, visualize=visualize)
                        return True

                    return came_from_start, came_from_end, curr_square, nei

                elif curr_square.is_open_alt() and nei.is_open():
                    if draw_best_path:
                        self.best_path_bi_dijkstra(graph, came_from_start, came_from_end,
                                                   nei, curr_square, visualize=visualize)
                        return True

                    return came_from_start, came_from_end, nei, curr_square

            # Decides the order of neighbours to check for both swarms.
            if temp[3] == 'start':
                for nei in curr_square.neighbours:
                    temp_g_score = g_score[curr_square] + 1

                    if temp_g_score < g_score[nei]:
                        came_from_start[nei] = curr_square
                        g_score[nei] = temp_g_score
                        if nei not in open_set_hash:
                            queue_pos += 1
                            open_set.put((g_score[nei], queue_pos, nei, 'start'))
                            open_set_hash.add(nei)
                            if nei != end and nei.color != self.CLOSED_COLOR and nei != ignore_node:
                                nei.set_open()
            elif temp[3] == 'end':
                for nei in curr_square.neighbours:
                    temp_g_score = g_score[curr_square] + 1

                    if temp_g_score < g_score[nei]:
                        came_from_end[nei] = curr_square
                        g_score[nei] = temp_g_score
                        if nei not in open_set_hash:
                            queue_pos += 1
                            open_set.put((g_score[nei], queue_pos, nei, 'end'))
                            open_set_hash.add(nei)
                            if nei != start and nei.color != self.CLOSED_COLOR and nei != ignore_node:
                                nei.set_open_alt()

            # Only visualize if called. Checks if square is closed to not repeat when mid node included.
            if visualize and not curr_square.is_closed():
                self.draw(graph, display_update=False)
                self.draw_vis_text(bi_dijkstra=True)

            # Sets square to closed after finished checking
            if curr_square != start and curr_square != end and curr_square != ignore_node:
                curr_square.set_closed()

        return False

    def best_path_bi_dijkstra(self, graph, came_from_start, came_from_end,
                              first_meet_node, second_meet_node, visualize=True):
        """Used by bi_dijkstra to draw best path from in two parts"""

        # Fixes bug when can't find a path
        if isinstance(came_from_start, bool) or isinstance(came_from_end, bool):
            return

        # Draws best path for first swarm
        self.best_path(graph, came_from_start, first_meet_node, visualize=visualize)
        # To not skip the last two at once, need a draw, draw_vis_text, and time.sleep here
        first_meet_node.set_path()
        # To not skip the last two at once, need a draw, draw_vis_text, and time.sleep here

        # Draws best path for second swarm
        second_meet_node.set_path()
        # To not skip the last two at once, need a draw and draw_vis_text here
        self.best_path(graph, came_from_end, second_meet_node, reverse=True, visualize=visualize)
        # To not skip the last two at once, need a draw, draw_vis_text, and time.sleep here

    def start_mid_end(self, graph, start, mid, end, dijkstra=False, a_star=False, bi_dijkstra=False, visualize=True):
        """Used if algos need to reach mid node first"""

        # Selects the correct algo to use
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
        elif a_star:
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
        elif bi_dijkstra:
            if visualize:
                start_to_mid = self.bi_dijkstra(graph, start, mid, ignore_node=end, draw_best_path=False)
                mid_to_end = self.bi_dijkstra(graph, mid, end, ignore_node=start, draw_best_path=False)
            else:
                start_to_mid = self.algo_no_vis(graph, start, mid, bi_dijkstra=True,
                                                ignore_node=end, draw_best_path=False)
                mid_to_end = self.algo_no_vis(graph, mid, end, bi_dijkstra=True, ignore_node=start,
                                              draw_best_path=False, reset=False)
                start.set_start(), mid.set_mid(), end.set_end()  # Fixes nodes disappearing when dragging

            # Fixes bug when can't find a path
            if not isinstance(start_to_mid, bool):
                self.best_path_bi_dijkstra(graph, start_to_mid[0], start_to_mid[1],
                                           start_to_mid[2], start_to_mid[3], visualize=visualize)
            if not isinstance(mid_to_end, bool):
                self.best_path_bi_dijkstra(graph, mid_to_end[0], mid_to_end[1],
                                           mid_to_end[2], mid_to_end[3], visualize=visualize)

    def algo_no_vis(self, graph, start, end, dijkstra=False, a_star=False, bi_dijkstra=False,
                    ignore_node=None, draw_best_path=True, reset=True):
        """Skip steps to end when visualizing algo. Used when dragging ordinal node once finished"""

        # Selects the correct algo to use
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
        elif a_star:
            if reset:   # Used to not reset start -> mid visualizations if going from mid -> end
                self.reset_algo(graph)
            self.a_star_finished = True

            # Separates calling algo_no_vis with mid node or not
            if draw_best_path:
                self.a_star(graph, start, end, visualize=False)
                start.set_start()  # Fixes start disappearing when dragging
            else:
                return self.a_star(graph, start, end, ignore_node=ignore_node, draw_best_path=False, visualize=False)
        elif bi_dijkstra:
            if reset:   # Used to not reset start -> mid visualizations if going from mid -> end
                self.reset_algo(graph)
            self.bi_dijkstra_finished = True

            # Separates calling algo_no_vis with mid node or not
            if draw_best_path:
                self.bi_dijkstra(graph, start, end, visualize=False)
                start.set_start()  # Fixes start disappearing when dragging
            else:
                return self.bi_dijkstra(graph, start, end, ignore_node=ignore_node,
                                        draw_best_path=False, visualize=False)

    def best_path(self, graph, came_from, curr_square, reverse=False, visualize=True):
        """Main algo for reconstructing path"""

        # Fixes bug when dragging where came_from would evaluate to bool instead of dict.
        if isinstance(came_from, bool):
            return

        # Puts node path into list so it's easier to traverse in either direction and choose start and end points
        path = []
        while curr_square in came_from:
            curr_square = came_from[curr_square]
            path.append(curr_square)

        # Need to traverse in reverse depending on what part of algo
        if reverse:
            for square in path[:-1]:
                square.set_path()
                if visualize:
                    time.sleep(self.best_path_sleep)
                    self.draw(graph, display_update=False)
                    self.draw_vis_text(best_path=True)
        else:
            for square in path[len(path)-2::-1]:
                square.set_path()
                if visualize:
                    time.sleep(self.best_path_sleep)
                    self.draw(graph, display_update=False)
                    self.draw_vis_text(best_path=True)

    def draw_recursive_maze(self, graph, chamber=None, visualize=True):
        """Creates maze using recursive division.
        Implemented following wikipedia guidelines.
        https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_division_method
        Inspired by https://github.com/ChrisKneller/pygame-pathfinder
        """

        # Sets min size for division
        division_limit = 3

        # Creates chambers to divide into
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

        # Helps with location of chambers
        x_divide = int(chamber_width/2)
        y_divide = int(chamber_height/2)

        # Draws vertical maze line within chamber
        if chamber_width >= division_limit:
            for y in range(chamber_height):
                graph[chamber_left + x_divide][chamber_top + y].set_wall()
                self.wall_nodes.add(graph[chamber_left + x_divide][chamber_top + y])
                if visualize:
                    self.draw(graph, display_update=False)
                    self.draw_vis_text(recursive_maze=True)

        # Draws horizontal maze line within chamber
        if chamber_height >= division_limit:
            for x in range(chamber_width):
                graph[chamber_left + x][chamber_top + y_divide].set_wall()
                self.wall_nodes.add(graph[chamber_left + x][chamber_top + y_divide])
                if visualize:
                    self.draw(graph, display_update=False)
                    self.draw_vis_text(recursive_maze=True)

        # Terminates if below division limit
        if chamber_width < division_limit and chamber_height < division_limit:
            return

        # Defining limits on where to draw walls
        top_left = (chamber_left, chamber_top, x_divide, y_divide)
        top_right = (chamber_left + x_divide+1, chamber_top, chamber_width - x_divide-1, y_divide)
        bottom_left = (chamber_left, chamber_top + y_divide+1, x_divide, chamber_height - y_divide-1)
        bottom_right = (chamber_left + x_divide+1, chamber_top + y_divide+1,
                        chamber_width - x_divide-1, chamber_height - y_divide-1)

        # Combines all chambers into one object
        chambers = (top_left, top_right, bottom_left, bottom_right)

        # Defines location of the walls
        left = (chamber_left, chamber_top + y_divide, x_divide, 1)
        right = (chamber_left + x_divide+1, chamber_top + y_divide, chamber_width - x_divide-1, 1)
        top = (chamber_left + x_divide, chamber_top, 1, y_divide)
        bottom = (chamber_left + x_divide, chamber_top + y_divide+1, 1, chamber_height - y_divide-1)

        # Combines walls into one object
        walls = (left, right, top, bottom)

        # Number of gaps to leave in walls after each division into four sub quadrants.
        num_gaps = 3

        # Prevents drawing wall over gaps
        gaps_to_offset = [x for x in range(num_gaps - 1, self.rows, num_gaps)]

        # Draws the gaps into the walls
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

        # Recursively divides chambers
        for chamber in chambers:
            if visualize:
                self.draw_recursive_maze(graph, chamber)
            else:
                self.draw_recursive_maze(graph, chamber, visualize=False)


class Square(PathfindingVisualizer):
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

    def draw_square(self, window):
        """Updates the square with node type"""
        pygame.draw.rect(window, self.color, (self.x, self.y, int(self.square_size), int(self.square_size)))

    def update_values(self, rows, square_size):
        """Updates the attributes of node. Used when changing graph size"""
        self.rows = rows
        self.square_size = square_size
        self.x = self.row * self.square_size
        self.y = self.col * self.square_size


'''
New features for the future:

Update only affect nodes rather than entire screen to improve performance (currently very good already)
    Especially when drawing lines. Currently creating mid and large graphs is slow
Instantly update algo when draw wall after completion, much like dragging nodes
Add prim maze and sticky mud


Bugs to fix:

Bi-directional dijkstra only draws best_path when edges of swarms are touching. Only manifests with mid nodes
Maze can change size if window loses focus for a few seconds. Mainly with the large maze.
    pygame.event.set_grab prevents mouse from leaving window but also prevents exists
    pygame.mouse.get_focused() potential elegant solution
'''
