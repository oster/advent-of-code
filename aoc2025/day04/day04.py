from typing import Any
from icecream import ic


type Pos = tuple[int, int]
type Grid = dict[Pos, str]


def read_data(filename: str) -> tuple[Grid, int]:
    grid = {}
    grid_size = 0
    with open(filename, "r") as input_file:
        for y, line in enumerate(input_file.readlines()):
            grid_size += 1
            for x, c in enumerate(line.strip()):
                grid[x, y] = c
    return grid, grid_size


def print_grid(grid: Grid, grid_size: int):
    for y in range(grid_size):
        for x in range(grid_size):
            print(f"{grid.get((x, y), ' '):2}", end="")
        print()
    print()


def eight_directions() -> list[Pos]:
    return [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]


def part1(filename: str) -> int:
    grid, size = read_data(filename)

    count = 0
    for (x, y), c in grid.items():
        if c != "@":
            continue

        adjacent_rolls = 0

        for direction in eight_directions():
            nx = x + direction[0]
            ny = y + direction[1]

            if nx >= 0 and nx < size and ny >= 0 and ny < size:
                if grid.get((nx, ny)) == "@":
                    adjacent_rolls += 1

        if adjacent_rolls < 4:
            count += 1

    return count


def part2(filename: str) -> int:
    grid, size = read_data(filename)

    count = 0
    changed = True
    while changed:
        changed = False

        grid_copy = grid.copy()

        for (x, y), c in grid.items():
            if c != "@":
                continue

            adjacent_rolls = 0

            for direction in eight_directions():
                nx = x + direction[0]
                ny = y + direction[1]

                if nx >= 0 and nx < size and ny >= 0 and ny < size:
                    if grid.get((nx, ny)) == "@":
                        adjacent_rolls += 1

            if adjacent_rolls < 4:
                count += 1
                grid_copy[(x, y)] = "."
                changed = True

        grid = grid_copy

    return count


# ic.disable()

assert ic(part1("./sample.txt")) == 13
assert ic(part1("./input.txt")) == 1474

assert ic(part2("./sample.txt")) == 43
assert ic(part2("./input.txt")) == 8910
