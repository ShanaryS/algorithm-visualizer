#include "square.h"


void Square::init(int graph_width, int pixel_offset)
{
    // Reset class
    s_clear_all_square_lists();
    s_graph.clear();
    s_graph.reserve(s_num_rows * s_num_cols);

    // Update values
    s_update_square_length(graph_width, pixel_offset);

    // Emplace each square into graph in row-major order
    for (int row{ 0 }; row < s_num_rows; ++row)
    {
        for (int col{ 0 }; col < s_num_cols; ++col)
        {
            // Store squares into array as row-major order
            s_graph.emplace_back(Square(row, col));
        }
    }

    // Update neighours after all squares are created
    for (Square& square : s_graph)
    {
        square.update_neighbours();
    }

    // Create a null square
    s_null_square.clear();
    s_null_square.emplace_back(Square(-1, -1));
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

std::vector<Square*> Square::get_neighbours() const
{
    std::vector<Square*> neighbours;
    for (auto& [direction, nei_ptr] : m_neighbours)
    {
        neighbours.push_back(nei_ptr);
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
        s_future_history_squares.insert(this);
    }

    discard_square();
    m_color = s_default_color;
    m_is_highway = false;
    s_squares_to_update.insert(this);
    s_all_empty_squares.insert(this);
}

void Square::set_open()
{
    // Don't do anything if already set correctly
    if (is_open()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_future_history_squares.insert(this);
    }

    discard_square();
    m_color = s_open_color;
    s_squares_to_update.insert(this);
    s_all_open_squares.insert(this);
}

void Square::set_open2()
{
    // Don't do anything if already set correctly
    if (is_open2()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_future_history_squares.insert(this);
    }

    discard_square();
    m_color = s_open2_color;
    s_squares_to_update.insert(this);
    s_all_open2_squares.insert(this);
}

void Square::set_open3()
{
    // Don't do anything if already set correctly
    if (is_open3()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_future_history_squares.insert(this);
    }

    discard_square();
    m_color = s_open3_color;
    s_squares_to_update.insert(this);
    s_all_open3_squares.insert(this);
}

void Square::set_closed()
{
    // Don't do anything if already set correctly
    if (is_closed()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_future_history_squares.insert(this);
    }

    discard_square();
    m_color = s_closed_color;
    s_squares_to_update.insert(this);
    s_all_closed_squares.insert(this);
}

void Square::set_closed2()
{
    // Don't do anything if already set correctly
    if (is_closed2()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_future_history_squares.insert(this);
    }

    discard_square();
    m_color = s_closed2_color;
    s_squares_to_update.insert(this);
    s_all_closed2_squares.insert(this);
}

void Square::set_closed3()
{
    // Don't do anything if already set correctly
    if (is_closed3()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_future_history_squares.insert(this);
    }

    discard_square();
    m_color = s_closed3_color;
    s_squares_to_update.insert(this);
    s_all_closed3_squares.insert(this);
}

void Square::set_start()
{
    // Don't do anything if already set correctly
    if (is_start()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_future_history_squares.insert(this);
    }

    discard_square(false);  // Don't remove ordinal square
    m_color = s_start_color;
    s_squares_to_update.insert(this);
    s_all_start_squares.insert(this);
}

void Square::set_mid()
{
    // Don't do anything if already set correctly
    if (is_mid()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_future_history_squares.insert(this);
    }

    discard_square(false);  // Don't remove ordinal square
    m_color = s_mid_color;
    s_squares_to_update.insert(this);
    s_all_mid_squares.insert(this);
}

void Square::set_end()
{
    // Don't do anything if already set correctly
    if (is_end()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_future_history_squares.insert(this);
    }

    discard_square(false);  // Don't remove ordinal square
    m_color = s_end_color;
    s_squares_to_update.insert(this);
    s_all_end_squares.insert(this);
}

void Square::set_wall()
{
    // Don't do anything if already set correctly
    if (is_wall()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_future_history_squares.insert(this);
    }

    discard_square();
    m_color = m_wall_color;
    s_squares_to_update.insert(this);
    s_all_wall_squares.insert(this);
}

void Square::set_path()
{
    // Don't do anything if already set correctly
    if (is_path()) { return; }

    // Add to note history if user requests to track
    if (s_track_square_history)
    {
        s_future_history_squares.insert(this);
    }

    discard_square();
    m_color = s_path_color;
    s_squares_to_update.insert(this);
    s_all_path_squares.insert(this);
}

void Square::set_history()
{
    // Don't do anything if already set correctly
    if (is_history()) { return; }

    // Don't do anything if ordinal square or path square
    if (is_path() || is_start() || is_mid() || is_end())
    {
        return;
    }

    // Don't discard square from list as will be immediately revert color
    // Also don't add to squares_to_update as it is handled differently
    m_color_history = m_color;
    m_color = s_history_color;
    s_all_history_squares.insert(this);
}

std::vector<Square*> Square::s_get_all_empty_squares()
{
    std::vector<Square*> empty_squares;
    empty_squares.reserve(s_all_empty_squares.size());
    for (Square* square_ptr : s_all_empty_squares)
    {
        empty_squares.push_back(square_ptr);
    }
    return empty_squares;
}

std::vector<Square*> Square::s_get_all_open_squares()
{
    std::vector<Square*> open_squares;
    open_squares.reserve(s_all_open_squares.size());
    for (Square* square_ptr : s_all_open_squares)
    {
        open_squares.push_back(square_ptr);
    }
    return open_squares;
}

std::vector<Square*> Square::s_get_all_open2_squares()
{
    std::vector<Square*> open2_squares;
    open2_squares.reserve(s_all_open2_squares.size());
    for (Square* square_ptr : s_all_open2_squares)
    {
        open2_squares.push_back(square_ptr);
    }
    return open2_squares;
}

std::vector<Square*> Square::s_get_all_open3_squares()
{
    std::vector<Square*> open3_squares;
    open3_squares.reserve(s_all_open3_squares.size());
    for (Square* square_ptr : s_all_open3_squares)
    {
        open3_squares.push_back(square_ptr);
    }
    return open3_squares;
}

std::vector<Square*> Square::s_get_all_closed_squares()
{
    std::vector<Square*> closed_squares;
    closed_squares.reserve(s_all_closed_squares.size());
    for (Square* square_ptr : s_all_closed_squares)
    {
        closed_squares.push_back(square_ptr);
    }
    return closed_squares;
}

std::vector<Square*> Square::s_get_all_closed2_squares()
{
    std::vector<Square*> closed2_squares;
    closed2_squares.reserve(s_all_closed2_squares.size());
    for (Square* square_ptr : s_all_closed2_squares)
    {
        closed2_squares.push_back(square_ptr);
    }
    return closed2_squares;
}

std::vector<Square*> Square::s_get_all_closed3_squares()
{
    std::vector<Square*> closed3_squares;
    closed3_squares.reserve(s_all_closed3_squares.size());
    for (Square* square_ptr : s_all_closed3_squares)
    {
        closed3_squares.push_back(square_ptr);
    }
    return closed3_squares;
}

std::vector<Square*> Square::s_get_all_start_squares()
{
    std::vector<Square*> start_squares;
    start_squares.reserve(s_all_start_squares.size());
    for (Square* square_ptr : s_all_start_squares)
    {
        start_squares.push_back(square_ptr);
    }
    return start_squares;
}

std::vector<Square*> Square::s_get_all_mid_squares()
{
    std::vector<Square*> mid_squares;
    mid_squares.reserve(s_all_mid_squares.size());
    for (Square* square_ptr : s_all_mid_squares)
    {
        mid_squares.push_back(square_ptr);
    }
    return mid_squares;
}

std::vector<Square*> Square::s_get_all_end_squares()
{
    std::vector<Square*> end_squares;
    end_squares.reserve(s_all_end_squares.size());
    for (Square* square_ptr : s_all_end_squares)
    {
        end_squares.push_back(square_ptr);
    }
    return end_squares;
}

std::vector<Square*> Square::s_get_all_wall_squares()
{
    std::vector<Square*> wall_squares;
    wall_squares.reserve(s_all_wall_squares.size());
    for (Square* square_ptr : s_all_wall_squares)
    {
        wall_squares.push_back(square_ptr);
    }
    return wall_squares;
}

std::vector<Square*> Square::s_get_all_path_squares()
{
    std::vector<Square*> path_squares;
    path_squares.reserve(s_all_path_squares.size());
    for (Square* square_ptr : s_all_path_squares)
    {
        path_squares.push_back(square_ptr);
    }
    return path_squares;
}

std::vector<Square*> Square::s_get_all_history_squares()
{
    std::vector<Square*> history_squares;
    history_squares.reserve(s_all_history_squares.size());
    for (Square* square_ptr : s_all_history_squares)
    {
        history_squares.push_back(square_ptr);
    }
    return history_squares;
}

std::vector<Square*> Square::s_get_squares_to_update()
{
    std::vector<Square*> squares_to_update;
    squares_to_update.reserve(s_squares_to_update.size());
    for (Square* square_ptr : s_squares_to_update)
    {
        squares_to_update.push_back(square_ptr);
    }
    return squares_to_update;
}

std::vector<Square*> Square::s_get_future_history_squares()
{
    std::vector<Square*> future_history_squares;
    future_history_squares.reserve(s_future_history_squares.size());
    for (Square* square_ptr : s_future_history_squares)
    {
        future_history_squares.push_back(square_ptr);
    }
    return future_history_squares;
}


void Square::s_reset_algo_squares()
{
    std::vector<std::vector<Square*>> squares_to_reset{
        s_get_all_open_squares(),
        s_get_all_open2_squares(),
        s_get_all_open3_squares(),
        s_get_all_closed_squares(),
        s_get_all_closed2_squares(),
        s_get_all_closed3_squares(),
        s_get_all_path_squares()
    };

    for (std::vector<Square*>& type_set : squares_to_reset)
    {
        for (Square* square : type_set)
        {
            square->reset();
        }
    }
}

void Square::s_reset_all_squares()
{
    std::vector<std::vector<Square*>> squares_to_reset{
        s_get_all_open_squares(),
        s_get_all_open2_squares(),
        s_get_all_open3_squares(),
        s_get_all_closed_squares(),
        s_get_all_closed2_squares(),
        s_get_all_closed3_squares(),
        s_get_all_start_squares(),
        s_get_all_mid_squares(),
        s_get_all_end_squares(),
        s_get_all_wall_squares(),
        s_get_all_path_squares(),
        s_get_all_history_squares()
    };

    for (std::vector<Square*>& type_set : squares_to_reset)
    {
        for (Square* square : type_set)
        {
            square->reset_wall_color();
            square->reset();
        }
    }
}

void Square::s_set_square_color_by_group(std::vector<Square*>& squares, std::string square_type)
{
    std::array<int, 3> color;
    if (square_type == "reset")
    {
        for (Square* square : squares)
        {
            square->reset();
        }
    }
    else if (square_type == "open")
    {
        for (Square* square : squares)
        {
            square->set_open();
        }
    }
    else if (square_type == "open2")
    {
        for (Square* square : squares)
        {
            square->set_open2();
        }
    }
    else if (square_type == "open3")
    {
        for (Square* square : squares)
        {
            square->set_open3();
        }
    }
    else if (square_type == "closed")
    {
        for (Square* square : squares)
        {
            square->set_closed();
        }
    }
    else if (square_type == "closed2")
    {
        for (Square* square : squares)
        {
            square->set_closed2();
        }
    }
    else if (square_type == "closed3")
    {
        for (Square* square : squares)
        {
            square->set_closed3();
        }
    }
    else if (square_type == "start")
    {
        for (Square* square : squares)
        {
            square->set_start();
        }
    }
    else if (square_type == "mid")
    {
        for (Square* square : squares)
        {
            square->set_mid();
        }
    }
    else if (square_type == "end")
    {
        for (Square* square : squares)
        {
            square->set_end();
        }
    }
    else if (square_type == "wall")
    {
        for (Square* square : squares)
        {
            square->set_wall();
        }
    }
    else if (square_type == "path")
    {
        for (Square* square : squares)
        {
            square->set_path();
        }
    }
    else if (square_type == "history")
    {
        for (Square* square : squares)
        {
            square->set_history();
        }
    }
    else if (square_type == "history_rollback")
    {
        for (Square* square : squares)
        {
            square->set_history_rollback();
        }
    }
    else
    {
        throw "NotImplementedError: Invalid square type provided";
    }
}

void Square::s_set_square_color_by_array(std::vector<std::vector<std::array<int, 4>>>& square_colors)
{
    int ROAD_CUTOFF = 1;  // Any value about this is a road
    int HIGHWAY_CUTOFF = 225;  // Any value below this is a highway

    double square_length = s_get_square_length();
    double square_length_squared = square_length * square_length;
    int length = int(square_length);

    for (int index{ 0 }; index < s_graph.size(); ++index)
    {
        Square& square = s_graph[index];
        square.set_wall_color_map();
        auto [row, col] = square.get_pos();

        int rgb_sum = 0;
        int blue_sum = 0;  // Used for highway
        int row_limit = (row + 1) * length;
        int col_limit = (col + 1) * length;
        for (int x{ row * length }; x < row_limit; ++x)
        {
            for (int y{ col * length }; y < col_limit; ++y)
            {
                auto [red, green, blue, alpha] = square_colors[x][y];
                rgb_sum += red + green + blue;
                blue_sum += blue;
            }
        }
        double rgb_avg = rgb_sum / square_length_squared * 3;
        double blue_avg = blue_sum / square_length_squared;

        // Set squares to roads, highways and non pathable space
        if (rgb_avg < ROAD_CUTOFF)
        {
            square.set_wall();
        }
        else
        {
            square.reset();
            if (blue_avg < HIGHWAY_CUTOFF)
            {
                square.set_highway(true);
            }
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
        m_neighbours.insert({ std::string("Left"), s_get_square(m_row, m_col - 1) });
    }
    if (m_row > 0)
    {
        m_neighbours.insert({ std::string("Up"), s_get_square(m_row - 1, m_col) });
    }
    if (m_col < s_num_cols - 1)
    {
        m_neighbours.insert({ std::string("Right"), s_get_square(m_row, m_col + 1) });
    }
    if (m_row < s_num_rows - 1)
    {
        m_neighbours.insert({ std::string("Down"), s_get_square(m_row + 1, m_col) });
    }
}

void Square::discard_square(bool remove_wall)
{
    // Ordinal squares should not remove wall to reinstate after dragging
    if (!remove_wall && is_wall()) { return; }

    // Remove this squares color from corresponding list
    if (is_empty()) { s_all_empty_squares.erase(this); }
    else if (is_open()) { s_all_open_squares.erase(this); }
    else if (is_open2()) { s_all_open2_squares.erase(this); }
    else if (is_open3()) { s_all_open3_squares.erase(this); }
    else if (is_closed()) { s_all_closed_squares.erase(this); }
    else if (is_closed2()) { s_all_closed2_squares.erase(this); }
    else if (is_closed3()) { s_all_closed3_squares.erase(this); }
    else if (is_start()) { s_all_start_squares.erase(this); }
    else if (is_mid()) { s_all_mid_squares.erase(this); }
    else if (is_end()) { s_all_end_squares.erase(this); }
    else if (is_wall()) { s_all_wall_squares.erase(this); }
    else if (is_path()) { s_all_path_squares.erase(this); }
    else if (is_history()) { s_all_history_squares.erase(this); }
}
