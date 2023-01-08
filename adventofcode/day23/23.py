# Day 23: Unstable Diffusion
import collections as coll
import copy


def main():
    grid = parse("23.txt")
    part_one(copy.deepcopy(grid))
    part_two(copy.deepcopy(grid))


def parse(file_path):
    grid = set()
    with open(file_path) as file:
        for y, line in enumerate(file):
            for x, item in enumerate(line.strip()):
                if item == "#":
                    grid.add(x + y*1j)
    return grid


def part_one(grid):
    grid, _ = game_of_life(grid, 10)
    answer = count_empty(grid)
    print(f"Part one: {answer}")


def part_two(grid):
    _, steps = game_of_life(grid, 10000)
    print(f"Part two: {steps}")


def game_of_life(grid, steps):
    directions = coll.deque([
        (-1 - 1j, 0 - 1j, 1 - 1j),  # North
        (-1 + 1j, 0 + 1j, 1 + 1j),  # South
        (-1 - 1j, -1 + 0j, -1 + 1j),  # West
        (1 - 1j, 1 + 0j, 1 + 1j),  # East
    ])
    for i in range(steps):
        proposals = {}
        for elf in grid:
            proposals[elf] = elf
            if is_alone(elf, grid):
                continue
            for move in directions:
                if not any(elf + d in grid for d in move):
                    proposals[elf] = elf + move[1]
                    break
        counter = coll.Counter(proposals.values())
        next_grid = set(proposals[elf] if counter[proposals[elf]] == 1 else elf for elf in grid)
        if grid == next_grid:
            break
        grid = next_grid
        directions.rotate(-1)
    return grid, i + 1


def is_alone(elf, grid):
    for y in range(-1, 2):
        for x in range(-1, 2):
            if y == 0 and x == 0:
                continue
            if elf + (x + y*1j) in grid:
                return False
    return True


def count_empty(grid):
    left = int(min(e.real for e in grid))
    right = int(max(e.real for e in grid))
    top = int(min(e.imag for e in grid))
    bottom = int(max(e.imag for e in grid))
    count = 0
    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            if x + y*1j not in grid:
                count += 1
    return count


if __name__ == "__main__":
    main()
