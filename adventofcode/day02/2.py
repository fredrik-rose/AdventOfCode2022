# Day 2: Rock Paper Scissors


def main():
    rounds = parse("2.txt")
    part_one(rounds.copy())
    part_two(rounds.copy())


def parse(file):
    rounds = []
    with open(file) as file:
        for line in file:
            line = line.strip()
            opponent, my = line.split(" ")
            rounds.append((opponent, my))
    return rounds


def part_one(rounds):
    selection = {"X": 1, "Y": 2, "Z": 3}
    outcome = {
        ("A", "X"): 3,
        ("A", "Y"): 6,
        ("A", "Z"): 0,
        ("B", "X"): 0,
        ("B", "Y"): 3,
        ("B", "Z"): 6,
        ("C", "X"): 6,
        ("C", "Y"): 0,
        ("C", "Z"): 3,
    }
    points = play(rounds, selection, outcome)
    print(f"Part one: {points}")


def part_two(rounds):
    selection = {"X": 0, "Y": 3, "Z": 6}
    outcome = {
        ("A", "X"): 3,
        ("A", "Y"): 1,
        ("A", "Z"): 2,
        ("B", "X"): 1,
        ("B", "Y"): 2,
        ("B", "Z"): 3,
        ("C", "X"): 2,
        ("C", "Y"): 3,
        ("C", "Z"): 1,
    }
    points = play(rounds, selection, outcome)
    print(f"Part two: {points}")


def play(rounds, selection_strategy, outcome_strategy):
    points = sum(selection_strategy[play[1]] + outcome_strategy[play] for play in rounds)
    return points


if __name__ == "__main__":
    main()
