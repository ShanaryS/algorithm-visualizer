#include "algorithms.h"

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdlib>
#include <queue>
#include <random>
#include <unordered_set>


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
    _set_phase(phase);
    _set_algo(algo);
    _set_finished(false);
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
                    bi_dijkstra(this, m_start_ptr, m_end_ptr, m_ignore_square_ptr, true);
                }
            }
            else
            {
                start_mid_end(this, m_start_ptr, m_mid_ptr, m_end_ptr);
            }
            set_best_path_delay(DEFAULT_BEST_PATH_DELAY_MS);
            _set_algo(previous_algo);
            _set_finished(true);
            _set_phase(NONE);
        }

        else if (check_phase() == PHASE_MAZE && !check_finished())
        {
            if (check_algo() == ALGO_RECURSIVE_MAZE)
            {
                recursive_maze(this);
                set_recursive_maze_delay(DEFAULT_RECURSIVE_MAZE_DELAY_US);
            }
            _set_finished(true);
            _set_phase(NONE);
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
    std::priority_queue<std::tuple<int, int, Square*>> open_set{};
    int queue_pos{ 0 };
    std::tuple<int, int, Square*> queue_tuple{ std::make_tuple(0, queue_pos, start_ptr) };
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
        open_set.pop();

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
            // Ignore walls
            if (nei_ptr->is_wall())
            {
                continue;
            }
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
        // End timer to increment count
        algo->timer_end();
    }
    return came_from;
}


std::unordered_map<Square*, Square*> a_star(
    AlgoState* algo, Square* start_ptr, Square* end_ptr,
    Square* ignore_square_ptr, bool draw_best_path)
{
    // Clear preivious and start timer here
    algo->timer_reset();
    algo->timer_start();

    // Used to determine the order of squares to check. Order of args helper decide the priority.
    std::priority_queue<std::tuple<int, int, Square*>> open_set{};
    int queue_pos{ 0 };
    std::tuple<int, int, Square*> queue_tuple{ std::make_tuple(0, queue_pos, start_ptr) };
    open_set.push(queue_tuple);

    // Determine what is the best square to check
    std::vector<std::vector<Square>>& graph = *Square::s_get_graph();
    std::unordered_map<Square*, int> g_score{};
    std::unordered_map<Square*, int> f_score{};
    for (std::vector<Square>& row : graph)
    {
        for (Square& square : row)
        {
            g_score[&square] = std::numeric_limits<int>::lowest();
            f_score[&square] = std::numeric_limits<int>::lowest();
        }
    }
    g_score[start_ptr] = 0;
    f_score[start_ptr] = heuristic(start_ptr->get_pos(), end_ptr->get_pos());

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
        open_set.pop();

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
            // Ignore walls
            if (nei_ptr->is_wall())
            {
                continue;
            }
            int temp_g_score{ g_score.at(curr_square_ptr) - 1 };
            if (temp_g_score > g_score.at(nei_ptr))
            {
                came_from[nei_ptr] = curr_square_ptr;
                g_score[nei_ptr] = temp_g_score;
                f_score[nei_ptr] = temp_g_score - heuristic(nei_ptr->get_pos(), end_ptr->get_pos());
                --queue_pos;
                std::tuple<int, int, Square*> queue_tuple{ std::make_tuple(f_score.at(nei_ptr), queue_pos, nei_ptr) };
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
        // End timer to increment count
        algo->timer_end();
    }
    return came_from;
}

int heuristic(const std::array<int, 2>& pos1, const std::array<int, 2>& pos2)
{
    auto [x1, y1] = pos1;
    auto [x2, y2] = pos2;
    return std::abs(x1 - x2) + std::abs(y1 - y2);
}

