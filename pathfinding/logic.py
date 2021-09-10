"""Handles inputs from user"""
import pygame
from pathfinding.algorithms import dijkstra, a_star, bi_dijkstra, start_mid_end, algo_no_vis, draw_recursive_maze
from pathfinding.graph import set_graph, draw, reset_graph, reset_algo, HEIGHT
from pathfinding.graph import change_graph_size, wall_nodes, square_size, rows


# Extra variables
dijkstra_finished = False
a_star_finished = False
bi_dijkstra_finished = False
maze = False   # Used to prevent drawing extra walls during maze
ordinal_node_clicked = []   # Used for dragging start and end once algos are finished. Length is 0 or 1.


def get_clicked_pos(pos):
    """Turns the location data of the mouse into location of squares"""

    y, x = pos
    row = int(y / square_size)
    col = int(x / square_size)
    return row, col


# Put all game specific variables in here so it's easy to restart with main()
def main():
    """The pygame logic loop. This runs forever until exited. This is what should be called to run program."""

    global dijkstra_finished, a_star_finished, bi_dijkstra_finished, maze

    graph = set_graph()

    # Defining ordinal nodes to be used within the loop in various places
    start = None
    mid = None
    end = None

    run = True
    while run:
        draw(graph, legend=True)

        # Allow clicking the "X" on the pygame window to end the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Used to know if no longer dragging ordinal node after algo completion
            if not pygame.mouse.get_pressed(3)[0]:
                ordinal_node_clicked.clear()

            # LEFT MOUSE CLICK. HEIGHT condition prevents out of bound when clicking on legend.
            if pygame.mouse.get_pressed(3)[0] and pygame.mouse.get_pos()[1] < HEIGHT:

                # Get square clicked
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                square = graph[row][col]

                # Checks if algo is completed, used for dragging algo
                if (dijkstra_finished or a_star_finished or bi_dijkstra_finished) and start and end:

                    # Checks if ordinal node is being dragged
                    if ordinal_node_clicked:

                        # Checks if the mouse is currently on an ordinal node, no need to update anything
                        if square != start and square != mid and square != end:
                            last_square = ordinal_node_clicked[0]  # Used to move ordinal node to new pos

                            # Checks if ordinal node was previously a wall to reinstate it after moving, else reset
                            if last_square == 'start':
                                if start in wall_nodes:
                                    start.set_wall()
                                else:
                                    start.reset()
                                start = square
                                square.set_start()
                            elif last_square == 'mid':
                                if mid in wall_nodes:
                                    mid.set_wall()
                                else:
                                    mid.reset()
                                mid = square
                                square.set_mid()
                            elif last_square == 'end':
                                if end in wall_nodes:
                                    end.set_wall()
                                else:
                                    end.reset()
                                end = square
                                square.set_end()

                            # Runs the algo again instantly with no visualizations, handles whether mid exists
                            if dijkstra_finished:
                                if mid:
                                    start_mid_end(graph, start, mid, end, is_dijkstra=True, visualize=False)
                                else:
                                    algo_no_vis(graph, start, end, is_dijkstra=True)
                            elif a_star_finished:
                                if mid:
                                    start_mid_end(graph, start, mid, end, is_a_star=True, visualize=False)
                                else:
                                    algo_no_vis(graph, start, end, is_a_star=True)
                            elif bi_dijkstra_finished:
                                if mid:
                                    start_mid_end(graph, start, mid, end, is_bi_dijkstra=True, visualize=False)
                                else:
                                    algo_no_vis(graph, start, end, is_bi_dijkstra=True)

                    # If ordinal node is not being dragged, prepare it to
                    elif square is start:
                        ordinal_node_clicked.append('start')
                    elif square is mid:
                        ordinal_node_clicked.append('mid')
                    elif square is end:
                        ordinal_node_clicked.append('end')

                # If start node does not exist, create it. If not currently ordinal node.
                elif not start and square != mid and square != end:
                    start = square
                    square.set_start()

                    # Handles removing and adding start manually instead of dragging on algo completion.
                    if dijkstra_finished and start and end:
                        algo_no_vis(graph, start, end, is_dijkstra=True)
                    elif a_star_finished and start and end:
                        algo_no_vis(graph, start, end, is_a_star=True)
                    elif bi_dijkstra_finished and start and end:
                        algo_no_vis(graph, start, end, is_bi_dijkstra=True)

                # If end node does not exist, and start node does exist, create end node.
                # If not currently ordinal node.
                elif not end and square != start and square != mid:
                    end = square
                    square.set_end()

                    # Handles removing and adding end manually instead of dragging on algo completion.
                    if dijkstra_finished and start and end:
                        algo_no_vis(graph, start, end, is_dijkstra=True)
                    elif a_star_finished and start and end:
                        algo_no_vis(graph, start, end, is_a_star=True)
                    elif bi_dijkstra_finished and start and end:
                        algo_no_vis(graph, start, end, is_bi_dijkstra=True)

                # If start and end node exists, create wall. If not currently ordinal node.
                # Saves pos of wall to be able to reinstate it after dragging ordinal node past it.
                elif square != start and square != mid and square != end and maze is False:
                    square.set_wall()
                    wall_nodes.add(square)

            # RIGHT MOUSE CLICK. HEIGHT condition prevents out of bound when clicking on legend.
            elif pygame.mouse.get_pressed(3)[2] and pygame.mouse.get_pos()[1] < HEIGHT:

                # Get square clicked
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                square = graph[row][col]

                # If square to remove is wall, need to remove it from wall_node as well to retain accuracy
                if square.is_wall():
                    wall_nodes.discard(square)

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
                row, col = get_clicked_pos(pos)
                square = graph[row][col]

                # Set square to mid if no square is already mid, and not currently ordinal node.
                if not mid:
                    if square != start and square != end:
                        mid = square
                        square.set_mid()

                        # Handles removing and adding mid manually instead of dragging on algo completion.
                        if dijkstra_finished and start and mid and end:
                            start_mid_end(graph, start, mid, end, is_dijkstra=True, visualize=False)
                        elif a_star_finished and start and mid and end:
                            start_mid_end(graph, start, mid, end, is_a_star=True, visualize=False)
                        elif bi_dijkstra_finished and start and mid and end:
                            start_mid_end(graph, start, mid, end, is_bi_dijkstra=True, visualize=False)

            # Reset graph with "SPACE" on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_graph(graph)

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
                    reset_algo(graph)

                    # Updates neighbours in case anything has changed
                    for row in graph:
                        for square in row:
                            square.update_neighbours(graph)

                    # Necessary to for dragging nodes on completion
                    dijkstra_finished = True

                    # Handles whether or not mid exists
                    if mid:
                        start_mid_end(graph, start, mid, end, is_dijkstra=True)
                    else:
                        dijkstra(graph, start, end)

            # Run A* with "A" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:

                    # Resets algo visualizations without removing ordinal nodes or walls
                    reset_algo(graph)

                    # Updates neighbours in case anything has changed
                    for row in graph:
                        for square in row:
                            square.update_neighbours(graph)

                    # Necessary to for dragging nodes on completion
                    a_star_finished = True

                    # Handles whether or not mid exists
                    if mid:
                        start_mid_end(graph, start, mid, end, is_a_star=True)
                    else:
                        a_star(graph, start, end)

            # Run Bi-directional Dijkstra with "B" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and start and end:

                    # Resets algo visualizations without removing ordinal nodes or walls
                    reset_algo(graph)

                    # Updates neighbours in case anything has changed
                    for row in graph:
                        for square in row:
                            square.update_neighbours(graph)

                    # Necessary to for dragging nodes on completion
                    bi_dijkstra_finished = True

                    # Handles whether or not mid exists
                    if mid:
                        start_mid_end(graph, start, mid, end, is_bi_dijkstra=True)
                    else:
                        bi_dijkstra(graph, start, end)

            # Draw recursive maze with "G" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    # Resets entire graph to prevent any unintended behaviour
                    reset_graph(graph)

                    # Draw maze
                    draw_recursive_maze(graph)

                    # Necessary for handling dragging over barriers if in maze
                    maze = True

                    # Reset ordinal nodes as it cannot be in reset_graph due to scope
                    start = None
                    mid = None
                    end = None

            # Draw recursive maze with NO VISUALIZATIONS with "I" key on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    # Resets entire graph to prevent any unintended behaviour
                    reset_graph(graph)

                    # Draw maze instantly with no visualizations
                    draw_recursive_maze(graph, visualize=False)

                    # Necessary for handling dragging over barriers if in maze
                    maze = True

                    # Reset ordinal nodes as it cannot be in reset_graph due to scope
                    start = None
                    mid = None
                    end = None

            # Redraw small maze with "S" key on keyboard if not currently small
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:

                    # If maze is currently small, no need to redraw
                    if rows != 22:
                        # Changes graph size to small
                        graph = change_graph_size(22)

                        # Reset ordinal nodes as it cannot be in reset_graph due to scope
                        start = None
                        mid = None
                        end = None

            # Redraw medium maze with "M" key on keyboard if not currently medium
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:

                    # If maze is already medium, no need to redraw
                    if rows != 46:
                        # Changes graph size to medium
                        graph = change_graph_size(46)

                        # Reset ordinal nodes as it cannot be in reset_graph due to scope
                        start = None
                        mid = None
                        end = None

            # Redraw large maze with "L" key on keyboard if not currently large
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:

                    # If maze is already large, no need to redraw
                    if rows != 95:
                        # Changes graph size to large
                        graph = change_graph_size(95)

                        # Reset ordinal nodes as it cannot be in reset_graph due to scope
                        start = None
                        mid = None
                        end = None

    # Only reached if while loop ends, which happens if window is closed. Program terminates.
    pygame.quit()


'''
New features for the future:

Instantly update algo when draw wall after completion, much like dragging nodes
Add prim maze and sticky mud


Bugs to fix:

Instant algo even after clearing graph
Crash when changing graph size sometimes
When clicking to remove start/end node with mid node and reinstating it on completed algo, doesn't update properly
Bi-directional dijkstra only draws best_path when edges of swarms are touching. Only manifests with mid nodes
Maze can change size if window loses focus for a few seconds. Mainly with the large maze.
    pygame.event.set_grab prevents mouse from leaving window but also prevents exists
    pygame.mouse.get_focused() potential elegant solution
'''
