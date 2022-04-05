#include "square.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <pybind11/operators.h>

#include <stdexcept>


void Square::init(int graph_width, int pixel_offset)
{
    // Reset class
    s_clear_all_square_lists();
    s_graph.clear();

    // Update values
    s_update_square_length(graph_width, pixel_offset);

    // Create each square
    for (int row{ 0 }; row < s_num_rows; ++row)
    {
        s_graph.push_back({});
        for (int col{ 0 }; col < s_num_cols; ++col)
        {
            s_graph[row].emplace_back(Square(row, col));
        }
    }

    // Update neighours after all squares are created
    for (std::vector<Square>& row : s_graph)
    {
        for (Square& square : row)
        {
            square.update_neighbours();
        }
    }
}


// Allow hashing using row and col position
template<>
struct std::hash<Square>
{
    size_t operator()(const Square& square) const
    {
        std::array<int, 2> pos = square.get_pos();
        std::size_t row_hash = std::hash<int>()(pos[0]);
        std::size_t col_hash = std::hash<int>()(pos[1]) << 1;
        return row_hash ^ col_hash;
    }
};

std::vector<Square> Square::get_neighbours() const
{
    std::vector<Square> neighbours;
    for (auto&[direction, nei] : m_neighbours)
    {
        neighbours.push_back(nei);
    }
    return neighbours;
}

void Square::reset()
{
    // Don't do anything if already set correctly
    if (is_empty()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_square_history.insert(*this);
    }

    discard_square();
    m_color = s_default_color;
    m_is_highway = false;
    s_squares_to_update.insert(*this);
    s_all_empty_squares.insert(*this);
}

void Square::set_open()
{
    // Don't do anything if already set correctly
    if (is_open()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_square_history.insert(*this);
    }

    discard_square();
    m_color = s_open_color;
    s_squares_to_update.insert(*this);
    s_all_open_squares.insert(*this);
}

void Square::set_open2()
{
    // Don't do anything if already set correctly
    if (is_open2()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_square_history.insert(*this);
    }

    discard_square();
    m_color = s_open2_color;
    s_squares_to_update.insert(*this);
    s_all_open2_squares.insert(*this);
}

void Square::set_open3()
{
    // Don't do anything if already set correctly
    if (is_open3()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_square_history.insert(*this);
    }

    discard_square();
    m_color = s_open3_color;
    s_squares_to_update.insert(*this);
    s_all_open3_squares.insert(*this);
}

void Square::set_closed()
{
    // Don't do anything if already set correctly
    if (is_closed()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_square_history.insert(*this);
    }

    discard_square();
    m_color = s_closed_color;
    s_squares_to_update.insert(*this);
    s_all_closed_squares.insert(*this);
}

void Square::set_closed2()
{
    // Don't do anything if already set correctly
    if (is_closed2()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_square_history.insert(*this);
    }

    discard_square();
    m_color = s_closed2_color;
    s_squares_to_update.insert(*this);
    s_all_closed2_squares.insert(*this);
}

void Square::set_closed3()
{
    // Don't do anything if already set correctly
    if (is_closed3()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_square_history.insert(*this);
    }

    discard_square();
    m_color = s_closed3_color;
    s_squares_to_update.insert(*this);
    s_all_closed3_squares.insert(*this);
}

void Square::set_start()
{
    // Don't do anything if already set correctly
    if (is_start()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_square_history.insert(*this);
    }

    discard_square(false);  // Don't remove ordinal square
    m_color = s_start_color;
    s_squares_to_update.insert(*this);
    s_all_start_squares.insert(*this);
}

void Square::set_mid()
{
    // Don't do anything if already set correctly
    if (is_mid()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_square_history.insert(*this);
    }

    discard_square(false);  // Don't remove ordinal square
    m_color = s_mid_color;
    s_squares_to_update.insert(*this);
    s_all_mid_squares.insert(*this);
}

void Square::set_end()
{
    // Don't do anything if already set correctly
    if (is_end()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_square_history.insert(*this);
    }

    discard_square(false);  // Don't remove ordinal square
    m_color = s_end_color;
    s_squares_to_update.insert(*this);
    s_all_end_squares.insert(*this);
}

void Square::set_wall()
{
    // Don't do anything if already set correctly
    if (is_wall()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_square_history.insert(*this);
    }

    discard_square();
    m_color = m_wall_color;
    s_squares_to_update.insert(*this);
    s_all_wall_squares.insert(*this);
}

void Square::set_path()
{
    // Don't do anything if already set correctly
    if (is_path()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_square_history.insert(*this);
    }

    discard_square();
    m_color = s_path_color;
    s_squares_to_update.insert(*this);
    s_all_path_squares.insert(*this);
}

void Square::set_history()
{
    // Don't do anything if already set correctly
    if (is_history()) { return; }

    // Add to note history if user requests to track
    if (is_path() || is_start() || is_mid() || is_end())
    {
        s_square_history.insert(*this);
    }

    // Don't discard square from list as will be immediately revert color
    // Also don't add to squares_to_update as it is handled differently
    m_color_history = m_color;
    m_color = s_history_color;
    s_all_history_squares.insert(*this);
}

void Square::s_reset_algo_squares()
{
    std::array<std::unordered_set<Square, Square::hash>, 7> squares_to_reset{
        s_all_open_squares,
        s_all_open2_squares,
        s_all_open3_squares,
        s_all_closed_squares,
        s_all_closed2_squares,
        s_all_closed3_squares,
        s_all_path_squares
    };

    for (std::unordered_set<Square, Square::hash>& type_set : squares_to_reset)
    {
        for (Square square : type_set)
        {
            square.reset();
        }
    }
}

