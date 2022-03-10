"""Handles inputs from user"""


import os
from dataclasses import dataclass
import pygame
from src.pathfinding.algorithms import (
    dijkstra,
    a_star,
    bi_dijkstra,
    start_mid_end,
    algo_no_vis,
    draw_recursive_maze,
    AlgoState,
)
from src.pathfinding.graph import (
    GraphState,
    VisText,
    set_graph,
    draw,
    reset_graph,
    reset_algo,
    change_graph_size,
    set_squares_to_roads,
    draw_vis_text,
    HEIGHT,
)
from src.pathfinding.node import Square
from typing import Optional
from src.pathfinding.maps import (
    get_img_base,
    write_img_base,
    get_img_clean,
    write_img_clean,
)
from src.pathfinding.maps import IMG_LOCATION, IMG_BASE_NAME, IMG_CLEAN_NAME


@dataclass
class LogicState:
    """Stores the state of the logic"""

    start: Optional[Square] = None
    mid: Optional[Square] = None
    end: Optional[Square] = None
    run: bool = True
    GRAPH_SMALL: int = 22
    GRAPH_MEDIUM: int = 46
    GRAPH_LARGE: int = 95
    GRAPH_MAX: int = 400
    BEST_PATH_SLEEP: int = 3


def run_pathfinding(
    gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText
) -> None:
    """The pygame logic loop. This runs forever until exited. This is what should be called to run program."""

    # Creates the graph nodes
    set_graph(gph)

    # Defines the FPS of the game. Used by clock.tick() at bottom of while loop
    clock = pygame.time.Clock()

    while lgc.run:
        draw(gph, txt, legend=True)  # Draws the graph with all the necessary updates

        for event in pygame.event.get():

            """Special cases"""

            # Allow clicking the "X" on the pygame window to end the program
            if event.type == pygame.QUIT:
                lgc.run = False

            """Mouse buttons"""

            # Used to know if no longer dragging ordinal node after algo completion
            if not pygame.mouse.get_pressed(3)[0]:
                algo.ordinal_node_clicked.clear()

            # LEFT MOUSE CLICK. HEIGHT condition prevents out of bound when clicking on legend.
            if pygame.mouse.get_pressed(3)[0] and pygame.mouse.get_pos()[1] < HEIGHT and not gph.has_img:
                _left_click_button(gph, algo, lgc, txt)

            # RIGHT MOUSE CLICK. HEIGHT condition prevents out of bound when clicking on legend.
            elif pygame.mouse.get_pressed(3)[2] and pygame.mouse.get_pos()[1] < HEIGHT and not gph.has_img:
                _right_click_button(gph, lgc)

            # MIDDLE MOUSE CLICK. HEIGHT condition prevents out of bound when clicking on legend.
            elif pygame.mouse.get_pressed(3)[1] and pygame.mouse.get_pos()[1] < HEIGHT and not gph.has_img:
                _middle_click_button(gph, algo, lgc, txt)

            """Keyboard buttons"""

            # Reset graph with "SPACE" on keyboard
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not gph.has_img:
                _reset_graph_button(gph, algo, lgc, txt)

            # Run Dijkstra with "D" key on keyboard
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_d
                and lgc.start
                and lgc.end
                and not gph.has_img
            ):
                _dijkstra_button(gph, algo, lgc, txt)

            # Run A* with "A" key on keyboard
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_a
                and lgc.start
                and lgc.end
                and not gph.has_img
            ):
                _a_star_button(gph, algo, lgc, txt)

            # Run Bi-directional Dijkstra with "B" key on keyboard
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_b
                and lgc.start
                and lgc.end
                and not gph.has_img
            ):
                _bi_dijkstra_button(gph, algo, lgc, txt)

            # Draw recursive maze with "G" key on keyboard
            if event.type == pygame.KEYDOWN and event.key == pygame.K_g and not gph.has_img:
                if gph.rows not in {lgc.GRAPH_SMALL, lgc.GRAPH_MEDIUM, lgc.GRAPH_LARGE}:
                    _graph_size_buttons(
                        gph, algo, lgc, txt, lgc.GRAPH_LARGE, lgc.BEST_PATH_SLEEP
                    )
                _recursive_maze_buttons(gph, algo, lgc, txt)

            # Draw recursive maze with NO VISUALIZATIONS with "I" key on keyboard
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i and not gph.has_img:
                if gph.rows not in {lgc.GRAPH_SMALL, lgc.GRAPH_MEDIUM, lgc.GRAPH_LARGE}:
                    _graph_size_buttons(
                        gph, algo, lgc, txt, lgc.GRAPH_LARGE, lgc.BEST_PATH_SLEEP
                    )
                _recursive_maze_buttons(gph, algo, lgc, txt, visualize=False)

            # Redraw small maze with "S" key on keyboard if not currently small
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_s
                and gph.rows != lgc.GRAPH_SMALL
                and not gph.has_img
            ):
                _graph_size_buttons(
                    gph, algo, lgc, txt, lgc.GRAPH_SMALL, lgc.BEST_PATH_SLEEP
                )

            # Redraw medium maze with "M" key on keyboard if not currently medium
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_m
                and gph.rows != lgc.GRAPH_MEDIUM
                and not gph.has_img
            ):
                _graph_size_buttons(
                    gph, algo, lgc, txt, lgc.GRAPH_MEDIUM, lgc.BEST_PATH_SLEEP
                )

            # Redraw large maze with "L" key on keyboard if not currently large
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_l
                and gph.rows != lgc.GRAPH_LARGE
                and not gph.has_img
            ):
                _graph_size_buttons(
                    gph, algo, lgc, txt, lgc.GRAPH_LARGE, lgc.BEST_PATH_SLEEP
                )

            # Convert map into grid with "C" key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c and gph.has_img:
                _convert_img_to_squares(gph, txt)

            # Enter an address with the "ENTER" key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                _get_address_from_user(gph, algo, lgc, txt)
            
            # Visualize changes with the "V" key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                _visualize_changes_button(gph, lgc, txt)

        clock.tick(gph.FPS)

    # Only reached if while loop ends, which happens if window is closed. Program terminates.
    pygame.quit()


