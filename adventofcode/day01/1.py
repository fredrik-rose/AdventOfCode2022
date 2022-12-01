# Day 1: Calorie Counting


def parse(file):
    elves = []
    with open(file) as file:
        num_calories = 0
        for line in file:
            line = line.strip()
            if not line:
                elves.append(num_calories)
                num_calories = 0
            else:
                num_calories += int(line)
    return elves


def part_one(elves):
    answer = max(elves)
    print(f"Part one: {answer}")


def part_two(elves):
    answer = sum(sorted(elves)[-3:])
    print(f"Part two: {answer}")


def main():
    elves = parse("1.txt")
    part_one(elves.copy())
    part_two(elves.copy())


if __name__ == "__main__":
    main()
