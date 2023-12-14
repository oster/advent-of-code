import sys
from typing import Any
from functools import reduce


def read_input(filename: str) -> list[list[str]]:
    data = []
    with open(filename, "r") as input_file:
        for line in input_file.readlines():
            data.append(list(line.rstrip()))
            # data.append(line.rstrip())

    return data


def print_grid(grid: list[list[Any]]):
    for line in grid:
        for val in line:
            print(f"{val:2}", end="")
        print()
    print()


def die(msg: str):
    raise Exception(msg)


def compute_sum_section(round_rocks, last_square_rock_y, height) -> int:
    if round_rocks == 0:
        return 0

    i = height - (last_square_rock_y + round_rocks)
    # Σ k for k [i,i+r[
    return round_rocks * (2 * i + round_rocks - 1) // 2


def part1(filename: str) -> int:
    data = read_input(filename)
    width = len(data[0])
    height = len(data)

    sum_values = 0
    for x in range(width):
        round_rocks = 0
        last_square_rock_y = -1

        sum_column = 0
        for y in range(height):
            match data[y][x]:
                case "O":
                    round_rocks += 1
                case "#":
                    sum_column += compute_sum_section(
                        round_rocks, last_square_rock_y, height
                    )
                    round_rocks = 0
                    last_square_rock_y = y
                case ".":
                    pass
                case _:
                    die("Invalid character.")
        sum_column += compute_sum_section(round_rocks, last_square_rock_y, height)
        sum_values += sum_column

    return sum_values


def tilted_column_north(tilted, x, y, last_square_rock_y, round_rocks):
    i = last_square_rock_y + 1
    for k in range(i, i + round_rocks):
        tilted[k][x] = "O"

    if last_square_rock_y != -1:
        tilted[last_square_rock_y][x] = "#"


def tilted_grid_north(tilted, grid, width, height):
    for x in range(width):
        round_rocks = 0
        last_square_rock_y = -1

        for y in range(height):
            match grid[y][x]:
                case "O":
                    round_rocks += 1
                case "#":
                    tilted_column_north(tilted, x, y, last_square_rock_y, round_rocks)
                    round_rocks = 0
                    last_square_rock_y = y
                case ".":
                    pass
                case _:
                    die("Invalid character.")
        tilted_column_north(tilted, x, height, last_square_rock_y, round_rocks)


def compute_sum_grid(data) -> int:
    width = len(data[0])
    height = len(data)

    sum = reduce(
        lambda acc, v: acc + v,
        (data[y].count("O") * (height - y) for y in range(height)),
    )

    return sum


def part1_alt(filename: str) -> int:
    grid = read_input(filename)
    width = len(grid[0])
    height = len(grid)

    tilted = [["."] * width for _ in range(height)]

    tilted_grid_north(tilted, grid, width, height)

    return compute_sum_grid(tilted)


def reverse_lines(grid):
    size = len(grid)
    for i in range(size):
        j = 0
        k = size - 1
        while j < k:
            t = grid[i][j]
            grid[i][j] = grid[i][k]
            grid[i][k] = t
            j += 1
            k -= 1


def reverse_columns(grid):
    size = len(grid)
    for i in range(size):
        j = 0
        k = size - 1
        while j < k:
            t = grid[j][i]
            grid[j][i] = grid[k][i]
            grid[k][i] = t
            j += 1
            k -= 1


def transpose(grid):
    size = len(grid)
    for i in range(size):
        for j in range(i, size):
            t = grid[i][j]
            grid[i][j] = grid[j][i]
            grid[j][i] = t


def rotate_clockwise_90(grid):
    transpose(grid)
    reverse_lines(grid)
    return grid


def rotate_anti_clockwise_90(grid):
    transpose(grid)
    reverse_columns(grid)
    return grid


def rotate_clockwise_90_inplace(grid):
    size = len(grid[0])
    for i in range(size // 2):
        for j in range(i, size - i - 1):
            temp = grid[i][j]
            grid[i][j] = grid[size - 1 - j][i]
            grid[size - 1 - j][i] = grid[size - 1 - i][size - 1 - j]
            grid[size - 1 - i][size - 1 - j] = grid[j][size - 1 - i]
            grid[j][size - 1 - i] = temp
    return grid


def part2(filename: str) -> int:
    grid = read_input(filename)
    size = len(grid)

    sums_of_cycle = [0] * 4  # 4-uplet to store the sums of each rotation during a cycle
    sums_at_cycle = {}

    cycle = 0
    jumped = False
    while cycle <= 1000000000:
        for rotation in range(4):  # 4 rotations
            tilted = [["."] * size for _ in range(size)]
            tilted_grid_north(tilted, grid, size, size)
            grid = rotate_clockwise_90_inplace(tilted)
            sums_of_cycle[rotation] = compute_sum_grid(grid)

        # print(f"cycle {cycle:3}: {tuple(sums_of_cycle)}")
        key = tuple(sums_of_cycle)
        if not key in sums_at_cycle:
            sums_at_cycle[key] = cycle
        else:
            # print(f">> cycle {cycle:3} ({sums_of_cycle}) already seen at {sums_at_cycle[key]}")
            if not jumped:
                cycle_start = sums_at_cycle[key]
                cycle_length = cycle - sums_at_cycle[key]
                cycle_to_found = cycle_start + (1000000000 - 1 - cycle) % cycle_length
                key = (
                    sum_cycle
                    for sum_cycle, id_cycle in sums_at_cycle.items()
                    if id_cycle == cycle_to_found
                ).__next__()
                return key[3]

                # jumped = True
                # cycle_length = cycle - sums_at_cycle[key]
                # jumps_count = (1000000000 - cycle) // cycle_length
                # target_cycle = cycle + jumps_count * cycle_length
                # # print(f">> jumping to cycle {target_cycle} ({cycle} + {jumps_count} x {cycle_length})")
                # cycle = target_cycle + 1

        cycle += 1

    return compute_sum_grid(grid)



assert part1("./sample.txt") == 136
assert part1("./sample2.txt") == 145
assert part1("./input.txt") == 113078

assert part1_alt("./sample.txt") == 136
assert part1_alt("./sample2.txt") == 145
assert part1_alt("./input.txt") == 113078

assert part2("./sample.txt") == 64
assert part2("./input.txt") == 94255


import timeit
time_p1 = timeit.timeit(lambda: part1("./input.txt"), number=100)
print("Time part 1 (mean time over 100 runs):", time_p1 / 100)

time_p2 = timeit.timeit(lambda: part2("./input.txt"), number=10)
print("Time part 2 (mean time over 10 runs):", time_p2 / 10)
