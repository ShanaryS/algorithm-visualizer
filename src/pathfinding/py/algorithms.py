"""Contains pathfinding and maze generation algorithms"""


# Handles how much C++ the the program should use
from src.pathfinding.cpp_or_py import use_square_h
if use_square_h:
    from src.pathfinding.cpp.modules import Square
else:
    from src.pathfinding.py.square import Square
from lib.timer import sleep

from threading import Lock
from dataclasses import dataclass, field
from queue import PriorityQueue
from time import perf_counter_ns
import random


@dataclass(slots=True)
class AlgoState:
    """Stores the state of the algorithms, whether they are finished or not"""
    # Possible phases
    PHASE_ALGO: int = field(init=False)
    PHASE_MAZE: int = field(init=False)
    
    # Possible algorithms
    ALGO_DIJKSTRA: int = field(init=False)
    ALGO_A_STAR: int = field(init=False)
    ALGO_BI_DIJKSTRA: int = field(init=False)
    ALGO_BEST_PATH: int = field(init=False)
    ALGO_RECURSIVE_MAZE: int = field(init=False)
    
    # The current phase and current/last algorithm.
    _phase: int = field(init=False)
    _algo: int = field(init=False)
    _finished: bool = False  # Cobination with ALGO preserves past
    
    # Special variables
    _unique_int: int = 0  # Starts +1 when called by self._next_int()
    NONE: int = _unique_int  # Value is 0 which returns false when casted to bool
    lock: Lock  = Lock()

    # Run options
    _start: Square = None
    _mid: Square = None
    _end: Square = None
    _ignore_square: Square = None
    
    # Control the speed of algorithms
    _DEFAULT_BEST_PATH_DELAY_MS: int = 3
    _best_path_delay_ms: int = field(init=False)
    _DEFAULT_RECURSIVE_MAZE_DELAY_US: int = 250
    _recursive_maze_delay_us: int = field(init=False)

    # Timer for algorithms
    timer_total: float = 0
    timer_avg: float = None
    timer_max: float = float("-inf")
    timer_min: float = float("inf")
    timer_count: int = 0
    _timer_start_time: float = None
    
    def __post_init__(self):
        """Initialize variables with their unique values."""
        self.PHASE_ALGO = self._generate_unique_int()
        self.PHASE_MAZE = self._generate_unique_int()
        self.ALGO_DIJKSTRA = self._generate_unique_int()
        self.ALGO_A_STAR = self._generate_unique_int()
        self.ALGO_BI_DIJKSTRA = self._generate_unique_int()
        self.ALGO_BEST_PATH = self._generate_unique_int()
        self.ALGO_RECURSIVE_MAZE = self._generate_unique_int()
        self.reset()

    def start_loop(self) -> None:
        """Starts the algo loop. Place on a daemon thread."""
        self._algo_loop()

    def run_options(self, start, mid, end, ignore_square) -> None:
        """Set the options that will be performed on run"""
        with self.lock:
            self._start = start
            self._mid = mid
            self._end = end
            self._ignore_square = ignore_square

    def run(self, phase, algo) -> None:
        """Start an algorithm using PHASE and ALGO, NULL where applicable."""
        self._set_phase(phase)
        self._set_algo(algo)
        self._set_finished(False)
    
    def check_phase(self) -> int:
        """Checks the phase"""
        with self.lock:
            return self._phase

    def check_algo(self) -> int:
        """Checks the algo"""
        with self.lock:
            return self._algo

    def check_finished(self) -> bool:
        """Checks if algo is finished"""
        with self.lock:
            return self._finished

    def reset(self) -> None:
        """Resets options to their default values"""
        with self.lock:
            self._phase = self.NONE
            self._algo = self.NONE
            self._start = None
            self._mid = None
            self._end = None
            self._ignore_square = None
            self._finished = False
            self._best_path_delay_ms = self._DEFAULT_BEST_PATH_DELAY_MS
            self._recursive_maze_delay_us = self._DEFAULT_RECURSIVE_MAZE_DELAY_US

    def set_best_path_delay(self, ms: int) -> None:
        """Change the delay for the next best path"""
        with self.lock:
            self._best_path_delay_ms = ms

    def set_recursive_maze_delay(self, us: int) -> None:
        """Change the delay for the next recursive maze"""
        with self.lock:
            self._recursive_maze_delay_us = us

    def _set_phase(self, phase: int) -> None:
        """Change the phase. Use PHASE constants."""
        with self.lock:
            self._phase = phase
    
    def _set_algo(self, algo: int) -> None:
        """Change the algo. Use ALGO constants."""
        with self.lock:
            self._algo = algo

    def _set_finished(self, x: bool) -> None:
        """Set finshed to true or false"""
        with self.lock:
            self._finished = x

    def _algo_loop(self) -> None:
        """This loop is placed on a daemon thread and watches for updates."""
        while True:
            # Check if algo
            if self.check_phase() == self.PHASE_ALGO and not self.check_finished():
                previous_algo = self.check_algo()
                if not self._mid:
                    if self.check_algo() == self.ALGO_DIJKSTRA:
                        dijkstra(self, self._start, self._end, self._ignore_square, draw_best_path=True)
                    elif self.check_algo() == self.ALGO_A_STAR:
                        a_star(self, self._start, self._end, self._ignore_square, draw_best_path=True)
                    elif self.check_algo() == self.ALGO_BI_DIJKSTRA:
                        bi_dijkstra(self, self._start, self._end, self._ignore_square, draw_best_path=True)
                else:
                    start_mid_end(self, self._start, self._mid, self._end)
                self.set_best_path_delay(self._DEFAULT_BEST_PATH_DELAY_MS)  # Set to 0 with no vis
                self._set_algo(previous_algo)  # Preserves more info
                self._set_finished(True)
                self._set_phase(self.NONE)

            # Check if maze
            elif self.check_phase() == self.PHASE_MAZE and not self.check_finished():
                if self.check_algo() == self.ALGO_RECURSIVE_MAZE:
                    recursive_maze(self)
                    self.set_recursive_maze_delay(self._DEFAULT_RECURSIVE_MAZE_DELAY_US)
                self._set_finished(True)
                self._set_phase(self.NONE)

    def _timer_start(self) -> None:
        """Start timer for algo. Not for general use."""
        self._timer_start_time = perf_counter_ns()

    def _timer_end(self, count=True) -> None:
        """End timer for algo. Not for general use."""
        end = perf_counter_ns()
        total = (end - self._timer_start_time) / 10**9  # Time in seconds
        self.timer_total += total
        if count:
            self.timer_count += 1
        if self.timer_count:
            self.timer_avg = self.timer_total / self.timer_count
        if total:  # Make it obvious for 0 max values
            self.timer_max = max(self.timer_max, total)
        if total:  # 0 min values are trivial
            self.timer_min = min(self.timer_min, total)

    def _timer_reset(self) -> None:
        """Resets timer. Not for general use."""
        self.timer_total: float = 0
        self.timer_avg: float = None
        self.timer_max: float = float("-inf")
        self.timer_min: float = float("inf")
        self.timer_count: int = 0
        self._timer_start_time: float = None
    
    def _generate_unique_int(self) -> int:
        """Assign unique int on every call"""
        self._unique_int += 1
        return self._unique_int

    def thread_lock(self) -> None:
        """For use in custom context manager for consistency with C++"""
        self.lock.acquire()

    def thread_unlock(self) -> None:
        """For use in custom context manager for consistency with C++"""
        self.lock.release()


