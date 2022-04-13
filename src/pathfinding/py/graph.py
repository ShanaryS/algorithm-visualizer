"""Draws and updates graph for visualization"""


# Handles how much C++ the the program should use
from src.pathfinding.cpp_or_py import use_square_h, use_algorithms_h
if use_square_h:
    from src.pathfinding.cpp.modules import Square
elif use_algorithms_h:
    from src.pathfinding.cpp.modules import Square, AlgoState
else:
    from src.pathfinding.py.square import Square
    from src.pathfinding.py.algorithms import AlgoState
from lib.cpp_py_lock import CppPyLock

import pygame
from dataclasses import dataclass


# Colors
DEFAULT_COLOR = (255, 255, 255)
LINE_COLOR = (128, 128, 128)
LEGEND_COLOR = (0, 0, 0)
LEGEND_AREA_COLOR = (128, 128, 128)
VIS_COLOR = (255, 0, 0)

# Defining window properties as well as graph size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 879
WIDTH = WINDOW_WIDTH
HEIGHT = WINDOW_WIDTH
GRAPH_RECT = pygame.Rect(0, 0, WINDOW_WIDTH, HEIGHT)
LEGEND_RECT = pygame.Rect(0, HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - HEIGHT)
pygame.font.init()

# Other constants
CENTER_GRAPH = HEIGHT // 2
CENTER_LEGEND_AREA = HEIGHT + (WINDOW_HEIGHT - HEIGHT) // 2


@dataclass(slots=True)
class GraphState:
    """Stores the state of the graph. Changes with graph size."""

    rects_to_update: list
    window: pygame.Surface = None
    base_drawn: bool = False
    update_legend: bool = False
    update_entire_screen: bool = False
    has_img: bool = False
    img: bytes = None
    visualize_square_history: bool = False

    # These control the speed of the program. The last is used for speeding up certain parts when necessary.
    FPS: int = 1000

    def create_pygame_window(self) -> None:
        """Create the pygame window."""
        title = "Pathfinding Visualizer"
        if any([use_algorithms_h, use_square_h]):
            title += " (#include "
            title += "algorithms.h, " if use_algorithms_h else ""
            title += "square.h" if use_square_h else ""
            title += ")"
        pygame.display.set_caption(title)
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    def add_to_update_queue(self, obj) -> None:
        """Adds rect to update, converts non rects to rect"""

        if isinstance(obj, Square):
            square_color = obj.get_color()
            square_pos = obj.draw_square()
            obj = _draw_square(self, square_color, square_pos)

        self.rects_to_update.append(obj)


@dataclass
class VisText:
    """Creates the text needed for legend and when visualizing"""

    address: str = ""
    algo_timer: str = ""

    FONT = pygame.font.SysFont("Comic Sans MS", 12)

    legend_add_square = FONT.render(
        "Left Click - Add square (Start -> End -> Walls)", True, LEGEND_COLOR
    )
    legend_add_mid_square = FONT.render("Middle Click - Add mid square", True, LEGEND_COLOR)
    legend_remove_square = FONT.render("Right Click - Remove square", True, LEGEND_COLOR)
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
        "Generate maze (Instant) - Press 'I'", True, LEGEND_COLOR
    )
    legend_address = FONT.render(
        "Press 'Enter' to visit anywhere in the world!", True, LEGEND_COLOR
    )
    legend_convert_map = FONT.render(
        "Press 'C' to convert location into the graph", True, LEGEND_COLOR
    )
    legend_square_history = FONT.render(
        "Track changes on graph - Press 'V'", True, LEGEND_COLOR
    )
    legend_square_history_show = FONT.render(
        "Storing changes for square history... Press 'V' to show", True, VIS_COLOR
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
        "Type an address then press 'Enter':", True, LEGEND_COLOR
    )
    vis_text_address = FONT.render(f"{address}", True, LEGEND_COLOR)
    vis_text_base_img = FONT.render(f"Getting base image...", True, VIS_COLOR)
    vis_text_clean_img = FONT.render(f"Getting clean image...", True, VIS_COLOR)
    vis_text_converting_img = FONT.render(f"Converting image...", True, VIS_COLOR)
    vis_text_algo_timer = FONT.render(f"{algo_timer}", True, LEGEND_COLOR)

    def update_vis_text_address(self) -> None:
        """Updates vis_text_address with new input_text"""
        self.vis_text_address = self.FONT.render(f"{self.address}", True, LEGEND_COLOR)

    def update_vis_text_algo_timer(self) -> None:
        """Updates vix_text_algo_timer with new time"""
        self.vis_text_algo_timer = self.FONT.render(
            f"{self.algo_timer}", True, LEGEND_COLOR
        )
    
    def timer_to_string(self, timer_total, timer_count) -> None:
        """Gets values from timer to display on screen"""
        self.algo_timer = f"Time: {timer_total:.3f}s - # squares: {timer_count:,}"


