"""Contains pathfinding and maze generation algorithms"""


from src.pathfinding.colors import *
from dataclasses import dataclass
import pygame
from src.pathfinding.graph import draw, draw_vis_text, reset_algo, GraphState, VisText
from src.pathfinding.values import get_random_sample, get_randrange
from queue import PriorityQueue
from src.pathfinding.node import Square
from time import perf_counter
from typing import Union
from lib.timer import timer_start, timer_end, timer_print
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


@dataclass
class AlgoState:
    """Stores the state of the algorithms, whether they are finished or not"""

    ordinal_node_clicked: list
    dijkstra_finished: bool = False
    a_star_finished: bool = False
    bi_dijkstra_finished: bool = False
    maze: bool = False
    best_path_sleep: int = 3
    highway_multiplier: int = 3

    # Timer for algorithm
    timer_total: float = 0
    timer_avg: float = None
    timer_max: float = float("-inf")
    timer_min: float = float("inf")
    timer_count: int = 0
    timer_start_time: float = None

    def timer_start(self) -> None:
        """Start timer for algo"""
        self.timer_start_time = perf_counter()

    def timer_end(self, count=True) -> None:
        """End timer for algo"""
        end = perf_counter()
        total = end - self.timer_start_time
        self.timer_total += total
        if count:
            self.timer_count += 1
        if self.timer_count:
            self.timer_avg = self.timer_total / self.timer_count
        self.timer_max = max(self.timer_min, total)
        if total > 0:  # 0 min values are trivial
            self.timer_min = min(self.timer_min, total)

    def timer_to_string(self) -> str:
        """Get string of current state of timer"""
        s = f"Time: {self.timer_total:.3f}s - # Nodes: {self.timer_count:,}"
        return s

    def timer_reset(self) -> None:
        """Resets timer"""
        self.timer_total: float = 0
        self.timer_avg: float = None
        self.timer_max: float = float("-inf")
        self.timer_min: float = float("inf")
        self.timer_count: int = 0
        self.timer_start_time: float = None


def dijkstra(
    gph: GraphState,
    algo: AlgoState,
    txt: VisText,
    start: Square,
    end: Square,
    ignore_node: Square = None,
    draw_best_path: bool = True,
    visualize: bool = True,
) -> Union[dict, bool]:

    """Code for the dijkstra algorithm"""

    # Clear previous and start timer here to include setup of algo into timer
    algo.timer_reset()
    algo.timer_start()

    # Used to determine the order of squares to check. Order of args helper decide the priority.
    queue_pos: int = 0
    open_set = PriorityQueue()
    open_set.put((0, queue_pos, start))

    # Determine what is the best square to check
    g_score: dict = {square: float("inf") for row in gph.graph for square in row}
    g_score[start] = 0

    # Keeps track of next node for every node in graph. A linked list basically.
    came_from: dict = {}

    # End timer here to start it again in loop
    algo.timer_end(count=False)

    # Continues until every node has been checked or best path found
    i = 0
    while not open_set.empty():

        # Time increments for each node being checked
        algo.timer_start()

        # If uses closes window the program terminates
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys

                sys.exit()

        # Gets the square currently being checked
        curr_square: Square = open_set.get()[2]

        # Terminates if found the best path
        if curr_square == end:
            if draw_best_path:
                best_path(gph, algo, txt, came_from, end, visualize=visualize)
                return True

            return came_from

        # Decides the order of neighbours to check
        nei: Square
        for nei in curr_square.get_neighbours():
            temp_g_score: int = g_score[curr_square] + 1

            if temp_g_score < g_score[nei]:
                came_from[nei] = curr_square
                g_score[nei] = temp_g_score
                queue_pos += 1
                open_set.put((g_score[nei], queue_pos, nei))
                if nei != end and not nei.is_closed() and nei != ignore_node:
                    nei.set_open()

        # Sets square to closed after finished checking
        already_closed = curr_square.is_closed()
        if curr_square != start and curr_square != ignore_node:
            curr_square.set_closed()

        # End timer before visualizing for better comparisons
        algo.timer_end()
        txt.algo_timer = algo.timer_to_string()

        # Only visualize if called. Checks if square is closed to not repeat when mid node included.
        if visualize and not already_closed:
            i += 1
            if i % gph.algo_speed_multiplier == 0:
                i = 0
                draw(gph, txt, algo_running=True)
                draw_vis_text(txt, is_dijkstra=True)

    return False