std::tuple<std::unordered_map<Square*, Square*>, Square*, Square*> bi_dijkstra(
    AlgoState* algo, Square* start_ptr, Square* end_ptr,
    Square* ignore_square_ptr, bool draw_best_path)
{
    // Clear preivious and start timer here
    algo->timer_reset();
    algo->timer_start();

    // Used to determine the order of squares to check. Order of args helper decide the priority.
    std::priority_queue<std::tuple<int, int, Square*, std::string>> open_set{};
    int queue_pos{ 0 };
    std::string FIRST_SWARM{ "FIRST_SWARM" };
    std::tuple<int, int, Square*, std::string> queue_tuple_first_swarm{ std::make_tuple(0, queue_pos, start_ptr, FIRST_SWARM) };
    open_set.push(queue_tuple_first_swarm);
    --queue_pos;
    std::string SECOND_SWARM{ "SECOND_SWARM" };
    std::tuple<int, int, Square*, std::string> queue_tuple_second_swarm{ std::make_tuple(0, queue_pos, end_ptr, SECOND_SWARM) };
    open_set.push(queue_tuple_second_swarm);


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
    g_score[end_ptr] = 0;

    // Keeps track of next square for every square in graph. A linked list basically.
    std::unordered_map<Square*, Square*> came_from{};

    // Track the last squares for each swarm
    std::unordered_set<Square*> first_swarm;
    std::unordered_set<Square*> second_swarm;
    Square* first_swarm_meet_square_ptr{ nullptr };
    Square* second_swarm_meet_square_ptr{ nullptr };

    // End timer here to start it again in loop
    algo->timer_end(false);

    // Continues until every square has been checked or best path found
    while (!open_set.empty())
    {
        // Terminates if the swarms meet each other
        if (first_swarm_meet_square_ptr || second_swarm_meet_square_ptr)
        {
            if (draw_best_path)
            {
                best_path_bi_dijkstra(algo, came_from, first_swarm_meet_square_ptr, second_swarm_meet_square_ptr);
            }
            return std::make_tuple(came_from, first_swarm_meet_square_ptr, second_swarm_meet_square_ptr);
        }

        // Time increments for each square being checked
        algo->timer_start();

        // Gets the square currently being checked
        Square* curr_square_ptr{ std::get<2>(open_set.top()) };
        std::string swarm{ std::get<3>(open_set.top()) };
        open_set.pop();

        // Decides the order of neighbours to check
        for (Square* nei_ptr : curr_square_ptr->get_neighbours())
        {
            // Ignore walls
            if (nei_ptr->is_wall())
            {
                continue;
            }
            int temp_g_score{ g_score.at(curr_square_ptr) - 1 };
            if (temp_g_score > g_score.at(nei_ptr))
            {
                came_from[nei_ptr] = curr_square_ptr;
                g_score[nei_ptr] = temp_g_score;
                --queue_pos;
                std::tuple<int, int, Square*, std::string> queue_tuple{ std::make_tuple(g_score.at(nei_ptr), queue_pos, nei_ptr, swarm) };
                open_set.push(queue_tuple);

                if (!nei_ptr->is_closed() && nei_ptr != ignore_square_ptr)
                {
                    if (swarm == FIRST_SWARM && nei_ptr != end_ptr)
                    {
                        first_swarm.insert(nei_ptr);
                        std::scoped_lock{ algo->m_lock };
                        nei_ptr->set_open();
                    }
                    else if (swarm == SECOND_SWARM && nei_ptr != start_ptr)
                    {
                        second_swarm.insert(nei_ptr);
                        std::scoped_lock{ algo->m_lock };
                        nei_ptr->set_open();
                    }
                }
            }
            // Conditions for when path is found
            else if (swarm == FIRST_SWARM && second_swarm.contains(nei_ptr))
            {
                first_swarm_meet_square_ptr = curr_square_ptr;
                second_swarm_meet_square_ptr = nei_ptr;
                break;
            }
            else if (swarm == SECOND_SWARM && first_swarm.contains(nei_ptr))
            {
                first_swarm_meet_square_ptr = nei_ptr;
                second_swarm_meet_square_ptr = curr_square_ptr;
                break;
            }
        }
        // Sets square to closed after finished checking
        if (curr_square_ptr != start_ptr && curr_square_ptr != end_ptr && curr_square_ptr != ignore_square_ptr)
        {
            std::scoped_lock{ algo->m_lock };
            curr_square_ptr->set_closed();
        }
        // End timer to increment count
        algo->timer_end();
    }
    return std::make_tuple(came_from, first_swarm_meet_square_ptr, second_swarm_meet_square_ptr);
}

