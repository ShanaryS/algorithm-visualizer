"""Handles inputs from user"""


# Handles how much C++ the the program should use
from src.pathfinding.cpp_or_py import use_square_h
if use_square_h:
    from src.pathfinding.cpp.square import Square
else:
    from src.pathfinding.py.square import Square

# Handles how much C++ the the program should use
from src.pathfinding.cpp_or_py import use_algorithms_h
if use_algorithms_h:
    from src.pathfinding.cpp.algorithms import (AlgoState, dijkstra, a_star,
        bi_dijkstra, start_mid_end, recursive_maze)
else:
    from src.pathfinding.py.algorithms import (AlgoState, dijkstra, a_star,
        bi_dijkstra, start_mid_end, recursive_maze)

from src.pathfinding.py.maps import get_img_base, get_img_clean
from src.pathfinding.py.graph import (GraphState, VisText, set_graph, draw,
    reset_graph, reset_algo, change_graph_size, set_squares_to_roads,
    draw_vis_text, HEIGHT)

import pygame
from dataclasses import dataclass


@dataclass(slots=True)
class LogicState:
    """Stores the state of the logic"""

    ordinal_square_clicked: list
    start: Square = None
    mid: Square = None
    end: Square = None
    run: bool = True
    GRAPH_SMALL: int = 22
    GRAPH_MEDIUM: int = 46
    GRAPH_LARGE: int = 95
    GRAPH_MAX: int = 400
    BEST_PATH_SLEEP: int = 3


def run_pathfinding(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """The pygame logic loop. This runs forever until exited. This is what should be called to run program."""
    
    # Create pygame window
    gph.create_pygame_window()

    # Creates the graph squares
    set_graph(gph)
    
    # Only allow certain events
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

    # Defines the FPS of the game. Used by clock.tick() at bottom of while loop
    clock = pygame.time.Clock()

    while lgc.run:
        draw(gph, algo, txt, legend=True)  # Draws the graph with all the necessary updates

        for event in pygame.event.get():

            """Special cases"""

            # Allow clicking the "X" on the pygame window to end the program
            if event.type == pygame.QUIT:
                lgc.run = False

            """Mouse buttons"""

            # Used to know if no longer dragging ordinal square after algo completion
            if not pygame.mouse.get_pressed(3)[0]:
                lgc.ordinal_square_clicked.clear()

            # LEFT MOUSE CLICK. HEIGHT condition prevents out of bound when clicking on legend.
            if (pygame.mouse.get_pressed(3)[0] and pygame.mouse.get_pos()[1] < HEIGHT and not gph.has_img):
                _left_click_button(gph, algo, lgc, txt)

            # RIGHT MOUSE CLICK. HEIGHT condition prevents out of bound when clicking on legend.
            elif (pygame.mouse.get_pressed(3)[2] and pygame.mouse.get_pos()[1] < HEIGHT and not gph.has_img):
                _right_click_button(gph, algo, lgc, txt)

            # MIDDLE MOUSE CLICK. HEIGHT condition prevents out of bound when clicking on legend.
            elif (pygame.mouse.get_pressed(3)[1] and pygame.mouse.get_pos()[1] < HEIGHT and not gph.has_img):
                _middle_click_button(algo, lgc)

            """Keyboard buttons"""

            # Reset graph with "SPACE" on keyboard
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not gph.has_img):
                _reset_graph_button(gph, algo, lgc, txt)

            # Run Dijkstra with "D" key on keyboard
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_d and lgc.start and lgc.end and not gph.has_img):
                _dijkstra_button(gph, algo, lgc, txt)

            # Run A* with "A" key on keyboard
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_a and lgc.start and lgc.end and not gph.has_img):
                _a_star_button(gph, algo, lgc, txt)

            # Run Bi-directional Dijkstra with "B" key on keyboard
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_b and lgc.start and lgc.end and not gph.has_img):
                _bi_dijkstra_button(gph, algo, lgc, txt)

            # Draw recursive maze with "G" key on keyboard
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_g and not gph.has_img):
                if Square.get_num_rows() == lgc.GRAPH_MAX:
                    _graph_size_buttons(gph, algo, lgc, txt, lgc.GRAPH_LARGE, lgc.BEST_PATH_SLEEP)
                _recursive_maze_buttons(gph, algo, lgc, txt)

            # Draw recursive maze with NO VISUALIZATIONS with "I" key on keyboard
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_i and not gph.has_img):
                if Square.get_num_rows() == lgc.GRAPH_MAX:
                    _graph_size_buttons(gph, algo, lgc, txt, lgc.GRAPH_LARGE, lgc.BEST_PATH_SLEEP)
                _recursive_maze_buttons(gph, algo, lgc, txt)

            # Redraw small maze with "S" key on keyboard if not currently small
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_s and Square.get_num_rows() != lgc.GRAPH_SMALL and not gph.has_img):
                _graph_size_buttons(gph, algo, lgc, txt, lgc.GRAPH_SMALL, lgc.BEST_PATH_SLEEP)

            # Redraw medium maze with "M" key on keyboard if not currently medium
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_m and Square.get_num_rows() != lgc.GRAPH_MEDIUM and not gph.has_img):
                _graph_size_buttons(gph, algo, lgc, txt, lgc.GRAPH_MEDIUM, lgc.BEST_PATH_SLEEP)

            # Redraw large maze with "L" key on keyboard if not currently large
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_l and Square.get_num_rows() != lgc.GRAPH_LARGE and not gph.has_img):
                _graph_size_buttons(gph, algo, lgc, txt, lgc.GRAPH_LARGE, lgc.BEST_PATH_SLEEP)

            # Enter an address with the "ENTER" key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                _get_address_from_user(gph, algo, lgc, txt)

            # Convert map into grid with "C" key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c and gph.has_img:
                _convert_img_to_squares(gph, algo, txt)

            # Visualize changes with the "V" key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                _visualize_changes_button(gph, algo, txt)

        clock.tick(gph.FPS)

    # Only reached if while loop ends, which happens if window is closed. Program terminates.
    quit_program()


