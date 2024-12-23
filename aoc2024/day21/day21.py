from functools import cache, reduce
from icecream import ic
from enum import IntEnum

from typing import Any

type Grid = dict[Pos, int]
type Pos = tuple[int, int]
type DigitCode = tuple[Digit, Digit, Digit, Digit]
# from typing import NewType
# Pos = NewType("Pos", tuple[int, int])
# Grid = NewType("Grid", dict[Pos, str])
# DigitCode = NewType("DigitCode", tuple[Digit, Digit, Digit, Digit])


class Direction(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3
    ACTIVATE = 666
    NONE = -1

    def right(self):
        return Direction((self + 1) % 4)

    def left(self):
        return Direction((self - 1) % 4)

    def as_str(self):
        return {
            Direction.RIGHT: ">",
            Direction.DOWN: "v",
            Direction.LEFT: "<",
            Direction.UP: "^",
            Direction.ACTIVATE: "A",
        }[self]


# def direction_to_from(current: Pos, next: Pos) -> Direction:
#     nx, ny = next  
#     cx, cy = current

#     assert abs(nx - cx) + abs(ny - cy) == 1

#     if nx == cx:
#         if ny < cy:
#             return Direction.UP
#         else:
#             return Direction.DOWN
#     else:
#         if nx < cx:
#             return Direction.LEFT
#         else:
#             return Direction.RIGHT


# assert direction_to_from((0, 0), (0, 1)) == Direction.DOWN
# assert direction_to_from((0, 0), (1, 0)) == Direction.RIGHT
# assert direction_to_from((0, 1), (0, 0)) == Direction.UP
# assert direction_to_from((1, 0), (0, 0)) == Direction.LEFT 



class Digit(IntEnum):
    NONE = -1
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    ACTIVATE = 66

    def as_str(self):
        return {
            Digit.ZERO: "0",
            Digit.ONE: "1",
            Digit.TWO: "2",
            Digit.THREE: "3",
            Digit.FOUR: "4",
            Digit.FIVE: "5",
            Digit.SIX: "6",
            Digit.SEVEN: "7",
            Digit.EIGHT: "8",
            Digit.NINE: "9",
            Digit.ACTIVATE: "A",
        }[self]

    @staticmethod
    def from_str(s: str):# -> Digit:
        return {
            "0": Digit.ZERO,
            "1": Digit.ONE,
            "2": Digit.TWO,
            "3": Digit.THREE,
            "4": Digit.FOUR,
            "5": Digit.FIVE,
            "6": Digit.SIX,
            "7": Digit.SEVEN,
            "8": Digit.EIGHT,
            "9": Digit.NINE,
            "A": Digit.ACTIVATE,
        }[s]


def read_data(filename: str) -> list[DigitCode]:
    unlock_codes = []
    with open(filename, "r") as data_file:
        for line in data_file:
            a,b,c,d = line.strip()
            a = Digit.from_str(a)
            b = Digit.from_str(b)
            c = Digit.from_str(c)
            d = Digit.ACTIVATE
            unlock_codes.append([a,b,c,d])
    return unlock_codes



# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

# numeric_keypad = [
#     [7,  8,  9],
#     [4,  5,  6],
#     [1,  2,  3],
#     [-1, 0, 66]
# ]

# numeric_keypad_width = 3
# numeric_keypad_height = 4


numeric_coords = {
    7: (0, 0),
    8: (1, 0),
    9: (2, 0),
    4: (0, 1),
    5: (1, 1),
    6: (2, 1),
    1: (0, 2),
    2: (1, 2),
    3: (2, 2),
    Digit.NONE: (0, 3),
    0: (1, 3),
    Digit.ACTIVATE: (2, 3),
}

coords_to_numeric = {pos: digit for digit, pos in numeric_coords.items()}

# ic(coords_to_numeric)

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

# directional_keypad = [
#     [ -1,             Direction.UP,   Direction.ACTIVATE ],
#     [ Direction.LEFT, Direction.DOWN, Direction.RIGHT ],
# ]

# directional_keypad_width = 3
# directional_keypad_height = 2


directional_coords = {
    Direction.NONE : (0, 0),
    Direction.UP: (1, 0),
    Direction.ACTIVATE: (2, 0),
    Direction.LEFT: (0, 1),
    Direction.DOWN: (1, 1),
    Direction.RIGHT: (2, 1),
}


coords_to_directional = {pos: direction for direction, pos in directional_coords.items()}

#
# NOTE: does not work as we cannot filter the path that go throught the missing key (-1) on the keypad
#
# def get_all_path_between_two_pos(grid: dict[Pos, Any], start: Pos, end: Pos) -> Generator[tuple[Direction]]:
#     dx = end[0] - start[0]
#     dy = end[1] - start[1]

#     required_moves = []
#     horizontal_direction = Direction.RIGHT if dx > 0 else Direction.LEFT
#     vertical_direction = Direction.DOWN if dy > 0 else Direction.UP

#     required_moves = [ horizontal_direction for x in range(abs(dx))] + [ vertical_direction for y in range(abs(dy))]
#     required_moves = set(permutations(required_moves))
#     required_moves = [list(moves) +  [ Direction.ACTIVATE ] for moves in required_moves]

#     return required_moves

KEYPAD_MISSING = -1

def get_all_path_between_two_pos(grid: dict[Pos, Any], start: Pos, end: Pos) -> list[list[Direction]]:
    sol = []
    def get_all_path_between_two_pos_rec(grid: dict[Pos, Any], start: Pos, end: Pos, r):

        if start == end:
            sol.append( r + [ Direction.ACTIVATE ])
            return

        if grid[start] == KEYPAD_MISSING:
            return 

        startx, starty = start
        endx, endy = end

        deltaX = endx - startx
        deltaY = endy - starty

        if deltaX > 0:
            next = (startx + 1, starty)
            get_all_path_between_two_pos_rec(grid, next, end, r + [ Direction.RIGHT ])
        if deltaX < 0:
            next = (startx - 1, starty)
            get_all_path_between_two_pos_rec(grid, next, end, r + [ Direction.LEFT ])
        if deltaY > 0:
            next = (startx, starty + 1)
            get_all_path_between_two_pos_rec(grid, next, end, r + [ Direction.DOWN ])
        if deltaY < 0:
            next = (startx, starty - 1)
            get_all_path_between_two_pos_rec(grid, next, end, r + [ Direction.UP ])

    get_all_path_between_two_pos_rec(grid, start, end, [])

    return sol


def direction_path_as_str(path: list[Direction]) -> str:
    return "".join([d.as_str() for d in path])


path_between_two_digits_cache = {}
# def get_all_path_between_two_digits(numeric_coords: dict[int, Pos], d1: int, d2: int, coords_to_numeric: dict[Pos, int]) -> list[list[Direction]]:
def get_all_path_between_two_digits(d1: Digit, d2: Digit) -> list[list[Direction]]:
    if (d1, d2) in path_between_two_digits_cache:
        return path_between_two_digits_cache[(d1, d2)]

    start = numeric_coords[d1]
    end = numeric_coords[d2]
    p = get_all_path_between_two_pos(coords_to_numeric, start, end)
    path_between_two_digits_cache[(d1, d2)] = p
    return p


paths_between_two_directions_cache = {}
# def get_all_path_between_two_directions(directional_coords: dict[int, Pos], d1: int, d2: int, coords_to_directional: dict[Pos, int]) -> list[list[Direction]]:
def get_all_path_between_two_directions(d1: Direction, d2: Direction) -> list[list[Direction]]:
    if (d1, d2) in paths_between_two_directions_cache:
        return paths_between_two_directions_cache[(d1, d2)]

    start = directional_coords[d1]
    end = directional_coords[d2]
    p = get_all_path_between_two_pos(coords_to_directional, start, end)
    paths_between_two_directions_cache[(d1, d2)] = p
    return p


# 379A
# ic(get_all_path_between_two_digits(Digit.ACTIVATE, Digit.THREE))

# for p in get_all_path_between_two_digits(Digit.ACTIVATE, Digit.THREE):
#     ic(direction_path_as_str(p))

# for p in get_all_path_between_two_digits(Digit.THREE, Digit.SEVEN):
#     ic(direction_path_as_str(p))

# ic(get_all_path_between_two_directions(Direction.ACTIVATE, Direction.LEFT))

# for p in get_all_path_between_two_directions(Direction.ACTIVATE, Direction.LEFT):
#     ic(direction_path_as_str(p))


min_path_for_path_on_directional_pad_cache = {}
# def get_min_path_on_directional_pad(path_to_type: list[Direction], directional_coords: dict[int, Pos], coords_to_directional: dict[Pos, int], times: int) -> tuple[int, list[Direction]]:
def get_min_path_on_directional_pad(path_to_type: list[Direction], times: int) -> tuple[int, list[Direction]]:
    path_to_type_as_tuple = tuple(path_to_type)

    if (path_to_type_as_tuple, times) in min_path_for_path_on_directional_pad_cache:
        return min_path_for_path_on_directional_pad_cache[(path_to_type_as_tuple, times)]

    if times == 0:
        min_path_for_path_on_directional_pad_cache[(path_to_type_as_tuple, times)] = len(path_to_type), path_to_type
        return len(path_to_type), path_to_type
    else:
        start_direction_key = Direction.ACTIVATE
        result_len, result_path = 0, []
        for direction_to_type in path_to_type:
            # all_possible_paths = get_all_path_between_two_directions(directional_coords, start_direction_key, direction_to_type, coords_to_directional)
            all_possible_paths = get_all_path_between_two_directions(start_direction_key, direction_to_type)

            paths = []
            for path in all_possible_paths:
                # paths.append(get_min_path_on_directional_pad(path, directional_coords, coords_to_directional, times - 1))
                paths.append(get_min_path_on_directional_pad(path, times - 1))
            min_len, min_path = min(paths)
            result_len += min_len
            # result_path.extend(min_path)
            start_direction_key = direction_to_type
        
        min_path_for_path_on_directional_pad_cache[(path_to_type_as_tuple, times)] = result_len, result_path
        return result_len, result_path


# def get_min_path_on_digitcode(numeric_coords: dict[int, Pos], coords_to_numeric: dict[Pos, int], directional_coords: dict[int, Pos], coords_to_directional: dict[Pos, int], code_digits: tuple[int], robots_count: int) -> tuple[int, list[Direction]]:
def get_min_path_on_digitcode(code_digits: DigitCode, robots_count: int) -> tuple[int, list[Direction]]:
    start_digit_key = Digit.ACTIVATE
    res = 0
    result_len, result_path = 0, []
    for digit in code_digits:
        # posible_paths_between_two_digits = get_all_path_between_two_digits(numeric_coords, start_digit_key, digit, coords_to_numeric)
        posible_paths_between_two_digits = get_all_path_between_two_digits(start_digit_key, digit)
        paths = []
        for path in posible_paths_between_two_digits:
            # paths.append(get_min_path_on_directional_pad(path, directional_coords, coords_to_directional, robots_count))
            paths.append(get_min_path_on_directional_pad(path, robots_count))
        min_len, min_path = min(paths)
        result_len += min_len
        # result_path.extend(min_path)
        start_digit_key = digit
    return result_len, result_path

# ic(get_min_path_on_digitcode(numeric_coords, coords_to_numeric, directional_coords, coords_to_directional, [0, 2, 9, 66], 2))
# ic(get_min_path_on_digitcode(numeric_coords, coords_to_numeric, directional_coords, coords_to_directional, [9, 8, 0, 66], 2))
# ic(get_min_path_on_digitcode(numeric_coords, coords_to_numeric, directional_coords, coords_to_directional, [1, 7, 8, 66], 2))
# ic(get_min_path_on_digitcode(numeric_coords, coords_to_numeric, directional_coords, coords_to_directional, [4, 5, 6, 66], 2))
# ic(get_min_path_on_digitcode(numeric_coords, coords_to_numeric, directional_coords, coords_to_directional, [3, 7, 9, 66], 2))


def complexity(code: DigitCode, robots_count: int) -> int:
    # min_path_len, min_path = get_min_path_on_digitcode(numeric_coords, coords_to_numeric, directional_coords, coords_to_directional, code, robots_count)
    min_path_len, min_path = get_min_path_on_digitcode(code, robots_count)
    n = reduce(lambda x, y: x * 10 + y, code[:-1], 0) # '980A' -> 980
    return min_path_len * n


def part1(filename: str) -> int:
    values = read_data(filename)
    return sum(complexity(code, 2) for code in values)


def part2(filename: str) -> int:
    values = read_data(filename)
    return sum(complexity(code, 25) for code in values)


assert ic(part1('sample.txt')) == 126384
assert ic(part1('input.txt')) == 248684

assert ic(part2('sample.txt')) == 154115708116294
assert ic(part2('input.txt')) == 307055584161760
