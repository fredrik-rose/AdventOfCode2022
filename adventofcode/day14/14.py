# Day 14: Regolith Reservoir
import copy


def main():
    positions = parse("14.txt")
    part_one(copy.deepcopy(positions))
    part_two(copy.deepcopy(positions))


def parse(file_path):
    rocks = set()
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            rocks = rocks.union(parse_lines(line))
    return rocks


def parse_lines(text):
    segments = text.split(" -> ")
    rocks = set()
    for start, end in zip(segments[:-1], segments[1:]):
        rocks = rocks.union(parse_segment(start, end))
    return rocks


def parse_segment(start_text, end_text):
    start = parse_coordinate(start_text)
    end = parse_coordinate(end_text)
    difference = end - start
    step = sign(difference.real) + sign(difference.imag) * 1j
    position = start
    rocks = set([start])
    while position != end:
        position += step
        rocks.add(position)
    return rocks


def parse_coordinate(text):
    x, y = (int(e) for e in text.split(","))
    return int(x) + int(y) * 1j


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def part_one(rocks):
    answer = simulate(rocks)
    print(f"Part one: {answer}")


def part_two(rocks):
    max_rock = get_max_rock(rocks)
    for x in range(-1000, 1000, 1):
        rocks.add((500 + x) + (max_rock.imag + 2) * 1j)
    answer = simulate(rocks)
    print(f"Part two: {answer}")


def simulate(rocks):
    max_rock = get_max_rock(rocks)
    desert = rocks
    count = 0
    while simulate_sand(desert, max_rock):
        count += 1
    return count


def simulate_sand(desert, max_rock):
    sand = 500 + 0j
    if sand in desert:
        return False
    while sand.imag <= max_rock.imag:
        for step in (0 + 1j, -1 + 1j, 1 + 1j):
            next_sand = sand + step
            if next_sand not in desert:
                sand = next_sand
                break
        else:
            desert.add(sand)
            return True
    return False


def get_max_rock(rocks):
    max_rock = max(rocks, key=lambda x: x.imag)
    return max_rock


if __name__ == "__main__":
    main()