def _get_clicked_pos(pos) -> tuple[int, int]:
    """Turns the location data of the mouse into location of squares"""
    x, y = pos
    square_length = Square.get_square_length()
    row = int(x / square_length)
    col = int(y / square_length)
    
    # Fix clicking past square boundaries.
    square_max = Square.get_num_rows()-1
    row = square_max if row > square_max else row
    col = square_max if col > square_max else col
    return row, col


def _get_square_clicked() -> Square:
    """Gets the the square that was clicked"""
    pos = pygame.mouse.get_pos()
    row, col = _get_clicked_pos(pos)
    square: Square = Square.get_square(row, col)
    return square


def _left_click_button(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """Handles mouse left click"""
    square = _get_square_clicked()
    # Checks if algo is completed, used for dragging algo
    if ((algo.algo == algo.ALGO_DIJKSTRA or algo.algo == algo.ALGO_A_STAR or algo.algo == algo.ALGO_BI_DIJKSTRA)
        and lgc.start and lgc.end):
        # Checks if ordinal square is being dragged
        if lgc.ordinal_square_clicked:

            # Checks if the mouse is currently on an ordinal square, no need to update anything
            if square != lgc.start and square != lgc.mid and square != lgc.end:
                # Used to move ordinal square to new pos
                last_square = lgc.ordinal_square_clicked[0]

                # Checks if ordinal square was previously a wall to reinstate it after moving, else reset
                if last_square == "start":
                    if lgc.start in Square.get_all_wall_squares():
                        lgc.start.set_wall()
                    else:
                        lgc.start.reset()
                    lgc.start = square
                    square.set_start()
                elif last_square == "mid":
                    if lgc.mid in Square.get_all_wall_squares():
                        lgc.mid.set_wall()
                    else:
                        lgc.mid.reset()
                    lgc.mid = square
                    square.set_mid()
                elif last_square == "end":
                    if lgc.end in Square.get_all_wall_squares():
                        lgc.end.set_wall()
                    else:
                        lgc.end.reset()
                    lgc.end = square
                    square.set_end()

                # Runs the algo again instantly with no visualizations, handles whether mid exists
                if algo.algo == algo.ALGO_DIJKSTRA:
                    _dijkstra_button(gph, algo, lgc, txt)
                elif algo.algo == algo.ALGO_A_STAR:
                    _a_star_button(gph, algo, lgc, txt)
                elif algo.algo == algo.ALGO_BI_DIJKSTRA:
                    _bi_dijkstra_button(gph, algo, lgc, txt)

        # If ordinal square is not being dragged, prepare it to
        elif square is lgc.start:
            lgc.ordinal_square_clicked.append("start")
        elif square is lgc.mid:
            lgc.ordinal_square_clicked.append("mid")
        elif square is lgc.end:
            lgc.ordinal_square_clicked.append("end")

        # On algo completion, add wall and update algo
        else:
            # Add wall
            square.set_wall()

            # Updates algo
            if algo.algo == algo.ALGO_DIJKSTRA:
                _dijkstra_button(gph, algo, lgc, txt)
            elif algo.algo == algo.ALGO_A_STAR:
                _a_star_button(gph, algo, lgc, txt)
            elif algo.algo == algo.ALGO_BI_DIJKSTRA:
                _bi_dijkstra_button(gph, algo, lgc, txt)

    # If start square does not exist, create it. If not currently ordinal square.
    elif not lgc.start and square != lgc.mid and square != lgc.end:
        lgc.start = square
        square.set_start()

        # Handles removing and adding start manually instead of dragging on algo completion.
        if algo.algo == algo.ALGO_DIJKSTRA and lgc.start and lgc.end:
            _dijkstra_button(gph, algo, lgc, txt)
        elif algo.algo == algo.ALGO_A_STAR and lgc.start and lgc.end:
            _a_star_button(gph, algo, lgc, txt)
        elif algo.algo == algo.ALGO_BI_DIJKSTRA and lgc.start and lgc.end:
            _bi_dijkstra_button(gph, algo, lgc, txt)

    # If end square does not exist, and start square does exist, create end square.
    # If not currently ordinal square.
    elif not lgc.end and square != lgc.start and square != lgc.mid:
        lgc.end = square
        square.set_end()

        # Handles removing and adding end manually instead of dragging on algo completion.
        if algo.algo == algo.ALGO_DIJKSTRA and lgc.start and lgc.end:
            _dijkstra_button(gph, algo, lgc, txt)
        elif algo.algo == algo.ALGO_A_STAR and lgc.start and lgc.end:
            _a_star_button(gph, algo, lgc, txt)
        elif algo.algo == algo.ALGO_BI_DIJKSTRA and lgc.start and lgc.end:
            _bi_dijkstra_button(gph, algo, lgc, txt)

    # If start and end square exists, create wall. If not currently ordinal square.
    # Saves pos of wall to be able to reinstate it after dragging ordinal square past it.
    elif square != lgc.start and square != lgc.mid and square != lgc.end:
        square.set_wall()


def _right_click_button(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """Handles mouse right click"""
    square = _get_square_clicked()
    # Reset square and ordinal square if it was any
    square.reset()
    was_ordinal = False
    if square == lgc.start:
        lgc.start = None
        was_ordinal = True
    elif square == lgc.mid:
        lgc.mid = None
        was_ordinal = True
    elif square == lgc.end:
        lgc.end = None
        was_ordinal = True
        
    # Updates algo
    if not was_ordinal:
        if algo.algo == algo.ALGO_DIJKSTRA:
            _dijkstra_button(gph, algo, lgc, txt)
        elif algo.algo == algo.ALGO_A_STAR:
            _a_star_button(gph, algo, lgc, txt)
        elif algo.algo == algo.ALGO_BI_DIJKSTRA:
            _bi_dijkstra_button(gph, algo, lgc, txt)


def _middle_click_button(algo: AlgoState, lgc: LogicState) -> None:
    """Handles mouse wheel click"""
    square = _get_square_clicked()
    # Set square to mid if no square is already mid, and not currently ordinal square.
    if not lgc.mid and square != lgc.start and square != lgc.end:
        lgc.mid = square
        square.set_mid()
        
        # Handles removing and adding mid manually instead of dragging on algo completion.
        if algo.algo == algo.ALGO_DIJKSTRA and lgc.start and lgc.mid and lgc.end:
            reset_algo(algo)
            start_mid_end(algo, lgc.start, lgc.mid, lgc.end,)
        elif algo.algo == algo.ALGO_A_STAR and lgc.start and lgc.mid and lgc.end:
            reset_algo(algo)
            start_mid_end(algo, lgc.start, lgc.mid, lgc.end,)
        elif algo.algo == algo.ALGO_BI_DIJKSTRA and lgc.start and lgc.mid and lgc.end:
            reset_algo(algo)
            start_mid_end(algo, lgc.start, lgc.mid, lgc.end)


def _reset_ordinal_squares(lgc: LogicState) -> None:
    """Resets the ordinal squares"""
    lgc.start = lgc.mid = lgc.end = None


def _reset_graph_button(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """Resets the graph"""
    reset_graph(gph, algo, txt, graph_max=lgc.GRAPH_MAX, graph_default=lgc.GRAPH_MEDIUM)
    _reset_ordinal_squares(lgc)


def _dijkstra_button(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """Run the dijkstra algorithm"""
    # Resets algo visualizations without removing ordinal squares or walls
    reset_algo(algo)
    draw(gph, algo, txt, clear_legend=True)

    # Handles whether or not mid exists
    if lgc.mid:
        start_mid_end(algo, lgc.start, lgc.mid, lgc.end)
    else:
        dijkstra(algo, lgc.start, lgc.end)


def _a_star_button(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """Runs the A* algorithm"""
    # Resets algo visualizations without removing ordinal squares or walls
    reset_algo(algo)
    draw(gph, algo, txt, clear_legend=True)

    # Handles whether or not mid exists
    if lgc.mid:
        start_mid_end(algo, lgc.start, lgc.mid, lgc.end)
    else:
        a_star(algo, lgc.start, lgc.end)


def _bi_dijkstra_button(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """Runs the Bi-Directional Dijkstra algorithm"""
    # Resets algo visualizations without removing ordinal squares or walls
    reset_algo(algo)
    draw(gph, algo, txt, clear_legend=True)

    # Handles whether or not mid exists
    if lgc.mid:
        start_mid_end(algo, lgc.start, lgc.mid, lgc.end)
    else:
        bi_dijkstra(algo, lgc.start, lgc.end)


def _recursive_maze_buttons(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """Draws recursive maze"""
    reset_graph(gph, algo, txt)
    draw(gph, algo, txt, clear_legend=True)
    gph.base_drawn = False
    recursive_maze(gph, algo, txt)  # Draw maze
    gph.update_legend = True
    _reset_ordinal_squares(lgc)


def _graph_size_buttons(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText, new_graph_size, best_path_sleep) -> None:
    """Changes the size of the graph"""
    algo.best_path_sleep = best_path_sleep
    gph.has_img = False
    change_graph_size(gph, algo, txt, new_graph_size)
    _reset_ordinal_squares(lgc)


def _load_img_to_graph(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """Loads the image onto the graph"""
    draw_vis_text(gph, algo, txt, is_base_img=True)
    change_graph_size(gph, algo, txt, lgc.GRAPH_MAX, to_draw=False)

    gph.img = pygame.image.load(get_img_base(txt.address))
    gph.has_img = True
    draw(gph, algo, txt)
    _reset_ordinal_squares(lgc)


def _convert_img_to_squares(gph: GraphState, algo: AlgoState, txt: VisText) -> None:
    """Coverts the map data into squares the algorithms can use"""
    draw_vis_text(gph, algo, txt, is_clean_img=True)

    gph.img = pygame.image.load(get_img_clean(txt.address))

    gph.base_drawn = False
    draw(gph, algo, txt)
    draw_vis_text(gph, algo, txt, is_converting_img=True)

    gph.update_legend = True
    gph.has_img = False
    algo.algo_speed_multiplier = 500
    algo.path_speed_multiplier = 1

    set_squares_to_roads(gph)


def _get_address_from_user(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """Gets the address from the user"""
    # Used to get rid of commas inserted by url encoding.
    txt.address = txt.address.replace(",", "")

    gph.base_drawn = False
    draw(gph, algo, txt)
    draw_vis_text(gph, algo, txt, is_input=True)

    while lgc.run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lgc.run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    txt.address += event.unicode
                elif event.unicode.isalnum():
                    txt.address += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    txt.address = txt.address[:-1]
                elif event.key == pygame.K_RETURN:
                    txt.address = ", ".join(txt.address.split())
                    _load_img_to_graph(gph, algo, lgc, txt)
                    return

                draw_vis_text(gph, algo, txt, is_input=True)

    quit_program()


def _visualize_changes_button(gph: GraphState, algo: AlgoState, txt: VisText) -> None:
    """Visualize the changed parts of the screen between toggles"""
    # Stop tracking square history and display it
    if Square.get_track_square_history():
        Square.set_track_square_history(False)
        gph.visualize_square_history = True
    # Start tracking square history
    else:
        Square.set_track_square_history(True)

    gph.update_legend = True
    draw(gph, algo, txt, legend=True)


def quit_program() -> None:
    """Quits the program"""
    pygame.quit()
    import sys
    sys.exit()
