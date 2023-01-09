# Day 24: Blizzard Basin
import copy
import heapq


class Board:
    def __init__(self, positions, directions, width, height):
        self.positions = positions
        self.directions = directions
        self.width = width
        self.height = height
        self._memory = {}

    def reset(self, positions):
        self.positions = positions
        self._memory = {}

    def get_positions_at_time(self, time):
        if time in self._memory:
            return self._memory[time]
        if time == 0:
            positions = self.positions
        else:
            positions = self.time_step(self.get_positions_at_time(time - 1))
        self._memory[time] = positions
        return self._memory[time]

    def time_step(self, positions):
        assert len(positions) == len(self.directions)
        new_positions = []
        for pos, delta in zip(positions, self.directions):
            next_position = pos + delta
            next_position = (next_position.real % self.width) + (next_position.imag % self.height) * 1j
            new_positions.append(next_position)
        return new_positions


def main():
    board, start, end = parse("24.txt")
    part_one(copy.deepcopy(board), start, end)
    part_two(copy.deepcopy(board), start, end)


def parse(file_path):
    char_to_direction = {
        ">": 1 + 0j,
        "v": 0 + 1j,
        "<": -1 + 0j,
        "^": 0 - 1j,
    }
    positions = []
    directions = []
    with open(file_path) as file:
        lines = file.read().splitlines()
        start = lines[0].index(".") - 1 - 1j
        end = lines[-1].index(".") - 1 + (len(lines) - 2) * 1j
        for y, line in enumerate(lines[1:-1]):
            for x, char in enumerate(line[1:-1]):
                if char == ".":
                    continue
                positions.append(x + y*1j)
                directions.append(char_to_direction[char])
        height = len(lines) - 2
        width = len(lines[0]) - 2
    return Board(positions, directions, width, height), start, end


def part_one(board, start, end):
    answer = unweighted_a_star(board, start, end)
    print(f"Part one: {answer}")


def part_two(board, start, end):
    a = unweighted_a_star(board, start, end)
    board.reset(board.get_positions_at_time(a))
    b = unweighted_a_star(board, end, start)
    board.reset(board.get_positions_at_time(b))
    c = unweighted_a_star(board, start, end)
    print(f"Part two: {a + b + c}")


def unweighted_a_star(graph, start, end):
    queue = []
    visited = set()
    # The purpose of the counter is to avoid comparing data elements in the priority queue for cases
    # with equal priority. By having (priority, counter) as first member of the tuple the
    # following data elements will never be used in the comparison as (priority, counter) is
    # guaranteed to be unique.
    priority_counter = 0
    heapq.heappush(queue, ((0, priority_counter), start, 0))
    priority_counter += 1
    visited.add((start, 0))
    while queue:
        _, node, steps = heapq.heappop(queue)
        if node == end:
            return steps
        for neighbor in neighbors_generator(graph, node, steps, end):
            state = (neighbor, steps + 1)
            if state in visited:
                continue
            priority = steps + 1 + heuristic(neighbor, end)
            heapq.heappush(queue, ((priority, priority_counter), neighbor, steps + 1))
            priority_counter += 1
            visited.add(state)
    assert False


def neighbors_generator(graph, node, steps, end):
    next_blizzards = set(graph.get_positions_at_time(steps + 1))
    for direction in (1 + 0j, 0 + 1j, -1 + 0j, 0 - 1j):
        next_node = node + direction
        if next_node in next_blizzards:
            continue
        if next_node == end or (0 <= next_node.real < graph.width and 0 <= next_node.imag < graph.height):
            yield next_node
    if node not in next_blizzards:
        yield node


def heuristic(position, end):
    return abs(position.real - end.real) + abs(position.imag - end.imag)


if __name__ == "__main__":
    main()
