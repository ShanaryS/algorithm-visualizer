"""Draws and updates graph for visualization"""


from dataclasses import dataclass
import pygame
from pathfinding.colors import *
from pathfinding.values import ROWS, SQUARE_SIZE, WIDTH_HEIGHT
from pathfinding.node import Square
from typing import Optional


# Defining window properties as well as graph size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 879
WIDTH = WIDTH_HEIGHT
HEIGHT = WIDTH_HEIGHT
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
LEGEND_AREA = pygame.Rect(0, HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - HEIGHT)
pygame.display.set_caption("Pathfinding Visualizer - github.com/ShanaryS/algorithm-visualizer")
pygame.font.init()


@dataclass
class GraphState:
    """Stores the state of the graph. Changes with graph size."""

    graph: list
    wall_nodes: set
    rows: int = ROWS
    square_size: float = SQUARE_SIZE
    has_img: bool = False
    img: Optional[bytes] = None

    # These control the speed of the program. The last is used for speeding up certain parts when necessary.
    FPS: int = 240
    speed_multiplier: int = 1


@dataclass
class VisText:
    """Creates the text needed for legend and when visualizing"""

    address: str = ""

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
    legend_address = FONT.render("Press 'Enter' to visit anywhere in the world!", True, LEGEND_COLOR)
    legend_convert_map = FONT.render("Press 'C' to convert location into the graph", True, LEGEND_COLOR)

    vis_text_dijkstra = FONT.render("Visualizing Dijkstra...", True, VIS_COLOR)
    vis_text_a_star = FONT.render("Visualizing A*...", True, VIS_COLOR)
    vis_text_bi_dijkstra = FONT.render("Visualizing Bi-directional Dijkstra...", True, VIS_COLOR)
    vis_text_best_path = FONT.render("Laying best path...", True, VIS_COLOR)
    vis_text_recursive_maze = FONT.render("Generating recursive maze...", True, VIS_COLOR)
    vis_text_graph_size = FONT.render("Changing graph size... May take up to 30 seconds", True, VIS_COLOR)
    vis_text_input = FONT.render("Enter an address (NO COMMAS, ONLY SPACES):", True, LEGEND_COLOR)
    vis_text_address = FONT.render(f"{address}", True, LEGEND_COLOR)

    def update_vis_text_input(self) -> None:
        """Updates vis_text_input with new input_text"""
        self.vis_text_address = self.FONT.render(f"{self.address}", True, LEGEND_COLOR)


def set_graph(gph: GraphState) -> None:
    """Creates the graph object that stores the location of all the squares"""

    gph.graph = []
    for i in range(gph.rows):
        gph.graph.append([])
        for j in range(gph.rows):
            # Uses Square class to create square object with necessary attributes
            square = Square(i, j)

            # Necessary for when changing graph size
            square.update_values(gph.rows, gph.square_size)

            gph.graph[i].append(square)


def draw(gph: GraphState, txt: VisText, legend=False, display_update=True) -> None:
    """Main function to update the window. Called by all operations that updates the window."""

    # Sets background of graph to white and legend to grey
    WINDOW.fill(DEFAULT_COLOR)
    WINDOW.fill(LEGEND_AREA_COLOR, LEGEND_AREA)

    # If colors of square were updated, reflected here
    for row in gph.graph:
        for square in row:
            square_color, square_pos = square.draw_square()
            _draw_square(square_color, square_pos)

    # Draws the horizontal and vertical lines on the graph
    _draw_lines(gph)
    if gph.has_img:
        _draw_img(gph)

    # Legend is only shown if graph can be interacted with
    if legend:
        _draw_legend(gph, txt)

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
    img = gph.img
    return WINDOW.blit(img, (0, 0))


def set_squares_to_roads(gph: GraphState) -> None:
    """Gets the color of a single pixel"""

    # These two loops x,y gets all the squares in the graph. At 400 graph size a square is a pixel.
    for x in range(len(gph.graph)):
        for y in range(len(gph.graph[0])):
            square = gph.graph[x][y]
            square.wall_color = WALL_COLOR_MAP
            tot = 0
            tot_b = 0  # Used to check if highway since they are yellow.

            # These two loops i,j get each pixel in each square. Time Complexity is O(n) in regards to pixels.
            for i in range(square.row * int(gph.square_size), (square.row+1) * int(gph.square_size)):
                for j in range(square.col * int(gph.square_size), (square.col+1) * int(gph.square_size)):
                    r, g, b, a = WINDOW.get_at((i, j))
                    tot += r + g + b
                    tot_b += b
            avg_tot = tot / gph.square_size**2 / 3  # Gets the average of each square
            avg_b = tot_b / gph.square_size**2
            cutoff = 1  # Any color with value above this will be set as a viable path

            # If the square's color is above cutoff, set it as path. Else wall node
            if avg_tot > cutoff:
                # If b is greater, then it is white.
                if avg_b > 225:
                    square.reset()
                else:
                    square.set_highway()
            else:
                square.set_wall()
                gph.wall_nodes.add(square)