def set_graph(gph: GraphState) -> None:
    """Creates the graph object that stores the location of all the squares"""

    # Not actually creating squares on screen so need to update screen manually
    # This function just draws lines over a white back ground, squares are
    # technically created upon a set_* method from the graph's prespective.
    gph.update_entire_screen = True

    # Everything square related is handle in here
    Square.init(WIDTH)


def draw(gph: GraphState, algo: AlgoState, txt: VisText, legend=False, clear_legend=False) -> None:
    """Main function to update the window. Called by all operations that updates the window."""

    if clear_legend:
        gph.add_to_update_queue(gph.window.fill(LEGEND_AREA_COLOR, LEGEND_RECT))

    # Draws the horizontal and vertical lines on the graph unless it has image
    if not gph.base_drawn:
        algo.reset()
        
        if gph.has_img:
            _draw_img(gph)
        else:
            # Sets background of graph to white
            gph.add_to_update_queue(gph.window.fill(DEFAULT_COLOR, GRAPH_RECT))
            _draw_lines(gph)
        # Sets background of legend to grey
        gph.add_to_update_queue(gph.window.fill(LEGEND_AREA_COLOR, LEGEND_RECT))

        if legend:
            _draw_legend(gph, txt)

        gph.base_drawn = True
    else:
        if legend:
            gph.update_legend = True
        elif algo.check_phase() == algo.NONE:
            if not clear_legend:
                gph.base_drawn = False

    if gph.update_legend:
        gph.update_legend = False
        gph.add_to_update_queue(gph.window.fill(LEGEND_AREA_COLOR, LEGEND_RECT))
        _draw_legend(gph, txt)

    # Get squares to draw
    graph = []
    with CppPyLock(algo):
        if gph.visualize_square_history:
            gph.visualize_square_history = False
            for square in Square.get_future_history_squares():
                square.set_history()
                gph.add_to_update_queue(square)
            Square.clear_future_history_squares()
        # Queues all changed squares to update
        else:
            square: Square
            for square in Square.get_squares_to_update():
                graph.append(square)
                gph.add_to_update_queue(square)
            Square.clear_squares_to_update()

        # Used to reset squares to previous color like nothing happened
        for square in Square.get_all_history_squares():
            square.set_history_rollback()
        Square.clear_history_squares()

    # Update the pygame display
    # It's faster to update entire screen if number of rects is greater than 20
    # 40x speedup
    if len(gph.rects_to_update) > 20 or gph.update_entire_screen:
        gph.update_entire_screen = False
        _draw_lines(gph)
        pygame.display.flip()
    else:
        _draw_square_borders(gph, graph)
        pygame.display.update(gph.rects_to_update)
    gph.rects_to_update.clear()


def _draw_square(gph: GraphState, square_color, square_pos) -> pygame.Rect:
    """Draws square with color and correct positioning"""
    return pygame.draw.rect(gph.window, square_color, square_pos)


def _draw_square_borders(gph: GraphState, graph) -> None:
    """Draws the lines surrounding the updating squares"""

    square: Square
    square_length = Square.get_square_length()
    for square in graph:
        x, y, *_ = square.draw_square()
        top_left = x, y
        top_right = x, y + square_length
        bottom_left = x + square_length, y
        bottom_right = x + square_length, y + square_length

        # Top
        pygame.draw.line(gph.window, LINE_COLOR, top_left, top_right)
        # Right
        pygame.draw.line(gph.window, LINE_COLOR, top_right, bottom_right)
        # Bottom
        pygame.draw.line(gph.window, LINE_COLOR, bottom_left, bottom_right)
        # Left
        pygame.draw.line(gph.window, LINE_COLOR, top_left, bottom_left)


