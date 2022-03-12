"""Draws and updates graph for visualization"""


from src.pathfinding.colors import *
from dataclasses import dataclass
import pygame
from src.pathfinding.values import ROWS, SQUARE_SIZE, WIDTH_HEIGHT
from src.pathfinding.node import Square
from typing import Optional
from src.timer import timer_start, timer_end, timer_print


# Defining window properties as well as graph size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 879
WIDTH = WIDTH_HEIGHT
HEIGHT = WIDTH_HEIGHT
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
GRAPH_RECT = pygame.Rect(0, 0, WINDOW_WIDTH, HEIGHT)
LEGEND_RECT = pygame.Rect(0, HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - HEIGHT)
pygame.display.set_caption(
    "Pathfinding Visualizer - github.com/ShanaryS/algorithm-visualizer"
)
pygame.font.init()

# Other constants
DEFAULT_SPEED_MULTIPLIER = 1


@dataclass
class GraphState:
    """Stores the state of the graph. Changes with graph size."""

    graph: list
    rects_to_update: list
    base_drawn: bool = False
    update_legend: bool = False
    update_entire_screen: bool = False
    rows: int = ROWS
    square_size: float = SQUARE_SIZE
    has_img: bool = False
    img: Optional[bytes] = None
    visualize_node_history: bool = False

    # These control the speed of the program. The last is used for speeding up certain parts when necessary.
    FPS: int = 240
    speed_multiplier: int = DEFAULT_SPEED_MULTIPLIER

    def add_to_update_queue(self, obj) -> None:
        """Adds rect to update, converts non rects to rect"""

        if isinstance(obj, Square):
            square_color, square_pos = obj.draw_square()
            obj = _draw_square(square_color, square_pos)

        self.rects_to_update.append(obj)


@dataclass
class VisText:
    """Creates the text needed for legend and when visualizing"""

    address: str = ""

    FONT = pygame.font.SysFont("Comic Sans MS", 12)

    legend_add_node = FONT.render(
        "Left Click - Add Node (Start -> End -> Walls)", True, LEGEND_COLOR
    )
    legend_add_mid_node = FONT.render("Middle Click - Add mid node", True, LEGEND_COLOR)
    legend_remove_node = FONT.render("Right Click - Remove Node", True, LEGEND_COLOR)
    legend_clear_graph = FONT.render("Press 'SPACE' - Clear graph", True, LEGEND_COLOR)
    legend_graph_size = FONT.render(
        "Press 'S', 'M', 'L' - Change graph size", True, LEGEND_COLOR
    )
    legend_dijkstra = FONT.render("Dijkstra - Press 'D'", True, LEGEND_COLOR)
    legend_a_star = FONT.render("A* - Press 'A'", True, LEGEND_COLOR)
    legend_bi_dijkstra = FONT.render(
        "Bi-directional Dijkstra - Press 'B'", True, LEGEND_COLOR
    )
    legend_recursive_maze = FONT.render("Generate maze - Press 'G'", True, LEGEND_COLOR)
    legend_instant_recursive_maze = FONT.render(
        "Generate maze (Invisible) - Press 'I'", True, LEGEND_COLOR
    )
    legend_address = FONT.render(
        "Press 'Enter' to visit anywhere in the world!", True, LEGEND_COLOR
    )
    legend_convert_map = FONT.render(
        "Press 'C' to convert location into the graph", True, LEGEND_COLOR
    )
    legend_node_history = FONT.render(
        "Track changes on graph - Press 'V'", True, LEGEND_COLOR
    )
    legend_node_history_show = FONT.render(
        "Storing changes for node history... Press 'V' to show", True, VIS_COLOR
    )

    vis_text_dijkstra = FONT.render("Visualizing Dijkstra...", True, VIS_COLOR)
    vis_text_a_star = FONT.render("Visualizing A*...", True, VIS_COLOR)
    vis_text_bi_dijkstra = FONT.render(
        "Visualizing Bi-directional Dijkstra...", True, VIS_COLOR
    )
    vis_text_best_path = FONT.render("Laying best path...", True, VIS_COLOR)
    vis_text_recursive_maze = FONT.render(
        "Generating recursive maze...", True, VIS_COLOR
    )
    vis_text_graph_size = FONT.render("Changing graph size...", True, VIS_COLOR)
    vis_text_input = FONT.render(
        "Enter an address (NO COMMAS, ONLY SPACES):", True, LEGEND_COLOR
    )
    vis_text_address = FONT.render(f"{address}", True, LEGEND_COLOR)

    def update_vis_text_input(self) -> None:
        """Updates vis_text_input with new input_text"""
        self.vis_text_address = self.FONT.render(f"{self.address}", True, LEGEND_COLOR)


