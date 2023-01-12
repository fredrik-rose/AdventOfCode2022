# Day 22: Monkey Map
import copy
import re


SIZE = 50
FRONT_FACE = 4
LEFT_FACE = 3
RIGHT_FACE = 1
BACK_FACE = 0
TOP_FACE = 2
BOTTOM_FACE = 5
RIGHT = 1 + 0j
DOWN = 0 + 1j
LEFT = -1 + 0j
UP = 0 + -1j


def main():
    faces, path = parse("22.txt")
    part_one(copy.deepcopy(faces), copy.deepcopy(path))
    part_two(copy.deepcopy(faces), copy.deepcopy(path))


def parse(file_path):
    grid = []
    with open(file_path) as file:
        for line in file:
            grid.append(list(line.rstrip()))
    index = 0
    faces = {}
    for y in range(0, len(grid), SIZE):
        for x in range(0, len(grid[y]), SIZE):
            if grid[y][x] != " ":
                side = []
                for i in range(SIZE):
                    side.append(grid[y + i][x:x + SIZE])
                faces[index] = ((x + y*1j), side)
                index += 1
    path = extract_path("".join(grid[-1]))
    return faces, path


def extract_path(text):
    return [x if x in ("L", "R") else int(x) for x in re.findall(r'-?\d+|R|L', text)]


def part_one(faces, path):
    position, direction = walk(faces, path, get_next_position_on_board)
    answer = get_password(position, direction)
    print(f"Part one: {answer}")


def part_two(faces, path):
    position, direction = walk(faces, path, get_next_position_on_cube)
    answer = get_password(position, direction)
    print(f"Part two: {answer}")


def walk(faces, path, get_next_position):
    face = 0
    position = 0 + 0j
    direction = RIGHT
    for step in path:
        assert get_tile(faces, face, position) == "."
        if step == "R":
            direction = rotate_clockwise(direction)
        elif step == "L":
            direction = rotate_counter_clockwise(direction)
        else:
            assert isinstance(step, int)
            for _ in range(step):
                next_face, next_position, next_direction = get_next_position(face, position, direction)
                if get_tile(faces, next_face, next_position) == "#":
                    break
                face, position, direction = next_face, next_position, next_direction
    final_position = get_absolute_position(faces, face, position)
    return final_position, direction


def rotate_clockwise(direction):
    return direction * 1j


def rotate_counter_clockwise(direction):
    return direction * -1j


def get_tile(faces, face, position):
    return faces[face][1][int(position.imag)][int(position.real)]


def get_absolute_position(faces, face, position):
    return faces[face][0] + position


def get_password(position, direction):
    direction_to_password = {
        RIGHT: 0,
        DOWN: 1,
        LEFT: 2,
        UP: 3,
    }
    return int(1000 * (position.imag + 1) + 4 * (position.real + 1) + direction_to_password[direction])


def get_next_position_on_board(face, position, direction):  # noqa: C901 pylint: disable=R0912, R0915
    next_position = position + direction
    next_face = face
    next_direction = direction
    if is_position_valid(next_position):
        pass
    elif face == BACK_FACE:
        if right_border(next_position):
            next_face = RIGHT_FACE
        elif left_border(next_position):
            next_face = RIGHT_FACE
        elif top_border(next_position):
            next_face = FRONT_FACE
        elif bottom_border(next_position):
            next_face = TOP_FACE
        else:
            assert False
    elif face == RIGHT_FACE:
        if right_border(next_position):
            next_face = BACK_FACE
        elif left_border(next_position):
            next_face = BACK_FACE
        elif top_border(next_position):
            next_face = RIGHT_FACE
        elif bottom_border(next_position):
            next_face = RIGHT_FACE
        else:
            assert False
    elif face == TOP_FACE:
        if right_border(next_position):
            next_face = TOP_FACE
        elif left_border(next_position):
            next_face = TOP_FACE
        elif top_border(next_position):
            next_face = BACK_FACE
        elif bottom_border(next_position):
            next_face = FRONT_FACE
        else:
            assert False
    elif face == LEFT_FACE:
        if right_border(next_position):
            next_face = FRONT_FACE
        elif left_border(next_position):
            next_face = FRONT_FACE
        elif top_border(next_position):
            next_face = BOTTOM_FACE
        elif bottom_border(next_position):
            next_face = BOTTOM_FACE
        else:
            assert False
    elif face == FRONT_FACE:
        if right_border(next_position):
            next_face = LEFT_FACE
        elif left_border(next_position):
            next_face = LEFT_FACE
        elif top_border(next_position):
            next_face = TOP_FACE
        elif bottom_border(next_position):
            next_face = BACK_FACE
        else:
            assert False
    elif face == BOTTOM_FACE:
        if right_border(next_position):
            next_face = BOTTOM_FACE
        elif left_border(next_position):
            next_face = BOTTOM_FACE
        elif top_border(next_position):
            next_face = LEFT_FACE
        elif bottom_border(next_position):
            next_face = LEFT_FACE
        else:
            assert False
    else:
        assert False
    next_position = (next_position.real % SIZE) + (next_position.imag % SIZE)*1j
    return next_face, next_position, next_direction