def a_star(
    gph: GraphState,
    algo: AlgoState,
    txt: VisText,
    start: Square,
    end: Square,
    ignore_node: Square = None,
    draw_best_path: bool = True,
    visualize: bool = True,
) -> Union[dict, bool]:

    """Code for the A* algorithm"""

    # Clear previous and start timer here to include setup of algo into timer
    algo.timer_reset()
    algo.timer_start()

    # Used to determine the order of squares to check. Order of args helper decide the priority.
    queue_pos: int = 0
    open_set = PriorityQueue()
    open_set.put((0, queue_pos, start))

    # Determine what is the best square to check
    g_score: dict = {square: float("inf") for row in gph.graph for square in row}
    g_score[start] = 0
    f_score: dict = {square: float("inf") for row in gph.graph for square in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    # Keeps track of next node for every node in graph. A linked list basically.
    came_from: dict = {}

    # End timer here to start it again in loop
    algo.timer_end(count=False)

    # Continues until every node has been checked or best path found
    i = 0  # Used to speed up graph if using map
    while not open_set.empty():

        # Time increments for each node being checked
        algo.timer_start()

        # If uses closes window the program terminates
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys

                sys.exit()

        # Gets the square currently being checked
        curr_square: Square = open_set.get()[2]

        # Terminates if found the best path
        if curr_square == end:
            if draw_best_path:
                best_path(gph, algo, txt, came_from, end, visualize=visualize)
                return True

            return came_from

        # Decides the order of neighbours to check
        nei: Square
        for nei in curr_square.get_neighbours():
            temp_g_score: int = g_score[curr_square] + 1

            if temp_g_score < g_score[nei]:
                came_from[nei] = curr_square
                g_score[nei] = temp_g_score
                f_score[nei] = temp_g_score + heuristic(nei.get_pos(), end.get_pos())
                queue_pos += 1
                open_set.put((f_score[nei], queue_pos, nei))
                if nei != end and not nei.is_closed() and nei != ignore_node:
                    nei.set_open()

        # Sets square to closed after finished checking
        already_closed = curr_square.is_closed()
        if curr_square != start and curr_square != ignore_node:
            curr_square.set_closed()

        # End timer before visualizing for better comparisons
        algo.timer_end()
        txt.algo_timer = algo.timer_to_string()

        # Only visualize if called. Checks if square is closed to not repeat when mid node included.
        if visualize and not already_closed:
            i += 1
            if i % gph.algo_speed_multiplier == 0:
                i = 0
                draw(gph, txt, algo_running=True)
                draw_vis_text(txt, is_a_star=True)

    return False


def heuristic(pos1: tuple, pos2: tuple) -> int:
    """Used by A* to prioritize traveling towards next node"""

    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def bi_dijkstra(
    gph: GraphState,
    algo: AlgoState,
    txt: VisText,
    start: Square,
    end: Square,
    alt_color: bool = False,
    ignore_node: Square = None,
    draw_best_path: bool = True,
    visualize: bool = True,
) -> Union[dict, bool]:

    """Code for Bi-directional Dijkstra algorithm. Custom algorithm made by me."""

    # Clear previous and start timer here to include setup of algo into timer
    algo.timer_reset()
    algo.timer_start()

    # Used to determine the order of squares to check. Order of args helper decide the priority.
    queue_pos: int = 0
    open_set = PriorityQueue()
    open_set.put((0, queue_pos, start, "start"))
    queue_pos += 1
    open_set.put((0, queue_pos, end, "end"))

    # Determine what is the best square to check
    g_score: dict = {square: float("inf") for row in gph.graph for square in row}
    g_score[start] = 0
    g_score[end] = 0

    # Keeps track of next node for every node in graph. A linked list basically.
    came_from_start: dict = {}
    came_from_end: dict = {}

    # End timer here to start it again in loop
    algo.timer_end(count=False)

    # Continues until every node has been checked or best path found
    i = 0
    while not open_set.empty():

        # Time increments for each node being checked
        algo.timer_start()

        # If uses closes window the program terminates
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys

                sys.exit()

        # Gets the square currently being checked
        temp: tuple = open_set.get()
        curr_square: Square = temp[2]

        # Terminates if found the best path
        nei: Square
        for nei in curr_square.get_neighbours():
            # Start swarm reaching mid (end node if no mid) swarm
            if curr_square.is_open() and nei.is_open_alt():
                if draw_best_path:
                    best_path_bi_dijkstra(
                        gph,
                        algo,
                        txt,
                        came_from_start,
                        came_from_end,
                        curr_square,
                        nei,
                        visualize=visualize,
                    )
                    return True

                return came_from_start, came_from_end, curr_square, nei

            # Mid (end if no mid) swarm reaching start swarm
            elif curr_square.is_open_alt() and nei.is_open() and not alt_color:
                if draw_best_path:
                    best_path_bi_dijkstra(
                        gph,
                        algo,
                        txt,
                        came_from_start,
                        came_from_end,
                        nei,
                        curr_square,
                        visualize=visualize,
                    )
                    return True

                return came_from_start, came_from_end, nei, curr_square

            # Mid swarm reaching end swarm
            elif curr_square.is_open_alt() and nei.is_open_alt_():
                if draw_best_path:
                    best_path_bi_dijkstra(
                        gph,
                        algo,
                        txt,
                        came_from_start,
                        came_from_end,
                        curr_square,
                        nei,
                        visualize=visualize,
                    )
                    return True

                return came_from_start, came_from_end, curr_square, nei

            # End swarm reaching mid swarm
            elif curr_square.is_open_alt_() and nei.is_open_alt():
                if draw_best_path:
                    best_path_bi_dijkstra(
                        gph,
                        algo,
                        txt,
                        came_from_start,
                        came_from_end,
                        nei,
                        curr_square,
                        visualize=visualize,
                    )
                    return True

                return came_from_start, came_from_end, nei, curr_square

        # Decides the order of neighbours to check for both swarms.
        temp_g_score: int
        if temp[3] == "start":
            for nei in curr_square.get_neighbours():
                temp_g_score = g_score[curr_square] + 1

                if temp_g_score < g_score[nei]:
                    came_from_start[nei] = curr_square
                    g_score[nei] = temp_g_score
                    queue_pos += 1
                    open_set.put((g_score[nei], queue_pos, nei, "start"))
                    if nei != end and not nei.is_closed() and nei != ignore_node:
                        if alt_color:
                            nei.set_open_alt()
                        else:
                            nei.set_open()
        elif temp[3] == "end":
            for nei in curr_square.get_neighbours():
                temp_g_score = g_score[curr_square] + 1

                if temp_g_score < g_score[nei]:
                    came_from_end[nei] = curr_square
                    g_score[nei] = temp_g_score
                    queue_pos += 1
                    open_set.put((g_score[nei], queue_pos, nei, "end"))
                    if nei != start and not nei.is_closed() and nei != ignore_node:
                        if alt_color:
                            nei.set_open_alt_()
                        else:
                            nei.set_open_alt()

        # Sets square to closed after finished checking
        already_closed = any(
            (
                curr_square.is_closed(),
                curr_square.is_closed_alt(),
                curr_square.is_closed_alt_(),
            )
        )
        if curr_square != start and curr_square != end and curr_square != ignore_node:
            # Set square to proper closed value based on it's open value
            if curr_square.is_open():
                curr_square.set_closed()
            elif curr_square.is_open_alt():
                curr_square.set_closed_alt()
            elif curr_square.is_open_alt_():
                curr_square.set_closed_alt_()

        # End timer before visualizing for better comparisons
        algo.timer_end()
        txt.algo_timer = algo.timer_to_string()

        # Only visualize if called. Checks if square is closed to not repeat when mid node included.
        if visualize and not already_closed:
            i += 1
            if i % gph.algo_speed_multiplier == 0:
                i = 0
                draw(gph, txt, algo_running=True)
                draw_vis_text(txt, is_bi_dijkstra=True)

    return False


def best_path_bi_dijkstra(
    gph: GraphState,
    algo: AlgoState,
    txt: VisText,
    came_from_start: dict,
    came_from_end: dict,
    first_meet_node: Square,
    second_meet_node: Square,
    visualize: bool = True,
) -> None:

    """Used by bi_dijkstra to draw best path from in two parts"""

    # Fixes bug when can't find a path
    if isinstance(came_from_start, bool) or isinstance(came_from_end, bool):
        return

    # Draws best path for first swarm
    best_path(gph, algo, txt, came_from_start, first_meet_node, visualize=visualize)
    # To not skip the last two at once, need a draw, draw_vis_text, and sleep here
    first_meet_node.set_path()
    # To not skip the last two at once, need a draw, draw_vis_text, and sleep here

    # Draws best path for second swarm
    second_meet_node.set_path()
    # To not skip the last two at once, need a draw and draw_vis_text here
    best_path(
        gph,
        algo,
        txt,
        came_from_end,
        second_meet_node,
        reverse=True,
        visualize=visualize,
    )
    # To not skip the last two at once, need a draw, draw_vis_text, and sleep here


def best_path(
    gph: GraphState,
    algo: AlgoState,
    txt: VisText,
    came_from: dict,
    curr_square: Square,
    reverse: bool = False,
    visualize: bool = True,
) -> None:

    """Main algo for reconstructing path"""

    # Fixes bug when dragging where came_from would evaluate to bool instead of dict.
    if isinstance(came_from, bool):
        return

    # Puts node path into list so it's easier to traverse in either direction and choose start and end points
    path: list = []
    while curr_square in came_from:
        curr_square = came_from[curr_square]
        path.append(curr_square)

    # Need to traverse in reverse depending on what part of algo
    i = 0
    square: Square
    if reverse:
        for square in path[:-1]:
            square.set_path()
            i += 1
            if visualize:
                if i % gph.path_speed_multiplier == 0:
                    i = 0
                    pygame.time.delay(algo.best_path_sleep)
                    draw(gph, txt, algo_running=True)
                    draw_vis_text(txt, is_best_path=True)
    else:
        for square in path[len(path) - 2 :: -1]:
            square.set_path()
            i += 1
            if visualize:
                if i % gph.path_speed_multiplier == 0:
                    i = 0
                    pygame.time.delay(algo.best_path_sleep)
                    draw(gph, txt, algo_running=True)
                    draw_vis_text(txt, is_best_path=True)
    gph.update_legend = True


def start_mid_end(
    gph: GraphState,
    algo: AlgoState,
    txt: VisText,
    start: Square,
    mid: Square,
    end: Square,
    is_dijkstra: bool = False,
    is_a_star: bool = False,
    is_bi_dijkstra: bool = False,
    visualize: bool = True,
) -> None:

    """Used if algos need to reach mid node first"""

    # Selects the correct algo to use
    if is_dijkstra:
        if visualize:
            start_to_mid = dijkstra(
                gph, algo, txt, start, mid, ignore_node=end, draw_best_path=False
            )
            mid_to_end = dijkstra(
                gph, algo, txt, mid, end, ignore_node=start, draw_best_path=False
            )
        else:
            start_to_mid = algo_no_vis(
                gph,
                algo,
                txt,
                start,
                mid,
                is_dijkstra=True,
                ignore_node=end,
                draw_best_path=False,
            )
            mid_to_end = algo_no_vis(
                gph,
                algo,
                txt,
                mid,
                end,
                is_dijkstra=True,
                ignore_node=start,
                draw_best_path=False,
                reset=False,
            )

            # Fixes nodes disappearing when dragging
            start.set_start()
            mid.set_mid()
            end.set_end()

        best_path(gph, algo, txt, start_to_mid, mid, visualize=visualize)
        best_path(gph, algo, txt, mid_to_end, end, visualize=visualize)
    elif is_a_star:
        if visualize:
            start_to_mid = a_star(
                gph, algo, txt, start, mid, ignore_node=end, draw_best_path=False
            )
            mid_to_end = a_star(
                gph, algo, txt, mid, end, ignore_node=start, draw_best_path=False
            )
        else:
            start_to_mid = algo_no_vis(
                gph,
                algo,
                txt,
                start,
                mid,
                is_a_star=True,
                ignore_node=end,
                draw_best_path=False,
            )
            mid_to_end = algo_no_vis(
                gph,
                algo,
                txt,
                mid,
                end,
                is_a_star=True,
                ignore_node=start,
                draw_best_path=False,
                reset=False,
            )

            # Fixes nodes disappearing when dragging
            start.set_start()
            mid.set_mid()
            end.set_end()

        best_path(gph, algo, txt, start_to_mid, mid, visualize=visualize)
        best_path(gph, algo, txt, mid_to_end, end, visualize=visualize)
    elif is_bi_dijkstra:
        if visualize:
            start_to_mid = bi_dijkstra(
                gph, algo, txt, start, mid, ignore_node=end, draw_best_path=False
            )
            mid_to_end = bi_dijkstra(
                gph,
                algo,
                txt,
                mid,
                end,
                alt_color=True,
                ignore_node=start,
                draw_best_path=False,
            )
        else:
            start_to_mid = algo_no_vis(
                gph,
                algo,
                txt,
                start,
                mid,
                is_bi_dijkstra=True,
                ignore_node=end,
                draw_best_path=False,
            )
            mid_to_end = algo_no_vis(
                gph,
                algo,
                txt,
                mid,
                end,
                alt_color=True,
                is_bi_dijkstra=True,
                ignore_node=start,
                draw_best_path=False,
                reset=False,
            )

            # Fixes nodes disappearing when dragging
            start.set_start()
            mid.set_mid()
            end.set_end()

        # Fixes bug when can't find a path
        if not isinstance(start_to_mid, bool):
            best_path_bi_dijkstra(
                gph,
                algo,
                txt,
                start_to_mid[0],
                start_to_mid[1],
                start_to_mid[2],
                start_to_mid[3],
                visualize=visualize,
            )
        if not isinstance(mid_to_end, bool):
            best_path_bi_dijkstra(
                gph,
                algo,
                txt,
                mid_to_end[0],
                mid_to_end[1],
                mid_to_end[2],
                mid_to_end[3],
                visualize=visualize,
            )


def algo_no_vis(
    gph: GraphState,
    algo: AlgoState,
    txt: VisText,
    start: Square,
    end: Square,
    is_dijkstra: bool = False,
    is_a_star: bool = False,
    is_bi_dijkstra: bool = False,
    alt_color: bool = False,
    ignore_node: Square = None,
    draw_best_path: bool = True,
    reset: bool = True,
) -> Union[dict, bool]:

    """Skip steps to end when visualizing algo. Used when dragging ordinal node once finished"""

    # Selects the correct algo to use
    if is_dijkstra:
        # Used to not reset start -> mid visualizations if going from mid -> end
        if reset:
            reset_algo(algo)
        algo.dijkstra_finished = True

        # Separates calling algo_no_vis with mid node or not
        if draw_best_path:
            dijkstra(gph, algo, txt, start, end, visualize=False)

            # Fixes start disappearing when dragging
            start.set_start()
            end.set_end()
        else:
            return dijkstra(
                gph,
                algo,
                txt,
                start,
                end,
                ignore_node=ignore_node,
                draw_best_path=False,
                visualize=False,
            )
    elif is_a_star:
        # Used to not reset start -> mid visualizations if going from mid -> end
        if reset:
            reset_algo(algo)
        algo.a_star_finished = True

        # Separates calling algo_no_vis with mid node or not
        if draw_best_path:
            a_star(gph, algo, txt, start, end, visualize=False)

            # Fixes start disappearing when dragging
            start.set_start()
            end.set_end()
        else:
            return a_star(
                gph,
                algo,
                txt,
                start,
                end,
                ignore_node=ignore_node,
                draw_best_path=False,
                visualize=False,
            )
    elif is_bi_dijkstra:
        # Used to not reset start -> mid visualizations if going from mid -> end
        if reset:
            reset_algo(algo)
        algo.bi_dijkstra_finished = True

        # Separates calling algo_no_vis with mid node or not
        if draw_best_path:
            bi_dijkstra(
                gph, algo, txt, start, end, alt_color=alt_color, visualize=False
            )

            # Fixes start disappearing when dragging
            start.set_start()
            end.set_end()
        else:
            return bi_dijkstra(
                gph,
                algo,
                txt,
                start,
                end,
                alt_color=alt_color,
                ignore_node=ignore_node,
                draw_best_path=False,
                visualize=False,
            )


def draw_recursive_maze(
    gph: GraphState,
    algo: AlgoState,
    txt: VisText,
    chamber: tuple = None,
    visualize: bool = True,
) -> None:

    """Creates maze using recursive division.
    Implemented following wikipedia guidelines.
    https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_division_method
    Inspired by https://github.com/ChrisKneller/pygame-pathfinder
    """

    # Only reset timer on first call
    if not chamber:
        algo.timer_reset()
    # Start timer here to include setup in timer
    algo.timer_start()

    # Sets min size for division
    division_limit: int = 3

    # Creates chambers to divide into
    if chamber is None:
        chamber_width: int = len(gph.graph)
        chamber_height: int = len(gph.graph[1])
        chamber_left: int = 0
        chamber_top: int = 0
    else:
        chamber_width: int = chamber[2]
        chamber_height: int = chamber[3]
        chamber_left: int = chamber[0]
        chamber_top: int = chamber[1]

    # Helps with location of chambers
    x_divide = int(chamber_width / 2)
    y_divide = int(chamber_height / 2)

    # End timer here to resume in loop
    algo.timer_end(count=False)

    # Draws vertical maze line within chamber
    if chamber_width >= division_limit:
        for y in range(chamber_height):
            algo.timer_start()
            square: Square = gph.graph[chamber_left + x_divide][chamber_top + y]
            square.set_wall()
            algo.timer_end()
            txt.algo_timer = algo.timer_to_string()
            if visualize:
                draw(gph, txt, algo_running=True)
                draw_vis_text(txt, is_recursive_maze=True)

    # Draws horizontal maze line within chamber
    if chamber_height >= division_limit:
        for x in range(chamber_width):
            algo.timer_start()
            square: Square = gph.graph[chamber_left + x][chamber_top + y_divide]
            square.set_wall()
            algo.timer_end()
            txt.algo_timer = algo.timer_to_string()
            if visualize:
                draw(gph, txt, algo_running=True)
                draw_vis_text(txt, is_recursive_maze=True)

    # Terminates if below division limit
    if chamber_width < division_limit and chamber_height < division_limit:
        return

    algo.timer_start()

    # Defining limits on where to draw walls
    top_left: tuple = (chamber_left, chamber_top, x_divide, y_divide)
    top_right: tuple = (
        chamber_left + x_divide + 1,
        chamber_top,
        chamber_width - x_divide - 1,
        y_divide,
    )
    bottom_left: tuple = (
        chamber_left,
        chamber_top + y_divide + 1,
        x_divide,
        chamber_height - y_divide - 1,
    )
    bottom_right: tuple = (
        chamber_left + x_divide + 1,
        chamber_top + y_divide + 1,
        chamber_width - x_divide - 1,
        chamber_height - y_divide - 1,
    )

    # Combines all chambers into one object
    chambers: tuple = (top_left, top_right, bottom_left, bottom_right)

    # Defines location of the walls
    left: tuple = (chamber_left, chamber_top + y_divide, x_divide, 1)
    right: tuple = (
        chamber_left + x_divide + 1,
        chamber_top + y_divide,
        chamber_width - x_divide - 1,
        1,
    )
    top: tuple = (chamber_left + x_divide, chamber_top, 1, y_divide)
    bottom: tuple = (
        chamber_left + x_divide,
        chamber_top + y_divide + 1,
        1,
        chamber_height - y_divide - 1,
    )

    # Combines walls into one object
    walls: tuple = (left, right, top, bottom)

    # Number of gaps to leave in walls after each division into four sub quadrants.
    num_gaps: int = 3

    # Prevents drawing wall over gaps
    gaps_to_offset: list = [x for x in range(num_gaps - 1, gph.rows, num_gaps)]

    # End timer here to resume in loop
    algo.timer_end(count=False)

    # Draws the gaps into the walls
    for wall in get_random_sample(walls, num_gaps):

        # Continue timer here
        algo.timer_start()

        if wall[3] == 1:
            x = get_randrange(wall[0], wall[0] + wall[2])
            y = wall[1]
            if x in gaps_to_offset and y in gaps_to_offset:
                if wall[2] == x_divide:
                    x -= 1
                else:
                    x += 1
            if x >= gph.rows:
                x = gph.rows - 1
        else:
            x = wall[0]
            y = get_randrange(wall[1], wall[1] + wall[3])
            if y in gaps_to_offset and x in gaps_to_offset:
                if wall[3] == y_divide:
                    y -= 1
                else:
                    y += 1
            if y >= gph.rows:
                y = gph.rows - 1
        square: Square = gph.graph[x][y]
        square.reset()

        # End timer before visualizing
        algo.timer_end()
        txt.algo_timer = algo.timer_to_string()

        if visualize:
            draw(gph, txt, algo_running=True)
            draw_vis_text(txt, is_recursive_maze=True)

    # Recursively divides chambers
    for chamber in chambers:
        draw_recursive_maze(gph, algo, txt, chamber, visualize=visualize)
