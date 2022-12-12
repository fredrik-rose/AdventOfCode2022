# Day 12: Hill Climbing Algorithm
import copy
import os
import sys

# pylint: disable=c-extension-no-member
sys.path.append(os.path.join(sys.path[0], '..', 'algorithms'))
import algorithms as algo  # # noqa: E402, pylint: disable=wrong-import-position


def main():
    grid, start, end = parse("12.txt")
    part_one(copy.deepcopy(grid), copy.deepcopy(start), copy.deepcopy(end))
    part_two(copy.deepcopy(grid), copy.deepcopy(end))


def parse(file_path):
    grid = []
    start = None
    end = None
    with open(file_path) as file:
        for y, line in enumerate(file):
            grid.append([])
            line = line.strip()
            for x, element in enumerate(list(line)):
                if element == "S":
                    start = (x, y)
                    element = "a"
                elif element == "E":
                    end = (x, y)
                    element = "z"
                grid[y].append(ord(element) - ord("a"))
    assert start is not None
    assert end is not None
    return grid, start, end


def part_one(grid, start, end):
    path_length = algo.breadth_first_search(grid, start, end, neighbors)
    print(f"Part one: {path_length}")


def part_two(grid, end):
    shortest_path = 1e10
    for y, _ in enumerate(grid):
        for x, __ in enumerate(grid[0]):
            if grid[y][x] == 0:
                distance = algo.breadth_first_search(grid, (x, y), end, neighbors)
                if distance is None:
                    continue
                shortest_path = min(distance, shortest_path)
    print(f"Part two: {shortest_path}")


def neighbors(grid, position):
    delta_x = (-1, 1, 0, 0)
    delta_y = (0, 0, -1, 1)
    x = position[0]
    y = position[1]
    element = grid[y][x]
    for dx, dy in zip(delta_x, delta_y):
        next_x = x + dx
        next_y = y + dy
        if 0 <= next_x < len(grid[0]) and 0 <= next_y < len(grid):
            next_element = grid[next_y][next_x]
            if next_element - element <= 1:
                yield (next_x, next_y)


if __name__ == "__main__":
    main()
