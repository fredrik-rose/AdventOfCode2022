# Day 13: Distress Signal
import ast
import copy


def main():
    pairs = parse("13.txt")
    part_one(copy.deepcopy(pairs))
    part_two(copy.deepcopy(pairs))


def parse(file_path):
    pairs = []
    with open(file_path) as file:
        data = file.read().split("\n\n")
        for pair in data:
            pair = pair.split("\n")
            # NOTE: Using eval is dangerous!
            left = ast.literal_eval(pair[0].strip())
            right = ast.literal_eval(pair[1].strip())
            pairs.append((left, right))
    return pairs


def part_one(pairs):
    valid_sum = 0
    for i, (left, right) in enumerate(pairs):
        if compare(left, right):
            valid_sum += i + 1
    print(f"Part one: {valid_sum}")


def part_two(pairs):
    packets = [packet for pair in pairs for packet in pair]
    first_position = find_sorted_position([[2]], packets)
    second_position = find_sorted_position([[6]], packets)
    answer = (first_position + 1) * (second_position + 2)
    print(f"Part two: {answer}")


def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return None if a == b else a < b
    elif isinstance(a, int):
        assert isinstance(b, list)
        return compare([a], b)
    elif isinstance(b, int):
        assert isinstance(a, list)
        return compare(a, [b])
    else:
        assert isinstance(a, list) and isinstance(b, list)
        for x, y in zip(a, b):
            result = compare(x, y)
            if result is None:
                continue
            return result
        return None if len(a) == len(b) else len(a) < len(b)


def find_sorted_position(packet, packets):
    return sum(1 for other in packets if compare(other, packet))


if __name__ == "__main__":
    main()