void Square::s_reset_all_squares()
{
    std::array<std::unordered_set<Square, Square::hash>, 12> squares_to_reset{
        s_all_open_squares,
        s_all_open2_squares,
        s_all_open3_squares,
        s_all_closed_squares,
        s_all_closed2_squares,
        s_all_closed3_squares,
        s_all_start_squares,
        s_all_mid_squares,
        s_all_end_squares,
        s_all_wall_squares,
        s_all_path_squares,
        s_all_history_squares
    };

    for (std::unordered_set<Square, Square::hash>& type_set : squares_to_reset)
    {
        for (Square square : type_set)
        {
            square.reset_wall_color();
            square.reset();
        }
    }
}

void Square::s_clear_all_square_lists()
{
    s_all_empty_squares.clear();
    s_all_open_squares.clear();
    s_all_open2_squares.clear();
    s_all_open3_squares.clear();
    s_all_closed_squares.clear();
    s_all_closed2_squares.clear();
    s_all_closed3_squares.clear();
    s_all_start_squares.clear();
    s_all_mid_squares.clear();
    s_all_end_squares.clear();
    s_all_wall_squares.clear();
    s_all_path_squares.clear();
    s_all_history_squares.clear();
}

void Square::update_neighbours()
{
    if (m_col > 0)
    {
        m_neighbours.insert({ "Left", s_graph[m_row][m_col - 1] });
    }
    if (m_row > 0)
    {
        m_neighbours.insert({ "Up", s_graph[m_row - 1][m_col] });
    }
    if (m_col < s_num_cols - 1)
    {
        m_neighbours.insert({ "Right", s_graph[m_row][m_col + 1] });
    }
    if (m_row < s_num_rows - 1)
    {
        m_neighbours.insert({ "Down", s_graph[m_row + 1][m_col] });
    }
}

void Square::discard_square(bool remove_wall)
{
    // Ordinal squares should not remove wall to reinstate after dragging
    if (!remove_wall && m_color == m_wall_color) { return; }
    
    // Remove this squares color from corresponding list
    if (m_color == s_default_color) { s_all_empty_squares.erase(*this); }
    else if (m_color == s_open_color) { s_all_open_squares.erase(*this); }
    else if (m_color == s_open2_color) { s_all_open2_squares.erase(*this); }
    else if (m_color == s_open3_color) { s_all_open3_squares.erase(*this); }
    else if (m_color == s_closed_color) { s_all_closed_squares.erase(*this); }
    else if (m_color == s_closed2_color) { s_all_closed2_squares.erase(*this); }
    else if (m_color == s_closed3_color) { s_all_closed3_squares.erase(*this); }
    else if (m_color == s_start_color) { s_all_start_squares.erase(*this); }
    else if (m_color == s_mid_color) { s_all_mid_squares.erase(*this); }
    else if (m_color == s_end_color) { s_all_end_squares.erase(*this); }
    else if (m_color == m_wall_color) { s_all_wall_squares.erase(*this); }
    else if (m_color == s_path_color) { s_all_path_squares.erase(*this); }
    else if (m_color == s_history_color) { s_all_history_squares.erase(*this); }
}

// Allow code to be imported into python using pybind11

// Prevent copies being made when passing these types around
PYBIND11_MAKE_OPAQUE(std::vector<std::vector<Square>>);
PYBIND11_MAKE_OPAQUE(std::vector<Square>);
PYBIND11_MAKE_OPAQUE(std::unordered_set<Square, Square::hash>);

namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(pathfinding_cpp_square, m) {
    // Define Python API for opaque types
    py::bind_vector<std::vector<std::vector<Square>>>(m, "VectorGraph");
    py::bind_vector<std::vector<Square>>(m, "VectorSquare");

    py::class_<std::unordered_set<Square, Square::hash>>(m, "UnorderedSetSquare")
        .def(py::init<>())
        .def("copy", [](std::unordered_set<Square, Square::hash>& self) { throw std::runtime_error("Use the copy module in python to copy."); })
        .def("__len__", [](const std::unordered_set<Square, Square::hash>& self) { return self.size(); })
        .def("__iter__", [](std::unordered_set<Square, Square::hash>& self) { return py::make_iterator(self.begin(), self.end()); }, py::keep_alive<0, 1>());

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
        .def("init", &Square::init, "pixel_offset"_a=0, py::return_value_policy::automatic_reference)
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
        .def_static("get_square_history", &Square::s_get_square_history, py::return_value_policy::automatic_reference)
        .def_static("get_track_square_history", &Square::s_get_track_square_history, py::return_value_policy::automatic_reference)
        .def_static("reset_algo_squares", &Square::s_reset_algo_squares, py::return_value_policy::automatic_reference)
        .def_static("reset_all_squares", &Square::s_reset_all_squares, py::return_value_policy::automatic_reference)
        .def_static("clear_squares_to_update", &Square::s_clear_squares_to_update, py::return_value_policy::automatic_reference)
        .def_static("clear_history_squares", &Square::s_clear_history_squares, py::return_value_policy::automatic_reference)
        .def_static("clear_square_history", &Square::s_clear_square_history, py::return_value_policy::automatic_reference)
        .def_static("clear_all_square_lists", &Square::s_clear_all_square_lists, py::return_value_policy::automatic_reference)
        .def_static("set_track_square_history", &Square::s_set_track_square_history, py::return_value_policy::automatic_reference)
        .def_static("update_num_rows_cols", &Square::s_update_num_rows_cols, py::return_value_policy::automatic_reference);

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}