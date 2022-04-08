#include "algorithms.h"

#include <pybind11/pybind11.h>

#include <algorithm>
#include <queue>


void AlgoState::timer_end(bool count)
{
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> total = end - m_timer_start_time;
    m_timer_total += total;
    if (count)
    {
        m_timer_count += 1;
    }
    if (m_timer_count)
    {
        m_timer_avg = m_timer_total / m_timer_count;
    }
    if (total)
    {
        m_timer_max = std::max(m_timer_max, total);
    }
    if (total)
    {
        m_timer_min = std::min(m_timer_min, total);
    }
}

void AlgoState::timer_reset()
{
    m_timer_total = 0.0;
    m_timer_avg = 0.0;
    m_timer_max = std::numeric_limits<int>::min();
    m_timer_min = std::numeric_limits<int>::max();
    m_timer_count = 0;
    m_timer_start_time = 0;
}


std::unordered_map<Square*, Square*> dijkstra(
    const auto& gph, const auto& algo, const auto& txt,
    const Square& start, const Square& end, const Square& ignore_square,
    bool draw_best_path, bool visualize
)
{
    // Clear preivious and start timer here
    algo.timer_reset()
        algo.timer_start()

        // Used to determine the order of squares to check. Order of args helper decide the priority.
        int queue_pos{ 0 };
    std::tuple<int, int, Square> queue_tuple{ std::make_tuple(0, queue_pos, start) };
    std::priority_queue<std::tuple<int, int, Square>> open_set{}; // May need to specific vector elements and define comparison for square
    open_set.push(queue_tuple);

    // Determine what is the best square to check
    std::unordered_map<Square, int> g_score{};
    for (const auto& row : graph)
    {
        for (const auto& square : row)
        {
            g_score[square] = std::numeric_limits<int>::max();
        }
    }
    g_score[start] = 0;

    // Keeps track of next node for every node in graph. A linked list basically.
    std::unordered_map<Square, Square> came_from{};

    // End timer here to start it again in loop
    algo.timer_end(false)

        // Continues until every node has been checked or best path found
        int i{ 0 };
    while (!open_set.empty())
    {
        // Time increments for each square being checked
        algo.timer_start()

            // Gets the square currently being checked
            Square curr_square
        {
            std::get<2>(open_set.top())
        };
        curr_square = Square();

        // Terminates if found the best path
        if (curr_square == end)
        {
            if (draw_best_path)
            {
                best_path(came_from, end, visualize);
            }
            return came_from;
        }

        // Decides the order of neighbours to check
        for (const auto& nei : curr_square.get_neighbours())
        {
            int temp_g_score{ g_score[curr_square] + 1 };
            if (temp_g_score < g_score[nei])
            {
                came_from[nei] = curr_square;
                g_score[nei] = temp_g_score;

                ++queue_pos;
                std::tuple<int, int, Square> queue_tuple{ std::make_tuple(g_score[nei], queue_pos, nei) };
                open_set.push(queue_tuple);
                if (nei != end && !nei.is_closed() && nei != ignore_node)
                {
                    nei.set_open();
                }
            }
        }

        // Sets square to closed after finished checking
        bool already_closed{ curr_square.is_closed() };
        if (curr_square != start && curr_square != ignore_node)
        {
            curr_square.set_closed();
        }

        // End timer before visualizing for better comparisions
        algo.timer_end();
        txt.timer_to_string(algo.timer_total, algo.timer_count)

        // Only visualize if called. Checks if square is closed to not repeat when mid square included.
        if (visualize && !already_closed)
        {
            i += 1;
            if (i % gph.algo_speed_multiplier == 0)
            {
                i = 0;
                draw(gph, txt, algo_running = true);
                draw_vis_text(gph, txt, is_dijkstra = true);
            }
        }
    }
    return came_from;
}

std::unordered_map<Square*, Square*> a_star(
    const auto& gph, const auto& algo, const auto& txt,
    const Square& start, const Square& end, const Square& ignore_square,
    bool draw_best_path, bool visualize
)
{}

