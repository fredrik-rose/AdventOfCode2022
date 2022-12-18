# Day 18: Boiling Boulders
import collections as coll
import copy
import re


def main():
    cubes = parse("18.txt")
    part_one(copy.deepcopy(cubes))
    part_two(copy.deepcopy(cubes))


def parse(file_path):
    cubes = set()
    with open(file_path) as file:
        for line in file:
            cubes.add(tuple(extract_ints(line)))
    return cubes


def extract_ints(text):
    return [int(x) for x in re.findall(r'-?\d+', text)]


def part_one(cubes):
    faces = 0
    for c in cubes:
        faces += sum(1 for n in neighbors_generator(c) if n not in cubes)
    print(f"Part one: {faces}")


def part_two(cubes):
    faces = flood_fill(cubes)
    print(f"Part two: {faces}")


def neighbors_generator(cube):
    deltas = (
        (0, 0, -1),
        (0, 0, 1),
        (0, -1, 0),
        (0, 1, 0),
        (-1, 0, 0),
        (1, 0, 0)
    )
    for d in deltas:
        neighbor = (cube[0] + d[0], cube[1] + d[1], cube[2] + d[2])
        yield neighbor


def flood_fill(cubes):
    min_x = min(c[0] for c in cubes) - 1
    max_x = max(c[0] for c in cubes) + 1
    min_y = min(c[1] for c in cubes) - 1
    max_y = max(c[1] for c in cubes) + 1
    min_z = min(c[2] for c in cubes) - 1
    max_z = max(c[2] for c in cubes) + 1
    queue = coll.deque()
    visited = set()
    start = (min_x, min_y, min_z)
    queue.append(start)
    visited.add(start)
    counter = 0
    while queue:
        c = queue.popleft()
        for n in neighbors_generator(c):
            if n in visited:
                continue
            if n in cubes:
                counter += 1
                continue
            if min_x <= n[0] <= max_x and min_y <= n[1] <= max_y and min_z <= n[2] <= max_z:
                queue.append(n)
                visited.add(n)
    return counter


if __name__ == "__main__":
    main()
