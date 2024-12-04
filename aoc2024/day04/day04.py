from typing import Generator
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


def die(msg: str):
    raise Exception(msg)


def print_grid(grid: Grid, grid_size: int):
    for y in range(grid_size):
        for x in range(grid_size):
            print(f"{grid.get((x, y), ' '):2}", end="")
        print()
    print()


def print_remaining_grid(grid: Grid, mask: Grid, grid_size: int):
    for y in range(grid_size):
        for x in range(grid_size):
            if mask.get((x, y)) == ".":
                print(f"{grid.get((x, y)):2}", end="")
            else:
                print(f"  ", end="")
        print()
    print()


def part1(filename: str) -> int:
    grid, size = read_data(filename)

    count = 0
    for y in range(size):
        for x in range(size):
            count += find_xmas(grid, size, x, y)

    return count


def eight_directions() -> list[Pos]:
    return [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]


def find_xmas(grid: Grid, size: int, x: int, y: int) -> int:
    xmas = "XMAS"

    # count = 0
    # for direction in eight_directions():
    #     if all(
    #         grid.get((x + k * direction[0], y + k * direction[1])) == xmas[k]
    #         for k in range(len(xmas))
    #     ):
    #         count += 1
    # return count

    return sum(
        (
            all(
                (
                    grid.get((x + k * direction[0], y + k * direction[1])) == xmas[k]
                    for k in range(len(xmas))
                )
            )
            for direction in eight_directions()
        )
    )


def find_mas_cross(grid: Grid, size: int, x: int, y: int) -> bool:
    return (
        (
            grid.get((x - 1, y - 1)) == "M"
            and grid.get((x, y)) == "A"
            and grid.get((x + 1, y + 1)) == "S"
            and grid.get((x - 1, y + 1)) == "M"
            and grid.get((x + 1, y - 1)) == "S"
        )
        or (
            grid.get((x - 1, y - 1)) == "M"
            and grid.get((x, y)) == "A"
            and grid.get((x + 1, y + 1)) == "S"
            and grid.get((x - 1, y + 1)) == "S"
            and grid.get((x + 1, y - 1)) == "M"
        )
        or (
            grid.get((x - 1, y - 1)) == "S"
            and grid.get((x, y)) == "A"
            and grid.get((x + 1, y + 1)) == "M"
            and grid.get((x - 1, y + 1)) == "S"
            and grid.get((x + 1, y - 1)) == "M"
        )
        or (
            grid.get((x - 1, y - 1)) == "S"
            and grid.get((x, y)) == "A"
            and grid.get((x + 1, y + 1)) == "M"
            and grid.get((x - 1, y + 1)) == "M"
            and grid.get((x + 1, y - 1)) == "S"
        )
    )


def part2(filename: str) -> int:
    grid, size = read_data(filename)

    # count = 0
    # for y in range(size):
    #     for x in range(size):
    #         count += find_mas_cross(grid, size, x, y)
    # return count

    return sum(
        (
            find_mas_cross(grid, size, x, y)
            for y in range(size)
            for x in range(size)
        )
    )


# ic.disable()

assert ic(part1("./sample.txt")) == 18
assert ic(part1("./input.txt")) == 2530

assert ic(part2("./sample.txt")) == 9
assert ic(part2("./input.txt")) == 1921
