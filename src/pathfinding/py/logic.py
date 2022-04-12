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
    from src.pathfinding.cpp.algorithms import AlgoState
else:
    from src.pathfinding.py.algorithms import AlgoState

from src.pathfinding.py.maps import get_img_base, get_img_clean
from src.pathfinding.py.graph import (GraphState, VisText, set_graph, draw,
    reset_graph, reset_algo, change_graph_size, set_squares_to_roads,
    draw_vis_text, HEIGHT)
from lib.timer import sleep

import threading
import pygame
from dataclasses import dataclass


@dataclass(slots=True)
class LogicState:
    """Stores the state of the logic"""

    ordinal_square_clicked_last_tick: list
    start: Square = None
    mid: Square = None
    end: Square = None
    run: bool = True
    visualize: bool = True
    GRAPH_SMALL: int = 22
    GRAPH_MEDIUM: int = 46
    GRAPH_LARGE: int = 95
    GRAPH_MAX: int = 400


def run_pathfinding(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """The pygame logic loop. This runs forever until exited. This is what should be called to run program."""
    # Start other loops
    threading.Thread(target=algo.start_loop, args=(), daemon=True).start()
    
    # Create pygame window
    gph.create_pygame_window()

    # Creates the graph squares
    set_graph(gph)
    
    # Only allow certain events
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
    
    logic_loop(gph, algo, lgc, txt)
 

def logic_loop(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """Main loop that handles logic, inputs, and GUI on a single thread."""
    # Defines the FPS of the game. Used by clock.tick() at bottom of while loop
    clock = pygame.time.Clock()
    
    while lgc.run:
        # Draws the graph with all the necessary updates
        if algo.check_phase() == algo.NONE:
            draw(gph, algo, txt, legend=True)
        elif lgc.visualize:
            draw(gph, algo, txt)
            draw_vis_text(gph, algo, txt)

        for event in pygame.event.get():

            """Special cases"""

            # Allow clicking the "X" on the pygame window to end the program
            if event.type == pygame.QUIT:
                lgc.run = False

            # Don't allow button presses in certain phases
            if algo.check_phase() != algo.NONE:
                continue

            """Mouse buttons"""

            # Used to know if no longer dragging ordinal square after algo completion
            if not pygame.mouse.get_pressed(3)[0]:
                lgc.ordinal_square_clicked_last_tick.clear()

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
                _dijkstra_button(algo, lgc)

            # Run A* with "A" key on keyboard
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_a and lgc.start and lgc.end and not gph.has_img):
                _a_star_button(algo, lgc)

            # Run Bi-directional Dijkstra with "B" key on keyboard
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_b and lgc.start and lgc.end and not gph.has_img):
                _bi_dijkstra_button(algo, lgc)

            # Draw recursive maze with "G" key on keyboard
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_g and not gph.has_img):
                if Square.get_num_rows() == lgc.GRAPH_MAX:
                    _graph_size_buttons(gph, algo, lgc, txt, lgc.GRAPH_LARGE)
                _recursive_maze_buttons(gph, algo, lgc, txt, True)

            # Draw recursive maze with NO VISUALIZATIONS with "I" key on keyboard
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_i and not gph.has_img):
                if Square.get_num_rows() == lgc.GRAPH_MAX:
                    _graph_size_buttons(gph, algo, lgc, txt, lgc.GRAPH_LARGE)
                _recursive_maze_buttons(gph, algo, lgc, txt, False)

            # Redraw small maze with "S" key on keyboard if not currently small
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_s and Square.get_num_rows() != lgc.GRAPH_SMALL and not gph.has_img):
                _graph_size_buttons(gph, algo, lgc, txt, lgc.GRAPH_SMALL)

            # Redraw medium maze with "M" key on keyboard if not currently medium
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_m and Square.get_num_rows() != lgc.GRAPH_MEDIUM and not gph.has_img):
                _graph_size_buttons(gph, algo, lgc, txt, lgc.GRAPH_MEDIUM)

            # Redraw large maze with "L" key on keyboard if not currently large
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_l and Square.get_num_rows() != lgc.GRAPH_LARGE and not gph.has_img):
                _graph_size_buttons(gph, algo, lgc, txt, lgc.GRAPH_LARGE)

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
    if algo.check_finished() and lgc.start and lgc.end:
        # Checks if ordinal square is being dragged
        if lgc.ordinal_square_clicked_last_tick:

            # Checks if the mouse is currently on an ordinal square, no need to update anything
            if square != lgc.start and square != lgc.mid and square != lgc.end:
                # Used to move ordinal square to new pos
                last_square = lgc.ordinal_square_clicked_last_tick[0]

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

                # Runs the algo again instantly with no visualizations.
                _run_pathfinding_algo(algo, lgc, algo.check_algo(), False)

        # If ordinal square is not being dragged, prepare it to
        elif square is lgc.start:
            lgc.ordinal_square_clicked_last_tick.append("start")
        elif square is lgc.mid:
            lgc.ordinal_square_clicked_last_tick.append("mid")
        elif square is lgc.end:
            lgc.ordinal_square_clicked_last_tick.append("end")

        # On algo completion, add wall and update algo
        else:
            # Add wall
            square.set_wall()

            # Update algo
            if algo.check_finished():
                _run_pathfinding_algo(algo, lgc, algo.check_algo(), False)

    # If start square does not exist, create it. If not currently ordinal square.
    elif not lgc.start and square != lgc.mid and square != lgc.end:
        lgc.start = square
        square.set_start()

        # Handles removing and adding end manually instead of dragging on algo completion.
        if algo.check_finished() and lgc.end:
            _run_pathfinding_algo(algo, lgc, algo.check_algo(), False)

   # If start square does not exist, create it. If not currently ordinal square.
    elif not lgc.end and square != lgc.start and square != lgc.mid:
        lgc.end = square
        square.set_end()

        # Handles removing and adding end manually instead of dragging on algo completion.
        if algo.check_finished():
            _run_pathfinding_algo(algo, lgc, algo.check_algo(), False)

    # If start and end square exists, create wall. If not currently ordinal square.
    # Saves pos of wall to be able to reinstate it after dragging ordinal square past it.
    elif square != lgc.start and square != lgc.mid and square != lgc.end:
        square.set_wall()


