# Day 10: Cathode-Ray Tube
import copy


def main():
    instructions = parse("10.txt")
    part_one(copy.deepcopy(instructions))
    part_two(copy.deepcopy(instructions))


def parse(file_path):
    instructions = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            if line.startswith("noop"):
                instructions.append((line, 0))
            elif line.startswith("addx"):
                operator, operand = line.strip().split(" ")
                instructions.append((operator, int(operand)))
            else:
                assert False, line
    return instructions


def part_one(instructions):
    cpu = cpu_tick(instructions)
    answer = 0
    for i, register in enumerate(cpu):
        cycle = i + 1
        if cycle in (20, 60, 100, 140, 180, 220):
            answer += cycle * register
    print(f"Part one: {answer}")


def part_two(instructions):
    cpu = cpu_tick(instructions)
    crt = crt_tick(40, 60)
    print("Part two:")
    for register, x in zip(cpu, crt):
        if x == 0:
            print("")
        output = "#" if x - 1 <= register <= x + 1 else " "
        print(output, end="")
    print("")


def cpu_tick(instructions):
    register = 1
    for operator, operand in instructions:
        if operator == "noop":
            yield register
        elif operator == "addx":
            yield register
            yield register
            register += operand
        else:
            assert False, operator


def crt_tick(width, height):
    for _ in range(height):
        for x in range(width):
            yield x


if __name__ == "__main__":
    main()