def _get_clicked_pos(gph: GraphState, pos) -> tuple[int, int]:
    """Turns the location data of the mouse into location of squares"""
    y, x = pos
    row = int(y / gph.square_size)
    col = int(x / gph.square_size)
    return row, col


def _get_square_clicked(gph: GraphState) -> tuple[tuple[int, int], int, int, Square]:
    """Gets the the square that was clicked"""
    pos = pygame.mouse.get_pos()
    row, col = _get_clicked_pos(gph, pos)
    square: Square = gph.graph[row][col]
    return pos, row, col, square


def _left_click_button(
    gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText
) -> None:
    """Handles mouse left click"""

    pos, row, col, square = _get_square_clicked(gph)

    # Checks if algo is completed, used for dragging algo
    if (
        (algo.dijkstra_finished or algo.a_star_finished or algo.bi_dijkstra_finished)
        and lgc.start
        and lgc.end
    ):

        # Checks if ordinal node is being dragged
        if algo.ordinal_node_clicked:

            # Checks if the mouse is currently on an ordinal node, no need to update anything
            if square != lgc.start and square != lgc.mid and square != lgc.end:
                # Used to move ordinal node to new pos
                last_square = algo.ordinal_node_clicked[0]

                # Checks if ordinal node was previously a wall to reinstate it after moving, else reset
                if last_square == "start":
                    if lgc.start in Square.all_wall_nodes:
                        lgc.start.set_wall(gph)
                    else:
                        lgc.start.reset(gph)
                    lgc.start = square
                    square.set_start(gph)
                elif last_square == "mid":
                    if lgc.mid in Square.all_wall_nodes:
                        lgc.mid.set_wall(gph)
                    else:
                        lgc.mid.reset(gph)
                    lgc.mid = square
                    square.set_mid(gph)
                elif last_square == "end":
                    if lgc.end in Square.all_wall_nodes:
                        lgc.end.set_wall(gph)
                    else:
                        lgc.end.reset(gph)
                    lgc.end = square
                    square.set_end(gph)

                # Runs the algo again instantly with no visualizations, handles whether mid exists
                if algo.dijkstra_finished:
                    if lgc.mid:
                        start_mid_end(
                            gph,
                            algo,
                            txt,
                            lgc.start,
                            lgc.mid,
                            lgc.end,
                            is_dijkstra=True,
                            visualize=False,
                        )
                    else:
                        algo_no_vis(
                            gph, algo, txt, lgc.start, lgc.end, is_dijkstra=True
                        )
                elif algo.a_star_finished:
                    if lgc.mid:
                        start_mid_end(
                            gph,
                            algo,
                            txt,
                            lgc.start,
                            lgc.mid,
                            lgc.end,
                            is_a_star=True,
                            visualize=False,
                        )
                    else:
                        algo_no_vis(gph, algo, txt, lgc.start, lgc.end, is_a_star=True)
                elif algo.bi_dijkstra_finished:
                    if lgc.mid:
                        start_mid_end(
                            gph,
                            algo,
                            txt,
                            lgc.start,
                            lgc.mid,
                            lgc.end,
                            is_bi_dijkstra=True,
                            visualize=False,
                        )
                    else:
                        algo_no_vis(
                            gph, algo, txt, lgc.start, lgc.end, is_bi_dijkstra=True
                        )

        # If ordinal node is not being dragged, prepare it to
        elif square is lgc.start:
            algo.ordinal_node_clicked.append("start")
        elif square is lgc.mid:
            algo.ordinal_node_clicked.append("mid")
        elif square is lgc.end:
            algo.ordinal_node_clicked.append("end")

        # On algo completion, add wall and update algo
        else:
            # Add wall
            square.set_wall(gph)

            # Updates algo
            if algo.dijkstra_finished:
                _dijkstra_button(gph, algo, lgc, txt, visualize=False)
            elif algo.a_star_finished:
                _a_star_button(gph, algo, lgc, txt, visualize=False)
            elif algo.bi_dijkstra_finished:
                _bi_dijkstra_button(gph, algo, lgc, txt, visualize=False)

    # If start node does not exist, create it. If not currently ordinal node.
    elif not lgc.start and square != lgc.mid and square != lgc.end:
        lgc.start = square
        square.set_start(gph)

        # Handles removing and adding start manually instead of dragging on algo completion.
        if algo.dijkstra_finished and lgc.start and lgc.end:
            _dijkstra_button(gph, algo, lgc, txt, visualize=False)
        elif algo.a_star_finished and lgc.start and lgc.end:
            _a_star_button(gph, algo, lgc, txt, visualize=False)
        elif algo.bi_dijkstra_finished and lgc.start and lgc.end:
            _bi_dijkstra_button(gph, algo, lgc, txt, visualize=False)

    # If end node does not exist, and start node does exist, create end node.
    # If not currently ordinal node.
    elif not lgc.end and square != lgc.start and square != lgc.mid:
        lgc.end = square
        square.set_end(gph)

        # Handles removing and adding end manually instead of dragging on algo completion.
        if algo.dijkstra_finished and lgc.start and lgc.end:
            _dijkstra_button(gph, algo, lgc, txt, visualize=False)
        elif algo.a_star_finished and lgc.start and lgc.end:
            _a_star_button(gph, algo, lgc, txt, visualize=False)
        elif algo.bi_dijkstra_finished and lgc.start and lgc.end:
            _bi_dijkstra_button(gph, algo, lgc, txt, visualize=False)

    # If start and end node exists, create wall. If not currently ordinal node.
    # Saves pos of wall to be able to reinstate it after dragging ordinal node past it.
    elif (
        square != lgc.start
        and square != lgc.mid
        and square != lgc.end
        and algo.maze is False
    ):
        square.set_wall(gph)


