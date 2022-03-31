#include <pybind11/pybind11.h>

#include "square.h"


std::vector<Square> Square::get_neighbours(bool include_walls = false) const
{
    std::vector<Square> neighbours;
    for (const auto& direction : m_neighbours)
    {
        Square nei{ direction.second };
        if (static_cast<bool>(nei))
        {
            if (!nei.is_wall())
            {
                neighbours.push_back(nei);
            }
            else if (include_walls)
            {
                neighbours.push_back(nei);
            }
        }
    }
    return neighbours;
}

std::tuple<std::array<int, 3>, std::tuple<float, float, int, int>> Square::draw_square() const
{
    auto square_pos = std::make_tuple(m_x, m_y, static_cast<int>(m_square_size), static_cast<int>(m_square_size));
    return std::make_tuple(m_color, square_pos);
}

void Square::reset()
{
    // Don't do anything if already set correctly
    if (is_empty()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = s_default_color;
    m_is_highway = false;
    s_nodes_to_update.insert(*this);
    s_all_empty_nodes.insert(*this);
}

void Square::set_open()
{
    // Don't do anything if already set correctly
    if (is_open()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = s_open_color;
    s_nodes_to_update.insert(*this);
    s_all_open_nodes.insert(*this);
}

void Square::set_open2()
{
    // Don't do anything if already set correctly
    if (is_open2()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = s_open2_color;
    s_nodes_to_update.insert(*this);
    s_all_open2_nodes.insert(*this);
}

void Square::set_open3()
{
    // Don't do anything if already set correctly
    if (is_open3()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = s_open3_color;
    s_nodes_to_update.insert(*this);
    s_all_open3_nodes.insert(*this);
}

void Square::set_closed()
{
    // Don't do anything if already set correctly
    if (is_closed()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = s_closed_color;
    s_nodes_to_update.insert(*this);
    s_all_closed_nodes.insert(*this);
}

void Square::set_closed2()
{
    // Don't do anything if already set correctly
    if (is_closed2()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = s_closed2_color;
    s_nodes_to_update.insert(*this);
    s_all_closed2_nodes.insert(*this);
}

void Square::set_closed3()
{
    // Don't do anything if already set correctly
    if (is_closed3()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = s_closed3_color;
    s_nodes_to_update.insert(*this);
    s_all_closed3_nodes.insert(*this);
}

void Square::set_start()
{
    // Don't do anything if already set correctly
    if (is_start()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node(false);  // Don't remove ordinal node
    m_color = s_start_color;
    s_nodes_to_update.insert(*this);
    s_all_start_nodes.insert(*this);
}

void Square::set_mid()
{
    // Don't do anything if already set correctly
    if (is_mid()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node(false);  // Don't remove ordinal node
    m_color = s_mid_color;
    s_nodes_to_update.insert(*this);
    s_all_mid_nodes.insert(*this);
}

void Square::set_end()
{
    // Don't do anything if already set correctly
    if (is_end()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node(false);  // Don't remove ordinal node
    m_color = s_end_color;
    s_nodes_to_update.insert(*this);
    s_all_end_nodes.insert(*this);
}

void Square::set_wall()
{
    // Don't do anything if already set correctly
    if (is_wall()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = m_wall_color;
    s_nodes_to_update.insert(*this);
    s_all_wall_nodes.insert(*this);
}

void Square::set_path()
{
    // Don't do anything if already set correctly
    if (is_path()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = s_path_color;
    s_nodes_to_update.insert(*this);
    s_all_path_nodes.insert(*this);
}

void Square::set_history()
{
    // Don't do anything if already set correctly
    if (is_history()) { return; }

    // Add to note history if user requests to track
    if (is_path() || is_start() || is_mid() || is_end())
    {
        s_node_history.insert(*this);
    }

    // Don't discard node from list as will be immediately revert color
    // Also don't add to nodes_to_update as it is handled differently
    m_color_history = m_color;
    m_color = s_history_color;
    s_all_history_nodes.insert(*this);
}

void Square::update_neighbours(auto gph)
{
    if (m_col > 0) { m_neighbours["Left"] = gph.graph[m_row][m_col - 1]; }
    if (m_row > 0) { m_neighbours["Up"] = gph.graph[m_row - 1][m_col]; }
    if (m_col < m_rows - 1) { m_neighbours["Right"] = gph.graph[m_row][m_col + 1]; }
    if (m_row < m_rows - 1) { m_neighbours["Down"] = gph.graph[m_row + 1][m_col]; }
}

void Square::s_clear_all_node_lists()
{
    s_all_empty_nodes.clear();
    s_all_open_nodes.clear();
    s_all_open2_nodes.clear();
    s_all_open3_nodes.clear();
    s_all_closed_nodes.clear();
    s_all_closed2_nodes.clear();
    s_all_closed3_nodes.clear();
    s_all_start_nodes.clear();
    s_all_mid_nodes.clear();
    s_all_end_nodes.clear();
    s_all_wall_nodes.clear();
    s_all_path_nodes.clear();
    s_all_history_nodes.clear();
}

void Square::discard_node(bool remove_wall = true)
{
    // Ordinal nodes should not remove wall to reinstate after dragging
    if (!remove_wall && m_color == m_wall_color) { return; }
    
    // Remove this squares color from corresponding list
    if (m_color == s_default_color) { s_all_empty_nodes.erase(*this); }
    else if (m_color == s_open_color) { s_all_open_nodes.erase(*this); }
    else if (m_color == s_open2_color) { s_all_open2_nodes.erase(*this); }
    else if (m_color == s_open3_color) { s_all_open3_nodes.erase(*this); }
    else if (m_color == s_closed_color) { s_all_closed_nodes.erase(*this); }
    else if (m_color == s_closed2_color) { s_all_closed2_nodes.erase(*this); }
    else if (m_color == s_closed3_color) { s_all_closed3_nodes.erase(*this); }
    else if (m_color == s_start_color) { s_all_start_nodes.erase(*this); }
    else if (m_color == s_mid_color) { s_all_mid_nodes.erase(*this); }
    else if (m_color == s_end_color) { s_all_end_nodes.erase(*this); }
    else if (m_color == m_wall_color) { s_all_wall_nodes.erase(*this); }
    else if (m_color == s_path_color) { s_all_path_nodes.erase(*this); }
    else if (m_color == s_history_color) { s_all_history_nodes.erase(*this); }
}

// Allow code to be imported into python using pybind11

namespace py = pybind11;

PYBIND11_MODULE(pathfinding_cpp_node, m) {
    py::class_<Square>(m, "Square")
        .def("reset", &Square::reset);

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}