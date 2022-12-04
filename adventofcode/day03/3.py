# Day 3: Rucksack Reorganization


def main():
    packs = parse("3.txt")
    part_one(packs.copy())
    part_two(packs.copy())


def parse(file_path):
    packs = []
    with open(file_path) as file:
        packs = [line.strip() for line in file]
    return packs


def part_one(packs):
    common_items = []
    for pack in packs:
        half = len(pack) // 2
        common = set(pack[:half]).intersection(pack[half:])
        assert len(common) == 1
        common_items.append(list(common)[0])
    priority_sum = get_priority(common_items)
    print(f"Part one: {priority_sum}")


def part_two(packs):
    common_items = []
    for group in (packs[i:i + 3] for i in range(0, len(packs), 3)):
        common = set(group[0]).intersection(*group[1:])
        assert len(common) == 1
        common_items.append(list(common)[0])
    priority_sum = priority_sum = get_priority(common_items)
    print(f"Part two: {priority_sum}")


def get_priority(items):
    priority_sum = 0
    for item in items:
        if item.isupper():
            priority_sum += ord(item) - 38
        else:
            priority_sum += ord(item) - 96
    return priority_sum


if __name__ == "__main__":
    main()
