# Day 17: Pyroclastic Flow
import copy


def main():
    pattern = parse("17.txt")
    part_one(copy.deepcopy(pattern))
    part_two(copy.deepcopy(pattern))


def parse(file_path):
    with open(file_path) as file:
        return file.readline().strip()


def part_one(pattern):
    answer = simulate(pattern, 2022, 2022)
    print(f"Part one: {answer}")


def part_two(pattern):
    answer = simulate(pattern, 1000000000000, 50)
    print(f"Part two: {answer}")


def simulate(pattern, time, height_for_sate):
    directions = direction_generator(pattern)
    sprites = sprite_generator()
    board = set()
    top = 0
    rocks = 0
    visited = {}
    height_of_cycle = 0
    while rocks < time:
        sprite, sprite_index = next(sprites)
        sprite = translate(sprite, 2 + (top + 4) * 1j)
        while True:
            direction, direction_index = next(directions)
            sprite = translate(sprite, direction)
            if collision(sprite, board):
                sprite = translate(sprite, -direction)
            sprite = translate(sprite, 0 - 1j)
            if collision(sprite, board):
                sprite = translate(sprite, 0 + 1j)
                add_to_board(sprite, board)
                break
        top = top_of_board(board)
        rocks += 1
        # Check for cycle.
        if top >= height_for_sate:
            state = (direction_index, sprite_index, get_board_state(board, height_for_sate))
            if state in visited:
                previous_time, previous_top = visited[state]
                delta_rocks = rocks - previous_time
                delta_top = top - previous_top
                steps = (time - rocks) // delta_rocks
                rocks += steps * delta_rocks
                height_of_cycle += steps * delta_top
                assert rocks <= time
            visited[state] = (rocks, top)
    output = int(top + height_of_cycle)
    # print_board(board)
    return output


def direction_generator(pattern):
    while True:
        for i, p in enumerate(pattern):
            yield (-1, i) if p == "<" else (1, i)


def sprite_generator():
    h_line = [0 + 0j, 1 + 0j, 2 + 0j, 3 + 0j]
    v_line = [0 + 0j, 0 + 1j, 0 + 2j, 0 + 3j]
    l_shape = [2 + 2j, 2 + 1j, 0 + 0j, 1 + 0j, 2 + 0j]
    box = [0 + 0j, 0 + 1j, 1 + 0j, 1 + 1j]
    cross = [1 + 0j, 0 + 1j, 1 + 1j, 2 + 1j, 1 + 2j]
    while True:
        for i, sprite in enumerate((h_line, cross, l_shape, v_line, box)):
            yield (sprite, i)


def translate(sprite, translation):
    return [c + translation for c in sprite]


def collision(sprite, board):
    board_collision = any(c in board for c in sprite)
    left_collision = any(c.real < 0 for c in sprite)
    right_collision = any(c.real > 6 for c in sprite)
    bottom_collision = any(c.imag <= 0 for c in sprite)
    return board_collision or left_collision or right_collision or bottom_collision


def add_to_board(sprite, board):
    assert not board.intersection(sprite)
    board.update(sprite)


def top_of_board(board):
    return max(c.imag for c in board)


def get_board_state(board, height):
    top = top_of_board(board)
    return frozenset(c.real + (top - c.imag) * 1j for c in board if c.imag > top - height)


def print_board(board):
    top = int(top_of_board(board))
    for y in range(top + 1, 0, -1):
        line = []
        for x in range(7):
            if x + y*1j in board:
                line.append("#")
            else:
                line.append(" ")
        print(f"|{''.join(line)}|")
    print("+-------+")


if __name__ == "__main__":
    main()
