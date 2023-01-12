# Day 11: Monkey in the Middle
import copy
import functools as ftools
import re


class Monkey:
    def __init__(self, monkey_id, items, operation, test, true, false):
        self.monkey_id = monkey_id
        self.items = items
        self.operation = operation
        self.test = test
        self.true = true
        self.false = false

    def __repr__(self):
        return f"Monkey({self.monkey_id}, {self.items}, {self.operation}, {self.test}, {self.true}, {self.false})"


def main():
    monkeys = parse("11.txt")
    part_one(copy.deepcopy(monkeys))
    part_two(copy.deepcopy(monkeys))


def parse(file_path):
    monkeys = []
    with open(file_path) as file:
        text_monkeys = file.read().split("\n\n")
        for i, text in enumerate(text_monkeys):
            monkey = parse_monkey(text)
            assert monkey.monkey_id == i, monkey.monkey_id
            monkeys.append(monkey)
    return monkeys


def parse_monkey(text):
    lines = text.split("\n")
    monkey_id = extract_ints(lines[0])[0]
    items = extract_ints(lines[1])
    # NOTE: This is dangerous!
    operation = lambda old: eval(lines[2].split("= ")[1])  # noqa pylint: disable=eval-used
    test = extract_ints(lines[3])[0]
    true = extract_ints(lines[4])[0]
    false = extract_ints(lines[5])[0]
    return Monkey(monkey_id, items, operation, test, true, false)


def extract_ints(text):
    return [int(x) for x in re.findall(r'-?\d+', text)]


def part_one(monkeys):
    answer = simulate(monkeys, lambda x: x // 3, 20)
    print(f"Part one: {answer}")


def part_two(monkeys):
    # All numbers are prime, no need to divide by the gcd when calculating the lcm.
    least_common_multiple = ftools.reduce(lambda x, y: x * y, [monkey.test for monkey in monkeys])
    answer = simulate(monkeys, lambda x: x % least_common_multiple, 10000)
    print(f"Part two: {answer}")


def simulate(monkeys, update, n):
    activity = [0] * len(monkeys)
    for _ in range(n):
        for monkey in monkeys:
            activity[monkey.monkey_id] += len(monkey.items)
            for item in monkey.items:
                new = monkey.operation(item)
                new = update(new)
                next_monkey = monkey.true if new % monkey.test == 0 else monkey.false
                monkeys[next_monkey].items.append(new)
            monkey.items = []
    activity = sorted(activity)
    return activity[-1] * activity[-2]


if __name__ == "__main__":
    main()
