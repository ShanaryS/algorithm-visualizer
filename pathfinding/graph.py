"""Draws and updates graph for visualization"""


from dataclasses import dataclass
import pygame
from pathfinding.colors import *
from pathfinding.values import WIDTH_HEIGHT
from pathfinding.node import Square
from typing import Optional


@dataclass
class GraphState:
    """Stores the state of the graph. Changes with graph size."""

    rows: int
    square_size: float
    wall_nodes: set
    img: bool
    img_file: Optional[bytes]


# Defining window properties as well as graph size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 879
WIDTH = WIDTH_HEIGHT
HEIGHT = WIDTH_HEIGHT
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
LEGEND_AREA = pygame.Rect(0, HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - HEIGHT)
pygame.display.set_caption("Pathfinding Visualizer - github.com/ShanaryS/algorithm-visualizer")


# Creates the text needed for legend and when visualizing
pygame.font.init()
FONT = pygame.font.SysFont('Comic Sans MS', 12)

legend_add_node = FONT.render("Left Click - Add Node (Start -> End -> Walls)", True, LEGEND_COLOR)
legend_add_mid_node = FONT.render("Middle Click - Add mid node", True, LEGEND_COLOR)
legend_remove_node = FONT.render("Right Click - Remove Node", True, LEGEND_COLOR)
legend_clear_graph = FONT.render("Press 'SPACE' - Clear graph", True, LEGEND_COLOR)
legend_graph_size = FONT.render("Press 'S', 'M', 'L' - Change graph size", True, LEGEND_COLOR)
legend_dijkstra = FONT.render("Dijkstra - Press 'D'", True, LEGEND_COLOR)
legend_a_star = FONT.render("A* - Press 'A'", True, LEGEND_COLOR)
legend_bi_dijkstra = FONT.render("Bi-directional Dijkstra - Press 'B'", True, LEGEND_COLOR)
legend_recursive_maze = FONT.render("Generate maze - Press 'G'", True, LEGEND_COLOR)
legend_instant_recursive_maze = FONT.render("Generate maze (Instantly) - Press 'I'", True, LEGEND_COLOR)

vis_text_dijkstra = FONT.render("Visualizing Dijkstra...", True, VIS_COLOR)
vis_text_a_star = FONT.render("Visualizing A*...", True, VIS_COLOR)
vis_text_bi_dijkstra = FONT.render("Visualizing Bi-directional Dijkstra...", True, VIS_COLOR)
vis_text_best_path = FONT.render("Laying best path...", True, VIS_COLOR)
vis_text_recursive_maze = FONT.render("Generating recursive maze...", True, VIS_COLOR)
vis_text_graph_size = FONT.render("Changing graph size... May take up to 30 seconds", True, VIS_COLOR)


def set_graph(gph: GraphState) -> list:
    """Creates the graph object that stores the location of all the squares"""

    graph = []
    for i in range(gph.rows):
        graph.append([])
        for j in range(gph.rows):
            # Uses Square class to create square object with necessary attributes
            square = Square(i, j)

            # Necessary for when changing graph size
            square.update_values(gph.rows, gph.square_size)

            graph[i].append(square)

    return graph


def draw(graph, gph: GraphState, legend=False, display_update=True) -> None:
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
    if gph.img:
        _draw_img(gph)
    _draw_lines(gph)

    # Legend is only shown if graph can be interacted with
    if legend:
        _draw_legend()

    # Display may not want to update display immediately before doing other operations
    if display_update:
        pygame.display.update()


def _draw_square(square_color, square_pos) -> None:
    """Draws square with color and correct positioning"""
    pygame.draw.rect(WINDOW, square_color, square_pos)


def _draw_lines(gph: GraphState) -> None:
    """Helper function to define the properties of the horizontal and vertical graph lines"""

    for i in range(gph.rows):
        pygame.draw.line(WINDOW, LINE_COLOR,
                         (0, i * gph.square_size), (WIDTH, i * gph.square_size))
        pygame.draw.line(WINDOW, LINE_COLOR,
                         (i * gph.square_size, 0), (i * gph.square_size, WIDTH))


def _draw_img(gph: GraphState) -> pygame.Rect:
    """Draws the maps image onto the graph"""
    img = gph.img_file
    return WINDOW.blit(img, (0, 0))


def set_squares_to_roads(graph, gph: GraphState) -> None:
    """Gets the color of a single pixel"""

    for a in range(len(graph)):
        for b in range(len(graph[0])):
            square = graph[a][b]
            total = 0
            for i in range(square.col * int(gph.square_size), (square.col+1) * int(gph.square_size)):
                for j in range(square.row * int(gph.square_size), (square.row+1) * int(gph.square_size)):
                    temp = WINDOW.get_at((i, j))
                    total += temp[0] + temp[1] + temp[2] + temp[3]
            avg = total / gph.square_size**2 / 4
            print(avg)

            if avg > 210:
                square.reset()
            else:
                square.set_wall()

    gph.img = False


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


def reset_graph(graph, gph: GraphState, algo) -> None:
    """Resets entire graph removing every square"""

    # Need to update these values
    algo.dijkstra_finished = False
    algo.a_star_finished = False
    algo.bi_dijkstra_finished = False
    algo.maze = False

    # Resets each square
    for i in range(gph.rows):
        for j in range(gph.rows):
            square = graph[i][j]
            square.reset()


def reset_algo(graph, gph: GraphState, algo) -> None:
    """Resets algo colors while keeping ordinal nodes and walls"""

    # Need to update these values
    algo.dijkstra_finished = False
    algo.a_star_finished = False
    algo.bi_dijkstra_finished = False

    # Resets only certain colors
    for i in range(gph.rows):
        for j in range(gph.rows):
            square = graph[i][j]
            if square.is_open() or square.is_open_alt() or square.is_open_alt_()\
                    or square.is_closed() or square.is_path():
                square.reset()


def change_graph_size(new_row_size, gph: GraphState) -> list:
    """Changes graph size and updates squares and their locations as well.
    Restricted to certain sizes as recursive maze breaks otherwise
    """

    # Displays text that size is changing
    draw_vis_text(is_graph_size=True)

    # Updates rows and square size with new values
    gph.rows = new_row_size
    gph.square_size = WIDTH / gph.rows

    # Recreates graph with new values
    graph = set_graph(gph)
    draw(graph, gph)

    return graph
