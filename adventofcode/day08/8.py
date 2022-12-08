# Day 8: Treetop Tree House
import copy

import numpy as np


def main():
    forest = parse("8.txt")
    part_one(copy.deepcopy(forest))
    part_two(copy.deepcopy(forest))


def parse(file_path):
    forest = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            forest.append([int(e) for e in list(line)])
    return np.array(forest)


def part_one(forest):
    left = left_sight(forest)
    right = np.fliplr(left_sight(np.fliplr(forest)))
    top = top_sight(forest)
    bottom = np.flipud(top_sight(np.flipud(forest)))
    seen = np.logical_or(np.logical_or(left, right), np.logical_or(top, bottom))
    answer = np.sum(seen)
    print(f"Part one: {answer}")


def left_sight(forest):
    output = np.zeros(forest.shape)
    for y in range(forest.shape[0]):
        max_value = -1
        for x in range(forest.shape[1]):
            if forest[y, x] > max_value:
                output[y, x] = 1
                max_value = forest[y, x]
    return output


def top_sight(forest):
    output = np.zeros(forest.shape)
    for x in range(forest.shape[1]):
        max_value = -1
        for y in range(forest.shape[1]):
            if forest[y, x] > max_value:
                output[y, x] = 1
                max_value = forest[y, x]
    return output


def part_two(forest):
    max_score = -1
    for y in range(forest.shape[0]):
        for x in range(forest.shape[1]):
            score = get_scenic_score(forest, y, x)
            max_score = max(score, max_score)
    print(f"Part two: {max_score}")


def get_scenic_score(forest, y, x):
    scenic_score = 1
    dy = [0, 1, 0, -1]
    dx = [-1, 0, 1, 0]
    for dy, dx in zip(dy, dx):
        col = x + dx
        row = y + dy
        sight = 0
        while 0 <= col < forest.shape[1] and 0 <= row < forest.shape[0]:
            sight += 1
            if forest[row, col] >= forest[y, x]:
                break
            col += dx
            row += dy
        scenic_score *= sight
    return scenic_score


if __name__ == "__main__":
    main()
