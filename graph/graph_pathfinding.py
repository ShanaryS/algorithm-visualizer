import pygame
from graph.node import Square
from calc.colors import *
from calc.values import ROWS, WIDTH_HEIGHT, SQUARE_SIZE, get_random_sample, get_randrange
from queue import PriorityQueue


# Defining window properties as well as graph size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 879
WIDTH = WIDTH_HEIGHT
HEIGHT = WIDTH_HEIGHT
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
LEGEND_AREA = pygame.Rect(0, HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - HEIGHT)
pygame.display.set_caption("Pathfinding Visualizer - github.com/ShanaryS/algorithm-visualizer")

# Defining the size of the squares. Changes with change_graph_size
rows = ROWS
square_size = SQUARE_SIZE
# Recursive division only works on certain row values. 22,23,46,47,94,95.


# Creates the text needed for legend and when visualizing
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 12)

legend_add_node = font.render("Left Click - Add Node (Start -> End -> Walls)", True, LEGEND_COLOR)
legend_add_mid_node = font.render("Middle Click - Add mid node", True, LEGEND_COLOR)
legend_remove_node = font.render("Right Click - Remove Node", True, LEGEND_COLOR)
legend_clear_graph = font.render("Press 'SPACE' - Clear graph", True, LEGEND_COLOR)
legend_graph_size = font.render("Press 'S', 'M', 'L' - Change graph size", True, LEGEND_COLOR)
legend_dijkstra = font.render("Dijkstra - Press 'D'", True, LEGEND_COLOR)
legend_a_star = font.render("A* - Press 'A'", True, LEGEND_COLOR)
legend_bi_dijkstra = font.render("Bi-directional Dijkstra - Press 'B'", True, LEGEND_COLOR)
legend_recursive_maze = font.render("Generate maze - Press 'G'", True, LEGEND_COLOR)
legend_instant_recursive_maze = font.render("Generate maze (Instantly) - Press 'I'", True, LEGEND_COLOR)

vis_text_dijkstra = font.render("Visualizing Dijkstra...", True, VIS_COLOR)
vis_text_a_star = font.render("Visualizing A*...", True, VIS_COLOR)
vis_text_bi_dijkstra = font.render("Visualizing Bi-directional Dijkstra...", True, VIS_COLOR)
vis_text_best_path = font.render("Laying best path...", True, VIS_COLOR)
vis_text_recursive_maze = font.render("Generating recursive maze...", True, VIS_COLOR)
vis_text_graph_size = font.render("Changing graph size... May take up to 30 seconds", True, VIS_COLOR)


# Extra variables needed in scope of entire class for different functions.
dijkstra_finished = False
a_star_finished = False
bi_dijkstra_finished = False
maze = False   # Used to prevent drawing extra walls during maze
ordinal_node_clicked = []   # Used for dragging start and end once algos are finished. Length is 0 or 1.
wall_nodes = set()     # Used to reinstate walls after deletion for mazes and dragging
BEST_PATH_SLEEP = 3