def _right_click_button(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """Handles mouse right click"""
    square = _get_square_clicked()
    # Reset square and ordinal square if it was any
    square.reset()
    if square == lgc.start:
        lgc.start = None
    elif square == lgc.mid:
        lgc.mid = None
    elif square == lgc.end:
        lgc.end = None
        
    # Updates algo
    if algo.check_finished() and lgc.start and lgc.end:
        _run_pathfinding_algo(algo, lgc, algo.check_algo(), False)


def _middle_click_button(algo: AlgoState, lgc: LogicState) -> None:
    """Handles mouse wheel click"""
    square = _get_square_clicked()
    # Set square to mid if no square is already mid, and not currently ordinal square.
    if not lgc.mid and square != lgc.start and square != lgc.end:
        lgc.mid = square
        square.set_mid()
        
        # Handles removing and adding mid manually instead of dragging on algo completion.
        if algo.check_finished() and lgc.start and lgc.mid and lgc.end:
            _run_pathfinding_algo(algo, lgc, algo.check_algo(), False)


def _reset_ordinal_squares(lgc: LogicState) -> None:
    """Resets the ordinal squares"""
    lgc.start = lgc.mid = lgc.end = None


def _reset_graph_button(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """Resets the graph"""
    reset_graph(gph, algo, txt, graph_max=lgc.GRAPH_MAX, graph_default=lgc.GRAPH_MEDIUM)
    _reset_ordinal_squares(lgc)


def _none_to_null_square(square) -> Square:
    """Turns a square from None to a null_square"""
    if square is None:
        square = Square.get_null_square()
    return square


def _run_pathfinding_algo(algo: AlgoState, lgc: LogicState, algo_to_run, visualize: bool) -> None:
    """Run's the specificed algo"""
    # Resets algo visualizations without removing ordinal squares or walls
    reset_algo(algo)

    # These fix sending none to C++
    start = _none_to_null_square(lgc.start)
    mid = _none_to_null_square(lgc.mid)
    end = _none_to_null_square(lgc.end)
    null_square = _none_to_null_square(None)       

    # Set algorithm to run
    algo.run_options(start, mid, end, null_square)
    algo.run(algo.PHASE_ALGO, algo_to_run)
    lgc.visualize = visualize
    if not visualize:
        algo.set_best_path_delay(0)


def _dijkstra_button(algo: AlgoState, lgc: LogicState) -> None:
    """Run the dijkstra algorithm"""
    _run_pathfinding_algo(algo, lgc, algo.ALGO_DIJKSTRA, True)


def _a_star_button(algo: AlgoState, lgc: LogicState) -> None:
    """Runs the A* algorithm"""
    _run_pathfinding_algo(algo, lgc, algo.ALGO_A_STAR, True)


def _bi_dijkstra_button(algo: AlgoState, lgc: LogicState) -> None:
    """Runs the Bi-Directional Dijkstra algorithm"""
    _run_pathfinding_algo(algo, lgc, algo.ALGO_BI_DIJKSTRA, True)


def _recursive_maze_buttons(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText, visualize) -> None:
    """Draws recursive maze"""
    reset_graph(gph, algo, txt)
    draw(gph, algo, txt, clear_legend=True)
    gph.base_drawn = False
    gph.update_legend = True
    _reset_ordinal_squares(lgc)

    # These fix sending none to C++
    start = _none_to_null_square(lgc.start)
    mid = _none_to_null_square(lgc.mid)
    end = _none_to_null_square(lgc.end)
    null_square = _none_to_null_square(None)       

    # Set algorithm to run
    algo.run_options(start, mid, end, null_square)
    algo.run(algo.PHASE_MAZE, algo.ALGO_RECURSIVE_MAZE)
    lgc.visualize = visualize
    if visualize:
        sleep(15, unit="ms")  # Need to sleep a bit for algo to work.
    else:
        algo.set_recursive_maze_delay(0)


def _graph_size_buttons(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText, new_graph_size) -> None:
    """Changes the size of the graph"""
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