def _right_click_button(gph: GraphState, lgc: LogicState) -> None:
    """Handles mouse right click"""

    pos, row, col, square = _get_square_clicked(gph)

    # Reset square and ordinal node if it was any
    square.reset(gph)
    if square == lgc.start:
        lgc.start = None
    elif square == lgc.mid:
        lgc.mid = None
    elif square == lgc.end:
        lgc.end = None


def _middle_click_button(
    gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText
) -> None:
    """Handles mouse wheel click"""

    pos, row, col, square = _get_square_clicked(gph)

    # Set square to mid if no square is already mid, and not currently ordinal node.
    if not lgc.mid and square != lgc.start and square != lgc.end:
        lgc.mid = square
        square.set_mid(gph)

        # Handles removing and adding mid manually instead of dragging on algo completion.
        if algo.dijkstra_finished and lgc.start and lgc.mid and lgc.end:
            start_mid_end(
                gph,
                algo,
                txt,
                lgc.start,
                lgc.mid,
                lgc.end,
                is_dijkstra=True,
                visualize=False,
            )
        elif algo.a_star_finished and lgc.start and lgc.mid and lgc.end:
            start_mid_end(
                gph,
                algo,
                txt,
                lgc.start,
                lgc.mid,
                lgc.end,
                is_a_star=True,
                visualize=False,
            )
        elif algo.bi_dijkstra_finished and lgc.start and lgc.mid and lgc.end:
            start_mid_end(
                gph,
                algo,
                txt,
                lgc.start,
                lgc.mid,
                lgc.end,
                is_bi_dijkstra=True,
                visualize=False,
            )


