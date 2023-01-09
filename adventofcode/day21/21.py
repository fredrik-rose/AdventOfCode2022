# Day 21: Monkey Math
import copy
import os
import sys

# pylint: disable=c-extension-no-member
sys.path.append(os.path.join(sys.path[0], '..', 'algorithms'))
import algorithms as algo  # # noqa: E402, pylint: disable=wrong-import-position


class MonkeyError(Exception):
    pass


def main():
    monkeys = parse("21.txt")
    part_one(copy.deepcopy(monkeys))
    part_two(copy.deepcopy(monkeys))


def parse(file_path):
    monkeys = {}
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            monkey, expression = line.split(": ")
            parts = expression.split(" ")
            if len(parts) == 1:
                monkeys[monkey] = int(parts[0])
            else:
                assert len(parts) == 3
                monkeys[monkey] = (parts[1], parts[0], parts[2])  # (operator, operand_1, operand_2)
    return monkeys


def part_one(monkeys):
    answer = int(monkey_eval("root", monkeys))
    print(f"Part one: {answer}")


def part_two(monkeys):
    monkeys["humn"] = None
    monkeys["root"] = ("-", ) + monkeys["root"][1:]
    answer = monkey_match("root", 0, monkeys)
    assert algo.newtons_method(get_f("root", monkeys), 0, 1000) == answer
    print(f"Part two: {int(answer)}")


def monkey_eval(expression, env):
    if expression is None:
        raise MonkeyError()
    if isinstance(expression, (int, float)):
        return expression
    if isinstance(expression, str):
        return monkey_eval(env[expression], env)
    assert len(expression) == 3
    operator, operand_a, operand_b = expression
    left = monkey_eval(operand_a, env)
    right = monkey_eval(operand_b, env)
    return monkey_apply(operator, left, right)


def monkey_apply(operator, operand_a, operand_b):
    if operator == "+":
        return operand_a + operand_b
    if operator == "-":
        return operand_a - operand_b
    if operator == "*":
        return operand_a * operand_b
    if operator == "/":
        return operand_a / operand_b
    assert False


def monkey_match(expression, match, env):
    if expression is None:
        return match
    if isinstance(expression, str):
        return monkey_match(env[expression], match, env)
    assert not isinstance(expression, int)
    assert len(expression) == 3
    operator, operand_a, operand_b = expression
    left = monkey_match_left(operator, operand_a, operand_b, match, env)
    right = monkey_match_right(operator, operand_a, operand_b, match, env)
    return left or right


def monkey_match_right(operator, operand_a, operand_b, match, env):
    try:
        left = monkey_eval(operand_a, env)
    except MonkeyError:
        return None
    if operator == "+":
        match = match - left
    if operator == "-":
        match = left - match
    if operator == "*":
        match = match // left
    if operator == "/":
        match = left // match
    return monkey_match(operand_b, match, env)


def monkey_match_left(operator, operand_a, operand_b, match, env):
    try:
        right = monkey_eval(operand_b, env)
    except MonkeyError:
        return None
    if operator == "+":
        match = match - right
    if operator == "-":
        match = match + right
    if operator == "*":
        match = match // right
    if operator == "/":
        match = match * right
    return monkey_match(operand_a, match, env)


def get_f(expression, monkeys):
    def f(x):
        monkeys["humn"] = x
        return monkey_eval(expression, monkeys)

    return f


if __name__ == "__main__":
    main()
