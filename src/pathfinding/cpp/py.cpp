// Allow code to be imported into python using pybind11

// Must include all project .cpp files or else CMake won't link.
#include "square.cpp"
#include "algorithms.cpp"

// pybind11 includes
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <pybind11/operators.h>

namespace py = pybind11;
using namespace pybind11::literals;

// Prevent copies being made when passing these types around
PYBIND11_MAKE_OPAQUE(std::vector<std::vector<Square>>);
PYBIND11_MAKE_OPAQUE(std::vector<Square>);
PYBIND11_MAKE_OPAQUE(std::vector<Square*>);

// Define Python API for classes and functions
// Default to automatic_reference return policy.
// Return pointers to return a reference to python. Must make container opaque to prevent pybind11 from copying.
// Use reference_internal if C++ might delete data while python is using it (should be rare)
// Use take_ownership when C++ will have no use and python should call the destructor.
PYBIND11_MODULE(modules, m)
{
    py::bind_vector<std::vector<std::vector<Square>>>(m, "VectorGraph");
    py::bind_vector<std::vector<Square>>(m, "VectorSquare");
    py::bind_vector<std::vector<Square*>>(m, "VectorSquare*");

    py::class_<Square>(m, "Square")
        .def(py::init<int, int>())
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def("__bool__", &Square::op_bool, py::is_operator(), py::return_value_policy::automatic_reference)
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
}
