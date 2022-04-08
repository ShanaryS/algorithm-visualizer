#pragma once

#include "square.h"

#include <chrono>
#include <limits>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>


struct AlgoState
{
public:
    bool m_dijkstra_finished{ false };
    bool m_a_star_finished{ false };
    bool m_bi_dijkstra_finished{ false };
    bool m_maze{ false };
    int m_best_path_sleep{ 3 };
    int m_highway_multiplier{ 3 };

    void timer_start() { m_timer_start_time = std::chrono::high_resolution_clock::now(); }
    void timer_end(bool count = true);
    void timer_reset();

private:
    // Timer for algorithm
    double m_timer_total{ 0.0 };
    double m_timer_avg{ 0.0 };
    double m_timer_max{ std::numeric_limits<double>::min() };
    double m_timer_min{ std::numeric_limits<double>::max() };
    int m_timer_count{ 0 };
    std::chrono::time_point<std::chrono::high_resolution_clock> m_timer_start_time;
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

    // Remove once no longer importing draw funcs
    bool legend{ false };
    bool clear_legend{ false };
    bool algo_running{ false };
    bool is_best_path{ false };
    bool is_recursive_maze{ false };
    bool is_graph_size{ false };
    bool is_input{ false };
    bool is_base_img{ false };
    bool is_clean_img{ false };
    bool is_converting_img{ false };

    Square& null_square() { return m_null_square; }
    std::array<int, 4>& null_chamber() { return m_null_chamber; }
    std::vector<std::vector<Square>>& null_graph() { return m_null_graph; }

    // Reset args back to default
    void args_reset();

private:
    Square& m_null_square = Square::s_get_null_square();
    std::array<int, 4> m_null_chamber{};
    std::vector<std::vector<Square>> m_null_graph{};
};

static Args arg;

// Code for dijkstra algorithm
std::unordered_map<Square*, Square*> dijkstra(
    const auto& gph, const auto& algo, const auto& txt,
    const Square& start, const Square& end, const Square& ignore_square = arg.null_square(),
    bool draw_best_path = true, bool visualize = true
);

/*
// Code for A* algorithm
std::unordered_map<Square*, Square*> a_star(
    const auto& gph, const auto& algo, const auto& txt,
    const Square& start, const Square& end, const Square& ignore_square = arg.null_square(),
    bool draw_best_path = true, bool visualize = true
);

// Used by A* to prioritize traveling towards next square
int heuristic(const std::array<int, 2>& pos1, const std::array<int, 2>& pos2);

// Code for Bi-directional dijkstra. Custom algorithm.
std::tuple<std::unordered_map<Square*, Square*>, std::unordered_map<Square*, Square*>, Square*, Square*> bi_dijkstra(
    const auto& gph, const auto& algo, const auto& txt,
    const Square& start, const Square& end, bool alt_color = false,
    const Square& ignore_square = arg.null_square(), bool draw_best_path = true, bool visualize = true
);

// Used by bi_dijkstra to draw best path in two parts
void best_path_bi_dijkstra(
    const auto& gph, const auto& algo, const auto& txt,
    const std::unordered_map<Square*, Square*>& came_from_start,
    const std::unordered_map<Square*, Square*>& came_from_end,
    const Square& first_meet_square, const Square& second_meet_square,
    bool visualize = true
);

*/
// Main algo for reconstructing path
void best_path(
    const auto& gph, const auto& algo, const auto& txt,
    const std::unordered_map<Square*, Square*>& came_from,
    const Square* curr_square, bool reverse = false, bool visualize = true
);

/*
// Used if algos need to reach mid square first
void start_mid_end(
    const auto& gph, const auto& algo, const auto& txt,
    const Square& start, const Square& mid, const Square& end,
    bool is_dijkstra = false, bool is_a_star = false, bool is_bi_dijkstra = false,
    bool visualize = true
);

// Skips steps to end when visualizing algo. Used when dragging oridnal squares
std::unordered_map<> algo_no_vis(
    const auto& gph, const auto& algo, const auto& txt,
    const Square& start, const Square& end, bool is_dijkstra = false,
    bool is_a_star = false, bool is_bi_dijkstra = false, bool alt_color = false,
    const Square& ignore_square = arg.null_square(), bool draw_best_path = true
);

// Creates maze using recursive division.
void recursive_maze(
    const auto& gph, const auto& algo, const auto& txt,
    const std::array<int, 4>& chamber = arg.null_chamber, const std::vector<std::vector<Square>>& graph = arg.null_graph,
    bool visualize = true
);

// Returns a k length vector of unique elements from population
std::vector<> get_random_sample(const std::array<>& population, int k);

// Return a random int within a range
int get_randrange(int start, int stop);
*/