def dijkstra(algo: AlgoState, start: Square, end: Square, ignore_square: Square, draw_best_path: bool) -> dict:
    """Code for the dijkstra algorithm"""
    # Clear previous and start timer here to include setup of algo into timer
    algo._timer_reset()
    algo._timer_start()

    # Used to determine the order of squares to check. Order of args helper decide the priority.
    open_set = PriorityQueue()
    queue_pos = 0
    open_set.put((0, queue_pos, start))

    # Determine what is the best square to check
    g_score = {Square.get_square(row, col): float("inf") for row in range(Square.get_num_rows()) for col in range(Square.get_num_cols())}
    g_score[start] = 0

    # Keeps track of next square for every square in graph. A linked list basically.
    came_from = {}

    # End timer here to start it again in loop
    algo._timer_end(count=False)

    # Continues until every square has been checked or best path found
    while not open_set.empty():

        # Time increments for each square being checked
        algo._timer_start()

        # Gets the square currently being checked
        curr_square: Square = open_set.get()[2]

        # Terminates if found the best path
        if curr_square == end:
            if draw_best_path:
                _best_path(algo, came_from, end)
            return came_from

        # Decides the order of neighbours to check
        nei: Square
        for nei in curr_square.get_neighbours():
            # Ignore walls
            if nei.is_wall():
                continue

            # Only check square if not already checked.
            temp_g_score = g_score[curr_square] + 1
            if temp_g_score < g_score[nei]:
                came_from[nei] = curr_square
                g_score[nei] = temp_g_score
                queue_pos += 1
                open_set.put((g_score[nei], queue_pos, nei))

                # Set nei to open under certain conditions
                if not nei.is_closed() and nei != end and nei != ignore_square:
                    with algo.lock:
                        nei.set_open()

        # Sets square to closed after finished checking
        if curr_square != start and curr_square != ignore_square:
            with algo.lock:
                curr_square.set_closed()

        # End timer to increment count
        algo._timer_end()
    
    return came_from