def set_graph(gph: GraphState) -> None:
    """Creates the graph object that stores the location of all the squares"""

    # Changing so many nodes, faster to update entire screen
    gph.update_entire_screen = True

    # Clear lists from previous graph
    Square.clear_all_node_lists()

    gph.graph = []
    for row in range(gph.rows):
        gph.graph.append([])
        for col in range(gph.rows):
            # Uses Square class to create square object with necessary attributes
            square = Square(row, col, gph.rows, gph.square_size)
            gph.graph[row].append(square)

    # Updates neighbours
    square: Square
    for row in gph.graph:
        for square in row:
            square.update_neighbours(gph)


def draw(
    gph: GraphState,
    txt: VisText,
    legend=False,
    clear_legend=False,
    algo_running=False,
) -> None:
    """Main function to update the window. Called by all operations that updates the window."""

    if clear_legend:
        gph.add_to_update_queue(WINDOW.fill(LEGEND_AREA_COLOR, LEGEND_RECT))

    # Draws the horizontal and vertical lines on the graph unless it has image
    if not gph.base_drawn:
        if gph.has_img:
            _draw_img(gph)
        else:
            # Sets background of graph to white
            gph.add_to_update_queue(WINDOW.fill(DEFAULT_COLOR, GRAPH_RECT))
            _draw_lines(gph)
        # Sets background of legend to grey
        gph.add_to_update_queue(WINDOW.fill(LEGEND_AREA_COLOR, LEGEND_RECT))

        if legend:
            _draw_legend(gph, txt)

        gph.base_drawn = True
    else:
        if not legend and not algo_running:
            gph.base_drawn = False

    if gph.update_legend:
        gph.update_legend = False
        gph.add_to_update_queue(WINDOW.fill(LEGEND_AREA_COLOR, LEGEND_RECT))
        _draw_legend(gph, txt)

    # Decides how much of the display to update
    if gph.update_entire_screen:
        # Pygame chokes when updating a lot of rects that covers the screen
        # So we just upate the entire screen like this instead
        gph.update_entire_screen = False
        pygame.display.update()
        gph.rects_to_update.clear()
    else:
        # Queues all changed squares to visualize change
        if gph.visualize_node_history:
            gph.visualize_node_history = False
            for square in Square.get_node_history():
                square.set_history()
                gph.add_to_update_queue(square)
            Square.clear_node_history()
        # Queues all changed squares to update
        else:
            square: Square
            for square in Square.get_nodes_to_update():
                gph.add_to_update_queue(square)


    _draw_square_borders(gph)

    if gph.rects_to_update:
        pygame.display.update(gph.rects_to_update)
        
        # Used to reset squares to previous color like nothing happened
        for square in Square.get_all_history_nodes():
            square.color = square.color_history
            square.color_history = None

    # Clear update queues
    Square.clear_nodes_to_update()
    Square.clear_history_nodes()
    gph.rects_to_update.clear()


def _draw_square(square_color, square_pos) -> None:
    """Draws square with color and correct positioning"""
    return pygame.draw.rect(WINDOW, square_color, square_pos)


def _draw_square_borders(gph: GraphState) -> None:
    """Draws the lines surrounding the updating squares"""

    square: Square
    for square in Square.get_nodes_to_update():
        top_left = square.x, square.y
        top_right = square.x, square.y + gph.square_size
        bottom_left = square.x + gph.square_size, square.y
        bottom_right = square.x + gph.square_size, square.y + gph.square_size

        # Top
        pygame.draw.line(WINDOW, LINE_COLOR, top_left, top_right)
        # Right
        pygame.draw.line(WINDOW, LINE_COLOR, top_right, bottom_right)
        # Bottom
        pygame.draw.line(WINDOW, LINE_COLOR, bottom_left, bottom_right)
        # Left
        pygame.draw.line(WINDOW, LINE_COLOR, top_left, bottom_left)


def _draw_lines(gph: GraphState) -> None:
    """Helper function to define the properties of the horizontal and vertical graph lines"""

    for i in range(gph.rows):
        row = col = i * gph.square_size

        # Horizonatal lines
        pygame.draw.line(WINDOW, LINE_COLOR, (0, row), (WIDTH, row))
        # Vertical lines
        pygame.draw.line(WINDOW, LINE_COLOR, (col, 0), (col, WIDTH))


def _draw_img(gph: GraphState) -> None:
    """Draws the maps image onto the graph"""
    gph.add_to_update_queue(WINDOW.blit(gph.img, (0, 0)))


