"""Draws and updates graph for visualization"""


import pygame
from pathfinding.colors import PygameColors as PygC
from pathfinding.values import ROWS, WIDTH_HEIGHT, SQUARE_SIZE
from pathfinding.node import Square


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

legend_add_node = font.render("Left Click - Add Node (Start -> End -> Walls)", True, PygC.LEGEND_COLOR)
legend_add_mid_node = font.render("Middle Click - Add mid node", True, PygC.LEGEND_COLOR)
legend_remove_node = font.render("Right Click - Remove Node", True, PygC.LEGEND_COLOR)
legend_clear_graph = font.render("Press 'SPACE' - Clear graph", True, PygC.LEGEND_COLOR)
legend_graph_size = font.render("Press 'S', 'M', 'L' - Change graph size", True, PygC.LEGEND_COLOR)
legend_dijkstra = font.render("Dijkstra - Press 'D'", True, PygC.LEGEND_COLOR)
legend_a_star = font.render("A* - Press 'A'", True, PygC.LEGEND_COLOR)
legend_bi_dijkstra = font.render("Bi-directional Dijkstra - Press 'B'", True, PygC.LEGEND_COLOR)
legend_recursive_maze = font.render("Generate maze - Press 'G'", True, PygC.LEGEND_COLOR)
legend_instant_recursive_maze = font.render("Generate maze (Instantly) - Press 'I'", True, PygC.LEGEND_COLOR)

vis_text_dijkstra = font.render("Visualizing Dijkstra...", True, PygC.VIS_COLOR)
vis_text_a_star = font.render("Visualizing A*...", True, PygC.VIS_COLOR)
vis_text_bi_dijkstra = font.render("Visualizing Bi-directional Dijkstra...", True, PygC.VIS_COLOR)
vis_text_best_path = font.render("Laying best path...", True, PygC.VIS_COLOR)
vis_text_recursive_maze = font.render("Generating recursive maze...", True, PygC.VIS_COLOR)
vis_text_graph_size = font.render("Changing graph size... May take up to 30 seconds", True, PygC.VIS_COLOR)


# Used to reinstate walls after deletion for mazes and dragging
wall_nodes = set()


def set_graph() -> list:
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


def draw(graph, legend=False, display_update=True) -> None:
    """Main function to update the window. Called by all operations that updates the window."""

    # Sets background of graph to white and legend to grey
    WINDOW.fill(PygC.DEFAULT_COLOR)
    WINDOW.fill(PygC.LEGEND_AREA_COLOR, LEGEND_AREA)

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


def _draw_square(square_color, square_pos) -> None:
    """Draws square with color and correct positioning"""
    pygame.draw.rect(WINDOW, square_color, square_pos)


def _draw_lines() -> None:
    """Helper function to define the properties of the horizontal and vertical graph lines"""

    for i in range(rows):
        pygame.draw.line(WINDOW, PygC.LINE_COLOR,
                         (0, i * square_size), (WIDTH, i * square_size))
        pygame.draw.line(WINDOW, PygC.LINE_COLOR,
                         (i * square_size, 0), (i * square_size, WIDTH))


def _draw_legend() -> None:
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
                  is_best_path=False, is_recursive_maze=False, is_graph_size=False) -> None:
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


def reset_graph(graph) -> None:
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


def reset_algo(graph) -> None:
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


def change_graph_size(new_row_size) -> list:
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
