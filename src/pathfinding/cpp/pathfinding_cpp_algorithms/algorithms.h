#pragma once

#include "square.h"

#include <vector>

class Square
{
public:
    friend bool operator== (const Square& self, const Square& other);
    friend bool operator< (const Square& self, const Square& other);
    friend bool operator!= (const Square& self, const Square& other);
    friend bool operator> (const Square& self, const Square& other);
    friend bool operator<= (const Square& self, const Square& other);
    friend bool operator>= (const Square& self, const Square& other);

    std::vector<Square> get_neighbours() const;
    bool is_closed() const;
    void set_open();
    void set_closed();
};

// Code for dijkstra algorithm
std::unordered_map<Square, Square> dijkstra(
    const std::vector<std::vector<Square>>& graph,
    const Square& start,
    const Square& end,
    const Square& ignore_node,
    bool draw_best_path = true,
    bool visualize = true
);

// Code for A* algorithm
std::unordered_map<Square, Square> a_star(
    const std::vector<std::vector<Square>>& graph,
    const Square& start,
    const Square& end,
    const Square& ignore_node,
    bool draw_best_path = true,
    bool visualize = true
);

// Code for Bi-directional dijkstra. Custom algorithm.
std::unordered_map<Square, Square> bi_dijkstra(
    const std::vector<std::vector<Square>>& graph,
    const Square& start,
    const Square& end,
    const Square& ignore_node,
    bool draw_best_path = true,
    bool visualize = true
);

// Main algo for reconstructing path
void best_path(const std::unordered_map<Square, Square>& came_from, const Square& end, bool visualize);