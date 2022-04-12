#include "algorithms.h"
#include "square.cpp"

#include <pybind11/pybind11.h>

#include <algorithm>
#include <queue>


void AlgoState::run_options(Square& start, Square& mid, Square& end, Square& ignore_square)
{
    std::scoped_lock{ m_lock };
    m_start_ptr = &start;
    m_mid_ptr = &mid;
    m_end_ptr = &end;
    m_ignore_square_ptr = &ignore_square;
}

void AlgoState::run(int phase, int algo)
{
    set_phase(phase);
    set_algo(algo);
    set_finished(false);
}

void AlgoState::reset()
{
    std::scoped_lock{ m_lock };
    m_phase = NONE;
    m_algo = NONE;
    m_start_ptr = nullptr;
    m_mid_ptr = nullptr;
    m_end_ptr = nullptr;
    m_ignore_square_ptr = nullptr;
    m_finished = false;
    m_best_path_delay_ms = DEFAULT_BEST_PATH_DELAY_MS;
    m_recursive_maze_delay_us = DEFAULT_RECURSIVE_MAZE_DELAY_US;
}

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

void AlgoState::algo_loop()
{
    while (true)
    {
        if (check_phase() == PHASE_ALGO && !check_finished())
        {
            int previous_algo = check_algo();
            if (!m_mid_ptr)
            {
                if (check_algo() == ALGO_DIJKSTRA)
                {
                    dijkstra(this, m_start_ptr, m_end_ptr, m_ignore_square_ptr, true);
                }
                else if (check_algo() == ALGO_A_STAR)
                {
                    a_star(this, m_start_ptr, m_end_ptr, m_ignore_square_ptr, true);
                }
                else if (check_algo() == ALGO_BI_DIJKSTRA)
                {
                    bi_dijkstra(this, m_start_ptr, m_end_ptr, false, m_ignore_square_ptr, true);
                }
            }
            else
            {
                start_mid_end(this, m_start_ptr, m_mid_ptr, m_end_ptr);
            }
            set_best_path_delay(DEFAULT_BEST_PATH_DELAY_MS);
            set_algo(previous_algo);
            set_finished(true);
            set_phase(NONE);
        }
        
        else if (check_phase() == PHASE_MAZE && !check_finished())
        {
            if (check_algo() == ALGO_RECURSIVE_MAZE)
            {
                recursive_maze(this);
                set_recursive_maze_delay(DEFAULT_RECURSIVE_MAZE_DELAY_US);
            }
            set_finished(true);
            set_phase(NONE);
        }
    }
}


