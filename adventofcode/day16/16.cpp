#include <algorithm>
#include <iostream>
#include <unordered_map>
#include <vector>

#include "16.hpp"

static std::unordered_map<int, int> DP;

static inline int hash(
    const int node,
    const int players,
    const int time,
    const int on)
{
    /* NOTE: Assumes time is 16 bits, time, 5 bits, players 2 bits and node 5 bits. */
    return (int)(((unsigned int)node << 23u) | ((unsigned int)players << 21u) |
        ((unsigned int)time << 16u) | (unsigned int)on);
}

static inline int set_bit(
    const int n,
    const int b)
{
    return (int)((unsigned int)n | (1u << (unsigned int)b));
}

static inline int get_bit(
    const int n,
    const int b)
{
    return (int)((unsigned int)n & (1u << (unsigned int)b));
}

static int solve(
    const std::vector<int> &flow_rates,
    const std::unordered_map<int, std::vector<std::pair<int, int>>> &graph,
    const std::pair<int, int> start,
    const int node,
    const int time,
    const int on,
    const int players)
{
    if (time <= 0)
    {
        return players > 1 ? solve(flow_rates, graph, start, start.first, start.second, on, players - 1) : 0;
    }

    const auto state = hash(node, players, time, on);

    if (DP.find(state) != DP.end())
    {
        return DP[state];
    }

    int output = 0;

    if (!get_bit(on, node))
    {
        const auto next_on = set_bit(on, node);
        const auto score = flow_rates[node] * (time - 1);

        output = std::max(output, score + solve(flow_rates, graph, start, node, time - 1, next_on, players));
    }
    for (const auto neighbor : graph.at(node))
    {
        const auto next_node = neighbor.first;
        const auto distance = neighbor.second;

        output = std::max(output, solve(flow_rates, graph, start, next_node, time - distance, on, players));
    }

    DP[state] = output;

    return output;
}

static void part_one(
    const std::vector<int> &flow_rates,
    const std::unordered_map<int, std::vector<std::pair<int, int>>> &graph,
    const int start)
{
    const std::pair<int, int> init = std::make_pair(start, 30);

    DP.clear();
    const int answer = solve(
        flow_rates,
        graph,
        init,
        init.first,
        init.second,
        set_bit(0, init.first),
        1);

    std::cout << "Part one: " << answer << std::endl;
}

static void part_two(
    const std::vector<int> &flow_rates,
    const std::unordered_map<int, std::vector<std::pair<int, int>>> &graph,
    const int start)
{
    const std::pair<int, int> init = std::make_pair(start, 26);

    DP.clear();
    const int answer = solve(
        flow_rates,
        graph,
        init,
        init.first,
        init.second,
        set_bit(0, init.first),
        2);

    std::cout << "Part two: " << answer << std::endl;
}

int main()
{
    part_one(flow_rates, graph, start);
    part_two(flow_rates, graph, start);

    return 0;
}