def _draw_lines(gph: GraphState) -> None:
    """Helper function to define the properties of the horizontal and vertical graph lines"""

    for i in range(Square.get_num_rows()):
        row = col = i * Square.get_square_length()

        # Horizonatal lines
        pygame.draw.line(gph.window, LINE_COLOR, (0, row), (WIDTH, row))
        # Vertical lines
        pygame.draw.line(gph.window, LINE_COLOR, (col, 0), (col, WIDTH))


def _draw_img(gph: GraphState) -> None:
    """Draws the maps image onto the graph"""
    gph.add_to_update_queue(gph.window.blit(gph.img, (0, 0)))


def set_squares_to_roads(gph: GraphState) -> None:
    """Sets squares to the color of a single pixel"""

    # These two loops x,y gets all the squares in the graph. At 400 graph size a square is a pixel.
    graph = Square.get_graph()
    for x in range(len(graph)):
        for y in range(len(graph[0])):
            square: Square = graph[x][y]
            row, col = square.get_pos()
            square.set_wall_color_map()  # Change wall color for easy visibility
            tot = 0
            tot_b = 0  # Used to check if highway since they are yellow.

            # These two loops i,j get each pixel in each square. Time Complexity is O(n) in regards to pixels.
            square_length = Square.get_square_length()
            for i in range(
                row * int(square_length),
                (row + 1) * int(square_length),
            ):
                for j in range(
                    col * int(square_length),
                    (col + 1) * int(square_length),
                ):
                    r, g, b, a = gph.window.get_at((i, j))
                    tot += r + g + b
                    tot_b += b
            avg_tot = tot / square_length ** 2 / 3  # Gets the average of each square
            avg_b = tot_b / square_length ** 2
            cutoff = 1  # Any color with value above this will be set as a viable path

            # If the square's color is above cutoff, set it as path. Else wall square
            if avg_tot > cutoff:
                # If b is greater, then it is white.
                if avg_b > 225:
                    square.reset()
                else:
                    square.reset()
                    square.set_highway(True)
            else:
                square.set_wall()


def _draw_legend(gph: GraphState, txt: VisText) -> None:
    """Helper function to define the location of the legend"""

    if not gph.has_img:
        # Left legend
        gph.window.blit(txt.legend_add_square, (2, 15 * 53.1 + 3))
        gph.window.blit(txt.legend_add_mid_square, (2, 15 * 54.1 + 3))
        gph.window.blit(txt.legend_remove_square, (2, 15 * 55.1 + 3))
        gph.window.blit(txt.legend_clear_graph, (2, 15 * 56.1 + 3))
        gph.window.blit(txt.legend_graph_size, (2, 15 * 57.1 + 3))

        # Right legend
        gph.window.blit(
            txt.legend_dijkstra,
            (WIDTH - txt.legend_dijkstra.get_width() - 2, 15 * 53.1 + 3),
        )
        gph.window.blit(
            txt.legend_a_star,
            (WIDTH - txt.legend_a_star.get_width() - 2, 15 * 54.1 + 3),
        )
        gph.window.blit(
            txt.legend_bi_dijkstra,
            (WIDTH - txt.legend_bi_dijkstra.get_width() - 2, 15 * 55.1 + 3),
        )
        gph.window.blit(
            txt.legend_recursive_maze,
            (WIDTH - txt.legend_recursive_maze.get_width() - 2, 15 * 56.1 + 3),
        )
        gph.window.blit(
            txt.legend_instant_recursive_maze,
            (WIDTH - txt.legend_instant_recursive_maze.get_width() - 2, 15 * 57.1 + 3),
        )

        # Center Legend
        gph.window.blit(
            txt.legend_address,
            (
                WIDTH // 2 - txt.legend_address.get_width() // 2,
                CENTER_LEGEND_AREA - txt.legend_address.get_height() // 2,
            ),
        )
        draw_algo_timer(gph, txt)
        if Square.get_track_square_history():
            gph.window.blit(
                txt.legend_square_history_show,
                (
                    WIDTH // 2 - txt.legend_square_history_show.get_width() // 2,
                    CENTER_LEGEND_AREA
                    - txt.legend_square_history_show.get_height() // 2
                    + 30,
                ),
            )
        else:
            gph.window.blit(
                txt.legend_square_history,
                (
                    WIDTH // 2 - txt.legend_square_history.get_width() // 2,
                    CENTER_LEGEND_AREA - txt.legend_square_history.get_height() // 2 + 30,
                ),
            )

    if gph.has_img:
        gph.window.blit(
            txt.legend_address,
            (
                WIDTH // 2 - txt.legend_address.get_width() // 2,
                CENTER_LEGEND_AREA - txt.legend_address.get_height() // 2 - 15,
            ),
        )
        gph.window.blit(
            txt.legend_convert_map,
            (
                WIDTH // 2 - txt.legend_convert_map.get_width() // 2,
                CENTER_LEGEND_AREA - txt.legend_convert_map.get_height() // 2,
            ),
        )
        if Square.get_track_square_history():
            gph.window.blit(
                txt.legend_square_history_show,
                (
                    WIDTH // 2 - txt.legend_square_history_show.get_width() // 2,
                    CENTER_LEGEND_AREA
                    - txt.legend_square_history_show.get_height() // 2
                    + 15,
                ),
            )
        else:
            gph.window.blit(
                txt.legend_square_history,
                (
                    WIDTH // 2 - txt.legend_square_history.get_width() // 2,
                    CENTER_LEGEND_AREA - txt.legend_square_history.get_height() // 2 + 15,
                ),
            )