def _draw_legend(gph: GraphState, txt: VisText) -> None:
    """Helper function to define the location of the legend"""

    # center_graph = HEIGHT//2
    center_legend_area = HEIGHT + (WINDOW_HEIGHT - HEIGHT)//2

    if not gph.has_img:
        # Left legend
        WINDOW.blit(txt.legend_add_node, (2, 15*53.1 + 3))
        WINDOW.blit(txt.legend_add_mid_node, (2, 15*54.1 + 3))
        WINDOW.blit(txt.legend_remove_node, (2, 15*55.1 + 3))
        WINDOW.blit(txt.legend_clear_graph, (2, 15*56.1 + 3))
        WINDOW.blit(txt.legend_graph_size, (2, 15*57.1 + 3))

        # Right legend
        WINDOW.blit(txt.legend_dijkstra, (WIDTH - txt.legend_dijkstra.get_width()-2, 15*53.1 + 3))
        WINDOW.blit(txt.legend_a_star, (WIDTH - txt.legend_a_star.get_width()-2, 15*54.1 + 3))
        WINDOW.blit(txt.legend_bi_dijkstra, (WIDTH - txt.legend_bi_dijkstra.get_width()-2, 15*55.1 + 3))
        WINDOW.blit(txt.legend_recursive_maze, (WIDTH - txt.legend_recursive_maze.get_width()-2, 15*56.1 + 3))
        WINDOW.blit(txt.legend_instant_recursive_maze,
                    (WIDTH - txt.legend_instant_recursive_maze.get_width()-2, 15*57.1 + 3))

    # Center Legend
    WINDOW.blit(txt.legend_address,
                (WIDTH // 2 - txt.legend_address.get_width() // 2,
                 center_legend_area - txt.legend_address.get_height() // 2))
    if gph.has_img:
        WINDOW.blit(txt.legend_convert_map,
                    (WIDTH // 2 - txt.legend_convert_map.get_width() // 2,
                     center_legend_area - txt.legend_convert_map.get_height() // 2 + 15))


def draw_vis_text(txt: VisText, is_dijkstra=False, is_a_star=False, is_bi_dijkstra=False, is_best_path=False,
                  is_recursive_maze=False, is_graph_size=False, is_input=False) -> None:
    """Special text indicating some operation is being performed. No inputs are registered."""

    # Defines the center of the graph and legend for text placement
    center_graph = HEIGHT//2
    center_legend_area = HEIGHT + (WINDOW_HEIGHT - HEIGHT)//2

    # Text to be shown depending on operation
    if is_dijkstra:
        WINDOW.blit(txt.vis_text_dijkstra,
                    (WIDTH//2 - txt.vis_text_dijkstra.get_width()//2,
                     center_legend_area - txt.vis_text_dijkstra.get_height()//2))
    elif is_a_star:
        WINDOW.blit(txt.vis_text_a_star,
                    (WIDTH//2 - txt.vis_text_a_star.get_width()//2,
                     center_legend_area - txt.vis_text_a_star.get_height()//2))
    elif is_bi_dijkstra:
        WINDOW.blit(txt.vis_text_bi_dijkstra,
                    (WIDTH//2 - txt.vis_text_bi_dijkstra.get_width()//2,
                     center_legend_area - txt.vis_text_bi_dijkstra.get_height()//2))
    elif is_best_path:
        WINDOW.blit(txt.vis_text_best_path,
                    (WIDTH // 2 - txt.vis_text_best_path.get_width() // 2,
                     center_legend_area - txt.vis_text_best_path.get_height() // 2))
    elif is_recursive_maze:
        WINDOW.blit(txt.vis_text_recursive_maze,
                    (WIDTH//2 - txt.vis_text_recursive_maze.get_width()//2,
                     center_legend_area - txt.vis_text_recursive_maze.get_height()//2))
    elif is_graph_size:
        WINDOW.blit(txt.vis_text_graph_size,
                    (WIDTH//2 - txt.vis_text_graph_size.get_width()//2,
                     center_graph - txt.vis_text_graph_size.get_height()//2))
    elif is_input:
        WINDOW.blit(txt.vis_text_input,
                    (WIDTH // 2 - txt.vis_text_input.get_width() // 2,
                     center_legend_area - txt.vis_text_input.get_height() // 2 - 15))
        txt.update_vis_text_input()
        WINDOW.blit(txt.vis_text_address,
                    (WIDTH // 2 - txt.vis_text_address.get_width() // 2,
                     center_legend_area - txt.vis_text_address.get_height() // 2))

    # Always called after draw. In that scenario draw won't update display so this will
    pygame.display.update()


def reset_graph(gph: GraphState, algo) -> None:
    """Resets entire graph removing every square"""

    # Need to update these values
    algo.dijkstra_finished = False
    algo.a_star_finished = False
    algo.bi_dijkstra_finished = False
    algo.maze = False
    gph.speed_multiplier = 1

    # Resets each square
    for i in range(gph.rows):
        for j in range(gph.rows):
            square = gph.graph[i][j]
            square.wall_color = WALL_COLOR
            square.reset()


def reset_algo(gph: GraphState, algo) -> None:
    """Resets algo colors while keeping ordinal nodes and walls"""

    # Need to update these values
    algo.dijkstra_finished = False
    algo.a_star_finished = False
    algo.bi_dijkstra_finished = False

    # Resets only certain colors
    for i in range(gph.rows):
        for j in range(gph.rows):
            square = gph.graph[i][j]
            if square.is_open() or square.is_open_alt() or square.is_open_alt_()\
                    or square.is_closed() or square.is_path():
                square.reset()


def change_graph_size(gph: GraphState, algo, txt: VisText, new_row_size) -> None:
    """Changes graph size and updates squares and their locations as well.
    Restricted to certain sizes as recursive maze breaks otherwise
    """

    # Displays text that size is changing
    draw_vis_text(txt, is_graph_size=True)

    # Updates rows and square size with new values
    reset_graph(gph, algo)
    gph.rows = new_row_size
    gph.square_size = WIDTH / gph.rows

    # Recreates graph with new values
    set_graph(gph)
    draw(gph, txt)
