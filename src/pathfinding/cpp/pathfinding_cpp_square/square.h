#pragma once

#include <array>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>


class Square
{
public:
    Square(int row, int col)
        : m_row{ row }, m_col{ col }
    {
        m_is_valid = true;  // If casted to bool, return true
        m_pos = std::array<int, 2>{ m_row, m_col };
        m_x = m_row * s_square_length;
        m_y = m_col * s_square_length;

        double square_length_trunc = static_cast<int>(s_square_length);
        m_square_dim = { m_x, m_y, square_length_trunc, square_length_trunc };
    }

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

    std::array<int, 2> get_pos() const { return m_pos; }
    std::array<int, 3>* get_color() { return &m_color; }
    std::vector<Square> get_neighbours() const;
    std::array<double, 4>* draw_square() { return &m_square_dim; }

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

    // Set wall color to the version for the map
    void set_wall_color_map() { m_wall_color = s__wall_color_map; }

    //////////////////////Static Below//////////////////////

    // Initialize the graph for the class
    static void init(int graph_width, int pixel_offset = 0);
    
    // Get get info about squares from class

    static std::vector<std::vector<Square>>* s_get_graph() { return &s_graph; }
    static Square* s_get_square(int row, int col) { return &s_graph[row][col]; }
    static int s_get_num_rows() { return s_num_rows; }
    static int s_get_num_cols() { return s_num_cols; }
    static double s_get_square_length() { return s_square_length; }
    static std::unordered_set<Square, Square::hash>* s_get_all_empty_squares() { return &s_all_empty_squares; }
    static std::unordered_set<Square, Square::hash>* s_get_all_open_squares() { return &s_all_open_squares; }
    static std::unordered_set<Square, Square::hash>* s_get_all_open2_squares() { return &s_all_open2_squares; }
    static std::unordered_set<Square, Square::hash>* s_get_all_open3_squares() { return &s_all_open3_squares; }
    static std::unordered_set<Square, Square::hash>* s_get_all_closed_squares() { return &s_all_closed_squares; }
    static std::unordered_set<Square, Square::hash>* s_get_all_closed2_squares() { return &s_all_closed2_squares; }
    static std::unordered_set<Square, Square::hash>* s_get_all_closed3_squares() { return &s_all_closed3_squares; }
    static std::unordered_set<Square, Square::hash>* s_get_all_start_squares() { return &s_all_start_squares; }
    static std::unordered_set<Square, Square::hash>* s_get_all_mid_squares() { return &s_all_mid_squares; }
    static std::unordered_set<Square, Square::hash>* s_get_all_end_squares() { return &s_all_end_squares; }
    static std::unordered_set<Square, Square::hash>* s_get_all_wall_squares() { return &s_all_wall_squares; }
    static std::unordered_set<Square, Square::hash>* s_get_all_path_squares() { return &s_all_path_squares; }
    static std::unordered_set<Square, Square::hash>* s_get_all_history_squares() { return &s_all_history_squares; }
    static std::unordered_set<Square, Square::hash>* s_get_squares_to_update() { return &s_squares_to_update; }
    static std::unordered_set<Square, Square::hash>* s_get_square_history() { return &s_square_history; }
    static bool s_get_track_square_history() { return s_track_square_history; }

    // Change square containers of the class

    static void s_reset_algo_squares();
    static void s_reset_all_squares();
    static void s_clear_squares_to_update() { s_squares_to_update.clear(); }
    static void s_clear_history_squares() { s_all_history_squares.clear(); }
    static void s_clear_square_history() { s_square_history.clear(); }
    static void s_clear_all_square_lists();

    // Handle changing track_square_history
    static void s_set_track_square_history(bool x) { s_track_square_history = x; }

    // Update values
    static void s_update_num_rows_cols(int new_num) { s_num_rows = s_num_cols = new_num; }

private:
    // Member variables assigned from constructor arguments

    int m_row;
    int m_col;

    // Member variables assigned in constructor

    std::array<int, 2> m_pos;
    double m_x;
    double m_y;
    std::array<double, 4> m_square_dim;  // x, y, x_length, y_length
    
    // Member variables with default values

    bool m_is_valid{ false }; // Set to true for non default constructor
    std::array<int, 3> m_color{ s_default_color };
    std::array<int, 3> m_wall_color{ s__wall_color };
    bool m_is_highway{ false };
    std::array<int, 3> m_color_history{-1, -1, -1}; // Initialize to invalid rgb

    // Member variables assigned in member functions

    std::unordered_map<std::string, Square&> m_neighbours;

    // Member functions

    void update_neighbours();
    void reset_wall_color() { m_wall_color = s__wall_color; }
    void discard_square(bool remove_wall = true);

    //////////////////////Static Below//////////////////////

    // Stores the instances of all the squares
    static inline std::vector<std::vector<Square>> s_graph;

    // Info about the squares
    static inline int s_num_rows = 46;  // Defualt value
    static inline int s_num_cols = 46;  // Default value
    static inline double s_square_length = 0;  // Assigned in init function
    
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

    // Class containers for square types

    static inline std::unordered_set<Square, Square::hash> s_all_empty_squares;
    static inline std::unordered_set<Square, Square::hash> s_all_open_squares;
    static inline std::unordered_set<Square, Square::hash> s_all_open2_squares;
    static inline std::unordered_set<Square, Square::hash> s_all_open3_squares;
    static inline std::unordered_set<Square, Square::hash> s_all_closed_squares;
    static inline std::unordered_set<Square, Square::hash> s_all_closed2_squares;
    static inline std::unordered_set<Square, Square::hash> s_all_closed3_squares;
    static inline std::unordered_set<Square, Square::hash> s_all_start_squares;
    static inline std::unordered_set<Square, Square::hash> s_all_mid_squares;
    static inline std::unordered_set<Square, Square::hash> s_all_end_squares;
    static inline std::unordered_set<Square, Square::hash> s_all_wall_squares;
    static inline std::unordered_set<Square, Square::hash> s_all_path_squares;
    static inline std::unordered_set<Square, Square::hash> s_all_history_squares;

    // Container that gets check from outside class to know what squares have changed
    static inline std::unordered_set<Square, Square::hash> s_squares_to_update;

    // Handle tracking squares that has been changed for visualization

    static inline std::unordered_set<Square, Square::hash> s_square_history;
    static inline bool s_track_square_history = false;

    // Update square lengths
    static void s_update_square_length(int graph_width, int pixel_offset) { s_square_length = static_cast<double>(graph_width - pixel_offset) / s_num_rows; }
};