def a_star(algo: AlgoState, start: Square, end: Square, ignore_square: Square, draw_best_path: bool) -> dict:
    """Code for the A* algorithm"""
    # Clear previous and start timer here to include setup of algo into timer
    algo._timer_reset()
    algo._timer_start()

    # Used to determine the order of squares to check. Order of args helper decide the priority.
    open_set = PriorityQueue()
    queue_pos = 0
    open_set.put((0, queue_pos, start))

    # Determine what is the best square to check
    g_score = {Square.get_square(row, col): float("inf") for row in range(Square.get_num_rows()) for col in range(Square.get_num_cols())}
    g_score[start] = 0
    f_score = {Square.get_square(row, col): float("inf") for row in range(Square.get_num_rows()) for col in range(Square.get_num_cols())}
    f_score[start] = _heuristic(start.get_pos(), end.get_pos())

    # Keeps track of next square for every square in graph. A linked list basically.
    came_from = {}

    # End timer here to start it again in loop
    algo._timer_end(count=False)

    # Continues until every square has been checked or best path found
    while not open_set.empty():

        # Time increments for each square being checked
        algo._timer_start()

        # Gets the square currently being checked
        curr_square: Square = open_set.get()[2]

        # Terminates if found the best path
        if curr_square == end:
            if draw_best_path:
                _best_path(algo, came_from, end)
            return came_from

        # Decides the order of neighbours to check
        nei: Square
        for nei in curr_square.get_neighbours():
            # Ignore walls
            if nei.is_wall():
                continue

            # Only check square if not already checked.
            temp_g_score = g_score[curr_square] + 1
            if temp_g_score < g_score[nei]:
                came_from[nei] = curr_square
                g_score[nei] = temp_g_score
                f_score[nei] = temp_g_score + _heuristic(nei.get_pos(), end.get_pos())
                queue_pos += 1
                open_set.put((f_score[nei], queue_pos, nei))

                # Set nei to open under certain conditions
                if not nei.is_closed() and nei != end and nei != ignore_square:
                    with algo.lock:
                        nei.set_open()

        # Sets square to closed after finished checking
        if curr_square != start and curr_square != ignore_square:
            with algo.lock:
                curr_square.set_closed()

        # End timer to increment count
        algo._timer_end()

    return came_from


