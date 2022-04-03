#pragma once

#include <array>
#include <unordered_map>
#include <unordered_set>
#include <vector>


class Square
{
public:
    Square(int row, int col, int rows, float square_size)
        : m_row{ row }, m_col{ col }, m_rows{ rows }, m_square_size{ square_size }
    {
        m_is_valid = true;  // If casted to bool, return true
        m_x = m_row * m_square_size;
        m_y = m_col * m_square_size;
        Square::graph[m_row].push_back(std::move(*this));
    }

    // Initialize the graph for the class
    static std::vector<std::vector<Square>> init(int rows, int cols, float square_size);

    // Allow these operators

    bool operator== (const Square& other) const { return m_row == other.m_row && m_col == other.m_col; }
    bool operator!= (const Square& other) const { return !(operator==(other)); }

    // Allow hashing using row and col position
    struct hash
    {
        std::size_t operator()(const Square& square) const
        {
            std::size_t row_hash = std::hash<int>()(square.m_row);
            std::size_t col_hash = std::hash<int>()(square.m_col) << 1;
            return row_hash ^ col_hash;
        }
    };
    
    // False if instanced using default constructor
    operator bool() const { return m_is_valid; }

    // Info about square

    std::array<int, 2> get_pos() const { return std::array<int, 2>{ m_row, m_col }; }
    std::array<int, 3>& get_color() { return m_color; }
    std::vector<Square> get_neighbours() const;
    std::array<float, 4> draw_square() const;

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
    bool is_wall() const { return m_color == m_wall_color; }
    bool is_path() const { return m_color == s_path_color; }
    bool is_history() const { return m_color == s_history_color; }

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
    void set_history_rollback() { m_color = m_color_history; }

    // Handle changing wall color

    void reset_wall_color() { m_wall_color = s__wall_color; }
    void set_wall_color_map() { m_wall_color = s__wall_color_map; }

    // Get get info about nodes from class

    static std::vector<std::vector<Square>>& s_get_graph() { return graph; }
    static Square& s_get_square(int row, int col) { return graph[row][col]; }
    static std::unordered_set<Square, Square::hash>& s_get_all_empty_nodes() { return s_all_empty_nodes; }
    static std::unordered_set<Square, Square::hash>& s_get_all_open_nodes() { return s_all_open_nodes; }
    static std::unordered_set<Square, Square::hash>& s_get_all_open2_nodes() { return s_all_open2_nodes; }
    static std::unordered_set<Square, Square::hash>& s_get_all_open3_nodes() { return s_all_open3_nodes; }
    static std::unordered_set<Square, Square::hash>& s_get_all_closed_nodes() { return s_all_closed_nodes; }
    static std::unordered_set<Square, Square::hash>& s_get_all_closed2_nodes() { return s_all_closed2_nodes; }
    static std::unordered_set<Square, Square::hash>& s_get_all_closed3_nodes() { return s_all_closed3_nodes; }
    static std::unordered_set<Square, Square::hash>& s_get_all_start_nodes() { return s_all_start_nodes; }
    static std::unordered_set<Square, Square::hash>& s_get_all_mid_nodes() { return s_all_mid_nodes; }
    static std::unordered_set<Square, Square::hash>& s_get_all_end_nodes() { return s_all_end_nodes; }
    static std::unordered_set<Square, Square::hash>& s_get_all_wall_nodes() { return s_all_wall_nodes; }
    static std::unordered_set<Square, Square::hash>& s_get_all_path_nodes() { return s_all_path_nodes; }
    static std::unordered_set<Square, Square::hash>& s_get_all_history_nodes() { return s_all_history_nodes; }
    static std::unordered_set<Square, Square::hash>& s_get_nodes_to_update() { return s_nodes_to_update; }
    static std::unordered_set<Square, Square::hash>& s_get_node_history() { return s_node_history; }
    static bool s_get_track_node_history() { return s_track_node_history; }

    // Change node containers of the class

    static void s_clear_nodes_to_update() { s_nodes_to_update.clear(); }
    static void s_clear_history_nodes() { s_all_history_nodes.clear(); }
    static void s_clear_node_history() { s_node_history.clear(); }
    static void s_clear_all_node_lists();

    // Handle changing track_node_history
    static void s_set_track_node_history(bool x) { s_track_node_history = x; }

private:
    // Stores the instances of all the nodes
    static inline std::vector<std::vector<Square>> graph;
    
    // Member variables assigned from constructor arguments

    int m_row;
    int m_col;
    int m_rows;
    float m_square_size;

    // Member variables assigned in constructor

    float m_x;
    float m_y;
    
    // Member variables with default values

    bool m_is_valid{ false }; // Set to true for non default constructor
    std::array<int, 3> m_color{ s_default_color };
    std::array<int, 3> m_wall_color{ s__wall_color };
    bool m_is_highway{ false };
    std::array<int, 3> m_color_history{-1, -1, -1}; // Initialize to invalid rgb

    // Member variables assigned in member functions

    std::unordered_map<const char*, Square&> m_neighbours;

    // Remove node from corresponding container
    void discard_node(bool remove_wall = true);

    // Colors for different states

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
    static constexpr std::array<int, 3> s__wall_color{ 0, 0, 0 };  // To avoid using over m_wall_color
    static constexpr std::array<int, 3> s__wall_color_map{ 0, 0, 0 };  // To avoid using over m_wall_color
    static constexpr std::array<int, 3> s_path_color{ 255, 255, 0 };
    static constexpr std::array<int, 3> s_history_color{ 106, 13, 173 };

    // Class containers for node types

    static inline std::unordered_set<Square, Square::hash> s_all_empty_nodes;
    static inline std::unordered_set<Square, Square::hash> s_all_open_nodes;
    static inline std::unordered_set<Square, Square::hash> s_all_open2_nodes;
    static inline std::unordered_set<Square, Square::hash> s_all_open3_nodes;
    static inline std::unordered_set<Square, Square::hash> s_all_closed_nodes;
    static inline std::unordered_set<Square, Square::hash> s_all_closed2_nodes;
    static inline std::unordered_set<Square, Square::hash> s_all_closed3_nodes;
    static inline std::unordered_set<Square, Square::hash> s_all_start_nodes;
    static inline std::unordered_set<Square, Square::hash> s_all_mid_nodes;
    static inline std::unordered_set<Square, Square::hash> s_all_end_nodes;
    static inline std::unordered_set<Square, Square::hash> s_all_wall_nodes;
    static inline std::unordered_set<Square, Square::hash> s_all_path_nodes;
    static inline std::unordered_set<Square, Square::hash> s_all_history_nodes;

    // Container that gets check from outside class to know what nodes have changed
    static inline std::unordered_set<Square, Square::hash> s_nodes_to_update;

    // Handle tracking nodes that has been changed for visualization

    static inline std::unordered_set<Square, Square::hash> s_node_history;
    static inline bool s_track_node_history = false;
};