# Put all game specific variables in here so it's easy to restart with main()
def main():
    """The pygame logic loop. This runs forever until exited. This is what should be called to run program."""

    global dijkstra_finished, a_star_finished, bi_dijkstra_finished, maze

    graph = set_graph()

    # Defining ordinal nodes to be used within the loop in various places
    start = None
    mid = None
    end = None

    run = True
    while run:
        draw(graph, legend=True)

        # Allow clicking the "X" on the pygame window to end the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Used to know if no longer dragging ordinal node after algo completion
            if not pygame.mouse.get_pressed(3)[0]:
                ordinal_node_clicked.clear()

            # LEFT MOUSE CLICK. HEIGHT condition prevents out of bound when clicking on legend.
            if pygame.mouse.get_pressed(3)[0] and pygame.mouse.get_pos()[1] < HEIGHT:

                # Get square clicked
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                square = graph[row][col]

                # Checks if algo is completed, used for dragging algo
                if (dijkstra_finished or a_star_finished or bi_dijkstra_finished) and start and end:

                    # Checks if ordinal node is being dragged
                    if ordinal_node_clicked:

                        # Checks if the mouse is currently on an ordinal node, no need to update anything
                        if square != start and square != mid and square != end:
                            last_square = ordinal_node_clicked[0]  # Used to move ordinal node to new pos

                            # Checks if ordinal node was previously a wall to reinstate it after moving, else reset
                            if last_square == 'start':
                                if start in wall_nodes:
                                    start.set_wall()
                                else:
                                    start.reset()
                                start = square
                                square.set_start()
                            elif last_square == 'mid':
                                if mid in wall_nodes:
                                    mid.set_wall()
                                else:
                                    mid.reset()
                                mid = square
                                square.set_mid()
                            elif last_square == 'end':
                                if end in wall_nodes:
                                    end.set_wall()
                                else:
                                    end.reset()
                                end = square
                                square.set_end()

                            # Runs the algo again instantly with no visualizations, handles whether mid exists
                            if dijkstra_finished:
                                if mid:
                                    start_mid_end(graph, start, mid, end, is_dijkstra=True, visualize=False)
                                else:
                                    algo_no_vis(graph, start, end, is_dijkstra=True)
                            elif a_star_finished:
                                if mid:
                                    start_mid_end(graph, start, mid, end, is_a_star=True, visualize=False)
                                else:
                                    algo_no_vis(graph, start, end, is_a_star=True)
                            elif bi_dijkstra_finished:
                                if mid:
                                    start_mid_end(graph, start, mid, end, is_bi_dijkstra=True, visualize=False)
                                else:
                                    algo_no_vis(graph, start, end, is_bi_dijkstra=True)

                    # If ordinal node is not being dragged, prepare it to
                    elif square is start:
                        ordinal_node_clicked.append('start')
                    elif square is mid:
                        ordinal_node_clicked.append('mid')
                    elif square is end:
                        ordinal_node_clicked.append('end')

                # If start node does not exist, create it. If not currently ordinal node.
                elif not start and square != mid and square != end:
                    start = square
                    square.set_start()

                    # Handles removing and adding start manually instead of dragging on algo completion.
                    if dijkstra_finished and start and end:
                        algo_no_vis(graph, start, end, is_dijkstra=True)
                    elif a_star_finished and start and end:
                        algo_no_vis(graph, start, end, is_a_star=True)
                    elif bi_dijkstra_finished and start and end:
                        algo_no_vis(graph, start, end, is_bi_dijkstra=True)

                # If end node does not exist, and start node does exist, create end node.
                # If not currently ordinal node.
                elif not end and square != start and square != mid:
                    end = square
                    square.set_end()

                    # Handles removing and adding end manually instead of dragging on algo completion.
                    if dijkstra_finished and start and end:
                        algo_no_vis(graph, start, end, is_dijkstra=True)
                    elif a_star_finished and start and end:
                        algo_no_vis(graph, start, end, is_a_star=True)
                    elif bi_dijkstra_finished and start and end:
                        algo_no_vis(graph, start, end, is_bi_dijkstra=True)

                # If start and end node exists, create wall. If not currently ordinal node.
                # Saves pos of wall to be able to reinstate it after dragging ordinal node past it.
                elif square != start and square != mid and square != end and maze is False:
                    square.set_wall()
                    wall_nodes.add(square)

            # RIGHT MOUSE CLICK. HEIGHT condition prevents out of bound when clicking on legend.
            elif pygame.mouse.get_pressed(3)[2] and pygame.mouse.get_pos()[1] < HEIGHT:

                # Get square clicked
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                square = graph[row][col]

                # If square to remove is wall, need to remove it from wall_node as well to retain accuracy
                if square.is_wall():
                    wall_nodes.discard(square)

                # Reset square and ordinal node if it was any
                square.reset()
                if square == start:
                    start = None
                elif square == mid:
                    mid = None
                elif square == end:
                    end = None

            # MIDDLE MOUSE CLICK. HEIGHT condition prevents out of bound when clicking on legend.
            elif pygame.mouse.get_pressed(3)[1] and pygame.mouse.get_pos()[1] < HEIGHT:

                # Get square clicked
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                square = graph[row][col]

                # Set square to mid if no square is already mid, and not currently ordinal node.
                if not mid:
                    if square != start and square != end:
                        mid = square
                        square.set_mid()

                        # Handles removing and adding mid manually instead of dragging on algo completion.
                        if dijkstra_finished and start and mid and end:
                            start_mid_end(graph, start, mid, end, is_dijkstra=True, visualize=False)
                        elif a_star_finished and start and mid and end:
                            start_mid_end(graph, start, mid, end, is_a_star=True, visualize=False)
                        elif bi_dijkstra_finished and start and mid and end:
                            start_mid_end(graph, start, mid, end, is_bi_dijkstra=True, visualize=False)

            # Reset graph with "SPACE" on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_graph(graph)

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
                    reset_algo(graph)

                    # Updates neighbours in case anything has changed
                    for row in graph:
                        for square in row:
                            square.update_neighbours(graph)

                    # Necessary to for dragging nodes on completion
                    dijkstra_finished = True

                    # Handles whether or not mid exists
                    if mid:
                        start_mid_end(graph, start, mid, end, is_dijkstra=True)
                    else:
                        dijkstra(graph, start, end)

            # Run A* with "A" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:

                    # Resets algo visualizations without removing ordinal nodes or walls
                    reset_algo(graph)

                    # Updates neighbours in case anything has changed
                    for row in graph:
                        for square in row:
                            square.update_neighbours(graph)

                    # Necessary to for dragging nodes on completion
                    a_star_finished = True

                    # Handles whether or not mid exists
                    if mid:
                        start_mid_end(graph, start, mid, end, is_a_star=True)
                    else:
                        a_star(graph, start, end)

            # Run Bi-directional Dijkstra with "B" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and start and end:

                    # Resets algo visualizations without removing ordinal nodes or walls
                    reset_algo(graph)

                    # Updates neighbours in case anything has changed
                    for row in graph:
                        for square in row:
                            square.update_neighbours(graph)

                    # Necessary to for dragging nodes on completion
                    bi_dijkstra_finished = True

                    # Handles whether or not mid exists
                    if mid:
                        start_mid_end(graph, start, mid, end, is_bi_dijkstra=True)
                    else:
                        bi_dijkstra(graph, start, end)

            # Draw recursive maze with "G" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    # Resets entire graph to prevent any unintended behaviour
                    reset_graph(graph)

                    # Draw maze
                    draw_recursive_maze(graph)

                    # Necessary for handling dragging over barriers if in maze
                    maze = True

                    # Reset ordinal nodes as it cannot be in reset_graph due to scope
                    start = None
                    mid = None
                    end = None

            # Draw recursive maze with NO VISUALIZATIONS with "I" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    # Resets entire graph to prevent any unintended behaviour
                    reset_graph(graph)

                    # Draw maze instantly with no visualizations
                    draw_recursive_maze(graph, visualize=False)

                    # Necessary for handling dragging over barriers if in maze
                    maze = True

                    # Reset ordinal nodes as it cannot be in reset_graph due to scope
                    start = None
                    mid = None
                    end = None

            # Redraw small maze with "S" key on keyboard if not currently small
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:

                    # If maze is currently small, no need to redraw
                    if rows != 22:
                        # Changes graph size to small
                        graph = change_graph_size(22)

                        # Reset ordinal nodes as it cannot be in reset_graph due to scope
                        start = None
                        mid = None
                        end = None

            # Redraw medium maze with "M" key on keyboard if not currently medium
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:

                    # If maze is already medium, no need to redraw
                    if rows != 46:
                        # Changes graph size to medium
                        graph = change_graph_size(46)

                        # Reset ordinal nodes as it cannot be in reset_graph due to scope
                        start = None
                        mid = None
                        end = None

            # Redraw large maze with "L" key on keyboard if not currently large
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:

                    # If maze is already large, no need to redraw
                    if rows != 95:
                        # Changes graph size to large
                        graph = change_graph_size(95)

                        # Reset ordinal nodes as it cannot be in reset_graph due to scope
                        start = None
                        mid = None
                        end = None

    # Only reached if while loop ends, which happens if window is closed. Program terminates.
    pygame.quit()


