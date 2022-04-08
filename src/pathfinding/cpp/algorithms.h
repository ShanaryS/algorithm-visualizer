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
    std::string timer_to_string();
    void timer_reset();

private:
    // Timer for algorithm
    auto m_timer_total{};
    auto m_timer_avg{ std::numeric_limits};
    auto m_timer_max{ std::numeric_limits<int>::min() };
    auto m_timer_min{ std::numeric_limits<int>::max() };
    int m_timer_count{};
    auto m_timer_start_time{};
};


// Code for dijkstra algorithm
std::unordered_map<Square*, Square*> dijkstra(
    const auto& gph, const auto& algo, const auto& txt,
    const Square& start, const Square& end, const Square& ignore_square,
    bool draw_best_path = true, bool visualize = true
);

// Code for A* algorithm
std::unordered_map<Square*, Square*> a_star(
    const auto& gph, const auto& algo, const auto& txt,
    const Square& start, const Square& end, const Square& ignore_square,
    bool draw_best_path = true, bool visualize = true
);

// Used by A* to prioritize traveling towards next square
int heuristic(const std::array<int, 2>& pos1, const std::array<int, 2>& pos2);

// Code for Bi-directional dijkstra. Custom algorithm.
std::tuple<std::unordered_map<Square*, Square*>, std::unordered_map<Square*, Square*>, Square*, Square*> bi_dijkstra(
    const auto& gph, const auto& algo, const auto& txt,
    const Square& start, const Square& end, bool alt_color = false,
    const Square& ignore_square, bool draw_best_path = true, bool visualize = true
);

// Used by bi_dijkstra to draw best path in two parts
void best_path_bi_dijkstra(
    const auto& gph, const auto& algo, const auto& txt,
    const std::unordered_map<Square*, Square*>& came_from_start,
    const std::unordered_map<Square*, Square*>& came_from_end,
    const Square& first_meet_square, const Square& second_meet_square,
    bool visualize = true
);

// Main algo for reconstructing path
void best_path(
    const auto& gph, const auto& algo, const auto& txt,
    const std::unordered_map<Square*, Square*>& came_from,
    const Square& curr_square, bool reverse = false, bool visualize = true
);

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
    const Square& ignore_square, bool draw_best_path = true, bool reset = false
);

// Creates maze using recursive division.
void recursive_maze(
    const auto& gph, const auto& algo, const auto& txt,
    const std::array<int, 4>& chamber, const std::vector<std::vector<Square>>& graph,
    bool visualize = true
);

// Returns a k length vector of unique elements from population
std::vector<> get_random_sample(const std::array<>& population, int k);

// Return a random int within a range
int get_randrange(int start, int stop);