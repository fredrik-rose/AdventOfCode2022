# Day 25: Full of Hot Air
import copy


BASE = 5


def main():
    numbers = parse("25.txt")
    part_one(copy.deepcopy(numbers))


def parse(file_path):
    with open(file_path) as file:
        numbers = [line.strip() for line in file]
    return numbers


def part_one(numbers):
    fuel = sum(snafu_to_decimal(n) for n in numbers)
    answer = decimal_to_snafu(fuel)
    print(f"Part one: {answer}")


def snafu_to_decimal(snafu):
    assert BASE == 5
    lut = {
        "2": 2,
        "1": 1,
        "0": 0,
        "-": -1,
        "=": -2
    }
    decimal = 0
    for i, digit in enumerate(snafu[::-1]):
        decimal += (BASE ** i) * lut[digit]
    return decimal


def decimal_to_snafu(decimal):
    assert BASE == 5
    lut = {
        0: "0",
        1: "1",
        2: "2",
        3: "=",
        4: "-"
    }
    snafu = []
    number = decimal
    while number > 0:
        digit = number % BASE
        if digit > BASE // 2:  # This would not be needed for an unbalanced (i.e. "normal") base 5.
            number += (BASE - digit)
        number = number // BASE
        snafu.append(lut[digit])
    return "".join(snafu[::-1])


if __name__ == "__main__":
    main()
