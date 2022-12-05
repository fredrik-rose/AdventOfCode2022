# Day 5: Supply Stacks
import collections as coll
import copy
import re


def main():
    stacks, instructions = parse("5.txt")
    part_one(copy.deepcopy(stacks), copy.deepcopy(instructions))
    part_two(copy.deepcopy(stacks), copy.deepcopy(instructions))


def parse(file_path):
    stacks = coll.defaultdict(list)
    with open(file_path) as file:
        for line in file:
            if "[" not in line:
                break
            for i, item in enumerate(line[1::4]):
                if item != " ":
                    stacks[i + 1].insert(0, item)
        file.readline()
        instructions = []
        for line in file:
            a, b, c = extract_ints(line)
            instructions.append((a, b, c))
    return stacks, instructions


def extract_ints(text):
    return [int(x) for x in re.findall(r'-?\d+', text)]


def part_one(stacks, instructions):
    for n, src, dst in instructions:
        for _ in range(n):
            stacks[dst].append(stacks[src].pop())
    answer = construct_answer(stacks)
    print(f"Part one: {answer}")


def part_two(stacks, instructions):
    for n, src, dst in instructions:
        temp = []
        for _ in range(n):
            temp.append(stacks[src].pop())
        for _ in range(n):
            stacks[dst].append(temp.pop())
    answer = construct_answer(stacks)
    print(f"Part two: {answer}")


def construct_answer(stacks):
    answer = "".join(stacks[i + 1][-1] for i in range(len(stacks)))
    return answer


if __name__ == "__main__":
    main()
