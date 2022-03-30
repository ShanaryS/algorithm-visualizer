#include <pybind11/pybind11.h>

#include <array>
#include <tuple>
#include <unordered_map>
#include <unordered_set>


class Square
{
public:
    Square(int row, int col, int rows, float square_size)
        : m_row{ row }, m_col{ col }, m_rows{ rows }, m_square_size{ square_size }
    {
        m_x = m_row * m_square_size;
        m_y = m_col * m_square_size;
        m_color = s_default_color;
        m_wall_color = s_wall_color;
        m_is_highway = false;
    }

    // Allow these operators

    friend bool operator== (const Square& first, const Square& second);
    friend bool operator!= (const Square& first, const Square& second);

    // Info about square

    std::array<int, 2> get_pos() const { return std::array<int, 2>{ m_row, m_col }; }
    std::array<int, 3> get_color() const { return m_color; }
    std::array<Square, 4> get_neighbours(bool include_walls = false) const;
    std::tuple<std::array<int, 3>, std::tuple<float, int>> draw_square() const;

    // Check square type

    bool is_empty() const { return m_color == s_default_color; }
    bool is_open() const { return m_color == s_open_color; }
    bool is_open2() const { return m_color == s_open2_color; }
    bool is_open3() const { return m_color == s_open3_color; }
    bool is_closed() const { return m_color == s_closed_color; }
    bool is_closed2() const { return m_color == s_closed2_color; }
    bool is_closed3() const { return m_color == s_closed3_color; }
    bool is_start() const { return m_color == s_start_color; }
    bool is_mid() const { return m_color == s_mid_color; }
    bool is_end() const { return m_color == s_end_color; }
    bool is_wall() const { return m_color == s_wall_color; }
    bool is_path() const { return m_color == s_path_color; }
    bool is_history() const { return m_color == s_node_history_color; }

    // Set square type

    void reset();
    void set_open();
    void set_open2();
    void set_open3();
    void set_closed();
    void set_closed2();
    void set_closed3();
    void set_start();
    void set_mid();
    void set_end();
    void set_wall();
    void set_path();
    void set_history();

    // Define square's neighbours
    void update_neighbours(auto gph);

    // Handle changing wall color

    void reset_wall_color() { m_wall_color = s_wall_color; }
    void set_wall_color_map() { m_wall_color = s_wall_color_map; }

    // Get get info about nodes from class

    std::unordered_set<Square> s_get_all_empty_nodes() { return s_all_empty_nodes; }
    std::unordered_set<Square> s_get_all_open_nodes() { return s_all_open_nodes; }
    std::unordered_set<Square> s_get_all_open_nodes2() { return s_all_open_nodes2; }
    std::unordered_set<Square> s_get_all_open_nodes3() { return s_all_open_nodes3; }
    std::unordered_set<Square> s_get_all_closed_nodes() { return s_all_closed_nodes; }
    std::unordered_set<Square> s_get_all_closed_nodes2() { return s_all_closed_nodes2; }
    std::unordered_set<Square> s_get_all_closed_nodes3() { return s_all_closed_nodes3; }
    std::unordered_set<Square> s_get_all_start_nodes() { return s_all_start_nodes; }
    std::unordered_set<Square> s_get_all_mid_nodes() { return s_all_mid_nodes; }
    std::unordered_set<Square> s_get_all_end_nodes() { return s_all_end_nodes; }
    std::unordered_set<Square> s_get_all_wall_nodes() { return s_all_wall_nodes; }
    std::unordered_set<Square> s_get_all_path_nodes() { return s_all_path_nodes; }
    std::unordered_set<Square> s_get_all_history_nodes() { return s_all_history_nodes; }
    std::unordered_set<Square> s_get_all_nodes_to_update() { return s_nodes_to_update; }
    std::unordered_set<Square> s_get_node_history() { return s_node_history; }

    // Change node containers of the class

    void s_clear_nodes_to_update() { s_nodes_to_update.clear(); }
    void s_clear_history_nodes() { s_all_history_nodes.clear(); }
    void s_clear_node_history() { s_node_history.clear(); }
    void s_clear_all_node_lists();

private:
    // Member variables assigned from outside class

    int m_row;
    int m_col;
    int m_rows;
    float m_square_size;

    // Member variables assigned in constructor

    float m_x;
    float m_y;
    std::unordered_map<Square, Square> m_neighbours;
    std::array<int, 3> m_color;
    std::array<int, 3> m_wall_color;
    std::array<int, 3> m_color_history;
    bool m_is_highway;

    // Remove node from corresponding container
    void discard_node(bool remove_wall = true);

    // Hard coded colors for different states

    static constexpr std::array<int, 3> s_default_color{ 255, 255, 255 };
    static constexpr std::array<int, 3> s_open_color{ 64, 224, 208 };
    static constexpr std::array<int, 3> s_open2_color{ 64, 223, 208 };
    static constexpr std::array<int, 3> s_open3_color{ 64, 225, 208 };
    static constexpr std::array<int, 3> s_closed_color{ 0, 0, 255 };
    static constexpr std::array<int, 3> s_closed2_color{ 0, 0, 254 };
    static constexpr std::array<int, 3> s_closed3_color{ 0, 0, 253 };
    static constexpr std::array<int, 3> s_start_color{ 0, 255, 0 };
    static constexpr std::array<int, 3> s_mid_color{ 255, 165, 0 };
    static constexpr std::array<int, 3> s_end_color{ 255, 0, 0 };
    static constexpr std::array<int, 3> s_wall_color{ 0, 0, 0 };
    static constexpr std::array<int, 3> s_wall_color_map{ 0, 0, 0 };
    static constexpr std::array<int, 3> s_path_color{ 255, 255, 0 };
    static constexpr std::array<int, 3> s_node_history_color{ 106, 13, 173 };

    // Class containers for node types

    static std::unordered_set<Square> s_all_empty_nodes;
    static std::unordered_set<Square> s_all_open_nodes;
    static std::unordered_set<Square> s_all_open_nodes2;
    static std::unordered_set<Square> s_all_open_nodes3;
    static std::unordered_set<Square> s_all_closed_nodes;
    static std::unordered_set<Square> s_all_closed_nodes2;
    static std::unordered_set<Square> s_all_closed_nodes3;
    static std::unordered_set<Square> s_all_start_nodes;
    static std::unordered_set<Square> s_all_mid_nodes;
    static std::unordered_set<Square> s_all_end_nodes;
    static std::unordered_set<Square> s_all_wall_nodes;
    static std::unordered_set<Square> s_all_path_nodes;
    static std::unordered_set<Square> s_all_history_nodes;

    // Container that gets check from outside class to know what nodes have changed
    static std::unordered_set<Square> s_nodes_to_update;

    // Handle tracking nodes that has been changed for visualization

    static std::unordered_set<Square> s_node_history;
    static inline bool s_track_node_history = false;
};


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