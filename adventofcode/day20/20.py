# Day 20: Grove Positioning System
import copy
import os
import sys

# pylint: disable=c-extension-no-member
sys.path.append(os.path.join(sys.path[0], '..', 'algorithms'))
import algorithms as algo  # # noqa: E402, pylint: disable=wrong-import-position


def main():
    data = parse("20.txt")
    part_one(copy.deepcopy(data))
    part_two(copy.deepcopy(data))


def parse(file_path):
    data = []
    with open(file_path) as file:
        data = [int(line) for line in file]
    return data


def part_one(data):
    node = mix(data, 1)
    answer = get_answer(node)
    print(f"Part one: {answer}")


def part_two(data):
    data = [n * 811589153 for n in data]
    node = mix(data, 10)
    answer = get_answer(node)
    print(f"Part two: {answer}")


def mix(data, steps):
    node = algo.create_circular_doubly_linked_list(data)
    pointers = get_node_pointers(node)
    for _ in range(steps):
        for p in pointers:
            steps = p.value % (len(pointers) - 1) if p.value >= 0 else -((-p.value) % (len(pointers) - 1))
            move(p, steps)
    return node


def get_node_pointers(node):
    pointers = [node]
    while True:
        node = pointers[-1].right
        if node == pointers[0]:
            break
        pointers.append(node)
    return pointers


def move(node, steps):
    this = node
    if steps == 0:
        return
    if steps > 0:
        for _ in range(steps):
            node = node.right
    elif steps < 0:
        for _ in range(-steps + 1):
            node = node.left
    this.remove()
    node.insert_right(this)


def get_answer(node):
    node = find(node, 0)
    assert node is not None
    answer = 0
    for _ in range(3):
        for i in range(1000):
            node = node.right
        answer += node.value
    return answer


def find(node, value):
    first = node
    while True:
        if node.value == value:
            return node
        right = node.right
        if right is None or right == first:
            break
        node = right
    return None


if __name__ == "__main__":
    main()