def set_graph():
    """Creates the graph object that stores the location of all the squares"""
    graph = []
    for i in range(rows):
        graph.append([])
        for j in range(rows):
            # Uses Square class to create square object with necessary attributes
            square = Square(i, j)

            # Necessary for when changing graph size
            square.update_values(rows, square_size)

            graph[i].append(square)

    return graph


def draw(graph, legend=False, display_update=True):
    """Main function to update the window. Called by all operations that updates the window."""

    # Sets background of graph to white and legend to grey
    WINDOW.fill(DEFAULT_COLOR)
    WINDOW.fill(LEGEND_AREA_COLOR, LEGEND_AREA)

    # If colors of square were updated, reflected here
    for row in graph:
        for square in row:
            square_color, square_pos = square.draw_square()
            _draw_square(square_color, square_pos)

    # Draws the horizontal and vertical lines on the graph
    _draw_lines()

    # Legend is only shown if graph can be interacted with
    if legend:
        _draw_legend()

    # Display may not want to update display immediately before doing other operations
    if display_update:
        pygame.display.update()


def _draw_lines():
    """Helper function to define the properties of the horizontal and vertical graph lines"""
    for i in range(rows):
        pygame.draw.line(WINDOW, LINE_COLOR,
                         (0, i * square_size), (WIDTH, i * square_size))
        pygame.draw.line(WINDOW, LINE_COLOR,
                         (i * square_size, 0), (i * square_size, WIDTH))