def set_squares_to_roads(gph: GraphState) -> None:
    """Sets squares to the color of a single pixel"""

    gph.update_entire_screen = True

    # These two loops x,y gets all the squares in the graph. At 400 graph size a square is a pixel.
    for x in range(len(gph.graph)):
        for y in range(len(gph.graph[0])):
            square: Square = gph.graph[x][y]
            square.wall_color = WALL_COLOR_MAP  # Change wall color for easy visibility
            tot = 0
            tot_b = 0  # Used to check if highway since they are yellow.

            # These two loops i,j get each pixel in each square. Time Complexity is O(n) in regards to pixels.
            for i in range(
                square.row * int(gph.square_size),
                (square.row + 1) * int(gph.square_size),
            ):
                for j in range(
                    square.col * int(gph.square_size),
                    (square.col + 1) * int(gph.square_size),
                ):
                    r, g, b, a = WINDOW.get_at((i, j))
                    tot += r + g + b
                    tot_b += b
            avg_tot = tot / gph.square_size ** 2 / 3  # Gets the average of each square
            avg_b = tot_b / gph.square_size ** 2
            cutoff = 1  # Any color with value above this will be set as a viable path

            # If the square's color is above cutoff, set it as path. Else wall node
            if avg_tot > cutoff:
                # If b is greater, then it is white.
                if avg_b > 225:
                    square.reset()
                else:
                    square.reset()
                    square.is_highway = True
            else:
                square.set_wall(gph)


def _draw_legend(gph: GraphState, txt: VisText) -> None:
    """Helper function to define the location of the legend"""

    # center_graph = HEIGHT//2
    center_legend_area = HEIGHT + (WINDOW_HEIGHT - HEIGHT) // 2

    if not gph.has_img:
        # Left legend
        WINDOW.blit(txt.legend_add_node, (2, 15 * 53.1 + 3))
        WINDOW.blit(txt.legend_add_mid_node, (2, 15 * 54.1 + 3))
        WINDOW.blit(txt.legend_remove_node, (2, 15 * 55.1 + 3))
        WINDOW.blit(txt.legend_clear_graph, (2, 15 * 56.1 + 3))
        WINDOW.blit(txt.legend_graph_size, (2, 15 * 57.1 + 3))

        # Right legend
        WINDOW.blit(
            txt.legend_dijkstra,
            (WIDTH - txt.legend_dijkstra.get_width() - 2, 15 * 53.1 + 3),
        )
        WINDOW.blit(
            txt.legend_a_star,
            (WIDTH - txt.legend_a_star.get_width() - 2, 15 * 54.1 + 3),
        )
        WINDOW.blit(
            txt.legend_bi_dijkstra,
            (WIDTH - txt.legend_bi_dijkstra.get_width() - 2, 15 * 55.1 + 3),
        )
        WINDOW.blit(
            txt.legend_recursive_maze,
            (WIDTH - txt.legend_recursive_maze.get_width() - 2, 15 * 56.1 + 3),
        )
        WINDOW.blit(
            txt.legend_instant_recursive_maze,
            (WIDTH - txt.legend_instant_recursive_maze.get_width() - 2, 15 * 57.1 + 3),
        )

    # Center Legend
    WINDOW.blit(
        txt.legend_address,
        (
            WIDTH // 2 - txt.legend_address.get_width() // 2,
            center_legend_area - txt.legend_address.get_height() // 2,
        ),
    )
    if Square.track_node_history:
        WINDOW.blit(
            txt.legend_node_history_show,
            (
                WIDTH // 2 - txt.legend_node_history_show.get_width() // 2,
                center_legend_area - txt.legend_node_history_show.get_height() // 2 + 30,
            ),
        )
    else:
        WINDOW.blit(
            txt.legend_node_history,
            (
                WIDTH // 2 - txt.legend_node_history.get_width() // 2,
                center_legend_area - txt.legend_node_history.get_height() // 2 + 30,
            ),
        )
    if gph.has_img:
        WINDOW.blit(
            txt.legend_convert_map,
            (
                WIDTH // 2 - txt.legend_convert_map.get_width() // 2,
                center_legend_area - txt.legend_convert_map.get_height() // 2 + 15,
            ),
        )