int heuristic(const std::array<int, 2>& pos1, const std::array<int, 2>& pos2) {}

std::tuple<std::unordered_map<Square*, Square*>, std::unordered_map<Square*, Square*>, Square*, Square*> bi_dijkstra(
    const auto& gph, const auto& algo, const auto& txt,
    const Square& start, const Square& end, bool alt_color,
    const Square& ignore_square, bool draw_best_path, bool visualize
)
{}

void best_path_bi_dijkstra(
    const auto& gph, const auto& algo, const auto& txt,
    const std::unordered_map<Square*, Square*>& came_from_start,
    const std::unordered_map<Square*, Square*>& came_from_end,
    const Square& first_meet_square, const Square& second_meet_square,
    bool visualize
)
{}

void best_path(
    const auto& gph, const auto& algo, const auto& txt,
    const std::unordered_map<Square*, Square*>& came_from,
    const Square& curr_square, bool reverse, bool visualize
)
{}

void start_mid_end(
    const auto& gph, const auto& algo, const auto& txt,
    const Square& start, const Square& mid, const Square& end,
    bool is_dijkstra, bool is_a_star, bool is_bi_dijkstra,
    bool visualize
)
{}

std::unordered_map<> algo_no_vis(
    const auto& gph, const auto& algo, const auto& txt,
    const Square& start, const Square& end, bool is_dijkstra,
    bool is_a_star, bool is_bi_dijkstra, bool alt_color,
    const Square& ignore_square, bool draw_best_path, bool reset
)
{}

void recursive_maze(
    const auto& gph, const auto& algo, const auto& txt,
    const std::array<int, 4>& chamber, const std::vector<std::vector<Square>>& graph,
    bool visualize
)
{}

std::vector<> get_random_sample(const std::array<>& population, int k) {}

int get_randrange(int start, int stop) {}

namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(algorithms, m)
{
    py::class_<AlgoState>(m, "AlgoState")
        .def_readwrite("dijkstra_finished", &AlgoState::m_dijkstra_finished, py::return_value_policy::reference_internal)
        .def_readwrite("a_star_finished", &AlgoState::m_a_star_finished, py::return_value_policy::reference_internal)
        .def_readwrite("bi_dijkstra_finished", &AlgoState::m_bi_dijkstra_finished, py::return_value_policy::reference_internal)
        .def_readwrite("maze", &AlgoState::m_maze, py::return_value_policy::reference_internal)
        .def_readonly("best_path_sleep", &AlgoState::m_best_path_sleep, py::return_value_policy::reference_internal)
        .def_readonly("highway_multiplier", &AlgoState::m_highway_multiplier, py::return_value_policy::reference_internal);

    m.def("dijkstra", &dijkstra, "ignore_square"_a = py::none, "draw_best_path"_a = true, "visualize"_a = true, py::return_value_policy::automatic_reference);
    m.def("a_star", &a_star, "ignore_square"_a = py::none, "draw_best_path"_a = true, "visualize"_a = true, py::return_value_policy::automatic_reference);
    m.def("bi_dijkstra", &bi_dijkstra, "alt_color"_a = false, "ignore_square"_a = py::none, "draw_best_path"_a = true, "visualize"_a = true, py::return_value_policy::automatic_reference);
    m.def("start_mid_end", &start_mid_end, "is_dijkstra"_a = false, "is_a_star"_a = false, "is_bi_dijkstra"_a = false, "visualize"_a = true, py::return_value_policy::automatic_reference);
    m.def("algo_no_vis", &algo_no_vis, "is_dijkstra"_a = false, "is_a_star"_a = false, "is_bi_dijkstra"_a = false, "alt_color"_a = false, "ignore_square"_a = py::none, "draw_best_path"_a = true, "reset"_a = true, py::return_value_policy::automatic_reference);
    m.def("recursive_maze", &recursive_maze, "chamber"_a = py::none, "graph"_a = py::none, "visualize"_a = true, py::return_value_policy::automatic_reference);
}