def _draw_square(square_color, square_pos):
    pygame.draw.rect(WINDOW, square_color, square_pos)


def _draw_legend():
    """Helper function to define the location of the legend"""
    # Left legend
    WINDOW.blit(legend_add_node, (2, 15*53.1 + 3))
    WINDOW.blit(legend_add_mid_node, (2, 15*54.1 + 3))
    WINDOW.blit(legend_remove_node, (2, 15*55.1 + 3))
    WINDOW.blit(legend_clear_graph, (2, 15*56.1 + 3))
    WINDOW.blit(legend_graph_size, (2, 15*57.1 + 3))

    # Right legend
    WINDOW.blit(legend_dijkstra, (WIDTH - legend_dijkstra.get_width()-2, 15*53.1 + 3))
    WINDOW.blit(legend_a_star, (WIDTH - legend_a_star.get_width()-2, 15*54.1 + 3))
    WINDOW.blit(legend_bi_dijkstra, (WIDTH - legend_bi_dijkstra.get_width()-2, 15*55.1 + 3))
    WINDOW.blit(legend_recursive_maze, (WIDTH - legend_recursive_maze.get_width()-2, 15*56.1 + 3))
    WINDOW.blit(legend_instant_recursive_maze, (WIDTH - legend_instant_recursive_maze.get_width()-2, 15*57.1 + 3))


