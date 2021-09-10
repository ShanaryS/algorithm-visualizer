"""Contains pathfinding and maze generation algorithms"""
import pygame
from pathfinding.colors import *
from pathfinding.graph import draw, draw_vis_text, reset_algo, wall_nodes, rows
from pathfinding.values import get_random_sample, get_randrange
from queue import PriorityQueue


# Sleep time (ms) between each best_path node when visualizing
BEST_PATH_SLEEP = 3


def dijkstra(graph, start, end, ignore_node=None, draw_best_path=True, visualize=True):
    """Code for the dijkstra algorithm"""

    # Used to determine the order of squares to check. Order of args helper decide the priority.
    queue_pos = 0
    open_set = PriorityQueue()
    open_set.put((0, queue_pos, start))
    open_set_hash = {start}

    # Determine what is the best square to check
    g_score = {square: float('inf') for row in graph for square in row}
    g_score[start] = 0

    # Keeps track of next node for every node in graph. A linked list basically.
    came_from = {}

    # Continues until every node has been checked or best path found
    while not open_set.empty():

        # If uses closes window the program terminates
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Gets the square currently being checked
        curr_square = open_set.get()[2]
        open_set_hash.remove(curr_square)

        # Terminates if found the best path
        if curr_square == end:
            if draw_best_path:
                best_path(graph, came_from, end, visualize=visualize)
                return True

            return came_from

        # Decides the order of neighbours to check
        for nei in curr_square.neighbours:
            temp_g_score = g_score[curr_square] + 1

            if temp_g_score < g_score[nei]:
                came_from[nei] = curr_square
                g_score[nei] = temp_g_score
                if nei not in open_set_hash:
                    queue_pos += 1
                    open_set.put((g_score[nei], queue_pos, nei))
                    open_set_hash.add(nei)
                    if nei != end and nei.color != CLOSED_COLOR and nei != ignore_node:
                        nei.set_open()

        # Only visualize if called. Checks if square is closed to not repeat when mid node included.
        if visualize and not curr_square.is_closed():
            draw(graph, display_update=False)
            draw_vis_text(is_dijkstra=True)

        # Sets square to closed after finished checking
        if curr_square != start and curr_square != ignore_node:
            curr_square.set_closed()

    return False


