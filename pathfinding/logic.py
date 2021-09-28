"""Handles inputs from user"""


import os.path
from dataclasses import dataclass
import pygame
from pathfinding.algorithms import dijkstra, a_star, bi_dijkstra, \
    start_mid_end, algo_no_vis, draw_recursive_maze, AlgoState
from pathfinding.graph import set_graph, draw, reset_graph, \
    reset_algo, change_graph_size, GraphState, set_squares_to_roads, HEIGHT
from pathfinding.node import Square
from typing import Optional
from pathfinding.maps import get_img_base, write_img_base, get_img_clean, write_img_clean


@dataclass
class LogicState:
    """Stores the state of the logic"""

    FPS: int
    start: Optional[Square]
    mid: Optional[Square]
    end: Optional[Square]
    run: bool


def get_clicked_pos(gph: GraphState, pos) -> tuple[int, int]:
    """Turns the location data of the mouse into location of squares"""

    y, x = pos
    row = int(y / gph.square_size)
    col = int(x / gph.square_size)
    return row, col


# Put all game specific variables in here so it's easy to restart with main()
def run_pathfinding(gph: GraphState, algo: AlgoState, lgc: LogicState) -> None:
    """The pygame logic loop. This runs forever until exited. This is what should be called to run program."""

    # Creates the graph nodes
    set_graph(gph)

    # Defines the FPS of the game. Used by clock.tick() at bottom of while loop
    clock = pygame.time.Clock()

    while lgc.run:
        draw(gph, legend=True)  # Draws the graph with all the necessary updates

        # Allow clicking the "X" on the pygame window to end the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lgc.run = False

            # Used to know if no longer dragging ordinal node after algo completion
            if not pygame.mouse.get_pressed(3)[0]:
                algo.ordinal_node_clicked.clear()

            # LEFT MOUSE CLICK. HEIGHT condition prevents out of bound when clicking on legend.
            if pygame.mouse.get_pressed(3)[0] and pygame.mouse.get_pos()[1] < HEIGHT:

                # Get square clicked
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(gph, pos)
                square = gph.graph[row][col]

                # Checks if algo is completed, used for dragging algo
                if (algo.dijkstra_finished or algo.a_star_finished or
                        algo.bi_dijkstra_finished) and lgc.start and lgc.end:

                    # Checks if ordinal node is being dragged
                    if algo.ordinal_node_clicked:

                        # Checks if the mouse is currently on an ordinal node, no need to update anything
                        if square != lgc.start and square != lgc.mid and square != lgc.end:
                            last_square = algo.ordinal_node_clicked[0]  # Used to move ordinal node to new pos

                            # Checks if ordinal node was previously a wall to reinstate it after moving, else reset
                            if last_square == 'start':
                                if lgc.start in gph.wall_nodes:
                                    lgc.start.set_wall()
                                else:
                                    lgc.start.reset()
                                lgc.start = square
                                square.set_start()
                            elif last_square == 'mid':
                                if lgc.mid in gph.wall_nodes:
                                    lgc.mid.set_wall()
                                else:
                                    lgc.mid.reset()
                                lgc.mid = square
                                square.set_mid()
                            elif last_square == 'end':
                                if lgc.end in gph.wall_nodes:
                                    lgc.end.set_wall()
                                else:
                                    lgc.end.reset()
                                lgc.end = square
                                square.set_end()

                            # Runs the algo again instantly with no visualizations, handles whether mid exists
                            if algo.dijkstra_finished:
                                if lgc.mid:
                                    start_mid_end(gph, algo, lgc.start, lgc.mid, lgc.end,
                                                  is_dijkstra=True, visualize=False)
                                else:
                                    algo_no_vis(gph, algo, lgc.start, lgc.end, is_dijkstra=True)
                            elif algo.a_star_finished:
                                if lgc.mid:
                                    start_mid_end(gph, algo, lgc.start, lgc.mid, lgc.end,
                                                  is_a_star=True, visualize=False)
                                else:
                                    algo_no_vis(gph, algo, lgc.start, lgc.end, is_a_star=True)
                            elif algo.bi_dijkstra_finished:
                                if lgc.mid:
                                    start_mid_end(gph, algo, lgc.start, lgc.mid, lgc.end,
                                                  is_bi_dijkstra=True, visualize=False)
                                else:
                                    algo_no_vis(gph, algo, lgc.start, lgc.end, is_bi_dijkstra=True)

                    # If ordinal node is not being dragged, prepare it to
                    elif square is lgc.start:
                        algo.ordinal_node_clicked.append('start')
                    elif square is lgc.mid:
                        algo.ordinal_node_clicked.append('mid')
                    elif square is lgc.end:
                        algo.ordinal_node_clicked.append('end')

                # If start node does not exist, create it. If not currently ordinal node.
                elif not lgc.start and square != lgc.mid and square != lgc.end:
                    lgc.start = square
                    square.set_start()

                    # Handles removing and adding start manually instead of dragging on algo completion.
                    if algo.dijkstra_finished and lgc.start and lgc.end:
                        algo_no_vis(gph, algo, lgc.start, lgc.end, is_dijkstra=True)
                    elif algo.a_star_finished and lgc.start and lgc.end:
                        algo_no_vis(gph, algo, lgc.start, lgc.end, is_a_star=True)
                    elif algo.bi_dijkstra_finished and lgc.start and lgc.end:
                        algo_no_vis(gph, algo, lgc.start, lgc.end, is_bi_dijkstra=True)

                # If end node does not exist, and start node does exist, create end node.
                # If not currently ordinal node.
                elif not lgc.end and square != lgc.start and square != lgc.mid:
                    lgc.end = square
                    square.set_end()

                    # Handles removing and adding end manually instead of dragging on algo completion.
                    if algo.dijkstra_finished and lgc.start and lgc.end:
                        algo_no_vis(gph, algo, lgc.start, lgc.end, is_dijkstra=True)
                    elif algo.a_star_finished and lgc.start and lgc.end:
                        algo_no_vis(gph, algo, lgc.start, lgc.end, is_a_star=True)
                    elif algo.bi_dijkstra_finished and lgc.start and lgc.end:
                        algo_no_vis(gph, algo, lgc.start, lgc.end, is_bi_dijkstra=True)

                # If start and end node exists, create wall. If not currently ordinal node.
                # Saves pos of wall to be able to reinstate it after dragging ordinal node past it.
                elif square != lgc.start and square != lgc.mid and square != lgc.end and algo.maze is False:
                    square.set_wall()
                    gph.wall_nodes.add(square)

            # RIGHT MOUSE CLICK. HEIGHT condition prevents out of bound when clicking on legend.
            elif pygame.mouse.get_pressed(3)[2] and pygame.mouse.get_pos()[1] < HEIGHT:

                # Get square clicked
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(gph, pos)
                square = gph.graph[row][col]

                # If square to remove is wall, need to remove it from wall_node as well to retain accuracy
                if square.is_wall():
                    gph.wall_nodes.discard(square)

                # Reset square and ordinal node if it was any
                square.reset()
                if square == lgc.start:
                    lgc.start = None
                elif square == lgc.mid:
                    lgc.mid = None
                elif square == lgc.end:
                    lgc.end = None

            # MIDDLE MOUSE CLICK. HEIGHT condition prevents out of bound when clicking on legend.
            elif pygame.mouse.get_pressed(3)[1] and pygame.mouse.get_pos()[1] < HEIGHT:

                # Get square clicked
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(gph, pos)
                square = gph.graph[row][col]

                # Set square to mid if no square is already mid, and not currently ordinal node.
                if not lgc.mid:
                    if square != lgc.start and square != lgc.end:
                        lgc.mid = square
                        square.set_mid()

                        # Handles removing and adding mid manually instead of dragging on algo completion.
                        if algo.dijkstra_finished and lgc.start and lgc.mid and lgc.end:
                            start_mid_end(gph, algo, lgc.start, lgc.mid, lgc.end, is_dijkstra=True, visualize=False)
                        elif algo.a_star_finished and lgc.start and lgc.mid and lgc.end:
                            start_mid_end(gph, algo, lgc.start, lgc.mid, lgc.end, is_a_star=True, visualize=False)
                        elif algo.bi_dijkstra_finished and lgc.start and lgc.mid and lgc.end:
                            start_mid_end(gph, algo, lgc.start, lgc.mid, lgc.end, is_bi_dijkstra=True, visualize=False)

            # Reset graph with "SPACE" on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_graph(gph, algo)

                    lgc.start = None
                    lgc.mid = None
                    lgc.end = None

            # Run Dijkstra with "D" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and lgc.start and lgc.end:

                    # Resets algo visualizations without removing ordinal nodes or walls
                    reset_algo(gph, algo)

                    # Updates neighbours in case anything has changed
                    for row in gph.graph:
                        for square in row:
                            square.update_neighbours(gph)

                    # Necessary to for dragging nodes on completion
                    algo.dijkstra_finished = True

                    # Handles whether or not mid exists
                    if lgc.mid:
                        start_mid_end(gph, algo, lgc.start, lgc.mid, lgc.end, is_dijkstra=True)
                    else:
                        dijkstra(gph, algo, lgc.start, lgc.end)

            # Run A* with "A" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and lgc.start and lgc.end:

                    # Resets algo visualizations without removing ordinal nodes or walls
                    reset_algo(gph, algo)

                    # Updates neighbours in case anything has changed
                    for row in gph.graph:
                        for square in row:
                            square.update_neighbours(gph)

                    # Necessary to for dragging nodes on completion
                    algo.a_star_finished = True

                    # Handles whether or not mid exists
                    if lgc.mid:
                        start_mid_end(gph, algo, lgc.start, lgc.mid, lgc.end, is_a_star=True)
                    else:
                        a_star(gph, algo, lgc.start, lgc.end)

            # Run Bi-directional Dijkstra with "B" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and lgc.start and lgc.end:

                    # Resets algo visualizations without removing ordinal nodes or walls
                    reset_algo(gph, algo)

                    # Updates neighbours in case anything has changed
                    for row in gph.graph:
                        for square in row:
                            square.update_neighbours(gph)

                    # Necessary to for dragging nodes on completion
                    algo.bi_dijkstra_finished = True

                    # Handles whether or not mid exists
                    if lgc.mid:
                        start_mid_end(gph, algo, lgc.start, lgc.mid, lgc.end, is_bi_dijkstra=True)
                    else:
                        bi_dijkstra(gph, algo, lgc.start, lgc.end)

            # Draw recursive maze with "G" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    # Resets entire graph to prevent any unintended behaviour
                    reset_graph(gph, algo)

                    # Draw maze
                    draw_recursive_maze(gph)

                    # Necessary for handling dragging over barriers if in maze
                    algo.maze = True

                    lgc.start = None
                    lgc.mid = None
                    lgc.end = None

            # Draw recursive maze with NO VISUALIZATIONS with "I" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    # Resets entire graph to prevent any unintended behaviour
                    reset_graph(gph, algo)

                    # Draw maze instantly with no visualizations
                    draw_recursive_maze(gph, visualize=False)

                    # Necessary for handling dragging over barriers if in maze
                    algo.maze = True

                    lgc.start = None
                    lgc.mid = None
                    lgc.end = None

            # Redraw small maze with "S" key on keyboard if not currently small
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:

                    # If maze is currently small, no need to redraw
                    if gph.rows != 22:
                        # Changes graph size to small
                        algo.best_path_sleep = 3
                        gph.has_img = False
                        change_graph_size(gph, algo, 22)

                        lgc.start = None
                        lgc.mid = None
                        lgc.end = None

            # Redraw medium maze with "M" key on keyboard if not currently medium
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:

                    # If maze is already medium, no need to redraw
                    if gph.rows != 46:
                        # Changes graph size to medium
                        algo.best_path_sleep = 3
                        gph.has_img = False
                        change_graph_size(gph, algo, 46)

                        lgc.start = None
                        lgc.mid = None
                        lgc.end = None

            # Redraw large maze with "L" key on keyboard if not currently large
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:

                    # If maze is already large, no need to redraw
                    if gph.rows != 95:
                        # Changes graph size to large
                        algo.best_path_sleep = 3
                        gph.has_img = False
                        change_graph_size(gph, algo, 95)

                        lgc.start = None
                        lgc.mid = None
                        lgc.end = None

            # Redraw large maze with "X" key on keyboard if not currently x-large
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:

                    # If maze is already large, no need to redraw
                    if not gph.has_img:
                        # Changes graph size to large
                        gph.has_img = True
                        gph.img = pygame.image.load(os.path.join('pathfinding', 'img_base.jpg')).convert()
                        change_graph_size(gph, algo, 400)

                        lgc.start = None
                        lgc.mid = None
                        lgc.end = None

            # Convert map into grid with "C" key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    if gph.has_img:
                        gph.img = pygame.image.load(os.path.join('pathfinding', 'img_clean.jpg')).convert()
                        draw(gph, legend=True)
                        gph.has_img = False
                        set_squares_to_roads(gph)

        clock.tick(lgc.FPS)

    # Only reached if while loop ends, which happens if window is closed. Program terminates.
    pygame.quit()


'''
New features for the future:

Instantly update algo when draw wall after completion, much like dragging nodes
Add prim maze and sticky mud


Bugs to fix:

When clicking to remove start/end node with mid node and reinstating it on completed algo, doesn't update properly
Bi-directional dijkstra only draws best_path when edges of swarms are touching. Only manifests with mid nodes
Maze can change size if window loses focus for a few seconds. Mainly with the large maze.
    pygame.event.set_grab prevents mouse from leaving window but also prevents exists
    pygame.mouse.get_focused() potential elegant solution
'''