def draw_vis_text(is_dijkstra=False, is_a_star=False, is_bi_dijkstra=False,
                  is_best_path=False, is_recursive_maze=False, is_graph_size=False):
    """Special text indicating some operation is being performed. No inputs are registered."""

    # Defines the center of the graph and legend for text placement
    center_graph = HEIGHT//2
    center_legend_area = HEIGHT + (WINDOW_HEIGHT - HEIGHT)//2

    # Text to be shown depending on operation
    if is_dijkstra:
        WINDOW.blit(vis_text_dijkstra,
                    (WIDTH//2 - vis_text_dijkstra.get_width()//2,
                     center_legend_area - vis_text_dijkstra.get_height()//2))
    elif is_a_star:
        WINDOW.blit(vis_text_a_star,
                    (WIDTH//2 - vis_text_a_star.get_width()//2,
                     center_legend_area - vis_text_a_star.get_height()//2))
    elif is_bi_dijkstra:
        WINDOW.blit(vis_text_bi_dijkstra,
                    (WIDTH//2 - vis_text_bi_dijkstra.get_width()//2,
                     center_legend_area - vis_text_bi_dijkstra.get_height()//2))
    elif is_best_path:
        WINDOW.blit(vis_text_best_path,
                    (WIDTH // 2 - vis_text_best_path.get_width() // 2,
                     center_legend_area - vis_text_best_path.get_height() // 2))
    elif is_recursive_maze:
        WINDOW.blit(vis_text_recursive_maze,
                    (WIDTH//2 - vis_text_recursive_maze.get_width()//2,
                     center_legend_area - vis_text_recursive_maze.get_height()//2))
    elif is_graph_size:
        WINDOW.blit(vis_text_graph_size,
                    (WIDTH//2 - vis_text_graph_size.get_width()//2,
                     center_graph - vis_text_graph_size.get_height()//2))

    # Always called after draw. In that scenario draw won't update display so this will
    pygame.display.update()


def reset_graph(graph):
    """Resets entire graph removing every square"""

    # Need to update these values
    global dijkstra_finished, a_star_finished, bi_dijkstra_finished, maze
    dijkstra_finished = False
    a_star_finished = False
    bi_dijkstra_finished = False
    maze = False

    # Resets each square
    for i in range(rows):
        for j in range(rows):
            square = graph[i][j]
            square.reset()


def reset_algo(graph):
    """Resets algo colors while keeping ordinal nodes and walls"""

    # Need to update these values
    global dijkstra_finished, a_star_finished, bi_dijkstra_finished
    dijkstra_finished = False
    a_star_finished = False
    bi_dijkstra_finished = False

    # Resets only certain colors
    for i in range(rows):
        for j in range(rows):
            square = graph[i][j]
            if square.is_open() or square.is_open_alt() or square.is_open_alt_()\
                    or square.is_closed() or square.is_path():
                square.reset()


def change_graph_size(new_row_size):
    """Changes graph size and updates squares and their locations as well.
    Restricted to certain sizes as recursive maze breaks otherwise
    """

    # Displays text that size is changing
    draw_vis_text(is_graph_size=True)

    # Updates rows and square size with new values
    global rows, square_size
    rows = new_row_size
    square_size = WIDTH / rows

    # Recreates graph with new values
    graph = set_graph()
    draw(graph)

    return graph


def get_clicked_pos(pos):
    """Turns the location data of the mouse into location of squares"""
    y, x = pos
    row = int(y / square_size)
    col = int(x / square_size)
    return row, col


def dijkstra(graph, start, end, ignore_node=None, draw_best_path=True, visualize=True):
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
                best_path(graph, came_from, end, visualize=visualize)
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
                    if nei != end and nei.color != CLOSED_COLOR and nei != ignore_node:
                        nei.set_open()

        # Only visualize if called. Checks if square is closed to not repeat when mid node included.
        if visualize and not curr_square.is_closed():
            draw(graph, display_update=False)
            draw_vis_text(is_dijkstra=True)

        # Sets square to closed after finished checking
        if curr_square != start and curr_square != ignore_node:
            curr_square.set_closed()

    return False


def a_star(graph, start, end, ignore_node=None, draw_best_path=True, visualize=True):
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
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

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
                best_path(graph, came_from, end, visualize=visualize)
                return True

            return came_from

        # Decides the order of neighbours to check
        for nei in curr_square.neighbours:
            temp_g_score = g_score[curr_square] + 1

            if temp_g_score < g_score[nei]:
                came_from[nei] = curr_square
                g_score[nei] = temp_g_score
                f_score[nei] = temp_g_score + heuristic(nei.get_pos(), end.get_pos())
                if nei not in open_set_hash:
                    queue_pos += 1
                    open_set.put((f_score[nei], queue_pos, nei))
                    open_set_hash.add(nei)
                    if nei != end and nei.color != CLOSED_COLOR and nei != ignore_node:
                        nei.set_open()

        # Only visualize if called. Checks if square is closed to not repeat when mid node included.
        if visualize and not curr_square.is_closed():
            draw(graph, display_update=False)
            draw_vis_text(is_a_star=True)

        # Sets square to closed after finished checking
        if curr_square != start and curr_square != ignore_node:
            curr_square.set_closed()

    return False


def heuristic(pos1, pos2):
    """Used by A* to prioritize traveling towards next node"""
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def bi_dijkstra(graph, start, end, alt_color=False, ignore_node=None, draw_best_path=True, visualize=True):
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
                    best_path_bi_dijkstra(graph, came_from_start, came_from_end,
                                          curr_square, nei, visualize=visualize)
                    return True

                return came_from_start, came_from_end, curr_square, nei

            elif curr_square.is_open_alt() and nei.is_open() and not alt_color:
                if draw_best_path:
                    best_path_bi_dijkstra(graph, came_from_start, came_from_end,
                                          nei, curr_square, visualize=visualize)
                    return True

                return came_from_start, came_from_end, nei, curr_square

            elif curr_square.is_open_alt() and nei.is_open_alt_():
                if draw_best_path:
                    best_path_bi_dijkstra(graph, came_from_start, came_from_end,
                                          curr_square, nei, visualize=visualize)
                    return True

                return came_from_start, came_from_end, curr_square, nei

            elif curr_square.is_open_alt_() and nei.is_open_alt():
                if draw_best_path:
                    best_path_bi_dijkstra(graph, came_from_start, came_from_end,
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
                        if nei != end and nei.color != CLOSED_COLOR and nei != ignore_node:
                            if alt_color:
                                nei.set_open_alt()
                            else:
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
                        if nei != start and nei.color != CLOSED_COLOR and nei != ignore_node:
                            if alt_color:
                                nei.set_open_alt_()
                            else:
                                nei.set_open_alt()

        # Only visualize if called. Checks if square is closed to not repeat when mid node included.
        if visualize and not curr_square.is_closed():
            draw(graph, display_update=False)
            draw_vis_text(is_bi_dijkstra=True)

        # Sets square to closed after finished checking
        if curr_square != start and curr_square != end and curr_square != ignore_node:
            curr_square.set_closed()

    return False


def best_path_bi_dijkstra(graph, came_from_start, came_from_end,
                          first_meet_node, second_meet_node, visualize=True):
    """Used by bi_dijkstra to draw best path from in two parts"""

    # Fixes bug when can't find a path
    if isinstance(came_from_start, bool) or isinstance(came_from_end, bool):
        return

    # Draws best path for first swarm
    best_path(graph, came_from_start, first_meet_node, visualize=visualize)
    # To not skip the last two at once, need a draw, draw_vis_text, and sleep here
    first_meet_node.set_path()
    # To not skip the last two at once, need a draw, draw_vis_text, and sleep here

    # Draws best path for second swarm
    second_meet_node.set_path()
    # To not skip the last two at once, need a draw and draw_vis_text here
    best_path(graph, came_from_end, second_meet_node, reverse=True, visualize=visualize)
    # To not skip the last two at once, need a draw, draw_vis_text, and sleep here


def start_mid_end(graph, start, mid, end, is_dijkstra=False, is_a_star=False, is_bi_dijkstra=False, visualize=True):
    """Used if algos need to reach mid node first"""

    # Selects the correct algo to use
    if is_dijkstra:
        if visualize:
            start_to_mid = dijkstra(graph, start, mid, ignore_node=end, draw_best_path=False)
            mid_to_end = dijkstra(graph, mid, end, ignore_node=start, draw_best_path=False)
        else:
            start_to_mid = algo_no_vis(graph, start, mid, is_dijkstra=True, ignore_node=end, draw_best_path=False)
            mid_to_end = algo_no_vis(graph, mid, end, is_dijkstra=True, ignore_node=start,
                                     draw_best_path=False, reset=False)
            start.set_start(), mid.set_mid(), end.set_end()  # Fixes nodes disappearing when dragging

        best_path(graph, start_to_mid, mid, visualize=visualize)
        best_path(graph, mid_to_end, end, visualize=visualize)
    elif is_a_star:
        if visualize:
            start_to_mid = a_star(graph, start, mid, ignore_node=end, draw_best_path=False)
            mid_to_end = a_star(graph, mid, end, ignore_node=start, draw_best_path=False)
        else:
            start_to_mid = algo_no_vis(graph, start, mid, is_a_star=True, ignore_node=end, draw_best_path=False)
            mid_to_end = algo_no_vis(graph, mid, end, is_a_star=True, ignore_node=start,
                                     draw_best_path=False, reset=False)
            start.set_start(), mid.set_mid(), end.set_end()  # Fixes nodes disappearing when dragging

        best_path(graph, start_to_mid, mid, visualize=visualize)
        best_path(graph, mid_to_end, end, visualize=visualize)
    elif is_bi_dijkstra:
        if visualize:
            start_to_mid = bi_dijkstra(graph, start, mid, ignore_node=end, draw_best_path=False)
            mid_to_end = bi_dijkstra(graph, mid, end, alt_color=True, ignore_node=start, draw_best_path=False)
        else:
            start_to_mid = algo_no_vis(graph, start, mid, is_bi_dijkstra=True, ignore_node=end, draw_best_path=False)
            mid_to_end = algo_no_vis(graph, mid, end, alt_color=True, is_bi_dijkstra=True, ignore_node=start,
                                     draw_best_path=False, reset=False)
            start.set_start(), mid.set_mid(), end.set_end()  # Fixes nodes disappearing when dragging

        # Fixes bug when can't find a path
        if not isinstance(start_to_mid, bool):
            best_path_bi_dijkstra(graph, start_to_mid[0], start_to_mid[1],
                                  start_to_mid[2], start_to_mid[3], visualize=visualize)
        if not isinstance(mid_to_end, bool):
            best_path_bi_dijkstra(graph, mid_to_end[0], mid_to_end[1],
                                  mid_to_end[2], mid_to_end[3], visualize=visualize)


def algo_no_vis(graph, start, end, is_dijkstra=False, is_a_star=False, is_bi_dijkstra=False, alt_color=False,
                ignore_node=None, draw_best_path=True, reset=True):
    """Skip steps to end when visualizing algo. Used when dragging ordinal node once finished"""

    global dijkstra_finished, a_star_finished, bi_dijkstra_finished

    # Selects the correct algo to use
    if is_dijkstra:
        if reset:   # Used to not reset start -> mid visualizations if going from mid -> end
            reset_algo(graph)
        dijkstra_finished = True

        # Separates calling algo_no_vis with mid node or not
        if draw_best_path:
            dijkstra(graph, start, end, visualize=False)
            start.set_start()  # Fixes start disappearing when dragging
        else:
            return dijkstra(graph, start, end, ignore_node=ignore_node, draw_best_path=False, visualize=False)
    elif is_a_star:
        if reset:   # Used to not reset start -> mid visualizations if going from mid -> end
            reset_algo(graph)
        a_star_finished = True

        # Separates calling algo_no_vis with mid node or not
        if draw_best_path:
            a_star(graph, start, end, visualize=False)
            start.set_start()  # Fixes start disappearing when dragging
        else:
            return a_star(graph, start, end, ignore_node=ignore_node, draw_best_path=False, visualize=False)
    elif is_bi_dijkstra:
        if reset:   # Used to not reset start -> mid visualizations if going from mid -> end
            reset_algo(graph)
        bi_dijkstra_finished = True

        # Separates calling algo_no_vis with mid node or not
        if draw_best_path:
            bi_dijkstra(graph, start, end, alt_color=alt_color, visualize=False)
            start.set_start()  # Fixes start disappearing when dragging
        else:
            return bi_dijkstra(graph, start, end, alt_color=alt_color, ignore_node=ignore_node,
                               draw_best_path=False, visualize=False)


def best_path(graph, came_from, curr_square, reverse=False, visualize=True):
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
                pygame.time.delay(BEST_PATH_SLEEP)
                draw(graph, display_update=False)
                draw_vis_text(is_best_path=True)
    else:
        for square in path[len(path)-2::-1]:
            square.set_path()
            if visualize:
                pygame.time.delay(BEST_PATH_SLEEP)
                draw(graph, display_update=False)
                draw_vis_text(is_best_path=True)


def draw_recursive_maze(graph, chamber=None, visualize=True):
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
            wall_nodes.add(graph[chamber_left + x_divide][chamber_top + y])
            if visualize:
                draw(graph, display_update=False)
                draw_vis_text(is_recursive_maze=True)

    # Draws horizontal maze line within chamber
    if chamber_height >= division_limit:
        for x in range(chamber_width):
            graph[chamber_left + x][chamber_top + y_divide].set_wall()
            wall_nodes.add(graph[chamber_left + x][chamber_top + y_divide])
            if visualize:
                draw(graph, display_update=False)
                draw_vis_text(is_recursive_maze=True)

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
    gaps_to_offset = [x for x in range(num_gaps - 1, rows, num_gaps)]

    # Draws the gaps into the walls
    for wall in get_random_sample(walls, num_gaps):
        if wall[3] == 1:
            x = get_randrange(wall[0], wall[0] + wall[2])
            y = wall[1]
            if x in gaps_to_offset and y in gaps_to_offset:
                if wall[2] == x_divide:
                    x -= 1
                else:
                    x += 1
            if x >= rows:
                x = rows - 1
        else:
            x = wall[0]
            y = get_randrange(wall[1], wall[1] + wall[3])
            if y in gaps_to_offset and x in gaps_to_offset:
                if wall[3] == y_divide:
                    y -= 1
                else:
                    y += 1
            if y >= rows:
                y = rows - 1
        graph[x][y].reset()
        wall_nodes.discard(graph[x][y])
        if visualize:
            draw(graph, display_update=False)
            draw_vis_text(is_recursive_maze=True)

    # Recursively divides chambers
    for chamber in chambers:
        if visualize:
            draw_recursive_maze(graph, chamber)
        else:
            draw_recursive_maze(graph, chamber, visualize=False)


'''
New features for the future:

Update only affect nodes rather than entire screen to improve performance (currently very good already)
    Especially when drawing lines. Currently creating mid and large graphs is slow
Instantly update algo when draw wall after completion, much like dragging nodes
Add prim maze and sticky mud


Bugs to fix:

When clicking to remove start/end node with mid node and reinstating it on completed algo, doesn't update properly
Bi-directional dijkstra only draws best_path when edges of swarms are touching. Only manifests with mid nodes
Maze can change size if window loses focus for a few seconds. Mainly with the large maze.
    pygame.event.set_grab prevents mouse from leaving window but also prevents exists
    pygame.mouse.get_focused() potential elegant solution
'''