def draw_vis_text(
    gph: GraphState,
    algo: AlgoState,
    txt: VisText,
    is_graph_size=False,
    is_input=False,
    is_base_img=False,
    is_clean_img=False,
    is_converting_img=False,
) -> None:
    """Special text indicating some operation is being performed. No inputs are registered."""

    # Clear legend to prevent drawing overself.
    # Same cost as using precise rects.
    gph.window.fill(LEGEND_AREA_COLOR, LEGEND_RECT)

    text_rects = []  # Used to only update text area

    txt.timer_to_string(algo.timer_total, algo.timer_count)

    # Text to be shown depending on operation
    if algo.check_algo() == algo.ALGO_DIJKSTRA:
        text_rects.append(draw_algo_timer(gph, txt))
        text_rects.append(
            gph.window.blit(
                txt.vis_text_dijkstra,
                (
                    WIDTH // 2 - txt.vis_text_dijkstra.get_width() // 2,
                    CENTER_LEGEND_AREA - txt.vis_text_dijkstra.get_height() // 2 - 10,
                ),
            )
        )
    elif algo.check_algo() == algo.ALGO_A_STAR:
        text_rects.append(draw_algo_timer(gph, txt))
        text_rects.append(
            gph.window.blit(
                txt.vis_text_a_star,
                (
                    WIDTH // 2 - txt.vis_text_a_star.get_width() // 2,
                    CENTER_LEGEND_AREA - txt.vis_text_a_star.get_height() // 2 - 10,
                ),
            )
        )
    elif algo.check_algo() == algo.ALGO_BI_DIJKSTRA:
        text_rects.append(draw_algo_timer(gph, txt))
        text_rects.append(
            gph.window.blit(
                txt.vis_text_bi_dijkstra,
                (
                    WIDTH // 2 - txt.vis_text_bi_dijkstra.get_width() // 2,
                    CENTER_LEGEND_AREA
                    - txt.vis_text_bi_dijkstra.get_height() // 2
                    - 10,
                ),
            )
        )
    elif algo.check_algo() == algo.ALGO_BEST_PATH:
        text_rects.append(draw_algo_timer(gph, txt))
        text_rects.append(
            gph.window.blit(
                txt.vis_text_best_path,
                (
                    WIDTH // 2 - txt.vis_text_best_path.get_width() // 2,
                    CENTER_LEGEND_AREA - txt.vis_text_best_path.get_height() // 2 + 10,
                ),
            )
        )
    elif algo.check_algo() == algo.ALGO_RECURSIVE_MAZE:
        text_rects.append(
            gph.window.blit(
                txt.vis_text_recursive_maze,
                (
                    WIDTH // 2 - txt.vis_text_recursive_maze.get_width() // 2,
                    CENTER_LEGEND_AREA - txt.vis_text_recursive_maze.get_height() // 2,
                ),
            )
        )
    elif is_graph_size:
        text_rects.append(
            gph.window.blit(
                txt.vis_text_graph_size,
                (
                    WIDTH // 2 - txt.vis_text_graph_size.get_width() // 2,
                    CENTER_GRAPH - txt.vis_text_graph_size.get_height() // 2,
                ),
            )
        )
    elif is_input:
        # Reset legend area (inefficient, only need area with new text)
        text_rects.append(gph.window.fill(LEGEND_AREA_COLOR, LEGEND_RECT))

        # Instructions on what to type
        text_rects.append(
            gph.window.blit(
                txt.vis_text_input,
                (
                    WIDTH // 2 - txt.vis_text_input.get_width() // 2,
                    CENTER_LEGEND_AREA - txt.vis_text_input.get_height() // 2 - 15,
                ),
            )
        )
        # Update text with new input
        txt.update_vis_text_address()
        text_rects.append(
            gph.window.blit(
                txt.vis_text_address,
                (
                    WIDTH // 2 - txt.vis_text_address.get_width() // 2,
                    CENTER_LEGEND_AREA - txt.vis_text_address.get_height() // 2,
                ),
            )
        )
    elif is_base_img:
        text_rects.append(
            gph.window.blit(
                txt.vis_text_base_img,
                (
                    WIDTH // 2 - txt.vis_text_base_img.get_width() // 2,
                    CENTER_LEGEND_AREA - txt.vis_text_base_img.get_height() // 2 + 15,
                ),
            )
        )
    elif is_clean_img:
        # Reset legend area (inefficient, only need area with new text)
        text_rects.append(gph.window.fill(LEGEND_AREA_COLOR, LEGEND_RECT))

        text_rects.append(
            gph.window.blit(
                txt.vis_text_clean_img,
                (
                    WIDTH // 2 - txt.vis_text_clean_img.get_width() // 2,
                    CENTER_LEGEND_AREA - txt.vis_text_clean_img.get_height() // 2,
                ),
            )
        )
    elif is_converting_img:
        text_rects.append(
            gph.window.blit(
                txt.vis_text_converting_img,
                (
                    WIDTH // 2 - txt.vis_text_converting_img.get_width() // 2,
                    CENTER_LEGEND_AREA - txt.vis_text_converting_img.get_height() // 2,
                ),
            )
        )

    # Updates the portion of the screen that contains changing text
    pygame.display.update(text_rects)


