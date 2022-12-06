# Day 6: Tuning Trouble
import copy


def main():
    stream = parse("6.txt")
    part_one(copy.deepcopy(stream))
    part_two(copy.deepcopy(stream))


def parse(file_path):
    with open(file_path) as file:
        return file.readline().strip()


def part_one(stream):
    answer = find_marker(stream, 4)
    print(f"Part one: {answer}")


def part_two(stream):
    answer = find_marker(stream, 14)
    print(f"Part two: {answer}")


def find_marker(stream, marker_length):
    for i in range(marker_length, len(stream)):
        if len(set(stream[i - marker_length:i])) == marker_length:
            return i
    return -1


if __name__ == "__main__":
    main()