def _reset_ordinal_nodes(lgc: LogicState) -> None:
    """Resets the ordinal nodes"""
    lgc.start = lgc.mid = lgc.end = None


def _reset_graph_button(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """Resets the graph"""
    reset_graph(gph, algo, txt, graph_max=lgc.GRAPH_MAX, graph_default=lgc.GRAPH_MEDIUM)
    _reset_ordinal_nodes(lgc)


def _dijkstra_button(
    gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText, visualize=True
) -> None:
    """Run the dijkstra algorithm"""

    # Resets algo visualizations without removing ordinal nodes or walls
    reset_algo(gph, algo)
    draw(gph, txt, clear_legend=True, algo_running=True)

    # Necessary to for dragging nodes on completion
    algo.dijkstra_finished = True

    # Handles whether or not mid exists
    if lgc.mid:
        start_mid_end(
            gph,
            algo,
            txt,
            lgc.start,
            lgc.mid,
            lgc.end,
            is_dijkstra=True,
            visualize=visualize,
        )
    else:
        if visualize:
            dijkstra(gph, algo, txt, lgc.start, lgc.end)
        else:
            algo_no_vis(gph, algo, txt, lgc.start, lgc.end, is_dijkstra=True)


def _a_star_button(
    gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText, visualize=True
) -> None:
    """Runs the A* algorithm"""

    # Resets algo visualizations without removing ordinal nodes or walls
    reset_algo(gph, algo)
    draw(gph, txt, clear_legend=True, algo_running=True)

    # Necessary to for dragging nodes on completion
    algo.a_star_finished = True

    # Handles whether or not mid exists
    if lgc.mid:
        start_mid_end(
            gph,
            algo,
            txt,
            lgc.start,
            lgc.mid,
            lgc.end,
            is_a_star=True,
            visualize=visualize,
        )
    else:
        if visualize:
            a_star(gph, algo, txt, lgc.start, lgc.end)
        else:
            algo_no_vis(gph, algo, txt, lgc.start, lgc.end, is_a_star=True)


def _bi_dijkstra_button(
    gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText, visualize=True
) -> None:
    """Runs the Bi-Directional Dijkstra algorithm"""

    # Resets algo visualizations without removing ordinal nodes or walls
    reset_algo(gph, algo)
    draw(gph, txt, clear_legend=True, algo_running=True)

    # Necessary to for dragging nodes on completion
    algo.bi_dijkstra_finished = True

    # Handles whether or not mid exists
    if lgc.mid:
        start_mid_end(
            gph,
            algo,
            txt,
            lgc.start,
            lgc.mid,
            lgc.end,
            is_bi_dijkstra=True,
            visualize=visualize,
        )
    else:
        if visualize:
            bi_dijkstra(gph, algo, txt, lgc.start, lgc.end)
        else:
            algo_no_vis(gph, algo, txt, lgc.start, lgc.end, is_bi_dijkstra=True)


def _recursive_maze_buttons(
    gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText, visualize=True
) -> None:
    """Draws recursive maze"""
    reset_graph(gph, algo, txt)  # Resets entire graph to prevent any unintended behaviour
    draw(gph, txt, clear_legend=True, algo_running=True)
    gph.base_drawn = False
    draw_recursive_maze(gph, txt, visualize=visualize)  # Draw maze
    gph.update_legend = True
    algo.maze = True  # Necessary for handling dragging over barriers if in maze
    _reset_ordinal_nodes(lgc)


def _graph_size_buttons(
    gph: GraphState,
    algo: AlgoState,
    lgc: LogicState,
    txt: VisText,
    new_graph_size,
    best_path_sleep,
) -> None:
    """Changes the size of the graph"""
    algo.best_path_sleep = best_path_sleep
    gph.has_img = False
    change_graph_size(gph, algo, txt, new_graph_size)
    _reset_ordinal_nodes(lgc)


def _load_img_to_graph(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """Loads the image onto the graph"""
    
    change_graph_size(gph, algo, txt, lgc.GRAPH_MAX, to_draw=False)

    write_img_base(get_img_base(txt.address))

    gph.has_img = True
    gph.img = pygame.image.load(os.path.join(IMG_LOCATION, IMG_BASE_NAME))
    os.remove(os.path.join(IMG_LOCATION, IMG_BASE_NAME))
    set_graph(gph)
    draw(gph, txt)
    _reset_ordinal_nodes(lgc)


def _convert_img_to_squares(gph: GraphState, txt: VisText) -> None:
    """Coverts the map data into nodes the algorithms can use"""

    write_img_clean(get_img_clean(txt.address))

    gph.img = pygame.image.load(os.path.join(IMG_LOCATION, IMG_CLEAN_NAME))
    os.remove(os.path.join(IMG_LOCATION, IMG_CLEAN_NAME))

    gph.base_drawn = False
    draw(gph, txt)

    gph.update_legend = True
    gph.has_img = False
    gph.speed_multiplier = 500

    set_squares_to_roads(gph)


def _get_address_from_user(gph: GraphState, algo: AlgoState, lgc: LogicState, txt: VisText) -> None:
    """Gets the address from the user"""

    # Used to get rid of commas inserted by url encoding.
    txt.address = txt.address.replace(",", "")

    gph.base_drawn = False
    draw(gph, txt)
    draw_vis_text(txt, is_input=True)

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

                draw_vis_text(txt, is_input=True)

    pygame.quit()


def _visualize_changes_button(gph: GraphState, lgc: LogicState, txt: VisText) -> None:
    """Visualize the changed parts of the screen between toggles"""
    # Stop tracking node history and display it
    if Square.track_node_history:
        Square.track_node_history = False
        gph.visualize_node_history = True
        gph.update_legend = True
        draw(gph, txt, legend=True)
    # Start tracking node history
    else:
        Square.track_node_history = True
        gph.update_legend = True
        draw(gph, txt, legend=True)