def _heuristic(pos1: tuple, pos2: tuple) -> int:
    """Used by A* to prioritize traveling towards next square"""
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def bi_dijkstra(algo: AlgoState, start: Square, end: Square, ignore_square: Square, draw_best_path: bool) -> dict | Square:
    """Code for Bi-directional Dijkstra algorithm. Custom algorithm made by me."""
    # Clear previous and start timer here to include setup of algo into timer
    algo._timer_reset()
    algo._timer_start()

    # Used to determine the order of squares to check. Order of args helper decide the priority.
    open_set = PriorityQueue()
    queue_pos = 0
    FIRST_SWARM = "FIRST_SWARM"
    open_set.put((0, queue_pos, start, FIRST_SWARM))
    queue_pos += 1
    SECOND_SWARM = "SECOND_SWARM"
    open_set.put((0, queue_pos, end, SECOND_SWARM))

    # Determine what is the best square to check
    g_score = {Square.get_square(row, col): float("inf") for row in range(Square.get_num_rows()) for col in range(Square.get_num_cols())}
    g_score[start] = 0
    g_score[end] = 0

    # Keeps track of next square for every square in graph. A linked list basically.
    came_from = {}

    # Track the last squares for each swarm
    first_swarm = set()
    second_swarm = set()
    first_swarm_meet_square: Square = None
    second_swarm_meet_square: Square = None

    # End timer here to start it again in loop
    algo._timer_end(count=False)

    # Continues until every square has been checked or best path found
    while not open_set.empty():

        # Terminates if the swarms meet each other
        if first_swarm_meet_square or second_swarm_meet_square:
            # Allow access the meet squares using the known start and end squares
            if draw_best_path:
                _best_path_bi_dijkstra(algo, came_from, first_swarm_meet_square, second_swarm_meet_square)
            return came_from, first_swarm_meet_square, second_swarm_meet_square

        # Time increments for each square being checked
        algo._timer_start()
        
        # Gets the square currently being checked.
        temp = open_set.get()
        curr_square: Square = temp[2]
        swarm = temp[3]

        # Decides the order of neighbours to check for both swarms.
        for nei in curr_square.get_neighbours():
            # Ignore walls
            if nei.is_wall():
                continue

            # Only check square if not already checked.
            temp_g_score = g_score[curr_square] + 1
            if temp_g_score < g_score[nei]:
                came_from[nei] = curr_square
                g_score[nei] = temp_g_score
                queue_pos += 1
                open_set.put((g_score[nei], queue_pos, nei, swarm))

                # Set nei to open under certain conditions
                if not nei.is_closed() and nei != ignore_square:
                    if swarm == FIRST_SWARM and nei != end:
                        first_swarm.add(nei)
                        with algo.lock:
                            nei.set_open()
                    elif swarm == SECOND_SWARM and nei != start:
                        second_swarm.add(nei)
                        with algo.lock:
                            nei.set_open()
            # Conditions for when path is found
            elif swarm == FIRST_SWARM and nei in second_swarm:
                first_swarm_meet_square = curr_square
                second_swarm_meet_square = nei
                break
            elif swarm == SECOND_SWARM and nei in first_swarm:
                first_swarm_meet_square = nei
                second_swarm_meet_square = curr_square
                break

        # Sets square to closed after finished checking
        if curr_square != start and curr_square != end and curr_square != ignore_square:
            with algo.lock:
                    curr_square.set_closed()

        # End timer to increment count
        algo._timer_end()
    
    return came_from, first_swarm_meet_square, second_swarm_meet_square


def _best_path_bi_dijkstra(algo: AlgoState, came_from: dict,
    first_swarm_meet_square: Square,second_swarm_meet_square: Square) -> None:
    """Used by bi_dijkstra to draw best path for both swarms"""
    _best_path(algo, came_from, first_swarm_meet_square)
    # Best path skips these two naturally so need to set them here.
    with algo.lock:
        first_swarm_meet_square.set_path()
        second_swarm_meet_square.set_path()
    _best_path(algo, came_from, second_swarm_meet_square, reverse=True)


def _best_path(algo: AlgoState, came_from: dict, curr_square: Square, reverse: bool = False) -> None:
    """Main algo for reconstructing path"""
    # Update info
    algo._set_algo(algo.ALGO_BEST_PATH)
    
    # Puts square path into list so it's easier to traverse in either direction and choose start and end points
    path: list = []
    while curr_square in came_from:
        curr_square = came_from[curr_square]
        path.append(curr_square)

    # Need to traverse in reverse depending on what part of algo
    square: Square
    if reverse:
        for square in path[:-1]:
            sleep(algo._best_path_delay_ms, unit="ms")
            with algo.lock:
                square.set_path()
    else:
        for square in path[len(path) - 2 :: -1]:
            sleep(algo._best_path_delay_ms, unit="ms")
            with algo.lock:
                square.set_path()


