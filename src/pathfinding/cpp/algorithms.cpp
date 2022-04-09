#include "algorithms.h"

#include <pybind11/pybind11.h>

#include <algorithm>
#include <queue>


void AlgoState::timer_end(bool count)
{
    auto end = std::chrono::high_resolution_clock::now();
    double total = std::chrono::duration<double>(end - m_timer_start_time).count();
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
    m_timer_start_time = std::chrono::high_resolution_clock::now();
}


std::unordered_map<Square*, Square*> dijkstra(
    const auto& algo, const Square& start, const Square& end,
    const Square& ignore_square, bool draw_best_path)
{
    // Clear preivious and start timer here
    algo.timer_reset();
    algo.timer_start();

    // Get pointers to squares for consistency
    Square* start_ptr = &start;
    Square* end_ptr = &end;
    Square* ignore_square_ptr = &ignore_square;

    // Used to determine the order of squares to check. Order of args helper decide the priority.
    int queue_pos{ 0 };
    std::tuple<int, int, Square*> queue_tuple{ std::make_tuple(0, queue_pos, start_ptr) };
    std::priority_queue<std::tuple<int, int, Square*>> open_set{}; // May need to specific vector elements and define comparison for square
    open_set.push(queue_tuple);

    // Determine what is the best square to check
    std::vector<std::vector<Square>>& graph = *Square::s_get_graph();
    std::unordered_map<Square*, int> g_score{};
    for (const std::vector<Square>& row : graph)
    {
        for (Square* square : row)
        {
            g_score[square] = std::numeric_limits<int>::max();
        }
    }
    g_score[start_ptr] = 0;

    // Keeps track of next square for every square in graph. A linked list basically.
    std::unordered_map<Square*, Square*> came_from{};

    // End timer here to start it again in loop
    algo.timer_end(false);

    // Continues until every square has been checked or best path found
    while (!open_set.empty())
    {
        // Time increments for each square being checked
        algo.timer_start();

        // Gets the square currently being checked
        Square* curr_square_ptr{ std::get<2>(open_set.top()) };

        // Terminates if found the best path
        if (curr_square_ptr == end_ptr)
        {
            if (draw_best_path)
            {
                best_path(gph, algo, txt, came_from, end_ptr, visualize);
            }
            return came_from;
        }

        // Decides the order of neighbours to check
        for (Square* nei_ptr : curr_square_ptr->get_neighbours())
        {
            int temp_g_score{ g_score[curr_square_ptr] + 1 };
            if (temp_g_score < g_score[nei_ptr])
            {
                came_from[nei_ptr] = curr_square_ptr;
                g_score[nei_ptr] = temp_g_score;

                ++queue_pos;
                std::tuple<int, int, Square*> queue_tuple{ std::make_tuple(g_score[nei_ptr], queue_pos, nei_ptr) };
                open_set.push(queue_tuple);
                if (nei_ptr != end_ptr && !nei_ptr->is_closed() && nei_ptr != ignore_square_ptr)
                {
                    nei_ptr->set_open();
                }
            }
        }

        // Sets square to closed after finished checking
        if (curr_square_ptr != start_ptr && curr_square_ptr != ignore_square_ptr)
        {
            curr_square_ptr->set_closed();
        }

        // End timer before visualizing for better comparisions
        algo.timer_end();
    }
    return came_from;
}

/*
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

*/
void best_path(
    const auto& gph, const auto& algo, const auto& txt,
    const std::unordered_map<Square*, Square*>& came_from,
    const Square* curr_square, bool reverse, bool visualize
)
{}

/*
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
    const Square& ignore_square, bool draw_best_path
)
{}

void recursive_maze(
    const auto& gph, const auto& algo, const auto& txt,
    const std::array<int, 4>& chamber, const std::vector<std::vector<Square>>& graph,
    bool visualize
)
{}
*/


void Args::args_reset()
{
    draw_best_path = true;
    visualize = true;
    alt_color = true;
    reverse = true;
    is_dijkstra = true;
    is_a_star = true;
    is_bi_dijkstra = true;

    legend = true;
    clear_legend = true;
    algo_running = true;
    is_best_path = true;
    is_recursive_maze = true;
    is_graph_size = true;
    is_input = true;
    is_base_img = true;
    is_clean_img = true;
    is_converting_img = true;
}


// std::vector<> get_random_sample(const std::array<>& population, int k) {}

// int get_randrange(int start, int stop) {}


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

    m.def("dijkstra", &dijkstra, "ignore_square"_a = py::none(), "draw_best_path"_a = true, "visualize"_a = true, py::return_value_policy::automatic_reference);
    m.def("a_star", &a_star, "ignore_square"_a = py::none, "draw_best_path"_a = true, "visualize"_a = true, py::return_value_policy::automatic_reference);
    m.def("bi_dijkstra", &bi_dijkstra, "alt_color"_a = false, "ignore_square"_a = py::none, "draw_best_path"_a = true, "visualize"_a = true, py::return_value_policy::automatic_reference);
    m.def("start_mid_end", &start_mid_end, "is_dijkstra"_a = false, "is_a_star"_a = false, "is_bi_dijkstra"_a = false, "visualize"_a = true, py::return_value_policy::automatic_reference);
    m.def("algo_no_vis", &algo_no_vis, "is_dijkstra"_a = false, "is_a_star"_a = false, "is_bi_dijkstra"_a = false, "alt_color"_a = false, "ignore_square"_a = py::none, "draw_best_path"_a = true, py::return_value_policy::automatic_reference);
    m.def("recursive_maze", &recursive_maze, "chamber"_a = py::none, "graph"_a = py::none, "visualize"_a = true, py::return_value_policy::automatic_reference);
}