def draw_algo_timer(gph: GraphState, txt: VisText) -> pygame.Rect:
    """Draws timer of algo"""
    txt.update_vis_text_algo_timer()
    return gph.window.blit(
        txt.vis_text_algo_timer,
        (
            WIDTH // 2 - txt.vis_text_algo_timer.get_width() // 2,
            CENTER_LEGEND_AREA - txt.vis_text_algo_timer.get_height() // 2 - 32,
        ),
    )


def reset_graph(gph: GraphState, algo, txt: VisText, graph_max=None, graph_default=None, reset=True) -> None:
    """Resets entire graph removing every square"""
    # Need to update these values
    algo.reset()
    gph.has_img = False

    # Resets each square
    if reset:
        # If reseting graph from map, not a circular call
        if Square.get_num_rows() == graph_max:
            change_graph_size(gph, algo, txt, graph_default)
            return

        # Default case
        Square.reset_all_squares()


def reset_algo(algo) -> None:
    """Resets algo colors while keeping ordinal squares and walls"""
    # Resets only certain colors
    Square.reset_algo_squares()


def change_graph_size(gph: GraphState, algo: AlgoState, txt: VisText, new_num_rows_cols, to_draw=True) -> None:
    """Changes graph size and updates squares and their locations as well.
    Restricted to certain sizes as recursive maze breaks otherwise
    """
    # Updates rows and square size with new values
    reset_graph(gph, algo, txt, reset=False)
    Square.update_num_rows_cols(new_num_rows_cols)

    # Recreates graph with new values
    set_graph(gph)
    if to_draw:
        draw(gph, algo, txt)