def start_mid_end(algo: AlgoState, start: Square, mid: Square, end: Square) -> None:
    """Used if algos need to reach mid square first"""
    # Selects the correct algo to use
    if algo.check_algo() == algo.ALGO_DIJKSTRA:
        start_to_mid = dijkstra(algo, start, mid, end, draw_best_path=False)
        mid_to_end = dijkstra(algo, mid, end, start, draw_best_path=False)
        
        # Fixes squares disappearing when dragging
        with algo.lock:
            start.set_start()
            mid.set_mid()
            end.set_end()
    
        _best_path(algo, start_to_mid, mid)
        _best_path(algo, mid_to_end, end)
    elif algo.check_algo() == algo.ALGO_A_STAR:
        start_to_mid = a_star(algo, start, mid, end, draw_best_path=False)
        mid_to_end = a_star(algo, mid, end, start, draw_best_path=False)

        # Fixes squares disappearing when dragging
        with algo.lock:
            start.set_start()
            mid.set_mid()
            end.set_end()

        _best_path(algo, start_to_mid, mid)
        _best_path(algo, mid_to_end, end)
    elif algo.check_algo() == algo.ALGO_BI_DIJKSTRA:
        temp = bi_dijkstra(algo, start, mid, end, draw_best_path=False)
        start_to_mid = temp[0]
        first_swarm_meet_square = temp[1]
        second_swarm_meet_square = temp[2]
        temp = bi_dijkstra(algo, mid, end, start, draw_best_path=False)
        mid_to_end = temp[0]
        third_swarm_meet_square = temp[1]
        fourth_swarm_meet_square = temp[2]
        
        # Fixes squares disappearing when dragging
        with algo.lock:
            start.set_start()
            mid.set_mid()
            end.set_end()

        _best_path_bi_dijkstra(algo, start_to_mid, first_swarm_meet_square, second_swarm_meet_square)
        _best_path_bi_dijkstra(algo, mid_to_end, third_swarm_meet_square, fourth_swarm_meet_square)


def recursive_maze(algo: AlgoState, chamber: tuple = None,
    division_limit: int = 3, num_gaps: int = 3) -> None:
    """Creates maze using recursive division."""
    # Only perform these on first call
    if not chamber:
        algo._timer_reset()

    # Start timer here to include setup in timer
    algo._timer_start()
    
    # Creates chambers to divide into
    if chamber is None:
        chamber_width: int = Square.get_num_rows()
        chamber_height: int = Square.get_num_cols()
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
    algo._timer_end(count=False)

    # Draws vertical maze line within chamber
    if chamber_width >= division_limit:
        for y in range(chamber_height):
            algo._timer_start()
            square: Square = Square.get_square(chamber_left + x_divide, chamber_top + y)
            with algo.lock:
                square.set_wall()
            sleep(algo._recursive_maze_delay_us, unit="us")
            algo._timer_end()

    # Draws horizontal maze line within chamber
    if chamber_height >= division_limit:
        for x in range(chamber_width):
            algo._timer_start()
            square: Square = Square.get_square(chamber_left + x, chamber_top + y_divide)
            with algo.lock:
                square.set_wall()
            sleep(algo._recursive_maze_delay_us, unit="us")
            algo._timer_end()

    # Start timer again
    algo._timer_start()
    
    # Terminates if below division limit
    if chamber_width < division_limit and chamber_height < division_limit:
        return

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

    # Prevents drawing wall over gaps
    gaps_to_offset: list = [x for x in range(num_gaps - 1, Square.get_num_rows(), num_gaps)]

    # End timer here to resume in loop
    algo._timer_end(count=False)

    # Draws the gaps into the walls
    for wall in _get_random_sample(walls, num_gaps):

        # Continue timer here
        algo._timer_start()

        if wall[3] == 1:
            x = _get_randrange(wall[0], wall[0] + wall[2])
            y = wall[1]
            if x in gaps_to_offset and y in gaps_to_offset:
                if wall[2] == x_divide:
                    x -= 1
                else:
                    x += 1
            if x >= Square.get_num_rows():
                x = Square.get_num_rows() - 1
        else:
            x = wall[0]
            y = _get_randrange(wall[1], wall[1] + wall[3])
            if y in gaps_to_offset and x in gaps_to_offset:
                if wall[3] == y_divide:
                    y -= 1
                else:
                    y += 1
            if y >= Square.get_num_rows():
                y = Square.get_num_rows() - 1
        square: Square = Square.get_square(x, y)
        with algo.lock:
            square.reset()

        algo._timer_end()

    # Recursively divides chambers
    for chamber in chambers:
        recursive_maze(algo, chamber)


def _get_random_sample(population: tuple, k: int) -> list:
    """Returns a k length list of unique elements from population"""
    return random.sample(population, k)


def _get_randrange(start: int, stop: int) -> int:
    """Return a random int within a range"""
    return random.randrange(start, stop)
