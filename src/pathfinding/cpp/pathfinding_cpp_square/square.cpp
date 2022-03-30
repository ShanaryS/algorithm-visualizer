#include <pybind11/pybind11.h>

#include <array>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>


struct Color
{
    const std::array<int, 3> DEFAULT_COLOR{ 255, 255, 255 };
    const std::array<int, 3> OPEN_COLOR{ 64, 224, 208 };
    const std::array<int, 3> OPEN_2_COLOR{ 64, 223, 208 };
    const std::array<int, 3> OPEN_3_COLOR{ 64, 225, 208 };
    const std::array<int, 3> CLOSED_COLOR{ 0, 0, 255 };
    const std::array<int, 3> CLOSED_2_COLOR{ 0, 0, 254 };
    const std::array<int, 3> CLOSED_3_COLOR{ 0, 0, 253 };
    const std::array<int, 3> START_COLOR{ 0, 255, 0 };
    const std::array<int, 3> MID_COLOR{ 255, 165, 0 };
    const std::array<int, 3> END_COLOR{ 255, 0, 0 };
    const std::array<int, 3> WALL_COLOR{ 0, 0, 0 };
    const std::array<int, 3> WALL_COLOR_MAP{ 0, 0, 0 };
    const std::array<int, 3> PATH_COLOR{ 255, 255, 0 };
    const std::array<int, 3> NODE_HISTORY_COLOR{ 106, 13, 173 };
};


class Square
{
public:
    Square(int row, int col, int rows, float square_size)
        : m_row{ row }, m_col{ col }, m_rows{ rows }, m_square_size{ square_size }
    {
        m_x = m_row * m_square_size;
        m_y = m_col * m_square_size;
        m_color = color::DEFAULT_COLOR;
        m_wall_color = color::WALL_COLOR;
        m_is_highway = false;
    }

    friend bool operator== (const Square& first, const Square& second);
    friend bool operator!= (const Square& first, const Square& second);

    std::array<int, 2> get_pos() const { return std::array<int, 2>{ m_row, m_col }; }
    std::array<int, 3> get_color() const { return m_color; }
    std::array<Square, 4> get_neighbours(bool include_walls = false) const;
    void update_neighbours(auto gph);
    std::tuple<std::array<int, 3>, std::tuple<float, int>> draw_square() const;

    bool is_empty() const { return m_color == color::DEFAULT_COLOR; }
    bool is_open() const { return m_color == color::OPEN_COLOR; }
    bool is_open2() const { return m_color == color::OPEN_2_COLOR; }
    bool is_open3() const { return m_color == color::OPEN_3_COLOR; }
    bool is_closed() const { return m_color == color::CLOSED_COLOR; }
    bool is_closed2() const { return m_color == color::CLOSED_2_COLOR; }
    bool is_closed3() const { return m_color == color::CLOSED_3_COLOR; }
    bool is_start() const { return m_color == color::START_COLOR; }
    bool is_mid() const { return m_color == color::MID_COLOR; }
    bool is_end() const { return m_color == color::END_COLOR; }
    bool is_wall() const { return m_color == color::WALL_COLOR; }
    bool is_path() const { return m_color == color::PATH_COLOR; }
    bool is_history() const { return m_color == color::NODE_HISTORY_COLOR; }

    void reset();
    void set_open();
    void set_open_2();
    void set_open_3();
    void set_closed();
    void set_closed_2();
    void set_closed_3();
    void set_start();
    void set_mid();
    void set_end();
    void set_wall();
    void set_path();
    void set_history();

    void reset_wall_color() { m_wall_color = color::WALL_COLOR; }
    void set_wall_color_map() { m_wall_color = color::WALL_COLOR_MAP; }

    std::unordered_set<Square> s_get_all_empty_nodes() { return s_all_empty_nodes; }
    std::unordered_set<Square> s_get_all_open_nodes() { return s_all_open_nodes; }
    std::unordered_set<Square> s_get_all_open_nodes_2() { return s_all_open_nodes_2; }
    std::unordered_set<Square> s_get_all_open_nodes_3() { return s_all_open_nodes_3; }
    std::unordered_set<Square> s_get_all_closed_nodes() { return s_all_closed_nodes; }
    std::unordered_set<Square> s_get_all_closed_nodes_2() { return s_all_closed_nodes_2; }
    std::unordered_set<Square> s_get_all_closed_nodes_3() { return s_all_closed_nodes_3; }
    std::unordered_set<Square> s_get_all_start_nodes() { return s_all_start_nodes; }
    std::unordered_set<Square> s_get_all_mid_nodes() { return s_all_mid_nodes; }
    std::unordered_set<Square> s_get_all_end_nodes() { return s_all_end_nodes; }
    std::unordered_set<Square> s_get_all_wall_nodes() { return s_all_wall_nodes; }
    std::unordered_set<Square> s_get_all_path_nodes() { return s_all_path_nodes; }
    std::unordered_set<Square> s_get_all_history_nodes() { return s_all_history_nodes; }
    std::unordered_set<Square> s_get_all_nodes_to_update() { return s_nodes_to_update; }
    std::unordered_set<Square> s_get_node_history() { return s_node_history; }

    void s_clear_nodes_to_update() { s_nodes_to_update.clear(); }
    void s_clear_history_nodes() { s_all_history_nodes.clear(); }
    void s_clear_node_history() { s_node_history.clear(); }
    void s_clear_all_node_lists();

private:
    static Color color;
    
    int m_row;
    int m_col;
    int m_rows;
    float m_square_size;

    float m_x;
    float m_y;
    std::unordered_map<Square, Square> m_neighbours;
    std::array<int, 3> m_color;
    std::array<int, 3> m_wall_color;
    std::array<int, 3> m_color_history;
    bool m_is_highway;

    void discard_node(bool remove_wall = true);

    static std::unordered_set<Square> s_all_empty_nodes;
    static std::unordered_set<Square> s_all_open_nodes;
    static std::unordered_set<Square> s_all_open_nodes_2;
    static std::unordered_set<Square> s_all_open_nodes_3;
    static std::unordered_set<Square> s_all_closed_nodes;
    static std::unordered_set<Square> s_all_closed_nodes_2;
    static std::unordered_set<Square> s_all_closed_nodes_3;
    static std::unordered_set<Square> s_all_start_nodes;
    static std::unordered_set<Square> s_all_mid_nodes;
    static std::unordered_set<Square> s_all_end_nodes;
    static std::unordered_set<Square> s_all_wall_nodes;
    static std::unordered_set<Square> s_all_path_nodes;
    static std::unordered_set<Square> s_all_history_nodes;

    static std::unordered_set<Square> s_nodes_to_update;
    static std::unordered_set<Square> s_node_history;
    static inline bool s_track_node_history = false;
};


namespace py = pybind11;

PYBIND11_MODULE(pathfinding_cpp_node, m) {
    py::class_<Square>(m, "Square")
        .def(py::init<>)

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}