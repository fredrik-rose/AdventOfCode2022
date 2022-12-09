# Day 9: Rope Bridge
import copy


def main():
    motions = parse("9.txt")
    part_one(copy.deepcopy(motions))
    part_two(copy.deepcopy(motions))


def parse(file_path):
    direction_to_motion = {
        "L": 1 + 0j,
        "R": -1 + 0j,
        "U": 0 - 1j,
        "D": 0 + 1j,
    }
    motions = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            direction, steps = line.split(" ")
            motions.append((direction_to_motion[direction], int(steps)))
    return motions


def part_one(motions):
    answer = simulate(motions, 2)
    print(f"Part one: {answer}")


def part_two(motions):
    answer = simulate(motions, 10)
    print(f"Part two: {answer}")


def simulate(motions, number_of_knots):
    knots = [0 + 0j] * number_of_knots
    visited = set([knots[-1]])
    for direction, steps in motions:
        for _ in range(steps):
            knots[0] += direction
            for i in range(1, len(knots)):
                knots[i] = move_tail(knots[i - 1], knots[i])
            visited.add(knots[-1])
    return len(visited)


def move_tail(head, tail):
    difference = head - tail
    if abs(difference) >= 2:
        tail += sign(difference.real) + sign(difference.imag) * 1j
    return tail


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


if __name__ == "__main__":
    main()
