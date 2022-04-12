#include "algorithms.h"
#include "square.cpp"  // Must include cpp files or else cmake won't link.

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
    m_start_ptr = arg.null_square_ptr();
    m_mid_ptr = arg.null_square_ptr();
    m_end_ptr = arg.null_square_ptr();
    m_ignore_square_ptr = arg.null_square_ptr();
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
            if (!*m_mid_ptr)
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
            g_score[&square] = std::numeric_limits<int>::lowest();
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
            int temp_g_score{ g_score.at(curr_square_ptr) - 1 };
            if (temp_g_score > g_score.at(nei_ptr))
            {
                came_from[nei_ptr] = curr_square_ptr;
                g_score[nei_ptr] = temp_g_score;

                --queue_pos;
                std::tuple<int, int, Square*> queue_tuple{ std::make_tuple(g_score.at(nei_ptr), queue_pos, nei_ptr) };
                open_set.push(queue_tuple);
                if (nei_ptr != end_ptr && !nei_ptr->is_closed() && nei_ptr != ignore_square_ptr)
                {
                    std::scoped_lock{ algo->m_lock };
                    nei_ptr->set_open();
                }
            }
        }

        // Sets square to closed after finished checking
        if (curr_square_ptr != start_ptr && curr_square_ptr != ignore_square_ptr)
        {
            std::scoped_lock{ algo->m_lock };
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
        .def("start_loop", &AlgoState::start_loop, py::return_value_policy::automatic_reference, py::call_guard<py::gil_scoped_release>())
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
    
    //
    // FROM square.cpp. Need to include this here for imports to work.
    //

    // Define Python API for opaque types
    py::bind_vector<std::vector<std::vector<Square>>>(m, "VectorGraph");
    py::bind_vector<std::vector<Square>>(m, "VectorSquare");
    py::bind_vector<std::vector<Square*>>(m, "VectorSquare*");

    // Define Python API for Square class
    // Default to automatic_reference return policy.
    // Return pointers to return a reference to python. Must make container opaque to prevent pybind11 from copying.
    // Use reference_internal if C++ might delete data while python is using it (should be rare)
    // Use take_ownership when C++ will have no use and python should call the destructor.
    py::class_<Square>(m, "Square")
        .def(py::init<int, int>())
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(hash(py::self))
        .def("get_pos", &Square::get_pos, py::return_value_policy::automatic_reference)
        .def("get_color", &Square::get_color, py::return_value_policy::automatic_reference)
        .def("get_neighbours", &Square::get_neighbours, py::return_value_policy::automatic_reference)
        .def("draw_square", &Square::draw_square, py::return_value_policy::automatic_reference)
        .def("is_empty", &Square::is_empty, py::return_value_policy::automatic_reference)
        .def("is_open", &Square::is_open, py::return_value_policy::automatic_reference)
        .def("is_open2", &Square::is_open2, py::return_value_policy::automatic_reference)
        .def("is_open3", &Square::is_open3, py::return_value_policy::automatic_reference)
        .def("is_closed", &Square::is_closed, py::return_value_policy::automatic_reference)
        .def("is_closed2", &Square::is_closed2, py::return_value_policy::automatic_reference)
        .def("is_closed3", &Square::is_closed3, py::return_value_policy::automatic_reference)
        .def("is_start", &Square::is_start, py::return_value_policy::automatic_reference)
        .def("is_mid", &Square::is_mid, py::return_value_policy::automatic_reference)
        .def("is_end", &Square::is_end, py::return_value_policy::automatic_reference)
        .def("is_wall", &Square::is_wall, py::return_value_policy::automatic_reference)
        .def("is_path", &Square::is_path, py::return_value_policy::automatic_reference)
        .def("is_history", &Square::is_history, py::return_value_policy::automatic_reference)
        .def("is_highway", &Square::is_highway, py::return_value_policy::automatic_reference)
        .def("reset", &Square::reset, py::return_value_policy::automatic_reference)
        .def("set_open", &Square::set_open, py::return_value_policy::automatic_reference)
        .def("set_open2", &Square::set_open2, py::return_value_policy::automatic_reference)
        .def("set_open3", &Square::set_open3, py::return_value_policy::automatic_reference)
        .def("set_closed", &Square::set_closed, py::return_value_policy::automatic_reference)
        .def("set_closed2", &Square::set_closed2, py::return_value_policy::automatic_reference)
        .def("set_closed3", &Square::set_closed3, py::return_value_policy::automatic_reference)
        .def("set_start", &Square::set_start, py::return_value_policy::automatic_reference)
        .def("set_mid", &Square::set_mid, py::return_value_policy::automatic_reference)
        .def("set_end", &Square::set_end, py::return_value_policy::automatic_reference)
        .def("set_wall", &Square::set_wall, py::return_value_policy::automatic_reference)
        .def("set_path", &Square::set_path, py::return_value_policy::automatic_reference)
        .def("set_history", &Square::set_history, py::return_value_policy::automatic_reference)
        .def("set_history_rollback", &Square::set_history_rollback, py::return_value_policy::automatic_reference)
        .def("set_wall_color_map", &Square::set_wall_color_map, py::return_value_policy::automatic_reference)
        .def("set_highway", &Square::set_highway, py::return_value_policy::automatic_reference)
        .def("init", &Square::init, "pixel_offset"_a = 0, py::return_value_policy::automatic_reference)
        .def_static("get_graph", &Square::s_get_graph, py::return_value_policy::automatic_reference)
        .def_static("get_square", &Square::s_get_square, py::return_value_policy::automatic_reference)
        .def_static("get_num_rows", &Square::s_get_num_rows, py::return_value_policy::automatic_reference)
        .def_static("get_num_cols", &Square::s_get_num_cols, py::return_value_policy::automatic_reference)
        .def_static("get_square_length", &Square::s_get_square_length, py::return_value_policy::automatic_reference)
        .def_static("get_all_empty_squares", &Square::s_get_all_empty_squares, py::return_value_policy::automatic_reference)
        .def_static("get_all_open_squares", &Square::s_get_all_open_squares, py::return_value_policy::automatic_reference)
        .def_static("get_all_open2_squares", &Square::s_get_all_open2_squares, py::return_value_policy::automatic_reference)
        .def_static("get_all_open3_squares", &Square::s_get_all_open3_squares, py::return_value_policy::automatic_reference)
        .def_static("get_all_closed_squares", &Square::s_get_all_closed_squares, py::return_value_policy::automatic_reference)
        .def_static("get_all_closed2_squares", &Square::s_get_all_closed2_squares, py::return_value_policy::automatic_reference)
        .def_static("get_all_closed3_squares", &Square::s_get_all_closed3_squares, py::return_value_policy::automatic_reference)
        .def_static("get_all_start_squares", &Square::s_get_all_start_squares, py::return_value_policy::automatic_reference)
        .def_static("get_all_mid_squares", &Square::s_get_all_mid_squares, py::return_value_policy::automatic_reference)
        .def_static("get_all_end_squares", &Square::s_get_all_end_squares, py::return_value_policy::automatic_reference)
        .def_static("get_all_wall_squares", &Square::s_get_all_wall_squares, py::return_value_policy::automatic_reference)
        .def_static("get_all_path_squares", &Square::s_get_all_path_squares, py::return_value_policy::automatic_reference)
        .def_static("get_all_history_squares", &Square::s_get_all_history_squares, py::return_value_policy::automatic_reference)
        .def_static("get_squares_to_update", &Square::s_get_squares_to_update, py::return_value_policy::automatic_reference)
        .def_static("get_future_history_squares", &Square::s_get_future_history_squares, py::return_value_policy::automatic_reference)
        .def_static("get_track_square_history", &Square::s_get_track_square_history, py::return_value_policy::automatic_reference)
        .def_static("get_null_square", &Square::s_get_null_square, py::return_value_policy::automatic_reference)
        .def_static("reset_algo_squares", &Square::s_reset_algo_squares, py::return_value_policy::automatic_reference)
        .def_static("reset_all_squares", &Square::s_reset_all_squares, py::return_value_policy::automatic_reference)
        .def_static("clear_squares_to_update", &Square::s_clear_squares_to_update, py::return_value_policy::automatic_reference)
        .def_static("clear_history_squares", &Square::s_clear_history_squares, py::return_value_policy::automatic_reference)
        .def_static("clear_future_history_squares", &Square::s_clear_future_history_squares, py::return_value_policy::automatic_reference)
        .def_static("set_track_square_history", &Square::s_set_track_square_history, py::return_value_policy::automatic_reference)
        .def_static("update_num_rows_cols", &Square::s_update_num_rows_cols, py::return_value_policy::automatic_reference);
}
