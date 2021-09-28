"""Handles inputs from user"""


import os.path
import pygame
from pathfinding.algorithms import dijkstra, a_star, bi_dijkstra, \
    start_mid_end, algo_no_vis, draw_recursive_maze, AlgoState
from pathfinding.graph import set_graph, draw, reset_graph, \
    reset_algo, change_graph_size, GraphState, set_squares_to_roads, HEIGHT
from pathfinding.maps import get_img_base, write_img_base, get_img_clean, write_img_clean


def get_clicked_pos(gph: GraphState, pos) -> tuple[int, int]:
    """Turns the location data of the mouse into location of squares"""

    y, x = pos
    row = int(y / gph.square_size)
    col = int(x / gph.square_size)
    return row, col


# Put all game specific variables in here so it's easy to restart with main()
def run_pathfinding(gph: GraphState, algo: AlgoState) -> None:
    """The pygame logic loop. This runs forever until exited. This is what should be called to run program."""

    graph = set_graph(gph)

    # Defining ordinal nodes to be used within the loop in various places
    start = None
    mid = None
    end = None

    # Defines the FPS of the game. Used by clock.tick() at bottom of while loop
    FPS = 60
    clock = pygame.time.Clock()

    run = True
    while run:
        draw(graph, gph, legend=True)

        # Allow clicking the "X" on the pygame window to end the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Used to know if no longer dragging ordinal node after algo completion
            if not pygame.mouse.get_pressed(3)[0]:
                algo.ordinal_node_clicked.clear()

            # LEFT MOUSE CLICK. HEIGHT condition prevents out of bound when clicking on legend.
            if pygame.mouse.get_pressed(3)[0] and pygame.mouse.get_pos()[1] < HEIGHT:

                # Get square clicked
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(gph, pos)
                square = graph[row][col]

                # Checks if algo is completed, used for dragging algo
                if (algo.dijkstra_finished or algo.a_star_finished or algo.bi_dijkstra_finished) and start and end:

                    # Checks if ordinal node is being dragged
                    if algo.ordinal_node_clicked:

                        # Checks if the mouse is currently on an ordinal node, no need to update anything
                        if square != start and square != mid and square != end:
                            last_square = algo.ordinal_node_clicked[0]  # Used to move ordinal node to new pos

                            # Checks if ordinal node was previously a wall to reinstate it after moving, else reset
                            if last_square == 'start':
                                if start in gph.wall_nodes:
                                    start.set_wall()
                                else:
                                    start.reset()
                                start = square
                                square.set_start()
                            elif last_square == 'mid':
                                if mid in gph.wall_nodes:
                                    mid.set_wall()
                                else:
                                    mid.reset()
                                mid = square
                                square.set_mid()
                            elif last_square == 'end':
                                if end in gph.wall_nodes:
                                    end.set_wall()
                                else:
                                    end.reset()
                                end = square
                                square.set_end()

                            # Runs the algo again instantly with no visualizations, handles whether mid exists
                            if algo.dijkstra_finished:
                                if mid:
                                    start_mid_end(graph, start, mid, end, gph, algo, is_dijkstra=True, visualize=False)
                                else:
                                    algo_no_vis(graph, start, end, gph, algo, is_dijkstra=True)
                            elif algo.a_star_finished:
                                if mid:
                                    start_mid_end(graph, start, mid, end, gph, algo, is_a_star=True, visualize=False)
                                else:
                                    algo_no_vis(graph, start, end, gph, algo, is_a_star=True)
                            elif algo.bi_dijkstra_finished:
                                if mid:
                                    start_mid_end(graph, start, mid, end, gph, algo,
                                                  is_bi_dijkstra=True, visualize=False)
                                else:
                                    algo_no_vis(graph, start, end, gph, algo, is_bi_dijkstra=True)

                    # If ordinal node is not being dragged, prepare it to
                    elif square is start:
                        algo.ordinal_node_clicked.append('start')
                    elif square is mid:
                        algo.ordinal_node_clicked.append('mid')
                    elif square is end:
                        algo.ordinal_node_clicked.append('end')

                # If start node does not exist, create it. If not currently ordinal node.
                elif not start and square != mid and square != end:
                    start = square
                    square.set_start()

                    # Handles removing and adding start manually instead of dragging on algo completion.
                    if algo.dijkstra_finished and start and end:
                        algo_no_vis(graph, start, end, gph, algo, is_dijkstra=True)
                    elif algo.a_star_finished and start and end:
                        algo_no_vis(graph, start, end, gph, algo, is_a_star=True)
                    elif algo.bi_dijkstra_finished and start and end:
                        algo_no_vis(graph, start, end, gph, algo, is_bi_dijkstra=True)

                # If end node does not exist, and start node does exist, create end node.
                # If not currently ordinal node.
                elif not end and square != start and square != mid:
                    end = square
                    square.set_end()

                    # Handles removing and adding end manually instead of dragging on algo completion.
                    if algo.dijkstra_finished and start and end:
                        algo_no_vis(graph, start, end, gph, algo, is_dijkstra=True)
                    elif algo.a_star_finished and start and end:
                        algo_no_vis(graph, start, end, gph, algo, is_a_star=True)
                    elif algo.bi_dijkstra_finished and start and end:
                        algo_no_vis(graph, start, end, gph, algo, is_bi_dijkstra=True)

                # If start and end node exists, create wall. If not currently ordinal node.
                # Saves pos of wall to be able to reinstate it after dragging ordinal node past it.
                elif square != start and square != mid and square != end and algo.maze is False:
                    square.set_wall()
                    gph.wall_nodes.add(square)

            # RIGHT MOUSE CLICK. HEIGHT condition prevents out of bound when clicking on legend.
            elif pygame.mouse.get_pressed(3)[2] and pygame.mouse.get_pos()[1] < HEIGHT:

                # Get square clicked
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(gph, pos)
                square = graph[row][col]

                # If square to remove is wall, need to remove it from wall_node as well to retain accuracy
                if square.is_wall():
                    gph.wall_nodes.discard(square)

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
                row, col = get_clicked_pos(gph, pos)
                square = graph[row][col]

                # Set square to mid if no square is already mid, and not currently ordinal node.
                if not mid:
                    if square != start and square != end:
                        mid = square
                        square.set_mid()

                        # Handles removing and adding mid manually instead of dragging on algo completion.
                        if algo.dijkstra_finished and start and mid and end:
                            start_mid_end(graph, start, mid, end, gph, algo, is_dijkstra=True, visualize=False)
                        elif algo.a_star_finished and start and mid and end:
                            start_mid_end(graph, start, mid, end, gph, algo, is_a_star=True, visualize=False)
                        elif algo.bi_dijkstra_finished and start and mid and end:
                            start_mid_end(graph, start, mid, end, gph, algo, is_bi_dijkstra=True, visualize=False)

            # Reset graph with "SPACE" on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_graph(graph, gph, algo)

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
                    reset_algo(graph, gph, algo)

                    # Updates neighbours in case anything has changed
                    for row in graph:
                        for square in row:
                            square.update_neighbours(graph)

                    # Necessary to for dragging nodes on completion
                    algo.dijkstra_finished = True

                    # Handles whether or not mid exists
                    if mid:
                        start_mid_end(graph, start, mid, end, gph, algo, is_dijkstra=True)
                    else:
                        dijkstra(graph, start, end, gph, algo)

            # Run A* with "A" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:

                    # Resets algo visualizations without removing ordinal nodes or walls
                    reset_algo(graph, gph, algo)

                    # Updates neighbours in case anything has changed
                    for row in graph:
                        for square in row:
                            square.update_neighbours(graph)

                    # Necessary to for dragging nodes on completion
                    algo.a_star_finished = True

                    # Handles whether or not mid exists
                    if mid:
                        start_mid_end(graph, start, mid, end, gph, algo, is_a_star=True)
                    else:
                        a_star(graph, start, end, gph, algo)

            # Run Bi-directional Dijkstra with "B" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and start and end:

                    # Resets algo visualizations without removing ordinal nodes or walls
                    reset_algo(graph, gph, algo)

                    # Updates neighbours in case anything has changed
                    for row in graph:
                        for square in row:
                            square.update_neighbours(graph)

                    # Necessary to for dragging nodes on completion
                    algo.bi_dijkstra_finished = True

                    # Handles whether or not mid exists
                    if mid:
                        start_mid_end(graph, start, mid, end, gph, algo, is_bi_dijkstra=True)
                    else:
                        bi_dijkstra(graph, start, end, gph, algo)

            # Draw recursive maze with "G" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    # Resets entire graph to prevent any unintended behaviour
                    reset_graph(graph, gph, algo)

                    # Draw maze
                    draw_recursive_maze(graph, gph)

                    # Necessary for handling dragging over barriers if in maze
                    algo.maze = True

                    # Reset ordinal nodes as it cannot be in reset_graph due to scope
                    start = None
                    mid = None
                    end = None

            # Draw recursive maze with NO VISUALIZATIONS with "I" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    # Resets entire graph to prevent any unintended behaviour
                    reset_graph(graph, gph, algo)

                    # Draw maze instantly with no visualizations
                    draw_recursive_maze(graph, gph, visualize=False)

                    # Necessary for handling dragging over barriers if in maze
                    algo.maze = True

                    # Reset ordinal nodes as it cannot be in reset_graph due to scope
                    start = None
                    mid = None
                    end = None

            # Redraw small maze with "S" key on keyboard if not currently small
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:

                    # If maze is currently small, no need to redraw
                    if gph.rows != 22:
                        # Changes graph size to small
                        algo.best_path_sleep = 3
                        gph.has_img = False
                        graph = change_graph_size(22, gph)

                        # Reset ordinal nodes as it cannot be in reset_graph due to scope
                        start = None
                        mid = None
                        end = None

            # Redraw medium maze with "M" key on keyboard if not currently medium
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:

                    # If maze is already medium, no need to redraw
                    if gph.rows != 46:
                        # Changes graph size to medium
                        algo.best_path_sleep = 3
                        gph.has_img = False
                        graph = change_graph_size(46, gph)

                        # Reset ordinal nodes as it cannot be in reset_graph due to scope
                        start = None
                        mid = None
                        end = None

            # Redraw large maze with "L" key on keyboard if not currently large
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:

                    # If maze is already large, no need to redraw
                    if gph.rows != 95:
                        # Changes graph size to large
                        algo.best_path_sleep = 3
                        gph.has_img = False
                        graph = change_graph_size(95, gph)

                        # Reset ordinal nodes as it cannot be in reset_graph due to scope
                        start = None
                        mid = None
                        end = None

            # Redraw large maze with "X" key on keyboard if not currently x-large
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:

                    # If maze is already large, no need to redraw
                    if not gph.has_img:
                        # Changes graph size to large
                        algo.best_path_sleep = 0
                        gph.has_img = True
                        gph.img = pygame.image.load(os.path.join('pathfinding', 'img_base.jpg')).convert()
                        graph = change_graph_size(400, gph)

                        # Reset ordinal nodes as it cannot be in reset_graph due to scope
                        start = None
                        mid = None
                        end = None

            # Convert map into grid with "C" key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    if gph.has_img:
                        gph.img = pygame.image.load(os.path.join('pathfinding', 'img_clean.jpg')).convert()
                        draw(graph, gph, legend=True)
                        gph.has_img = False
                        set_squares_to_roads(graph, gph)

        clock.tick(FPS)

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
