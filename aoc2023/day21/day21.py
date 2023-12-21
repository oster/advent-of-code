from collections import deque
from typing import Any


def die(msg: str):
    raise Exception(msg)


def print_grid(grid: list[list[Any]]):
    for line in grid:
        for val in line:
            print(f"{val:2}", end="")
        print()
    print()


def read_input(filename: str) -> tuple[list[list[str]], tuple[int, int]]:
    data = []
    start = (0, 0)
    with open(filename, "r") as input_file:
        for line in input_file.readlines():
            row = list(line.rstrip())
            data.append(row)
            if "S" in row:
                start = (row.index("S"), len(data) - 1)

    return data, start


def neighbors(current: tuple[int, int], grid: list[list[str]]) -> set[tuple[int, int]]:
    size = len(grid)
    x, y = current

    next_positions = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    next_positions = filter(
        lambda pos: pos[0] >= 0 and pos[0] < size and pos[1] >= 0 and pos[1] < size,
        next_positions,
    )
    next_positions = filter(lambda pos: grid[pos[1]][pos[0]] != "#", next_positions)

    return set(next_positions)


def part1(filename: str, max_step: int) -> int:
    grid, start = read_input(filename)

    states = deque()
    states.append((0, [start]))

    while states:
        step, nodes = states.popleft()

        if step >= max_step:
            return len(nodes)

        neighbors_for_step = set()
        for node in nodes:
            for n in neighbors(node, grid):
                neighbors_for_step.add(n)

        states.append((step + 1, neighbors_for_step))
    return -1


assert part1("./sample.txt", 6) == 16
assert part1("./input.txt", 64) == 3830