void best_path_bi_dijkstra(
    AlgoState* algo, std::unordered_map<Square*, Square*>& came_from,
    Square* first_swarm_meet_square_ptr, Square* second_swarm_meet_square_ptr)
{
    // Draw best path for first swarm
    best_path(algo, came_from, first_swarm_meet_square_ptr);
    {
        // Best path skips these two naturally so need to set them here
        std::scoped_lock{ algo->m_lock };
        first_swarm_meet_square_ptr->set_path();
        second_swarm_meet_square_ptr->set_path();
    }
    best_path(algo, came_from, second_swarm_meet_square_ptr, true);
}


void best_path(
    AlgoState* algo, std::unordered_map<Square*, Square*>& came_from,
    Square* curr_square_ptr, bool reverse)
{
    // Update info
    algo->_set_algo(algo->ALGO_BEST_PATH);

    // Puts square path into vector so it's easier to traverse in either direction
    std::vector<Square*> path;
    while (came_from.contains(curr_square_ptr))
    {
        curr_square_ptr = came_from[curr_square_ptr];
        path.push_back(curr_square_ptr);
    }

    // Need to traverse in reverse depending on what part of algo
    if (reverse)
    {
        for (int i{ 0 }; i < static_cast<int>(path.size()) - 1; ++i)
        {
            sleep(algo->m_best_path_delay_ms, "ms");
            Square* square = path[i];
            std::scoped_lock{ algo->m_lock };
            square->set_path();
        }
    }
    else
    {
        for (int i{ static_cast<int>(path.size()) - 2 }; i >= 0; --i)
        {
            sleep(algo->m_best_path_delay_ms, "ms");
            Square* square = path[i];
            std::scoped_lock{ algo->m_lock };
            square->set_path();
        }
    }
}


void start_mid_end(
    AlgoState* algo, Square* start_ptr, Square* mid_ptr, Square* end_ptr)
{
    // Selects the correct algo to use
    if (algo->check_algo() == algo->ALGO_DIJKSTRA)
    {
        std::unordered_map<Square*, Square*> start_to_mid = dijkstra(algo, start_ptr, mid_ptr, end_ptr, false);
        std::unordered_map<Square*, Square*> mid_to_end = dijkstra(algo, mid_ptr, end_ptr, start_ptr, false);

        // Fixes square disappearing when dragging
        {
            std::scoped_lock{ algo->m_lock };
            start_ptr->set_start();
            mid_ptr->set_mid();
            end_ptr->set_end();
        }
        best_path(algo, start_to_mid, mid_ptr);
        best_path(algo, mid_to_end, end_ptr);
    }
    else if (algo->check_algo() == algo->ALGO_A_STAR)
    {
        std::unordered_map<Square*, Square*> start_to_mid = a_star(algo, start_ptr, mid_ptr, end_ptr, false);
        std::unordered_map<Square*, Square*> mid_to_end = a_star(algo, mid_ptr, end_ptr, start_ptr, false);

        // Fixes square disappearing when dragging
        {
            std::scoped_lock{ algo->m_lock };
            start_ptr->set_start();
            mid_ptr->set_mid();
            end_ptr->set_end();
        }
        best_path(algo, start_to_mid, mid_ptr);
        best_path(algo, mid_to_end, end_ptr);
    }
    else if (algo->check_algo() == algo->ALGO_BI_DIJKSTRA)
    {
        auto temp_first_swarm = bi_dijkstra(algo, start_ptr, mid_ptr, end_ptr, false);
        std::unordered_map<Square*, Square*> start_to_mid = std::get<0>(temp_first_swarm);
        Square* first_swarm_meet_square_ptr = std::get<1>(temp_first_swarm);
        Square* second_swarm_meet_square_ptr = std::get<2>(temp_first_swarm);
        auto temp_second_swarm = bi_dijkstra(algo, mid_ptr, end_ptr, start_ptr, false);
        std::unordered_map<Square*, Square*> mid_to_end = std::get<0>(temp_second_swarm);
        Square* third_swarm_meet_square_ptr = std::get<1>(temp_second_swarm);
        Square* fourth_swarm_meet_square_ptr = std::get<2>(temp_second_swarm);

        // Fixes square disappearing when dragging
        {
            std::scoped_lock{ algo->m_lock };
            start_ptr->set_start();
            mid_ptr->set_mid();
            end_ptr->set_end();
        }
        best_path_bi_dijkstra(algo, start_to_mid, first_swarm_meet_square_ptr, second_swarm_meet_square_ptr);
        best_path_bi_dijkstra(algo, mid_to_end, third_swarm_meet_square_ptr, fourth_swarm_meet_square_ptr);
    }
}