def get_next_position_on_cube(face, position, direction):  # noqa: C901 pylint: disable=R0912, R0915
    next_position = position + direction
    end = SIZE - 1
    real = position.real
    imag = position.imag
    inv_imag = end - position.imag
    if is_position_valid(next_position):
        next_face = face
        next_direction = direction
    elif face == BACK_FACE:
        if right_border(next_position):
            next_face = RIGHT_FACE
            next_position = 0 + imag*1j
            next_direction = RIGHT
        elif left_border(next_position):
            next_face = LEFT_FACE
            next_position = 0 + inv_imag*1j
            next_direction = RIGHT
        elif top_border(next_position):
            next_face = BOTTOM_FACE
            next_position = 0 + real*1j
            next_direction = RIGHT
        elif bottom_border(next_position):
            next_face = TOP_FACE
            next_position = real + 0j
            next_direction = DOWN
        else:
            assert False
    elif face == RIGHT_FACE:
        if right_border(next_position):
            next_face = FRONT_FACE
            next_position = end + inv_imag*1j
            next_direction = LEFT
        elif left_border(next_position):
            next_face = BACK_FACE
            next_position = end + imag*1j
            next_direction = LEFT
        elif top_border(next_position):
            next_face = BOTTOM_FACE
            next_position = real + end*1j
            next_direction = UP
        elif bottom_border(next_position):
            next_face = TOP_FACE
            next_position = end + real*1j
            next_direction = LEFT
        else:
            assert False
    elif face == TOP_FACE:
        if right_border(next_position):
            next_face = RIGHT_FACE
            next_position = imag + end*1j
            next_direction = UP
        elif left_border(next_position):
            next_face = LEFT_FACE
            next_position = imag + 0j
            next_direction = DOWN
        elif top_border(next_position):
            next_face = BACK_FACE
            next_position = real + end*1j
            next_direction = UP
        elif bottom_border(next_position):
            next_face = FRONT_FACE
            next_position = real + 0j
            next_direction = DOWN
        else:
            assert False
    elif face == LEFT_FACE:
        if right_border(next_position):
            next_face = FRONT_FACE
            next_position = 0 + imag*1j
            next_direction = RIGHT
        elif left_border(next_position):
            next_face = BACK_FACE
            next_position = 0 + inv_imag*1j
            next_direction = RIGHT
        elif top_border(next_position):
            next_face = TOP_FACE
            next_position = 0 + real*1j
            next_direction = RIGHT
        elif bottom_border(next_position):
            next_face = BOTTOM_FACE
            next_position = real + 0j
            next_direction = DOWN
        else:
            assert False
    elif face == FRONT_FACE:
        if right_border(next_position):
            next_face = RIGHT_FACE
            next_position = end + inv_imag*1j
            next_direction = LEFT
        elif left_border(next_position):
            next_face = LEFT_FACE
            next_position = end + imag*1j
            next_direction = LEFT
        elif top_border(next_position):
            next_face = TOP_FACE
            next_position = real + end*1j
            next_direction = UP
        elif bottom_border(next_position):
            next_face = BOTTOM_FACE
            next_position = end + real*1j
            next_direction = LEFT
        else:
            assert False
    elif face == BOTTOM_FACE:
        if right_border(next_position):
            next_face = FRONT_FACE
            next_position = imag + end*1j
            next_direction = UP
        elif left_border(next_position):
            next_face = BACK_FACE
            next_position = imag + 0j
            next_direction = DOWN
        elif top_border(next_position):
            next_face = LEFT_FACE
            next_position = real + end*1j
            next_direction = UP
        elif bottom_border(next_position):
            next_face = RIGHT_FACE
            next_position = real + 0j
            next_direction = DOWN
        else:
            assert False
    else:
        assert False
    return next_face, next_position, next_direction


def is_position_valid(position):
    return 0 <= position.real < SIZE and 0 <= position.imag < SIZE


def right_border(position):
    return position.real >= SIZE


def left_border(position):
    return position.real < 0


def top_border(position):
    return position.imag < 0


def bottom_border(position):
    return position.imag >= SIZE


if __name__ == "__main__":
    main()
