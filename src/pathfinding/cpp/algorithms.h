#pragma once

#include "square.h"

#include <chrono>
#include <limits>
#include <mutex>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>


struct AlgoState
{
public:
    AlgoState()
    {
        NONE = 0;
        PHASE_ALGO = generate_unique_int();
        PHASE_MAZE = generate_unique_int();
        ALGO_DIJKSTRA = generate_unique_int();
        ALGO_A_STAR = generate_unique_int();
        ALGO_BI_DIJKSTRA = generate_unique_int();
        ALGO_BEST_PATH = generate_unique_int();
        ALGO_RECURSIVE_MAZE = generate_unique_int();
        reset();
        timer_reset();
    }

    // Possible phases

    int PHASE_ALGO;
    int PHASE_MAZE;

    // Possible algorithms

    int ALGO_DIJKSTRA;
    int ALGO_A_STAR;
    int ALGO_BI_DIJKSTRA;
    int ALGO_BEST_PATH;
    int ALGO_RECURSIVE_MAZE;

    // Special variables

    int NONE;  // Value is 0 which returns false when casted to bool
    std::mutex m_lock;

    // Control the speed of algorithms. Keep 3x faster than python to maintain speed difference.

    int DEFAULT_BEST_PATH_DELAY_MS = 1;
    int m_best_path_delay_ms;
    int DEFAULT_RECURSIVE_MAZE_DELAY_US = 80;
    int m_recursive_maze_delay_us;

    // Timer for algorithms

    double m_timer_total;
    double m_timer_avg;
    double m_timer_max;
    double m_timer_min;
    int m_timer_count;

    // Functions

    void start_loop() { algo_loop(); }
    void run_options(Square& start, Square& mid, Square& end, Square& ignore_square);
    void run(int phase, int algo);
    int check_phase() { std::scoped_lock{ m_lock }; return m_phase; }
    int check_algo() { std::scoped_lock{ m_lock }; return m_algo; }
    bool check_finished() { std::scoped_lock{ m_lock }; return m_finished; }
    void reset();
    void set_best_path_delay(int ms) { std::scoped_lock{ m_lock }; m_best_path_delay_ms = ms; }
    void set_recursive_maze_delay(int us) { std::scoped_lock{ m_lock }; m_recursive_maze_delay_us = us; }

    // Timer functions

    void timer_start() { m_timer_start_time = std::chrono::high_resolution_clock::now(); }
    void timer_end(bool count = true);
    void timer_reset();

    // Allow python to lock thread

    void thread_lock() { m_lock.lock(); }
    void thread_unlock() { m_lock.unlock(); }

    // Should not be used outside this unit

    void _set_phase(int phase) { std::scoped_lock{ m_lock }; m_phase = phase; }
    void _set_algo(int algo) { std::scoped_lock{ m_lock }; m_algo = algo; }
    void _set_finished(bool x) { std::scoped_lock{ m_lock }; m_finished = x; }

private:
    // The current phase and current/last algorithm

    int m_phase;
    int m_algo;
    int m_finished;  // Combination with ALGO preserves the past

    // Special variables

    int m_unique_int = 0;  // Starts +1 when call by self._next_int()

    // Run options

    Square* m_start_ptr;
    Square* m_mid_ptr;
    Square* m_end_ptr;
    Square* m_ignore_square_ptr;

    // Timer for algorithms

    std::chrono::time_point<std::chrono::high_resolution_clock> m_timer_start_time;

    // Functions

    void algo_loop();
    int generate_unique_int() { return ++m_unique_int; }
};


// Organize the arguments to functions.
struct Args
{
public:
    Square* null_square_ptr() const { return m_null_square_ptr; }

private:
    Square* m_null_square_ptr = Square::s_get_null_square();
};

static Args arg;

// Code for dijkstra algorithm
std::unordered_map<Square*, Square*> dijkstra(
    AlgoState* algo, Square* start_ptr, Square* end_ptr,
    Square* ignore_square_ptr, bool draw_best_path);


// Code for A* algorithm
std::unordered_map<Square*, Square*> a_star(
    AlgoState* algo, Square* start_ptr, Square* end_ptr,
    Square* ignore_square_ptr, bool draw_best_path);

// Used by A* to prioritize traveling towards next square
int heuristic(const std::array<int, 2>& pos1, const std::array<int, 2>& pos2);

// Code for Bi-directional dijkstra. Custom algorithm.
std::tuple<std::unordered_map<Square*, Square*>, Square*, Square*> bi_dijkstra(
    AlgoState* algo, Square* start_ptr, Square* end_ptr,
    Square* ignore_square_ptr, bool draw_best_path);

// Used by bi_dijkstra to draw best path in two parts
void best_path_bi_dijkstra(
    AlgoState* algo, std::unordered_map<Square*, Square*>& came_from,
    Square* first_swarm_meet_square_ptr, Square* second_swarm_meet_square_ptr);


// Main algo for reconstructing path
void best_path(
    AlgoState* algo, std::unordered_map<Square*, Square*>& came_from,
    Square* curr_square_ptr, bool reverse = false);


// Used if algos need to reach mid square first
void start_mid_end(
    AlgoState* algo, Square* start_ptr, Square* mid_ptr, Square* end_ptr);

// Creates maze using recursive division.
void recursive_maze(
    AlgoState* algo, std::array<int, 4>* chamber = nullptr,
    std::vector<std::vector<Square>>* graph = nullptr,
    int division_limit = 3, int num_gaps = 3);

// Returns a k length vector of unique elements from population
std::vector<std::array<int, 4>> get_random_sample(std::array<std::array<int, 4>, 4> population, int k);

// Return a random int within a range
int get_randrange(int start, int stop);

// Sleep for an exact amout of time using a no-op loop
void sleep(int delay, std::string unit = "s");