def a_star(graph, start, end, ignore_node=None, draw_best_path=True, visualize=True):
    """Code for the A* algorithm"""

    # Used to determine the order of squares to check. Order of args helper decide the priority.
    queue_pos = 0
    open_set = PriorityQueue()
    open_set.put((0, queue_pos, start))
    open_set_hash = {start}

    # Determine what is the best square to check
    g_score = {square: float('inf') for row in graph for square in row}
    g_score[start] = 0
    f_score = {square: float('inf') for row in graph for square in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    # Keeps track of next node for every node in graph. A linked list basically.
    came_from = {}

    # Continues until every node has been checked or best path found
    while not open_set.empty():

        # If uses closes window the program terminates
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Gets the square currently being checked
        curr_square = open_set.get()[2]
        open_set_hash.remove(curr_square)

        # Terminates if found the best path
        if curr_square == end:
            if draw_best_path:
                best_path(graph, came_from, end, visualize=visualize)
                return True

            return came_from

        # Decides the order of neighbours to check
        for nei in curr_square.neighbours:
            temp_g_score = g_score[curr_square] + 1

            if temp_g_score < g_score[nei]:
                came_from[nei] = curr_square
                g_score[nei] = temp_g_score
                f_score[nei] = temp_g_score + heuristic(nei.get_pos(), end.get_pos())
                if nei not in open_set_hash:
                    queue_pos += 1
                    open_set.put((f_score[nei], queue_pos, nei))
                    open_set_hash.add(nei)
                    if nei != end and nei.color != CLOSED_COLOR and nei != ignore_node:
                        nei.set_open()

        # Only visualize if called. Checks if square is closed to not repeat when mid node included.
        if visualize and not curr_square.is_closed():
            draw(graph, display_update=False)
            draw_vis_text(is_a_star=True)

        # Sets square to closed after finished checking
        if curr_square != start and curr_square != ignore_node:
            curr_square.set_closed()

    return False


def heuristic(pos1, pos2):
    """Used by A* to prioritize traveling towards next node"""

    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def bi_dijkstra(graph, start, end, alt_color=False, ignore_node=None, draw_best_path=True, visualize=True):
    """Code for Bi-directional Dijkstra algorithm. Custom algorithm made by me."""

    # Used to determine the order of squares to check. Order of args helper decide the priority.
    queue_pos = 0
    open_set = PriorityQueue()
    open_set_hash = {start, end}
    open_set.put((0, queue_pos, start, 'start'))
    queue_pos += 1
    open_set.put((0, queue_pos, end, 'end'))

    # Determine what is the best square to check
    g_score = {square: float('inf') for row in graph for square in row}
    g_score[start] = 0
    g_score[end] = 0

    # Keeps track of next node for every node in graph. A linked list basically.
    came_from_start = {}
    came_from_end = {}

    # Continues until every node has been checked or best path found
    while not open_set.empty():

        # If uses closes window the program terminates
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Gets the square currently being checked
        temp = open_set.get()
        curr_square = temp[2]
        open_set_hash.remove(curr_square)

        # Terminates if found the best path
        for nei in curr_square.neighbours:
            if curr_square.is_open() and nei.is_open_alt():
                if draw_best_path:
                    best_path_bi_dijkstra(graph, came_from_start, came_from_end,
                                          curr_square, nei, visualize=visualize)
                    return True

                return came_from_start, came_from_end, curr_square, nei

            elif curr_square.is_open_alt() and nei.is_open() and not alt_color:
                if draw_best_path:
                    best_path_bi_dijkstra(graph, came_from_start, came_from_end,
                                          nei, curr_square, visualize=visualize)
                    return True

                return came_from_start, came_from_end, nei, curr_square

            elif curr_square.is_open_alt() and nei.is_open_alt_():
                if draw_best_path:
                    best_path_bi_dijkstra(graph, came_from_start, came_from_end,
                                          curr_square, nei, visualize=visualize)
                    return True

                return came_from_start, came_from_end, curr_square, nei

            elif curr_square.is_open_alt_() and nei.is_open_alt():
                if draw_best_path:
                    best_path_bi_dijkstra(graph, came_from_start, came_from_end,
                                          nei, curr_square, visualize=visualize)
                    return True

                return came_from_start, came_from_end, nei, curr_square

        # Decides the order of neighbours to check for both swarms.
        if temp[3] == 'start':
            for nei in curr_square.neighbours:
                temp_g_score = g_score[curr_square] + 1

                if temp_g_score < g_score[nei]:
                    came_from_start[nei] = curr_square
                    g_score[nei] = temp_g_score
                    if nei not in open_set_hash:
                        queue_pos += 1
                        open_set.put((g_score[nei], queue_pos, nei, 'start'))
                        open_set_hash.add(nei)
                        if nei != end and nei.color != CLOSED_COLOR and nei != ignore_node:
                            if alt_color:
                                nei.set_open_alt()
                            else:
                                nei.set_open()
        elif temp[3] == 'end':
            for nei in curr_square.neighbours:
                temp_g_score = g_score[curr_square] + 1

                if temp_g_score < g_score[nei]:
                    came_from_end[nei] = curr_square
                    g_score[nei] = temp_g_score
                    if nei not in open_set_hash:
                        queue_pos += 1
                        open_set.put((g_score[nei], queue_pos, nei, 'end'))
                        open_set_hash.add(nei)
                        if nei != start and nei.color != CLOSED_COLOR and nei != ignore_node:
                            if alt_color:
                                nei.set_open_alt_()
                            else:
                                nei.set_open_alt()

        # Only visualize if called. Checks if square is closed to not repeat when mid node included.
        if visualize and not curr_square.is_closed():
            draw(graph, display_update=False)
            draw_vis_text(is_bi_dijkstra=True)

        # Sets square to closed after finished checking
        if curr_square != start and curr_square != end and curr_square != ignore_node:
            curr_square.set_closed()

    return False


def best_path_bi_dijkstra(graph, came_from_start, came_from_end,
                          first_meet_node, second_meet_node, visualize=True):
    """Used by bi_dijkstra to draw best path from in two parts"""

    # Fixes bug when can't find a path
    if isinstance(came_from_start, bool) or isinstance(came_from_end, bool):
        return

    # Draws best path for first swarm
    best_path(graph, came_from_start, first_meet_node, visualize=visualize)
    # To not skip the last two at once, need a draw, draw_vis_text, and sleep here
    first_meet_node.set_path()
    # To not skip the last two at once, need a draw, draw_vis_text, and sleep here

    # Draws best path for second swarm
    second_meet_node.set_path()
    # To not skip the last two at once, need a draw and draw_vis_text here
    best_path(graph, came_from_end, second_meet_node, reverse=True, visualize=visualize)
    # To not skip the last two at once, need a draw, draw_vis_text, and sleep here


def best_path(graph, came_from, curr_square, reverse=False, visualize=True):
    """Main algo for reconstructing path"""

    # Fixes bug when dragging where came_from would evaluate to bool instead of dict.
    if isinstance(came_from, bool):
        return

    # Puts node path into list so it's easier to traverse in either direction and choose start and end points
    path = []
    while curr_square in came_from:
        curr_square = came_from[curr_square]
        path.append(curr_square)

    # Need to traverse in reverse depending on what part of algo
    if reverse:
        for square in path[:-1]:
            square.set_path()
            if visualize:
                pygame.time.delay(BEST_PATH_SLEEP)
                draw(graph, display_update=False)
                draw_vis_text(is_best_path=True)
    else:
        for square in path[len(path)-2::-1]:
            square.set_path()
            if visualize:
                pygame.time.delay(BEST_PATH_SLEEP)
                draw(graph, display_update=False)
                draw_vis_text(is_best_path=True)


def start_mid_end(graph, start, mid, end, is_dijkstra=False, is_a_star=False, is_bi_dijkstra=False, visualize=True):
    """Used if algos need to reach mid node first"""

    # Selects the correct algo to use
    if is_dijkstra:
        if visualize:
            start_to_mid = dijkstra(graph, start, mid, ignore_node=end, draw_best_path=False)
            mid_to_end = dijkstra(graph, mid, end, ignore_node=start, draw_best_path=False)
        else:
            start_to_mid = algo_no_vis(graph, start, mid, is_dijkstra=True, ignore_node=end, draw_best_path=False)
            mid_to_end = algo_no_vis(graph, mid, end, is_dijkstra=True, ignore_node=start,
                                     draw_best_path=False, reset=False)
            start.set_start(), mid.set_mid(), end.set_end()  # Fixes nodes disappearing when dragging

        best_path(graph, start_to_mid, mid, visualize=visualize)
        best_path(graph, mid_to_end, end, visualize=visualize)
    elif is_a_star:
        if visualize:
            start_to_mid = a_star(graph, start, mid, ignore_node=end, draw_best_path=False)
            mid_to_end = a_star(graph, mid, end, ignore_node=start, draw_best_path=False)
        else:
            start_to_mid = algo_no_vis(graph, start, mid, is_a_star=True, ignore_node=end, draw_best_path=False)
            mid_to_end = algo_no_vis(graph, mid, end, is_a_star=True, ignore_node=start,
                                     draw_best_path=False, reset=False)
            start.set_start(), mid.set_mid(), end.set_end()  # Fixes nodes disappearing when dragging

        best_path(graph, start_to_mid, mid, visualize=visualize)
        best_path(graph, mid_to_end, end, visualize=visualize)
    elif is_bi_dijkstra:
        if visualize:
            start_to_mid = bi_dijkstra(graph, start, mid, ignore_node=end, draw_best_path=False)
            mid_to_end = bi_dijkstra(graph, mid, end, alt_color=True, ignore_node=start, draw_best_path=False)
        else:
            start_to_mid = algo_no_vis(graph, start, mid, is_bi_dijkstra=True, ignore_node=end, draw_best_path=False)
            mid_to_end = algo_no_vis(graph, mid, end, alt_color=True, is_bi_dijkstra=True, ignore_node=start,
                                     draw_best_path=False, reset=False)
            start.set_start(), mid.set_mid(), end.set_end()  # Fixes nodes disappearing when dragging

        # Fixes bug when can't find a path
        if not isinstance(start_to_mid, bool):
            best_path_bi_dijkstra(graph, start_to_mid[0], start_to_mid[1],
                                  start_to_mid[2], start_to_mid[3], visualize=visualize)
        if not isinstance(mid_to_end, bool):
            best_path_bi_dijkstra(graph, mid_to_end[0], mid_to_end[1],
                                  mid_to_end[2], mid_to_end[3], visualize=visualize)


def algo_no_vis(graph, start, end, is_dijkstra=False, is_a_star=False, is_bi_dijkstra=False, alt_color=False,
                ignore_node=None, draw_best_path=True, reset=True):
    """Skip steps to end when visualizing algo. Used when dragging ordinal node once finished"""

    global dijkstra_finished, a_star_finished, bi_dijkstra_finished

    # Selects the correct algo to use
    if is_dijkstra:
        if reset:   # Used to not reset start -> mid visualizations if going from mid -> end
            reset_algo(graph)
        dijkstra_finished = True

        # Separates calling algo_no_vis with mid node or not
        if draw_best_path:
            dijkstra(graph, start, end, visualize=False)
            start.set_start()  # Fixes start disappearing when dragging
        else:
            return dijkstra(graph, start, end, ignore_node=ignore_node, draw_best_path=False, visualize=False)
    elif is_a_star:
        if reset:   # Used to not reset start -> mid visualizations if going from mid -> end
            reset_algo(graph)
        a_star_finished = True

        # Separates calling algo_no_vis with mid node or not
        if draw_best_path:
            a_star(graph, start, end, visualize=False)
            start.set_start()  # Fixes start disappearing when dragging
        else:
            return a_star(graph, start, end, ignore_node=ignore_node, draw_best_path=False, visualize=False)
    elif is_bi_dijkstra:
        if reset:   # Used to not reset start -> mid visualizations if going from mid -> end
            reset_algo(graph)
        bi_dijkstra_finished = True

        # Separates calling algo_no_vis with mid node or not
        if draw_best_path:
            bi_dijkstra(graph, start, end, alt_color=alt_color, visualize=False)
            start.set_start()  # Fixes start disappearing when dragging
        else:
            return bi_dijkstra(graph, start, end, alt_color=alt_color, ignore_node=ignore_node,
                               draw_best_path=False, visualize=False)


def draw_recursive_maze(graph, chamber=None, visualize=True):
    """Creates maze using recursive division.
    Implemented following wikipedia guidelines.
    https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_division_method
    Inspired by https://github.com/ChrisKneller/pygame-pathfinder
    """

    # Sets min size for division
    division_limit = 3

    # Creates chambers to divide into
    if chamber is None:
        chamber_width = len(graph)
        chamber_height = len(graph[1])
        chamber_left = 0
        chamber_top = 0
    else:
        chamber_width = chamber[2]
        chamber_height = chamber[3]
        chamber_left = chamber[0]
        chamber_top = chamber[1]

    # Helps with location of chambers
    x_divide = int(chamber_width/2)
    y_divide = int(chamber_height/2)

    # Draws vertical maze line within chamber
    if chamber_width >= division_limit:
        for y in range(chamber_height):
            graph[chamber_left + x_divide][chamber_top + y].set_wall()
            wall_nodes.add(graph[chamber_left + x_divide][chamber_top + y])
            if visualize:
                draw(graph, display_update=False)
                draw_vis_text(is_recursive_maze=True)

    # Draws horizontal maze line within chamber
    if chamber_height >= division_limit:
        for x in range(chamber_width):
            graph[chamber_left + x][chamber_top + y_divide].set_wall()
            wall_nodes.add(graph[chamber_left + x][chamber_top + y_divide])
            if visualize:
                draw(graph, display_update=False)
                draw_vis_text(is_recursive_maze=True)

    # Terminates if below division limit
    if chamber_width < division_limit and chamber_height < division_limit:
        return

    # Defining limits on where to draw walls
    top_left = (chamber_left, chamber_top, x_divide, y_divide)
    top_right = (chamber_left + x_divide+1, chamber_top, chamber_width - x_divide-1, y_divide)
    bottom_left = (chamber_left, chamber_top + y_divide+1, x_divide, chamber_height - y_divide-1)
    bottom_right = (chamber_left + x_divide+1, chamber_top + y_divide+1,
                    chamber_width - x_divide-1, chamber_height - y_divide-1)

    # Combines all chambers into one object
    chambers = (top_left, top_right, bottom_left, bottom_right)

    # Defines location of the walls
    left = (chamber_left, chamber_top + y_divide, x_divide, 1)
    right = (chamber_left + x_divide+1, chamber_top + y_divide, chamber_width - x_divide-1, 1)
    top = (chamber_left + x_divide, chamber_top, 1, y_divide)
    bottom = (chamber_left + x_divide, chamber_top + y_divide+1, 1, chamber_height - y_divide-1)

    # Combines walls into one object
    walls = (left, right, top, bottom)

    # Number of gaps to leave in walls after each division into four sub quadrants.
    num_gaps = 3

    # Prevents drawing wall over gaps
    gaps_to_offset = [x for x in range(num_gaps - 1, rows, num_gaps)]

    # Draws the gaps into the walls
    for wall in get_random_sample(walls, num_gaps):
        if wall[3] == 1:
            x = get_randrange(wall[0], wall[0] + wall[2])
            y = wall[1]
            if x in gaps_to_offset and y in gaps_to_offset:
                if wall[2] == x_divide:
                    x -= 1
                else:
                    x += 1
            if x >= rows:
                x = rows - 1
        else:
            x = wall[0]
            y = get_randrange(wall[1], wall[1] + wall[3])
            if y in gaps_to_offset and x in gaps_to_offset:
                if wall[3] == y_divide:
                    y -= 1
                else:
                    y += 1
            if y >= rows:
                y = rows - 1
        graph[x][y].reset()
        wall_nodes.discard(graph[x][y])
        if visualize:
            draw(graph, display_update=False)
            draw_vis_text(is_recursive_maze=True)

    # Recursively divides chambers
    for chamber in chambers:
        if visualize:
            draw_recursive_maze(graph, chamber)
        else:
            draw_recursive_maze(graph, chamber, visualize=False)
