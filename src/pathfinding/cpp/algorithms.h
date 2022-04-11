#pragma once

#include "square.h"

#include <chrono>
#include <limits>
#include <mutex>
#include <string>
#include <thread>
#include <tuple>
#include <unordered_map>
#include <vector>


struct AlgoState
{
public:
    AlgoState()
    {
        PHASE_ALGO = generate_unique_int();
        PHASE_MAZE = generate_unique_int();
        ALGO_DIJKSTRA = generate_unique_int();
        ALGO_A_STAR = generate_unique_int();
        ALGO_BI_DIJKSTRA = generate_unique_int();
        ALGO_BEST_PATH = generate_unique_int();
        ALGO_RECURSIVE_MAZE = generate_unique_int();
        reset();
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

    // Timer for algorithms

    double m_timer_total{ 0.0 };
    double m_timer_avg{ 0.0 };
    double m_timer_max{ std::numeric_limits<double>::min() };
    double m_timer_min{ std::numeric_limits<double>::max() };
    int m_timer_count{ 0 };

    void start_loop() {}
    void run_options(const Square& start, const Square& mid, const Square& end, const Square& ignore_square);
    void run(int phase, int algo) { set_phase(phase); set_algo(algo); set_finished(false); }
    int check_phase() { std::scoped_lock{ m_lock }; return m_phase; }
    int check_algo() { std::scoped_lock{ m_lock }; return m_phase; }
    bool check_finished() { std::scoped_lock{ m_lock }; return m_phase; }
    void reset();
    void set_best_path_delay(int ms) {}
    void set_recursive_maze_delay(int us) {}

    void timer_start() { m_timer_start_time = std::chrono::high_resolution_clock::now(); }
    void timer_end(bool count = true);
    void timer_reset();

private:
    // The current phase and current/last algorithm

    int m_phase;
    int m_algo;
    int m_finished;  // Combination with ALGO preserves the past

    // Special variables

    int m_unique_int = 0;  // Starts +1 when call by self._next_int()

    // Run options

    const Square* m_start = nullptr;
    const Square* m_mid = nullptr;
    const Square* m_end = nullptr;
    const Square* m_ignore_square = nullptr;

    // Control the speed of algorithms

    int DEFAULT_BEST_PATH_DELAY_MS = 3;
    int m_best_path_delay_ms;
    int DEFAULT_RECURSIVE_MAZE_DELAY_US = 250;
    int m_recursive_maze_delay_us;

    // Timer for algorithms

    std::chrono::time_point<std::chrono::high_resolution_clock> m_timer_start_time;

    void set_phase(int phase) {}
    void set_algo(int algo) {}
    void set_finished(bool x) {}
    void algo_loop();
    int generate_unique_int() { return ++m_unique_int; }
};


// Organize the arguments to functions.
struct Args
{
public:
    bool draw_best_path{ true };
    bool visualize{ true };
    bool alt_color{ true };
    bool reverse{ true };
    bool is_dijkstra{ true };
    bool is_a_star{ true };
    bool is_bi_dijkstra{ true };

    const Square& null_square() const { return m_null_square; }
    const std::array<int, 4>& null_chamber() const { return m_null_chamber; }
    const std::vector<std::vector<Square>>& null_graph() const { return m_null_graph; }

    // Reset args back to default
    void args_reset();

private:
    const Square& m_null_square = Square::s_get_null_square();
    const std::array<int, 4> m_null_chamber{};
    const std::vector<std::vector<Square>> m_null_graph{};
};

static Args arg;

// Code for dijkstra algorithm
std::unordered_map<Square*, Square*> dijkstra(
    AlgoState& algo, Square& start, Square& end,
    Square& ignore_square, bool draw_best_path);


// Code for A* algorithm
std::unordered_map<Square*, Square*> a_star(
    AlgoState& algo, Square& start, Square& end,
    Square& ignore_square, bool draw_best_path);

// Used by A* to prioritize traveling towards next square
int heuristic(const std::array<int, 2>& pos1, const std::array<int, 2>& pos2);

// Code for Bi-directional dijkstra. Custom algorithm.
std::tuple<std::unordered_map<Square*, Square*>, std::unordered_map<Square*, Square*>, Square*, Square*> bi_dijkstra(
    AlgoState& algo, Square& start, Square& end,
    bool alt_color, Square& ignore_square, bool draw_best_path);

// Used by bi_dijkstra to draw best path in two parts
void best_path_bi_dijkstra(
    AlgoState& algo,
    const std::unordered_map<Square*, Square*>& came_from_start,
    const std::unordered_map<Square*, Square*>& came_from_end,
    const Square* first_meet_square, const Square* second_meet_square);


// Main algo for reconstructing path
void best_path(
    AlgoState& algo, const std::unordered_map<Square*, Square*>& came_from,
    const Square* curr_square, bool reverse = false);


// Used if algos need to reach mid square first
void start_mid_end(
    AlgoState& algo, Square& start, Square& mid, Square& end);

// Creates maze using recursive division.
void recursive_maze(
    AlgoState& algo,
    const std::array<int, 4>& chamber = arg.null_chamber(), const std::vector<std::vector<Square>>& graph = arg.null_graph());

// Returns a k length vector of unique elements from population
//std::vector<> get_random_sample(const std::array<>& population, int k);

// Return a random int within a range
int get_randrange(int start, int stop);
