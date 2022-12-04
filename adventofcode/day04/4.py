# Day 4: Camp Cleanup


def main():
    pairs = parse("4.txt")
    part_one(pairs.copy())
    part_two(pairs.copy())


def parse(file):
    pairs = []
    with open(file) as file:
        for line in file:
            pair = line.strip().split(",")
            assert len(pair) == 2
            first = [int(e) for e in pair[0].split("-")]
            second = [int(e) for e in pair[1].split("-")]
            pairs.append((first, second))
    return pairs


def part_one(pairs):
    contained = 0
    for first, second in pairs:
        if first[0] >= second[0] and first[1] <= second[1]:
            contained += 1
        elif second[0] >= first[0] and second[1] <= first[1]:
            contained += 1
    print(f"Part one: {contained}")


def part_two(pairs):
    overlap = 0
    for first, second in pairs:
        if first[1] >= second[0] and first[0] <= second[1]:
            overlap += 1
    print(f"Part two: {overlap}")


if __name__ == "__main__":
    main()
