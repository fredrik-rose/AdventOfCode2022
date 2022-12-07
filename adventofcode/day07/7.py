# Day 7:  No Space Left On Device
import copy


class Node:
    def __init__(self, name):
        self.name = name
        self.children = {}
        self.files = []

    def __repr__(self):
        return f"Node({self.name}, {self.children.keys()}, {self.files})"


def main():
    root = parse("7.txt")
    part_one(copy.deepcopy(root))
    part_two(copy.deepcopy(root))


def parse(file_path):
    path = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            if line.startswith("$ cd .."):
                assert path
                path.pop()
            elif line.startswith("$ cd "):
                name = line.split(" ")[-1]
                current = Node(name)
                if path:
                    path[-1].children[name] = current
                path.append(current)
            elif line.startswith("dir"):
                continue
            elif line.startswith("$ ls"):
                continue
            else:
                assert not line.startswith("$"), line
                size, name = line.split(" ")
                path[-1].files.append((int(size), name))
    return path[0]


def part_one(root):
    sizes = []
    sum_dir_sizes(root, sizes)
    answer = 0
    for size in sizes:
        if size <= 100000:
            answer += size
    print(f"Part one: {answer}")


def part_two(root):
    sizes = []
    free_size = 70000000 - sum_dir_sizes(root, sizes)
    required_size = 30000000 - free_size
    assert required_size > 0
    answer = 1e10
    for size in sizes:
        if size >= required_size:
            answer = min(size, answer)
    print(f"Part two: {answer}")


def sum_dir_sizes(node, output):
    tot_sum = 0
    for size, _ in node.files:
        tot_sum += size
    for child in node.children.values():
        tot_sum += sum_dir_sizes(child, output)
    output.append(tot_sum)
    return tot_sum


if __name__ == "__main__":
    main()