def draw_vis_text(
    txt: VisText,
    is_dijkstra=False,
    is_a_star=False,
    is_bi_dijkstra=False,
    is_best_path=False,
    is_recursive_maze=False,
    is_graph_size=False,
    is_input=False,
) -> None:
    """Special text indicating some operation is being performed. No inputs are registered."""

    # Defines the center of the graph and legend for text placement
    center_graph = HEIGHT // 2
    center_legend_area = HEIGHT + (WINDOW_HEIGHT - HEIGHT) // 2

    text_rect = []  # Used to only update text area

    # Text to be shown depending on operation
    if is_dijkstra:
        text_rect.append(
            WINDOW.blit(
                txt.vis_text_dijkstra,
                (
                    WIDTH // 2 - txt.vis_text_dijkstra.get_width() // 2,
                    center_legend_area - txt.vis_text_dijkstra.get_height() // 2 - 10,
                ),
            )
        )
    elif is_a_star:
        text_rect.append(
            WINDOW.blit(
                txt.vis_text_a_star,
                (
                    WIDTH // 2 - txt.vis_text_a_star.get_width() // 2,
                    center_legend_area - txt.vis_text_a_star.get_height() // 2 - 10,
                ),
            )
        )
    elif is_bi_dijkstra:
        text_rect.append(
            WINDOW.blit(
                txt.vis_text_bi_dijkstra,
                (
                    WIDTH // 2 - txt.vis_text_bi_dijkstra.get_width() // 2,
                    center_legend_area
                    - txt.vis_text_bi_dijkstra.get_height() // 2
                    - 10,
                ),
            )
        )
    elif is_best_path:
        text_rect.append(
            WINDOW.blit(
                txt.vis_text_best_path,
                (
                    WIDTH // 2 - txt.vis_text_best_path.get_width() // 2,
                    center_legend_area - txt.vis_text_best_path.get_height() // 2 + 10,
                ),
            )
        )
    elif is_recursive_maze:
        text_rect.append(
            WINDOW.blit(
                txt.vis_text_recursive_maze,
                (
                    WIDTH // 2 - txt.vis_text_recursive_maze.get_width() // 2,
                    center_legend_area - txt.vis_text_recursive_maze.get_height() // 2,
                ),
            )
        )
    elif is_graph_size:
        text_rect.append(
            WINDOW.blit(
                txt.vis_text_graph_size,
                (
                    WIDTH // 2 - txt.vis_text_graph_size.get_width() // 2,
                    center_graph - txt.vis_text_graph_size.get_height() // 2,
                ),
            )
        )
    elif is_input:
        # Reset legend area (inefficient, only need area with new text)
        text_rect.append(WINDOW.fill(LEGEND_AREA_COLOR, LEGEND_RECT))

        # Instructions on what to type
        text_rect.append(
            WINDOW.blit(
                txt.vis_text_input,
                (
                    WIDTH // 2 - txt.vis_text_input.get_width() // 2,
                    center_legend_area - txt.vis_text_input.get_height() // 2 - 15,
                ),
            )
        )
        # Update text with new input
        txt.update_vis_text_input()
        text_rect.append(
            WINDOW.blit(
                txt.vis_text_address,
                (
                    WIDTH // 2 - txt.vis_text_address.get_width() // 2,
                    center_legend_area - txt.vis_text_address.get_height() // 2,
                ),
            )
        )

    # Updates the portion of the screen that contains changing text
    pygame.display.update(text_rect)


def reset_graph(
    gph: GraphState, algo, txt: VisText, graph_max=None, graph_default=None, reset=True
) -> None:
    """Resets entire graph removing every square"""

    # Need to update these values
    gph.speed_multiplier = DEFAULT_SPEED_MULTIPLIER
    gph.has_img = False
    algo.dijkstra_finished = False
    algo.a_star_finished = False
    algo.bi_dijkstra_finished = False
    algo.maze = False

    # Resets each square
    if reset:
        # If reseting graph from map, not a circular call
        if gph.rows == graph_max:
            change_graph_size(gph, algo, txt, graph_default)
            return

        # Default case
        for i in range(gph.rows):
            for j in range(gph.rows):
                square: Square = gph.graph[i][j]
                square.wall_color = WALL_COLOR
                square.reset()


def reset_algo(algo) -> None:
    """Resets algo colors while keeping ordinal nodes and walls"""

    # Need to update these values
    algo.dijkstra_finished = False
    algo.a_star_finished = False
    algo.bi_dijkstra_finished = False

    # Resets only certain colors
    nodes_to_reset = [
        Square.all_open_nodes,
        Square.all_open_nodes_alt,
        Square.all_open_nodes_alt_,
        Square.all_closed_nodes,
        Square.all_closed_nodes_alt,
        Square.all_closed_nodes_alt_,
        Square.all_path_nodes,
    ]
    square: Square
    for type_list in nodes_to_reset:
        for square in type_list:
            square.reset()


def change_graph_size(
    gph: GraphState, algo, txt: VisText, new_row_size, to_draw=True
) -> None:
    """Changes graph size and updates squares and their locations as well.
    Restricted to certain sizes as recursive maze breaks otherwise
    """

    # Displays text that size is changing
    # draw_vis_text(txt, is_graph_size=True)  # So fast now it's not worth it.

    # Updates rows and square size with new values
    reset_graph(gph, algo, txt, reset=False)
    gph.rows = new_row_size
    gph.square_size = WIDTH / gph.rows

    # Recreates graph with new values
    set_graph(gph)
    if to_draw:
        draw(gph, txt)