std::unordered_map<Square*, Square*> dijkstra(
    AlgoState* algo, Square* start_ptr, Square* end_ptr,
    Square* ignore_square_ptr, bool draw_best_path)
{
    // Clear preivious and start timer here
    algo->timer_reset();
    algo->timer_start();

    // Used to determine the order of squares to check. Order of args helper decide the priority.
    int queue_pos{ 0 };
    std::tuple<int, int, Square*> queue_tuple{ std::make_tuple(0, queue_pos, start_ptr) };
    std::priority_queue<std::tuple<int, int, Square*>> open_set{}; // May need to specific vector elements and define comparison for square
    open_set.push(queue_tuple);

    // Determine what is the best square to check
    std::vector<std::vector<Square>>& graph = *Square::s_get_graph();
    std::unordered_map<Square*, int> g_score{};
    for (std::vector<Square>& row : graph)
    {
        for (Square& square : row)
        {
            g_score[&square] = std::numeric_limits<int>::max();
        }
    }
    g_score[start_ptr] = 0;

    // Keeps track of next square for every square in graph. A linked list basically.
    std::unordered_map<Square*, Square*> came_from{};

    // End timer here to start it again in loop
    algo->timer_end(false);

    // Continues until every square has been checked or best path found
    while (!open_set.empty())
    {
        // Time increments for each square being checked
        algo->timer_start();

        // Gets the square currently being checked
        Square* curr_square_ptr{ std::get<2>(open_set.top()) };

        // Terminates if found the best path
        if (curr_square_ptr == end_ptr)
        {
            if (draw_best_path)
            {
                best_path(algo, came_from, end_ptr);
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
        algo->timer_end();
    }
    return came_from;
}


std::unordered_map<Square*, Square*> a_star(
    AlgoState* algo, Square* start_ptr, Square* end_ptr,
    Square* ignore_square_ptr, bool draw_best_path)
{
    return std::unordered_map<Square*, Square*>{};
}

int heuristic(const std::array<int, 2>& pos1, const std::array<int, 2>& pos2) { return 1; }

std::tuple<std::unordered_map<Square*, Square*>, std::unordered_map<Square*, Square*>, Square*, Square*> bi_dijkstra(
    AlgoState* algo, Square* start_ptr, Square* end_ptr,
    bool alt_color, Square* ignore_square_ptr, bool draw_best_path)
{
    return std::tuple<std::unordered_map<Square*, Square*>, std::unordered_map<Square*, Square*>, Square*, Square*>{};
}

void best_path_bi_dijkstra(
    AlgoState* algo,
    const std::unordered_map<Square*, Square*>& came_from_start,
    const std::unordered_map<Square*, Square*>& came_from_end,
    const Square* first_meet_square_ptr, const Square* second_meet_square_ptr)
{}


void best_path(
    AlgoState* algo, const std::unordered_map<Square*, Square*>& came_from,
    const Square* curr_square_ptr, bool reverse)
{}


void start_mid_end(
    AlgoState* algo, Square* start_ptr, Square* mid_ptr, Square* end_ptr)
{}

void recursive_maze(
    AlgoState* algo, const std::array<int, 4>& chamber,
    const std::vector<std::vector<Square>>& graph)
{}


// std::vector<> get_random_sample(const std::array<>& population, int k) {}

int get_randrange(int start, int stop) { return 1; }


namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(algorithms, m)
{
    py::class_<AlgoState>(m, "AlgoState")
        .def(py::init())
        .def_readonly("PHASE_ALGO", &AlgoState::PHASE_ALGO)
        .def_readonly("PHASE_MAZE", &AlgoState::PHASE_MAZE)
        .def_readonly("ALGO_DIJKSTRA", &AlgoState::ALGO_DIJKSTRA)
        .def_readonly("ALGO_A_STAR", &AlgoState::ALGO_A_STAR)
        .def_readonly("ALGO_BI_DIJKSTRA", &AlgoState::ALGO_BI_DIJKSTRA)
        .def_readonly("ALGO_BEST_PATH", &AlgoState::ALGO_BEST_PATH)
        .def_readonly("ALGO_RECURSIVE_MAZE", &AlgoState::ALGO_RECURSIVE_MAZE)
        .def_readonly("NONE", &AlgoState::NONE)
        .def_readonly("timer_total", &AlgoState::m_timer_total)
        .def_readonly("timer_avg", &AlgoState::m_timer_avg)
        .def_readonly("timer_max", &AlgoState::m_timer_max)
        .def_readonly("timer_min", &AlgoState::m_timer_min)
        .def_readonly("timer_count", &AlgoState::m_timer_count)
        .def("start_loop", &AlgoState::start_loop, py::return_value_policy::automatic_reference)
        .def("run_options", &AlgoState::run_options, py::return_value_policy::automatic_reference)
        .def("run", &AlgoState::run, py::return_value_policy::automatic_reference)
        .def("check_phase", &AlgoState::check_phase, py::return_value_policy::automatic_reference)
        .def("check_algo", &AlgoState::check_algo, py::return_value_policy::automatic_reference)
        .def("check_finished", &AlgoState::check_finished, py::return_value_policy::automatic_reference)
        .def("reset", &AlgoState::reset, py::return_value_policy::automatic_reference)
        .def("set_best_path_delay", &AlgoState::set_best_path_delay, py::return_value_policy::automatic_reference)
        .def("set_recursive_maze_delay", &AlgoState::set_recursive_maze_delay, py::return_value_policy::automatic_reference)
        .def("timer_start", &AlgoState::timer_start, py::return_value_policy::automatic_reference)
        .def("timer_end", &AlgoState::timer_end, "count"_a = true, py::return_value_policy::automatic_reference)
        .def("timer_reset", &AlgoState::timer_reset, py::return_value_policy::automatic_reference)
        .def("thread_lock", &AlgoState::thread_lock, py::return_value_policy::automatic_reference)
        .def("thread_unlock", &AlgoState::thread_unlock, py::return_value_policy::automatic_reference);
}