void recursive_maze(
    AlgoState* algo, std::array<int, 4>* chamber_ptr,
    std::vector<std::vector<Square>>* graph_ptr, int division_limit, int num_gaps)
{
    // Only perform these on first call
    if (!chamber_ptr)
    {
        algo->timer_reset();
    }

    // Start timer here to include setup in timer
    algo->timer_start();

    // Only get graph once then use it for recursive calls
    std::vector<std::vector<Square>>* graph_ptr_;
    if (!graph_ptr)
    {
        graph_ptr = Square::s_get_graph();
    }
    std::vector<std::vector<Square>>& graph = *graph_ptr_;

    // Creates chambers to divide into
    int chamber_width;
    int chamber_height;
    int chamber_left;
    int chamber_top;
    if (!chamber_ptr)
    {
        chamber_width = Square::s_get_num_rows();
        chamber_height = Square::s_get_num_cols();
        chamber_left = 0;
        chamber_top = 0;
    }
    else
    {
        chamber_width = (*chamber_ptr)[2];
        chamber_height = (*chamber_ptr)[3];
        chamber_left = (*chamber_ptr)[0];
        chamber_top = (*chamber_ptr)[1];
    }

    // Helps with location of chambers
    int x_divide = static_cast<int>(chamber_width / 2);
    int y_divide = static_cast<int>(chamber_height / 2);

    // End timer here to resume in loop
    algo->timer_end(false);

    // Draws vertical maze line wihin chamber
    if (chamber_width >= division_limit)
    {
        for (int y{ 0 }; y < chamber_height; ++y)
        {
            algo->timer_start();
            Square& square = graph[chamber_left + x_divide][chamber_top + y];
            {
                std::scoped_lock{ algo->m_lock };
                square.set_wall();
            }
            sleep(algo->m_recursive_maze_delay_us, "us");
            algo->timer_end();
        }
    }

    // Draws horizontal maze line within chamber
    if (chamber_height >= division_limit)
    {
        for (int x{ 0 }; x < chamber_width; ++x)
        {
            algo->timer_start();
            Square& square = graph[chamber_left + x][chamber_top + y_divide];
            {
                std::scoped_lock{ algo->m_lock };
                square.set_wall();
            }
            sleep(algo->m_recursive_maze_delay_us, "us");
            algo->timer_end();
        }
    }

    // Start timer again
    algo->timer_start();

    // Terminates if below division limit
    if (chamber_width < division_limit && chamber_height < division_limit)
    {
        return;
    }

    // Defining limits on where to draw walls
    std::array<int, 4> top_left{ chamber_left, chamber_top, x_divide, y_divide };
    std::array<int, 4> top_right{ chamber_left + x_divide + 1, chamber_top, chamber_width - x_divide - 1, y_divide };
    std::array<int, 4> bottom_left{ chamber_left, chamber_top + y_divide + 1, x_divide, chamber_height - y_divide - 1 };
    std::array<int, 4> bottom_right{ chamber_left + x_divide + 1, chamber_top + y_divide + 1, chamber_width - x_divide - 1, chamber_height - y_divide - 1 };

    // Combines all chambers into one object
    std::array<std::array<int, 4>, 4> chambers{ top_left, top_right, bottom_left, bottom_right };

    // Defines location of walls
    std::array<int, 4> left{ chamber_left, chamber_top + y_divide, x_divide, 1 };
    std::array<int, 4> right{ chamber_left + x_divide + 1, chamber_top + y_divide, chamber_width - x_divide - 1, 1 };
    std::array<int, 4> top{ chamber_left + x_divide, chamber_top, 1, y_divide };
    std::array<int, 4> bottom{ chamber_left + x_divide, chamber_top + y_divide + 1, 1, chamber_height - y_divide - 1 };

    // Combines walls into one object
    std::array<std::array<int, 4>, 4> walls{ left, right, top, bottom };

    // Prevents drawing wall over gaps
    std::vector<int> gaps_to_offset;
    gaps_to_offset.reserve(Square::s_get_num_rows() / num_gaps);
    for (int i{ num_gaps - 1 }; i < Square::s_get_num_rows(); i += num_gaps)
    {
        gaps_to_offset.push_back(i);
    }

    // End timer here to resume in loop
    algo->timer_end(false);

    // Draws the gaps into the walls
    for (std::array<int, 4>&wall : get_random_sample(walls, num_gaps))
    {
        // Continue timer here
        algo->timer_start();

        int x;
        int y;
        if (wall[3] == 1)
        {
            x = get_randrange(wall[0], wall[0] + wall[2]);
            y = wall[1];
            if (std::find(gaps_to_offset.begin(), gaps_to_offset.end(), x) != gaps_to_offset.end())
            {
                if (std::find(gaps_to_offset.begin(), gaps_to_offset.end(), y) != gaps_to_offset.end())
                {
                    if (wall[2] == x_divide) { --x; }
                    else { ++x; }
                }
            }
            if (x >= Square::s_get_num_rows())
            {
                x = Square::s_get_num_rows() - 1;
            }
        }
        else
        {
            x = wall[0];
            y = get_randrange(wall[1], wall[1] + wall[3]);
            if (std::find(gaps_to_offset.begin(), gaps_to_offset.end(), y) != gaps_to_offset.end())
            {
                if (std::find(gaps_to_offset.begin(), gaps_to_offset.end(), x) != gaps_to_offset.end())
                {
                    if (wall[3] == y_divide) { --y; }
                    else { ++y; }
                }
            }
            if (y >= Square::s_get_num_rows())
            {
                y = Square::s_get_num_rows() - 1;
            }
        }
        Square& square = graph[x][y];
        {
            std::scoped_lock{ algo->m_lock };
            square.reset();
        }
        algo->timer_end();
    }

    // Recursively divides chambers
    for (std::array<int, 4>&chamber : chambers)
    {
        recursive_maze(algo, &chamber, graph_ptr_);
    }
}


std::vector<std::array<int, 4>> get_random_sample(std::array<std::array<int, 4>, 4> population, int k)
{
    std::vector<std::array<int, 4>> res;
    res.reserve(k);

    std::random_device rd;
    std::mt19937 g(rd());

    std::sample(population.begin(), population.end(), std::back_inserter(res), k, g);
    return res;
}

int get_randrange(int start, int stop)
{
    return start + (rand() % (stop - start));
}

void sleep(int delay, std::string unit)
{
    auto end = std::chrono::high_resolution_clock::now();

    if (unit == "ns")
    {
        end += std::chrono::nanoseconds(delay);
    }
    else if (unit == "us")
    {
        end += std::chrono::microseconds(delay);
    }
    else if (unit == "ms")
    {
        end += std::chrono::milliseconds(delay);
    }
    else if (unit == "s")
    {
        end += std::chrono::seconds(delay);
    }
    else if (unit == "min")
    {
        end += std::chrono::minutes(delay);
    }
    else if (unit == "h")
    {
        end += std::chrono::hours(delay);
    }
    else
    {
        throw "NotImplementedError: Invalid time for sleep";
    }

    while (std::chrono::high_resolution_clock::now() < end) {}
}
